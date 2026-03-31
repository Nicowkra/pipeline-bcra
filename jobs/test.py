import os
import pandas as pd
import matplotlib.pyplot as plt

# Usamos __file__ para pararnos en la carpeta 'jobs', subir un nivel al proyecto raíz,
# y desde ahí entrar a 'data/gold/dollar'
GOLD_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "gold",
    "dollar"
)

df_gold = pd.read_parquet(GOLD_PATH)

# Aseguramos que la fecha sea el índice para graficar bien
df_gold['date'] = pd.to_datetime(df_gold['date'])
df_gold.set_index('date', inplace=True)

# ... (sigue el resto de tu código de gráficos) ...

# --- PRUEBA 1: Ver la tabla entera en Spyder ---
