# Semana 7 · Consultas SQL y pandas

```python
FULL_NAME   = "Nicol Alexandra Vargas Sanchez"
GITHUB_USER = "nalvargas-2024a-gif"
```

Asignatura: Ciencia de Datos · Ingeniería Industrial · CORHUILA · 2026-B · Corte 2.
Guía de la actividad: *Semana 7 · Herramientas y lenguajes (SQL, NoSQL, Python)* (formativa, opcional).

## Qué se entrega

| Archivo | Contenido |
|---|---|
| [`queries.sql`](queries.sql) | 3 consultas SQL: `WHERE`, `JOIN` y `GROUP BY`, cada una con su pregunta |
| [`queries.py`](queries.py) | Ejecuta las consultas sobre SQLite y reproduce en pandas **las tres** (la guía pide al menos el `GROUP BY`) |
| [`resultados.md`](resultados.md) | Salida completa de las tres consultas |

Las consultas se ejecutan sobre el modelo de la [semana 6](../06-week/README.md), con los 10 000 registros del CSV limpio.

```bash
python queries.py    # necesita la carpeta 06-week al lado de esta
```

El script **falla si SQL y pandas no coinciden** (`assert_frame_equal`); con los datos entregados pasa sin diferencias.

## Qué responde cada consulta

### Q1 · `WHERE`: tipo L, herramienta muy desgastada y torque alto con falla

```sql
SELECT udi, product_id, desgaste_min, torque_nm, velocidad_rpm, n_modos
FROM v_registro
WHERE tipo = 'L' AND desgaste_min >= 200 AND torque_nm >= 50 AND falla_maquina = 1
ORDER BY desgaste_min DESC, udi;
```

Devuelve **56 registros**: 50 con un solo modo de falla y 6 con dos. Usa la vista `v_registro`, que ya trae `n_modos`. Todos tienen al menos un modo de falla registrado.

### Q2 · `JOIN`: registros con más de un modo de falla

```sql
SELECT r.udi, r.product_id, t.calidad,
       GROUP_CONCAT(f.modo_codigo, '+') AS modos, COUNT(*) AS n_modos
FROM registro_proceso AS r
JOIN tipo_producto AS t ON t.tipo_codigo = r.tipo_codigo
JOIN (SELECT udi, modo_codigo FROM registro_falla ORDER BY udi, modo_codigo) AS f ON f.udi = r.udi
JOIN modo_falla AS m ON m.modo_codigo = f.modo_codigo
GROUP BY r.udi, r.product_id, t.calidad
HAVING COUNT(*) > 1
ORDER BY r.udi;
```

Devuelve **24 registros** (23 con dos modos y 1 con tres). Es la consulta que justifica la tabla intermedia N:M: sin ella, no se podría guardar «OSF+PWF» en un registro sin repetir filas. La combinación más frecuente es **OSF+PWF** (11 registros); también aparecen HDF+OSF (6), HDF+PWF (3), OSF+TWF (2) y RNF+TWF (1), más un registro con tres modos (OSF+PWF+TWF). La subconsulta ordenada hace que `GROUP_CONCAT` entregue los modos en orden alfabético.

### Q3 · `GROUP BY`: fallas por tipo de producto

```sql
SELECT t.tipo_codigo AS tipo, COUNT(*) AS registros, SUM(r.falla_maquina) AS fallas,
       ROUND(100.0 * SUM(r.falla_maquina) / COUNT(*), 2) AS pct_falla,
       ROUND(AVG(r.desgaste_min), 1) AS desgaste_promedio_min
FROM registro_proceso AS r
JOIN tipo_producto AS t ON t.tipo_codigo = r.tipo_codigo
GROUP BY t.tipo_codigo
ORDER BY pct_falla DESC, t.tipo_codigo;
```

| tipo | registros | fallas | % falla | desgaste prom. (min) |
|---|---:|---:|---:|---:|
| L | 6 000 | 235 | 3,92 | 108,4 |
| M | 2 997 | 83 | 2,77 | 107,3 |
| H | 1 003 | 21 | 2,09 | 107,4 |

**Lectura:** el tipo L (calidad baja) falla más que el M, y este más que el H, con un desgaste promedio casi idéntico. Una prueba de independencia entre tipo y falla (hecha aparte con `scipy`, no incluida en el script) da p ≈ 0,001, así que la diferencia no parece ruido. Ojo con el tamaño: H tiene solo 21 fallas, por lo que su porcentaje es el más inestable. Es una asociación **en este dataset sintético**, no una conclusión sobre máquinas reales.

## Equivalente en pandas

```python
gr = plano.groupby("type")
p3 = pd.DataFrame({
    "registros": gr.size(),
    "fallas": gr["machine_failure"].sum().astype(int),
    "desgaste_promedio_min": gr["tool_wear_min"].mean().round(1),
})
p3["pct_falla"] = (100 * p3["fallas"] / p3["registros"]).round(2)
```

Es la misma agrupación sobre la tabla plana: `size()` equivale a `COUNT(*)` y la suma de una columna booleana equivale a `SUM(falla)`.

## Limitaciones

- Las consultas comparan porcentajes sin intervalos; las diferencias pequeñas se revisan en la semana 10.
- `falla_maquina` no coincide con los modos en 27 registros (ver semana 9); aquí se usa tal cual viene.
- Los datos son sintéticos: describen el archivo, no una máquina real.

## Referencias

CORHUILA. (2026). *Ciencia de Datos · Semana 7 · Herramientas y lenguajes (SQL, NoSQL, Python)* [Material de clase]. Corporación Universitaria del Huila. https://code-corhuila.github.io/ova-web/2026-B/ciencia-datos/07-week/01-session/

Elmasri, R., y Navathe, S. B. (2016). *Fundamentals of database systems* (7.ª ed.). Pearson.

McKinney, W. (2022). *Python for data analysis* (3.ª ed.). O'Reilly Media.

pandas. (s. f.). *Comparison with SQL*. https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html

pandas. (s. f.). *Group by: split-apply-combine*. https://pandas.pydata.org/docs/user_guide/groupby.html

Python Software Foundation. (s. f.). *sqlite3 — DB-API 2.0 interface for SQLite databases*. https://docs.python.org/3/library/sqlite3.html

SQLite. (s. f.). *SQL as understood by SQLite*. https://www.sqlite.org/lang.html
