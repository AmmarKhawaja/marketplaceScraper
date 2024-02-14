import random
import re
from datetime import date, datetime
import string
from bs4 import BeautifulSoup
import gpt
import scraper
import extract
import csv

gpt.setup()
scraper.setup()

p_file = open('products.txt', 'r', encoding='utf-8')
p_lines = p_file.readlines()
existing_products = []
for l in p_lines:
    existing_products.append(l.replace("\n", "").strip())
ctr = 0
new_p = open('products.txt', 'a', encoding='utf-8')
vendors = ['Toyota', 'Volkswagen', 'Ford', 'Chevrolet', 'Honda', 'Nissan', 'BMW', 'Mercedes-Benz', 'Audi', 'Tesla', 'Hyundai', 'Kia', 'Subaru', 'Porsche', 'Cadillac', 
'Volvo', 'Mazda', 'Honda', 'Jeep', 'Lexus', 'Land Rover', 'Ram', 'Kawasaki', 'Yamaha', 'Mitsubishi']
temp_urls = ['https://www.facebook.com/marketplace/sanfrancisco/search?query=', 'https://www.facebook.com/marketplace/dallas/search?query=', 'https://www.facebook.com/marketplace/dc/search?query=']
for i in range(0):
    r_string = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(2, 5)))
    url = random.choice(temp_urls) + random.choice(vendors) + ' ' + r_string
    text = scraper.get_raw_text(url)
    
    soup = BeautifulSoup(text, 'html.parser')
    for i in extract.get_new_products(text):
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

csv_file = open('data/' + str(date.today()) + '.csv', 'r+', newline='', encoding='utf-8')
csv_writer_dict = csv.DictWriter(csv_file, fieldnames=['NAME', 'PRICE', 'MILES'])
csv_writer_list = csv.writer(csv_file)
csv_writer_dict.writeheader()

average = 0
ctr = 0

for product in products:
    ctr += 1
    if average:
        print(str((ctr / len(p_lines)) * 100)[0:5])
    print(str(datetime.now())[0:19])
    for location in locations.keys():
        url = 'https://www.facebook.com/marketplace/' + locations[location].strip() + '/search?query=' + product.replace(' ', '%20')
    
        text = scraper.get_raw_text(url)

        if len(text) < 30:
            raise Exception("PROXY: Proxy is not working.")
        
        get_products = extract.get_products_car(text)
        
        average = 0
        for get_product in get_products:
            if get_product['PRICE'] > 0:
                average += get_product['PRICE']
        if len(get_products) != 0:
            average /= len(get_products)
        average = round(average, 2)
        for get_product in get_products:
            if get_product['PRICE'] > 0:
                price = get_product['PRICE']
                if price < 0.25 * average or price > 4.0 * average:
                    get_product['PRICE'] = -2
        average = 0
        for get_product in get_products:
            if get_product['PRICE'] > 0:
                average += get_product['PRICE']
        if len(get_products) != 0:
            average /= len(get_products)
        average = round(average, 2)
        
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row == [get_product['NAME'], get_product['PRICE'], get_product['MILES']]:
                continue
        csv_writer_list.writerows([['-', str(product), str(location), str(average)]])
        csv_writer_dict.writerows(get_products)
        
csv_file.close()