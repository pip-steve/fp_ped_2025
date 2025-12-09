import requests
import pandas as pd
import time

# Tu token
TOKEN = "04f39bff-3be4-4941-beae-92f9042f6a2d"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Lista de indicadores mensuales/trimestrales que suelen tener más datos históricos
indicadores = [
    "1002000001",  # Población total (ejemplo)
    "620703",      # Subocupación (ejemplo)
    "6200100791",  # Tasa de informalidad (ejemplo)
    "381016",      # Otro indicador de empleo (ejemplo)
    "444612"       # Otro indicador económico (ejemplo)
]

dfs = []

def obtener_serie(id_ind):
    url = (f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/"
           f"INDICATOR/{id_ind}/es/00/false/BISE/2.0/{TOKEN}?type=json")
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f"Error {resp.status_code} para indicador {id_ind}")
        return None
    try:
        data = resp.json()
        series = data.get("Series", [])
        if not series:
            print(f"No hay series para indicador {id_ind}")
            return None
        obs = series[0].get("OBSERVATIONS", [])
        df = pd.DataFrame([{
            "indicador": id_ind,
            "periodo": o.get("TIME_PERIOD"),
            "valor": o.get("OBS_VALUE")
        } for o in obs if o.get("OBS_VALUE") is not None])
        return df
    except Exception as e:
        print(f"Error al procesar JSON de {id_ind}: {e}")
        return None

# Iterar sobre los indicadores y combinar
for id_ind in indicadores:
    df = obtener_serie(id_ind)
    if df is not None and len(df) > 0:
        dfs.append(df)
        print(f"Obtenidas {len(df)} observaciones de {id_ind}")
    time.sleep(0.3)  # evitar saturar la API

if dfs:
    df_combinado = pd.concat(dfs, ignore_index=True)
    df_combinado.to_csv("inegi_api_combinado.csv", index=False)
    print(f"Archivo guardado: inegi_api_combinado.csv con {len(df_combinado)} registros")
else:
    print("No se obtuvieron datos de ningún indicador")
