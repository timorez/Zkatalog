import requests
from bs4 import BeautifulSoup as bs


class Citilink:
    def __init__(self, url):
        self.url = url
        self.data = bs((requests.get(self.url)).text, 'html.parser')

    def get_price(self):
        price = self.data.find('span', class_='ProductPrice__price ProductPagePriceSection__default-price__price')
        price = (str(price).split('\n')[1])
        return price.strip()

    def get_name(self):
        name = self.data.find('h1', class_='Heading Heading_level_1 ProductPageTitleSection__text')
        name = (str(name).split('\n'))[-2]
        return name.strip()

