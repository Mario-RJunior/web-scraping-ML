import requests
from bs4 import BeautifulSoup
import re
import numpy as np
from time import sleep
import pandas as pd

zonas = ['norte', 'sul', 'leste', 'oeste']
paginas = ['', '_Desde_49', '_Desde_97', '_Desde_145', '_Desde_193', '_Desde_241', '_Desde_289']
url_ml = 'https://imoveis.mercadolivre.com.br/casas/aluguel/sao-paulo/sao-paulo-zona-{}/{}'

re_precos = r'<span class="price-tag-fraction">(.*)<'
re_quartos = r'([1-9]{1,2}) quarto[s]?'
re_areas = r'<li class="ui-search-card-attributes__attribute">(.*) m²'


class Scraper:
    zona = []
    area = []
    quartos = []
    preco = []
    dados = {}

    def __init__(self, url, zona, pagina):

        self.zona = zona
        self.url = url.format(zona, pagina)

    def get_atributes(self):

        c = requests.get(self.url).content
        soup = BeautifulSoup(c, 'html.parser')

        for dado in soup.select('.ui-search-result__content-wrapper'):
            preco = dado.select_one('.price-tag-fraction')
            metros = dado.select_one('.ui-search-card-attributes__attribute ')

            precos = re.findall(re_precos, str(preco))
            areas = re.findall(re_areas, str(metros))
            quartos = re.findall(re_quartos, dado.text)

            for p in precos:
                if isinstance(p, str):
                    p = int(p.replace('.', '').replace(',', '').strip())
                    Scraper.preco.append(p)

            if len(areas) == 0:
                areas.append(np.nan)
            for a in areas:
                if isinstance(a, str):
                    a = int(a.replace('.', '').replace(',', '').strip())
                Scraper.area.append(a)

            if len(quartos) == 0:
                quartos.append(np.nan)
            for q in quartos:
                Scraper.quartos.append(q)

            Scraper.zona.append(self.zona)

            Scraper.dados['zona'] = Scraper.zona
            Scraper.dados['quartos'] = Scraper.quartos
            Scraper.dados['area'] = Scraper.area
            Scraper.dados['preco'] = Scraper.preco

        sleep(2)
        return Scraper.dados

    def create_csv(self):
        df = pd.DataFrame(Scraper.dados)
        for i in range(48, 1344, 48):
            if len(df) == 1344:
                df.to_csv('dados_imoveis.csv', index=False)
                break


if __name__ == '__main__':
    for zona in zonas:
        for pagina in paginas:
            sleep(2)
            scrap = Scraper(url_ml, zona, pagina)
            scrap.get_atributes()
            scrap.create_csv()
