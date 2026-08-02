# Evolución de los perfiles neuropsicológicos y predicción de la progresión a deterioro de rango demencial en una clínica de memoria argentina: estudio longitudinal de mundo real

**Congreso Argentino de Neurología (CAN)** · Área temática: **Neurología Cognitiva, Demencias y Neuropsicología** · Tipo: Tema libre (oral/póster)

**Autores:** Fernando Márquez¹˒²˒⁴; Paula Virginia Arellano¹˒³˒⁴; Diana Bruno¹˒²; Luciana Vita¹⁻⁴; María Beatriz Bistué¹˒³˒⁴; María Celeste Moyano¹˒³˒⁴; María Laura Noguera Roberto¹; Mariana Zanino¹˒³˒⁴; Cristian Ignacio Posleman¹˒³˒⁴; Iara Jácome¹˒²; Florencia Portillo¹˒³˒⁴; Daniel Lucato²; Martín Alejandro Bruno¹˒³˒⁴.

**Afiliaciones:** ¹ Universidad Católica de Cuyo, San Juan, Argentina. ² Instituto de Neurociencias San Juan (Clínica El Castaño), San Juan, Argentina. ³ Hospital Dr. Guillermo Rawson, San Juan, Argentina. ⁴ Consejo Nacional de Investigaciones Científicas y Técnicas (CONICET), Argentina.

**Autor de correspondencia:** Fernando Márquez — fmarquez.mum@gmail.com

**Productos digitales de acceso abierto:**
- **Simulador de riesgo (calculadora client-side):** https://fermarquez88.github.io/kaizenai-demencia/
- **Artefacto navegable de trayectoria cognitiva** (heatmaps interactivos + tabla maestra): enlazado desde la app.
- **Código:** https://github.com/fermarquez88/kaizenai-demencia

> Referencias verificadas vía **PubMed** (DOI). Reporte según **TRIPOD** (predicción) y **STROBE** (cohorte). **Uso de inteligencia artificial declarado en Métodos.**

---

## Resumen (estructurado)

**Introducción.** La evolución de los perfiles neuropsicológicos en la práctica real de una clínica de memoria —y su
predictibilidad desde la evaluación basal— está poco caracterizada en Latinoamérica, región subrepresentada en la
investigación de demencias.

**Objetivo.** (1) Describir, a nivel de dominio y de test, cómo evolucionan los perfiles cognitivos en una cohorte
argentina de mundo real; y (2) derivar y validar internamente un modelo parsimonioso, normado localmente, que prediga la
progresión a un deterioro de rango demencial desde la evaluación basal.

**Materiales y métodos.** Estudio longitudinal retrospectivo de adultos con ≥2 evaluaciones neuropsicológicas en fechas
distintas (2020–2026). Tras una depuración exhaustiva de la base (deduplicación por hash, recuperación de perfiles desde
el PDF firmado y corrección de fechas), el perfil se codificó desde la sección Conclusiones mediante un modelo de
lenguaje restringido por un codebook (uso de IA declarado). La **banda de severidad** (normal/DCL/demencia) se ancló en
el criterio funcional (juicio clínico narrativo; ADLQ del informante como sensibilidad) y el **subtipo** (amnésico/no
amnésico × dominio único/múltiple) en el patrón objetivo de z (Petersen/Winblad). Las trayectorias por test se
analizaron con **cambio fiable regression-based** (RCI, que descuenta regresión a la media y práctica). El modelo,
pre-especificado por teoría (memoria de relatos diferida y edad), usó regresión logística con validación cruzada
anidada, corrección de optimismo y calibración de Platt.

