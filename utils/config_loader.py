import yaml
import os

def load_config():
    # ruta absoluta al directorio actual (utils/)
    current_dir = os.path.dirname(__file__)
    
    # subir un nivel → raíz del proyecto
    project_root = os.path.abspath(os.path.join(current_dir, '..'))
    
    # construir path al config.yaml
    config_path = os.path.join(project_root, 'config', 'config.yaml')

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config