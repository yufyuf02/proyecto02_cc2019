"""Gramatica del Proyecto 2, CC2019."""
from collections import defaultdict

PRODUCCIONES = {
    'S': [('NP', 'VP')],
    'VP': [('VP', 'PP'), ('V', 'NP'), ('cooks',), ('drinks',), ('eats',), ('cuts',)],
    'PP': [('P', 'NP')],
    'NP': [('Det', 'N'), ('he',), ('she',)],
    'V': [('cooks',), ('drinks',), ('eats',), ('cuts',)],
    'P': [('in',), ('with',)],
    'N': [(w,) for w in 'cat dog beer cake juice meat soup fork knife oven spoon'.split()],
    'Det': [('a',), ('the',)],
}
NO_TERMINALES = frozenset(PRODUCCIONES)
TERMINALES = frozenset(rhs[0] for rules in PRODUCCIONES.values() for rhs in rules if len(rhs) == 1 and rhs[0] not in NO_TERMINALES)

def tokens(frase):
    return tuple(frase.lower().strip().split())

def validar_cnf():
    for cabeza, reglas in PRODUCCIONES.items():
        for rhs in reglas:
            assert (len(rhs) == 1 and rhs[0] in TERMINALES) or (len(rhs) == 2 and all(s in NO_TERMINALES for s in rhs)), (cabeza, rhs)
