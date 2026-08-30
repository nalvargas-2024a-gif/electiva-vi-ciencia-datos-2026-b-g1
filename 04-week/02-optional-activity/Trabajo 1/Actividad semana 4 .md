# Diagnóstico de Datos de un Proceso — Mantenimiento Predictivo de Máquinas Industriales

**Actividad calificable · Corte 1 — Diagnóstico de datos de un proceso (Semana 4 del corte)**
Programa de Ingeniería Industrial, Corporación Universitaria del Huila · Ciencia de Datos
Autora: Nicol Alexandra Vargas Sanchez

---

## 1. Problema y pregunta de datos

El proceso elegido corresponde al mantenimiento de máquinas industriales en un proceso de fresado, usando como base el conjunto de datos sintético **AI4I 2020 Predictive Maintenance Dataset** [1]. Las paradas no planificadas por falla de máquina afectan la continuidad de la producción, generan sobrecostos de mantenimiento correctivo y ponen en riesgo el cumplimiento de los pedidos.

**Pregunta de datos:** ¿Podemos predecir qué máquinas fallarán en las próximas horas, a partir de sus variables de operación, para programar el mantenimiento antes de que ocurra la falla?

**Decisión esperada:** priorizar qué máquina debe recibir mantenimiento primero cuando los recursos de mantenimiento son limitados, evitando que una falla no anticipada detenga la producción.

---

## 2. Inventario de datos

| # | Fuente / campo | Descripción | Tipo |
|---|---|---|---|
| 1 | Temperatura del aire [K] | Lectura del sensor ambiental de la máquina, registrada por ciclo de operación. | Estructurado |
| 2 | Temperatura del proceso [K] | Lectura del sensor de temperatura del proceso de fresado. | Estructurado |
| 3 | Velocidad rotacional [rpm] | Velocidad de giro de la herramienta durante el proceso. | Estructurado |
| 4 | Torque [Nm] | Par aplicado por la herramienta durante el mecanizado. | Estructurado |
| 5 | Desgaste de la herramienta [min] | Minutos acumulados de uso de la herramienta de corte. | Estructurado |
| 6 | Tipo de producto / calidad (L/M/H) | Variante de calidad del producto fabricado en cada orden. | Estructurado |
| 7 | Etiqueta y modo de falla (Machine failure, TWF, HDF, PWF, OSF, RNF) | Indicador binario de falla y modo específico de falla registrado en el dataset. | Estructurado |
| 8 | Órdenes de mantenimiento (CMMS) | Fecha, máquina, tipo de intervención y repuestos usados en mantenimientos previos. | Estructurado |
| 9 | Notas de técnicos de mantenimiento | Texto libre con la descripción de síntomas y el diagnóstico registrado por el técnico. | No estructurado |
| 10 | Flujo de vibración de sensores IoT | Serie de tiempo de alta frecuencia capturada en formato de eventos/JSON durante la operación. | Semiestructurado |

Los campos 1–7 provienen directamente del dataset AI4I 2020 [1] (CSV, estructurado). Los campos 8–10 son fuentes complementarias que un proyecto real de mantenimiento predictivo incorporaría para enriquecer el análisis.

---

## 3. Tipo de analítica aplicable

El caso recorre los cuatro niveles de analítica de datos [5], [6]:

- **Descriptiva** — caracterizar la tasa histórica de fallas por tipo de máquina y por modo de falla (TWF, HDF, PWF, OSF, RNF).
- **Diagnóstica** — identificar qué combinaciones de temperatura, velocidad, torque y desgaste de herramienta están más asociadas con cada modo de falla (por qué ocurre la falla).
- **Predictiva** *(núcleo del caso)* — estimar la probabilidad de que una máquina falle en las próximas horas a partir de sus variables de operación actuales, siguiendo el proceso de descubrimiento de conocimiento en bases de datos [5].
- **Prescriptiva** — traducir la probabilidad de falla estimada en una recomendación concreta de qué máquina debe recibir mantenimiento primero, bajo restricciones de recursos [6].

### ¿Es un caso de Big Data? Justificación con las V