**Resultados.** De 334 pacientes con múltiples visitas, 254 tuvieron reevaluación genuina (mediana 1,8 años); la
depuración recuperó 63 perfiles y 4 reevaluaciones antes perdidas (219 analizables con perfil basal y final). El
compromiso de memoria fue el eje del riesgo: los perfiles con memoria objetivamente afectada progresaron más que los de
memoria conservada (31% vs 4%; OR de Fisher 9,8; p=0,008); el subtipo amnésico multidominio dominó la cohorte y
concentró los eventos. El **modelo memoria diferida + edad** predijo la progresión con **AUC 0,74 (IC95% 0,54–0,92; 140
pacientes, 37 eventos)**, con alto valor predictivo negativo (VPN 93%). Con un criterio funcional independiente (ADLQ),
el modelo se sostuvo (AUC 0,84). El **análisis de trayectoria por test** mostró patrones fenotipo-específicos: el
perfil amnésico declinó en memoria episódica diferida (hasta 46%), el disejecutivo en velocidad/ejecutivo, y el
amnésico-multidominio en múltiples frentes; los perfiles preservados permanecieron estables. Añadir cuestionarios de
ánimo (GDS) o quejas (CQC) no mejoró la predicción.

**Conclusiones.** Los perfiles cognitivos evolucionan por trayectorias mecanísticamente coherentes y fenotipo-específicas
en las que el compromiso de memoria es el eje del riesgo, y la progresión es predecible con dos variables de rutina. Se
despliegan dos productos digitales abiertos (simulador de riesgo y artefacto de trayectoria). Los hallazgos son
exploratorios y unicéntricos; el desenlace no equivale a demencia confirmada.

**Palabras clave:** deterioro cognitivo leve; demencia; neuropsicología; predicción; trayectoria cognitiva; índice de cambio fiable; Latinoamérica.

---

## Introducción

El deterioro cognitivo leve (DCL) es una entidad heterogénea cuyo desenlace depende de cómo se lo define y del fenotipo
cognitivo subyacente.[1–3] Desde su caracterización inicial como estado transicional con predominio de compromiso de
memoria,[1,2] el consenso internacional estableció que el DCL exige deterioro cognitivo objetivo con **actividades de la
vida diaria preservadas** —el rasgo que lo separa de la demencia— y reconoció subtipos amnésico y no amnésico, de
dominio único o múltiple, con pronósticos distintos.[3] Es el **perfil neuropsicológico** —y no la mera presencia de
deterioro— lo central para el pronóstico.[4–6]

Dentro de ese perfil, la memoria episódica ocupa un lugar privilegiado. El **síndrome amnésico de tipo temporal-medial**
—una falla de almacenamiento que el señalamiento no normaliza— identifica la enfermedad de Alzheimer prodrómica con alta
especificidad,[7] y el **recuerdo diferido** es el predictor neuropsicológico más potente de conversión.[7–13] Los
**criterios neuropsicológicos actuariales** mejoran la estratificación y reducen los falsos positivos.[14–16] El
compromiso amnésico multidominio, la atrofia temporal medial y la carga vascular incrementan el riesgo,[5,17,18] mientras
que la **reserva** modula la expresión clínica,[19] y los síntomas conductuales/anímicos pueden constituir un
pródromo.[20] La mayor parte de esta evidencia proviene de cohortes de altos ingresos, con baterías fijas.

Dos vacíos motivan este trabajo. Primero, la **evolución longitudinal de los perfiles en la práctica de rutina** —a nivel
de dominio y de test— rara vez se describe con el cuidado psicométrico que exigen los datos seriados (cambio fiable,
regresión a la media, efecto de piso), pese a que la prevención depende de identificar la trayectoria temprana.[21,22]
Segundo, **Latinoamérica está marcadamente subrepresentada**; las herramientas validadas en otros contextos transfieren
mal, y las iniciativas regionales enfatizan desarrollar instrumentos localmente desde **medidas de rutina**.[23–25]

## Materiales y métodos

