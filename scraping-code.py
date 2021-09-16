import requests
from bs4 import BeautifulSoup
import re
import numpy as np
from time import sleep, time
import pandas as pd


def create_links(quantidade):
    zonas = ['norte', 'sul', 'leste', 'oeste']
    link = 'https://imoveis.mercadolivre.com.br/casas/aluguel/sao-paulo/sao-paulo-zona-{}/{}'

    for zona in zonas:
        cont = 0
        var = 49

        while cont < quantidade:
            if cont == 0:
                num_pag = ''

            else:
                num_pag = f'_Desde_{var}'
                var += 48

            yield (link.format(zona, num_pag), zona)
            cont += 1


def get_html(link):
    c = requests.get(link).content
    soup = BeautifulSoup(c, 'html.parser')

    return soup


def get_zonas(dicionario_zonas):
    l_zonas = [k for k, v in dicionario_zonas.items() for _ in range(v)]
    return l_zonas


def get_precos(soup_html):
    re_precos = r'<span class="price-tag-fraction">(.*)<'
    lista_precos = []

    for dado in soup_html.select('.ui-search-result__content-wrapper'):
        preco = dado.select_one('.price-tag-fraction')
        precos = re.findall(re_precos, str(preco))

        if len(precos) == 0:
            lista_precos.append(np.nan)
        else:
            p = int(precos[0].replace('.', ''))
            lista_precos.append(p)

    return lista_precos


def get_atributos(soup_html):

    re_quartos = r'([1-9]{1,2}) quarto[s]?'
    re_areas = r'<li class="ui-search-card-attributes__attribute">(.*) m²'

    lista_areas = []
    lista_quartos = []

    for dado in soup_html.select('.ui-search-result__content-wrapper'):
        metro = dado.select_one('.ui-search-card-attributes__attribute ')
        metros = re.findall(re_areas, str(metro))

        quartos = re.findall(re_quartos, dado.text)

        if len(metros) == 0:
            lista_areas.append(np.nan)
        else:
            lista_areas.append(int(metros[0].replace(',', '')))

        if len(quartos) == 0:
            lista_quartos.append(np.nan)
        else:
            q = int(quartos[0])
            lista_quartos.append(q)

    return lista_areas, lista_quartos


def create_dataframe(lista_precos, lista_areas, lista_quartos):
    dados = {}

    dados['preco'] = lista_precos
    dados['area'] = lista_areas
    dados['quartos'] = lista_quartos

    df = pd.DataFrame(dados)

    return df


def create_csv(dataframe):
    df = pd.DataFrame(dataframe)
    df.to_csv('dados_imoveis_normal.csv', index=False)


def main():
    gen = create_links(2)
    precos_temp = []
    area_temp = []
    quartos_temp = []
    teste = {}
    lista_norte = []
    lista_sul = []
    lista_leste = []
    lista_oeste = []

    for i in gen:
        html = get_html(i[0])
        p = get_precos(html)

        if i[1] == 'norte':
            lista_norte.extend(p)

        elif i[1] == 'sul':
            lista_sul.extend(p)

        elif i[1] == 'leste':
            lista_leste.extend(p)

        else:
            lista_oeste.extend(p)

    teste['norte'] = len(lista_norte)
    teste['sul'] = len(lista_sul)
    teste['leste'] = len(lista_leste)
    teste['oeste'] = len(lista_oeste)

    print(teste)
    """
        
        while cont < 2:
            html = get_html(i[0])
            print(html)
            p = get_precos(html)
            x.append(len(p))
            print(i[1])
            print(x)
            print('-' * 50)"""
    #print('-' * 100)
    #cont += 1

    """
        html = get_html(i)
        print(html)
        #p = get_precos(html)

        #print(p)
        print('-' * 50)

        at = get_atributos(html)

        precos_temp = precos_temp + p
        area_temp = area_temp + at[0]
        quartos_temp = quartos_temp + at[1]

    df = create_dataframe(precos_temp, area_temp, quartos_temp)
    create_csv(df)
"""


if __name__ == '__main__':
    t0 = time()
    main()
    print(f'Tempo de execução: {time() - t0} segundos.')

    # Tempo de execução: 93.20756077766418 segundos.
