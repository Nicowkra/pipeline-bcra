import requests

from utils.config_loader import load_config
from utils.logger import get_logger

# Inicializamos el logger y la configuración
logger = get_logger(__name__) 
config = load_config()

BASE_URL = config["api"]["base_url"]
BLUE_URL = config["api"]["argDatos_url"]


def get_variable(id_variable, desde, hasta):
    url = f"{BASE_URL}/Monetarias/{id_variable}"
    
    params = {
        "desde": desde,
        "hasta": hasta,
        "limit": 1000
    }
    
    logger.info(f"Llamando API BCRA para la variable ID: {id_variable}")
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if "results" not in data or not data["results"]:
            raise ValueError(f"Respuesta inválida de la API para ID {id_variable}")
            
        return data["results"][0]["detalle"]
        
    except Exception as e:
        logger.error(f"Error al obtener datos del BCRA (Variable {id_variable}): {e}")
        raise  

def get_blue(desde, hasta):
    url = f"{BLUE_URL}"
    logger.info("Llamando API ArgentinaDatos para Dólar Blue")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        resultados = []
        for fila in data:
            # Filtramos por fecha y estandarizamos las claves
            if desde <= fila["fecha"] <= hasta:
                resultados.append({
                    "fecha": fila["fecha"],
                    # Promedio entre las puntas compradora y vendedora (Mid-price)
                    "valor": (fila["venta"] + fila["compra"]) / 2  
                })
                
        return resultados
        
    except Exception as e:
        logger.error(f"Error al obtener datos del Dólar Blue: {e}")
        raise