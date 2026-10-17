# Resultados de la semana 7

Generado por `queries.py`. Q1, Q2 y Q3 se verificaron contra su equivalente en pandas con `assert_frame_equal`.

## Q1

Filtra con `WHERE` (cuatro condiciones) los registros de tipo L con mucho desgaste, torque alto y falla de máquina. Usa la vista `v_registro` para traer `n_modos`.

```sql
-- Pregunta: ¿qué registros de producto tipo L, con la herramienta muy desgastada
-- (200 min o más) y torque alto (50 Nm o más), terminaron en falla de máquina?
SELECT udi, product_id, desgaste_min, torque_nm, velocidad_rpm, n_modos
FROM v_registro
WHERE tipo = 'L' AND desgaste_min >= 200 AND torque_nm >= 50 AND falla_maquina = 1
ORDER BY desgaste_min DESC, udi;
```

Filas devueltas: 56

| udi | product_id | desgaste_min | torque_nm | velocidad_rpm | n_modos |
|---|---|---|---|---|---|
| 2859 | L50038 | 231 | 51.5 | 1417 | 1 |
| 4033 | L51212 | 231 | 50.3 | 1383 | 1 |
| 9665 | L56844 | 231 | 54.8 | 1317 | 1 |
| 4384 | L51563 | 229 | 65.5 | 1298 | 2 |
| 1336 | L48515 | 228 | 53.8 | 1371 | 1 |
| 4644 | L51823 | 228 | 54.2 | 1324 | 2 |
| 4643 | L51822 | 226 | 54.6 | 1238 | 2 |
| 8027 | L55206 | 222 | 50.2 | 1399 | 1 |
| 2333 | L49512 | 220 | 50.4 | 1378 | 1 |
| 8609 | L55788 | 220 | 50.6 | 1369 | 1 |
| 162 | L47341 | 218 | 52.3 | 1412 | 1 |
| 250 | L47429 | 218 | 56.2 | 1405 | 1 |
| 1596 | L48775 | 218 | 52.9 | 1365 | 1 |
| 2332 | L49511 | 218 | 53.6 | 1384 | 1 |
| 9494 | L56673 | 217 | 55.4 | 1398 | 1 |
| 161 | L47340 | 216 | 60.7 | 1282 | 1 |
| 249 | L47428 | 216 | 56.8 | 1362 | 1 |
| 6674 | L53853 | 216 | 51.8 | 1380 | 1 |
| 9660 | L56839 | 216 | 61.9 | 1287 | 1 |
| 927 | L48106 | 215 | 55.6 | 1372 | 1 |
| 4730 | L51909 | 215 | 61.0 | 1306 | 2 |
| 8196 | L55375 | 215 | 53.9 | 1376 | 1 |
| 1168 | L48347 | 213 | 52.5 | 1362 | 1 |
| 4985 | L52164 | 213 | 58.7 | 1256 | 1 |
| 5489 | L52668 | 213 | 52.1 | 1450 | 1 |
| 1420 | L48599 | 212 | 53.3 | 1354 | 1 |
| 2762 | L49941 | 212 | 65.1 | 1299 | 1 |
| 3529 | L50708 | 212 | 53.1 | 1378 | 1 |
| 7510 | L54689 | 212 | 60.1 | 1372 | 1 |
| 9017 | L56196 | 212 | 52.7 | 1396 | 1 |
| 7084 | L54263 | 209 | 61.8 | 1416 | 2 |
| 8193 | L55372 | 209 | 65.2 | 1229 | 1 |
| 4815 | L51994 | 208 | 53.0 | 1401 | 1 |
| 5735 | L52914 | 208 | 56.2 | 1369 | 1 |
| 6925 | L54104 | 208 | 52.9 | 1461 | 1 |
| 7594 | L54773 | 208 | 67.5 | 1270 | 1 |
| 2495 | L49674 | 207 | 53.6 | 1329 | 1 |
| 3020 | L50199 | 207 | 54.2 | 1379 | 1 |
| 9415 | L56594 | 207 | 53.9 | 1354 | 1 |
| 7168 | L54347 | 206 | 60.3 | 1362 | 1 |
| 9831 | L57010 | 206 | 56.1 | 1337 | 1 |
| 3944 | L51123 | 205 | 66.7 | 1333 | 2 |
| 5220 | L52399 | 205 | 59.9 | 1365 | 1 |
| 4118 | L51297 | 204 | 55.7 | 1340 | 1 |
| 6256 | L53435 | 204 | 57.3 | 1379 | 1 |
| 328 | L47507 | 203 | 56.7 | 1373 | 1 |
| 6079 | L53258 | 203 | 59.1 | 1339 | 1 |
| 8438 | L55617 | 203 | 65.9 | 1181 | 1 |
| 9655 | L56834 | 203 | 56.3 | 1367 | 1 |
| 243 | L47422 | 202 | 58.8 | 1348 | 1 |
| 1086 | L48265 | 202 | 56.4 | 1385 | 1 |
| 1163 | L48342 | 202 | 57.1 | 1400 | 1 |
| 9654 | L56833 | 201 | 55.7 | 1373 | 1 |
| 1162 | L48341 | 200 | 61.2 | 1316 | 1 |
| 4724 | L51903 | 200 | 50.9 | 1366 | 1 |
| 5062 | L52241 | 200 | 62.5 | 1363 | 1 |

