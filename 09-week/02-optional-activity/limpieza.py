"""Semana 9 - Limpieza del dataset de mantenimiento predictivo AI4I 2020 (ai4i2020.csv).

Autora: Nicol Alexandra Vargas Sanchez (nalvargas-2024a-gif)

Uso:
    python limpieza.py                      # lee data/ai4i2020.csv
    python limpieza.py ruta/raw.csv ruta/salida_dir

Genera:
    data/ai4i2020_clean.csv          dataset limpio
    reportes/antes_despues.json      métricas antes/después
    reportes/antes_despues.md        la misma evidencia en tabla

Principio de diseño: no se inventa ni se borra ningún dato. Lo que no se puede corregir
(banderas de falla incoherentes) se MARCA y se documenta.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent

RENOMBRAR = {
    "UDI": "udi", "Product ID": "product_id", "Type": "type",
    "Air temperature [K]": "air_temperature_k", "Process temperature [K]": "process_temperature_k",
    "Rotational speed [rpm]": "rotational_speed_rpm", "Torque [Nm]": "torque_nm",
    "Tool wear [min]": "tool_wear_min", "Machine failure": "machine_failure",
    "TWF": "twf", "HDF": "hdf", "PWF": "pwf", "OSF": "osf", "RNF": "rnf",
}
MODOS = ["twf", "hdf", "pwf", "osf", "rnf"]
UMBRAL_OSF = {"L": 11000, "M": 12000, "H": 13000}   # min·Nm, por tipo (documentación del dataset)


def leer_crudo(ruta: Path) -> pd.DataFrame:
    """Lee todo como texto y SIN quitar el BOM, para poder medirlo."""
    return pd.read_csv(ruta, dtype=str, keep_default_na=False, encoding="utf-8")


def perfilar_antes(raw: pd.DataFrame, ruta: Path) -> dict:
    cols = list(raw.columns)
    bom = ruta.read_bytes()[:3] == b"\xef\xbb\xbf"   # pandas oculta el BOM; se mide en los bytes
    return {
        "etiqueta": "antes",
        "filas": int(len(raw)),
        "columnas": int(raw.shape[1]),
        "filas_duplicadas_exactas": int(raw.duplicated().sum()),
        "celdas_nulas": int((raw == "").sum().sum()),
        "bom_en_primer_nombre_de_columna": int(bom),
        "nombres_de_columna_no_snake_case": int(sum(
            not re.fullmatch(r"[a-z][a-z0-9_]*", c.lstrip("﻿")) for c in cols)),
        "nombres_con_unidad_entre_corchetes": int(sum("[" in c for c in cols)),
        "columnas_de_bandera_guardadas_como_texto_0_1": int(sum(
            raw[c].isin(["0", "1"]).all() for c in ["Machine failure", *[m.upper() for m in MODOS]])),
    }


def limpiar(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df.columns = [c.lstrip("﻿") for c in df.columns]          # quita el BOM
    df = df.rename(columns=RENOMBRAR)
    assert list(df.columns) == list(RENOMBRAR.values()), "columnas inesperadas"

    for c in ("product_id", "type"):
        df[c] = df[c].str.strip().str.upper()
    df["udi"] = pd.to_numeric(df["udi"]).astype("int64")
    for c in ("air_temperature_k", "process_temperature_k", "torque_nm"):
        df[c] = pd.to_numeric(df[c]).astype("float64")
    for c in ("rotational_speed_rpm", "tool_wear_min"):
        df[c] = pd.to_numeric(df[c]).astype("int64")
    for c in ["machine_failure", *MODOS]:
        assert df[c].isin(["0", "1"]).all(), f"{c} no es 0/1"
        df[c] = df[c].astype(int).astype(bool)

    # Validaciones de identificación y rangos
    assert (df["udi"] == np.arange(1, len(df) + 1)).all(), "UDI no es 1..n"
    assert df["product_id"].is_unique
    assert df["product_id"].str.fullmatch(r"[LMH]\d{5}").all()
    assert (df["product_id"].str[0] == df["type"]).all(), "la letra del Product ID no coincide con Type"
    assert (df["process_temperature_k"] > df["air_temperature_k"]).all()
    assert (df[["rotational_speed_rpm", "torque_nm"]] > 0).all().all()
    assert (df["tool_wear_min"] >= 0).all()
    assert df.isna().sum().sum() == 0

    # Banderas incoherentes: «machine_failure» debería ser 1 si y solo si hay algún modo de falla.
    # No hay fuente para saber cuál campo es el correcto, así que se MARCAN, no se corrigen.
    hay_modo = df[MODOS].any(axis=1)
    df["inconsistencia_falla"] = hay_modo != df["machine_failure"]
    return df.reset_index(drop=True)


def reglas_documentadas(df: pd.DataFrame) -> dict:
    """Comprueba que HDF, PWF y OSF coinciden con las reglas físicas descritas en la documentación
    del dataset (fallo = regla). Devuelve cuántas filas discrepan; en estos datos, 0."""
    dt = df["process_temperature_k"] - df["air_temperature_k"]
    pot = df["torque_nm"] * df["rotational_speed_rpm"] * 2 * np.pi / 60
    esfuerzo = df["tool_wear_min"] * df["torque_nm"]
    reglas = {
        "hdf": (dt < 8.6) & (df["rotational_speed_rpm"] < 1380),
        "pwf": (pot < 3500) | (pot > 9000),
        "osf": esfuerzo > df["type"].map(UMBRAL_OSF),
    }
    return {m: int((reglas[m] != df[m]).sum()) for m in reglas}


def perfilar_despues(limpio: pd.DataFrame) -> dict:
    cols = list(limpio.columns)
    return {
        "etiqueta": "después",
        "filas": int(len(limpio)),
        "columnas": int(limpio.shape[1]),
        "filas_duplicadas_exactas": int(limpio.duplicated().sum()),
        "celdas_nulas": int(limpio.isna().sum().sum()),
        "bom_en_primer_nombre_de_columna": 0,
        "nombres_de_columna_no_snake_case": int(sum(not re.fullmatch(r"[a-z][a-z0-9_]*", c) for c in cols)),
        "nombres_con_unidad_entre_corchetes": 0,
        "columnas_de_bandera_guardadas_como_texto_0_1": 0,
        "tipos": {c: str(t) for c, t in limpio.dtypes.items()},
        "inconsistencias_de_falla_marcadas": int(limpio["inconsistencia_falla"].sum()),
        "falla_sin_ningun_modo": int((limpio["machine_failure"] & ~limpio[MODOS].any(axis=1)).sum()),
        "modo_sin_falla_de_maquina": int((~limpio["machine_failure"] & limpio[MODOS].any(axis=1)).sum()),
        "filas_con_mas_de_un_modo": int((limpio[MODOS].sum(axis=1) > 1).sum()),
        "filas_que_discrepan_de_la_regla_documentada": reglas_documentadas(limpio),
    }


def tabla_md(a: dict, d: dict) -> str:
    filas = [
        ("Filas", a["filas"], d["filas"]),
        ("Columnas", a["columnas"], d["columnas"]),
        ("Filas duplicadas exactas", a["filas_duplicadas_exactas"], d["filas_duplicadas_exactas"]),
        ("Celdas nulas", a["celdas_nulas"], d["celdas_nulas"]),
        ("BOM en el nombre de la primera columna", a["bom_en_primer_nombre_de_columna"], 0),
        ("Nombres de columna que no son `snake_case` (de 14)", a["nombres_de_columna_no_snake_case"],
         d["nombres_de_columna_no_snake_case"]),
        ("Nombres con la unidad entre corchetes (p. ej. `[K]` o `[rpm]`)", a["nombres_con_unidad_entre_corchetes"], 0),
        ("Banderas 0/1 guardadas como texto (de 6)", a["columnas_de_bandera_guardadas_como_texto_0_1"], 0),
    ]
    out = ["| Métrica | Antes | Después |", "|---|---:|---:|"]
    out += [f"| {m} | {x:,} | {y:,} |".replace(",", " ") for m, x, y in filas]
    out += ["", f"Filas con bandera de falla incoherente, ahora **marcadas** en `inconsistencia_falla`: "
            f"{d['inconsistencias_de_falla_marcadas']} ({d['falla_sin_ningun_modo']} con "
            f"`machine_failure` = 1 y ningún modo; {d['modo_sin_falla_de_maquina']} con algún modo y "
            "`machine_failure` = 0). No se corrigieron.",
            "", "Filas que discrepan de la regla documentada (HDF, PWF, OSF): "
            + ", ".join(f"`{k}`={v}" for k, v in d["filas_que_discrepan_de_la_regla_documentada"].items()) + "."]
    return "\n".join(out)


def main(ruta: Path, salida: Path) -> pd.DataFrame:
    raw = leer_crudo(ruta)
    antes = perfilar_antes(raw, ruta)
    limpio = limpiar(raw)
    despues = perfilar_despues(limpio)

    (salida / "data").mkdir(parents=True, exist_ok=True)
    (salida / "reportes").mkdir(parents=True, exist_ok=True)
    limpio.to_csv(salida / "data" / "ai4i2020_clean.csv", index=False)
    (salida / "reportes" / "antes_despues.json").write_text(
        json.dumps({"antes": antes, "despues": despues}, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8")
    (salida / "reportes" / "antes_despues.md").write_text(tabla_md(antes, despues) + "\n", encoding="utf-8")
    print(tabla_md(antes, despues))
    return limpio


if __name__ == "__main__":
    raw_p = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "data" / "ai4i2020.csv"
    out_d = Path(sys.argv[2]) if len(sys.argv) > 2 else AQUI
    main(raw_p, out_d)
