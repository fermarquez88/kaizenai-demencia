# Evolución de los perfiles neuropsicológicos y predicción de la progresión a demencia en una clínica de memoria argentina: estudio longitudinal de mundo real

**Congreso Argentino de Neurología (CAN)** · Área temática: **Neurología Cognitiva, Demencias y Neuropsicología** · Tipo: Tema libre (oral/póster)

**Autores:** Fernando Márquez (MD)¹; Diana Bruno (Lic.)¹; [coautores]. ¹ Instituto de Neurociencias San Juan (Clínica El Castaño), San Juan, Argentina.
**Autor de correspondencia:** F. Márquez — fmarquez.mum@gmail.com

**Código y calculadora (acceso abierto):** https://github.com/fermarquez88/kaizenai-demencia · App: https://fermarquez88.github.io/kaizenai-demencia/

> Las referencias fueron recuperadas y verificadas mediante **PubMed**; se incluye el DOI de cada cita.

---

## Resumen (estructurado)

**Introducción y objetivos.** La evolución de los perfiles neuropsicológicos en la práctica real de una clínica de
memoria —y su predictibilidad desde la evaluación basal— está poco caracterizada en Latinoamérica, región
subrepresentada en la investigación de demencias. Nos propusimos (1) describir la evolución longitudinal de los
perfiles cognitivos en una cohorte argentina de mundo real y (2) derivar y validar internamente modelos
parsimoniosos, normados localmente, que predigan la progresión a demencia.

**Materiales y métodos.** Estudio longitudinal retrospectivo de adultos con ≥2 evaluaciones neuropsicológicas en
fechas distintas en un único instituto (2020–2026). Desde la sección *Conclusiones* del informe firmado se codificó,
mediante un codebook, un **perfil** con banda de severidad, subtipo cognitivo y mecanismo de memoria; se evaluaron su
**fiabilidad** (doble codificación ciega) y su **validez de constructo** (contra un patrón z objetivo). Los subtipos
se operacionalizaron según criterios de Petersen/Winblad a partir del **patrón objetivo de dominios** (memoria ×
número de dominios). El cambio se analizó ajustado por el basal (residuo ANCOVA) y con un **Índice de Cambio Fiable
(RCI)** derivado localmente. La progresión a demencia se definió como severidad final ≥ moderada. Los modelos
pronósticos usaron regresión logística penalizada con validación cruzada anidada, corrección de optimismo por
bootstrap y calibración de Platt, reportados según TRIPOD.

**Resultados.** De 334 pacientes con múltiples visitas, 250 tuvieron una reevaluación genuina (mediana de seguimiento
1,8 años). La codificación fue altamente reproducible (severidad κ=1,00; subtipo κ=0,88) y creció de forma monótona
con el z objetivo. El cambio seriado se ajustó por una **regresión a la media** moderada (pendiente final–basal 0,82,
r=0,73) y por un Índice de Cambio Fiable local; tras el ajuste, el perfil amnésico fue el que más declinó. La cohorte en riesgo estuvo **dominada por el subtipo amnésico multidominio**
(78%), que concentró la progresión a demencia (32%; IC95% 23–42); los subtipos de dominio único y no amnésicos fueron
infrecuentes y sin eventos, de modo que el gradiente fino entre subtipos resultó **infrapotenciado y dependiente de la
operacionalización** (el eje robusto del riesgo fue el compromiso de memoria, no la etiqueta categórica). El subtipo
amnésico se caracterizó por **compromiso del almacenamiento** (tipo temporal-medial; 93% de los casos amnésicos),
firma mecanística —no predictor independiente— del mayor riesgo. De 14 pacientes normales al basal, ninguno progresó a
demencia (0/14). La progresión se predijo con **memoria de relatos diferida y edad** (DCL→demencia AUC 0,84 [IC95%
0,54–1,0], 16 eventos; deterioro leve-moderado→demencia 0,80 [0,64–0,92], n=122); los modelos parsimoniosos igualaron
o superaron a la selección de alta dimensión.

**Conclusiones.** Los perfiles cognitivos evolucionan por trayectorias mecanísticamente coherentes que quedan ocultas
si el cambio no se ajusta por el basal, y en las que el **compromiso de memoria es el eje del riesgo**. Un modelo de
dos variables —recuerdo diferido de relatos y edad— predice la progresión a demencia con un rendimiento comparable al
de modelos publicados basados en neuropsicología, y se despliega como calculadora abierta que preserva la privacidad.
Los hallazgos son exploratorios y requieren validación externa.

**Palabras clave:** deterioro cognitivo leve; demencia; neuropsicología; predicción; Latinoamérica; índice de cambio fiable.

---

## Introducción