Como muestra estática, el conjunto AI4I 2020 tiene un volumen moderado (10 000 registros de una sola línea de fresado) [1], por lo que en sí mismo no constituye un problema de macrodatos. Sin embargo, el problema de negocio que representa —monitorear en tiempo real un parque de máquinas industriales— sí califica como un caso de Big Data al escalarlo a una planta completa, justificado en las V's del modelo de Laney, ampliado posteriormente en la literatura [2], [3]:

- **Volumen** — sería alto al agregar lecturas continuas de sensores de varias máquinas durante meses o años de operación.
- **Velocidad** — crítica porque el valor de la predicción depende de anticipar la falla mientras la máquina todavía está operando, exigiendo procesamiento casi en tiempo real.
- **Variedad** — evidente en el inventario de la sección 2: datos estructurados (sensores, CMMS), semiestructurados (vibración IoT) y no estructurados (notas de técnicos).
- **Veracidad** — los sensores pueden presentar lecturas erróneas o fuera de rango que deben validarse antes de alimentar el modelo.
- **Valor** — una predicción confiable permite evitar paradas no planificadas y reducir costos de mantenimiento correctivo [7].

---

## 4. Ciclo de vida del proyecto de datos

Ciclo iterativo aplicado al caso, coherente con guías metodológicas como CRISP-DM [4]:

```
+---------------------------------------------------------------------------+
|  1. PREGUNTA                                                              |
|  ¿Podemos predecir que maquinas fallaran en las proximas horas?          |
+-------------------------------------+-------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------+
|  2. OBTENER                                                               |
|  Dataset AI4I 2020 + sensores de planta + CMMS + notas de tecnicos       |
+-------------------------------------+-------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------+
|  3. LIMPIAR                                                               |
|  Validar rangos de sensores, tratar faltantes/atipicos, estandarizar     |
+-------------------------------------+-------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------+
|  4. ANALIZAR                                                              |
|  Modelo predictivo de falla + analisis diagnostico por modo de falla     |
+-------------------------------------+-------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------+
|  5. VISUALIZAR                                                            |
|  Tablero de riesgo de falla por maquina y variables mas influyentes      |
+-------------------------------------+-------------------------------------+
                                      |
                                      v
+---------------------------------------------------------------------------+
|  6. DECIDIR                                                               |
|  Priorizar la maquina que recibe mantenimiento primero                   |
+-------------------------------------+-------------------------------------+
                                      |
                (retroalimentacion: nuevas preguntas de negocio)
                                      |
                                      +---------------------> vuelve a 1. PREGUNTA
```

**Aplicación del ciclo al caso:**

1. **Pregunta.** ¿Podemos predecir qué máquinas fallarán en las próximas horas para programar mantenimiento antes de la falla?
2. **Obtener.** Extraer el conjunto AI4I 2020 [1] y, en un despliegue real, conectar los sensores de planta, el sistema CMMS y las notas de los técnicos.
3. **Limpiar.** Validar rangos de sensores, tratar valores faltantes o atípicos y estandarizar las etiquetas de los modos de falla.
4. **Analizar.** Entrenar y evaluar un modelo predictivo de falla y explorar qué variables explican cada modo de falla (componente diagnóstico).
5. **Visualizar.** Construir un tablero con el nivel de riesgo por máquina y las variables que más contribuyen a dicho riesgo.
6. **Decidir.** Priorizar la máquina que recibe mantenimiento primero y programar la intervención antes de que ocurra la falla.

---

## 5. Marco de referencia y conceptos bibliográficos

El caso se apoya en el conjunto de datos AI4I 2020, publicado por Matzka como un dataset sintético de mantenimiento predictivo para un proceso de fresado, diseñado específicamente para evaluar modelos de predicción de falla junto con técnicas de inteligencia artificial explicable [1]. La clasificación de las fuentes de datos en estructuradas, semiestructuradas y no estructuradas, aplicada en la sección 2, retoma la taxonomía descrita por Chen, Mao y Liu para los macrodatos [3], mientras que la justificación de este caso como un problema de Big Data se apoya en el modelo original de las V propuesto por Laney [2].

