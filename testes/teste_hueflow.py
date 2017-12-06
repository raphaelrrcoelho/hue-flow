import unittest
from hueflow.hueflow import No

class TesteNo(unittest.TestCase):
    
    def setUp(self):
       no_1 = No()
       no_2 = No()
       self.nos_entrada = [no_1, no_2]
        
    def teste_criar_no_com_lista_de_nos_de_entrada(self):
       no_teste = No(nos_entrada = self.nos_entrada)
       self.assertEqual(no_teste.nos_entrada, self.nos_entrada)

    def teste_adicionar_a_si_como_saida_dos_seus_nos_de_entrada(self):
        no_teste = No(nos_entrada = self.nos_entrada)
        
        self.assertTrue(no_teste in self.nos_entrada[0].nos_saida)
        self.assertTrue(no_teste in self.nos_entrada[1].nos_saida)
