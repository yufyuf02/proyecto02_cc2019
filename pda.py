"""Simulador NPDA top-down: BFS de configuraciones (estado, posicion, pila).
La pila se almacena con la cima en la posicion 0.
"""
from collections import deque
from gramatica import PRODUCCIONES, NO_TERMINALES, TERMINALES, tokens


def reconocer_pda(frase):
    palabras = tokens(frase)
    n = len(palabras)
    # Todas las variables generan al menos una palabra en esta gramatica.
    # Por tanto, una pila con mas simbolos utiles que palabras restantes no sirve.
    inicio = ('q0', 0, ('Z0',))
    cola = deque([inicio])
    anterior = {inicio: (None, 'inicio')}
    operaciones = 0
    final = None
    while cola:
        actual = cola.popleft()
        estado, pos, pila = actual
        operaciones += 1
        if estado == 'q2' and pos == n:
            final = actual
            break
        opciones = []
        if estado == 'q0' and pila == ('Z0',):
            opciones.append((('q1', pos, ('S', 'Z0')), 'epsilon, Z0 -> S Z0'))
        elif estado == 'q1' and pila:
            cima, resto = pila[0], pila[1:]
            if cima in NO_TERMINALES:
                for rhs in PRODUCCIONES[cima]:
                    opciones.append((('q1', pos, rhs + resto), f'epsilon, {cima} -> {" ".join(rhs)}'))
            elif cima == 'Z0':
                if pos == n:
                    opciones.append((('q2', pos, pila), 'epsilon, Z0 -> Z0'))
            elif pos < n and cima == palabras[pos]:
                opciones.append((('q1', pos + 1, resto), f'{cima}, {cima} -> epsilon'))
        for proximo, accion in opciones:
            _, nuevo_pos, nueva_pila = proximo
            utiles = nueva_pila[:-1] if nueva_pila and nueva_pila[-1] == 'Z0' else nueva_pila
            # Cada simbolo pendiente genera al menos un token; poda correcta.
            if len(utiles) > n - nuevo_pos:
                continue
            # Si la cima contiene terminales, deben coincidir con el prefijo restante.
            prefijo = []
            for s in utiles:
                if s in NO_TERMINALES:
                    break
                prefijo.append(s)
            if tuple(prefijo) != palabras[nuevo_pos:nuevo_pos + len(prefijo)]:
                continue
            if proximo not in anterior:
                anterior[proximo] = (actual, accion)
                cola.append(proximo)
    pasos = []
    if final is not None:
        actual = final
        while actual is not None:
            previo, accion = anterior[actual]
            estado, pos, pila = actual
            pasos.append({'estado': estado, 'entrada_restante': ' '.join(palabras[pos:]) or 'epsilon', 'pila': ' '.join(pila), 'transicion': accion})
            actual = previo
        pasos.reverse()
    return {'acepta': final is not None, 'pasos': pasos, 'operaciones': operaciones}