El deterioro cognitivo leve (DCL) es una entidad heterogénea cuyo desenlace depende de cómo se lo define y del
fenotipo cognitivo subyacente.[1–3] Desde su caracterización inicial como estado transicional con predominio de
compromiso de memoria,[1,2] el consenso internacional estableció que el DCL exige deterioro cognitivo objetivo con
**actividades de la vida diaria preservadas** —el rasgo que lo separa de la demencia— y reconoció subtipos amnésico y
no amnésico, de dominio único o múltiple, con pronósticos distintos.[3] Una proporción sustancial de pacientes
rotulados como DCL progresa a demencia mientras otros permanecen estables o revierten,[4,5] y la controversia sobre
las tasas de conversión y la propia identidad del DCL fue señalada tempranamente desde nuestra región.[6] Por ello es
el **perfil neuropsicológico** —y no la mera presencia de deterioro— lo central para el pronóstico.

Dentro de ese perfil, la memoria episódica ocupa un lugar privilegiado. El **síndrome amnésico de tipo
temporal-medial** —una falla de almacenamiento que el señalamiento (*cued recall*) no normaliza— identifica la
enfermedad de Alzheimer prodrómica con alta especificidad,[7] y el **recuerdo diferido** es, de forma consistente, el
predictor neuropsicológico más potente de conversión de DCL a Alzheimer.[7–13] El recuerdo diferido de relatos y de
listas supera repetidamente a las medidas de cribado global,[12,13] y los **criterios neuropsicológicos actuariales**
mejoran la estratificación del riesgo, reducen los falsos positivos y estabilizan el diagnóstico frente a las
definiciones convencionales.[14–16] El compromiso amnésico multidominio, la atrofia temporal medial y la carga
vascular incrementan el riesgo,[5,17,18] mientras que la **reserva cognitiva/cerebral** modula la expresión clínica de
una misma carga de patología,[19] y los síntomas conductuales o anímicos pueden constituir un pródromo propio.[20] La
mayor parte de esta evidencia, sin embargo, proviene de cohortes de investigación de países de altos ingresos, con
baterías fijas y seguimiento protocolizado.

Dos vacíos motivan este trabajo. Primero, la **evolución longitudinal de los perfiles en la práctica de rutina** rara
vez se describe con el cuidado metodológico que exigen los datos cognitivos seriados —umbrales de cambio fiable y
ajuste por regresión a la media—, pese a que la prevención de la demencia depende de identificar y actuar sobre la
trayectoria temprana.[21,22] Segundo, **Latinoamérica está marcadamente subrepresentada** en la investigación de
demencias; las herramientas validadas en otros contextos transfieren mal ante diferencias de educación, normas y
acceso, y las iniciativas regionales enfatizan la necesidad de instrumentos desarrollados localmente a partir de
**medidas clínicas de rutina**.[23–25]

Utilizamos, por tanto, una cohorte longitudinal de mundo real de una única clínica de memoria argentina para
(1) describir, con atención explícita al cambio fiable y al ajuste por el basal, cómo evolucionan los perfiles
neuropsicológicos; y (2) derivar, validar internamente y desplegar de forma abierta modelos parsimoniosos y normados
localmente que predigan la progresión a demencia desde la evaluación basal.

## Materiales y métodos

### Aspectos éticos
Análisis retrospectivo de datos clínicos de rutina, anonimizados mediante un identificador a nivel persona derivado del
documento nacional de identidad. No se comparten datos identificatorios.

### Diseño y cohorte
Se incluyeron adultos evaluados entre 2020 y 2026 con **≥2 evaluaciones neuropsicológicas en fechas distintas**
(reevaluación genuina). Se excluyeron evaluaciones pediátricas. Como los archivos contenían informes duplicados del
mismo día —la misma evaluación archivada con el nombre en distinto orden—, se depuró por (persona, fecha). La identidad
se resolvió por DNI, nunca por nombre, lo que además captó cambios de apellido.

### Evaluación neuropsicológica y codificación del perfil
Las baterías se adaptaron al motivo de consulta e incluyeron instrumentos normados localmente (ACE-III, INECO Frontal
Screening, Lista de Rey [RAVLT], Memoria de Relatos, Figura de Rey, fluencias verbales, dígitos, Hayling, CI
premórbido). El **perfil** se operacionalizó desde la sección *Conclusiones* mediante un codebook que capturó una
**banda de severidad** ordinal (normal < leve [DCL] < leve-a-moderado < moderado < moderado-grave < grave), el
**mecanismo de memoria** (almacenamiento comprometido vs. conservado), marcadores de error (intrusiones) y moduladores
señalados por el clínico (ánimo, sueño). La codificación se realizó con un modelo de lenguaje restringido por el
codebook. La **fiabilidad** se evaluó por una segunda codificación independiente y ciega de una muestra estratificada
(κ de Cohen, ponderada cuadrática para la severidad ordinal). La **validez de constructo** se contrastó con un patrón z
objetivo (número de dominios deficitarios de la batería, umbral z ≤ −2).

