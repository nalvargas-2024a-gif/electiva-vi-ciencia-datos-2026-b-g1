"""Genera el extracto "sucio" del ERP: data/ordenes_produccion_raw.csv

Dataset SINTÉTICO (semilla fija => reproducible) para el caso del Corte 1:
"predicción de retrasos en órdenes de producción" de una planta de empaques
plásticos con 4 máquinas y 3 turnos. Se simula la digitación manual de tres
supervisores, por eso el archivo trae los defectos típicos de un registro real:
duplicados, textos escritos de varias formas, fechas en dos formatos, comas
decimales, lecturas en °F, vacíos y valores imposibles.

Uso:  python generar_datos.py
"""
import csv
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
OUT = Path(__file__).parent / "data" / "ordenes_produccion_raw.csv"
OUT.parent.mkdir(exist_ok=True)

N = 420  # órdenes únicas (luego se añaden duplicados)

# ---------------------------------------------------------------- catálogos
MAQ = {  # id: (línea, año de instalación, sesgo de temperatura °C)
    "M-01": ("Línea 1", 2019, 0.0),
    "M-02": ("Línea 1", 2021, -0.3),
    "M-03": ("Línea 2", 2012, 2.2),   # la más antigua: más caliente
    "M-04": ("Línea 2", 2023, -0.5),
}
PROD_POR_LINEA = {"Línea 1": ["P-01", "P-02"], "Línea 2": ["P-03", "P-04", "P-05"]}
TURNOS = ["Mañana", "Tarde", "Noche"]

# ------------------------------------------------- orden "verdadera" (limpia)
maquina = rng.choice(list(MAQ), N, p=[0.27, 0.25, 0.25, 0.23])
turno = rng.choice(TURNOS, N, p=[0.40, 0.35, 0.25])
producto = np.array([rng.choice(PROD_POR_LINEA[MAQ[m][0]]) for m in maquina])

dias_habiles = pd.bdate_range("2026-03-02", "2026-08-14").to_numpy()
fecha_inicio = pd.to_datetime(rng.choice(dias_habiles, N))
dias_plan = rng.integers(2, 7, N)
fecha_fin_plan = fecha_inicio + pd.to_timedelta(dias_plan, unit="D")

cant_plan = (rng.integers(5, 19, N) * 100)               # 500..1800
cant_prod = np.round(cant_plan * rng.uniform(0.93, 1.0, N)).astype(int)
tasa_def = np.select([maquina == "M-03", maquina == "M-01"], [0.045, 0.02], 0.015)
defectuosas = rng.binomial(cant_prod, tasa_def)

horas_parada = np.round(
    rng.gamma(1.6, np.where(maquina == "M-03", 3.2, 1.5)), 1
)
mp_disponible = rng.random(N) > 0.16                      # materia prima
temp_c = np.round(rng.normal(32 + np.array([MAQ[m][2] for m in maquina]), 1.4), 1)

# Retraso latente: depende de paradas, falta de materia prima, máquina y turno
latente = (
    -0.6
    + 0.28 * horas_parada
    + 1.7 * (~mp_disponible)
    + 0.7 * (maquina == "M-03")
    + 0.3 * (turno == "Noche")
    + rng.normal(0, 1.1, N)
)
retraso = np.round(latente).astype(int)
fecha_fin_real = fecha_fin_plan + pd.to_timedelta(retraso, unit="D")

limpio = pd.DataFrame({
    "id_orden": [f"OP-{i:04d}" for i in range(1, N + 1)],
    "fecha_inicio": fecha_inicio,
    "fecha_fin_plan": fecha_fin_plan,
    "fecha_fin_real": fecha_fin_real,
    "maquina": maquina,
    "producto": producto,
    "turno": turno,
    "cant_plan": cant_plan,
    "cant_prod": cant_prod,
    "defectuosas": defectuosas.astype(float),
    "horas_parada": horas_parada,
    "mp_disponible": mp_disponible,
    "temperatura": temp_c,
})

# ------------------------------------------------------ ensuciar el registro
raw = limpio.copy()
idx = lambda k: rng.choice(N, k, replace=False)  # noqa: E731


def variantes(valor, opciones, prob=0.30):
    return opciones.get(valor, [valor]) if rng.random() < prob else [valor]


