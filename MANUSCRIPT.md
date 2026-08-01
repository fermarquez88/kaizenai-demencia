# Evolución de los perfiles neuropsicológicos y predicción de la progresión a demencia en una clínica de memoria argentina: estudio longitudinal de mundo real

**Congreso Argentino de Neurología (CAN)** · Área temática: **Neurología Cognitiva, Demencias y Neuropsicología** · Tipo: Tema libre (oral/póster)

**Autores:** Fernando Márquez (MD)¹; Diana Bruno (Lic.)¹; [coautores]. ¹ Instituto de Neurociencias San Juan (Clínica El Castaño), San Juan, Argentina.
**Autor de correspondencia:** F. Márquez — fmarquez.mum@gmail.com

**Código y calculadora (acceso abierto):** https://github.com/fermarquez88/kaizenai-demencia · App: https://fermarquez88.github.io/kaizenai-demencia/

> Las referencias fueron recuperadas y verificadas mediante **PubMed**; se incluye el DOI de cada cita.

---

## Resumen (estructurado)

**Introducción y objetivos.** Cómo evolucionan los distintos perfiles neuropsicológicos en la práctica real de una
clínica de memoria —y si esa evolución puede predecirse desde la evaluación basal— está poco caracterizado en
Latinoamérica, región históricamente subrepresentada en la investigación de demencias. Los objetivos fueron:
(1) describir la evolución longitudinal de los perfiles cognitivos en una cohorte argentina de mundo real, y
(2) derivar y validar internamente modelos parsimoniosos, normados localmente, que predigan la progresión a demencia.

**Materiales y métodos.** Estudio longitudinal retrospectivo de adultos con ≥2 evaluaciones neuropsicológicas en fechas
distintas en un único instituto (2020–2026). El perfil (banda de severidad, fenotipo dominante, mecanismo de memoria)
se extrajo de la sección Conclusiones del informe firmado mediante un codebook, con validación de **fiabilidad**
(doble codificación independiente) y de **validez de constructo** (contra un patrón z objetivo). Las trayectorias se
analizaron con cambio **ajustado por el basal** (residuo ANCOVA) y con un **Índice de Cambio Fiable (RCI)** derivado
localmente. La progresión a demencia se definió como severidad final ≥ moderada. Los modelos pronósticos emplearon
regresión logística penalizada con validación cruzada anidada, corrección de optimismo por bootstrap y calibración de
Platt, reportados según TRIPOD.

**Resultados.** De 334 pacientes con múltiples visitas, 250 tuvieron una reevaluación genuina (mediana de seguimiento
1,8 años). La codificación del perfil fue altamente reproducible (severidad κ=1,00; fenotipo κ=0,88) y creció de forma
monótona con el z objetivo. Tras el ajuste por el basal —obligatorio dada la fuerte **regresión a la media**
(r basal–final=0,26)— los fenotipos **amnésico** y **multidominio** y el **almacenamiento comprometido** predijeron
declive fiable (43–47% y 44%), mientras que los perfiles **disejecutivo**, **preservado** y **con modulador anímico**
siguieron cursos benignos (17–22%). Ningún paciente progresó **directamente de cognición normal a demencia**: la
progresión siempre atravesó un estadio intermedio. Se aportan normas locales de cambio (RCI global ≈0,97 z). La
progresión a demencia se predijo mejor con **memoria de relatos diferida y edad** (DCL→demencia AUC 0,84 [IC95%
0,54–1,0]; pre-demencia→demencia 0,81 [0,66–0,93]); los modelos parsimoniosos superaron a la selección de alta dimensión.

**Conclusiones.** Los perfiles cognitivos evolucionan por caminos fenotipo-específicos y biológicamente coherentes que
quedan ocultos si el cambio no se ajusta por el basal. Un modelo de dos variables —recuerdo diferido de relatos más
edad— predice la progresión a demencia con un rendimiento comparable al de modelos publicados basados en
neuropsicología, y se despliega como calculadora abierta que preserva la privacidad. Se requiere validación externa.

