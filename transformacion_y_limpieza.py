import os
import pandas as pd

def transformacion_y_limpieza():

    ## SE CARGA EL ARCHIVO CSV DESDE LA CARPETA

    carpeta = "datamexico_csv"

    # Detecta automáticamente el CSV
    archivo_csv = next(
        f for f in os.listdir(carpeta) if f.endswith(".csv")
    )

    ruta = os.path.join(carpeta, archivo_csv)

    print("Archivo cargado:", archivo_csv)

    df = pd.read_csv(ruta)

    #Inspeccion inicial

    print(df.head())
    print(df.shape)
    print(df.columns)
    print(df.info())

    ##LIMPIEZA BASICA
    # Eliminar filas totalmente vacías
    df = df.dropna(how="all")

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Normalizar nombres de columnas
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    ##CORRECCION DE TIPOS DE DATOS
    df['year'] = pd.to_numeric(df['year'], errors='coerce')

    for col in df.columns:
        if col not in ['year', 'state']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    ## TRANSFORMACION A FORMATO TIDY
    df_tidy = df.melt(
        id_vars=['year', 'state'],
        var_name='indicador',
        value_name='valor'
    )

    ## ESTANDARIZACION
    df_tidy['state'] = (
        df_tidy['state']
        .str.upper()
        .str.strip()
    )

    df_tidy = df_tidy.dropna(subset=['valor'])

    ## VALIDACION FINAL
    print(df_tidy.head())
    print(df_tidy.describe())
    print(df_tidy.isnull().sum())

    ## GUARDAR EL DATASET LIMPIOdf_tidy.to_csv(
    df_tidy.to_csv(
        "datamexico_coneval_limpio.csv",
        index=False,
        encoding="utf-8"
    )

    print("Archivo limpio generado: datamexico_coneval_limpio.csv")


if __name__ == "__main__":
    transformacion_y_limpieza()