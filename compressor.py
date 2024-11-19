import trie
import sys

def comprimir(arquivoEntrada):

    #inicializar trie
    dicionario = trie.Trie()
    for byte in range(256):
        dicionario.inserir(bytes([byte]))

    palavra = bytes()

    #processar arquivo
    with open(arquivoEntrada, 'rb') as entrada, open("./arquivoSaida", 'wb') as saida:
    
        while True:
            b = entrada.read(1)
            if not b:
                break

            if dicionario.procurar(palavra+b) != None:
                palavra = palavra+b
            else:
                saida.write(dicionario.procurar(palavra).valor)
                dicionario.inserir(palavra+b) #garantir que a logica da trie coloca o valor certo
                palavra = b

        #Garantir escrita da ultima palavra
        if palavra:
            saida.write(dicionario.procurar(palavra).valor)


    
if __name__ == '__main__':

    arquivo = sys.argv[1]
    comprimir(arquivo)