**Palabras clave:** deterioro cognitivo leve; demencia; neuropsicología; predicción; Latinoamérica; índice de cambio fiable.

---

## Introducción

El deterioro cognitivo leve (DCL) es una construcción heterogénea cuyo desenlace depende fuertemente de cómo se lo
defina y del fenotipo cognitivo subyacente.[1,2] Estudios poblacionales y de clínica muestran que una proporción
sustancial de pacientes rotulados como DCL progresa a demencia mientras otros permanecen estables o revierten, y que
los subtipos amnésico y no-amnésico conllevan pronósticos distintos.[1,3] La controversia sobre las tasas de conversión
y la propia identidad del DCL ha sido señalada tempranamente por autores de nuestra región.[4] En consecuencia, es el
**perfil neuropsicológico** —y no la mera presencia de deterioro— lo central para el pronóstico.

Una literatura consistente identifica a la memoria episódica, y en particular al **recuerdo diferido**, como el
predictor neuropsicológico más potente de conversión de DCL a enfermedad de Alzheimer.[5–10] El recuerdo diferido de
relatos (memoria lógica) y de listas supera repetidamente a las medidas de cribado global para anticipar la
progresión,[9,10] y los criterios neuropsicológicos actuariales mejoran la estratificación del riesgo por encima de las
definiciones convencionales.[11] El compromiso amnésico multidominio, la atrofia temporal medial y la carga vascular
incrementan el riesgo,[3,12,13] mientras que la **reserva cognitiva/cerebral** modifica la expresión clínica de una
misma carga de patología.[14] Los síntomas conductuales/anímicos, además, pueden constituir un pródromo
propio.[15] Sin embargo, la mayor parte de esta evidencia proviene de cohortes de investigación de países de altos
ingresos, con baterías fijas y seguimiento protocolizado.

Dos vacíos motivan este trabajo. Primero, la **evolución longitudinal de los perfiles en la práctica de rutina**
—cómo cambian los fenotipos amnésico, disejecutivo, multidominio y preservado a lo largo del seguimiento clínico
habitual— rara vez se ha descripto con el cuidado metodológico que exigen los datos cognitivos seriados (umbrales de
cambio fiable, ajuste por regresión a la media). Segundo, **Latinoamérica está marcadamente subrepresentada** en la
investigación de demencias; las herramientas diagnósticas y pronósticas validadas en otros contextos transfieren mal
ante diferencias de educación, normas locales y acceso, y las iniciativas regionales enfatizan la necesidad de
instrumentos desarrollados localmente a partir de **medidas clínicas de rutina**.[16,17]

Por ello utilizamos una cohorte longitudinal de mundo real de una única clínica de memoria argentina para
(1) describir, con atención explícita al cambio fiable y al ajuste por el basal, cómo evolucionan los distintos
perfiles neuropsicológicos; y (2) derivar, validar internamente y desplegar de forma abierta modelos parsimoniosos y
normados localmente que predigan la progresión a demencia desde la evaluación basal.

## Materiales y métodos

### Aspectos éticos
Análisis retrospectivo de datos clínicos de rutina, anonimizados por un identificador a nivel persona derivado del
documento nacional de identidad. No se comparten datos identificatorios.

### Diseño y cohorte
Se incluyeron adultos evaluados entre 2020 y 2026 con **≥2 evaluaciones neuropsicológicas en fechas distintas**
(reevaluación genuina). Se excluyeron evaluaciones pediátricas. Como los archivos contenían informes duplicados del
mismo día (la misma evaluación archivada con el nombre en distinto orden), se depuró por (persona, fecha); la identidad
se resolvió por DNI, nunca por nombre (lo que además captó cambios de apellido).

