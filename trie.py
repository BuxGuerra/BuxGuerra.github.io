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
    try:
      vertice = self.raiz
      for byte in string:
        if byte not in vertice.filho:
          vertice.filho[byte] = Vertice()
        else: 
           print("string já está na Trie")
           return False
        vertice = vertice.filho[byte]
      vertice.valor = bytes([self.tamanho])
      self.tamanho += 1
      return True
    except Exception as e:
      print(f"Erro {e} ao inserir string{string}")
      return False       

  def remover(self, palavra: bytes) -> bool:
    try:
      vertices_para_deletar = []
      v_atual = self.raiz

      for byte in palavra:
        if byte not in v_atual.filho:
            print("string não encontrada")
            return False
        vertices_para_deletar.append((v_atual, byte))
        v_atual = v_atual.filho[byte]
      
      if v_atual.valor is None:
        return False
      
      v_atual.valor = None

      while vertices_para_deletar:
        pai, byte = vertices_para_deletar.pop()
        v_filho = pai.filho[byte]

        if len(v_filho.filho[byte]) == 0 and v_filho.valor is None:
            del pai.filho[byte]

      self.tamanho -= 1
      return True
    
    except Exception as e:
       print(f"Erro {e} ao deletar string{palavra}")

  def procurar(self, palavra: bytes) -> Vertice:
    try:
      v_atual = self.raiz
      for byte in palavra:
        if byte not in v_atual.filho:
            return None
        v_atual = v_atual.filho[byte]
      return v_atual
    except Exception as e:
      print(f"Erro {e} ao buscar string{palavra}")
