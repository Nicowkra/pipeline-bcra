# Argentina Economic Pipeline
Este proyecto es un pipeline de datos ETL que extrae, procesa y cruza información de la API del Banco Central de la República Argentina con la cotización del Dólar Blue. El objetivo es calcular KPIs financieros listos para ser consumidos por herramientas de Business Intelligence.

## Objetivo

Construir un pipeline end-to-end que:

- Orquesta y automatiza todo el ciclo de vida del dato
- Ingesta datos desde APIs públicas
- Los almacena en un data lake (Bronze)
- Limpia y unifica la información (Silver)
- Genera métricas analíticas (Gold)

## Tecnologías Utilizadas

* **Lenguaje:** Python
* **Orquestación:** Apache Airflow (DAG + scheduling + retries)
* **Procesamiento de Datos:** PySpark, Pandas
* **Almacenamiento:** Parquet 
* **Ingesta:** APIs REST (BCRA, ArgentinaDatos) mediante Requests
* **Gestión de Configuración:** YAML

## Arquitectura de Datos

APIs → Bronze → Silver → Gold

1. **Bronze Layer (Raw):** - Extracción de datos crudos mediante requests y pandas.
   - APIs consumidas: BCRA (Oficial, Reservas, Inflación, Base Monetaria) y ArgentinaDatos (Dólar Blue).
   - Guardado en formato parquet, particionado por variable y fecha de ingesta.

2. **Silver Layer (Clean & Conformed):** - Procesamiento con **PySpark**.
   - Casteo de tipos de datos, eliminación de duplicados y Outer Join de todas las series temporales en una única tabla.
   - Implementación de **Forward Fill**  para completar datos faltantes en días no hábiles como fines de semana y feriados.

3. **Gold Layer (Business Analytics):**
   - Transformaciones analíticas y cálculos financieros usando PySpark:
     - **Brecha Cambiaria & Spread Absoluto.**
     - **Variación 24hs (Crawling Peg & Emisión).**
     - **Rolling Mean & Volatility (Desviación Estándar a 7 días).**
     
## Métricas generadas

- Brecha cambiaria
- Spread dólar oficial y blue
- Variación diaria oficial y blue
- Emisión monetaria (variación)
- Promedio móvil semanal
- Volatilidad precio del dólar semanal

## Estructura

```text
├── README.md
├── config
│   └── config.yaml
├── jobs
│   ├── agg.py
│   ├── clean.py
│   └── ingesta.py
├── requirements.txt
└── utils
    ├── client.py
    ├── config_loader.py
    ├── logger.py
    └── storage.py
```

## Logging

El pipeline implementa logging estructurado utilizando el módulo logging de Python.

- Registro de eventos clave (ingesta, transformaciones, guardado)
- Manejo de errores en llamadas a APIs
- Trazabilidad del pipeline completo

## Orquestación con Airflow

El pipeline se encuentra orquestado utilizando Apache Airflow, permitiendo automatizar la ejecución completa del flujo de datos.

Se definió un DAG con las siguientes tareas:

- `ingest`: extracción de datos desde APIs y guardado en la capa Bronze
- `clean`: procesamiento y unificación en la capa Silver
- `agg`: generación de métricas en la capa Gold

Dependencias del pipeline:

ingest → clean → agg

Características:

- Ejecución programada diaria (`@daily`)
- Reintentos automáticos ante fallas
- Monitoreo de ejecución y logs desde la UI de Airflow

## Ejemplo de dataset (Gold)
```markdown
      date  dolar_oficial  dolar_blue    brecha  spread  volatilidad7d
2026-03-31        1382.76      1400.0  0.012468   17.24       7.831158
2026-03-30        1394.92      1415.0  0.014395   20.08       9.479877
2026-03-29        1376.10      1405.0  0.021001   28.90       9.123468
2026-03-28        1376.10      1405.0  0.021001   28.90       9.999157
2026-03-27        1376.10      1405.0  0.021001   28.90      10.119820
```
