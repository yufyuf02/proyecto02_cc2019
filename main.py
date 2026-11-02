"""Uso: python main.py 'she eats the cake' --metodo ambos --pasos"""
import argparse
from pda import reconocer_pda
from cyk import reconocer_cyk


def ejecutar(frase, metodo='ambos', pasos=False):
    resultados = {}
    if metodo in ('pda', 'ambos'):
        r = reconocer_pda(frase)
        resultados['PDA'] = r['acepta']
        print(f'PDA: {"ACEPTADA" if r["acepta"] else "RECHAZADA"}; configuraciones exploradas: {r["operaciones"]}')
        if pasos:
            for k, p in enumerate(r['pasos']):
                print(f'  {k:02d}. ({p["estado"]}, {p["entrada_restante"]}, {p["pila"]}) [{p["transicion"]}]')
            if not r['acepta']:
                print('  No existe una trayectoria de aceptacion.')
    if metodo in ('cyk', 'ambos'):
        r = reconocer_cyk(frase)
        resultados['CYK'] = r['acepta']
        print(f'CYK: {"ACEPTADA" if r["acepta"] else "RECHAZADA"}; combinaciones comprobadas: {r["operaciones"]}')
        if pasos:
            for longitud, fila in enumerate(r['tabla'], 1):
                print(f'  Longitud {longitud}: {fila}')
            if r['derivacion']:
                print('  Arbol de derivacion:')
                for linea in r['derivacion']:
                    print('   ', linea)
            else:
                print('  S no aparece en la celda superior de la tabla.')
    return resultados

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Proyecto 2 - PDA y CYK')
    parser.add_argument('frase', nargs='?', help='Oracion entre comillas')
    parser.add_argument('--metodo', choices=['pda', 'cyk', 'ambos'], default='ambos')
    parser.add_argument('--pasos', action='store_true')
    args = parser.parse_args()
    ejecutar(args.frase if args.frase is not None else input('Ingrese una frase: '), args.metodo, args.pasos)
