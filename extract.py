from bs4 import BeautifulSoup
import re

def get_new_products(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6')

def get_product_prices(text):
    return re.findall(r'\$[\d]+,?[\d]+', text)[0:15]

def get_products_car(text):
    soup = BeautifulSoup(text, 'html.parser')
    wrappers = soup.find_all('div', class_='x9f619 x78zum5 xdt5ytf x1qughib x1rdy4ex xz9dl7a xsag5q8 xh8yej3 xp0eagm x1nrcals')
    products = []
    for wrapper in wrappers:
        sub_soup = BeautifulSoup(str(wrapper), 'html.parser')
        if sub_soup.find('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6'):
            name = sub_soup.find('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6').text
        else:
            name = 'n/a'
        if len(name) < 40:
            if len(sub_soup.find('span', class_='x78zum5').text.split('$')) == 2:
                price = int(''.join(sub_soup.find('span', class_='x78zum5').text.split('$')[1]).replace(',', ''))
            elif len(sub_soup.find('span', class_='x78zum5').text.split('$')) == 3:
                price = int(''.join(sub_soup.find('span', class_='x78zum5').text.split('$')[1]).replace(',', ''))
            else:
                price = -1
            if re.findall(r'\>(.{0,3}) miles', str(wrapper)) and 'M' not in re.findall(r'\>(.{0,3}) miles', str(wrapper))[0]:
                if '.' in re.findall(r'\>(.{0,3}) miles', str(wrapper))[0]:
                    miles = int(re.findall(r'\>(.{0,3}) miles', str(wrapper))[0].replace('.', '').replace('K', '00'))
                else:
                    miles = int(re.findall(r'\>(.{0,3}) miles', str(wrapper))[0].replace('K', '000'))
            else:
                miles = -1
            products.append({"NAME": name, "PRICE": price, "MILES": miles})
    return products