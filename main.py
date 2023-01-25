from flask import Flask
from flask import render_template
from bs4 import BeautifulSoup as bs
from time import sleep
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
            name = 'No Data'
        return name.strip()

    def get_img(self):
        img = (self.data.find('img'))
        if img is not None:
            img = str(self.data.find('img')['src'])
        else:
            img = 'static/placeholder.png'
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


class tm24(Citilink):
    def __init__(self, name):
        Citilink.__init__(self, name)
        self.url = list(self.cur.execute(f"""SELECT url_TM FROM goods WHERE name = ?""", (str(name), )))
        self.data = bs((requests.get(self.url[0][0])).text, 'html.parser')

    def get_price(self):
        price = self.data.find('div', class_='price-values').text
        return price.strip()

    def get_name(self):
        name = str(self.data.find('h1', itemprop='name').text)
        return name


app = Flask(__name__)
sleep(120)
Ctl1 = Citilink('lap1')
sleep(30)
Tml1 = AppleWave('lap1')
Ctl2 = Citilink('lap2')
sleep(30)
Tml2 = AppleWave('lap2')
Ctl3 = Citilink('lap3')
sleep(30)
Tml3 = AppleWave('lap3')
sleep(120)

Ctp1 = Citilink('phone1')
sleep(30)
AWp1 = AppleWave('phone1')
Tmp1 = tm24('phone1')
Ctp2 = Citilink('phone2')
sleep(30)
AWp2 = AppleWave('phone2')
Tmp2 = tm24('phone1')
Ctp3 = Citilink('phone3')
sleep(30)
AWp3 = AppleWave('phone3')
Tmp3 = tm24('phone1')
sleep(120)

Ctt1 = Citilink('TV1')
sleep(30)
Tmt1 = tm24('TV1')
Ctt2 = Citilink('TV2')
sleep(30)
Tmt2 = tm24('TV2')
Ctt3 = Citilink('TV3')
sleep(30)
Tmt3 = tm24('TV3')

flag = 0


@app.route('/')
def index():
    global flag
    flag = 0
    return render_template('index.html')


@app.route('/info')
def info():
    global flag
    flag = 0
    return render_template('info.html')


@app.route('/laptops')
def laptops():
    global flag
    flag = 1
    name_one = Tml1.get_name()
    url_one = str(Ctl1.get_img())
    name_two = Tml2.get_name()
    url_two = str(Ctl2.get_img())
    name_three = Tml3.get_name()
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
    name_one = Tmt1.get_name()
    url_one = str(Ctt1.get_img())
    name_two = Tmt2.get_name()
    url_two = str(Ctt2.get_img())
    name_three = Tmt2.get_name()
    url_three = str(Ctt2.get_img())
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
        name = Tml1.get_name()
        image = Ctl1.get_img()
        shop_one = 'citilink.ru ' + Ctl1.get_price() + ' Р'
        shop_two = 'telemarket24.ru ' + Tml1.get_price() + ' Р'
        shop_three = ''
    elif flag == 2:
        name = AWp1.get_name()
        image = Ctp1.get_img()
        shop_one = 'citilink.ru ' + Ctp1.get_price() + ' Р'
        shop_two = 'applewave.ru ' + AWp1.get_price() + ' Р'
        shop_three = 'telemarket24.ru ' + str(Tmp1.get_price())
    else:
        name = Tmt1.get_name()
        image = Ctt1.get_img()
        shop_one = 'citilink.ru ' + Ctt1.get_price() + ' Р'
        shop_two = 'telemarket24.ru ' + Tmt1.get_price() + ' Р'
        shop_three = ''
    return render_template('good.html',
                           name=name,
                           image=image,
                           shop_one=shop_one,
                           shop_two=shop_two,
                           shop_three=shop_three)


@app.route('/good_two')
def good2():
    if flag == 1:
        name = Tml2.get_name()
        image = Ctl2.get_img()
        shop_one = 'citilink.ru ' + Ctl2.get_price() + ' Р'
        shop_two = 'telemarket24.ru ' + Tml2.get_price() + ' Р'
        shop_three = ''
    elif flag == 2:
        name = AWp2.get_name()
        image = Ctp2.get_img()
        shop_one = 'citilink.ru ' + Ctp2.get_price() + ' Р'
        shop_two = 'applewave.ru ' + AWp2.get_price() + ' Р'
        shop_three = 'telemarket24.ru ' + str(Tmp2.get_price())
    else:
        name = Tmt2.get_name()
        image = Ctt2.get_img()
        shop_one = 'citilink.ru ' + Ctt2.get_price() + ' Р'
        shop_two = 'telemarket24.ru ' + Tmt2.get_price() + ' Р'
        shop_three = ''
    return render_template('good.html',
                           image=image,
                           name=name,
                           shop_one=shop_one,
                           shop_two=shop_two,
                           shop_three=shop_three)


@app.route('/good_three')
def good3():
    if flag == 1:
        name = Tml3.get_name()
        image = Ctl3.get_img()
        shop_one = 'citilink.ru ' + Ctl3.get_price() + ' Р'
        shop_two = 'telemarket24.ru ' + Tml3.get_price() + ' Р'
        shop_three = ''
    elif flag == 2:
        name = AWp3.get_name()
        image = Ctp3.get_img()
        shop_one = 'citilink.ru ' + Ctp3.get_price() + ' Р'
        shop_two = 'applewave.ru ' + AWp3.get_price() + ' Р'
        shop_three = 'telemarket24.ru ' + str(Tmp3.get_price())
    else:
        name = Tmt3.get_name()
        image = Ctt3.get_img()
        shop_one = 'citilink.ru ' + Ctt3.get_price() + ' Р'
        shop_two = 'telemarket24.ru ' + Tmt3.get_price() + ' Р'
        shop_three = ''
    return render_template('good.html',
                           name=name,
                           image=image,
                           shop_one=shop_one,
                           shop_two=shop_two,
                           shop_three=shop_three)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
