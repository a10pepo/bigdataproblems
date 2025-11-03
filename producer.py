#!/usr/bin/env python3
"""
Producer para el ejercicio de las 4 Vs del Big Data
Genera datos según los parámetros especificados
"""

import argparse
import time
import json
import csv
import random
from pathlib import Path
from datetime import datetime

class BigDataProducer:
    def __init__(self, velocity=False, volume=False, variety=False, veracity=False):
        self.velocity = velocity
        self.volume = volume
        self.variety = variety
        self.veracity = veracity
        self.data_folder = Path("data")
        self.data_folder.mkdir(exist_ok=True)
        
        # Contadores y configuraciones
        self.iteration = 0
        self.sleep_time = 2.0  # Para velocity
        self.numbers_count = 1  # Para volume
        self.current_number = 1
        
        # Para veracity: introducir errores ocasionalmente
        self.error_probability = 0.1

    def generate_number(self):
        """Genera el próximo número en secuencia"""
        number = self.current_number
        self.current_number += 1
        return number

    def introduce_error(self, number):
        """Para veracity: introduce errores ocasionalmente"""
        if self.veracity and random.random() < self.error_probability:
            # Introducir diferentes tipos de errores
            error_type = random.choice(['multiply', 'add', 'negative'])
            if error_type == 'multiply':
                return number * 10
            elif error_type == 'add':
                return number + 1000
            else:
                return -number
        return number

    def write_txt_file(self, numbers):
        """Escribe números en archivo TXT"""
        filename = self.data_folder / "data.txt"
        with open(filename, 'a') as f:  # 'a' para append
            for num in numbers:
                f.write(f"{num}\n")

    def write_csv_file(self, numbers):
        """Escribe números en archivo CSV"""
        filename = self.data_folder / "data.csv"
        # Verificar si el archivo existe para escribir header solo una vez
        file_exists = filename.exists()
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['number'])  # Header solo si es nuevo
            for num in numbers:
                writer.writerow([num])

    def write_json_file(self, numbers):
        """Escribe números en archivo JSON"""
        filename = self.data_folder / "data.json"
        
        # Leer datos existentes si el archivo existe
        existing_numbers = []
        if filename.exists():
            try:
                with open(filename, 'r') as f:
                    existing_data = json.load(f)
                    if 'numbers' in existing_data:
                        existing_numbers = existing_data['numbers']
            except (json.JSONDecodeError, KeyError):
                existing_numbers = []
        
        # Añadir nuevos números
        all_numbers = existing_numbers + numbers
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'iteration': self.iteration,
            'numbers': all_numbers
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def produce_data(self):
        """Produce datos según las configuraciones activas"""
        
        # Determinar cuántos números generar
        if self.volume:
            # Volume: incrementar cantidad de forma exponencial cada 2 iteraciones
            if self.iteration > 0 and self.iteration % 2 == 0:
                # Crecimiento exponencial: 1, 10, 100, 500, 1000, 2500, 5000, 10000...
                growth_factor = (self.iteration // 2) + 1
                if growth_factor <= 2:
                    self.numbers_count = growth_factor * 10  # 10, 20
                elif growth_factor <= 4:
                    self.numbers_count = growth_factor * 50   # 150, 200
                elif growth_factor <= 6:
                    self.numbers_count = growth_factor * 200  # 1000, 1200
                else:
                    self.numbers_count = growth_factor * 500  # 3500, 4000, 4500...
        
        # Generar números
        numbers = []
        for _ in range(self.numbers_count):
            base_number = self.generate_number()
            numbers.append(base_number)
        
        # Escribir según variety
        if self.variety:
            # Escribir en múltiples formatos
            # TXT - números normales
            txt_numbers = [self.introduce_error(num) for num in numbers.copy()]
            self.write_txt_file(txt_numbers)
            
            # CSV - números normales
            csv_numbers = [self.introduce_error(num) for num in numbers.copy()]
            self.write_csv_file(csv_numbers)
            
            # JSON - números normales
            json_numbers = [self.introduce_error(num) for num in numbers.copy()]
            self.write_json_file(json_numbers)
            
        else:
            # Solo escribir en TXT por defecto
            final_numbers = [self.introduce_error(num) for num in numbers]
            self.write_txt_file(final_numbers)
        
        print(f"📝 Iteración {self.iteration}: Generados {len(numbers)} números "
              f"(Sleep: {self.sleep_time:.1f}s)")

    def run(self):
        """Ejecuta el producer continuamente"""
        print("🏭 Producer iniciado...")
        print(f"   Velocity: {self.velocity}")
        print(f"   Volume: {self.volume}")
        print(f"   Variety: {self.variety}")
        print(f"   Veracity: {self.veracity}")
        
        try:
            while True:
                self.produce_data()
                
                # Velocity: reducir sleep time cada 2 iteraciones
                if self.velocity and self.iteration > 0 and self.iteration % 2 == 0:
                    self.sleep_time = max(0.1, self.sleep_time - 0.2)
                
                time.sleep(self.sleep_time)
                self.iteration += 1
                
        except KeyboardInterrupt:
            print("\n🛑 Producer detenido")

def main():
    parser = argparse.ArgumentParser(description="Producer para Big Data")
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
    
    producer = BigDataProducer(velocity, volume, variety, veracity)
    producer.run()

if __name__ == "__main__":
    main()