### Aspectos éticos y declaraciones
Análisis retrospectivo de datos clínicos de rutina, anonimizados por un identificador a nivel persona derivado del DNI;
no se comparten datos identificatorios. Por tratarse de datos asistenciales retrospectivos y anonimizados, no se requirió
consentimiento adicional. **Financiamiento:** ninguno específico. **Conflictos de interés:** ninguno.
**Uso de inteligencia artificial:** un modelo de lenguaje restringido por un codebook cerrado se usó para **extraer y
codificar** el perfil desde el texto de las Conclusiones, y como asistencia en el análisis y la redacción; la IA **no**
es autora y toda decisión metodológica y de interpretación fue de los autores. **Disponibilidad de datos:** los datos
individuales son sensibles y no pueden compartirse; el código, el codebook y los coeficientes del modelo son abiertos,
junto con conteos agregados que reproducen las cifras principales.

### Diseño, cohorte y depuración de la base
Adultos evaluados entre 2020 y 2026 con **≥2 evaluaciones en fechas distintas**. Se depuró rigurosamente: (i) los
duplicados del mismo día se confirmaron por **hash SHA-256** (mismo archivo re-archivado) y se conservó la mejor copia;
(ii) se **recuperaron 63 perfiles** que faltaban, extrayendo la sección Conclusiones del PDF firmado y codificándola con
el codebook; (iii) se **recuperaron 4 reevaluaciones** colapsadas por errores de fecha (la fecha real estaba en el nombre
del archivo). Para las evaluaciones sin PDF (solo Excel) se derivó una **severidad z-objetiva** (modelo ordinal calibrado
contra la narrativa, κ ponderada 0,65) usada como cohorte de sensibilidad. La identidad se resolvió por DNI.

### Evaluación, codificación del perfil y clasificación híbrida
Las baterías se adaptaron al motivo de consulta (ACE-III, IFS, Lista de Rey [RAVLT], Memoria de Relatos, Figura de Rey,
fluencias, dígitos, Hayling, WAIS-IV, CI premórbido). Del texto de *Conclusiones* se codificó, mediante un LLM
restringido por codebook, la **banda de severidad** ordinal, el mecanismo de memoria (almacenamiento vs. recuperación) y
moduladores (ánimo, sueño); la **fiabilidad** entre dos codificaciones ciegas fue alta (severidad κ=1,00; refleja
consistencia de extracción, no validación contra experto humano —pendiente). La **clasificación operacional** fue
**híbrida**: la **banda** (normal / DCL / demencia) se ancló en el **criterio funcional** (juicio clínico narrativo, que
incorpora función; ADLQ del informante como sensibilidad, cutoff calibrado ≥40% de áreas alteradas), y el **subtipo**
(amnésico/no amnésico × único/múltiple) en el **patrón objetivo de dominios** z (umbral z ≤ −1,5; Petersen/Winblad). El
almacenamiento comprometido enriquece —no reclasifica— el subtipo amnésico (firma temporal-medial de Dubois/Sarazin).

### Desenlaces y trayectoria
Desenlace primario: **progresión a deterioro de rango demencial** (banda de severidad final ≥ moderada; **sin** criterio
funcional independiente → progresión de severidad, no demencia confirmada). Cohortes por severidad basal: DCL (leve) y
deterioro leve-moderado (leve/leve-mod). Como sensibilidad, se re-definió el desenlace con **criterio funcional ADLQ**
(severidad ≥ moderada **Y** ADLQ ≥ 40%). **Trayectoria psicométrica:** cada test se re-escaló a una referencia común
(mediana/MAD basal, congelada); el cambio se cuantificó con un **Índice de Cambio Fiable regression-based** (SRB,
Crawford-Howell), que descuenta la **regresión a la media** y el efecto de práctica; los pacientes ya en piso al basal se
excluyeron del denominador de declive; la multiplicidad se controló por FDR (Benjamini-Hochberg).