### Evaluación neuropsicológica y codificación del perfil
Las baterías se adaptaron al motivo de consulta e incluyeron instrumentos normados localmente (ACE-III, INECO Frontal
Screening [IFS], Lista de Rey [RAVLT], Memoria de Relatos, Figura de Rey, fluencias verbales, dígitos, Hayling, CI
premórbido). El **perfil** se operacionalizó desde la sección *Conclusiones* mediante un codebook que capturó una
**banda de severidad** ordinal (normal < leve [DCL] < leve-a-moderado < moderado < moderado-grave < grave), el
**fenotipo dominante** (amnésico, disejecutivo, mixto, multidominio, lenguaje, visuoespacial, preservado), el
**mecanismo de memoria** (almacenamiento comprometido vs. conservado), marcadores de error (intrusiones) y moduladores
señalados por el clínico (ánimo, sueño). La codificación se realizó con un modelo de lenguaje restringido por el
codebook. La **fiabilidad** se evaluó por una segunda codificación independiente y ciega de una muestra estratificada
(n=42; κ de Cohen, ponderada cuadrática para la severidad ordinal). La **validez de constructo** se evaluó contra un
patrón z objetivo (número de dominios deficitarios de la batería).

### Desenlaces y cambio fiable
Desenlace primario: **progresión a demencia**, definida como banda de severidad final ≥ *moderada* (criterio clínico
del instituto, por el cual el “deterioro cognitivo moderado” denota un síndrome de rango demencial). Las cohortes se
definieron por la severidad **basal**: “DCL” (basal = leve) y “pre-demencia” (basal normal/leve/leve-a-moderado).
Desenlace secundario: **declive cognitivo fiable**, cambio de z global que supera un **RCI** derivado localmente
(RCI ≈ 1,96 × desvío robusto del cambio en pares estables ≈ 0,97 z). Se estimaron RCIs por dominio y por test
(MAD robusta; z winsorizados a [−6, 4] para eliminar artefactos de piso de los tests cronometrados).

### Análisis estadístico
El cambio se resumió en un índice z global (media de cinco dominios core). Como el cambio cognitivo seriado está
confundido por la **regresión a la media**, se modeló el puntaje final sobre el basal (ANCOVA) y se usó el **residuo**
como cambio ajustado; las tasas de declive por fenotipo usan esta métrica ajustada. Los modelos pronósticos usaron
**regresión logística penalizada** (L2 para los modelos desplegados; L1 para selección), con imputación por mediana +
indicadores de faltante y estandarización **dentro** de la validación cruzada. El rendimiento se estimó por
**validación cruzada anidada repetida** (5×20) con ajuste interno de hiperparámetros y por **corrección de optimismo por
bootstrap** (Steyerberg); las cohortes pequeñas usaron además LOOCV. Las probabilidades se **recalibraron (Platt)** y se
reportan con Brier y pendiente/intercepto de calibración. La robustez de las variables se evaluó por **stability
selection** (L1 sobre bootstraps). Las bandas de incertidumbre por paciente provienen de 200 modelos bootstrap
exportados a la calculadora. El reporte sigue **TRIPOD**.[18] Una implementación en JavaScript reproduce exactamente los
coeficientes (test de paridad).

## Resultados

### Cohorte y variable perfil (Tabla 1)
De 334 pacientes con más de una evaluación archivada, 81 tenían todas las evaluaciones el mismo día (duplicados) y 250
tuvieron una reevaluación genuina en ≥2 fechas distintas (mediana de seguimiento 1,83 años; IQR 1,25–2,97). Quienes
volvieron para reevaluación fueron mayores que los de una sola visita (66,9 vs 63,3 años) con severidad basal
comparable, lo que indica vigilancia guiada por la edad y la sospecha clínica más que por la gravedad.

El perfil codificado fue **altamente reproducible** entre dos codificaciones independientes (severidad κ=1,00, acuerdo
exacto 100%; almacenamiento κ=0,96; fenotipo κ=0,88; estabilidad longitudinal κ=0,85) y mostró fuerte **validez de
constructo**: el número medio de dominios deficitarios de la batería creció de forma monótona a través de las bandas de
severidad codificada (normal 0,44 → leve 1,98 → moderado 3,83 → grave 4,50), y la proporción con deterioro objetivo
subió de 29% (normal) a 100% (≥ leve-a-moderado). Estos resultados avalan el uso del perfil como desenlace.

