from typing import Dict
from dataclasses import dataclass, field


@dataclass
class Vertice:
  filho: Dict[int, 'Vertice'] = field(default_factory=dict)
  valor: int = None 


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

        vertice = vertice.filho[byte]
      vertice.valor = self.tamanho

      self.tamanho += 1
      return True
    except Exception as e:
      print(f"Erro {e} ao inserir string {string}")
      return False

  def remover(self, palavra: bytes) -> bool:
    try:
      def _remover(vertice, palavra, index):
        if index == len(palavra):
          if vertice.valor is not None:
            vertice.valor = None
            return len(vertice.filho) == 0
          return False
        byte = palavra[index]
        if byte in vertice.filho:
          should_delete = _remover(vertice.filho[byte], palavra, index + 1)
          if should_delete:
            del vertice.filho[byte]
            return len(vertice.filho) == 0 and vertice.valor is None
          return False
        return False
      result = _remover(self.raiz, palavra, 0)
      if result:
        self.tamanho -= 1
      return result
    except Exception as e:
      print(f"Erro {e} ao remover string {palavra}")
      return False
    
  def procurar(self, palavra: bytes) -> Vertice:
    try:
      v_atual = self.raiz
      for byte in palavra:
        if byte not in v_atual.filho:
          return None
        v_atual = v_atual.filho[byte]
      return v_atual
    except Exception as e:
      print(f"Erro {e} ao buscar string {palavra}")
      return None