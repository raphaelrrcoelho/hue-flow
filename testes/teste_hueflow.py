import unittest
import numpy as np
from hueflow.nos import No, Entrada, Soma
from hueflow.nos import Linear, Sigmoide, EQM
from hueflow.hueflow import ordenacao_topologica, propagacao, retropropagacao

class TesteGrafo(unittest.TestCase):
    def teste_ordenacao_topologica_de_nos(self):
        entrada_1 = Entrada()
        entrada_2 = Entrada()

        soma_teste = Soma(entrada_1, entrada_2)
        dict_entrada = {entrada_1: 42, entrada_2: 20}

        grafo_ordenado = [entrada_1, entrada_2, soma_teste]
        self.assertEqual(
            ordenacao_topologica(dict_entrada), grafo_ordenado)

    def teste_propagacao_da_rede(self):
        entrada_1 = Entrada()
        entrada_2 = Entrada()
        entrada_1.propagacao(42)
        entrada_2.propagacao(20)

        soma_teste = Soma(entrada_1, entrada_2)
        grafo_ordenado = [entrada_1, entrada_2, soma_teste]

        propagacao(grafo_ordenado)
        saida = soma_teste.valor
        self.assertAlmostEqual(saida, 62)

    def teste_retropropagacao_da_rede(self):
        entradas, pesos, vies, y = Entrada(), Entrada(), Entrada(), Entrada()

        entradas.propagacao(np.array([[-1., -2.],
                                      [-1, -2]]))
        pesos.propagacao(np.array([[2., 2], [3., 3]]))
        vies.propagacao(np.array([-3., -3]))
        y.propagacao(np.array([1., 2.]))

        linear = Linear([entradas, pesos, vies])
        sigmoide = Sigmoide([linear])
        custo = EQM([y, sigmoide])

        grafo_ordenado = [entradas, pesos, vies, linear,
                          sigmoide, y, custo]

        propagacao(grafo_ordenado)
        retropropagacao(grafo_ordenado)

        saida = np.array([[8.3504878e-05, 8.3504878e-05],
                          [8.3504878e-05, 8.3504878e-05]])
        np.testing.assert_almost_equal(
            pesos.gradientes[pesos], saida)
