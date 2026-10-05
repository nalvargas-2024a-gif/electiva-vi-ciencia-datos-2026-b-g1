-- Esquema relacional (3FN) del ERD de órdenes de producción.
-- Motor: SQLite (la sintaxis es estándar y portable a PostgreSQL/MySQL).

CREATE TABLE maquina (
    id_maquina       TEXT PRIMARY KEY,          -- 'M-01' .. 'M-04'
    nombre           TEXT NOT NULL,
    linea            TEXT NOT NULL,             -- 'Línea 1' | 'Línea 2'
    anio_instalacion INTEGER NOT NULL
);

CREATE TABLE producto (
    id_producto TEXT PRIMARY KEY,               -- 'P-01' .. 'P-05'
    nombre      TEXT NOT NULL,
    linea       TEXT NOT NULL                   -- línea donde se fabrica
);

CREATE TABLE turno (
    id_turno    INTEGER PRIMARY KEY,
    nombre      TEXT NOT NULL UNIQUE,           -- 'Mañana' | 'Tarde' | 'Noche'
    hora_inicio TEXT NOT NULL,
    hora_fin    TEXT NOT NULL
);

CREATE TABLE orden_produccion (
    id_orden       TEXT PRIMARY KEY,            -- 'OP-0001'
    id_maquina     TEXT    NOT NULL REFERENCES maquina(id_maquina),
    id_producto    TEXT    NOT NULL REFERENCES producto(id_producto),
    id_turno       INTEGER NOT NULL REFERENCES turno(id_turno),
    fecha_inicio   DATE    NOT NULL,
    fecha_fin_plan DATE    NOT NULL,
    fecha_fin_real DATE,                        -- NULL = orden aún en curso
    cant_plan      INTEGER NOT NULL CHECK (cant_plan > 0),
    cant_prod      INTEGER NOT NULL CHECK (cant_prod BETWEEN 0 AND 2000),
    defectuosas    INTEGER NOT NULL CHECK (defectuosas >= 0 AND defectuosas <= cant_prod),
    horas_parada   REAL    NOT NULL CHECK (horas_parada >= 0),
    temperatura_c  REAL    NOT NULL CHECK (temperatura_c BETWEEN 15 AND 60),
    mp_disponible  TEXT    NOT NULL CHECK (mp_disponible IN ('Sí', 'No', 'Sin dato')),
    dias_retraso   INTEGER,                     -- fecha_fin_real - fecha_fin_plan
    retrasada      INTEGER CHECK (retrasada IN (0, 1)),
    CHECK (fecha_fin_plan >= fecha_inicio)
);

CREATE INDEX ix_orden_maquina ON orden_produccion(id_maquina);
CREATE INDEX ix_orden_turno   ON orden_produccion(id_turno);