### Análisis estadístico y modelo
El modelo pronóstico **pre-especificado por teoría** (recuerdo diferido de relatos y edad) usó regresión logística con
estandarización e imputación **dentro** de la validación cruzada anidada repetida (5×20), **corrección de optimismo por
bootstrap** (Steyerberg) y **calibración de Platt**. Se reportan **riesgos absolutos** (por tercil), sens/esp/VPP/VPN,
calibración, **curva de decisión** y desempeño por **subgrupos** (sexo, educación). Los análisis de subtipos y subgrupos
son exploratorios (IC; Fisher para celdas escasas). Los modelos desplegados exportan coeficientes + Platt + 200 bootstrap;
una implementación en JavaScript reproduce los coeficientes (test de paridad). Reporte según **TRIPOD** y **STROBE**.

## Resultados

### Cohorte y depuración (Figura 1, Tabla 1)
De 334 pacientes con más de una evaluación archivada, 81 eran duplicados del mismo día (confirmados por hash) y 3 sin
fecha válida; 250 tuvieron reevaluación genuina, y la recuperación de fechas sumó 4 → **254 reevaluaciones** (mediana 1,83
años; IQR 1,25–2,97). Tras recuperar 63 perfiles desde el PDF, **219** quedaron analizables con perfil basal y final
(vs. 182 antes de la depuración). La codificación fue altamente reproducible (severidad κ=1,00) y creció monótonamente
con el número de dominios objetivamente deficitarios.

### El compromiso de memoria es el eje del riesgo (Figuras 2 y 3)
La progresión a rango demencial en la cohorte de deterioro leve-moderado fue de **12,0%/año** (37 eventos / 308
persona-años; IC95% Poisson 8,5–16,6). Con la clasificación híbrida (banda narrativa × subtipo z), los pacientes con
**memoria objetivamente afectada** progresaron mucho más que los de memoria conservada (**31%** vs **4%**; OR de Fisher
**9,8**; p=0,008). El **amnésico multidominio dominó** la cohorte en riesgo (≈78%) y concentró los eventos; los subtipos
de dominio único y no amnésicos fueron infrecuentes. Notablemente, el **multidominio narrativo fue 89% amnésico**
(memoria objetiva comprometida) — sólo 5 pacientes fueron no-amnésico-multidominio —, coherente con una población
enriquecida en AD. El **almacenamiento comprometido** (presente en el 93% de los amnésicos) define la firma
temporal-medial pero **no estratifica** más allá del subtipo (hipocampal 32% vs recuperación 32%). Ningún paciente normal
al basal progresó directamente a demencia (0/16).

### Cómo evolucionan los perfiles: trayectoria por test (Figura 7)
El análisis de cambio fiable por test —tras re-escalar, descontar la regresión a la media y manejar el piso— reveló
**trayectorias fenotipo-específicas**: el perfil **amnésico** declinó sobre todo en **memoria episódica diferida** (hasta
46% de declive fiable en Memoria de Relatos Diferido); el **disejecutivo**, en **velocidad de procesamiento y funciones
ejecutivas** (≈25%); el **amnésico-multidominio**, de forma amplia (memoria, ejecutivo y lenguaje); y los perfiles
**preservados** permanecieron estables —salvo un centinela de memoria diferida—. El declive fiable creció con la
severidad basal (Normal 4% → moderado o mayor 23%). Un hallazgo psicométrico relevante: los tests de memoria diferida
están fuertemente **en piso** al basal en una clínica de memoria (censura por abajo), lo que enmascara su declive en la
métrica cruda; al excluir a los ya-en-piso, la memoria-almacenamiento emerge como firma. La trayectoria completa,
navegable por test, se publica como artefacto abierto.

