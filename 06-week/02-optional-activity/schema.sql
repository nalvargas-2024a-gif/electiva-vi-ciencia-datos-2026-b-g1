-- Semana 6 - Modelo relacional del mantenimiento predictivo (AI4I 2020)
-- Autora: Nicol Alexandra Vargas Sanchez (nalvargas-2024a-gif)
-- Motor: SQLite 3 (las llaves foráneas se activan con PRAGMA foreign_keys = ON)

PRAGMA foreign_keys = ON;

-- Variante de calidad del producto (L, M, H). El umbral de sobreesfuerzo depende del tipo,
-- así que vive aquí y no se repite en cada registro (3FN).
CREATE TABLE tipo_producto (
    tipo_codigo           TEXT PRIMARY KEY CHECK (tipo_codigo IN ('L', 'M', 'H')),
    calidad               TEXT NOT NULL UNIQUE,          -- Low / Medium / High
    umbral_sobreesfuerzo  INTEGER NOT NULL CHECK (umbral_sobreesfuerzo > 0)   -- min·Nm
);

-- Catálogo de modos de falla del dataset
CREATE TABLE modo_falla (
    modo_codigo  TEXT PRIMARY KEY CHECK (modo_codigo IN ('TWF', 'HDF', 'PWF', 'OSF', 'RNF')),
    nombre       TEXT NOT NULL UNIQUE,
    regla        TEXT NOT NULL                            -- cómo se activa, según la documentación
);

-- Un registro = una lectura del proceso de un producto. product_id es único (hoy 1:1 con el registro).
CREATE TABLE registro_proceso (
    udi                   INTEGER PRIMARY KEY,
    product_id            TEXT    NOT NULL UNIQUE CHECK (length(product_id) = 6),
    tipo_codigo           TEXT    NOT NULL REFERENCES tipo_producto(tipo_codigo),
    temp_aire_k           REAL    NOT NULL CHECK (temp_aire_k > 0),
    temp_proceso_k        REAL    NOT NULL CHECK (temp_proceso_k > temp_aire_k),
    velocidad_rpm         INTEGER NOT NULL CHECK (velocidad_rpm > 0),
    torque_nm             REAL    NOT NULL CHECK (torque_nm > 0),
    desgaste_min          INTEGER NOT NULL CHECK (desgaste_min >= 0),
    falla_maquina         INTEGER NOT NULL CHECK (falla_maquina IN (0, 1)),
    -- marca de la semana 9: 1 si falla_maquina no coincide con la existencia de algún modo de falla
    inconsistencia_falla  INTEGER NOT NULL CHECK (inconsistencia_falla IN (0, 1))
);

-- N:M registro <-> modo de falla: un registro puede tener varios modos a la vez
-- (24 registros tienen 2 o 3) y un modo aparece en muchos registros.
CREATE TABLE registro_falla (
    udi          INTEGER NOT NULL REFERENCES registro_proceso(udi),
    modo_codigo  TEXT    NOT NULL REFERENCES modo_falla(modo_codigo),
    PRIMARY KEY (udi, modo_codigo)
);

CREATE INDEX idx_registro_tipo ON registro_proceso(tipo_codigo);
CREATE INDEX idx_registro_falla_modo ON registro_falla(modo_codigo);

-- Vista plana: el CSV con dos columnas derivadas (no se guardan: dependen de otras, 3FN)
CREATE VIEW v_registro AS
SELECT r.udi, r.product_id, r.tipo_codigo AS tipo,
       r.temp_aire_k, r.temp_proceso_k,
       ROUND(r.temp_proceso_k - r.temp_aire_k, 1)                  AS delta_temp_k,
       r.velocidad_rpm, r.torque_nm,
       ROUND(r.torque_nm * r.velocidad_rpm * 2 * 3.141592653589793 / 60, 0) AS potencia_w,
       r.desgaste_min, r.falla_maquina, r.inconsistencia_falla,
       (SELECT COUNT(*) FROM registro_falla f WHERE f.udi = r.udi) AS n_modos
FROM registro_proceso r;
