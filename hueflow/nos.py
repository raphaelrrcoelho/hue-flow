import numpy as np

class No(object):
    def __init__(self, nos_entrada = []):
        self.nos_entrada = nos_entrada

        self.nos_saida = []

        for no in self.nos_entrada:
            no.nos_saida.append(self)

        self.valor = None

    #def __eq__(self, obj):
    #   return isinstance(obj, self.__class__) and obj.valor == self.valor

    def propagacao(self):
        """
        Propagação para a frente.

        Calcula o valor de saída baseando-se nos 'nos_entrada' e
        armazena o valor final em self.value.
        """
        raise NotImplemented

class Entrada(No):
    def __init__(self):
        No.__init__(self)

    def propagacao(self, valor = None):
        if valor is not None:
            self.valor = valor

class Soma(No):
    def __init__(self, *arg):
        No.__init__(self, list(arg))

    def propagacao(self):
        self.valor = sum([ no.valor for no in self.nos_entrada ])

class Linear(No):
    def __init__(self, entrada_peso_vies = []):
        No.__init__(self, entrada_peso_vies)

    def propagacao(self):
        entradas = self.nos_entrada[0].valor
        pesos = self.nos_entrada[1].valor
        vies = self.nos_entrada[2].valor

        self.valor = np.array(entradas).dot(pesos) + vies

class Sigmoide(No):
    def __init__(self, no_entrada = []):
        No.__init__(self, no_entrada)

    def _sigmoide(self, x):
        """
        'x': Um objeto semelhante a uma array do numpy.

        Retorna o resultado da função Sigmóide.
        """
        return 1 / (1 + np.exp(-x))

    def _derivada(self, x):
        """
        'x': Um objeto semelhante a uma array do numpy.

        Retorna a derivada da função Sigmóide.
        """
        return self._sigmoide(x) * (1 - self._sigmoide(x))

    def propagacao(self):
        self.valor = self._sigmoide(
            np.array([ no.valor for no in self.nos_entrada]))[0]

class EQM(No):
    def __init__(self, nos_entrada = []):
        No.__init__(self, nos_entrada)

    def propagacao(self):
        y = self.nos_entrada[0].valor
        y_chapeu = self.nos_entrada[1].valor

        self.valor = np.square(y - y_chapeu).sum() / y.shape[0]

