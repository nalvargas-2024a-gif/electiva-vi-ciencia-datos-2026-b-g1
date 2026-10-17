"""Semana 6 - Carga el CSV limpio en el modelo relacional normalizado (SQLite).

Autora: Nicol Alexandra Vargas Sanchez (nalvargas-2024a-gif)

Uso:
    python build_db.py                 # crea mantenimiento.db junto a este archivo

Otras semanas importan `construir_db` para reutilizar el mismo modelo.
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
TABLAS = ["tipo_producto", "modo_falla", "registro_proceso", "registro_falla"]
MODOS = [
    ("TWF", "Tool wear failure", "El desgaste de la herramienta alcanza un valor crítico (en los datos, entre 198 y 253 min)"),
    ("HDF", "Heat dissipation failure", "Diferencia aire-proceso < 8,6 K y velocidad < 1 380 rpm"),
    ("PWF", "Power failure", "Potencia (torque x velocidad angular) fuera de 3 500-9 000 W"),
    ("OSF", "Overstrain failure", "Desgaste x torque supera el umbral del tipo (11 000 / 12 000 / 13 000 min·Nm)"),
    ("RNF", "Random failure", "Falla aleatoria, independiente de las lecturas"),
]
TIPOS = [("L", "Low", 11000), ("M", "Medium", 12000), ("H", "High", 13000)]


def leer_limpio(csv: Path) -> pd.DataFrame:
    return pd.read_csv(csv)


def construir_db(csv_limpio: Path, db_path: Path | None = None) -> sqlite3.Connection:
    """Crea la base (en archivo, o en memoria si db_path es None) y la llena."""
    df = leer_limpio(csv_limpio)
    assert df["udi"].is_unique and df["product_id"].is_unique

    if db_path is not None and Path(db_path).exists():
        Path(db_path).unlink()
    con = sqlite3.connect(":memory:" if db_path is None else str(db_path))
    con.executescript((AQUI / "schema.sql").read_text(encoding="utf-8"))

    con.executemany("INSERT INTO tipo_producto VALUES (?,?,?)", TIPOS)
    con.executemany("INSERT INTO modo_falla VALUES (?,?,?)", MODOS)
    con.executemany(
        "INSERT INTO registro_proceso VALUES (?,?,?,?,?,?,?,?,?,?)",
        [(int(r.udi), r.product_id, r.type, float(r.air_temperature_k), float(r.process_temperature_k),
          int(r.rotational_speed_rpm), float(r.torque_nm), int(r.tool_wear_min),
          int(r.machine_failure), int(r.inconsistencia_falla)) for r in df.itertuples(index=False)])
    filas = [(int(r.udi), m.upper()) for r in df.itertuples(index=False)
             for m in ("twf", "hdf", "pwf", "osf", "rnf") if getattr(r, m)]
    con.executemany("INSERT INTO registro_falla VALUES (?,?)", filas)
    con.commit()
    return con


def conteos(con: sqlite3.Connection) -> dict:
    return {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in TABLAS}


if __name__ == "__main__":
    csv = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "data" / "ai4i2020_clean.csv"
    con = construir_db(csv, AQUI / "mantenimiento.db")
    print("Filas por tabla:", conteos(con))
    print("Violaciones de llave foránea:", len(con.execute("PRAGMA foreign_key_check").fetchall()))