### Operacionalización de los subtipos de DCL
Para evitar la dependencia de una etiqueta narrativa única, los **subtipos** se derivaron del **patrón objetivo de
dominios** según los criterios operativos de Petersen/Winblad.[1–3] Un dominio se consideró afectado si su peor z era
≤ −1,5 (≥1 test); la afectación de memoria definió el eje amnésico/no amnésico y el número de dominios afectados
(uno vs. ≥2) definió el eje único/múltiple, generando cuatro subtipos (amnésico y no amnésico, de dominio único y
múltiple). Este esquema se aplicó en el basal de la cohorte en riesgo (severidad basal leve o leve-a-moderada). Como
análisis de concordancia se computaron, además, un esquema basado en los dominios señalados por el clínico y el
esquema previo basado en la etiqueta dominante.

### Desenlaces y cambio fiable
Desenlace primario: **progresión a deterioro moderado o mayor** (síndrome de rango demencial), definido como banda de
severidad final ≥ *moderada*. Dado que **no se aplicó un criterio funcional independiente** (compromiso de las
actividades de la vida diaria) para confirmar demencia, el desenlace se interpreta como progresión de severidad, no
como demencia confirmada (véase Limitaciones). Las cohortes se definieron por la severidad **basal**: “DCL” (basal =
leve) y “deterioro leve-moderado” (basal leve o leve-a-moderado); los pacientes con cognición basal normal se
analizaron por separado. Desenlace secundario: **declive cognitivo fiable**, cambio de z global que supera un **RCI**
derivado localmente (RCI ≈ 1,96 × desvío robusto del cambio en pares estables ≈ 0,97 z). Se estimaron RCIs por dominio
y por test (MAD robusta; z winsorizados a [−6, 4] para eliminar artefactos de piso de los tests cronometrados).

### Análisis estadístico
El cambio se resumió en un índice z global (media de cinco dominios core). Como el cambio cognitivo seriado está
confundido por la **regresión a la media**, se modeló el puntaje final sobre el basal (ANCOVA) y se usó el **residuo**
como cambio ajustado. Los modelos pronósticos usaron **regresión logística penalizada** (L2 para los modelos
desplegados; L1 para selección), con imputación por mediana e indicadores de faltante y estandarización **dentro** de
la validación cruzada; los faltantes fueron bajos (edad 0%, memoria diferida 6%, severidad basal 0%). Se estimó el
**valor incremental** de la memoria sobre la edad comparando el AUC de modelos anidados. El rendimiento se estimó por
**validación cruzada anidada repetida** (5×20) con ajuste interno de hiperparámetros y por **corrección de optimismo
por bootstrap** (Steyerberg); las cohortes pequeñas usaron además LOOCV. Las probabilidades se **recalibraron (Platt)**
y se reportan con Brier y pendiente/intercepto. La robustez de las variables se evaluó por **stability selection** (L1
sobre bootstraps). Las bandas de incertidumbre por paciente provienen de 200 modelos bootstrap exportados a la
calculadora. El reporte sigue **TRIPOD**.[28] Una implementación en JavaScript reproduce exactamente los coeficientes
(test de paridad).

## Resultados

### Cohorte y variable perfil (Tabla 1)
De 334 pacientes con más de una evaluación archivada, 84 tenían todas las evaluaciones el mismo día o sin fecha válida y
250 tuvieron una reevaluación genuina en ≥2 fechas distintas (mediana de seguimiento 1,83 años; IQR 1,25–2,97;
**Figura 1**). Quienes volvieron para reevaluación fueron mayores que los de una sola visita (67,0 vs 63,8 años) con
severidad basal comparable, lo que sugiere una vigilancia guiada por la edad y la sospecha clínica más que por la
gravedad.

El perfil codificado fue **altamente reproducible** entre dos codificaciones independientes (severidad κ=1,00, acuerdo
exacto 100%; almacenamiento κ=0,96; subtipo κ=0,88; estabilidad longitudinal κ=0,85) y mostró fuerte **validez de
constructo**: el número medio de dominios deficitarios de la batería creció de forma monótona a través de las bandas de
severidad (z ≤ −2: normal 0,5 → leve 2,0 → moderado 3,7 → grave 4,2) y la proporción con ≥1 dominio deficitario subió
del 38% (normal) al 100% (≥ leve-a-moderado). Cabe destacar que solo 2 de 121 pacientes con DCL codificado carecían de todo
deterioro objetivo en la batería: a diferencia de los criterios convencionales, que producen alrededor de un tercio de
falsos positivos “dentro de límites normales”,[14] la codificación clínica-narrativa casi no sobre-diagnosticó, lo que
respalda su validez.

