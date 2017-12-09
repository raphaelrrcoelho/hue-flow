import unittest
import numpy as np
from hueflow.nos import No, Entrada, Soma
from hueflow.nos import Linear, Sigmoide, EQM
from hueflow.hueflow import ordenacao_topologica, propagacao

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

class TesteEntrada(unittest.TestCase):
    def teste_propagacao_apenas_armazena_valor(self):
        entrada_teste = Entrada()

        self.assertEqual(entrada_teste.valor, None)

        entrada_teste.propagacao(42)
        self.assertEqual(entrada_teste.valor, 42)

class TesteSoma(unittest.TestCase):
    def teste_propagacao_soma_dois_nos_de_entrada(self):
        entrada_1 = Entrada()
        entrada_2 = Entrada()
        entrada_1.propagacao(42)
        entrada_2.propagacao(20)

        soma_teste = Soma(entrada_1, entrada_2)
        soma_teste.propagacao()

        self.assertEqual(soma_teste.valor, 62)

    def teste_propagacao_soma_n_nos_de_entrada(self):
        entrada_1 = Entrada()
        entrada_2 = Entrada()
        entrada_3 = Entrada()
        entrada_1.propagacao(42)
        entrada_2.propagacao(10)
        entrada_3.propagacao(40)

        soma_teste = Soma(entrada_1, entrada_2, entrada_3)
        soma_teste.propagacao()

        self.assertEqual(soma_teste.valor, 92)

class TesteLinear(unittest.TestCase):
    def teste_produto_escalar_de_nos_de_entradas_e_pesos(self):
        entradas, pesos, vies = Entrada(), Entrada(), Entrada()

        entradas.propagacao([6, 12, 3])
        pesos.propagacao([0.5, 0.25, 1.5])
        vies.propagacao([2])

        linear_teste = Linear([entradas, pesos, vies])
        linear_teste.propagacao()

        self.assertEqual(linear_teste.valor, 12.5)

    def teste_produto_escalar_matrizes_de_entradas_e_pesos(self):
        X, W, b = Entrada(), Entrada(), Entrada()

        X.propagacao(np.array([[-1., -2.], [-1, -2]]))
        W.propagacao(np.array([[2., -3], [2., -3]]))
        b.propagacao(np.array([-3., -5]))

        linear_teste = Linear([X, W, b])
        linear_teste.propagacao()

        saida = np.array([[-9., 4.], [-9., 4.]])
        self.assertTrue((linear_teste.valor == saida).all())

    def teste_retropropagacao_de_entradas_e_pesos(self):
        X, W, b, y = Entrada(), Entrada(), Entrada(), Entrada()
        linear_teste = Linear([X, W, b])

        custo = EQM([y, linear_teste])

        X.propagacao(np.array([[1., 1.], [1., 1.]]))
        W.propagacao(np.array([[1., 1.], [1., 1.]]))
        b.propagacao(np.array([0, 0]))
        y.propagacao(np.array([1, 3]))

        linear_teste.propagacao()
        custo.propagacao()

        custo.retropropagacao()
        linear_teste.retropropagacao()

        erro = (y.valor - linear_teste.valor)

        gradiente_entradas = (-2/3) * erro.dot(W.valor)
        gradiente_pesos = (-2/3) * erro.dot(X.valor)
        gradiente_vies = (-2/3) * erro.sum(axis = 1)

        np.testing.assert_almost_equal(
            linear_teste.gradientes[X], gradiente_entradas)
        np.testing.assert_almost_equal(
            linear_teste.gradientes[W], gradiente_pesos)
        np.testing.assert_almost_equal(
            linear_teste.gradientes[b], gradiente_vies)

class TesteSigmoide(unittest.TestCase):
    def teste_funcao_ativacao_de_sigmoide(self):
        sigmoide_teste = Sigmoide()
        entrada_infinita = np.array([np.log(0)])
        saida = np.array([0])

        self.assertAlmostEqual(
            sigmoide_teste._sigmoide(entrada_infinita), saida)

    def teste_derivada_do_sigmoide(self):
        sigmoide_teste = Sigmoide()
        x = np.array([0])
        x_linha = np.array([.25])

        np.testing.assert_almost_equal(
            sigmoide_teste._derivada(x), x_linha)

    def teste_sigmoide_em_produto_escalar_de_matrizes_e_pesos(self):
        X, W, b = Entrada(), Entrada(), Entrada()

        X.propagacao(np.array([[-1., -2.], [-1, -2]]))
        W.propagacao(np.array([[2., -3], [2., -3]]))
        b.propagacao(np.array([-3., -5]))

        linear = Linear([X, W, b])
        linear.propagacao()

        sigmoide_teste = Sigmoide([linear])
        sigmoide_teste.propagacao()

        saida = np.array([[1.23394576e-04, 9.82013790e-01],
                          [1.23394576e-04, 9.82013790e-01]])
        np.testing.assert_almost_equal(sigmoide_teste.valor, saida)

    def teste_retropropagacao_de_entradas_e_pesos(self):
        X, W, b = Entrada(), Entrada(), Entrada()
        y = Entrada()

        linear = Linear([X, W, b])
        sigmoide_teste = Sigmoide([linear])
        custo = EQM([y, sigmoide_teste])

        X.propagacao(np.array([[1., 0.],
                               [1., 1.]]))
        W.propagacao(np.array([[0.], [0.]]))
        b.propagacao(np.array([0, 0]))
        y.propagacao(np.array([0, 1]))

        linear.propagacao()
        sigmoide_teste.propagacao()
        custo.propagacao()

        custo.retropropagacao()
        sigmoide_teste.retropropagacao()

        sigmoide_derivada = sigmoide_teste._derivada(linear.valor)
        erro = (y.valor - sigmoide_teste.valor)

        gradiente_entradas = (-2/2) * (erro * sigmoide_derivada)

        np.testing.assert_almost_equal(
            sigmoide_teste.gradientes[linear], gradiente_entradas)

class TesteEQM(unittest.TestCase):
    def teste_erro_quadratico_medio_para_saida_e_aproximacao(self):
        y, y_chapeu = Entrada(), Entrada()

        y.propagacao(np.array([1, 2, 3]))
        y_chapeu.propagacao(np.array([4.5, 5, 10]))

        eqm_teste = EQM([y, y_chapeu])
        eqm_teste.propagacao()

        self.assertAlmostEqual(eqm_teste.valor, 23.4166666667)

    def teste_retropropagacao_saidas_e_corretos(self):
        y, y_chapeu = Entrada(), Entrada()

        y.propagacao(np.array([1, 2, 3]))
        y_chapeu.propagacao(np.array([4.5, 5, 10]))

        eqm_teste = EQM([y, y_chapeu])
        eqm_teste.propagacao()
        eqm_teste.retropropagacao()

        gradiente_entradas = (-2/3) * (y.valor - y_chapeu.valor)
        gradiente_respostas = (2/3) * (y.valor - y_chapeu.valor)

        np.testing.assert_almost_equal(
            eqm_teste.gradientes[y_chapeu], gradiente_entradas)
        np.testing.assert_almost_equal(
            eqm_teste.gradientes[y], gradiente_respostas)
