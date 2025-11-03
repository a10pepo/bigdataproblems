#!/bin/bash
# Script para detener el ejercicio de Big Data

echo "🛑 Deteniendo ejercicio Big Data..."

# Buscar procesos relacionados
PROCESSES=$(ps aux | grep -E "(bigdata|producer|consumer)" | grep -v grep | grep python)

if [ -z "$PROCESSES" ]; then
    echo "✅ No hay procesos del ejercicio ejecutándose"
else
    echo "📋 Procesos encontrados:"
    echo "$PROCESSES"
    
    # Extraer PIDs y terminar procesos
    PIDS=$(echo "$PROCESSES" | awk '{print $2}')
    
    echo "🔄 Terminando procesos..."
    for pid in $PIDS; do
        kill $pid 2>/dev/null
        echo "   Terminado PID: $pid"
    done
    
    # Esperar un momento y verificar
    sleep 2
    
    REMAINING=$(ps aux | grep -E "(bigdata|producer|consumer)" | grep -v grep | grep python)
    if [ -z "$REMAINING" ]; then
        echo "✅ Todos los procesos terminados correctamente"
    else
        echo "⚠️  Algunos procesos siguen ejecutándose, forzando terminación..."
        FORCE_PIDS=$(echo "$REMAINING" | awk '{print $2}')
        for pid in $FORCE_PIDS; do
            kill -9 $pid 2>/dev/null
            echo "   Forzado PID: $pid"
        done
    fi
fi

echo "🏁 Ejercicio detenido"