### La evolución de los perfiles solo se interpreta tras ajustar por el basal (Figuras 2 y 4)
La **matriz de transición** de severidad (Figura 2) muestra la evolución de cada banda basal: 34% de los pacientes
empeoró ≥1 banda, 53% permaneció estable y 13% mejoró; la **reversión** de DCL a normal ocurrió en 6% (5/85), en línea
con la menor reversión que reportan los criterios neuropsicológicos rigurosos.[16] La **tasa de progresión** a demencia
en la cohorte de deterioro leve-moderado fue de **11,9%/año** (32 eventos / 269 persona-años), dentro del rango de las
clínicas de memoria (~10–15%/año).[5] El cambio seriado estuvo parcialmente confundido por la **regresión a la media**:
al regresar el z global final sobre el basal la pendiente fue de 0,82 (r=0,73), de modo que el cambio crudo Δz dependió
del nivel basal (pendiente Δz ≈ −0,18; Figura 4). Como los fenotipos difieren en severidad basal, el cambio crudo debe
ajustarse antes de comparar trayectorias; tras el ajuste, el perfil amnésico fue el único que declinó, mientras que los
perfiles disejecutivo, multidominio y preservado no lo hicieron.

### El compromiso de memoria es el eje del riesgo; el subtipo fino está infrapotenciado (Figura 3)
Operacionalizados según criterios de Petersen/Winblad a partir del patrón objetivo de dominios, los subtipos de la
cohorte en riesgo estuvieron **dominados por el amnésico multidominio** (78%; 94/121), que concentró la progresión a
demencia (**32%**; IC95% 23–42; 30/94). El subtipo no amnésico multidominio progresó menos (9%; 1/11) y los subtipos de
dominio único —amnésico (0/9) y no amnésico (0/5)— no registraron eventos. En consecuencia, el gradiente fino entre
subtipos es **frágil**: alcanza significación marginal bajo el esquema objetivo (χ² p=0,041, con celdas de dominio único
casi vacías) y bajo la etiqueta dominante previa (p=0,008), pero no bajo el esquema de dominios señalados por el clínico
(p=0,411). La lectura robusta no es una jerarquía categórica, sino que **el compromiso de memoria (el eje amnésico), que
domina esta cohorte, porta esencialmente todo el riesgo** —conclusión que converge con el modelo pronóstico continuo
(véase abajo). La concordancia entre memoria afectada por z objetivo y por juicio clínico fue del 86%.

A nivel del mecanismo de memoria, el subtipo amnésico se **define** por el **compromiso del almacenamiento** (falla de
consolidación de tipo temporal-medial, à la Sarazin/Dubois[7]), presente en el **93%** de los casos amnésicos. Es la
firma que caracteriza al subtipo de mayor riesgo, no un predictor independiente: dentro del amnésico, el almacenamiento
comprometido no separó la progresión (32% vs 26%; diferencia no significativa). Los perfiles con **modulador anímico**
al basal mostraron menos declive en la métrica ajustada por el basal (≈17% vs 34%), consistente con un curso
parcialmente reversible, aunque el subgrupo es pequeño (n≈29) y el contraste no es concluyente. El juicio narrativo del
clínico sobre la estabilidad concordó estrechamente con el cambio
cuantitativo ajustado por el basal (declive declarado: Δz ajustado −0,52; estable: +0,84), triangulando dos mediciones
independientes.

### Ninguna transición directa observada de cognición normal a demencia
Entre los 14 pacientes cognitivamente normales al basal, ninguno progresó a demencia (0/14); la progresión partió
invariablemente de un estadio intermedio. El patrón es consistente con un modelo por estadios —aunque el escaso número
de normales es **insuficiente para probar** que la transición directa nunca ocurra— y justifica tomar los estados de
deterioro leve-moderado, no los normales, como denominador del pronóstico a corto plazo.

### Análisis de sensibilidad de la definición del desenlace
La definición de progresión (severidad final ≥ moderada) rindió 32 eventos en la cohorte de deterioro leve-moderado
(n=122). Umbrales más estrictos redujeron drásticamente los eventos —9 (≥moderado-grave) y 4 (grave)— tornándolos
inestimables. El desenlace se interpreta, por tanto, como **progresión a deterioro moderado o mayor** (síndrome de rango
demencial), no como demencia confirmada por criterio funcional independiente.

### Normas locales de cambio fiable
Aportamos RCIs locales para el testeo seriado: ≈0,97 z a nivel persona y umbrales por test de ±1,4 (recuerdo diferido de
lista) a ±2,5 (reconocimiento), con 7–14% de pacientes mostrando declive fiable por dominio en el intervalo. Son, hasta
donde sabemos, de las primeras normas locales de cambio para esta población.

### Predicción de la progresión a demencia (Tabla 2, Figura 5)
En los tres desenlaces, **la parsimonia superó a la complejidad**. La stability selection de alta dimensión sobre ~40
variables rindió un AUC honesto menor que el de sets pequeños pre-especificados, y un modelo de árbol de excelente AUC
aparente (0,97) colapsó a ~0,66 bajo corrección de optimismo, evidenciando sobreajuste a este tamaño muestral. Los
mejores modelos honestos fueron:

- **DCL → demencia:** memoria de relatos diferida + edad — AUC 0,84 (concordante entre CV anidada, optimismo y LOOCV; IC95% 0,54–1,0; 16 eventos).
- **Deterioro leve-moderado → demencia:** + severidad basal — AUC 0,80 (IC95% 0,64–0,92; 122 pacientes, 32 eventos), con beneficio clínico neto sobre “tratar a todos” en todo el rango de umbrales.
- **Declive fiable:** edad, Lista de Rey trial 1, intrusiones, CI premórbido, Hayling — AUC 0,69.

