import requests
import pandas as pd
import time

TOKEN = "04f39bff-3be4-4941-beae-92f9042f6a2d"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_indicator(id_ind, area="00", idioma="es"):
    url = (f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/"
           f"INDICATOR/{id_ind}/{idioma}/{area}/false/BISE/2.0/{TOKEN}?type=json")
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        return None
    try:
        data = resp.json()
    except ValueError:
        return None
    series = data.get("Series")
    if not series:
        return None
    obs = series[0].get("OBSERVATIONS", [])
    df = pd.DataFrame([{"id_ind": id_ind,
                        "periodo": o.get("TIME_PERIOD"),
                        "valor": o.get("OBS_VALUE")}
                       for o in obs if o.get("OBS_VALUE") is not None])
    # Agrega frecuencia si está disponible
    df.attrs["FREQ"] = series[0].get("FREQ")
    return df

def attempt_bulk(indicators, min_obs=300):
    all_dfs = []
    total_obs = 0
    for id_ind in indicators:
        df = get_indicator(id_ind)
        if df is not None and len(df) > 0:
            all_dfs.append(df)
            total_obs += len(df)
            print(f"Indicador {id_ind}: {len(df)} observaciones (freq: {df.attrs.get('FREQ')})")
        else:
            print(f"Indicador {id_ind} no válido o sin datos")
        time.sleep(0.3)  # pausa para evitar saturar la API
    if not all_dfs:
        print("No se obtuvo ninguna serie válida.")
        return None
    combined = pd.concat(all_dfs, ignore_index=True)
    print(f"Total combinado: {len(combined)} observaciones")
    if len(combined) < min_obs:
        print(f"Advertencia: se obtuvieron {len(combined)} < {min_obs} datos solicitados.")
    return combined

if __name__ == "__main__":
    # Ejemplo: una lista de indicadores candidatos
    indicadores_candidatos = [
        "1002000001",  # población total (ejemplo)
        "381016",      # ejemplo, revisar frecuencia
        "444612",      # otro ejemplo
        # Agrega más IDs que encuentres en el catálogo del INEGI
    ]
    df_all = attempt_bulk(indicadores_candidatos, min_obs=300)
    if df_all is not None:
        df_all.to_csv("inegi_dataset_combinado.csv", index=False)
        print("Archivo guardado como inegi_dataset_combinado.csv")

