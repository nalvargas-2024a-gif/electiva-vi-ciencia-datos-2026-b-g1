-- Semana 7 - Consultas SQL sobre el modelo de mantenimiento predictivo (AI4I 2020)
-- Autora: Nicol Alexandra Vargas Sanchez (nalvargas-2024a-gif)
-- Base: SQLite, creada con 06-week/build_db.py a partir de ai4i2020_clean.csv

-- [Q1] WHERE ---------------------------------------------------------------
-- Pregunta: ¿qué registros de producto tipo L, con la herramienta muy desgastada
-- (200 min o más) y torque alto (50 Nm o más), terminaron en falla de máquina?
SELECT udi, product_id, desgaste_min, torque_nm, velocidad_rpm, n_modos
FROM v_registro
WHERE tipo = 'L' AND desgaste_min >= 200 AND torque_nm >= 50 AND falla_maquina = 1
ORDER BY desgaste_min DESC, udi;

-- [Q2] JOIN ----------------------------------------------------------------
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

-- [Q3] GROUP BY ------------------------------------------------------------
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
