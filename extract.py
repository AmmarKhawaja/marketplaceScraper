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
            name = sub_soup.find('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6').text.replace(',', '')
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

def get_products_car_schema2_FACEBOOK(text, min_year=None, max_year=None, min_price=None, max_price=None, min_miles=None, max_miles=None):
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
                if '.' in miles[0]:
                    miles = int(miles[0].replace('.', '').replace('K', '00').replace('M', '00000'))
                else:
                    miles = int(miles[0].replace('K', '000').replace('M', '000000'))
            if (min_year != None and year < min_year) or (max_year != None and year > max_year) or (min_price != None and price > min_price) or (max_price != None and price > max_price) or (min_miles != None and miles < min_miles) or (max_miles != None and miles > max_miles):
                continue
            products.append({"NAME": name, "YEAR": year, "PRICE": price, "MILES": miles})
    return products
            
# def get_products_car_schema1_AUTOTRADER(text):
#     wrappers = re.findall(r'"vehicleIdentificationNumber":(.*?),"fuelEfficiency"', text)
#     products = []
#     for wrapper in wrappers:
#         name = re.findall()

def validate(e, type):
    if not e:
        if type == 'int':
            return -1
        elif type == 'str':
            return '-1'
    else:
        if type == 'int':
            return int(float(e[0]))
        elif type == 'str':
            return str(e[0])

def get_products_car(text, source, min_year=None, max_year=None, min_price=None, max_price=None, min_miles=None, max_miles=None):
    re_codes = []
    # wrapper, name, make, model, year, type, color, intcolor, miles, price
    if source == 'FACEBOOK':
        re_codes = [r'"node":(.*?)"MarketplaceSearchFeedStoriesEdge"}', r'"custom_title":"(.*?)"', r'^$', r'^$', 
                    r'(\d{4})', r'^$', r'^$', r'^$', r'"subtitle":"(.*?) miles"', r'"amount":"(.*?)"',]
    elif source == "AUTOTRADER":
        re_codes = [r'"vehicleIdentificationNumber":(.*?),"fuelEfficiency"', r'"name":"(.*?)","mpn"', 
                    r'{"code".*?"name":"(.*?)"}},"model"', r'"model":{"code".*?"name":"(.*?)"},"manufacturer"', 
                    r'(\d{4})', r'"vehicleEngine":"(.*?)"', r'"color":"(.*?)"', r'"vehicleInteriorColor":"(.*?)"', 
                    r'"value":"(.*?)"', r'"price":(.*?),']

    wrappers = re.findall(re_codes[0], text)
    products = []
    for wrapper in wrappers:
        name = re.findall(re_codes[1], wrapper)
        if name and len(name[0]) < 40:
            name = name[0]
            make = validate(re.findall(re_codes[2], wrapper), 'str')
            model = validate(re.findall(re_codes[3], wrapper), 'str')
            year = validate(re.findall(re_codes[4], name), 'int')
            type = validate(re.findall(re_codes[5], wrapper), 'str')
            color = validate(re.findall(re_codes[6], wrapper), 'str')
            intcolor = validate(re.findall(re_codes[7], wrapper), 'str')
            miles = validate(re.findall(re_codes[8], wrapper), 'str')
            if '.' in miles:
                miles = int(miles.replace('.', '').replace('K', '00').replace('M', '00000').replace(',', ''))
            else:
                miles = int(miles.replace('K', '000').replace('M', '000000').replace(',', ''))
            price = validate(re.findall(re_codes[9], wrapper), 'int')
            if (min_year != None and year < min_year) or (max_year != None and year > max_year) or (min_price != None and price > min_price) or (max_price != None and price > max_price) or (min_miles != None and miles < min_miles) or (max_miles != None and miles > max_miles):
                continue
            products.append({"NAME": name, "MAKE": make, "MODEL": model, "YEAR": year, "TYPE": type, "COLOR": color, "INTCOLOR": intcolor, "MILES": miles, "PRICE": price, 'SOURCE': source})
    return products