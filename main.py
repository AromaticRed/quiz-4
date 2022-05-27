import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import random


f = open('phones.csv', 'w', newline='\n', encoding="utf-8")
f_obj = csv.writer(f)
f_obj.writerow(['სახელწოდება','მეხსიერება', 'ფასდაკლება', 'ამჟამინდელი ფასი', 'ძველი ფასი', 'ფასებს შორის სხვაობა'])
for i in range(1, 6):
    url = f'https://alta.ge/smartphones-page-{str(i)}.html'
    res = requests.get(url).text
    soup_all = BeautifulSoup(res, 'html.parser')
    holder = soup_all.find('div', class_='grid-list')
    all_phones = holder.find_all('div', class_='ty-column3')
    for phone in all_phones:
        try:
            info = phone.div.form
            name_all = info.find('div', class_='ty-grid-list__item-name')
            name = name_all.a.text
            price_all = info.find('span', class_='ty-price')
            price = price_all.span.text
            storage = re.search('.\d\dGB', name)
            storage = storage.group(0)
            storage = storage.replace('/','')
            storage = storage.strip()
            pic = info.find('div', class_='ty-grid-list__image')
            try:
                sale_icon_on_pic = pic.span.img
                sale_icon_on_pic = True
                old_price_all = info.find('span', class_='ty-strike')
                old_price = old_price_all.span.text
            except:
                sale_icon_on_pic = False
                old_price = price

            difference = int(old_price) - int(price)
            f_obj.writerow([name,storage,sale_icon_on_pic, price, old_price, difference ])
        except:
            pass

    time.sleep(random.randint(15, 20))

f.close()