### La evolución de los perfiles solo se interpreta tras ajustar por el basal (Figura 1)
En el seguimiento, 33% empeoró ≥1 banda, 55% permaneció estable y 13% mejoró. Sin embargo, el cambio seriado estuvo
dominado por la **regresión a la media**: la correlación basal–final del z global fue de solo 0,26, de modo que quien
partía de “normal” solo podía empeorar y quien partía de “grave” solo podía mejorar. En la métrica **cruda** el
fenotipo amnésico parecía plano (Δz≈0,00); su declive emergió **únicamente tras el ajuste por el basal**.

Las tasas de declive fiable ajustadas por el basal difirieron marcadamente por **fenotipo basal**: multidominio 47%,
**amnésico 43%**, disejecutivo 22% y **preservado 0%** (Figura 1). A nivel mecanístico, el **almacenamiento
comprometido** (firma amnésica de tipo hipocampal) predijo declive (Δz ajustado −0,39; 44% de declive fiable) mientras
que el **almacenamiento conservado** (tipo recuperación) siguió un curso benigno (+0,41; 18%). Los perfiles con
**modulador anímico** señalado al basal declinaron aproximadamente la mitad (17% vs 34%), consistente con un curso
parcialmente reversible y no degenerativo. El juicio narrativo del clínico sobre la estabilidad concordó estrechamente
con el cambio cuantitativo ajustado por el basal (declive declarado: Δz ajustado −0,52; estable declarado: +0,84),
triangulando dos mediciones independientes.

### Ninguna transición directa de cognición normal a demencia
De 74 pacientes cuyo perfil final alcanzó el rango de demencia, **ninguno** era cognitivamente normal al basal
(0 normal→demencia). La progresión atravesó invariablemente un estadio intermedio (leve o leve-a-moderado), lo que
apoya un modelo por estadios y justifica tomar los estados pre-demencia —no los normales— como denominador del pronóstico.

### Normas locales de cambio fiable
Aportamos RCIs locales para el testeo seriado: ≈0,97 z a nivel persona y umbrales por test de ±1,4 (recuerdo diferido
de lista) a ±2,5 (reconocimiento), con 7–14% de pacientes mostrando declive fiable por dominio en el intervalo. Son,
hasta donde sabemos, de las primeras normas locales de cambio para esta población.

### Predicción de la progresión a demencia (Tabla 2, Figura 2)
En los tres desenlaces, **la parsimonia superó a la complejidad**. La stability selection de alta dimensión sobre ~40
variables dio menor AUC honesto que sets pequeños pre-especificados, y un modelo de árbol que parecía excelente por AUC
aparente (0,97) colapsó a ~0,66 bajo corrección de optimismo, evidenciando sobreajuste a este tamaño muestral. Los
mejores modelos honestos fueron:

- **DCL → demencia:** memoria de relatos diferida + edad — AUC 0,84 (concordante CV anidada/optimismo/LOOCV; IC95% 0,54–1,0; 16 eventos).
- **Pre-demencia → demencia:** + severidad basal — AUC 0,81 (IC95% 0,66–0,93; 32 eventos); beneficio clínico neto sobre “tratar a todos” en todo el rango de umbrales.
- **Declive fiable:** edad, Lista de Rey trial 1, intrusiones, CI premórbido, Hayling — AUC 0,69.

En todos, la **memoria (diferida) y la edad** dominaron (OR por DS: memoria ≈0,41; edad ≈1,7–2,0), recapitulando la
firma amnésica-más-edad de la conversión tipo-Alzheimer. Los modelos quedaron bien calibrados tras Platt. Los modelos
finales se despliegan como calculadora abierta que computa el riesgo con banda de incertidumbre bootstrap y **nunca
transmite datos del paciente** (Figura 3).

