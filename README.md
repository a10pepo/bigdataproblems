# Ejercicio de las 4 Vs del Big Data

Este ejercicio demuestra las cuatro características fundamentales del Big Data mediante scripts de Python que simulan un producer y consumer.

## 📁 Estructura del Proyecto

```
bigdataproblems/
├── bigdata.py              # Script principal que coordina el ejercicio
├── producer.py             # Genera datos según las 4 Vs
├── consumer.py             # Procesa datos, muestra tiempos y genera gráficas
├── test_4vs.py             # Script para pruebas automáticas
├── stop_exercise.sh        # Script para detener el ejercicio fácilmente
├── requirements.txt        # Dependencias del proyecto
├── data/                   # Carpeta donde se almacenan los datos (se limpia automáticamente)
├── demo.png               # Gráfica de rendimiento generada automáticamente
└── README.md              # Este archivo
```

## 🚀 Uso del Ejercicio

### Comando Básico
```bash
python3 bigdata.py --velocity true --volume true --variety true --veracity true
```

### Detener el Ejercicio
Si necesitas detener el ejercicio antes de tiempo:

**Método 1 - Ctrl+C (recomendado):**
```bash
# Presiona Ctrl+C en la terminal donde se ejecuta
```

**Método 2 - Script automático:**
```bash
./stop_exercise.sh
```

**Método 3 - Manual:**
```bash
# Buscar procesos
ps aux | grep -E "(bigdata|producer|consumer)" | grep -v grep

# Terminar por PID
kill [PID_NUMBERS]
```

### Opciones Disponibles
- `--velocity true/false`: Activa la prueba de velocidad
- `--volume true/false`: Activa la prueba de volumen  
- `--variety true/false`: Activa la prueba de variedad
- `--veracity true/false`: Activa la prueba de veracidad

### Ejemplos de Uso

```bash
# Solo velocidad
python3 bigdata.py --velocity true

# Velocidad y volumen
python3 bigdata.py --velocity true --volume true

# Todas las Vs
python3 bigdata.py --velocity true --volume true --variety true --veracity true

# Solo variedad y veracidad
python3 bigdata.py --variety true --veracity true
```

## 📊 Las 4 Vs del Big Data

### 1. 🚀 Velocity (Velocidad)
- **Producer**: Escribe números cada X segundos, reduciendo el tiempo de espera cada 2 iteraciones
- **Consumer**: Procesa **UN SOLO número por vez** para simular capacidad limitada de procesamiento
- **Efecto**: Se genera un **retraso creciente** - el consumer no puede mantener el ritmo del producer
- **Objetivo**: Demostrar el problema real del Big Data cuando los datos llegan más rápido de lo que pueden procesarse

#### 📊 Análisis de Patrones en Velocity

El ejercicio de Velocity demuestra claramente el problema del **desbordamiento de capacidad** típico del Big Data:

**Patrón Observable:**
| Iteración | Números en Archivo | Número Procesado | Retraso | Tendencia             |
| --------- | ------------------ | ---------------- | ------- | --------------------- |
| 15        | 15                 | 15               | 0       | Sincronizado          |
| 20        | 17                 | 16               | 1       | Inicio del retraso    |
| 22        | 30                 | 18               | 12      | Retraso exponencial   |
| 25        | 59                 | 21               | 38      | Crecimiento acelerado |
| 28        | 88                 | 24               | 64      | Sistema sobrecargado  |
| 30        | 107                | 26               | 81      | Backlog crítico       |

**Fases del Comportamiento:**
1. **Fase Inicial (0-15)**: Producer y Consumer sincronizados
2. **Punto de Inflexión (16-20)**: Producer comienza a acelerar
3. **Desbordamiento (20+)**: Retraso creciente exponencial
4. **Saturación (25+)**: Consumer no puede recuperar el ritmo

**Métricas Clave:**
- **Tiempo de Procesamiento**: Se mantiene constante (~0.2-1.5 ms)
- **Velocidad del Producer**: Aumenta progresivamente (sleep_time decrece)
- **Tasa de Retraso**: Crecimiento exponencial del backlog
- **Punto Crítico**: Iteración ~20 donde el sistema se satura