En todos, la **memoria diferida y la edad** dominaron (OR por DS: memoria ≈0,41; edad ≈1,7–2,0), recapitulando la firma
amnésica-más-edad de la conversión tipo Alzheimer. El **valor incremental** de la memoria sobre la edad sola fue
sustancial —ΔAUC **+0,13** en DCL→demencia (0,72→0,85) y **+0,08** en deterioro leve-moderado (0,69→0,78; Figura 5C)—,
confirmando que el puntaje de memoria aporta información más allá de la demografía. Los modelos quedaron bien calibrados
tras Platt (Figura 5B). Que la señal categórica de subtipo y el modelo continuo converjan sobre la misma variable —la
memoria diferida— refuerza que ese es el eje pronóstico. Los modelos finales se despliegan como calculadora abierta que
computa el riesgo con banda de incertidumbre bootstrap y **nunca transmite datos del paciente** (Figura 6).

## Discusión

En una clínica de memoria argentina de mundo real, los perfiles neuropsicológicos evolucionaron por **trayectorias
mecanísticamente coherentes**, y la progresión a demencia se predijo desde la evaluación basal con un modelo
notablemente **parsimonioso y normado localmente**. Tres hallazgos merecen énfasis.

**Primero, la interpretación del cambio seriado exige normas de cambio fiable y ajuste por el basal.** La regresión a la
media fue moderada (pendiente final–basal 0,82; r=0,73) pero suficiente para que el cambio crudo dependa del nivel basal
(Figura 4); como los fenotipos difieren en severidad basal, comparar trayectorias crudas puede distorsionar el orden de
los pronósticos. Tras el ajuste, el perfil amnésico siguió siendo el que más declinó, coherente con el resto de los
hallazgos. El mismo tipo de confusión —el cambio temprano condicionando la exposición o la medición— subyace a
asociaciones “protectoras” que se disuelven bajo escrutinio causal, como se demostró para el alcohol y la demencia
(causalidad inversa).[26] Un Índice de Cambio Fiable local y las métricas ajustadas por el basal, junto con los RCIs
corregidos por efecto de práctica,[27] deberían acompañar toda interpretación neuropsicológica seriada.

**Segundo, el eje del riesgo es el compromiso de memoria, más que una jerarquía categórica de subtipos.** La cohorte en
riesgo estuvo dominada por perfiles amnésicos multidominio, que concentraron la progresión, mientras que los subtipos de
dominio único y no amnésicos fueron infrecuentes y sin eventos. Antes que sobreinterpretar un gradiente entre subtipos
—que resultó infrapotenciado y sensible a la operacionalización—, la lectura honesta es que la memoria es el eje del
pronóstico, y así lo confirma la convergencia con el modelo continuo. Esta primacía de la memoria es mecanísticamente
esperable: el subtipo amnésico se define por el **compromiso del almacenamiento** (falla de consolidación de tipo
temporal-medial), frente a la falla de **recuperación** (frontal) de los perfiles disejecutivos; es el síndrome amnésico
que identifica la enfermedad de Alzheimer prodrómica[7] y explica por qué el recuerdo diferido es el predictor por
excelencia de la conversión.[7–13] El curso benigno de los perfiles con carga anímica concuerda con el deterioro
cognitivo reversible del trastorno afectivo de la vejez y con la noción del compromiso conductual como pródromo
diferenciable,[20], y advierte contra equiparar el deterioro actual con una trayectoria inexorable. Que ningún paciente
pasara de cognición normal directamente a demencia en ~2 años refuerza un modelo por estadios y tiene una implicancia
metodológica concreta: los estados de deterioro leve-moderado, no los individuos normales, son la población apropiada
para la predicción de demencia a corto plazo.

**Tercero, para predecir, menos fue más.** Un modelo de dos variables —recuerdo diferido de relatos y edad— predijo la
progresión DCL→demencia con un AUC optimismo-corregido de 0,84, comparable al de modelos publicados basados en
neuropsicología que emplean baterías mayores[7–13] —sin que ello constituya una comparación directa, dado que provienen
de cohortes distintas—, y el modelo de deterioro leve-moderado agregó solo la severidad basal para alcanzar 0,80 con
beneficio clínico neto demostrable. Los intentos de mejorarlo con selección de alta dimensión no ayudaron y a veces
perjudicaron, y la aparente excelencia de un árbol resultó ser memorización. A los recuentos de eventos típicos de una
clínica única, el techo de la discriminación lo fija el tamaño muestral y la ausencia de biomarcadores más que la
sofisticación algorítmica —consistente con la prioridad regional de extraer el máximo valor pronóstico de **medidas
cognitivas de rutina** mientras se expande el acceso a biomarcadores.[23–25] La parsimonia emergente es, además, lo que
vuelve usable la herramienta: cada input se transcribe de un informe estándar y la inferencia corre íntegramente en el
navegador, preservando la privacidad. Extraer el máximo de las medidas de rutina es también coherente con la agenda de
prevención, que sitúa la detección y el manejo tempranos de la trayectoria cognitiva en el centro de la reducción del
riesgo de demencia.[21,22]

