"""Semana 6 - Dibuja el ERD del mantenimiento predictivo AI4I 2020 (genera erd.png).

Autora: Nicol Alexandra Vargas Sanchez (nalvargas-2024a-gif)
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

AQUI = Path(__file__).resolve().parent
H = 0.36
ENC, PK, FK = "#0b6e75", "#fff4c2", "#e2f1f3"

# nombre: (x, y_superior, ancho, [(clave, columna, tipo)])
TABLAS = {
    "tipo_producto": (0.4, 9.4, 4.4, [
        ("PK", "tipo_codigo", "TEXT (L, M, H)"), ("", "calidad", "TEXT UNIQUE"),
        ("", "umbral_sobreesfuerzo", "INTEGER")]),
    "registro_proceso": (6.3, 9.4, 4.8, [
        ("PK", "udi", "INTEGER"), ("", "product_id", "TEXT UNIQUE"),
        ("FK", "tipo_codigo", "-> tipo_producto"), ("", "temp_aire_k", "REAL"),
        ("", "temp_proceso_k", "REAL"), ("", "velocidad_rpm", "INTEGER"), ("", "torque_nm", "REAL"),
        ("", "desgaste_min", "INTEGER"), ("", "falla_maquina", "0/1"),
        ("", "inconsistencia_falla", "0/1")]),
    "registro_falla": (6.3, 4.6, 4.8, [
        ("PK,FK", "udi", "-> registro_proceso"), ("PK,FK", "modo_codigo", "-> modo_falla")]),
    "modo_falla": (12.6, 4.6, 4.4, [
        ("PK", "modo_codigo", "TEXT (TWF, HDF, PWF, OSF, RNF)"), ("", "nombre", "TEXT UNIQUE"),
        ("", "regla", "TEXT")]),
}


def dibujar_tabla(ax, nombre, x, y, w, cols):
    alto = H * (len(cols) + 1)
    ax.add_patch(Rectangle((x, y - alto), w, alto, fc="white", ec="#333", lw=1.2, zorder=2))
    ax.add_patch(Rectangle((x, y - H), w, H, fc=ENC, ec="#333", lw=1.2, zorder=3))
    ax.text(x + w / 2, y - H / 2, nombre, color="white", ha="center", va="center",
            fontsize=10, fontweight="bold", zorder=4)
    for i, (clave, col, tipo) in enumerate(cols):
        yf = y - H * (i + 2)
        if clave:
            ax.add_patch(Rectangle((x, yf), w, H, fc=PK if "PK" in clave else FK, ec="none", zorder=3))
        ax.text(x + 0.08, yf + H / 2, clave, fontsize=7.5, va="center", color="#8a5a00",
                fontweight="bold", zorder=4)
        ax.text(x + 0.85, yf + H / 2, col, fontsize=8.5, va="center", zorder=4)
        ax.text(x + w - 0.08, yf + H / 2, tipo, fontsize=7, va="center", ha="right",
                color="#555", zorder=4)
    return {"x": x, "y": y, "w": w, "h": alto}


def main():
    fig, ax = plt.subplots(figsize=(17.4, 7.6))
    ax.set_xlim(0, 17.4)
    ax.set_ylim(2.6, 10.3)
    ax.axis("off")
    c = {n: dibujar_tabla(ax, n, *t) for n, t in TABLAS.items()}

    def pt(n, lado, f=0.5):
        b = c[n]
        return {"izq": (b["x"], b["y"] - b["h"] * f), "der": (b["x"] + b["w"], b["y"] - b["h"] * f),
                "arr": (b["x"] + b["w"] * f, b["y"]), "aba": (b["x"] + b["w"] * f, b["y"] - b["h"])}[lado]

    def unir(puntos, uno, muchos):
        """Línea por `puntos`; '1' junto al primer punto y 'N' junto al último."""
        ax.plot([p[0] for p in puntos], [p[1] for p in puntos], color="#333", lw=1.4, zorder=1)
        for (p, q, txt) in ((puntos[0], puntos[1], uno), (puntos[-1], puntos[-2], muchos)):
            dx, dy = q[0] - p[0], q[1] - p[1]
            n = max((dx ** 2 + dy ** 2) ** 0.5, 1e-9)
            ax.text(p[0] + dx / n * 0.28 - dy / n * 0.18, p[1] + dy / n * 0.28 + dx / n * 0.18, txt,
                    fontsize=10, fontweight="bold", color=ENC, ha="center", va="center")

    unir([pt("tipo_producto", "der", 0.5), pt("registro_proceso", "izq", 0.2)], "1", "N")
    unir([pt("registro_proceso", "aba", 0.5), pt("registro_falla", "arr", 0.5)], "1", "N")
    unir([pt("modo_falla", "izq", 0.5), pt("registro_falla", "der", 0.5)], "1", "N")
    ax.text(8.7, 10.1, "ERD · Mantenimiento predictivo AI4I 2020 (N:M registro ↔ modo de falla, resuelta con registro_falla)",
            ha="center", fontsize=12, fontweight="bold")
    ax.text(8.7, 3.0, "PK = llave primaria   FK = llave foránea   1 → N = uno a muchos   "
            "Autora: Nicol Alexandra Vargas Sanchez", ha="center", fontsize=8.2, color="#444")
    fig.savefig(AQUI / "erd.png", dpi=150, bbox_inches="tight", facecolor="white")
    print("erd.png generado")


if __name__ == "__main__":
    main()
