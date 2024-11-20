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
    
    proximo_vertice = 256
    buffer_bits = 0
    contador_bits = 0
    
    with open(arquivo_entrada, 'rb') as entrada, open(arquivo_saida, 'wb') as saida:
        palavra = bytes()
        
        while True:
            byte = entrada.read(1)
            if not byte:
                break
            
            palavra += byte
            vertice = dicionario.procurar(palavra)
            
            if vertice is None:
                # Escreve código da palavra anterior
                palavra_anterior = palavra[:-1]
                vertice_anterior = dicionario.procurar(palavra_anterior)
                if vertice_anterior:
                    vertice_anterior = int.from_bytes(vertice_anterior.valor, 'big')
                else:
                    raise ValueError("Código não encontrado na Trie")
                
                # Empacota código em n_max_bits
                buffer_bits = (buffer_bits << n_max_bits) | vertice_anterior
                contador_bits += n_max_bits
                
                # Escreve bytes completos
                while contador_bits >= 8:
                    byte_saida = (buffer_bits >> (contador_bits - 8)) & 0xFF
                    saida.write(bytes([byte_saida]))
                    contador_bits -= 8
                
                # Adiciona novo código se houver espaço
                if proximo_vertice < TAMANHO_MAX:
                    dicionario.inserir(palavra)
                    proximo_vertice += 1
                
                palavra = byte
        
        # Processa última palavra
        if palavra:
            vertice = dicionario.procurar(palavra).valor

            vertice = int.from_bytes(vertice, "big")

            buffer_bits = (buffer_bits << n_max_bits) | vertice
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
    
    # Default n_max_bits value
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
