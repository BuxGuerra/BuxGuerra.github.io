import trie
import sys

def comprimir(arquivoEntrada):

    #inicializar trie
    dicionario = trie.Trie()
    for byte in range(256):
        dicionario.inserir(bytes([byte]))

    l =""

    #processar arquivo
    with open(arquivoEntrada, 'rb') as entrada, open("./arquivoSaida", 'wb') as saida:
    
        while True:
            x = entrada.read(1)
            if not x:
                break

            if dicionario.procurar(l+x) != None:
                l = l+x
            else:
                saida.write(dicionario.procurar(l).valor)
                dicionario.inserir(l+x) #garantir que a logica da trie coloca o valor certo
                l = x

        #Garantir escrita da ultima palavra
        if l:
            saida.write(dicionario.procurar(l).valor)


    
if __name__ == '__main__':

    arquivo = sys.argv[1]
    comprimir(arquivo)