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

def ordenacao_topologica(dict_entrada):
    """
    Ordena nós genéricos em ordem topológica utilizando o Algorítmo de Kahn.
    'dict_entrada': Um dicionário onde a chave é um nó de 'Entrada'.
    Retorna uma lista de nós ordenados.
    """

    nos_entrada = [ n for n in dict_entrada.keys() ]

    G = {}
    nos = [ n for n in nos_entrada ]
    while len(nos) > 0:
        n = nos.pop(0)
        if n not in G:
            G[n] = {'entrada': set(), 'saida': set()}
        for m in n.nos_saida:
            if m not in G:
                G[m] = {'entrada': set(), 'saida': set()}
            G[n]['saida'].add(m)
            G[m]['entrada'].add(n)
            nos.append(m)

    L = []
    S = set(nos_entrada)
    while len(S) > 0:
        n = S.pop()

        if isinstance(n, Entrada):
            n.valor = dict_entrada[n]

        L.append(n)
        for m in n.nos_saida:
            G[n]['saida'].remove(m)
            G[m]['entrada'].remove(n)
            # Se não há nenhum outro nó de entrada, adicione em S
            if len(G[m]['entrada']) == 0:
                S.add(m)

    return L
