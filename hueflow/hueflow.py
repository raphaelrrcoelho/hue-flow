import numpy as np

class No(object):
    def __init__(self, nos_entrada = []):
        self.nos_entrada = nos_entrada

        self.nos_saida = []

        for no in self.nos_entrada:
            no.nos_saida.append(self)

        self.valor = None

    def propagacao_frente(self):
        """
        Propagação para a frente.

        Calcula o valor de saída baseando-se nos `inbound_nodes` e
        armazena o valor final em self.value.
        """
        raise NotImplemented

class Entrada(No):
    def __init__(self):
        No.__init__(self)

    def propagacao_frente(self, valor):
        if valor:
            self.valor = valor

class Soma(No):
    def __init__(self, x, y):
        No.__init__(self, [x, y])

    def propagacao_frente(self):
        return sum([ no.valor for no in self.nos_entrada ])