# Máquinas: 4 códigos -> ~16 formas de escribirlos
VAR_MAQ = {
    "M-01": ["m-01", "M01", " M-01 ", "M-1", "m1"],
    "M-02": ["m-02", "M02", " M-02", "M-2", "m 02"],
    "M-03": ["m-03", "M03", "M-03 ", "M-3", "M 03"],
    "M-04": ["m-04", "M04", " m-04 ", "M-4", "m4"],
}
raw["maquina"] = [rng.choice(VAR_MAQ[m]) if rng.random() < 0.30 else m for m in raw["maquina"]]

VAR_TUR = {
    "Mañana": ["manana", "MAÑANA", "Manana", " mañana", "Mañana "],
    "Tarde": ["tarde", "TARDE", " Tarde", "Tarde ", "tarde "],
    "Noche": ["noche", "NOCHE", "Noche ", " noche", "NOCHE "],
}
raw["turno"] = [rng.choice(VAR_TUR[t]) if rng.random() < 0.32 else t for t in raw["turno"]]

VAR_PROD = {p: [p.lower(), p.replace("-", ""), f" {p}", f"{p} "] for p in
            ["P-01", "P-02", "P-03", "P-04", "P-05"]}
raw["producto"] = [rng.choice(VAR_PROD[p]) if rng.random() < 0.20 else p for p in raw["producto"]]

# Disponibilidad de materia prima: Sí/No escrito de muchas maneras
raw["mp_disponible"] = [
    rng.choice(["Sí", "SI", "si", "S", "Si "]) if v else rng.choice(["No", "NO", "no", "N", "No "])
    for v in raw["mp_disponible"]
]

# Fechas: ISO (aaaa-mm-dd) o latino (dd/mm/aaaa) según el supervisor
def fmt_fecha(s):
    out = []
    for d in s:
        if pd.isna(d):
            out.append(None)
        elif rng.random() < 0.18:
            out.append(d.strftime("%d/%m/%Y"))
        else:
            out.append(d.strftime("%Y-%m-%d"))
    return out


for c in ["fecha_inicio", "fecha_fin_plan", "fecha_fin_real"]:
    raw[c] = fmt_fecha(raw[c])

# Temperatura: coma decimal (texto) y algunas lecturas en °F
temp = raw["temperatura"].astype(float).copy()
f_idx = idx(14)
temp.iloc[f_idx] = np.round(temp.iloc[f_idx] * 9 / 5 + 32, 1)
raw["temperatura"] = [
    f"{v:.1f}".replace(".", ",") if rng.random() < 0.45 else f"{v:.1f}" for v in temp
]
raw["horas_parada"] = [
    f"{v:.1f}".replace(".", ",") if rng.random() < 0.35 else f"{v:.1f}" for v in raw["horas_parada"]
]

# Vacíos
for col, k in [("defectuosas", 14), ("horas_parada", 22), ("temperatura", 12),
               ("mp_disponible", 9), ("fecha_fin_real", 10)]:
    raw.loc[idx(k), col] = np.nan

# Valores imposibles (violan reglas del negocio)
raw["defectuosas"] = raw["defectuosas"].astype(float)
i_inv = idx(3)
raw.loc[i_inv, "defectuosas"] = raw.loc[i_inv, "cant_prod"] + rng.integers(50, 400, 3)   # defectuosas > producidas
raw.loc[idx(2), "defectuosas"] = [-25.0, -61.0]                                           # negativas
i_cap = idx(2)
raw.loc[i_cap, "cant_prod"] = raw.loc[i_cap, "cant_prod"] * 10                            # "un cero de más"
i_fecha = idx(3)
for i in i_fecha:                                                                          # fin real ANTERIOR al inicio
    d = pd.to_datetime(raw.loc[i, "fecha_inicio"], dayfirst="/" in str(raw.loc[i, "fecha_inicio"]))
    raw.loc[i, "fecha_fin_real"] = (d - pd.Timedelta(days=10)).strftime("%Y-%m-%d")

# Duplicados: copias exactas por copiar y pegar
dups = raw.sample(18, random_state=7)
raw = pd.concat([raw, dups]).sample(frac=1, random_state=11).reset_index(drop=True)

raw.to_csv(OUT, index=False, quoting=csv.QUOTE_MINIMAL, encoding="utf-8")
print(f"{OUT.name}: {raw.shape[0]} filas x {raw.shape[1]} columnas")
