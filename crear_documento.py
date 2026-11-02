from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
root=Path(__file__).parent
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
pdfmetrics.registerFont(TTFont('DejaVu',font))
pdfmetrics.registerFont(TTFont('DejaVuBold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TituloP',fontName='DejaVuBold',fontSize=18,leading=24,spaceAfter=16,textColor=colors.HexColor('#153d57')))
styles.add(ParagraphStyle(name='SubP',fontName='DejaVuBold',fontSize=12,leading=17,spaceBefore=13,spaceAfter=7,textColor=colors.HexColor('#205977')))
styles.add(ParagraphStyle(name='TextoP',fontName='DejaVu',fontSize=9,leading=15,spaceAfter=8))
styles.add(ParagraphStyle(name='CodigoP',fontName='DejaVu',fontSize=8,leading=13,leftIndent=12,spaceAfter=4))
doc=SimpleDocTemplate(str(root/'Informe_Proyecto_2.pdf'),pagesize=letter,rightMargin=53,leftMargin=53,topMargin=50,bottomMargin=45)
story=[]
def h(t): story.append(Paragraph(t,styles['SubP']))
def p(t): story.append(Paragraph(t,styles['TextoP']))
def code(t): story.append(Paragraph(t.replace(' ','&#160;'),styles['CodigoP']))
story.append(Paragraph('Proyecto #2 - Reconocimiento de cadenas',styles['TituloP']))
p('Teoría de la Computación · CC2019 · Semestre 2, 2026')
p('<b>Integrantes:</b> ______________________________ &nbsp;&nbsp; <b>Repositorio privado:</b> ______________________________')
p('Este informe acompaña dos implementaciones en Python: un autómata de pila no determinista (NPDA) y el algoritmo CYK. Ambos reconocen cadenas del lenguaje definido por la gramática G del enunciado y muestran evidencia de sus decisiones.')
h('1. Gramática proporcionada')
for line in ['S → NP VP','VP → VP PP | V NP | cooks | drinks | eats | cuts','PP → P NP','NP → Det N | he | she','V → cooks | drinks | eats | cuts','P → in | with','N → cat | dog | beer | cake | juice | meat | soup','N → fork | knife | oven | spoon','Det → a | the']:
    code(line)
