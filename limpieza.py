import pandas as pd
from pandas import read_csv

df = read_csv("dataframes/Casas")

def eliminar_entradas_no_informadas(df):
    df = df[~df['Direcciones'].str.contains("Dirección no informada", na=False)]
    df = df[~df['Dimensiones'].str.contains("Sin dimensiones", na=False)]
    return df

if __name__ == "__main__":
    print("Datos antes de la limpieza:")
    print(df.info())
    df = df.dropna(axis="columns", how="all")
    df = df.dropna(axis="index", how="any")
    df = df.drop_duplicates()
    df['Precios'] = df['Precios'].str.replace(r"[^\d.,]", "", regex=True).str.strip()
    df['Dimensiones'] = df['Dimensiones'].str.replace(r"\s+", " ", regex=True).str.strip()
    df = eliminar_entradas_no_informadas(df)
    print("\nDatos después de la limpieza:")
    print(df.info())
    df.to_csv("dataframes/Casas_limpias.csv", index=False)
