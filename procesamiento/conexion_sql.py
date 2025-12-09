import pandas as pd
from sqlalchemy import create_engine, text
import pyodbc
import urllib

"""
Script: conexion.py
Autor: Maviel Cedillo
Funcion del Script:
Conecta con SQL Server, inserta los datos limpios desde el CSV 'datamexico_coneval_limpio.csv'
en la base de datos 'datamex_coneval' y permite consultar las primeras filas de la tabla 'coneval_limpio'.
"""

## Función para insertar datos

def insertar_datos():
    # Configuración de SQL Server
    server = r"localhost\SQLEXPRESS"
    database = "datamex_coneval"
    username = "sa"
    password = "Maviel26"
    driver = "ODBC Driver 18 for SQL Server"
    table_name = "coneval_limpio"

    # Ruta del CSV limpio
    csv_path = "datamexico_coneval_limpio.csv"

    # Cargar CSV
    df = pd.read_csv(csv_path)
    print(f"CSV cargado: {csv_path}, filas: {df.shape[0]}, columnas: {df.shape[1]}")
    print(df.sample(5))

    # Crear cadena de conexión segura
    params = urllib.parse.quote_plus(
        f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes"
    )
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    # Insertar datos
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"✅ Datos insertados en la tabla '{table_name}' de SQL Server")


## Función para consultar datos

def consultar_datos():
    server = r"localhost\SQLEXPRESS"
    database = "datamex_coneval"
    username = "sa"
    password = "Maviel26"
    driver = "ODBC Driver 18 for SQL Server"
    table_name = "coneval_limpio"

    params = urllib.parse.quote_plus(
        f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes"
    )
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    with engine.connect() as conexion:
        sql = text(f"SELECT TOP 20 * FROM {table_name}")
        df = pd.read_sql(sql, conexion)
        print(f"\nPrimeras 20 filas de la tabla '{table_name}' en SQL Server:")
        print(df)



if __name__ == "__main__":
    print("Drivers ODBC disponibles:", pyodbc.drivers())
    # Insertar datos (descomentar si quieres cargar CSV)
    # insertar_datos()
    # Consultar datos
    consultar_datos()