El estudio tiene **fortalezas**: datos genuinos de mundo real, depuración e identificación cuidadosas, una variable
perfil reproducible y altamente fiable validada contra puntajes objetivos, validación interna metodológicamente
rigurosa (CV anidada, corrección de optimismo, calibración, análisis de curva de decisión) reportada según TRIPOD,[28] y
liberación abierta del código y de una calculadora desplegada.

Las **limitaciones** acotan las conclusiones a un nivel **exploratorio**. (i) La muestra es modesta y los eventos
escasos; los **eventos por variable** fueron 6,8–10,7 (por debajo del ≥10 recomendado en dos modelos), y el modelo
DCL→demencia (16 eventos) tiene un IC amplio (0,54–1,0) con límite inferior poco informativo: es un **prototipo**
validado solo internamente. (ii) El análisis de **subtipos** se basa en grupos pequeños con celdas casi vacías; solo la
primacía del compromiso de memoria es robusta, no un ordenamiento fino entre subtipos. (iii) La cohorte generaliza a
quienes **regresan a reevaluarse** —subgrupo no aleatorio, de mayor edad, con posible gradiente de acceso—; el **riesgo
competitivo de muerte** no se modeló y la censura puede ser informativa. (iv) El desenlace binario a seguimiento variable
**ignora el tiempo**; un modelo de tiempo-al-evento (supervivencia en tiempo discreto) es el paso siguiente. (v) La
severidad basal (predictor) y el desenlace (severidad final) se codificaron de la misma sección del informe por el mismo
proceso automatizado en distintos momentos: comparten **varianza de método** y provienen de un **único centro y esquema
de codificación**, aunque la validez de constructo contra el z objetivo los respalda. (vi) Excluimos el diagnóstico
etiológico: los modelos predicen **trayectoria cognitiva, no enfermedad**, y el desenlace —“deterioro moderado o mayor”—
carece de criterio funcional independiente que confirme demencia según el consenso.[3] La deriva de la documentación de
mundo real y la ausencia de biomarcadores acotan aún más el rendimiento. La **validación externa** —idealmente en
consorcios regionales y frente a los biomarcadores en sangre que hoy se caracterizan en Latinoamérica[25]— es el paso
esencial, junto con la recalibración periódica a medida que crezca la cohorte.

## Conclusiones
En la práctica de rutina de una clínica de memoria argentina, los perfiles cognitivos evolucionan por trayectorias
mecanísticamente coherentes que se enmascaran sin ajuste por el basal, y en las que el compromiso de memoria es el eje
del riesgo. La progresión a demencia es predecible a partir de una combinación parsimoniosa y normada localmente de
memoria diferida y edad. Desplegado como calculadora abierta que preserva la privacidad, esto ofrece una ayuda
pronóstica transparente y de uso inmediato para entornos subrepresentados —a la espera de validación externa.

---

## Tablas

**Tabla 1. Características de la cohorte y fiabilidad/validez del perfil.**

| Variable | Reevaluación (n=250) | Una visita (n=2648) |
|---|---|---|
| Edad, años (media ± DE) | 67,0 ± 14,3 | 63,8 ± 19,1 |
| Educación, años (media ± DE) | 13,3 ± 3,4 | 12,9 ± 3,7 |
| Sexo femenino, % | 56 | 56 |
| Seguimiento, años, mediana (IQR) | 1,83 (1,25–2,97) | — |
| Nº de evaluaciones (2 / 3 / 4) | 213 / 36 / 1 | — |

*Una visita:* pacientes con una sola fecha de evaluación (comparador).
*Fiabilidad inter-codificador (κ):* severidad 1,00; almacenamiento 0,96; subtipo 0,88; estabilidad 0,85.
*Validez de constructo* (dominios deficitarios objetivos, z ≤ −2, por banda): normal 0,5 → leve 2,0 → moderado 3,7 → grave 4,2.
*Falsos positivos:* solo 2/121 DCL codificados sin deterioro objetivo (z ≤ −1,5) en la batería.

**Tabla 2. Rendimiento de los modelos pronósticos (TRIPOD).**

| Desenlace | Cohorte (n / eventos) | Predictores | AUC [IC95%] | EPV |
|---|---|---|---|---|
| DCL → demencia | 85 / 16 | Memoria de relatos diferida + edad | **0,84** [0,54–1,0] | 8,0 |
| Deterioro leve-moderado → demencia | 122 / 32 | + severidad basal | **0,80** [0,64–0,92] | 10,7 |
| Declive fiable | 182 / 34 | edad, Rey trial 1, intrusiones, CI premórbido, Hayling | 0,69 [0,48–0,88] | 6,8 |
| Conversión de banda | 189 / 58 | (débil; aparente 0,97 → honesto) | 0,66 [0,53–0,81] | — |

