# Argentina Economic Pipeline
Este proyecto es un pipeline de datos ETL que extrae, procesa y cruza información de la API del Banco Central de la República Argentina con la cotización del Dólar Blue. El objetivo es calcular KPIs financieros listos para ser consumidos por herramientas de Business Intelligence.

## Objetivo

Construir un pipeline end-to-end que:

- Ingesta datos desde APIs públicas
- Los almacena en un data lake (Bronze)
- Limpia y unifica la información (Silver)
- Genera métricas analíticas (Gold)

## Tecnologías Utilizadas

* **Lenguaje:** Python
* **Procesamiento de Datos:** Apache Spark, Pandas
* **Almacenamiento:** Parquet 
* **Ingesta:** APIs Requests 
* **Gestión de Configuración:** YAML

## Arquitectura de Datos

APIs → Ingesta → Bronze → Silver → Gold

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

## Próximos pasos

- Dashboard (Streamlit / Power BI)
- Deploy en Azure Databricks
