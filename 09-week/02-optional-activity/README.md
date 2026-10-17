# Semana 9 · Limpieza del dataset de mantenimiento predictivo (AI4I 2020)

```python
FULL_NAME   = "Nicol Alexandra Vargas Sanchez"
GITHUB_USER = "nalvargas-2024a-gif"
```

Asignatura: Ciencia de Datos · Ingeniería Industrial · CORHUILA · 2026-B · Corte 2.
Guía de la actividad: *Semana 9 · Transformación y calidad de datos* (formativa, opcional).

## Qué se entrega

| Archivo | Contenido |
|---|---|
| [`limpieza.py`](limpieza.py) | Script de limpieza en pandas (función `limpiar`) y generador del reporte antes/después |
| [`data/ai4i2020.csv`](data/ai4i2020.csv) | Dataset **original** (10 000 filas × 14 columnas) |
| [`data/ai4i2020_clean.csv`](data/ai4i2020_clean.csv) | Dataset **limpio** (10 000 filas × 15 columnas: 14 originales + `inconsistencia_falla`) |
| [`reportes/antes_despues.md`](reportes/antes_despues.md) y [`.json`](reportes/antes_despues.json) | Evidencia antes/después |

```bash
python limpieza.py     # lee data/ai4i2020.csv y regenera data/ y reportes/
```

**Decisión de diseño:** no se inventa ni se borra ningún dato. Lo que no se puede corregir se **marca** y se documenta.

**Expectativa honesta:** este dataset ya viene muy ordenado (es un conjunto sintético publicado en el repositorio UCI): no tiene nulos ni duplicados. Por eso la limpieza trata sobre **cómo están escritos y tipados los datos** y sobre **verificar su coherencia**, más que sobre rellenar huecos.

## 1. Evidencia antes/después

| Métrica | Antes | Después |
|---|---:|---:|
| Filas | 10 000 | 10 000 |
| Columnas | 14 | 15 |
| Filas duplicadas exactas | 0 | 0 |
| Celdas nulas | 0 | 0 |
| BOM al inicio del archivo | 1 | 0 |
| Nombres de columna que no son `snake_case` (de 14) | 14 | 0 |
| Nombres con la unidad entre corchetes (`[K]`, `[rpm]`…) | 5 | 0 |
| Banderas 0/1 guardadas como texto (de 6) | 6 | 0 |

Además, 27 filas con banderas de falla incoherentes quedan **marcadas** (no corregidas) en la columna nueva `inconsistencia_falla`.

## 2. Problemas encontrados y cómo los traté

| # | Problema | Cómo lo detecté | Tratamiento |
|---|---|---|---|
| 1 | **BOM** (`\xef\xbb\xbf`) al inicio del archivo | Leer los primeros bytes (pandas lo oculta al leer) | Se descarta al leer; el nombre de la primera columna queda limpio |
| 2 | **Nombres con espacios, unidades y corchetes** (`Air temperature [K]`, `Rotational speed [rpm]`…) y en mezcla de mayúsculas | Expresión regular `[a-z][a-z0-9_]*` sobre los 14 nombres | Renombrados a `snake_case` con la unidad al final: `air_temperature_k`, `rotational_speed_rpm`, `torque_nm`, `tool_wear_min`… |
| 3 | **Banderas guardadas como 0/1** (`Machine failure`, `TWF`, `HDF`, `PWF`, `OSF`, `RNF`) | Todas las celdas son `0` o `1` | Convertidas a `bool` |
| 4 | **Identificadores**: `UDI` y `Product ID` | `assert`: UDI = 1..10 000 sin saltos; Product ID único, con formato `[LMH]\d{5}` y la letra igual a `Type` | Sin cambios: ya eran correctos |
| 5 | **Rangos físicos** | `assert`: temperatura del proceso > temperatura del aire; velocidad y torque > 0; desgaste ≥ 0 | Sin cambios: ya eran correctos |
| 6 | **Banderas de falla incoherentes**: `Machine failure` debería ser 1 si y solo si hay algún modo de falla | Cruce entre `Machine failure` y la suma de los 5 modos | **27 filas**: 9 con falla de máquina y ningún modo; 18 con un modo (todos `RNF`) y sin falla de máquina. Se marcan en `inconsistencia_falla`; no hay fuente para saber cuál campo es el correcto |