### Predicción de la progresión (Tabla 2)
El modelo **pre-especificado de dos variables —recuerdo diferido de relatos y edad—** predijo la progresión con **AUC
0,74 (IC95% 0,54–0,92)** en la cohorte de deterioro leve-moderado (140 pacientes, 37 eventos; EPV 18,5). Añadir la
severidad basal, el **GDS** o el **CQC** no mejoró la discriminación (la memoria ya captura la señal). El riesgo observado
creció por tercil de riesgo predicho (9% → 26% → 45%), con **VPN 93%** (buen descarte) y VPP modesto (~40%); el modelo
sobre-predijo en el extremo (leer como ordenamiento de riesgo). En el subgrupo DCL (96/18) rindió 0,76, y con un
**criterio funcional independiente (ADLQ ≥ 40%)** el modelo se sostuvo (**AUC 0,84**; 68 pacientes, 11 eventos
funcionales), respondiendo a la objeción de que el desenlace carecía de criterio funcional. Un modelo de árbol de AUC
aparente 0,97 colapsó a ~0,66 bajo corrección de optimismo (sobreajuste).

## Discusión

En una clínica de memoria argentina de mundo real, los perfiles neuropsicológicos evolucionaron por **trayectorias
fenotipo-específicas y mecanísticamente coherentes**, y la progresión se predijo con un modelo parsimonioso, normado
localmente. Cuatro puntos merecen énfasis.

**Primero, el eje del riesgo es el compromiso de memoria.** El análisis híbrido —banda funcional (clínica) × subtipo
objetivo (z)— mostró un riesgo varias veces mayor con memoria comprometida (31% vs 4%; OR 9,8), y la trayectoria por test lo confirmó
a nivel mecanístico: el amnésico declina en memoria episódica diferida (firma temporal-medial),[7] el disejecutivo en
velocidad/ejecutivo, el multidominio de forma amplia. Que el multidominio sea 89% amnésico y que ningún normal progresara
directamente refuerzan un modelo por estadios amnésico-céntrico. El almacenamiento comprometido es la firma definitoria
del subtipo, no un predictor independiente.

**Segundo, la interpretación del cambio seriado exige psicometría de cambio fiable.** La regresión a la media y el
**efecto de piso** distorsionan el cambio crudo: en una clínica de memoria, los tests de memoria diferida están
saturados al basal y parecen “estables” por censura. El RCI regression-based y el manejo explícito del piso son
imprescindibles; sin ellos, el análisis ingenuo invierte el orden real de los pronósticos. Aportamos, además, normas
locales de cambio fiable, de las primeras para esta población.

**Tercero, un modelo pre-especificado de dos variables ofrece utilidad de rutina, y se sostiene con criterio funcional.**
Recuerdo diferido y edad predijeron la progresión (AUC 0,74), sobre todo como **prueba de descarte** (VPN 93%); su
robustez frente a un desenlace con criterio funcional independiente (ADLQ, AUC 0,84) responde a la crítica central de que
“severidad ≥ moderada” no es demencia. Los cuestionarios de ánimo y quejas no aportaron discriminación, aunque sí valor
descriptivo. A los recuentos de eventos de una clínica única, el techo lo fija el tamaño muestral y la ausencia de
biomarcadores más que el algoritmo —consistente con extraer el máximo de **medidas de rutina**.[23–25]

**Cuarto, productos digitales abiertos.** El trabajo se materializa en dos herramientas de acceso abierto que corren
íntegramente en el navegador (sin transmitir datos): un **simulador de riesgo** individual (calculadora client-side) y un
**artefacto navegable de trayectoria cognitiva** (heatmaps por test × severidad/fenotipo y tabla maestra ordenable), que
llevan la descripción y la predicción a la consulta y a la comunidad de neurología cognitiva.

