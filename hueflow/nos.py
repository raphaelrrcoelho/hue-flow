import numpy as np

class No(object):
    def __init__(self, nos_entrada = []):
        self.nos_entrada = nos_entrada

        self.nos_saida = []

        for no in self.nos_entrada:
            no.nos_saida.append(self)

        self.valor = None

        self.gradientes = {}

    #def __eq__(self, obj):
    #   return isinstance(obj, self.__class__) and obj.valor == self.valor

    def propagacao(self):
        """
        Todo nó que estende essa classe base deverá
        definir seu próprio método 'propagacao'.
        """
        raise NotImplemented

    def retropropagacao(self):
        """
        Todo nó que estende essa classe base deverá
        definir seu próprio método 'retropropagacao'.
        """
        raise NotImplementedError

class Entrada(No):
    def __init__(self):
        No.__init__(self)

    def propagacao(self, valor = None):
        if valor is not None:
            self.valor = valor

    def retropropagacao(self):
        self.gradientes = {self: 0}

        for no in self.nos_saida:
            gradiente_custo = no.gradientes[self]

            self.gradientes[self] += gradiente_custo * 1

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

    def retropropagacao(self):
        self.gradientes = { no: np.zeros(no.valor.shape) for no in self.nos_entrada }

        for no in self.nos_saida:
            gradiente_custo = no.gradientes[self]

            # parcial do custo em relação as entradas
            self.gradientes[self.nos_entrada[0]] += \
                    np.dot(gradiente_custo, self.nos_entrada[1].valor)
            # parcial do custo em relação aos pesos
            self.gradientes[self.nos_entrada[1]] += \
                    np.dot(gradiente_custo, self.nos_entrada[0].valor.T)
            # parcial do custo em relação aos vieses
            self.gradientes[self.nos_entrada[2]] += gradiente_custo.sum(axis = 1)

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
        Retorna a derivada da função Sigmóide.
        """
        return self._sigmoide(x) * (1 - self._sigmoide(x))

    def propagacao(self):
        self.valor = self._sigmoide(
            np.array([ no.valor for no in self.nos_entrada]))[0]

    def retropropagacao(self):
        self.gradientes = { no: np.zeros(no.valor.shape)
                            for no in self.nos_entrada }

        for no in self.nos_saida:
            gradiente_custo = no.gradientes[self]
            derivada = self._derivada(self.nos_entrada[0].valor)

            # parcial do custo em relação as entradas
            self.gradientes[self.nos_entrada[0]] += \
                    (gradiente_custo * derivada)

class EQM(No):
    def __init__(self, nos_entrada = []):
        No.__init__(self, nos_entrada)

    def propagacao(self):
        y = self.nos_entrada[0].valor
        y_chapeu = self.nos_entrada[1].valor

        self.erro = y - y_chapeu
        self.m = y.shape[0]
        self.valor = np.square(self.erro).sum() / self.m

    def retropropagacao(self):
        self.gradientes[self.nos_entrada[0]] = ( 2/self.m) * self.erro
        self.gradientes[self.nos_entrada[1]] = (-2/self.m) * self.erro

