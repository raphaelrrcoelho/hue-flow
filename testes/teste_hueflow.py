import unittest
import numpy as np
from hueflow.nos import No, Entrada, Soma
from hueflow.nos import Linear, Sigmoide, EQM
from hueflow.hueflow import ordenacao_topologica, propagacao

class TesteGrafo(unittest.TestCase):
    def teste_ordenacao_topologica_de_nos(self):
        entrada_1 = Entrada()
        entrada_2 = Entrada()

        soma_teste = Soma(entrada_1, entrada_2)
        dict_entrada = {entrada_1: 42, entrada_2: 20}

        nos_ordenados = [entrada_1, entrada_2, soma_teste]
        self.assertEqual(
            ordenacao_topologica(dict_entrada), nos_ordenados)

    def teste_propagacao_da_rede(self):
        entrada_1 = Entrada()
        entrada_2 = Entrada()
        entrada_1.propagacao(42)
        entrada_2.propagacao(20)

        soma_teste = Soma(entrada_1, entrada_2)
        nos_ordenados = [entrada_1, entrada_2, soma_teste]

        saida = propagacao(soma_teste, nos_ordenados)
        self.assertEqual(saida, 62)
