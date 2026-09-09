# Parcial Práctico · Corte 1

**Estudiante:** _[Nicol Alexandra Vargas Sanchez]_


---

## Caso seleccionado

**Cafetería El Aroma**, un negocio pequeño e independiente que vende café y repostería
tanto en su local físico como a través de apps de domicilios (Rappi / UberEats), y que
recibe reseñas de clientes en Google Maps e Instagram.

---

## 1. Tipos de datos identificados y su clasificación

| # | Tipo de dato | Descripción / fuente | Clasificación |
|---|---|---|---|
| 1 | Registro de ventas (POS) | Tabla con fecha, producto, cantidad, precio y medio de pago, almacenada en la base de datos relacional del punto de venta. | **Estructurado** |
| 2 | Base de clientes / programa de fidelización | Tabla con campos fijos: ID, nombre, correo, teléfono, puntos acumulados. | **Estructurado** |
| 3 | Pedidos de la app de domicilios | Llegan en formato JSON (cliente, dirección, ítems, hora de entrega); tienen etiquetas pero no un esquema rígido de tabla. | **Semiestructurado** |
| 4 | Reseñas y comentarios en Google Maps / Instagram | Texto libre de los clientes, a veces acompañado de fotos; sin estructura predefinida. | **No estructurado** |

---

## 2. Preguntas de analítica

- **Analítica descriptiva:**
  ¿Cuál fue el producto más vendido y en qué horario se concentran más ventas durante
  el último mes en la Cafetería El Aroma?

- **Analítica predictiva:**
  ¿Cuántas unidades de café con leche se venderán la próxima semana, considerando las
  ventas históricas, el clima y los días festivos?

---

## 3. Diagrama del flujo de datos

**Fuente → Almacenamiento → Análisis → Visualización**

```
[Fuente]                [Almacenamiento]         [Análisis]                [Visualización]
POS + App domicilios  →  Base de datos /     →   Excel / Python /     →    Dashboard
+ Redes sociales          Data warehouse          Power BI                 interactivo
                          (en la nube)             (modelos                (Power BI /
                                                    descriptivos y           Tableau)
                                                    predictivos)
```

```mermaid
flowchart LR
    A[Fuente<br/>POS, App de domicilios,<br/>Redes sociales] --> B[Almacenamiento<br/>Base de datos /<br/>Data warehouse en la nube]
    B --> C[Análisis<br/>Excel / Python / Power BI<br/>modelos descriptivos y predictivos]
    C --> D[Visualización<br/>Dashboard interactivo]
```



---

## 4. Descriptive vs. Predictive Analytics (English)

Descriptive analytics summarizes historical data to explain what has already happened
in a business, such as total sales by product over the last month.

Predictive analytics uses historical patterns and statistical models to estimate what
is likely to happen in the future, such as forecasting next week's sales.

---

## Bibliografía

- GeeksforGeeks. (2025). *Difference between structured, semi-structured and unstructured data*. Recuperado de https://geeksforgeeks.org/difference-between-structured-semi-structured-and-unstructured-data

- Splunk. (s.f.). *Structured, unstructured & semi-structured data*. Recuperado de https://www.splunk.com/en_us/blog/learn/data-structured-vs-unstructured-vs-semi-structured

- TechTarget. (s.f.). *What is semi-structured data?* Recuperado de https://whatis.techtarget.com/definition/semi-structured-data

- Educative. (s.f.). *Structured vs. semi-structured vs. unstructured data*. Recuperado de https://www.educative.io/answers/structured-vs-semi-structured-vs-unstructured-data

- INFORMS / Analytics Magazine. (2010). *Descriptive, predictive and prescriptive analytics*. Recuperado de https://pubsonline.informs.org/do/10.1287/LYTX.2010.06.01/full/

- Datamation. (s.f.). *Data pipeline architecture*. Recuperado de https://www.datamation.com/big-data/data-pipeline-architecture

- RisingWave. (2024). *7 eye-opening examples of data pipelines*. Recuperado de https://risingwave.com/blog/7-eye-opening-examples-of-data-pipelines-guide-2024
