# ERD en Mermaid (se renderiza directamente en GitHub)

```mermaid
erDiagram
    TIPO_PRODUCTO ||--o{ REGISTRO_PROCESO : "clasifica"
    REGISTRO_PROCESO ||--o{ REGISTRO_FALLA : "presenta"
    MODO_FALLA ||--o{ REGISTRO_FALLA : "aparece en"

    TIPO_PRODUCTO {
        text tipo_codigo PK
        text calidad UK
        int umbral_sobreesfuerzo
    }
    MODO_FALLA {
        text modo_codigo PK
        text nombre UK
        text regla
    }
    REGISTRO_PROCESO {
        int udi PK
        text product_id UK
        text tipo_codigo FK
        real temp_aire_k
        real temp_proceso_k
        int velocidad_rpm
        real torque_nm
        int desgaste_min
        int falla_maquina
        int inconsistencia_falla
    }
    REGISTRO_FALLA {
        int udi PK,FK
        text modo_codigo PK,FK
    }
```