Dos observaciones sobre los valores atípicos, que **no** traté como errores:

- Hay 32 registros con velocidad > 2 500 rpm (máximo 2 886) y 11 con torque < 10 Nm. Son colas de la distribución y no violan ninguna regla física; borrarlos o recortarlos sería inventar un criterio.
- Hay 120 registros con desgaste 0, que corresponden a una herramienta nueva.

## 3. Dos dimensiones de calidad que mejoré

Dimensiones de la sesión de clase: completitud, exactitud, consistencia, unicidad y vigencia (Wang y Strong, 1996; ISO/IEC, 2008).

### a) Consistencia (de representación): nombres y tipos uniformes

Los nombres mezclaban espacios, corchetes y mayúsculas (14 de 14 fuera de `snake_case`), y las banderas eran texto 0/1. Ahora todos los nombres siguen una sola convención con la unidad en el sufijo, y las banderas son booleanas. Esto evita errores concretos: en SQL un nombre como `Air temperature [K]` exige comillas, y en pandas `df["TWF"] == 1` y `df["twf"]` mezclan convenciones.

### b) Exactitud/consistencia lógica: incoherencias hechas visibles

La bandera `Machine failure` contradice a los modos de falla en 27 de 10 000 filas (0,27 %). No se pueden arreglar sin la fuente, pero **dejaron de pasar desapercibidas**: cualquier análisis puede excluirlas con `inconsistencia_falla` o contarlas aparte. También verifiqué que las reglas de los modos **HDF, PWF y OSF** (reproducidas de la documentación del dataset) coinciden con las banderas en el 100 % de las filas (0 discrepancias).

### Bonus: unicidad

`UDI` y `Product ID` son únicos en las 10 000 filas (se verifica con `assert` cada vez que corre el script).

## 4. Limitaciones

- No hay fuente para saber cuál es la bandera correcta en las 27 filas incoherentes; se usaron las banderas tal cual y quedó la marca.
- Las reglas HDF/PWF/OSF las reproduje de la descripción del dataset y las comprobé contra los datos; **TWF** y **RNF** no son reglas exactas y no se verifican.
- Los datos son sintéticos: que no haya nulos ni duplicados es una propiedad del dataset, no un resultado de la limpieza.

## 5. Referencias

CORHUILA. (2026). *Ciencia de Datos · Semana 9 · Transformación y calidad de datos* [Material de clase]. Corporación Universitaria del Huila. https://code-corhuila.github.io/ova-web/2026-B/ciencia-datos/09-week/01-session/

International Organization for Standardization & International Electrotechnical Commission. (2008). *ISO/IEC 25012:2008 Software engineering — Software product Quality Requirements and Evaluation (SQuaRE) — Data quality model*.

McKinney, W. (2022). *Python for data analysis* (3.ª ed.). O'Reilly Media.

pandas. (s. f.). *Working with missing data*. https://pandas.pydata.org/docs/user_guide/missing_data.html

Rahm, E., y Do, H. H. (2000). Data cleaning: Problems and current approaches. *IEEE Data Engineering Bulletin, 23*(4), 3–13.

UCI Machine Learning Repository. (s. f.). *AI4I 2020 Predictive Maintenance Dataset*. https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset

Wang, R. Y., y Strong, D. M. (1996). Beyond accuracy: What data quality means to data consumers. *Journal of Management Information Systems, 12*(4), 5–33.

Wickham, H. (2014). Tidy data. *Journal of Statistical Software, 59*(10), 1–23.
