import trie
import sys

def comprimir(arquivo_entrada: str,  n_max_bits: int, arquivo_saida: str=None) -> None:
    
    if arquivo_saida is None:
        arquivo_saida = arquivo_entrada + ".lzw"

    TAMANHO_MAX = 1 << n_max_bits

    # Inicializar trie
    dicionario = trie.Trie()
    for byte in range(256):
        dicionario.inserir(bytes([byte]))
    
    codigo_atual = 256  # Próximo código disponível

    buffer_bits = 0
    contador_bits = 0

    with open(arquivo_entrada, 'rb') as entrada, open(arquivo_saida, 'wb') as saida:
        w = bytes()

        # Primeiro byte do arquivo comprimido indica tamanho dos códigos
        saida.write(bytes([n_max_bits]))

        while True:
            k = entrada.read(1)
            if not k:
                break

            wk = w + k
            vertice = dicionario.procurar(wk)

            if vertice is not None:
                w = wk
            else:
                # Escreve código de w
                vertice_w = dicionario.procurar(w)
                if vertice_w:
                    code_w = vertice_w.valor
                else:
                    raise ValueError("Código não encontrado na Trie")

                # Empacota código em n_max_bits
                buffer_bits = (buffer_bits << n_max_bits) | code_w
                contador_bits += n_max_bits

                # Escreve bytes completos
                while contador_bits >= 8:
                    byte_saida = (buffer_bits >> (contador_bits - 8)) & 0xFF
                    saida.write(bytes([byte_saida]))
                    contador_bits -= 8

                # Adiciona wk ao dicionário se houver espaço
                if codigo_atual < TAMANHO_MAX:
                    dicionario.inserir(wk)
                    codigo_atual += 1

                w = k

        # Processa última palavra
        if w:
            vertice_w = dicionario.procurar(w)
            if vertice_w:
                code_w = vertice_w.valor
            else:
                raise ValueError("Código não encontrado na Trie")

            buffer_bits = (buffer_bits << n_max_bits) | code_w
            contador_bits += n_max_bits

            # Escreve bits restantes
            while contador_bits > 0:
                if contador_bits >= 8:
                    byte_saida = (buffer_bits >> (contador_bits - 8)) & 0xFF
                    saida.write(bytes([byte_saida]))
                    contador_bits -= 8
                else:
                    byte_saida = (buffer_bits << (8 - contador_bits)) & 0xFF
                    saida.write(bytes([byte_saida]))
                    contador_bits = 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python compressor.py arquivo_entrada [n_max_bits]")
        sys.exit(1)

    arquivo = sys.argv[1]
    n_max_bits = 12

    # Controle de argumento n_max_bits
    if len(sys.argv) > 2:
        try:
            n_max_bits = int(sys.argv[2])
            if n_max_bits < 8 or n_max_bits > 16:
                print("Erro: n_max_bits deve estar entre 8 e 16")
                sys.exit(1)
        except ValueError:
            print("Erro: n_max_bits deve ser um número inteiro")
            sys.exit(1)

    comprimir(arquivo, n_max_bits)