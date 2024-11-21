import trie
import sys
import time
import json
import os
from dataclasses import dataclass, asdict
from typing import List

@dataclass
class EstatisticasCompressao:
    momento: float
    tamanho_entrada: int
    tamanho_saida: int
    taxa_compressao: float
    tamanho_dicionario: int
    memoria_dicionario: int
    tempo_execucao: float

def calcular_memoria_dicionario(dicionario: trie.Trie, n_max_bytes: int) -> int:
    memoria = 0
    def calcular_memoria_no(no):
        return 8 + len(no.filho) * n_max_bytes  # Overhead mínimo + entradas do dicionario

    def percorrer(no):
        nonlocal memoria
        memoria += calcular_memoria_no(no)
        for filho in no.filho.values():
            percorrer(filho)

    percorrer(dicionario.raiz)
    return memoria

def comprimir(arquivo_entrada: str,  n_max_bits: int, arquivo_saida: str=None, coletar_stats: bool=False) -> List[EstatisticasCompressao]: 
    if arquivo_saida is None:
        arquivo_saida = arquivo_entrada + ".lzw"

    estatisticas = []
    tempo_inicio = time.time()

    TAMANHO_MAX = 1 << n_max_bits

    # Inicializar trie
    dicionario = trie.Trie()
    for byte in range(256):
        dicionario.inserir(bytes([byte]))
    
    codigo_atual = 256  # Próximo código disponível
    buffer_bits = 0
    contador_bits = 0

    tamanho_entrada = os.path.getsize(arquivo_entrada)
    bytes_processados = 0

    with open(arquivo_entrada, 'rb') as entrada, open(arquivo_saida, 'wb') as saida:
        w = bytes()

        # Primeiro byte do arquivo comprimido indica tamanho dos códigos
        saida.write(bytes([n_max_bits]))

        while True:
            k = entrada.read(1)
            if not k:
                break
            
            bytes_processados += 1
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
                # Coleta estatísticas após processar cada caractere
                if coletar_stats and bytes_processados % 100 == 0:  # Coleta a cada 100 bytes para reduzir overhead
                    stats_atual = EstatisticasCompressao(
                        momento=time.time() - tempo_inicio,
                        tamanho_entrada=bytes_processados,
                        tamanho_saida=saida.tell(),
                        taxa_compressao=saida.tell() / bytes_processados,
                        tamanho_dicionario=dicionario.tamanho,
                        memoria_dicionario=calcular_memoria_dicionario(dicionario, n_max_bits),
                        tempo_execucao=time.time() - tempo_inicio
                    )
                    estatisticas.append(stats_atual)

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

        if coletar_stats:
            stats_final = EstatisticasCompressao(
                momento=time.time() - tempo_inicio,
                tamanho_entrada=bytes_processados,
                tamanho_saida=saida.tell(),
                taxa_compressao=saida.tell() / bytes_processados,
                tamanho_dicionario=dicionario.tamanho,
                memoria_dicionario=calcular_memoria_dicionario(dicionario, n_max_bits),
                tempo_execucao=time.time() - tempo_inicio
            )
            estatisticas.append(stats_final)
            
    if coletar_stats:
        arquivo_stats = arquivo_saida + ".stats"
        with open(arquivo_stats, 'w') as f:
            json.dump([asdict(s) for s in estatisticas], f)
            
    return estatisticas

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Compressor LZW com coleta de estatísticas')
    parser.add_argument('arquivo_entrada', help='Arquivo a ser comprimido')
    parser.add_argument('--bits', '-b', type=int, default=12, 
                       help='Número máximo de bits (8-16, padrão: 12)')
    parser.add_argument('--stats', '-s', action='store_true',
                       help='Coletar estatísticas de compressão')
    parser.add_argument('--saida', '-o', help='Arquivo de saída (opcional)')
    
    args = parser.parse_args()

    if args.bits < 8 or args.bits > 16:
        print("Erro: número de bits deve estar entre 8 e 16")
        sys.exit(1)

    try:
        estatisticas = comprimir(
            arquivo_entrada=args.arquivo_entrada,
            n_max_bits=args.bits,
            arquivo_saida=args.saida,
            coletar_stats=args.stats
        )
        
        if args.stats:
            print(f"Estatísticas salvas em: {args.arquivo_entrada}.lzw.stats")
            
    except Exception as e:
        print(f"Erro durante a compressão: {e}")
        sys.exit(1)