El ciclo de vida propuesto en la sección 4 se alinea con la metodología CRISP-DM, ampliamente adoptada en proyectos de minería de datos, que organiza el trabajo en fases de comprensión del negocio, comprensión y preparación de los datos, modelado, evaluación y despliegue [4], y también es coherente con el proceso de descubrimiento de conocimiento en bases de datos descrito por Fayyad, Piatetsky-Shapiro y Smyth, quienes enfatizan que la extracción de patrones útiles requiere ciclos iterativos de selección, limpieza, transformación, minería e interpretación de los datos [5]. La clasificación de los niveles de analítica —descriptiva, diagnóstica, predictiva y prescriptiva— sigue la revisión de Lepenioti et al. sobre analítica prescriptiva [6], y la pertinencia del mantenimiento predictivo como aplicación industrial de estos conceptos está respaldada por la revisión sistemática de Zonta et al. sobre mantenimiento predictivo en el marco de la Industria 4.0 [7].

### Conclusión

El caso de mantenimiento predictivo de máquinas industriales, basado en el conjunto AI4I 2020, admite un inventario de datos diverso que va más allá de los campos estructurados originales del dataset, incorporando fuentes semiestructuradas y no estructuradas propias de un despliegue real en planta. Su tipo de analítica central es predictivo, con componentes diagnóstico y prescriptivo, y constituye un problema de Big Data cuando se escala a un monitoreo continuo de múltiples máquinas, justificado en las cinco V's del modelo de referencia. El ciclo de vida propuesto —pregunta, obtener, limpiar, analizar, visualizar, decidir— ofrece una guía iterativa para llevar este caso desde la pregunta de negocio hasta una decisión operativa concreta de priorización de mantenimiento.

---

## 6. Problem & data (English)

> **Problem & data.** This project addresses the problem of unplanned downtime in an industrial milling process, where machine failures interrupt production and increase maintenance costs. The business question is whether we can predict which machines are likely to fail in the next few hours, so that maintenance can be scheduled before the failure actually occurs. To answer this question, the project uses the AI4I 2020 Predictive Maintenance Dataset, which provides structured sensor readings such as air and process temperature, rotational speed, torque, and tool wear, together with the recorded failure mode for each unit [1]. In a real deployment, these structured records would be complemented with semi-structured IoT vibration streams and unstructured maintenance technician notes to enrich the analysis. The analytics type applied is mainly predictive, since the goal is to estimate the probability of failure before it happens, complemented by a diagnostic component that explains which operating conditions are associated with each failure mode, and by a prescriptive layer that recommends which machine should be prioritized for maintenance under limited resources.

---

## References (IEEE)

[1] S. Matzka, "Explainable artificial intelligence for predictive maintenance applications," in *Proc. 2020 Third Int. Conf. Artificial Intelligence for Industries (AI4I)*, Irvine, CA, USA, 2020, pp. 69–74.

[2] D. Laney, "3D data management: Controlling data volume, velocity, and variety," *META Group Research Note*, vol. 6, no. 70, p. 1, 2001.

[3] M. Chen, S. Mao, and Y. Liu, "Big data: A survey," *Mobile Networks and Applications*, vol. 19, no. 2, pp. 171–209, 2014.

[4] P. Chapman, J. Clinton, R. Kerber, T. Khabaza, T. Reinartz, C. Shearer, and R. Wirth, "CRISP-DM 1.0: Step-by-step data mining guide," SPSS Inc., 2000.

[5] U. Fayyad, G. Piatetsky-Shapiro, and P. Smyth, "From data mining to knowledge discovery in databases," *AI Magazine*, vol. 17, no. 3, pp. 37–54, 1996.

[6] K. Lepenioti, A. Bousdekis, D. Apostolou, and G. Mentzas, "Prescriptive analytics: Literature review and research challenges," *International Journal of Information Management*, vol. 50, pp. 57–70, 2020.

[7] T. Zonta, C. A. da Costa, R. da R. Righi, M. J. de Lima, E. S. da Trindade, and G. P. Li, "Predictive maintenance in the Industry 4.0: A systematic literature review," *Computers & Industrial Engineering*, vol. 150, art. no. 106889, 2020.
