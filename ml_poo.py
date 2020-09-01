import requests
from bs4 import BeautifulSoup
import re

zonas = ['norte', 'sul', 'leste', 'oeste']
url_ml = 'https://imoveis.mercadolivre.com.br/casas/aluguel/sao-paulo/sao-paulo-zona-{}'

re_precos = '<span class="price__fraction">(.*)</span>'
re_quartos = r'<li class="ui-search-card-attributes__attribute">(.*) quarto</li>'
re_areas = '> (.*) m² '
re_quarto_area_ausente = "> (.*) quarto"


class Scraper:

    def __init__(self, url, zona):
        self.url = url.format(zona)
        self.c = requests.get(self.url).content  # Tipo bytes
        self.soup = BeautifulSoup(self.c, 'html.parser')  # Tipo bs4.BeautifulSoup
        self.quartos = []
        self.metros = []
        self.dados = {'quartos': [], 'preco': []}

    def get_atributes(self):
        #precos = self.soup.find_all(name='span', attrs={'class': 'price-tag-fraction'})
        #atributos = self.soup.find_all(name='li', attrs={'class': 'ui-search-card-attributes__attribute'})
        cont = 0
        x = []

        for dado in self.soup.select('.ui-search-result__content-wrapper'):
            '''preco = dado.select_one('.price-tag-fraction')
            #metros = dado.select_one('.ui-search-card-attributes__attribute ')
            #x.append(metros)'''
            answers = dado.find_next_siblings("li")
            for answer in answers:
                answer_text = answer.get_text(strip=True)
                #is_selected = "ui-search-card-attributes__attribute" in answer.get()
                print(answer_text)
        #print(x)
        #print(len(x))



        """for preco in precos:
            self.dados['preco'].append(preco.text)
        #print(self.dados)

        for atributo in atributos:
            quarto = re.findall(re_quartos, str(atributo))
            print(atributo.text)"""

            #self.quarto.append(quarto)
            #print(quarto)
        #print(self.quarto)
        #print(len(self.quarto))
        """print(preco)
        print(atributos)
        print(type(preco))
        print(type(atributos))"""
        print('*' * 100)


if __name__ == '__main__':
    for zona in zonas:
        scrap = Scraper(url_ml, zona)
        scrap.get_atributes()