p('La gramática ya está en Forma Normal de Chomsky: todas las reglas son A → BC o A → a. Se utiliza directamente para CYK, sin transformaciones.')
h('2. Definición formal del PDA')
p('Se emplea la construcción top-down del material «Autómatas de pila 2026», páginas 6-7. El PDA es M = (Q, Σ, Γ, q0, Z0, F, δ), con Q = {q0, q1, q2}, F = {q2}, Γ = V ∪ Σ ∪ {Z0}, Σ igual al vocabulario terminal de G, y V = {S, VP, PP, NP, V, P, N, Det}.')
p('La cima de la pila es el símbolo más a la izquierda. La función δ incluye:')
code('δ(q0, ε, Z0) = {(q1, S Z0)}')
code('δ(q1, ε, Z0) = {(q2, Z0)}')
p('Por cada producción A → α de G, se agrega (q1, α) a δ(q1, ε, A). Para cada terminal a de Σ se agrega δ(q1, a, a) = {(q1, ε)}. Estas reglas definen todas las transiciones del autómata, incluyendo cada alternativa de VP, NP, N y las demás variables.')
p('El estado q2 acepta únicamente si toda la entrada ha sido consumida. Las expansiones son no deterministas: cuando una variable tiene varias producciones, se consideran todas las posibilidades.')
h('3. Implementación del PDA')
p('El simulador explora configuraciones (estado, posición de entrada, pila) mediante búsqueda en anchura (BFS). Conserva el predecesor y la transición aplicada para reconstruir una secuencia de descripciones instantáneas de aceptación. Para evitar ciclos por VP → VP PP, memoriza configuraciones visitadas y descarta pilas cuyo número de símbolos pendientes exceda el número de palabras restantes. Esta poda es válida porque, en G, cada variable genera al menos una palabra y no hay producciones vacías.')
h('4. Implementación CYK')
p('Para cada palabra w[i], la diagonal inicial de la tabla almacena las variables A con producción A → w[i]. Para cada intervalo de longitud l, se consideran todos los cortes k y pares B,C; si B aparece en el intervalo izquierdo, C en el derecho y A → BC, se incorpora A a la celda correspondiente. Se acepta si S pertenece a la celda que abarca la oración completa. Se guarda un testigo de cada producción para reconstruir un árbol de derivación.')
h('5. Complejidad asintótica')
p('<b>CYK:</b> para una gramática fija, el algoritmo recorre las longitudes l = 2,...,n, las posiciones de inicio (n-l+1) y los cortes (l-1). El número de combinaciones de intervalos y cortes es Σ(l-1)(n-l+1) = (n³-n)/6. Las comprobaciones de producciones cuestan una constante para esta gramática fija; por tanto el peor caso es O(n³) y el espacio de tabla es O(n²), sin contar la representación de árboles.')
p('<b>PDA:</b> la construcción no determinista no garantiza un número polinómico de configuraciones para una gramática arbitraria. Esta implementación enumera configuraciones con BFS; para G fija y entrada de longitud n, la pila útil se limita a n símbolos. El número de pilas posibles está acotado por una suma geométrica de |Γ|^k (k ≤ n), multiplicada por n+1 posiciones, de modo que el peor caso de exploración está acotado por O(n·|Γ|^n) configuraciones, y el costo de copiar/inspeccionar pilas añade hasta O(n) por transición: O(n²·|Γ|^n) en una implementación directa. Esta es una cota superior conservadora, no una afirmación de que toda entrada tarde exponencialmente. La longitud del camino aceptante puede ser mucho menor.')
p('Los contadores mostrados por el programa registran configuraciones exploradas (PDA) y pares de variables considerados (CYK). No sustituyen un análisis formal por número de operaciones ni miden segundos.')
h('6. Comparación de desempeño')
p('CYK tiene una cota polinómica predecible O(n³), trabaja sistemáticamente sobre subcadenas y necesita O(n²) celdas. Es robusto ante la recursión izquierda y la ambigüedad, aunque puede construir una tabla completa incluso cuando una frase es fácil de reconocer. El PDA refleja directamente las reglas gramaticales y ofrece una trayectoria de aceptación intuitiva; puede terminar pronto si encuentra una derivación corta, pero la exploración de alternativas y configuraciones puede crecer rápidamente. Para frases largas y análisis de peor caso, CYK ofrece mejores garantías; para demostrar la mecánica de un autómata de pila, el PDA es especialmente ilustrativo.')
h('7. Pruebas y evidencia')
rows=[['Frase','Resultado esperado'],['she eats','Aceptada'],['he cuts a cake with a knife','Aceptada'],['the cat eats the meat in the oven','Aceptada'],['he eats with','Rechazada'],['she eats pizza','Rechazada'],['the cat eats the','Rechazada']]
t=Table([[Paragraph(x,styles['TextoP']) for x in row] for row in rows],colWidths=[350,135],repeatRows=1,hAlign='LEFT')
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e4edf4')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LINEBELOW',(0,0),(-1,0),0.8,colors.HexColor('#4a7187')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f8fa')]),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
story.append(t)
p('Ejecución: python main.py "she eats the cake" --pasos. Pruebas automatizadas: python -m unittest -v. El comando --pasos muestra la secuencia de configuraciones del PDA, la tabla CYK y un árbol de derivación si la oración se acepta.')
h('8. Entrega y demostración')
p('Publicar los archivos .py y README.md en un repositorio privado, compartir acceso con docente y auxiliar, y adjuntar su enlace al informe. Grabar un video no listado de menos de 10 minutos mostrando la gramática, ejemplos aceptados y rechazados, trazas, pruebas y comparación de complejidad. Completar nombres y enlaces antes de entregar.')
h('Fuentes')
p('Universidad del Valle de Guatemala. (2026). Proyecto #2, Teoría de la Computación, CC2019. Universidad del Valle de Guatemala. (2026). Autómatas de pila, especialmente páginas 6-7. Análisis de complejidad de CYK y de la exploración BFS: deducción a partir de los algoritmos implementados.')
def footer(c,d):
    c.setFont('DejaVu',8);c.setFillColor(colors.grey);c.drawRightString(560,25,f'Página {d.page}')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(root/'Informe_Proyecto_2.pdf')
