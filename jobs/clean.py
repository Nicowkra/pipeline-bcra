# 1. Imports
import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date
from functools import reduce
from utils.config_loader import load_config
from utils.logger import get_logger
logger = get_logger(__name__) 

#TEMPORAL
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

spark = SparkSession.builder \
    .appName("Dollar Silver Layer") \
    .config("spark.driver.memory", "3g") \
    .getOrCreate()


BASE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "bronze",
    "dollar"
)

config = load_config()


# 4. Leer datos bronze (CORREGIDO)
def load_variable(variable_name):
    path = os.path.join(BASE_PATH, f"variable={variable_name}")
    df = spark.read.parquet(path)
    
    df = df.withColumn("date", to_date(col("date"), "yyyy-MM-dd"))
    df = df.withColumn("value", col("value").cast("double"))
    
    # Seleccionar, renombrar y ELIMINAR DUPLICADOS por fecha
    df = df.select(
        col("date"),
        col("value").alias(variable_name)
    ).dropDuplicates(["date"])

    return df


def run():

    variables = config["metricas"]
    print(variables)
    dfs = []

    for var in variables:
        logger.info(f"Cargando variable {var}")
        df = load_variable(var)
        dfs.append(df)
        logger.info(f"{var}: {df.count()} registros")
    
    logger.info("Realizando join de variables")
    df_final = reduce(
        lambda left, right: left.join(right, on="date", how="outer"),
        dfs
    )

    # 7. Ordenar por fecha
    df_final = df_final.orderBy("date")

    # 8. Forward fill (muy importante)
    from pyspark.sql.window import Window
    from pyspark.sql.functions import last

    window = Window.orderBy("date").rowsBetween(Window.unboundedPreceding, Window.currentRow)
    logger.info("Aplicando forward fill")
    for var in variables:
        df_final = df_final.withColumn(
            var,
            last(col(var), ignorenulls=True).over(window)
        )

    output_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "silver",
        "dollar"
    )
    logger.info("Guardando silver layer")
    df_final.write.mode("overwrite").parquet(output_path)

    
    df_silver = spark.read.parquet(output_path)
    df_silver.show()

if __name__ == "__main__":
    run()