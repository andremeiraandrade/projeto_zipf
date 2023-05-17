import fitz
import re
import pandas as pd
from collections import Counter

import numpy as np
import matplotlib as mt
import matplotlib.pyplot as plt
import seaborn as sns

# Fiz uma alteração aqui

with fitz.open('./base/Mente Milionária.pdf') as pdf:
    texto = ''
    for pagina in pdf:
        texto += pagina.get_text()

regex = re.compile("[a-z-áàãâéêíóôõçñ]+")
dados = regex.findall(texto.lower())

tot_palavras = len(dados)
tot_palavras_d = len(set(dados))

frequencia = Counter(dados).most_common()
frequencia_30 = dict(Counter(dados).most_common(30))
frequencia_50 = dict(Counter(dados).most_common(50))

i = 0
tabela = {}
posicoes = []

while i < len(frequencia):
    posicao = 10  
    for indice, item in enumerate(frequencia):  
        i += 1
        if indice == posicao-1:  
            posicoes.append(f'Posição: {posicao} | Palavra: {item[0]}')
            tabela[item[0]] = item[1]
            posicao *= 10

with open('./relatório/analiseZipf.txt', 'w', encoding='utf8') as arquivo:
    arquivo.write(f'Base: Mente Milionária.pdf\n\n')
    arquivo.write(f'Total de palavras: {tot_palavras}\nTotal de palavras distintas: {tot_palavras_d}\n\n')
    
    for item in posicoes:
        arquivo.write(f'{item}\n')


def visual_zipf():
    x = posicoes
    y = list(tabela.values())

    dados1 = pd.DataFrame({'Palavra': x, 'Quantidade': y})

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(dados1['Palavra']))

    grafico = ax.bar(x=x, height='Quantidade', data=dados1)

    ax.set_title('Análise de ZipF', fontsize=13, pad=15)
    ax.set_xlabel('Palavras', fontsize=12, labelpad=10)
    ax.set_ylabel('Quantidades', fontsize=12, labelpad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(dados1['Palavra'])
    ax.bar_label(grafico, size=10, label_type='edge')

    plt.savefig('./relatório/visual_Zipf.png', dpi=600, bbox_inches='tight')


def visual_30():
    dt = pd.DataFrame({
        'Palavra': frequencia_30.keys(),
        'Quantidade': frequencia_30.values()
    })

    x = list(frequencia_30.keys())
    y = list(frequencia_30.values())

    fig, ax = plt.subplots(figsize=(12, 6))
    mt.style.use(['seaborn'])

    sns.barplot(x=x, y=y)

    ax.set_title('Zipf Inicial (30+)', fontsize=12)
    ax.set_ylabel('Quantidade de Repetições', fontsize=12, color='purple')

    plt.xticks(rotation=60, fontsize=10)

    for indice, valor in enumerate(y):
        ax.text(x=indice-0.4, y=valor+0.9, s=valor, fontsize=10)

    plt.savefig('./relatório/visual_30.png', dpi=600, bbox_inches='tight')

  
