"""Semana 10 - Mini-proyecto de datos (cierre del Corte 2).

Autora: Nicol Alexandra Vargas Sanchez (nalvargas-2024a-gif)

Integra lo del corte en un solo flujo:
    EXTRAER (CSV crudo)  ->  LIMPIAR (pandas, semana 9)
    ->  CARGAR en el modelo relacional (semana 6)
    ->  ANALIZAR con 2 consultas (SQL y pandas, semana 7)

Uso:
    python pipeline.py

Necesita las carpetas 06-week y 09-week al lado de esta (reutiliza su código).
Escribe todo en salidas/.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "09-week"))
sys.path.insert(0, str(AQUI.parent / "06-week"))
from limpieza import leer_crudo, limpiar, perfilar_antes, perfilar_despues  # noqa: E402  (semana 9)
from build_db import conteos, construir_db, leer_limpio  # noqa: E402  (semana 6)

SALIDAS = AQUI / "salidas"
TEAL = "#0b6e75"
NARANJA = "#c4650a"
MODOS = ["twf", "hdf", "pwf", "osf", "rnf"]

# --- Análisis 1: SQL = filtro (WHERE) + agregación (GROUP BY) ---------------
# Se excluyen las 27 filas con bandera de falla incoherente (marcadas en la semana 9).
SQL_ANALISIS_1 = """
SELECT CASE WHEN desgaste_min < 50  THEN '0-49'
            WHEN desgaste_min < 100 THEN '50-99'
            WHEN desgaste_min < 150 THEN '100-149'
            WHEN desgaste_min < 200 THEN '150-199'
            ELSE '200 o más' END                          AS desgaste_tramo_min,
       COUNT(*)                                           AS registros,
       SUM(falla_maquina)                                 AS fallas,
       ROUND(100.0 * SUM(falla_maquina) / COUNT(*), 1)    AS pct_falla
FROM registro_proceso
WHERE inconsistencia_falla = 0
GROUP BY 1
ORDER BY MIN(desgaste_min);
"""


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Intervalo de confianza de Wilson para una proporción."""
    p = k / n
    den = 1 + z ** 2 / n
    centro = (p + z ** 2 / (2 * n)) / den
    mitad = z * math.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / den
    return centro - mitad, centro + mitad


def extraer(ruta: Path) -> pd.DataFrame:
    """E: lee el CSV tal cual (todo como texto, sin interpretar nada)."""
    df = leer_crudo(ruta)
    print(f"[extraer] {len(df)} filas x {df.shape[1]} columnas desde {ruta.name}")
    return df


def limpiar_datos(raw: pd.DataFrame, ruta: Path):
    """T: aplica la limpieza de la semana 9 y mide antes/después."""
    antes = perfilar_antes(raw, ruta)
    limpio = limpiar(raw)
    despues = perfilar_despues(limpio)
    print(f"[limpiar] filas {antes['filas']} -> {despues['filas']} | "
          f"columnas {antes['columnas']} -> {despues['columnas']} | "
          f"nombres no snake_case {antes['nombres_de_columna_no_snake_case']} -> "
          f"{despues['nombres_de_columna_no_snake_case']} | "
          f"incoherencias de falla marcadas {despues['inconsistencias_de_falla_marcadas']}")
    return limpio, antes, despues


def cargar(limpio: pd.DataFrame):
    """L: guarda el CSV limpio y lo carga en el modelo relacional normalizado."""
    SALIDAS.mkdir(exist_ok=True)
    csv = SALIDAS / "ai4i2020_clean.csv"
    limpio.to_csv(csv, index=False)
    con = construir_db(csv, SALIDAS / "mantenimiento.db")
    assert con.execute("PRAGMA foreign_key_check").fetchall() == [], "llaves foráneas rotas"
    print(f"[cargar] {conteos(con)}")
    return con, csv


