from flask import Flask
from flask import render_template
from bs4 import BeautifulSoup as bs
import requests
import sqlite3


class Citilink:
    def __init__(self, name):
        self.name = name
        con = sqlite3.connect('ZkatalogDB.sqlite')
        self.cur = con.cursor()
        self.url = list(self.cur.execute(f"""SELECT url_Ct FROM goods WHERE name = ?""", (str(name), )))
        self.data = bs((requests.get(self.url[0][0])).text, 'html.parser')
        self.code = requests.get(self.url[0][0])

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
    def __init__(self, name):
        Citilink.__init__(self, name)
        self.url = list(self.cur.execute(f"""SELECT url_AW FROM goods WHERE name = ?""", (str(name), )))
        self.data = bs((requests.get(self.url[0][0])).text, 'html.parser')
        print(self.data)

    def get_price(self):
        price = self.data.find('bdi')
        print(price)
        price = str(price).split()
        print(price)
        res = price[0][5::] + price[1]
        return res

    def get_name(self):
        name = str(self.data.find('h1').text)
        return name


app = Flask(__name__)
name1 = 'phone1'
Ct = Citilink(name1)
AW = AppleWave(name1)


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
                           name_one=name_one, url_one=url_one)


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


@app.route('/about')
def about():
    return render_template('template.html', name_one='12312')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
