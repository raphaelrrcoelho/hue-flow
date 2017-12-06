import unittest
from hueflow.hueflow import No

class TesteNo(unittest.TestCase):

    def teste_criar_no_com_lista_de_nos_de_entrada(self):
       no_1 = No()
       no_2 = No()
       no_3 = No(nos_entrada = [no_1, no_2])

       self.assertEqual(no_3.nos_entrada, [no_1, no_2])

    def teste_adicionar_a_si_como_saida_dos_seus_nos_de_entrada(self):
        pass
