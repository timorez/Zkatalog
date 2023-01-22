from flask import Flask
from flask import render_template
from bs4 import BeautifulSoup as bs
import requests


class Citilink:
    def __init__(self, url):
        self.url = url
        self.data = bs((requests.get(self.url)).text, 'html.parser')
        self.code = requests.get(url)

    def get_price(self):
        price = self.data.find('span', class_='ProductPrice__price ProductPagePriceSection__default-price__price')
        price = (str(price).split('\n')[1])
        return price.strip()

    def get_name(self):
        name = self.data.find('h1', class_='Heading Heading_level_1 ProductPageTitleSection__text')
        name = (str(name).split('\n'))[-2]
        return name.strip()


app = Flask(__name__)
url = 'https://www.citilink.ru/product/noutbuk-huawei-matebook-d-i3-1115g4-8gb-ssd256gb-15-6-ips-fhd-w11-grey-1774325/'
Ct = Citilink(url)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/laptops')
def laptops():
    return render_template('template.html', price_one=(Ct.get_price() + 'р'),
                           name_one=Ct.get_name())


@app.route('/phones')
def phones():
    return render_template('template.html', name_one='12312')


@app.route('/TVs')
def TVs():
    return render_template('template.html', name_one='12312')


@app.route('/acs')
def acs():
    return render_template('template.html', name_one='12312')


@app.route('/about')
def about():
    return render_template('template.html', name_one='12312')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
