import requests
from bs4 import BeautifulSoup
import re
import numpy as np
from time import sleep, time
import pandas as pd


paginas = ['', '_Desde_49', '_Desde_97', '_Desde_145',
           '_Desde_193', '_Desde_241', '_Desde_289']


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

            yield link.format(zona, num_pag)
            cont += 1


def get_html(link):
    c = requests.get(link).content
    soup = BeautifulSoup(c, 'html.parser')

    return soup


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
    df.to_csv('dados_imoveis2.csv', index=False)


def main():
    gen = create_links(2)
    precos_temp = []
    area_temp = []
    quartos_temp = []

    for i in gen:
        html = get_html(i)
        sleep(2)
        p = get_precos(html)
        at = get_atributos(html)

        precos_temp = precos_temp + p
        area_temp = area_temp + at[0]
        quartos_temp = quartos_temp + at[1]

    df = create_dataframe(precos_temp, area_temp, quartos_temp)
    create_csv(df)


if __name__ == '__main__':
    main()
