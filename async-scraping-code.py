from bs4 import BeautifulSoup
import re
import numpy as np
from time import time
import pandas as pd
import asyncio
import aiohttp


async def create_links(quantidade):
    zonas = ['norte', 'sul', 'leste', 'oeste']
    link = 'https://imoveis.mercadolivre.com.br/casas/aluguel/sao-paulo/sao-paulo-zona-{}/{}'
    links = []

    for zona in zonas:
        cont = 0
        var = 49

        while cont < quantidade:

            if cont == 0:
                num_pag = ''

            else:
                num_pag = f'_Desde_{var}'
                var += 48

            links.append(link.format(zona, num_pag))
            cont += 1

    return links


async def get_html(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            resp.raise_for_status

            return await resp.text()


async def get_precos(html):
    re_precos = r'<span class="price-tag-fraction">(.*)<'
    lista_precos = []

    soup = BeautifulSoup(html, 'html.parser')

    for dado in soup.select('.ui-search-result__content-wrapper'):
        preco = dado.select_one('.price-tag-fraction')
        precos = re.findall(re_precos, str(preco))

        if len(precos) == 0:
            lista_precos.append(np.nan)
        else:
            p = int(precos[0].replace('.', ''))
            lista_precos.append(p)

    return lista_precos


async def get_atributos(html):
    re_quartos = r'([1-9]{1,2}) quarto[s]?'
    re_areas = r'<li class="ui-search-card-attributes__attribute">(.*) m²'

    soup = BeautifulSoup(html, 'html.parser')

    lista_areas = []
    lista_quartos = []

    for dado in soup.select('.ui-search-result__content-wrapper'):
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


async def create_dataframe(lista_precos, lista_areas, lista_quartos):
    dados = {}

    dados['preco'] = lista_precos
    dados['area'] = lista_areas
    dados['quartos'] = lista_quartos

    df = pd.DataFrame(dados)

    return df


async def create_csv(dataframe):
    df = pd.DataFrame(dataframe)
    df.to_csv('dados_imoveis2.csv', index=False)


async def create_csv():
    links = await create_links(10)
    tarefas = []
    precos = []
    areas = []
    quartos = []

    for link in links:
        tarefas.append(asyncio.create_task(get_html(link)))

    for tarefa in tarefas:
        html = await tarefa

        dados = await asyncio.gather(
            get_precos(html),
            get_atributos(html)
        )

        precos = precos + dados[0]
        areas = areas + dados[1][0]
        quartos = quartos + dados[1][1]

    df = await create_dataframe(precos, areas, quartos)
    df = pd.DataFrame(df)
    df.to_csv('dados_imoveis_async.csv', index=False)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_csv())
    loop.close()


if __name__ == '__main__':
    t0 = time()
    main()
    print(f'Tempo de execução: {time() - t0} segundos.')

    # Tempo de execução: 29.01470398902893 segundos.
