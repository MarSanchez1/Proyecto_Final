import mysql.connector
import pandas as pd

def data():
    c = pd.read_csv("datasets/Casas_limpias.csv")
    if 'Unnamed: 0' in c.columns:
        c = c.drop(columns=['Unnamed: 0'])
    return c

def migracion(csv):
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="Aracely97",
            database="INMOBILIARIA"
        )
        cursor = conexion.cursor()

        #El primer elemento de la tupla devuelta por iterrows()
        # es el índice (que no necesitamos, por eso usamos _)

        for _, row in csv.iterrows():
            precios = int(str(row['Precios']).replace('$', '').replace(',', ''))

            cursor.execute("""
                INSERT INTO contenedora (id_zona, id_ciudad, precios, direcciones, dimensiones)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                row['Zona'],
                row['Ciudad'],
                precios,
                str(row['Direcciones'])[:255],#la segun lista es para que sepa el rango de caracteres
                str(row['Dimensiones'])[:255]
            ))

        conexion.commit()
        cursor.close()
        conexion.close()

    except mysql.connector.Error as e:
        print(e)

if __name__ == "__main__":
    csv = data()
    migracion(csv)