# Compressão LZW

Esse repositório contém uma implementação do método de compressão Lempel-Ziv-Welch (LZW). Esse algoritmo utiliza um dicionário que permite a transformação de palavras do arquivo original em códigos, e assim a redução de seu tamanho. A grande vantagem deste método é a construção do dicionário ao mesmo tempo em que a compressão ou descompressão do arquivo é feita, o que faz ele ser adaptado a cada instância.

## Estrutura do código

### Trie.py

Nessa implementação, o dicionário foi implementado através de uma árvore Trie, que está no arquivo trie.py. A árvore é construida com base nas palavras que queremos armazenar no dicionário, e contém os métodos para Inserção, Remoção e Pesquisa de palavras. Como as palavras inseridas são sequências de bytes, descer um nível da árvore representa o crescimento da palavra em 1 byte.

Os nós da Trie foram implementados na classe "Vertice", que cotém dois atributos. O atributo "filho" é um dicionário que contém os vértices filhos de determinado vértice. Aqui, esse dicionário pode ter até 256 entradas, cada uma representando um dos possíveis números representados em apenas um byte. O outro atributo é "valor", que armazena o código para a palavra que o vértice simboliza.


### Compressor.py

A compressão de arquivos é feita pelo script "compressor.py". Que deve ser utilizado da seguinte forma:


python3 compressor.py "arquivo para compressão" -b "N"

N -> Número entre 9 e 16 que define o tamanho em bits dos códigos


O compressor funciona com qualquer tipo de arquivo, pois sua lógica está implementada em cima dos arquivos em binário. Assim, as palavras armazenadas no dicionário serão todas sequências de bytes.
A lógica da compressão está na função "comprimir", que recebe o arquivo a ser comprimido, o tamanho em bits dos códigos e um caminho para o arquivo de saída.
A função se inicia com a inicialização do dicionário, ou seja, inserimos na Trie todos os 256 valores possíveis que apenas um byte consegue armazenar (0 a 255). Na sequência, abrimos o arquivo a ser comprimido para leitura em modo binário, e o arquivo que iremos utilizar como saída para escrita em modo binário. O algoritmo segue da seguinte forma, começamos com uma palavra P inicialmente vazia e iteramos sobre todos os bytes do arquivo de entrada. A cada iteração concatenamos o byte lido com P e verificamos se o resultado está presente no dicionário, caso esteja, passamos ao próximo byte, caso contrário, escrevemos o código de P no arquivo de saída, adicionamos a concatenação de P com o byte lido no dicionário e a palavra P passa a conter apenas o byte lido. Essa iteração 


### Descompressor.py

A descompressão de arquivos é feita pelo script "descompressor.py". Que deve ser utilizado da seguinte forma:

python3 descompressor.py "arquivo para descompressão

## Exemplos

## Análise