def analizar(con, csv: Path):
    plano = leer_limpio(csv)
    ok = plano[~plano["inconsistencia_falla"]]

    # ---- Análisis 1 (SQL): tasa de falla por tramo de desgaste de la herramienta
    a1 = pd.read_sql_query(SQL_ANALISIS_1, con)

    # Verificación cruzada SQL == pandas
    tramo = pd.cut(ok["tool_wear_min"], [0, 50, 100, 150, 200, np.inf], right=False)
    chk = ok.groupby(tramo, observed=True)["machine_failure"].agg(["size", "sum"])
    assert chk["size"].tolist() == a1["registros"].tolist()
    assert chk["sum"].tolist() == a1["fallas"].tolist()

    # ---- Análisis 2 (pandas): falla y modos de falla por tipo de producto, con IC 95 %
    filas = []
    for tipo, g in ok.groupby("type"):
        n, k = len(g), int(g["machine_failure"].sum())
        lo, hi = wilson(k, n)
        fila = {"tipo": tipo, "registros": n, "fallas": k, "pct_falla": round(100 * k / n, 2),
                "ic95_inf": round(100 * lo, 2), "ic95_sup": round(100 * hi, 2)}
        fila.update({m: int(g[m].sum()) for m in MODOS})
        filas.append(fila)
    a2 = pd.DataFrame(filas).sort_values("pct_falla", ascending=False).reset_index(drop=True)

    a1.to_csv(SALIDAS / "analisis1_falla_por_desgaste.csv", index=False)
    a2.to_csv(SALIDAS / "analisis2_falla_por_tipo.csv", index=False)
    print(f"[analizar] {len(ok)} registros sin incoherencia; análisis 1 (SQL) y 2 (pandas) listos; "
          "verificación cruzada OK")
    return a1, a2


def graficar(a1: pd.DataFrame, a2: pd.DataFrame) -> None:
    fig, ejes = plt.subplots(1, 2, figsize=(14.5, 5.2))
    ejes[0].bar(a1["desgaste_tramo_min"], a1["pct_falla"], color=TEAL)
    ejes[0].set_xlabel("Desgaste de la herramienta (min)")
    ejes[0].set_ylabel("% de registros con falla de máquina")
    ejes[0].set_title("Análisis 1 · Falla por tramo de desgaste", fontsize=11)
    for i, (p, n) in enumerate(zip(a1["pct_falla"], a1["registros"])):
        ejes[0].text(i, p + 0.3, f"{p:.1f} %\n(n={n})", ha="center", fontsize=8.5)
    ejes[0].set_ylim(0, a1["pct_falla"].max() * 1.25)

    d2 = a2.sort_values("pct_falla")
    y = list(range(len(d2)))
    ejes[1].errorbar(d2["pct_falla"], y,
                     xerr=[d2["pct_falla"] - d2["ic95_inf"], d2["ic95_sup"] - d2["pct_falla"]],
                     fmt="o", color=NARANJA, ecolor=NARANJA, capsize=4)
    ejes[1].set_yticks(y)
    ejes[1].set_yticklabels([f"{t}  (n={n}, {k} fallas)" for t, n, k in
                             zip(d2["tipo"], d2["registros"], d2["fallas"])])
    ejes[1].set_xlabel("% con falla de máquina (intervalo de confianza del 95 %)")
    ejes[1].set_title("Análisis 2 · Falla por tipo de producto", fontsize=11)
    ejes[1].set_xlim(0, d2["ic95_sup"].max() * 1.15)
    for ax in ejes:
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Mini-proyecto · Mantenimiento predictivo AI4I 2020 · Nicol Alexandra Vargas Sanchez",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(SALIDAS / "analisis.png", dpi=140, facecolor="white")


def main() -> None:
    ruta = AQUI / "data" / "ai4i2020.csv"
    raw = extraer(ruta)
    limpio, antes, despues = limpiar_datos(raw, ruta)
    con, csv = cargar(limpio)
    a1, a2 = analizar(con, csv)
    graficar(a1, a2)
    print("\nAnálisis 1 (SQL):\n" + a1.to_string(index=False))
    print("\nAnálisis 2 (pandas):\n" + a2.to_string(index=False))


if __name__ == "__main__":
    main()