## Discusión

En una clínica de memoria argentina de mundo real, los distintos perfiles neuropsicológicos evolucionaron por
**trayectorias fenotipo-específicas y biológicamente coherentes**, y la progresión a demencia se predijo desde la
evaluación basal con un modelo notablemente **parsimonioso y normado localmente**. Tres hallazgos merecen énfasis.

Primero, **la evolución de los perfiles solo es interpretable tras corregir la regresión a la media.** En la métrica
cruda, el fenotipo amnésico —el de peor pronóstico— parecía permanecer plano; su verdadero declive emergió solo tras el
ajuste por el basal. No es un tecnicismo: los análisis ingenuos de cambio seriado en clínicas de memoria pueden invertir
el orden real de los pronósticos. El mismo fenómeno subyace a asociaciones “protectoras” que se disuelven bajo escrutinio
causal, como se demostró recientemente para el alcohol y la demencia, donde el declive cognitivo temprano reduce la
exposición (causalidad inversa).[19] Nuestro RCI local y las métricas ajustadas por el basal ofrecen un remedio práctico
y, junto con los RCIs corregidos por efecto de práctica,[20] sostienen que las normas de cambio fiable deberían acompañar
toda interpretación neuropsicológica seriada.

Segundo, **los caminos fenotipo-específicos son mecanísticamente sensatos.** Los fenotipos amnésico y multidominio, y en
particular el **almacenamiento comprometido**, predijeron declive, mientras que los disejecutivos y con modulador anímico
siguieron cursos benignos. Esto refleja la distinción clásica entre falla de almacenamiento (hipocampal, tipo-Alzheimer)
y de recuperación (frontal), y concuerda con la evidencia de que el recuerdo diferido es el predictor por excelencia de la
conversión DCL→EA.[5–10] El curso benigno de los perfiles con carga anímica es consistente con el deterioro cognitivo
reversible del trastorno afectivo de la vejez y con la noción del compromiso conductual como pródromo diferenciable,[15]
y advierte contra equiparar el deterioro actual con una trayectoria inexorable. Que **ningún paciente pasara de cognición
normal directamente a demencia** en ~2 años refuerza un modelo por estadios y tiene una implicancia metodológica concreta:
los estados pre-demencia, no los individuos normales, son la población apropiada para la predicción de demencia a corto plazo.

Tercero, **para predecir, menos fue más.** Un modelo de dos variables —recuerdo diferido de relatos más edad— predijo la
progresión DCL→demencia con un AUC optimismo-corregido de 0,84, comparable o superior a modelos publicados basados en
neuropsicología que usan baterías mayores,[5–10] y un modelo de pre-demencia agregó solo la severidad basal para alcanzar
0,81 con beneficio clínico neto demostrable. Los intentos de mejorarlo con selección de alta dimensión no ayudaron y a
veces perjudicaron, y la aparente excelencia de un árbol resultó ser memorización. A los recuentos de eventos típicos de
una clínica única, el techo de la discriminación lo fija el tamaño muestral y la ausencia de biomarcadores más que la
sofisticación algorítmica —consistente con la prioridad regional de extraer el máximo valor pronóstico de **medidas
cognitivas de rutina** mientras se expande el acceso a biomarcadores.[16,17] La parsimonia emergente es también lo que
vuelve usable la herramienta: cada input se transcribe de un informe estándar y la inferencia corre íntegramente en el
navegador, preservando la privacidad.

El estudio tiene **fortalezas**: datos genuinos de mundo real, depuración e identificación cuidadosas, una variable perfil
reproducible y altamente fiable validada contra puntajes objetivos, validación interna metodológicamente rigurosa
(CV anidada, corrección de optimismo, calibración, análisis de curva de decisión) reportada según TRIPOD,[18] y liberación
abierta del código y de una calculadora desplegada.