El estudio tiene **fortalezas**: datos genuinos de mundo real, depuración e identificación cuidadosas con recuperación
auditada de N, una variable perfil reproducible, psicometría de cambio fiable, validación interna rigurosa reportada
según TRIPOD/STROBE, y liberación abierta de código y herramientas. Las **limitaciones** acotan las conclusiones a un
nivel exploratorio: (i) muestra modesta, eventos escasos (el subgrupo DCL, 18 eventos, es un prototipo); (ii) desenlace
sin criterio funcional universal (mitigado por la sensibilidad ADLQ, de cobertura parcial ~50% y linkeo por nombre);
(iii) sesgo de selección de quiénes se reevalúan y **censura informativa** → la tasa es un **límite inferior**, el riesgo
competitivo de muerte no se modeló; (iv) desenlace binario a seguimiento variable (un modelo de tiempo-al-evento es el
paso siguiente); (v) codificación por IA = extracción de texto, con fiabilidad LLM–LLM (pendiente validación vs experto);
(vi) sin biomarcadores ni etiología (se predice **trayectoria, no enfermedad**). La **validación externa** —en consorcios
regionales y frente a biomarcadores en sangre[25]— es el paso esencial.

## Conclusiones
Los perfiles cognitivos evolucionan por trayectorias fenotipo-específicas en las que el compromiso de memoria es el eje
del riesgo; el amnésico declina en memoria episódica diferida, el disejecutivo en velocidad/ejecutivo. La progresión a un
deterioro de rango demencial es predecible con memoria diferida y edad, útil como prueba de descarte y robusta con
criterio funcional. Se aportan dos productos digitales abiertos. Hallazgos exploratorios y unicéntricos; el desenlace no
equivale a demencia confirmada y se requiere validación externa.

---

## Tablas

**Tabla 1. Cohorte, depuración y fiabilidad/validez del perfil.**

| Variable | Reevaluación (n = 254) | Una visita (n = 2644) |
|---|---|---|
| Edad, años (media ± DE) | 66,9 ± 14,3 | 63,8 ± 19,1 |
| Educación, años (media ± DE) | 13,4 ± 3,4 | 12,8 ± 3,7 |
| Sexo femenino, % | 56 | 56 |
| Seguimiento, años, mediana (IQR) | 1,83 (1,25–2,97) | — |

*Depuración:* 81 duplicados mismo día (hash), 3 sin fecha; 63 perfiles + 4 reevaluaciones recuperados → **219 analizables**
(basal+final). *Fiabilidad (κ, extracción LLM–LLM):* severidad 1,00; subtipo 0,88. *Falsos positivos:* solo 2/121 DCL
codificados sin deterioro objetivo (z ≤ −1,5).

**Tabla 2. Rendimiento de los modelos (TRIPOD; validación interna).**

| Desenlace / cohorte | n / eventos | Predictores | AUC [IC95%] | EPV |
|---|---|---|---|---|
| **Rango demencial — leve-moderado (primario)** | 140 / 37 | Memoria de relatos diferida + edad | **0,74** [0,54–0,92] | 18,5 |
| Rango demencial — subgrupo DCL (sensibilidad) | 96 / 18 | Memoria de relatos diferida + edad | 0,76 [0,53–1,0] | 9,0 |
| Rango demencial — **criterio funcional ADLQ ≥40%** | 68 / 11 | Memoria + edad | 0,84 [0,62–1,0] | — |
| Declive cognitivo fiable | 250 / 47 | edad, Rey trial 1, intrusiones, CI premórbido, Hayling | 0,68 [0,52–0,83] | 9,4 |

*AUC por CV anidada, optimismo-corregido; calibración Platt. Riesgo por tercil 7%/33%/43%; VPN 93%. Añadir GDS/CQC no
mejoró el AUC. El modelo desplegado (memoria + edad) coincide en n/eventos/coeficientes con esta tabla.*

## Figuras

**Figura 1. Flujo de la cohorte y depuración.** ![Figura 1](Fig1_flujo.png)
*334 con ≥2 evaluaciones → 84 excluidos (81 duplicados de hash + 3 sin fecha) → 254 reevaluaciones (con 4 recuperadas);
63 perfiles recuperados del PDF → 219 analizables; cohortes DCL (96) y leve-moderado (140).*

