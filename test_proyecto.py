import unittest
from pda import reconocer_pda
from cyk import reconocer_cyk

CASOS = [
    ('she eats', True), ('he cooks', True), ('the cat drinks', True),
    ('she eats the cake', True), ('he cuts a cake with a knife', True),
    ('the cat eats the meat in the oven', True),
    ('he drinks the juice with a spoon', True),
    ('she', False), ('eats the cake', False), ('he the cake', False),
    ('he eats with', False), ('the cat eats the', False),
    ('she eats pizza', False), ('', False), ('he eats the cake with', False),
]

class Pruebas(unittest.TestCase):
    def test_casos(self):
        for frase, esperado in CASOS:
            with self.subTest(frase=frase):
                pda = reconocer_pda(frase)
                cyk = reconocer_cyk(frase)
                self.assertEqual(pda['acepta'], esperado)
                self.assertEqual(cyk['acepta'], esperado)
                if esperado:
                    self.assertTrue(pda['pasos'])
                    self.assertTrue(cyk['derivacion'])

if __name__ == '__main__':
    unittest.main()