Las **limitaciones** son relevantes. La muestra es modesta y los eventos escasos —en particular para el modelo DCL→demencia
(16 eventos), cuyo IC es amplio; debe considerarse un **prototipo** validado internamente. La cohorte generaliza a quienes
regresan a reevaluarse, subgrupo no aleatorio y de mayor edad con posible gradiente de acceso. Excluimos deliberadamente el
diagnóstico etiológico: los modelos predicen **trayectoria cognitiva, no enfermedad**, y la definición de demencia se apoya
en el juicio de severidad del clínico sin criterio funcional independiente. La deriva de la documentación de mundo real y la
ausencia de biomarcadores acotan aún más el rendimiento. La **validación externa** —idealmente en consorcios regionales y
frente a los biomarcadores en sangre que hoy se caracterizan en Latinoamérica[17]— es el paso esencial, junto con la
recalibración periódica a medida que crezca la cohorte.

## Conclusiones
En la práctica de rutina de una clínica de memoria argentina, los perfiles cognitivos evolucionan por trayectorias
fenotipo-específicas y mecanísticamente coherentes que se enmascaran sin ajuste por el basal, y la progresión a demencia es
predecible a partir de una combinación parsimoniosa y normada localmente de memoria diferida y edad. Desplegado como
calculadora abierta que preserva la privacidad, esto ofrece una ayuda pronóstica transparente y de uso inmediato para
entornos subrepresentados —a la espera de validación externa.

---

## Tablas

**Tabla 1.** Características de la cohorte y fiabilidad/validez del perfil (n=250; seguimiento mediano 1,8 a; κ severidad
1,00, almacenamiento 0,96, fenotipo 0,88; validez: dominios deficitarios 0,44 [normal] → 4,50 [grave]).

**Tabla 2.** Rendimiento de los modelos pronósticos (TRIPOD): desenlace, cohorte, predictores, n/eventos, AUC (CV anidada,
optimismo-corregido) con IC95%, calibración.

## Leyendas de figuras

**Figura 1.** Tasa de declive fiable ajustada por el basal según fenotipo basal (multidominio 47%, amnésico 43%,
disejecutivo 22%, preservado 0%) y según almacenamiento de memoria (comprometido 44% vs conservado 18%).

**Figura 2.** Discriminación (AUC) de los tres desenlaces con IC95%; estimaciones honestas (optimismo-corregidas) vs
aparentes, con el sobreajuste del árbol en conversión de banda.

**Figura 3.** Calculadora de riesgo desplegada (client-side): al seleccionar la severidad basal aparecen el modelo
aplicable y sus campos; el riesgo se muestra con banda de incertidumbre bootstrap y la prevalencia de la cohorte.

---

## Referencias
*Recuperadas y verificadas vía PubMed. Se incluye DOI.*