## Q2

Une 4 tablas con `JOIN`, agrupa por registro y usa `HAVING` para quedarse con los que tienen más de un modo. Es la consulta que justifica la tabla intermedia N:M.

```sql
-- Pregunta: ¿qué registros tienen más de un modo de falla a la vez, de qué tipo
-- de producto son y qué modos combinan?
SELECT r.udi,
       r.product_id,
       t.calidad,
       GROUP_CONCAT(f.modo_codigo, '+') AS modos,
       COUNT(*)                         AS n_modos
FROM registro_proceso AS r
JOIN tipo_producto AS t ON t.tipo_codigo = r.tipo_codigo
JOIN (SELECT udi, modo_codigo FROM registro_falla ORDER BY udi, modo_codigo) AS f ON f.udi = r.udi
JOIN modo_falla AS m ON m.modo_codigo = f.modo_codigo
GROUP BY r.udi, r.product_id, t.calidad
HAVING COUNT(*) > 1
ORDER BY r.udi;
```

Filas devueltas: 24

| udi | product_id | calidad | modos | n_modos |
|---|---|---|---|---|
| 70 | L47249 | Low | OSF+PWF | 2 |
| 1325 | M16184 | Medium | OSF+PWF | 2 |
| 1497 | L48676 | Low | OSF+PWF | 2 |
| 3612 | L50791 | Low | RNF+TWF | 2 |
| 3855 | L51034 | Low | OSF+PWF | 2 |
| 3944 | L51123 | Low | OSF+PWF | 2 |
| 4255 | L51434 | Low | HDF+PWF | 2 |
| 4343 | M19202 | Medium | HDF+PWF | 2 |
| 4371 | L51550 | Low | HDF+OSF | 2 |
| 4384 | L51563 | Low | HDF+OSF | 2 |
| 4418 | L51597 | Low | HDF+PWF | 2 |
| 4463 | L51642 | Low | HDF+OSF | 2 |
| 4643 | L51822 | Low | HDF+OSF | 2 |
| 4644 | L51823 | Low | HDF+OSF | 2 |
| 4730 | L51909 | Low | HDF+OSF | 2 |
| 5395 | M20254 | Medium | OSF+PWF | 2 |
| 5402 | M20261 | Medium | OSF+TWF | 2 |
| 5910 | H35323 | High | OSF+PWF+TWF | 3 |
| 6249 | L53428 | Low | OSF+PWF | 2 |
| 7084 | L54263 | Low | OSF+PWF | 2 |
| 8847 | M23706 | Medium | OSF+TWF | 2 |
| 8927 | M23786 | Medium | OSF+PWF | 2 |
| 9085 | L56264 | Low | OSF+PWF | 2 |
| 9975 | L57154 | Low | OSF+PWF | 2 |

## Q3

Agrupa con `GROUP BY` por tipo de producto para comparar volumen, fallas y desgaste.

```sql
-- Pregunta: por tipo de producto, ¿cuántos registros hay, cuántos con falla de
-- máquina, qué porcentaje y cuál es el desgaste promedio?
SELECT t.tipo_codigo                                  AS tipo,
       COUNT(*)                                       AS registros,
       SUM(r.falla_maquina)                           AS fallas,
       ROUND(100.0 * SUM(r.falla_maquina) / COUNT(*), 2) AS pct_falla,
       ROUND(AVG(r.desgaste_min), 1)                  AS desgaste_promedio_min
FROM registro_proceso AS r
JOIN tipo_producto AS t ON t.tipo_codigo = r.tipo_codigo
GROUP BY t.tipo_codigo
ORDER BY pct_falla DESC, t.tipo_codigo;
```

Filas devueltas: 3

| tipo | registros | fallas | pct_falla | desgaste_promedio_min |
|---|---|---|---|---|
| L | 6000 | 235 | 3.92 | 108.4 |
| M | 2997 | 83 | 2.77 | 107.3 |
| H | 1003 | 21 | 2.09 | 107.4 |
