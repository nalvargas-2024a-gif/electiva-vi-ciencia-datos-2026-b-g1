"""Semana 7 - Ejecuta las 3 consultas SQL y reproduce el WHERE y el GROUP BY en pandas.

Autora: Nicol Alexandra Vargas Sanchez (nalvargas-2024a-gif)

Uso:
    python queries.py

Requiere la carpeta 06-week al lado de esta (usa su modelo y su CSV limpio).
Escribe resultados.md con las salidas.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
SEMANA6 = AQUI.parent / "06-week"
sys.path.insert(0, str(SEMANA6))
from build_db import construir_db, leer_limpio  # noqa: E402


def cargar_consultas(ruta: Path) -> dict[str, str]:
    """Separa queries.sql en {Q1: sql, Q2: sql, Q3: sql} usando los marcadores [Qn]."""
    texto = ruta.read_text(encoding="utf-8")
    partes = re.split(r"^-- \[(Q\d)\].*$", texto, flags=re.M)
    return {partes[i]: partes[i + 1].strip() for i in range(1, len(partes), 2)}


def tabla_md(df: pd.DataFrame) -> str:
    cab = "| " + " | ".join(df.columns) + " |"
    sep = "|" + "|".join("---" for _ in df.columns) + "|"
    filas = ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join([cab, sep, *filas])


def main() -> None:
    csv = SEMANA6 / "data" / "ai4i2020_clean.csv"
    con = construir_db(csv)               # base en memoria
    consultas = cargar_consultas(AQUI / "queries.sql")
    plano = leer_limpio(csv)              # versión plana para pandas

    sql = {k: pd.read_sql_query(q, con) for k, q in consultas.items()}
    modos = ["twf", "hdf", "pwf", "osf", "rnf"]

    # ---- Equivalente pandas de Q1 (WHERE) --------------------------------
    f = plano[(plano["type"] == "L") & (plano["tool_wear_min"] >= 200) & (plano["torque_nm"] >= 50)
              & plano["machine_failure"]].copy()
    f["n_modos"] = f[modos].sum(axis=1)
    p1 = (f[["udi", "product_id", "tool_wear_min", "torque_nm", "rotational_speed_rpm", "n_modos"]]
          .rename(columns={"tool_wear_min": "desgaste_min", "rotational_speed_rpm": "velocidad_rpm"})
          .sort_values(["desgaste_min", "udi"], ascending=[False, True]).reset_index(drop=True))
    pd.testing.assert_frame_equal(sql["Q1"], p1, check_dtype=False)

    # ---- Equivalente pandas de Q2 (JOIN + HAVING) -------------------------
    g = plano.copy()
    g["n_modos"] = g[modos].sum(axis=1)
    g = g[g["n_modos"] > 1]
    g["modos"] = g.apply(lambda r: "+".join(m.upper() for m in sorted(modos) if r[m]), axis=1)
    calidad = {"L": "Low", "M": "Medium", "H": "High"}
    p2 = (g.assign(calidad=g["type"].map(calidad))[["udi", "product_id", "calidad", "modos", "n_modos"]]
          .sort_values("udi").reset_index(drop=True))
    pd.testing.assert_frame_equal(sql["Q2"], p2, check_dtype=False)

    # ---- Equivalente pandas de Q3 (GROUP BY) -----------------------------
    gr = plano.groupby("type")
    p3 = pd.DataFrame({
        "registros": gr.size(),
        "fallas": gr["machine_failure"].sum().astype(int),
        "desgaste_promedio_min": gr["tool_wear_min"].mean().round(1),
    }).reset_index().rename(columns={"type": "tipo"})
    p3["pct_falla"] = (100 * p3["fallas"] / p3["registros"]).round(2)
    p3 = (p3[["tipo", "registros", "fallas", "pct_falla", "desgaste_promedio_min"]]
          .sort_values(["pct_falla", "tipo"], ascending=[False, True]).reset_index(drop=True))
    pd.testing.assert_frame_equal(sql["Q3"], p3, check_dtype=False)

    print(f"Q1: {len(sql['Q1'])} registros tipo L, desgaste >= 200, torque >= 50 y falla  (SQL == pandas)")
    print(sql["Q1"].to_string(index=False))
    print(f"Q2: {len(sql['Q2'])} registros con más de un modo  (SQL == pandas)")
    print(sql["Q2"].to_string(index=False))
    print("Q3: por tipo de producto  (SQL == pandas)")
    print(sql["Q3"].to_string(index=False))

    explicacion = {
        "Q1": "Filtra con `WHERE` (cuatro condiciones) los registros de tipo L con mucho desgaste, torque "
              "alto y falla de máquina. Usa la vista `v_registro` para traer `n_modos`.",
        "Q2": "Une 4 tablas con `JOIN`, agrupa por registro y usa `HAVING` para quedarse con los que tienen "
              "más de un modo. Es la consulta que justifica la tabla intermedia N:M.",
        "Q3": "Agrupa con `GROUP BY` por tipo de producto para comparar volumen, fallas y desgaste.",
    }
    md = ["# Resultados de la semana 7", "",
          "Generado por `queries.py`. Q1, Q2 y Q3 se verificaron contra su equivalente en pandas con "
          "`assert_frame_equal`.", ""]
    for k in ("Q1", "Q2", "Q3"):
        md += [f"## {k}", "", explicacion[k], "", "```sql", consultas[k], "```", "",
               f"Filas devueltas: {len(sql[k])}", "", tabla_md(sql[k]), ""]
    (AQUI / "resultados.md").write_text("\n".join(md), encoding="utf-8")


if __name__ == "__main__":
    main()