**Interpretación Real:**
Este patrón simula escenarios típicos de Big Data como:
- 📱 **Redes Sociales**: Posts llegando más rápido que el análisis de sentimientos
- 📊 **IoT Sensors**: Datos de sensores superando capacidad de almacenamiento
- 🛒 **E-commerce**: Transacciones en picos de tráfico sobrecargando el sistema
- 📈 **Trading**: Datos de mercado llegando más rápido que el procesamiento de algoritmos

**Fórmulas de Análisis:**
```
Retraso(t) = Números_en_Archivo(t) - Números_Procesados(t)
Tasa_Producción(t) = Números_Generados / Tiempo_Transcurrido
Tasa_Consumo = 1 número/segundo (constante)
Saturación = Cuando Tasa_Producción > Tasa_Consumo
```

**Lecciones Aprendidas:**
1. **Escalabilidad Horizontal**: Necesidad de múltiples consumers paralelos
2. **Buffering Inteligente**: Sistemas de cola para gestionar picos
3. **Priorización**: Procesar datos críticos primero
4. **Monitoreo Proactivo**: Detectar saturación antes del colapso

### 📈 Análisis Visual Automático

Al finalizar, se generan gráficas que muestran:
- **Tendencia del Retraso**: Curva exponencial que demuestra la saturación
- **Punto de Inflexión**: Momento exacto donde el sistema se sobrecarga  
- **Patrón de Escalabilidad**: Cómo afecta el volumen al rendimiento
- **Métricas de Throughput**: Capacidad de procesamiento en tiempo real

### 2. 📈 Volume (Volumen)  
- **Producer**: Incrementa la cantidad de números escritos cada 2 iteraciones (1, 2, 3, 4...)
- **Consumer**: Procesa volúmenes crecientes de datos completos cada vez
- **Objetivo**: Mostrar cómo el aumento del volumen impacta los tiempos de procesamiento

#### 📊 Análisis de Patrones en Volume

El ejercicio de Volume demuestra el **crecimiento controlado** y su impacto en el rendimiento:

**Patrón de Crecimiento Exponencial:**
| Iteración | Números Totales | Volumen Añadido | Tiempo Proc. | Eficiencia      |
| --------- | --------------- | --------------- | ------------ | --------------- |
| 0         | 1               | 1               | 0.10 ms      | Óptima          |
| 3         | 22              | +20             | 0.46 ms      | Buena           |
| 7         | 192             | +150            | 0.63 ms      | Aceptable       |
| 11        | 542             | +200            | 0.73 ms      | Moderada        |
| 13        | 742             | +200            | 1.02 ms      | **Impacto**     |
| 15        | 1,742           | +1,000          | 1.46 ms      | **Degradación** |
| 17        | 2,742           | +1,000          | 1.90 ms      | **Crítica**     |
| 21        | 5,142           | +1,200          | 2.67 ms      | **Saturación**  |

**Fases del Volumen:**
1. **Micro Datos (1-50)**: Procesamiento instantáneo, sin impacto
2. **Datos Pequeños (50-500)**: Crecimiento visible, rendimiento estable  
3. **Datos Medianos (500-1K)**: Primer impacto en tiempo de procesamiento
4. **Big Data (1K-5K+)**: Degradación clara, necesidad de optimización
5. **Volumen Crítico (5K+)**: Saturación del sistema, tiempos exponenciales

**Métricas de Rendimiento:**
- **Escalabilidad**: Limitada (degradación visible con volúmenes >1K)
- **Punto de Inflexión**: ~750 números (tiempo >1ms)
- **Degradación**: 26x más lento (0.10ms → 2.67ms)
- **Throughput**: Disminuye exponencialmente con volumen alto
- **Saturación**: Evidente en volúmenes >5K números

**Interpretación Real:**
Este patrón simula escenarios como:
- 📊 **Data Warehouses**: Carga incremental diaria/semanal
- 📈 **Analytics**: Datasets crecientes en análisis histórico
- 🗄️ **Backups**: Volúmenes de respaldo incrementales
- 📋 **Batch Processing**: Procesamiento por lotes de tamaño creciente

