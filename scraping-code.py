import requests
from bs4 import BeautifulSoup
import re
import numpy as np
from time import sleep

zonas = ['norte', 'sul', 'leste', 'oeste']
url_ml = 'https://imoveis.mercadolivre.com.br/casas/aluguel/sao-paulo/sao-paulo-zona-{}'

re_precos = r'<span class="price-tag-fraction">(.*)<'
re_quartos = r'[1-9]{1,2} quarto'
re_areas = r'<li class="ui-search-card-attributes__attribute">(.*) m²'


class Scraper:

    def __init__(self, url, zona):
        self.zona = zona
        self.url = url.format(zona)
        self.c = requests.get(self.url).content  # Tipo bytes
        self.soup = BeautifulSoup(self.c, 'html.parser')  # Tipo bs4.BeautifulSoup
        self.quartos = []
        self.metros = []
        self.dados = {'zona': [],
                      'area': [],
                      'quartos': [],
                      'preco': []}

    def get_atributes(self):

        for dado in self.soup.select('.ui-search-result__content-wrapper'):
            preco = dado.select_one('.price-tag-fraction')
            metros = dado.select_one('.ui-search-card-attributes__attribute ')

            precos = re.findall(re_precos, str(preco))
            areas = re.findall(re_areas, str(metros))
            quartos = re.findall(re_quartos, dado.text)

            for p in precos:
                self.dados['preco'].append(p)

            if len(areas) == 0:
                areas.append(np.nan)
            for a in areas:
                self.dados['area'].append(a)

            temp = []  # Lista temporária
            if len(quartos) > 0:
                n_quartos = quartos[0].replace('quarto', '').strip()
                for q in quartos:
                    temp.append(n_quartos)
            else:
                temp.append(np.nan)

            for q in temp:
                self.dados['quartos'].append(q)

            self.dados['zona'].append(self.zona)
        sleep(2)

        print(self.dados)
        print(len(self.dados['zona']), len(self.dados['area']), len(self.dados['quartos']), len(self.dados['preco']))
        print('=' * 100)


if __name__ == '__main__':
    for zona in zonas:
        scrap = Scraper(url_ml, zona)
        scrap.get_atributes()