1. Ganguli M, Snitz BE, Saxton JA, et al. Outcomes of mild cognitive impairment by definition: a population study. *Arch Neurol.* 2011. https://doi.org/10.1001/archneurol.2011.101
2. Ganguli M. Mild cognitive impairment and the 7 uses of epidemiology. *Alzheimer Dis Assoc Disord.* 2006. https://doi.org/10.1097/00002093-200607001-00007
3. Espinosa A, Alegret M, Valero S, et al. A longitudinal follow-up of 550 mild cognitive impairment patients: evidence for large conversion to dementia rates and detection of major risk factors. *J Alzheimers Dis.* 2013. https://doi.org/10.3233/JAD-122002
4. Allegri RF, Glaser FB, Taragano FE, Buschke H. Mild cognitive impairment: believe it or not? *Int Rev Psychiatry.* 2008. https://doi.org/10.1080/09540260802095099
5. Gainotti G, Quaranta D, Vita MG, Marra C. Neuropsychological predictors of conversion from mild cognitive impairment to Alzheimer's disease. *J Alzheimers Dis.* 2014. https://doi.org/10.3233/JAD-130881
6. Modrego PJ. Predictors of conversion to dementia of probable Alzheimer type in patients with mild cognitive impairment. *Curr Alzheimer Res.* 2006. https://doi.org/10.2174/156720506776383103
7. García-Herranz S, Díaz-Mardomingo MC, Peraita H. Neuropsychological predictors of conversion to probable Alzheimer disease in elderly with mild cognitive impairment. *J Neuropsychol.* 2016. https://doi.org/10.1111/jnp.12067
8. López ME, Turrero A, Cuesta P, et al. A multivariate model of time to conversion from mild cognitive impairment to Alzheimer's disease. *GeroScience.* 2020. https://doi.org/10.1007/s11357-020-00260-7
9. Park HK, Choi SH, Park SA, et al. Memory performance on the story recall test and prediction of cognitive dysfunction progression in mild cognitive impairment and Alzheimer's dementia. *Geriatr Gerontol Int.* 2017. https://doi.org/10.1111/ggi.12940
10. Bao J, Wang Y, Qu D, et al. Impairment of delayed recall as a predictor of amnestic mild cognitive impairment development in normal older adults: a 7-year longitudinal cohort study. *BMC Psychiatry.* 2023. https://doi.org/10.1186/s12888-023-05309-3
11. Jak AJ, Preis SR, Beiser AS, et al. Neuropsychological criteria for mild cognitive impairment and dementia risk in the Framingham Heart Study. *J Int Neuropsychol Soc.* 2016. https://doi.org/10.1017/S1355617716000199
12. Lee YC, Kang JM, Lee H, et al. Amnestic multiple cognitive domains impairment and periventricular white matter hyperintensities are independently predictive factors of progression to dementia in mild cognitive impairment. *Int J Geriatr Psychiatry.* https://doi.org/10.1002/gps.4035
13. Persson K, Eldholm RS, Barca ML, et al. Visual evaluation of medial temporal lobe atrophy as a clinical marker of conversion from mild cognitive impairment to dementia. *Dement Geriatr Cogn Disord.* 2017. https://doi.org/10.1159/000477342
14. Mortimer JA, Borenstein AR, Gosche KM, Snowdon DA. Very early detection of Alzheimer neuropathology and the role of brain reserve in modifying its clinical expression. *J Geriatr Psychiatry Neurol.* 2005. https://doi.org/10.1177/0891988705281869
15. Taragano FE, Allegri RF, Lyketsos C. Mild behavioral impairment: a prodromal stage of dementia. *Dement Neuropsychol.* 2008. https://doi.org/10.1590/S1980-57642009DN20400004
16. Parra MA, Baez S, Allegri R, et al. Dementia in Latin America: assessing the present and envisioning the future. *Neurology.* 2018. https://doi.org/10.1212/WNL.0000000000004897
17. Maito MA, Santamaría-García H, Moguilner S, et al. Classification of Alzheimer's disease and frontotemporal dementia using routine clinical and cognitive measures across multicentric underrepresented samples. *Lancet Reg Health Am.* 2022. https://doi.org/10.1016/j.lana.2022.100387
18. Caviedes A, et al. Blood-based AT(N) biomarkers for Alzheimer's disease and frontotemporal lobar degeneration in Latin America. *Nat Aging.* 2026. https://doi.org/10.1038/s43587-025-01061-3
19. Topiwala A, Levey DF, Zhou H, et al. Alcohol use and risk of dementia in diverse populations: cohort, case-control and Mendelian randomisation approaches. *BMJ Evid Based Med.* 2026. https://doi.org/10.1136/bmjebm-2025-113913
20. Tröster AI, Woods SP, Morgan EE. Assessing cognitive change in Parkinson's disease: development of practice effect-corrected reliable change indices. *Arch Clin Neuropsychol.* 2007. https://doi.org/10.1016/j.acn.2007.05.004

*Guía de reporte: Collins GS, Reitsma JB, Altman DG, Moons KGM. TRIPOD statement (2015).*
