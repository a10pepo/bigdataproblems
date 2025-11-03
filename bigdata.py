#!/usr/bin/env python3
"""
Ejercicio de las 4 Vs del Big Data
- Velocity: Velocidad de escritura/lectura con intervalos variables
- Volume: Volumen creciente de datos
- Variety: Variedad de formatos (JSON, CSV, TXT)
- Veracity: Veracidad con discrepancias introducidas
"""

import argparse
import subprocess
import sys
import time
import os
import shutil
import signal
from pathlib import Path

def clean_data_folder():
    """Limpia la carpeta data y archivos PNG antes de empezar"""
    # Limpiar carpeta data
    data_folder = Path("data")
    if data_folder.exists():
        shutil.rmtree(data_folder)
    data_folder.mkdir(exist_ok=True)
    
    print("🧹 Carpeta data limpiada")

def run_exercise(velocity=False, volume=False, variety=False, veracity=False):
    """Ejecuta el ejercicio según los parámetros seleccionados"""
    
    # Limpiar carpeta data
    clean_data_folder()
    
    # Construir argumentos para producer y consumer
    # Usar python si estamos en un entorno virtual, sino python3
    python_cmd = "python" if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else "python3"
    producer_args = [python_cmd, "producer.py"]
    consumer_args = [python_cmd, "consumer.py"]
    
    if velocity:
        producer_args.extend(["--velocity", "true"])
        consumer_args.extend(["--velocity", "true"])
        
    if volume:
        producer_args.extend(["--volume", "true"])
        consumer_args.extend(["--volume", "true"])
        
    if variety:
        producer_args.extend(["--variety", "true"])
        consumer_args.extend(["--variety", "true"])
        
    if veracity:
        producer_args.extend(["--veracity", "true"])
        consumer_args.extend(["--veracity", "true"])
    
    print(f"🚀 Iniciando ejercicio Big Data...")
    print(f"   Velocity: {velocity}")
    print(f"   Volume: {volume}")
    print(f"   Variety: {variety}")
    print(f"   Veracity: {veracity}")
    print("-" * 50)
    
    # Iniciar producer en background
    producer_process = subprocess.Popen(
        producer_args,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Dar tiempo al producer para que empiece
    time.sleep(1)
    
    try:
        # Ejecutar consumer (que mostrará los tiempos)
        consumer_process = subprocess.Popen(
            consumer_args
        )
        
        # Esperar a que el consumer termine (o se interrumpa)
        consumer_process.wait()
        
    except KeyboardInterrupt:
        print("\n⏹️  Deteniendo ejercicio...")
        # Enviar SIGINT al consumer para que genere la gráfica
        consumer_process.send_signal(signal.SIGINT)
        # Dar tiempo para generar la gráfica
        try:
            consumer_process.wait(timeout=10)  # Esperar máximo 10 segundos
        except subprocess.TimeoutExpired:
            consumer_process.terminate()
    finally:
        # Terminar producer
        producer_process.terminate()
        producer_process.wait()
        print("\n✅ Ejercicio completado")

def main():
    parser = argparse.ArgumentParser(description="Ejercicio de las 4 Vs del Big Data")
    parser.add_argument("--velocity", type=str, default="false", 
                       help="Activar prueba de velocidad")
    parser.add_argument("--volume", type=str, default="false",
                       help="Activar prueba de volumen")
    parser.add_argument("--variety", type=str, default="false",
                       help="Activar prueba de variedad")
    parser.add_argument("--veracity", type=str, default="false",
                       help="Activar prueba de veracidad")
    
    args = parser.parse_args()
    
    # Convertir strings a booleans
    velocity = args.velocity.lower() == "true"
    volume = args.volume.lower() == "true"
    variety = args.variety.lower() == "true"
    veracity = args.veracity.lower() == "true"
    
    # Verificar que al menos una V esté activada
    if not any([velocity, volume, variety, veracity]):
        print("❌ Error: Debes activar al menos una de las 4 Vs del Big Data")
        sys.exit(1)
    
    run_exercise(velocity, volume, variety, veracity)

if __name__ == "__main__":
    main()
