import random
import re
from datetime import date, datetime
import string
from bs4 import BeautifulSoup
import gpt
import scraper
import parse

gpt.setup()
scraper.setup()

p_file = open('products.txt', 'r', encoding='utf-8')
p_lines = p_file.readlines()
existing_products = []
for l in p_lines:
    existing_products.append(l.replace("\n", "").strip())
ctr = 0
new_p = open('products.txt', 'a', encoding='utf-8')
vendors = ['Toyota', 'Volkswagen', 'Ford', 'Chevrolet', 'Honda', 'Nissan', 'BMW', 'Mercedes-Benz', 'Audi', 'Tesla', 'Hyundai', 'Kia', 'Subaru', 'Porsche', 
'Volvo', 'Mazda', 'Honda', 'Jeep', 'Lexus', 'Land Rover', 'Ram', 'Kawasaki', 'Yamaha', 'Harley Davidson']
temp_urls = ['https://www.facebook.com/marketplace/nyc/search?query=', 'https://www.facebook.com/marketplace/columbus/search?query=', 'https://www.facebook.com/marketplace/dc/search?query=']
for i in range(1):
    r_string = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(2, 5)))
    url = random.choice(temp_urls) + random.choice(vendors) + ' ' + r_string
    text = scraper.get_raw_text(url)
    soup = BeautifulSoup(text, 'html.parser')
    for i in parse.get_new_products(text):
        if ctr > 900:
            break
        if i.text not in existing_products and len(i.text) < 30 and len(i.text) > 10 and 'yes' in gpt.request(i.text).lower():
            print(i.text)
            print('------------------------------')
            new_p.write('{}\n'.format(i.text.lower()))
            ctr += 1

p_file = open('products.txt', 'r', encoding='utf-8')
p_lines = p_file.readlines()
products = []
for l in p_lines:
    products.append(l.replace("\n", "").strip())
l = open('locations.txt', encoding='utf-8')
l_lines = l.readlines()
locations = {}
for l in l_lines:
    l_parse = re.search(r'^(.*),(.*)', l)
    locations[l_parse.group(1)] = l_parse.group(2)
f = open('data/' + str(date.today()) + '.txt', 'w', encoding='utf-8')

prices = []
ctr = 0

for product in products:
    ctr += 1
    if prices:
        print(str((ctr / len(l_lines)) * 100)[0:5])
    print(datetime.now())
    print(prices)
    prices = []
    for location in locations.keys():
        url = 'https://www.facebook.com/marketplace/' + locations[location].strip() + '/search?query=' + product.replace(' ', '%20')
    
        text = scraper.get_raw_text(url)
        
        if len(text) < 30:
            raise Exception("PROXY: Proxy is not working.")
        
        prices = parse.get_product_prices(text)
        
        average = 0
        for price in prices:
            price = int(price.replace('$', '').replace(',', ''))
            average += price
        if len(prices) != 0:
            average /= len(prices)
        average = round(average, 2)

        for p in prices:
            price = int(p.replace('$', '').replace(',', ''))
            if price < 0.5 * average or price > 2.0 * average:
                prices.remove(p)

        average = 0
        for price in prices:
            price = int(price.replace('$', '').replace(',', ''))
            average += price
        if len(prices) != 0:
            average /= len(prices)
        average = round(average, 2)

        summary = ("\n{}, {}, {}".format(product, location, average))

        f.write(summary + '\n' + ', '.join(prices) + '\n')
        
    f.write("-------------------------")
f.close()
