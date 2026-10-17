| Métrica | Antes | Después |
|---|---:|---:|
| Filas | 10 000 | 10 000 |
| Columnas | 14 | 15 |
| Filas duplicadas exactas | 0 | 0 |
| Celdas nulas | 0 | 0 |
| BOM en el nombre de la primera columna | 1 | 0 |
| Nombres de columna que no son `snake_case` (de 14) | 14 | 0 |
| Nombres con la unidad entre corchetes (p. ej. `[K]` o `[rpm]`) | 5 | 0 |
| Banderas 0/1 guardadas como texto (de 6) | 6 | 0 |

Filas con bandera de falla incoherente, ahora **marcadas** en `inconsistencia_falla`: 27 (9 con `machine_failure` = 1 y ningún modo; 18 con algún modo y `machine_failure` = 0). No se corrigieron.

Filas que discrepan de la regla documentada (HDF, PWF, OSF): `hdf`=0, `pwf`=0, `osf`=0.
