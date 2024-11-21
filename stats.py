import json
import matplotlib.pyplot as plt
import sys
from pathlib import Path

def analisar_estatisticas_compressao(arquivo_stats: str):
    with open(arquivo_stats) as f:
        stats = json.load(f)
    
    partes = arquivo_stats.rsplit('.')
    nome_original = partes[0]

    momentos = [s['momento'] * 1000 for s in stats] 
    taxas_compressao = [s['taxa_compressao'] for s in stats]
    tamanhos_dicionario = [s['tamanho_dicionario'] for s in stats]
    memoria_dicionario = [s['memoria_dicionario'] / 1024 for s in stats]
    
    plt.style.use('seaborn')
    figsize = (10, 6)
    
    # Gráfico 1: Taxa de Compressão
    plt.figure(figsize=figsize)
    plt.plot(momentos, taxas_compressao, 'b-', linewidth=3)
    plt.title('Taxa de Compressão ao Longo do Tempo')
    plt.xlabel('Tempo (ms)')
    plt.ylabel('Taxa de Compressão')
    plt.grid(True)
    plt.savefig(f'{nome_original}-taxa_compressao.png')
    plt.close()
    
    # Gráfico 2: Tamanho do Dicionário
    plt.figure(figsize=figsize)
    plt.plot(momentos, tamanhos_dicionario, 'b-', linewidth=3)
    plt.title('Crescimento do Dicionário')
    plt.xlabel('Tempo (ms)')
    plt.ylabel('Número de Entradas')
    plt.grid(True)
    plt.savefig(f'{nome_original}-tamanho_dicionario.png')
    plt.close()
    
    # Gráfico 3: Memória do Dicionário
    plt.figure(figsize=figsize)
    plt.plot(momentos, memoria_dicionario, 'b-', linewidth=3)
    plt.title('Consumo de Memória do Dicionário')
    plt.xlabel('Tempo (ms)')
    plt.ylabel('Memória (KB)')
    plt.grid(True)
    plt.savefig(f'{nome_original}-memoria_dicionario.png')
    plt.close()
    
    # Relatório de estatísticas finais
    stats_final = stats[-1]
    with open(f'{nome_original}-relatorio_final.txt', 'w') as f:
        f.write(f"""Relatório Final de Compressão
=========================
Tempo Total: {stats_final['tempo_execucao']*1000:.2f}ms
Taxa de Compressão Final: {stats_final['taxa_compressao']:.2f}
Entradas no Dicionário: {stats_final['tamanho_dicionario']}
Memória do Dicionário: {stats_final['memoria_dicionario']/1024:.2f}KB
""")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python analisar_estatisticas.py <arquivo_stats>")
        sys.exit(1)
        
    analisar_estatisticas_compressao(sys.argv[1])