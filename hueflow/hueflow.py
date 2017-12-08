import numpy as np
from hueflow.nos import Entrada

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

def propagacao(no_saida, nos_ordenados):
    """
    Realiza uma passagem para a frente por uma lista de nós ordenados.

    Argumentos:
    'no_saida': O nó de saída do grafo (sem arestas de saída).
    'nos_ordenados': uma lista topologicamente ordenada de nós.

    Retorna o valor do nó de saída
    """

    for no in nos_ordenados:
        no.propagacao()

    return no_saida.valor
