# Compressão LZW

Esse repositório contém uma implementação do método de compressão Lempel-Ziv-Welch (LZW). Esse algoritmo utiliza um dicionário que permite a transformação de palavras do arquivo original em códigos, e assim a redução de seu tamanho. A grande vantagem deste método é a construção do dicionário ao mesmo tempo em que a compressão ou descompressão do arquivo é feita, o que faz ele ser adaptado a cada instância.

## Estrutura do código

### Trie.py

Nessa implementação, o dicionário foi implementado através de uma árvore Trie, que está no arquivo trie.py. A árvore é construida com base nas palavras que queremos armazenar no dicionário, e contém os métodos para Inserção, Remoção e Pesquisa de palavras. Como as palavras inseridas são sequências de bytes, descer um nível da árvore representa o crescimento da palavra em 1 byte.

Os nós da Trie foram implementados na classe "Vertice", que cotém dois atributos. O atributo "filho" é um dicionário que contém os vértices filhos de determinado vértice. Aqui, esse dicionário pode ter até 256 entradas, cada uma representando um dos possíveis números representados em apenas um byte. O outro atributo é "valor", que armazena o código para a palavra que o vértice simboliza.


### Compressor.py