*AUC por CV anidada, optimismo-corregido; calibración Platt (pendiente 1,3–1,4). EPV = eventos por variable.
IC del modelo DCL→demencia amplio por los 16 eventos (prototipo).*

## Figuras

**Figura 1. Flujo de la cohorte.**

![Figura 1](Fig1_flujo.png)

*Diagrama de participantes: de 334 pacientes con ≥2 evaluaciones archivadas se excluyeron 84 (duplicados del mismo día
o sin fecha válida), quedando 250 con reevaluación real; 182 con perfil basal y final codificado, y las cohortes de DCL
(n=85) y deterioro leve-moderado (n=122).*

**Figura 2. Evolución de los perfiles: matriz de transición de severidad (basal → reevaluación).**

![Figura 2](Fig2_transiciones.png)

*Cada celda muestra el n de pacientes; el color codifica el % de la fila. La línea roja separa el rango de demencia
(≥ moderado). Ningún paciente normal al basal (fila superior) transicionó directamente a demencia.*

**Figura 3. Progresión a demencia por subtipo operativo de DCL (Petersen/Winblad).**

![Figura 3](Fig3_subtipos.png)

*Subtipos derivados del patrón objetivo de dominios (memoria × número de dominios; umbral z ≤ −1,5) en la cohorte en
riesgo (n=122). Tasa de progresión con IC95% de Wilson y n/total. La cohorte está dominada por el subtipo amnésico
multidominio, que concentra los eventos; los subtipos de dominio único no registran eventos (celdas pequeñas, IC muy
amplios). El eje robusto del riesgo es el compromiso de memoria, no el ordenamiento fino entre subtipos.*

**Figura 4. Regresión a la media.**

![Figura 4](Fig4_regresion.png)

*Dispersión del cambio Δz (final − basal) frente al z cognitivo basal; la pendiente negativa muestra que el cambio
crudo depende del basal, lo que obliga a ajustar por el basal antes de interpretar la evolución.*

**Figura 5. Rendimiento de los modelos.**

![Figura 5](Fig5_rendimiento.png)

*A: curvas ROC de los modelos de demencia (out-of-fold). B: curva de calibración (modelo deterioro leve-moderado).
C: valor incremental — AUC de la edad sola vs memoria sola vs modelo completo, mostrando que la memoria aporta sobre la
demografía.*

**Figura 6. Calculadora desplegada (client-side).**

![Figura 6](Figure3.png)

*Al seleccionar la severidad basal aparecen el modelo aplicable y sus campos; el riesgo se muestra con banda de
incertidumbre bootstrap y la prevalencia de la cohorte como referencia. Corre 100% en el navegador (sin transmitir
datos). Disponible en https://fermarquez88.github.io/kaizenai-demencia/*

---

## Referencias
*Recuperadas y verificadas vía PubMed. Se incluye DOI.*

