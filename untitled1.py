import pandas as pd

# Usamos la ruta absoluta exacta a la carpeta gold generada por Spark
RUTA_GOLD = "/Users/nicowald/Desktop/Programacion/Hobby/BCRA/data/gold/dollar"

# Leemos la capa Gold indicando explícitamente el motor pyarrow para que entienda que es un directorio
df_gold = pd.read_parquet(RUTA_GOLD, engine='pyarrow')

# Ordenamos por fecha para ver los datos más recientes
df_gold = df_gold.sort_values("date", ascending=False)

# Mostramos las métricas calculadas
print(df_gold[["date", "dolar_oficial", "dolar_blue", "brecha", "spread", "volatilidad7d"]].head())