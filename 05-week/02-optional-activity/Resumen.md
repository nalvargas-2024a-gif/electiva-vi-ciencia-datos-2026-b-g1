# Resumen del proyecto

## Mantenimiento predictivo de máquinas industriales

Este proyecto aborda el problema de las **fallas no planificadas en máquinas industriales utilizadas en un proceso de fresado**. Estas fallas pueden interrumpir la producción, aumentar los costos de mantenimiento correctivo y afectar el cumplimiento de los pedidos.

La pregunta principal del proyecto es:

> **¿Podemos predecir qué máquinas fallarán en las próximas horas a partir de sus variables de operación para programar el mantenimiento antes de que ocurra la falla?**

La decisión esperada consiste en **priorizar qué máquina debe recibir mantenimiento primero cuando los recursos disponibles son limitados**, reduciendo el riesgo de paradas inesperadas.

El proyecto utiliza como fuente principal el **AI4I 2020 Predictive Maintenance Dataset** (Matzka, 2020), el cual contiene variables estructuradas como:

- Temperatura del aire.
- Temperatura del proceso.
- Velocidad rotacional.
- Torque.
- Desgaste de la herramienta.
- Tipo de producto.
- Etiqueta y modo de falla.

Para una implementación real, estas fuentes pueden complementarse con información proveniente de:

- Registros de mantenimiento mediante sistemas CMMS.
- Flujos de vibración generados por sensores IoT.
- Notas y diagnósticos escritos por técnicos de mantenimiento.

Esto permite integrar datos **estructurados, semiestructurados y no estructurados**.

Aunque el conjunto AI4I 2020 tiene un volumen moderado como muestra individual, el problema puede convertirse en un escenario de **Big Data** cuando se implementa en una planta con múltiples máquinas y sensores. Esta situación puede analizarse mediante las cinco V:

- **Volumen:** acumulación de grandes cantidades de datos generados por sensores.
- **Velocidad:** generación continua de información que requiere procesamiento oportuno.
- **Variedad:** integración de diferentes formatos y fuentes de datos.
- **Veracidad:** necesidad de validar datos erróneos, incompletos o fuera de rango.
- **Valor:** utilización de los datos para reducir paradas y costos de mantenimiento.

La arquitectura propuesta sigue un flujo desde las fuentes de datos hasta la toma de decisiones. Primero se recopilan los datos de sensores, sistemas de mantenimiento y técnicos. Posteriormente, los datos son almacenados e integrados, preparados mediante procesos de limpieza y validación, y finalmente utilizados en modelos analíticos.

El proyecto incorpora cuatro tipos de analítica:

1. **Analítica descriptiva:** permite conocer qué ha ocurrido históricamente con las fallas.
2. **Analítica diagnóstica:** permite identificar por qué ocurren determinadas fallas.
3. **Analítica predictiva:** permite estimar qué máquinas tienen mayor probabilidad de fallar.
4. **Analítica prescriptiva:** permite recomendar qué máquina debe recibir mantenimiento primero.

La analítica predictiva constituye el núcleo del proyecto, mientras que los demás niveles complementan la comprensión y la toma de decisiones.

Finalmente, se identifica como riesgo ético la **dependencia excesiva de decisiones automatizadas**. Un modelo puede generar predicciones incorrectas debido a problemas en los datos o cambios en las condiciones reales de operación. Por esta razón, el sistema debe funcionar como una herramienta de apoyo a la decisión y mantener la supervisión de los responsables y técnicos de mantenimiento.

En conclusión, el proyecto integra los fundamentos de Ciencia de Datos y Big Data para transformar datos industriales en información útil para anticipar fallas y apoyar la priorización del mantenimiento.

## Referencias

Chapman, P., Clinton, J., Kerber, T., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS Inc.

Chen, M., Mao, S., & Liu, Y. (2014). Big data: A survey. *Mobile Networks and Applications, 19*(2), 171–209. https://doi.org/10.1007/s11036-013-0489-0

Fayyad, U., Piatetsky-Shapiro, G., & Smyth, P. (1996). From data mining to knowledge discovery in databases. *AI Magazine, 17*(3), 37–54. https://doi.org/10.1609/aimag.v17i3.1230

Laney, D. (2001). *3D data management: Controlling data volume, velocity, and variety*. META Group.

Lepenioti, K., Bousdekis, A., Apostolou, D., & Mentzas, G. (2020). Prescriptive analytics: Literature review and research challenges. *International Journal of Information Management, 50*, 57–70. https://doi.org/10.1016/j.ijinfomgt.2019.04.003

Matzka, S. (2020). Explainable artificial intelligence for predictive maintenance applications. In *Proceedings of the 2020 Third International Conference on Artificial Intelligence for Industries (AI4I)* (pp. 69–74). IEEE. https://doi.org/10.1109/AI4I49448.2020.00023

Zonta, T., da Costa, C. A., da Rosa Righi, R., de Lima, M. J., da Trindade, E. S., & Li, G. P. (2020). Predictive maintenance in the Industry 4.0: A systematic literature review. *Computers & Industrial Engineering, 150*, Article 106889. https://doi.org/10.1016/j.cie.2020.106889
