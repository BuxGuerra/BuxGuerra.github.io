import trie
import sys


def descomprimir(arquivo_entrada: str, arquivo_saida: str=None) -> None:
    if arquivo_saida is None:
        partes = arquivo_entrada.rsplit('.', 2)
        if len(partes) == 3 and partes[2] == 'lzw':
            arquivo_saida = f"{partes[0]}_descomprimido.{partes[1]}"
        else:
            raise ValueError("Formato do arquivo de entrada inválido. Esperado: nome_do_arquivo.{extensão}.lzw")

    # Inicializar trie
    dicionario = trie.Trie()
    codigo_para_sequencia = {}
    for i in range(256):
      seq = bytes([i])
      dicionario.inserir(seq)
      codigo_para_sequencia[i] = seq

    codigo_atual = 256
    buffer_bits = 0
    contador_bits = 0
    
    with open(arquivo_entrada, 'rb') as entrada, open(arquivo_saida, 'wb') as saida:
        n_max_bits_data = entrada.read(1)
        if not n_max_bits_data:
            print("Arquivo vazio ou corrompido.")
            return
        n_max_bits = n_max_bits_data[0]
        TAMANHO_MAX = 1 << n_max_bits
        
        # Lê todos os códigos do arquivo
        sequencia_codigos = []
        while True:
            byte = entrada.read(1)
            if not byte:
                break
            buffer_bits = (buffer_bits << 8) | byte[0]
            contador_bits += 8
            while contador_bits >= n_max_bits:
                contador_bits -= n_max_bits
                codigo = (buffer_bits >> contador_bits) & (TAMANHO_MAX - 1)
                sequencia_codigos.append(codigo)
                buffer_bits &= (1 << contador_bits) - 1  # Limpa os bits já usados
                    
        # Decodificação usando o Trie
        w = b''
        for k in sequencia_codigos:
            if k in codigo_para_sequencia:
                entrada_atual = codigo_para_sequencia[k]
            elif k == codigo_atual and w:
                entrada_atual = w + w[:1]
            else:
                raise ValueError(f'Erro ao decodificar: código inválido {k}')

            saida.write(entrada_atual)

            if w:
                novo_entrada = w + entrada_atual[:1]
                if codigo_atual < TAMANHO_MAX:
                    dicionario.inserir(novo_entrada)
                    codigo_para_sequencia[codigo_atual] = novo_entrada
                    codigo_atual += 1

            w = entrada_atual

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Uso: python descompressor.py arquivo_entrada")
    sys.exit(1)

  arquivo = sys.argv[1]
  descomprimir(arquivo)
