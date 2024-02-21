from bs4 import BeautifulSoup
import re

def get_new_products(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6')

def get_product_prices(text):
    return re.findall(r'\$[\d]+,?[\d]+', text)[0:15]

def get_products_car_schema1(text):
    soup = BeautifulSoup(text, 'html.parser')
    wrappers = soup.find_all('div', class_='x9f619 x78zum5 xdt5ytf x1qughib x1rdy4ex xz9dl7a xsag5q8 xh8yej3 xp0eagm x1nrcals')
    products = []
    for wrapper in wrappers:
        sub_soup = BeautifulSoup(str(wrapper), 'html.parser')
        if sub_soup.find('span', class_='x78zum5 x1q0g3np x1iorvi4 x4uap5 xjkvuk6 xkhd6sd'):
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

def get_products_car_schema2(text):
    wrappers = re.findall(r'"node":(.*?)"MarketplaceSearchFeedStoriesEdge"}', text)
    products = []
    for wrapper in wrappers:
        name = re.findall(r'"custom_title":"(.*?)"', wrapper)
        if name and len(name[0]) < 40:
            name = name[0]
            year = re.findall(r'(\d{4})', name)
            if not year:
                year = -1
            else:
                year = int(year[0])
            price = re.findall(r'"amount":"(.*?)"', wrapper)
            if not price:
                price = -1
            else:
                price = int(float(price[0]))
            miles = re.findall(r'"subtitle":"(.*?) miles"', wrapper)
            if not miles:
                miles = -1
            else:
                miles = int(miles[0].replace('.', '').replace('K', '00').replace('M', '000000'))
            products.append({"NAME": name, "YEAR": year, "PRICE": price, "MILES": miles})
            print(products)
    return products
            

        
