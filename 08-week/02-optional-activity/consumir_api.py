"""Semana 8 - Consume una API pública con `requests` y muestra 3 registros.

Autora: Nicol Alexandra Vargas Sanchez (nalvargas-2024a-gif)

API: UCI Machine Learning Repository (pública y sin llave). Se piden los metadatos del dataset
AI4I 2020 (id 601), de donde salen las variables que el repositorio declara. Sirven para
contrastar el CSV con su documentación (por ejemplo, el nombre del identificador).

Uso:
    python consumir_api.py

Si no hay conexión (o la API falla), el script usa la muestra guardada en
api_sample.json y lo avisa; así la actividad es reproducible sin internet.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import requests

AQUI = Path(__file__).resolve().parent
URL = "https://archive.ics.uci.edu/api/dataset"


def extraer(dataset_id: int = 601) -> tuple[dict, str]:
    """E de ETL: pide los datos. Devuelve (json, origen)."""
    try:
        resp = requests.get(URL, params={"id": dataset_id}, timeout=10)
        resp.raise_for_status()
        return resp.json(), "API en vivo"
    except requests.RequestException as err:
        print(f"[aviso] no se pudo consultar la API ({type(err).__name__}); "
              "uso la muestra guardada (api_sample.json).")
        muestra = json.loads((AQUI / "api_sample.json").read_text(encoding="utf-8"))
        return muestra, "muestra guardada"


def transformar(datos: dict) -> pd.DataFrame:
    """T de ETL: de JSON anidado (data -> variables) a tabla."""
    return pd.DataFrame(datos["data"]["variables"])[["name", "role", "type", "units"]]


def main() -> None:
    datos, origen = extraer()
    d = datos["data"]
    tabla = transformar(datos)
    print(f"Origen: {origen} | dataset: {d['name']} | instancias: {d['num_instances']}")
    print("3 registros (variables declaradas):")
    print(tabla.head(3).to_string(index=False))
    # L de ETL: se guarda el resultado para usarlo después
    tabla.head(3).to_csv(AQUI / "muestra_api_3_registros.csv", index=False)


if __name__ == "__main__":
    main()