**Figura 2. Matriz de transición de severidad (basal → reevaluación).** ![Figura 2](Fig2_transiciones.png)

**Figura 3. El compromiso de memoria es el eje del riesgo (subtipo objetivo).** ![Figura 3](Fig3_subtipos.png)

**Figura 4. Regresión a la media.** ![Figura 4](Fig4_regresion.png)

**Figura 5. Rendimiento del modelo (memoria + edad).** ![Figura 5](Fig5_rendimiento.png)

**Figura 6. Simulador de riesgo desplegado (client-side).** ![Figura 6](Figure3.png)
*Prototipo de investigación, no validado para decisión clínica. https://fermarquez88.github.io/kaizenai-demencia/*

**Figura 7. Trayectoria cognitiva por test × fenotipo (% con declive fiable).** ![Figura 7](Fig7_trayectoria.png)
*% de pacientes con declive fiable (RCI regression-based ≤ −1,645) en cada test, por fenotipo basal (multidominio dividido
amnésico/no-amnésico; excluidos los ya-en-piso al basal). El amnésico declina en memoria episódica diferida; el
disejecutivo en velocidad/ejecutivo; el amnésico-multidominio de forma amplia; el preservado permanece estable. Versión
navegable como artefacto abierto.*

---

## Referencias
*Recuperadas y verificadas vía PubMed. Se incluye DOI.*

