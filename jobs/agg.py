import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lag, avg, stddev
from pyspark.sql.window import Window
from utils.logger import get_logger
logger = get_logger(__name__) 

#TEMPORAL
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


spark = SparkSession.builder \
    .appName("Dollar Gold Layer") \
    .config("spark.driver.memory", "3g") \
    .getOrCreate()

SILVER_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "silver",
    "dollar"
)
def run():
    df = spark.read.parquet(SILVER_PATH)
    df = df.orderBy("date")
    
    initial_count = df.count()
    logger.info(f"Registros iniciales cargados: {initial_count}")
    
    window_spec = Window.orderBy("date")
    rolling_7d = Window.orderBy("date").rowsBetween(-6, 0)
    
    #Metricas
    logger.info("Inicio de cálculo de métricas (gold layer)")
    
    logger.info("Calculando brecha cambiaria")
    df = df.withColumn(
        "brecha",
        (col("dolar_blue") - col("dolar_oficial")) / col("dolar_oficial")
    )
    df = df.withColumn(
        "spread",
        col("dolar_blue") - col("dolar_oficial")
    )
    
    logger.info("Calculando variaciones diarias")
    # Lag para variaciones
    df = df.withColumn(
        "lag_oficial",
        lag("dolar_oficial").over(window_spec)
    ).withColumn(
        "lag_blue",
        lag("dolar_blue").over(window_spec)
    ).withColumn(
        "lag_base",
        lag("base_monetaria").over(window_spec)
    )
    
    # Variación diaria
    df = df.withColumn(
        "variacion24hs_oficial",
        (col("dolar_oficial") - col("lag_oficial")) / col("lag_oficial")
    ).withColumn(
        "variacion24hs_blue",
        (col("dolar_blue") - col("lag_blue")) / col("lag_blue")
    ).withColumn(
        "variacion24hs_emision",
        (col("base_monetaria") - col("lag_base")) / col("lag_base")
    )
    
    logger.info("Calculando promedio y volatilidad")
    # promedio precio dolar oficial 7 dias
    df = df.withColumn(
        "oficial_promedio7d",
        avg("dolar_oficial").over(rolling_7d)
    )
    
    # Volatilidad 7 dias
    df = df.withColumn(
        "volatilidad7d",
        stddev("dolar_oficial").over(rolling_7d)
    )
    
    #---
    logger.info("Eliminando columnas auxiliares")
    df = df.drop("lag_oficial", "lag_blue", "lag_base")
    df = df.dropna(subset=["dolar_oficial", "dolar_blue"])
    OUTPUT_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "gold",
        "dollar"
    )
    logger.info("Guardando gold layer")
    df.write.mode("overwrite").parquet(OUTPUT_PATH)
    
    logger.info("Pipeline finalizado con éxito. Datos listos para dashboards.")

if __name__ == "__main__":
    run()