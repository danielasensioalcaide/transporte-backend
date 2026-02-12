from fastapi import FastAPI
import requests
import os

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

EMT_STOP = "1574"
EMT_LINES = {"62", "64", "92"}
METRO_STATION = "TURIA"

@app.get("/tiempos")
def tiempos():
    resultado = {
        "emt": [],
        "metro": []
    }

    # EMT (endpoint OpenData)
    emt_url = "https://valencia.opendatasoft.com/api/records/1.0/search/"
    emt_params = {
        "dataset": "emt",
        "q": "",
        "rows": 10,
        "refine.id_parada": EMT_STOP
    }

    emt_resp = requests.get(emt_url, params=emt_params, timeout=5).json()

    for r in emt_resp.get("records", []):
        f = r["fields"]
        if f.get("linea") in EMT_LINES:
            resultado["emt"].append({
                "linea": f.get("linea"),
                "minutos": f.get("minutos")
            })

    # Metrovalencia
    metro_url = "https://www.metrovalencia.es/wp-json/metrovalencia/v1/wait-times"
    metro_resp = requests.get(metro_url, timeout=5).json()

    for m in metro_resp:
        if m.get("station", "").upper() == METRO_STATION:
            resultado["metro"].append({
                "linea": m.get("line"),
                "minutos": m.get("minutes")
            })

    return resultado

