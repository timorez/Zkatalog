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
        if price is not None:
            price = (str(price).split('\n')[1])
        else:
            price = 'No Data'
        return price.strip()

    def get_name(self):
        name = self.data.find('h1', class_='Heading Heading_level_1 ProductPageTitleSection__text')
        if name is not None:
            name = (str(name).split('\n'))[-2]
        else:
            name = 'Сайт магазина не отвечает. Попробуйте позже'
        return name.strip()

    def get_img(self):
        img = str(self.data.find('img'))
        if not img:
            img = str(self.data.find('img')['src'])
        else:
            img = ''
        return img


class AppleWave(Citilink):
    def __init__(self, name):
        Citilink.__init__(self, name)
        self.url = list(self.cur.execute(f"""SELECT url_AW FROM goods WHERE name = ?""", (str(name), )))
        self.data = bs((requests.get(self.url[0][0])).text, 'html.parser')

    def get_price(self):
        price = self.data.find('bdi')
        price = str(price).split()
        res = price[0][5::] + price[1]
        return res

    def get_name(self):
        name = str(self.data.find('h1').text)
        return name


app = Flask(__name__)
Ctl1 = Citilink('lap1')
AWl1 = AppleWave('lap1')
Ctl2 = Citilink('lap2')
AWl2 = AppleWave('lap2')
Ctl3 = Citilink('lap3')
AWl3 = AppleWave('lap3')

Ctp1 = Citilink('phone1')
AWp1 = AppleWave('phone1')
Ctp2 = Citilink('phone2')
AWp2 = AppleWave('phone2')
Ctp3 = Citilink('phone3')
AWp3 = AppleWave('phone3')

Ctt1 = Citilink('TV1')
AWt1 = AppleWave('TV1')
Ctt2 = Citilink('TV2')
AWt2 = AppleWave('TV2')
Ctt3 = Citilink('TV3')
AWt3 = AppleWave('TV3')

flag = 0


@app.route('/')
def index():
    global flag
    flag = 0
    return render_template('index.html')


@app.route('/laptops')
def laptops():
    global flag
    flag = 1
    name_one = Ctl1.get_name()
    url_one = str(Ctl1.get_img())
    name_two = Ctl2.get_name()
    url_two = str(Ctl2.get_img())
    name_three = Ctl3.get_name()
    url_three = str(Ctl3.get_img())
    return render_template('template.html',
                           name_one=name_one,
                           url_one=url_one,
                           name_two=name_two,
                           url_two=url_two,
                           name_three=name_three,
                           url_three=url_three
                           )


@app.route('/phones')
def phones():
    global flag
    flag = 2
    name_one = AWp1.get_name()
    url_one = str(Ctp1.get_img())
    name_two = AWp2.get_name()
    url_two = str(Ctp2.get_img())
    name_three = AWp3.get_name()
    url_three = str(Ctp3.get_img())
    return render_template('template.html',
                           name_one=name_one,
                           url_one=url_one,
                           name_two=name_two,
                           url_two=url_two,
                           name_three=name_three,
                           url_three=url_three
                           )


@app.route('/TVs')
def TVs():
    global flag
    flag = 3
    name_one = Ctt1.get_name()
    url_one = str(Ctt1.get_img())
    name_two = Ctt2.get_name()
    url_two = str(Ctt2.get_img())
    name_three = Ctt3.get_name()
    url_three = str(Ctt3.get_img())
    return render_template('template.html',
                           name_one=name_one,
                           url_one=url_one,
                           name_two=name_two,
                           url_two=url_two,
                           name_three=name_three,
                           url_three=url_three
                           )


@app.route('/good_one')
def good1():
    if flag == 1:
        name = Ctl1.get_name()
        shop_one = 'Citilink ' + Ctl1.get_price() + 'р'
        shop_two = 'AppleWave ' + AWl1.get_price() + 'р'
        shop_three = ''
    elif flag == 2:
        name = Ctl1.get_name()
        shop_one = 'Citilink ' + Ctp1.get_price() + 'р'
        shop_two = 'AppleWave ' + AWp1.get_price() + 'р'
        shop_three = ''
    else:
        name = Ctt1.get_name()
        shop_one = 'Citilink ' + Ctt1.get_price() + 'р'
        shop_two = 'AppleWave ' + AWt1.get_price() + 'р'
        shop_three = ''
    return render_template('good.html',
                           name=name,
                           shop_one=shop_one,
                           shop_two=shop_two,
                           shop_three=shop_three)


@app.route('/good_two')
def good2():
    if flag == 1:
        name = Ctl2.get_name()
        shop_one = 'Citilink ' + Ctl2.get_price() + 'р'
        shop_two = 'AppleWave ' + AWl2.get_price() + 'р'
        shop_three = ''
    elif flag == 2:
        name = Ctl2.get_name()
        shop_one = 'Citilink ' + Ctp2.get_price() + 'р'
        shop_two = 'AppleWave ' + AWp2.get_price() + 'р'
        shop_three = ''
    else:
        name = Ctt2.get_name()
        shop_one = 'Citilink ' + Ctt2.get_price() + 'р'
        shop_two = 'AppleWave ' + AWt2.get_price() + 'р'
        shop_three = ''
    return render_template('good.html',
                           name=name,
                           shop_one=shop_one,
                           shop_two=shop_two,
                           shop_three=shop_three)


@app.route('/good_three')
def good3():
    if flag == 1:
        name = Ctl3.get_name()
        shop_one = 'Citilink ' + Ctl3.get_price() + 'р'
        shop_two = 'AppleWave ' + AWl3.get_price() + 'р'
        shop_three = ''
    elif flag == 2:
        name = Ctl3.get_name()
        shop_one = 'Citilink ' + Ctp3.get_price() + 'р'
        shop_two = 'AppleWave ' + AWp3.get_price() + 'р'
        shop_three = ''
    else:
        name = Ctt3.get_name()
        shop_one = 'Citilink ' + Ctt3.get_price() + 'р'
        shop_two = 'AppleWave ' + AWt3.get_price() + 'р'
        shop_three = ''
    return render_template('good.html',
                           name=name,
                           shop_one=shop_one,
                           shop_two=shop_two,
                           shop_three=shop_three)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