**Lecciones del Volume:**
1. **Escalabilidad Vertical**: Sistemas que manejan volumen sin degradación
2. **Planificación de Capacidad**: Predecir recursos según crecimiento
3. **Optimización de Memoria**: Gestión eficiente de datasets grandes
4. **Arquitectura Batch**: Diseño para procesar volúmenes variables

### 📈 Análisis Visual Automático

Las gráficas generadas revelan:
- **Curva de Escalabilidad**: Relación no-lineal entre volumen y tiempo
- **Punto de Saturación**: Umbral donde el rendimiento se degrada
- **Patrones de Eficiencia**: Identificación de volúmenes óptimos
- **Throughput Variable**: Cómo cambia la eficiencia con el tamaño### 3. 🔄 Variety (Variedad)
- **Producer**: Escribe los mismos datos en múltiples formatos (JSON, CSV, TXT)
- **Consumer**: Lee y procesa diferentes formatos, mostrando resultados por tipo
- **Objetivo**: Demostrar la complejidad de manejar múltiples formatos de datos

### 4. ⚠️ Veracity (Veracidad)
- **Producer**: Introduce errores aleatorios en algunos valores (10% de probabilidad)
- **Consumer**: Detecta discrepancias entre archivos del mismo lote
- **Objetivo**: Mostrar problemas de calidad y consistencia de datos

## 📋 Funcionamiento Detallado

### Inicialización
1. El script `bigdata.py` limpia la carpeta `data/` automáticamente
2. Inicia el `producer.py` en segundo plano
3. Ejecuta el `consumer.py` en primer plano para mostrar resultados

### Gestión de Archivos
- **Producer**: Siempre escribe a los mismos archivos (`data.txt`, `data.csv`, `data.json`)
- **TXT/CSV**: Añade nuevos números al final del archivo (append)
- **JSON**: Actualiza el array completo de números preservando los anteriores
- **Consumer**: Solo procesa cuando detecta cambios en el tamaño de los archivos

### Producer (Generador de Datos)
- Genera números secuenciales (1, 2, 3, 4...)
- Aplica las transformaciones según las Vs activadas
- **Escribe siempre a los mismos archivos** (`data.txt`, `data.csv`, `data.json`) añadiendo datos

### Consumer (Procesador de Datos)
- Monitorea los archivos fijos en `data/` continuamente
- Procesa solo cuando detecta cambios en el tamaño de los archivos
- **Muestra únicamente los tiempos de procesamiento** como se solicitó
- Detecta discrepancias cuando veracity está activo

## ⏱️ Salida del Consumer

El consumer muestra:
- **Tiempo de procesamiento en milisegundos**
- Número de archivos procesados
- Suma total de números
- Para variety: resultados separados por formato
- Para veracity: alertas de discrepancias detectadas

## 📊 Gráficas Automáticas

Al finalizar cada ejercicio, se genera automáticamente una **gráfica de 4 paneles** que muestra:

1. **Tiempo de Procesamiento**: Evolución temporal del rendimiento
2. **Volumen de Datos**: Comparación entre números en archivo vs procesados
3. **Análisis Específico**:
   - **Velocity**: Retraso creciente entre producer y consumer
   - **Volume**: Escalabilidad (volumen vs tiempo de procesamiento)
4. **Throughput**: Números procesados por milisegundo

### Archivos Generados
- `demo.png` - Gráfica de rendimiento con 4 paneles de análisis visual

**Nota importante**: Para asegurar que la gráfica se genere correctamente, usa **Ctrl+C** para terminar el ejercicio y espera a ver el mensaje "✅ Gráfica guardada exitosamente como: demo.png". Las gráficas se guardan automáticamente al finalizar el análisis.

## 🛠️ Requisitos

- Python 3.6+
- Librerías listadas en `requirements.txt`

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

O instalar manualmente:
```bash
pip install matplotlib seaborn numpy pandas
```

## 🧪 Script de Pruebas Automáticas

Para probar cada V individualmente de manera automática:

```bash
python3 test_4vs.py
```

Este script ejecuta 5 pruebas secuenciales:
1. **Velocity** - Solo velocidad variable (10s)
2. **Volume** - Solo volumen creciente (8s)  
3. **Variety** - Solo múltiples formatos (6s)
4. **Veracity** - Detección de errores (10s)
5. **All** - Las 4 Vs combinadas (12s)

