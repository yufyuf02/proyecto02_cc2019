# Proyecto 2 - Teoria de la Computacion (CC2019)

Implementacion en Python 3, sin dependencias externas, de un PDA no determinista construido a partir de la gramatica G y del algoritmo CYK.

## Ejecutar

```bash
python main.py "she eats the cake" --pasos
python main.py "he cuts a cake with a knife" --metodo pda --pasos
python main.py "the cat drinks" --metodo cyk --pasos
python -m unittest -v
```

Sin argumento, el programa solicita una frase. Las palabras se separan por espacios y se convierten a minusculas.

## Archivos

- `gramatica.py`: producciones exactas del enunciado y comprobacion de CNF.
- `pda.py`: simulacion de NPDA mediante exploracion BFS de configuraciones, con registro de trayectoria aceptante.
- `cyk.py`: tabla CYK y reconstruccion de un arbol de derivacion.
- `main.py`: interfaz de linea de comandos.
- `test_proyecto.py`: pruebas automaticas positivas y negativas.

## Notas

- El PDA usa transiciones epsilon para expandir variables y consume palabras terminales cuando coinciden con la cima de la pila.
- Se evita el ciclo infinito de la recursion izquierda `VP -> VP PP` mediante deteccion de configuraciones repetidas y una poda basada en la longitud minima generada por los simbolos pendientes.
- CYK muestra la tabla por longitudes y un arbol de derivacion cuando acepta.
- Los contadores de operaciones son instrumentacion de la implementacion y NO equivalen a tiempos de reloj ni a un conteo uniforme de todas las instrucciones de Python.
- No se requiere GUI ni diagramas, segun el enunciado.
