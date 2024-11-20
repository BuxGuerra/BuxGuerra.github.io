from typing import Dict
from dataclasses import dataclass, field


@dataclass
class Vertice:
  filho: Dict[int, 'Vertice'] = field(default_factory=dict)
  valor: bytes = None


class Trie:
  def __init__(self):
    self.raiz = Vertice()
    self.tamanho = 0

  def inserir(self, string: bytes) -> bool:
    vAtual = self.raiz
    codigo = self.tamanho

    #começa do menos significativo
    for i in range(max_bits):
      bit = (codigo >> i) & 1
      if bit not in vAtual.filho:
        vAtual.filho[bit] = Vertice()
    vAtual = vAtual.filho[bit]
    
    vAtual.valor = string
    self.tamanho += 1
    return Trie
  

#  def remover(self, palavra: bytes) -> bool:
#    try:
#      vertices_para_deletar = []
#      v_atual = self.raiz
#
#      for byte in palavra:
#        if byte not in v_atual.filho:
#            print("string não encontrada")
#            return False
#        vertices_para_deletar.append((v_atual, byte))
#        v_atual = v_atual.filho[byte]
#      
#      if v_atual.valor is None:
#        return False
#      
#      v_atual.valor = None
#
#      while vertices_para_deletar:
#        pai, byte = vertices_para_deletar.pop()
#        v_filho = pai.filho[byte]
#
#        if len(v_filho.filho[byte]) == 0 and v_filho.valor is None:
#            del pai.filho[byte]
#
#      self.tamanho -= 1
#      return True
#    
#    except Exception as e:
#       print(f"Erro {e} ao deletar string{palavra}")



  def procurar(self, codigo: bytes) -> Vertice:

    vAtual = self.raiz
    #começa do menos significativo
    for i in range(max_bits):
      bit = (codigo >> i) & 1
      if bit not in vAtual.filho:
        return None
    vAtual = vAtual.filho[bit]
    return vAtual