1. Petersen RC, Smith GE, Waring SC, et al. Mild cognitive impairment: clinical characterization and outcome. *Arch Neurol.* 1999. https://doi.org/10.1001/archneur.56.3.303
2. Petersen RC, Doody R, Kurz A, et al. Current concepts in mild cognitive impairment. *Arch Neurol.* 2001. https://doi.org/10.1001/archneur.58.12.1985
3. Winblad B, Palmer K, Kivipelto M, et al. Mild cognitive impairment — beyond controversies, towards a consensus: report of the International Working Group on Mild Cognitive Impairment. *J Intern Med.* 2004. https://doi.org/10.1111/j.1365-2796.2004.01380.x
4. Ganguli M, Snitz BE, Saxton JA, et al. Outcomes of mild cognitive impairment by definition: a population study. *Arch Neurol.* 2011. https://doi.org/10.1001/archneurol.2011.101
5. Espinosa A, Alegret M, Valero S, et al. A longitudinal follow-up of 550 mild cognitive impairment patients: evidence for large conversion to dementia rates and detection of major risk factors. *J Alzheimers Dis.* 2013. https://doi.org/10.3233/JAD-122002
6. Allegri RF, Glaser FB, Taragano FE, Buschke H. Mild cognitive impairment: believe it or not? *Int Rev Psychiatry.* 2008. https://doi.org/10.1080/09540260802095099
7. Sarazin M, Berr C, De Rotrou J, et al. Amnestic syndrome of the medial temporal type identifies prodromal AD: a longitudinal study. *Neurology.* 2007. https://doi.org/10.1212/01.wnl.0000279336.36610.f7
8. Gainotti G, Quaranta D, Vita MG, Marra C. Neuropsychological predictors of conversion from mild cognitive impairment to Alzheimer's disease. *J Alzheimers Dis.* 2014. https://doi.org/10.3233/JAD-130881
9. Modrego PJ. Predictors of conversion to dementia of probable Alzheimer type in patients with mild cognitive impairment. *Curr Alzheimer Res.* 2006. https://doi.org/10.2174/156720506776383103
10. García-Herranz S, Díaz-Mardomingo MC, Peraita H. Neuropsychological predictors of conversion to probable Alzheimer disease in elderly with mild cognitive impairment. *J Neuropsychol.* 2016. https://doi.org/10.1111/jnp.12067
11. López ME, Turrero A, Cuesta P, et al. A multivariate model of time to conversion from mild cognitive impairment to Alzheimer's disease. *GeroScience.* 2020. https://doi.org/10.1007/s11357-020-00260-7
12. Park HK, Choi SH, Park SA, et al. Memory performance on the story recall test and prediction of cognitive dysfunction progression in mild cognitive impairment and Alzheimer's dementia. *Geriatr Gerontol Int.* 2017. https://doi.org/10.1111/ggi.12940
13. Bao J, Wang Y, Qu D, et al. Impairment of delayed recall as a predictor of amnestic mild cognitive impairment development in normal older adults: a 7-year longitudinal cohort study. *BMC Psychiatry.* 2023. https://doi.org/10.1186/s12888-023-05309-3
14. Bondi MW, Edmonds EC, Jak AJ, et al. Neuropsychological criteria for mild cognitive impairment improves diagnostic precision, biomarker associations, and progression rates. *J Alzheimers Dis.* 2014. https://doi.org/10.3233/JAD-140276
15. Jak AJ, Preis SR, Beiser AS, et al. Neuropsychological criteria for mild cognitive impairment and dementia risk in the Framingham Heart Study. *J Int Neuropsychol Soc.* 2016. https://doi.org/10.1017/S1355617716000199
16. Wong CG, Thomas KR, Edmonds EC, et al. Neuropsychological criteria for mild cognitive impairment in the Framingham Heart Study's old-old. *Dement Geriatr Cogn Disord.* 2018. https://doi.org/10.1159/000493541
17. Lee YC, Kang JM, Lee H, et al. Amnestic multiple cognitive domains impairment and periventricular white matter hyperintensities are independently predictive factors of progression to dementia in mild cognitive impairment. *Int J Geriatr Psychiatry.* https://doi.org/10.1002/gps.4035
18. Persson K, Eldholm RS, Barca ML, et al. Visual evaluation of medial temporal lobe atrophy as a clinical marker of conversion from mild cognitive impairment to dementia. *Dement Geriatr Cogn Disord.* 2017. https://doi.org/10.1159/000477342
19. Mortimer JA, Borenstein AR, Gosche KM, Snowdon DA. Very early detection of Alzheimer neuropathology and the role of brain reserve in modifying its clinical expression. *J Geriatr Psychiatry Neurol.* 2005. https://doi.org/10.1177/0891988705281869
20. Taragano FE, Allegri RF, Lyketsos C. Mild behavioral impairment: a prodromal stage of dementia. *Dement Neuropsychol.* 2008. https://doi.org/10.1590/S1980-57642009DN20400004
21. Livingston G, Huntley J, Sommerlad A, et al. Dementia prevention, intervention, and care: 2020 report of the Lancet Commission. *Lancet.* 2020. https://doi.org/10.1016/S0140-6736(20)30367-6
22. Livingston G, Huntley J, Liu KY, et al. Dementia prevention, intervention, and care: 2024 report of the Lancet standing Commission. *Lancet.* 2024. https://doi.org/10.1016/S0140-6736(24)01296-0
23. Parra MA, Baez S, Allegri R, et al. Dementia in Latin America: assessing the present and envisioning the future. *Neurology.* 2018. https://doi.org/10.1212/WNL.0000000000004897
24. Maito MA, Santamaría-García H, Moguilner S, et al. Classification of Alzheimer's disease and frontotemporal dementia using routine clinical and cognitive measures across multicentric underrepresented samples. *Lancet Reg Health Am.* 2022. https://doi.org/10.1016/j.lana.2022.100387
25. Caviedes A, et al. Blood-based AT(N) biomarkers for Alzheimer's disease and frontotemporal lobar degeneration in Latin America. *Nat Aging.* 2026. https://doi.org/10.1038/s43587-025-01061-3
26. Topiwala A, Levey DF, Zhou H, et al. Alcohol use and risk of dementia in diverse populations: cohort, case-control and Mendelian randomisation approaches. *BMJ Evid Based Med.* 2026. https://doi.org/10.1136/bmjebm-2025-113913
27. Tröster AI, Woods SP, Morgan EE. Assessing cognitive change in Parkinson's disease: development of practice effect-corrected reliable change indices. *Arch Clin Neuropsychol.* 2007. https://doi.org/10.1016/j.acn.2007.05.004
28. Collins GS, Reitsma JB, Altman DG, Moons KGM. Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD): the TRIPOD statement. *Ann Intern Med.* 2015. https://doi.org/10.7326/M14-0697