## 🔧 Personalización

Puedes modificar los siguientes parámetros en el código:

### En `producer.py`:
- `sleep_time`: Tiempo inicial entre iteraciones (default: 2.0s)
- `error_probability`: Probabilidad de errores para veracity (default: 0.1)
- Tipos de errores introducidos

### En `consumer.py`:
- Intervalo de monitoreo (default: 1s)
- Formatos de archivo soportados

## 📝 Ejemplos de Salida

### Ejemplo: Solo Velocity
```
📋 Iteración 15:  [SINCRONIZADO]
⏱️  Tiempo de procesamiento: 0.94 ms
📄 data.txt: 15 números en el archivo
🔢 Número procesado: 15
📊 Total procesados hasta ahora: 15

📋 Iteración 20:  [INICIO DEL RETRASO]
⏱️  Tiempo de procesamiento: 1.44 ms
📄 data.txt: 17 números en el archivo
🔢 Número procesado: 16
📊 Total procesados hasta ahora: 16
         ⚠️ Retraso: 1 número

📋 Iteración 25:  [SATURACIÓN DEL SISTEMA]
⏱️  Tiempo de procesamiento: 1.20 ms
📄 data.txt: 59 números en el archivo
🔢 Número procesado: 21
📊 Total procesados hasta ahora: 21
         🚨 Retraso: 38 números - SISTEMA SOBRECARGADO

📋 Iteración 30:  [COLAPSO INMINENTE]
⏱️  Tiempo de procesamiento: 0.59 ms
📄 data.txt: 107 números en el archivo
🔢 Número procesado: 26
📊 Total procesados hasta ahora: 26
         💥 Retraso: 81 números - BACKLOG CRÍTICO
```

### Ejemplo: Solo Volume
```
📋 Iteración 0:  [MICRO DATOS]
⏱️  Tiempo de procesamiento: 0.10 ms
📁 Archivos procesados: 1
🔢 Suma total: 1
📊 Números totales procesados: 1

📋 Iteración 7:  [DATOS PEQUEÑOS]
⏱️  Tiempo de procesamiento: 0.63 ms
📁 Archivos procesados: 1
🔢 Suma total: 18,528
📊 Números totales procesados: 192
         📈 Salto exponencial: +150 números

📋 Iteración 13:  [PUNTO DE INFLEXIÓN]
⏱️  Tiempo de procesamiento: 1.02 ms
📁 Archivos procesados: 1
🔢 Suma total: 275,653
📊 Números totales procesados: 742
         ⚠️ Degradación: >1ms por primera vez

� Iteración 17:  [BIG DATA VISIBLE]
⏱️  Tiempo de procesamiento: 1.90 ms
📁 Archivos procesados: 1
🔢 Suma total: 3,760,653
📊 Números totales procesados: 2,742
         🚨 Impacto: 19x más lento que el inicio

📋 Iteración 21:  [SATURACIÓN DEL SISTEMA]
⏱️  Tiempo de procesamiento: 2.67 ms
📁 Archivos procesados: 1
🔢 Suma total: 13,222,653
📊 Números totales procesados: 5,142
         � Crítico: 26x más lento - OPTIMIZACIÓN NECESARIA
```

### Variety + Veracity
```
📋 Iteración 2:

⏱️  Tiempo de procesamiento: 8.42 ms
📁 Archivos nuevos procesados: 3
   .txt: Suma=156, Números=12, Archivos=1
   .csv: Suma=156, Números=12, Archivos=1  
   .json: Suma=1156, Números=12, Archivos=1
⚠️  DISCREPANCIA DETECTADA: Las sumas no coinciden entre formatos
```

## 🎯 Objetivos de Aprendizaje

Este ejercicio ayuda a entender:
1. **Velocity**: Cómo la velocidad variable afecta el procesamiento en tiempo real
2. **Volume**: El impacto del crecimiento de datos en el rendimiento
3. **Variety**: La complejidad de integrar múltiples formatos
4. **Veracity**: La importancia de la calidad y consistencia de los datos

¡Experimenta con diferentes combinaciones de las 4 Vs para ver cómo interactúan entre sí!
