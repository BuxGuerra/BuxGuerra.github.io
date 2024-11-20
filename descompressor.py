import trie
import sys


def descomprimir(arquivo_entrada: str, arquivo_saida: str=None) -> None:
    
    # Inicializar trie
    dicionario = trie.Trie()
    for byte in range(256):
        dicionario.inserir(bytes([byte]))
    
    proximo_vertice = 256
    buffer_bits = 0
    contador_bits = 0
    
    with open(arquivo_entrada, 'rb') as entrada, open(arquivo_saida, 'wb') as saida:
        palavra = bytes()

        n_max_bits = entrada.read(1)
        
        while True:
            byte = entrada.read(1)
            if not byte:
                break


            buffer_bits = (buffer_bits << 8) | byte
            contador_bits += 8

            if contador_bits >= n_max_bits:
                c = (buffer_bits >> (contador_bits - n_max_bits)) & 0xFF
                
                if(dicionario.procurar(c) == None):
                    



            
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
        print("Uso: python descompressor.py arquivo_entrada")
        sys.exit(1)

    arquivo = sys.argv[1]
    

    descomprimir(arquivo)
