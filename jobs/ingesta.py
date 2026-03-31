import os
import sys
from datetime import datetime
import pandas as pd

#TEMPORAL
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.client import get_variable, get_blue
from utils.config_loader import load_config
from utils.storage import save_parquet
from utils.logger import get_logger
logger = get_logger(__name__) 

hoy = datetime.today().strftime('%Y-%m-%d')
config = load_config()
variables = config.get("variables", {})
desde = "2022-12-01"

def run():
    logger.info("Inicio de ingesta de datos")
    for name, var_id in variables.items():
        #ingesta BCRA
        logger.info(f"Ingestando variable {name} (id {var_id})")
        try:
            data = get_variable(var_id, desde, hoy)
        except Exception as e:
            logger.error(f"Error al obtener {name}: {e}")
            continue
        
        df = pd.DataFrame(data)
        logger.info(f"{name}: {len(df)} registros obtenidos")
        df["variable"] = name
        df["ingestion_date"] = hoy

        df = df.rename(columns={
            "fecha": "date",
            "valor": "value"})
        save_parquet(df, name, hoy)
        logger.info(f"{name} guardado en bronze")
        
        
    #ingesta Blue
    logger.info("Ingestando dolar_blue")
    data_blue = get_blue(desde, hoy)
    df_blue = pd.DataFrame(data_blue)
    
    df_blue["variable"] = "dolar_blue"
    df_blue["ingestion_date"] = hoy
    df_blue = df_blue.rename(columns={
        "fecha": "date", 
        "valor": "value"})
    
    save_parquet(df_blue, "dolar_blue", hoy)
    logger.info(f"dolar_blue: {len(df_blue)} registros")

if __name__ == "__main__":
    run()