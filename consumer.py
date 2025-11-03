#!/usr/bin/env python3
"""
Consumer para el ejercicio de las 4 Vs del Big Data
Lee y procesa datos mostrando tiempos de ejecución
"""

import argparse
import time
import json
import csv
import glob
from pathlib import Path
from collections import defaultdict
try:
    import matplotlib
    matplotlib.use('Agg')  # Backend sin GUI para generar archivos
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  matplotlib no está disponible. Las gráficas no se generarán.")
    print("   Instala con: pip install matplotlib seaborn numpy")

class BigDataConsumer:
    def __init__(self, velocity=False, volume=False, variety=False, veracity=False):
        self.velocity = velocity
        self.volume = volume
        self.variety = variety
        self.veracity = veracity
        self.data_folder = Path("data")
        self.output_folder = "."  # Carpeta donde se guardan las gráficas (directorio actual)
        
        # Contador para mostrar solo cuando hay cambios significativos
        self.last_file_sizes = {}
        
        # Para velocity: trackear cuántos números ya hemos procesado
        self.processed_count = 0
        
        # Para generar gráficas: recopilar datos de rendimiento
        self.performance_data = {
            'iterations': [],
            'processing_times': [],
            'numbers_in_file': [],
            'numbers_processed': [],
            'total_numbers_processed': [],
            'veracity_errors': []
        }

    def read_txt_file(self, filepath):
        """Lee números de un archivo TXT"""
        numbers = []
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        numbers.append(int(line))
        except (ValueError, FileNotFoundError):
            pass
        return numbers

    def read_csv_file(self, filepath):
        """Lee números de un archivo CSV"""
        numbers = []
        try:
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header
                for row in reader:
                    if row:
                        numbers.append(int(row[0]))
        except (ValueError, FileNotFoundError, IndexError):
            pass
        return numbers

    def read_json_file(self, filepath):
        """Lee números de un archivo JSON"""
        numbers = []
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                if 'numbers' in data:
                    numbers = data['numbers']
        except (json.JSONDecodeError, FileNotFoundError, KeyError):
            pass
        return numbers

    def get_file_numbers(self, filepath):
        """Obtiene números de un archivo según su extensión"""
        path = Path(filepath)
        
        if path.suffix == '.txt':
            return self.read_txt_file(filepath)
        elif path.suffix == '.csv':
            return self.read_csv_file(filepath)
        elif path.suffix == '.json':
            return self.read_json_file(filepath)
        
        return []

    def get_next_number_for_velocity(self, filepath):
        """Para velocity: obtiene solo el siguiente número no procesado"""
        numbers = self.get_file_numbers(filepath)
        
        # Si hay números nuevos más allá de los ya procesados
        if len(numbers) > self.processed_count:
            # Devolver solo el siguiente número
            next_number = numbers[self.processed_count]
            self.processed_count += 1
            return [next_number], len(numbers)  # [número], total_en_archivo
        
        return [], len(numbers)  # Sin números nuevos

    def _generate_chart_filename(self):
        """Genera el nombre del archivo basado en las V's activadas"""
        v_names = []
        if self.velocity: v_names.append('vel')
        if self.volume: v_names.append('vol')
        if self.variety: v_names.append('var')
        if self.veracity: v_names.append('ver')
        
        # Unir con guiones y añadir extensión
        if v_names:
            return f"{'_'.join(v_names)}.png"
        else:
            return "demo.png"  # Fallback por si no hay ninguna V activada

    def _cleanup_data_folder(self):
        """Limpia la carpeta data después de generar la gráfica"""
        try:
            from pathlib import Path
            import shutil
            
            data_folder = Path("data")
            if data_folder.exists():
                # Contar archivos antes de limpiar
                files_before = list(data_folder.rglob("*"))
                file_count = len([f for f in files_before if f.is_file()])
                
                if file_count > 0:
                    shutil.rmtree(data_folder)
                    data_folder.mkdir(exist_ok=True)
                    print(f"🧹 Carpeta data limpiada ({file_count} archivos eliminados)")
                else:
                    print("📁 Carpeta data ya estaba vacía")
            else:
                print("📁 Carpeta data no existe")
                
        except Exception as e:
            print(f"⚠️  Error limpiando carpeta data: {e}")

    def generate_performance_chart(self):
        """Genera gráfica de rendimiento al finalizar"""
        if not MATPLOTLIB_AVAILABLE:
            print("📊 Gráficas no disponibles (matplotlib no instalado)")
            return
            
        if not self.performance_data['iterations']:
            print("⚠️  No hay datos de rendimiento para generar gráfica")
            return
            
        print(f"📊 Generando gráfica con {len(self.performance_data['iterations'])} puntos de datos...")
        
        # Deshabilitar interrupciones durante TODO el proceso de generación
        import signal
        import os
        old_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
        
        try:
            # Configurar el estilo de la gráfica
            try:
                plt.style.use('seaborn-v0_8')
            except:
                plt.style.use('seaborn')
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
            iterations = self.performance_data['iterations']
            times = self.performance_data['processing_times']
            numbers_in_file = self.performance_data['numbers_in_file']
            numbers_processed = self.performance_data['numbers_processed']
            total_processed = self.performance_data['total_numbers_processed']
            
            # Gráfica 1: Tiempo de procesamiento por iteración
            ax1.plot(iterations, times, 'b-o', linewidth=2, markersize=4)
            ax1.set_title('Tiempo de Procesamiento por Iteración', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Iteración')
            ax1.set_ylabel('Tiempo (ms)')
            ax1.grid(True, alpha=0.3)
            ax1.set_facecolor('#f8f9fa')
            
            # Gráfica 2: Números en archivo vs Números procesados
            ax2.plot(iterations, numbers_in_file, 'r-s', label='Números en Archivo', linewidth=2, markersize=4)
            ax2.plot(iterations, total_processed, 'g-^', label='Total Procesados', linewidth=2, markersize=4)
            ax2.set_title('Volumen: Archivo vs Procesados', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Iteración')
            ax2.set_ylabel('Cantidad de Números')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.set_facecolor('#f8f9fa')
            
            # Gráfica 3: Retraso (solo para velocity)
            if self.velocity:
                delay = [nf - tp for nf, tp in zip(numbers_in_file, total_processed)]
                ax3.plot(iterations, delay, 'orange', linewidth=3, marker='d', markersize=5)
                ax3.fill_between(iterations, delay, alpha=0.3, color='orange')
                ax3.set_title('Retraso Creciente (Velocity)', fontsize=14, fontweight='bold')
                ax3.set_xlabel('Iteración')
                ax3.set_ylabel('Números de Retraso')
                ax3.grid(True, alpha=0.3)
                ax3.set_facecolor('#fff3cd')
            else:
                # Para volume: mostrar escalabilidad
                if len(times) > 1 and max(numbers_in_file) > min(numbers_in_file):
                    ax3.scatter(numbers_in_file, times, c=iterations, cmap='viridis', s=50, alpha=0.7)
                    ax3.set_title('Escalabilidad: Volumen vs Tiempo', fontsize=14, fontweight='bold')
                    ax3.set_xlabel('Números en Archivo')
                    ax3.set_ylabel('Tiempo de Procesamiento (ms)')
                    cbar = plt.colorbar(ax3.scatter(numbers_in_file, times, c=iterations, cmap='viridis', s=50, alpha=0.7), ax=ax3)
                    cbar.set_label('Iteración')
                    ax3.grid(True, alpha=0.3)
                    ax3.set_facecolor('#e8f5e8')
                else:
                    ax3.text(0.5, 0.5, 'Datos insuficientes\npara análisis de escalabilidad', 
                            ha='center', va='center', transform=ax3.transAxes, fontsize=12)
                    ax3.set_title('Escalabilidad: Volumen vs Tiempo', fontsize=14, fontweight='bold')
            
            # Gráfico 4: Veracity - Errores detectados
            ax4.bar(range(len(self.performance_data['veracity_errors'])), 
                   self.performance_data['veracity_errors'],
                   color='red', alpha=0.7)
            ax4.set_title("Veracity: Errores detectados por iteración")
            ax4.set_xlabel("Iteración")
            ax4.set_ylabel("Número de errores")
            
            plt.tight_layout()
            
            # Generar nombre de archivo basado en las Vs activadas
            filename = self._generate_chart_filename()
            filepath = os.path.join(self.output_folder, filename)
            
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"📈 Gráfica guardada como: {filename}")
            
            # Limpiar datos después de generar la gráfica
            self._cleanup_data_folder()
            
            # Configurar título general
            mode_names = []
            if self.velocity: mode_names.append('Velocity')
            if self.volume: mode_names.append('Volume')  
            if self.variety: mode_names.append('Variety')
            if self.veracity: mode_names.append('Veracity')
            
            title = f"Análisis de Rendimiento - {' + '.join(mode_names)}"
            fig.suptitle(title, fontsize=16, fontweight='bold')
            
        except Exception as e:
            print(f"❌ Error durante la generación de gráfica: {e}")
        finally:
            # Restaurar el handler original de señales SIEMPRE
            signal.signal(signal.SIGINT, old_handler)
            # Cerrar la figura para liberar memoria
            try:
                plt.close()
            except:
                pass
            
        print(f"✅ Gráfica generada exitosamente")
        
        # Mostrar estadísticas finales
        if self.performance_data['processing_times']:
            times = self.performance_data['processing_times']
            iterations = self.performance_data['iterations']
            numbers_in_file = self.performance_data['numbers_in_file']
            total_processed = self.performance_data['total_numbers_processed']
            
            print(f"\n📈 ESTADÍSTICAS FINALES:")
            print(f"   Iteraciones totales: {len(iterations)}")
            print(f"   Tiempo promedio: {np.mean(times):.2f} ms")
            print(f"   Tiempo máximo: {max(times):.2f} ms")
            print(f"   Tiempo mínimo: {min(times):.2f} ms")
            if self.velocity and len(numbers_in_file) > 0 and len(total_processed) > 0:
                final_delay = numbers_in_file[-1] - total_processed[-1]
                print(f"   Retraso final: {final_delay} números")
            if len(numbers_in_file) > 0:
                print(f"   Volumen máximo: {max(numbers_in_file)} números")

    def find_files_to_process(self):
        """Encuentra archivos existentes para procesar"""
        all_files = []
        
        if self.variety:
            # Buscar múltiples formatos con nombres fijos
            filenames = ['data.txt', 'data.csv', 'data.json']
            for filename in filenames:
                filepath = self.data_folder / filename
                if filepath.exists():
                    all_files.append(str(filepath))
        else:
            # Solo TXT por defecto
            filepath = self.data_folder / 'data.txt'
            if filepath.exists():
                all_files.append(str(filepath))
        
        return all_files

    def process_files(self):
        """Procesa todos los archivos disponibles"""
        start_time = time.time()
        
        files_to_process = self.find_files_to_process()
        
        if not files_to_process:
            return None
        
        # Para velocity: verificar si hay números nuevos que procesar
        if self.velocity:
            # En velocity, verificamos si hay más números que los ya procesados
            for filepath in files_to_process:
                numbers = self.get_file_numbers(filepath)
                if len(numbers) > self.processed_count:
                    # Hay números nuevos para procesar
                    break
            else:
                # No hay números nuevos
                return None
        else:
            # Para otros modos: verificar cambios en tamaño de archivos
            current_sizes = {}
            has_changes = False
            
            for filepath in files_to_process:
                try:
                    size = Path(filepath).stat().st_size
                    current_sizes[filepath] = size
                    if filepath not in self.last_file_sizes or self.last_file_sizes[filepath] != size:
                        has_changes = True
                except:
                    current_sizes[filepath] = 0
            
            # Si no hay cambios, no procesar
            if not has_changes and self.last_file_sizes:
                return None
            
            # Actualizar tamaños
            self.last_file_sizes = current_sizes.copy()
        
        if self.variety and self.velocity:
            # Variety + Velocity: procesar un número de cada formato
            results_by_type = defaultdict(lambda: {'sum': 0, 'count': 0, 'files': [], 'total_in_file': 0})
            
            has_new_numbers = False
            for filepath in files_to_process:
                # Para velocity: obtener solo el siguiente número sin procesar
                new_numbers, total_in_file = self.get_next_number_for_velocity(filepath)
                file_type = Path(filepath).suffix
                
                if new_numbers:
                    has_new_numbers = True
                    file_sum = new_numbers[0]  # Solo el número nuevo
                    results_by_type[file_type]['sum'] = file_sum
                    results_by_type[file_type]['count'] = 1
                    results_by_type[file_type]['files'] = [Path(filepath).name]
                    results_by_type[file_type]['total_in_file'] = total_in_file
            
            if not has_new_numbers:
                return None
            
            end_time = time.time()
            processing_time = (end_time - start_time) * 1000
            
            print(f"\n⏱️  Tiempo de procesamiento: {processing_time:.2f} ms")
            print(f"📁 Archivos procesados: {len(files_to_process)}")
            
            # Mostrar resultados por tipo
            total_in_all_files = 0
            for file_type, data in results_by_type.items():
                print(f"   {file_type}: Número procesado={data['sum']}, "
                      f"Total en archivo={data['total_in_file']}")
                total_in_all_files = max(total_in_all_files, data['total_in_file'])
            
            print(f"🔢 Número procesado de cada formato")
            print(f"📊 Total procesados hasta ahora: {self.processed_count}")
            
            # Detectar discrepancias si veracity está activo
            errors_detected = 0
            if self.veracity and len(results_by_type) > 1:
                sums = [data['sum'] for data in results_by_type.values()]
                if len(set(sums)) > 1:
                    errors_detected = 1
                    print(f"⚠️  DISCREPANCIA DETECTADA: Los números no coinciden entre formatos")
            
            # Recopilar datos para gráfica (variety + velocity)
            if len(self.performance_data['iterations']) == 0:
                iteration = 0
            else:
                iteration = self.performance_data['iterations'][-1] + 1
            
            self.performance_data['iterations'].append(iteration)
            self.performance_data['processing_times'].append(processing_time)
            self.performance_data['numbers_in_file'].append(total_in_all_files)
            self.performance_data['numbers_processed'].append(1)  # Solo 1 por iteración en velocity
            self.performance_data['total_numbers_processed'].append(self.processed_count)
            self.performance_data['veracity_errors'].append(errors_detected)
            
            return processing_time
            
        elif self.variety:
            # Variety sin velocity: procesar todos los números
            results_by_type = defaultdict(lambda: {'sum': 0, 'count': 0, 'files': []})
            
            for filepath in files_to_process:
                numbers = self.get_file_numbers(filepath)
                if numbers:
                    file_sum = sum(numbers)
                    file_type = Path(filepath).suffix
                    
                    results_by_type[file_type]['sum'] = file_sum  # Cambio: asignar en lugar de sumar
                    results_by_type[file_type]['count'] = len(numbers)  # Total actual
                    results_by_type[file_type]['files'] = [Path(filepath).name]
            
            end_time = time.time()
            processing_time = (end_time - start_time) * 1000
            
            print(f"\n⏱️  Tiempo de procesamiento: {processing_time:.2f} ms")
            print(f"📁 Archivos procesados: {len(files_to_process)}")
            
            # Mostrar resultados por tipo
            total_numbers_variety = 0
            for file_type, data in results_by_type.items():
                print(f"   {file_type}: Suma={data['sum']}, "
                      f"Números={data['count']}, "
                      f"Archivos={len(data['files'])}")
                if data['count'] > total_numbers_variety:
                    total_numbers_variety = data['count']  # Usar el máximo
            
            # Detectar discrepancias si veracity está activo
            errors_detected = 0
            if self.veracity and len(results_by_type) > 1:
                sums = [data['sum'] for data in results_by_type.values()]
                if len(set(sums)) > 1:
                    errors_detected = 1
                    print(f"⚠️  DISCREPANCIA DETECTADA: Las sumas no coinciden entre formatos")
            
            # Recopilar datos para gráfica (variety/veracity)
            if len(self.performance_data['iterations']) == 0:
                iteration = 0
            else:
                iteration = self.performance_data['iterations'][-1] + 1
            
            self.performance_data['iterations'].append(iteration)
            self.performance_data['processing_times'].append(processing_time)
            self.performance_data['numbers_in_file'].append(total_numbers_variety)
            self.performance_data['numbers_processed'].append(total_numbers_variety)
            self.performance_data['total_numbers_processed'].append(total_numbers_variety)
            self.performance_data['veracity_errors'].append(errors_detected)
            
            return processing_time
            
        elif self.velocity:
            # Velocity sin variety: procesar solo UN número nuevo por vez
            for filepath in files_to_process:
                new_numbers, total_in_file = self.get_next_number_for_velocity(filepath)
                
                if new_numbers:
                    end_time = time.time()
                    processing_time = (end_time - start_time) * 1000
                    
                    number_processed = new_numbers[0]
                    print(f"\n⏱️  Tiempo de procesamiento: {processing_time:.2f} ms")
                    print(f"📄 {Path(filepath).name}: {total_in_file} números en el archivo")
                    print(f"🔢 Número procesado: {number_processed}")
                    print(f"📊 Total procesados hasta ahora: {self.processed_count}")
                    
                    # Recopilar datos para gráfica (solo en velocity)
                    if len(self.performance_data['iterations']) == 0:
                        iteration = 0
                    else:
                        iteration = self.performance_data['iterations'][-1] + 1
                    
                    self.performance_data['iterations'].append(iteration)
                    self.performance_data['processing_times'].append(processing_time)
                    self.performance_data['numbers_in_file'].append(total_in_file)
                    self.performance_data['numbers_processed'].append(1)  # Siempre 1 en velocity
                    self.performance_data['total_numbers_processed'].append(self.processed_count)
                    self.performance_data['veracity_errors'].append(0)  # No hay errores en velocity puro
                    
                    return processing_time
            
            # No hay números nuevos
            return None
            
        else:
            # Volume u otros: procesar todos los números
            total_sum = 0
            total_numbers = 0
            
            for filepath in files_to_process:
                numbers = self.get_file_numbers(filepath)
                if numbers:
                    total_sum = sum(numbers)  # Total actual en el archivo
                    total_numbers = len(numbers)  # Cantidad actual
            
            end_time = time.time()
            processing_time = (end_time - start_time) * 1000
            
            print(f"\n⏱️  Tiempo de procesamiento: {processing_time:.2f} ms")
            print(f"📁 Archivos procesados: {len(files_to_process)}")
            print(f"🔢 Suma total: {total_sum}")
            print(f"📊 Números totales procesados: {total_numbers}")
            
            # Recopilar datos para gráfica (volume, etc)
            if len(self.performance_data['iterations']) == 0:
                iteration = 0
            else:
                iteration = self.performance_data['iterations'][-1] + 1
            
            self.performance_data['iterations'].append(iteration)
            self.performance_data['processing_times'].append(processing_time)
            self.performance_data['numbers_in_file'].append(total_numbers)
            self.performance_data['numbers_processed'].append(total_numbers)
            self.performance_data['total_numbers_processed'].append(total_numbers)
            self.performance_data['veracity_errors'].append(0)  # No hay errores en volume puro
            
            return processing_time

    def run(self):
        """Ejecuta el consumer continuamente"""
        print("🔍 Consumer iniciado...")
        print(f"   Velocity: {self.velocity}")
        print(f"   Volume: {self.volume}")
        print(f"   Variety: {self.variety}")
        print(f"   Veracity: {self.veracity}")
        print("-" * 50)
        
        iteration = 0
        
        try:
            while True:
                print(f"\n📋 Iteración {iteration}:")
                
                processing_time = self.process_files()
                
                if processing_time is None:
                    print("   ⏳ No hay archivos nuevos para procesar...")
                
                time.sleep(1)  # Intervalo de lectura
                iteration += 1
                
        except KeyboardInterrupt:
            print(f"\n🛑 Consumer detenido después de {iteration} iteraciones")
            
            # Generar gráfica de rendimiento
            print("\n📊 Generando gráfica de rendimiento...")
            try:
                self.generate_performance_chart()
            except Exception as e:
                print(f"⚠️  Error generando gráfica: {e}")
                print("Asegúrate de tener matplotlib instalado: pip install matplotlib")

def main():
    parser = argparse.ArgumentParser(description="Consumer para Big Data")
    parser.add_argument("--velocity", type=str, default="false")
    parser.add_argument("--volume", type=str, default="false")
    parser.add_argument("--variety", type=str, default="false")
    parser.add_argument("--veracity", type=str, default="false")
    
    args = parser.parse_args()
    
    # Convertir a booleans
    velocity = args.velocity.lower() == "true"
    volume = args.volume.lower() == "true"
    variety = args.variety.lower() == "true"
    veracity = args.veracity.lower() == "true"
    
    consumer = BigDataConsumer(velocity, volume, variety, veracity)
    consumer.run()

if __name__ == "__main__":
    main()
