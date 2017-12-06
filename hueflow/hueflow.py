import numpy as np

class No(object):
    def __init__(self, nos_entrada = []):
       self.nos_entrada = nos_entrada

       self.nos_saida = []

       for no in self.nos_entrada:
           no.nos_saida.append(self)
