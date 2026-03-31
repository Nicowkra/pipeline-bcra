import os
import sys
from utils.logger import get_logger
logger = get_logger(__name__) 

def save_parquet(df, variable_name, execution_date):
    base_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "bronze",
        "dollar",
        f"variable={variable_name}",
        f"ingestion_date={execution_date}"
    )
    logger.info(f"Guardando parquet en {base_path}")

    os.makedirs(base_path, exist_ok=True)

    file_path = os.path.join(base_path, "data.parquet")
    df.to_parquet(file_path, index=False)
    
    logger.info(f"Archivo guardado: {file_path}")
