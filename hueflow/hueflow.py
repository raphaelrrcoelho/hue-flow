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

    def propagacao_frente(self, valor = None):
        if valor is not None:
            self.valor = valor

class Soma(No):
    def __init__(self, x, y):
        No.__init__(self, [x, y])

    def propagacao_frente(self):
        self.valor = sum([ no.valor for no in self.nos_entrada ])

def ordenacao_topologica(dict_entrada):
    """
    Ordena nós genéricos em ordem topológica utilizando o Algorítmo de Kahn.
    'dict_entrada': Um dicionário onde a chave é um nó de 'Entrada'.
    Retorna uma lista de nós ordenados.
    """

    nos_entrada = [ no for no in dict_entrada.keys() ]

    G = {}
    nos = [ n for n in nos_entrada ]
    while len(nos) > 0:
        no = nos.pop(0)
        if no not in G:
            G[no] = {'entrada': set(), 'saida': set()}
        for m in no.nos_saida:
            if m not in G:
                G[m] = {'entrada': set(), 'saida': set()}
            G[no]['saida'].add(m)
            G[m]['entrada'].add(no)
            nos.append(m)

    L = []
    S = set(nos_entrada)
    while len(S) > 0:
        no = S.pop()

        if isinstance(no, Entrada):
            no.valor = dict_entrada[no]

        L.append(no)
        for m in no.nos_saida:
            G[no]['saida'].remove(m)
            G[m]['entrada'].remove(no)
            # Se não há nenhum outro nó de entrada, adicione em S
            if len(G[m]['entrada']) == 0:
                S.add(m)

    return L

def propagacao_frente(no_saida, nos_ordenados):
    """
    Realiza uma passagem para a frente por uma lista de nós ordenados.

    Argumentos:
    'output_node': O nó de saída do grafo (sem arestas de saída).
    'sorted_nodes': uma lista topologicamente ordenada de nós.

    Retorna o valor do nó de saída
    """

    for no in nos_ordenados:
        no.propagacao_frente()

    return no_saida.valor