1. Petersen RC, Smith GE, Waring SC, et al. Mild cognitive impairment: clinical characterization and outcome. *Arch Neurol.* 1999. https://doi.org/10.1001/archneur.56.3.303
2. Petersen RC, Doody R, Kurz A, et al. Current concepts in mild cognitive impairment. *Arch Neurol.* 2001. https://doi.org/10.1001/archneur.58.12.1985
3. Winblad B, Palmer K, Kivipelto M, et al. Mild cognitive impairment — beyond controversies, towards a consensus. *J Intern Med.* 2004. https://doi.org/10.1111/j.1365-2796.2004.01380.x
4. Ganguli M, Snitz BE, Saxton JA, et al. Outcomes of mild cognitive impairment by definition: a population study. *Arch Neurol.* 2011. https://doi.org/10.1001/archneurol.2011.101
5. Espinosa A, Alegret M, Valero S, et al. A longitudinal follow-up of 550 mild cognitive impairment patients. *J Alzheimers Dis.* 2013. https://doi.org/10.3233/JAD-122002
6. Allegri RF, Glaser FB, Taragano FE, Buschke H. Mild cognitive impairment: believe it or not? *Int Rev Psychiatry.* 2008. https://doi.org/10.1080/09540260802095099
7. Sarazin M, Berr C, De Rotrou J, et al. Amnestic syndrome of the medial temporal type identifies prodromal AD: a longitudinal study. *Neurology.* 2007. https://doi.org/10.1212/01.wnl.0000279336.36610.f7
8. Gainotti G, Quaranta D, Vita MG, Marra C. Neuropsychological predictors of conversion from MCI to Alzheimer's disease. *J Alzheimers Dis.* 2014. https://doi.org/10.3233/JAD-130881
9. Modrego PJ. Predictors of conversion to dementia of probable Alzheimer type in patients with MCI. *Curr Alzheimer Res.* 2006. https://doi.org/10.2174/156720506776383103
10. García-Herranz S, Díaz-Mardomingo MC, Peraita H. Neuropsychological predictors of conversion to probable Alzheimer disease in elderly with MCI. *J Neuropsychol.* 2016. https://doi.org/10.1111/jnp.12067
11. López ME, Turrero A, Cuesta P, et al. A multivariate model of time to conversion from MCI to Alzheimer's disease. *GeroScience.* 2020. https://doi.org/10.1007/s11357-020-00260-7
12. Park HK, Choi SH, Park SA, et al. Memory performance on the story recall test and prediction of progression in MCI and Alzheimer's dementia. *Geriatr Gerontol Int.* 2017. https://doi.org/10.1111/ggi.12940
13. Bao J, Wang Y, Qu D, et al. Impairment of delayed recall as a predictor of amnestic MCI development in normal older adults. *BMC Psychiatry.* 2023. https://doi.org/10.1186/s12888-023-05309-3
14. Bondi MW, Edmonds EC, Jak AJ, et al. Neuropsychological criteria for MCI improves diagnostic precision, biomarker associations, and progression rates. *J Alzheimers Dis.* 2014. https://doi.org/10.3233/JAD-140276
15. Jak AJ, Preis SR, Beiser AS, et al. Neuropsychological criteria for MCI and dementia risk in the Framingham Heart Study. *J Int Neuropsychol Soc.* 2016. https://doi.org/10.1017/S1355617716000199
16. Wong CG, Thomas KR, Edmonds EC, et al. Neuropsychological criteria for MCI in the Framingham Heart Study's old-old. *Dement Geriatr Cogn Disord.* 2018. https://doi.org/10.1159/000493541
17. Lee YC, Kang JM, Lee H, et al. Amnestic multiple cognitive domains impairment and periventricular WMH predict progression to dementia in MCI. *Int J Geriatr Psychiatry.* 2016. https://doi.org/10.1002/gps.4035
18. Persson K, Eldholm RS, Barca ML, et al. Visual evaluation of medial temporal lobe atrophy as a marker of conversion from MCI to dementia. *Dement Geriatr Cogn Disord.* 2017. https://doi.org/10.1159/000477342
19. Mortimer JA, Borenstein AR, Gosche KM, Snowdon DA. Very early detection of Alzheimer neuropathology and the role of brain reserve. *J Geriatr Psychiatry Neurol.* 2005. https://doi.org/10.1177/0891988705281869
20. Taragano FE, Allegri RF, Lyketsos C. Mild behavioral impairment: a prodromal stage of dementia. *Dement Neuropsychol.* 2008. https://doi.org/10.1590/S1980-57642009DN20400004
21. Livingston G, Huntley J, Sommerlad A, et al. Dementia prevention, intervention, and care: 2020 report of the Lancet Commission. *Lancet.* 2020. https://doi.org/10.1016/S0140-6736(20)30367-6
22. Livingston G, Huntley J, Liu KY, et al. Dementia prevention, intervention, and care: 2024 report of the Lancet standing Commission. *Lancet.* 2024. https://doi.org/10.1016/S0140-6736(24)01296-0
23. Parra MA, Baez S, Allegri R, et al. Dementia in Latin America: assessing the present and envisioning the future. *Neurology.* 2018. https://doi.org/10.1212/WNL.0000000000004897
24. Maito MA, Santamaría-García H, Moguilner S, et al. Classification of Alzheimer's disease and frontotemporal dementia using routine clinical and cognitive measures across multicentric underrepresented samples. *Lancet Reg Health Am.* 2022. https://doi.org/10.1016/j.lana.2022.100387
25. Caviedes A, et al. Blood-based AT(N) biomarkers for Alzheimer's disease and frontotemporal lobar degeneration in Latin America. *Nat Aging.* 2026. https://doi.org/10.1038/s43587-025-01061-3
26. Jacobson NS, Truax P. Clinical significance: a statistical approach to defining meaningful change in psychotherapy research. *J Consult Clin Psychol.* 1991. https://doi.org/10.1037/0022-006X.59.1.12
27. Tröster AI, Woods SP, Morgan EE. Assessing cognitive change in Parkinson's disease: practice effect-corrected reliable change indices. *Arch Clin Neuropsychol.* 2007. https://doi.org/10.1016/j.acn.2007.05.004
28. Collins GS, Reitsma JB, Altman DG, Moons KGM. Transparent reporting of a multivariable prediction model (TRIPOD). *Ann Intern Med.* 2015. https://doi.org/10.7326/M14-0697
