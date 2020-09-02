import requests
from bs4 import BeautifulSoup
import re
import numpy as np
from time import sleep
import pandas as pd

zonas = ['norte', 'sul', 'leste', 'oeste']
url_ml = 'https://imoveis.mercadolivre.com.br/casas/aluguel/sao-paulo/sao-paulo-zona-{}'

re_precos = r'<span class="price-tag-fraction">(.*)<'
re_quartos = r'[1-9]{1,2} quarto'
re_areas = r'<li class="ui-search-card-attributes__attribute">(.*) m²'


class Scraper:
    zona = []
    area = []
    quartos = []
    preco = []
    dados = {}

    def __init__(self, url, zona):
        self.zona = zona
        self.url = url.format(zona)
        self.c = requests.get(self.url).content  # Tipo bytes
        self.soup = BeautifulSoup(self.c, 'html.parser')  # Tipo bs4.BeautifulSoup

    def get_atributes(self):

        for dado in self.soup.select('.ui-search-result__content-wrapper'):
            preco = dado.select_one('.price-tag-fraction')
            metros = dado.select_one('.ui-search-card-attributes__attribute ')

            precos = re.findall(re_precos, str(preco))
            areas = re.findall(re_areas, str(metros))
            quartos = re.findall(re_quartos, dado.text)

            for p in precos:
                Scraper.preco.append(p)

            if len(areas) == 0:
                areas.append(np.nan)
            for a in areas:
                Scraper.area.append(a)

            if len(quartos) > 0:
                n_quartos = quartos[0].replace('quarto', '').strip()
                for q in quartos:
                    Scraper.quartos.append(n_quartos)
            else:
                Scraper.quartos.append(np.nan)

            Scraper.zona.append(self.zona)

            Scraper.dados['zona'] = Scraper.zona
            Scraper.dados['quartos'] = Scraper.quartos
            Scraper.dados['area'] = Scraper.area
            Scraper.dados['preco'] = Scraper.preco

        sleep(3)
        return Scraper.dados

    def create_csv(self):
        df = pd.DataFrame(self.dados)
        for i in [48, 96, 144]:
            if len(df) == i:
                continue
            if len(df) == 192:
                df.to_csv('mercado_livre.csv', index=False)
                break


if __name__ == '__main__':
    for zona in zonas:
        scrap = Scraper(url_ml, zona)
        scrap.get_atributes()
        scrap.create_csv()
