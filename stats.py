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
    figsize = (15, 10)
    
    fig, axs = plt.subplots(2, 2, figsize=figsize)
    
    # Adiciona título à figura
    fig.suptitle(f'Estatísticas de Compressão - {nome_original}', fontsize=16)
    
    # Gráfico 1: Taxa de Compressão
    axs[0, 0].plot(momentos, taxas_compressao, 'b-', linewidth=3)
    axs[0, 0].set_title('Taxa de Compressão ao Longo do Tempo')
    axs[0, 0].set_xlabel('Tempo (ms)')
    axs[0, 0].set_ylabel('Taxa de Compressão')
    axs[0, 0].grid(True)
    
    # Gráfico 2: Tamanho do Dicionário
    axs[0, 1].plot(momentos, tamanhos_dicionario, 'b-', linewidth=3)
    axs[0, 1].set_title('Crescimento do Dicionário')
    axs[0, 1].set_xlabel('Tempo (ms)')
    axs[0, 1].set_ylabel('Número de Entradas')
    axs[0, 1].grid(True)
    
    # Gráfico 3: Memória do Dicionário
    axs[1, 0].plot(momentos, memoria_dicionario, 'b-', linewidth=3)
    axs[1, 0].set_title('Consumo de Memória do Dicionário')
    axs[1, 0].set_xlabel('Tempo (ms)')
    axs[1, 0].set_ylabel('Memória (KB)')
    axs[1, 0].grid(True)
    
    # Remove the empty subplot
    fig.delaxes(axs[1, 1])
    
    plt.tight_layout()
    plt.savefig(f'{nome_original}-estatisticas_completas.png')
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

