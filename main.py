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

    def get_img(self):
        img = str(self.data.find('img')['src'])
        return img


class AppleWave(Citilink):
    def get_price(self):
        price = self.data.find('bdi')
        price = str(price).split()
        res = price[0][5::] + price[1]
        return res

    def get_name(self):
        name = str(self.data.find('h1').text)
        return name


app = Flask(__name__)
url = 'https://www.citilink.ru/product/noutbuk-huawei-matebook-d-i3-1115g4-8gb-ssd256gb-15-6-ips-fhd-w11-grey-1774325/'
url1 = 'https://applewave.ru/product/apple-iphone-11-128gb-chyornyj/?utm-sourse=m15ekat'
Ct = Citilink(url)
AW = AppleWave(url1)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/laptops')
def laptops():
    price_one = Ct.get_price() + 'р'
    name_one = Ct.get_name()
    url_one = str(Ct.get_img())
    print(url_one)
    return render_template('template.html', price_one=price_one,
                           name_one=name_one, url_one='')


@app.route('/phones')
def phones():
    price_one = AW.get_price() + 'р'
    name_one = AW.get_name()
    url_one = str(AW.get_img())
    print(url_one)
    return render_template('template.html', price_one=price_one,
                           name_one=name_one,
                           url_one=url_one)


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
