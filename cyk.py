"""Reconocimiento CYK con tabla y derivacion reconstruida."""
from collections import defaultdict
from gramatica import PRODUCCIONES, tokens, validar_cnf


def reconocer_cyk(frase):
    validar_cnf()
    palabras = tokens(frase)
    n = len(palabras)
    if not n:
        return {'acepta': False, 'tabla': [], 'derivacion': [], 'operaciones': 0}
    terminales = defaultdict(set)
    binarias = defaultdict(set)
    for cabeza, reglas in PRODUCCIONES.items():
        for rhs in reglas:
            (terminales if len(rhs) == 1 else binarias)[rhs].add(cabeza)
    tabla = [[{} for _ in range(n + 1)] for _ in range(n)]
    operaciones = 0
    for i, palabra in enumerate(palabras):
        for cabeza in terminales.get((palabra,), ()):
            tabla[i][1][cabeza] = ('terminal', palabra)
        operaciones += 1
    for longitud in range(2, n + 1):
        for inicio in range(n - longitud + 1):
            for corte in range(1, longitud):
                izq, der = tabla[inicio][corte], tabla[inicio + corte][longitud - corte]
                for b in izq:
                    for c in der:
                        operaciones += 1
                        for a in binarias.get((b, c), ()):
                            tabla[inicio][longitud].setdefault(a, ('binaria', corte, b, c))
    acepta = 'S' in tabla[0][n]
    derivacion = []
    def construir(i, longitud, simbolo, profundidad=0):
        regla = tabla[i][longitud][simbolo]
        if regla[0] == 'terminal':
            derivacion.append('  ' * profundidad + f'{simbolo} -> {regla[1]}')
        else:
            _, corte, b, c = regla
            derivacion.append('  ' * profundidad + f'{simbolo} -> {b} {c}')
            construir(i, corte, b, profundidad + 1)
            construir(i + corte, longitud - corte, c, profundidad + 1)
    if acepta:
        construir(0, n, 'S')
    vista = [[sorted(tabla[i][longitud]) for i in range(n - longitud + 1)] for longitud in range(1, n + 1)]
    return {'acepta': acepta, 'tabla': vista, 'derivacion': derivacion, 'operaciones': operaciones}
