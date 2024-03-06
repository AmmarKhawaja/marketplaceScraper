import random
import re
from datetime import date, datetime
import time
import string
from bs4 import BeautifulSoup
import gpt
import scraper
import extract
import csv
import os
import sys
import statistics
from functools import reduce

print('RUNNING')

PYTHONANYWHERE = False

#TODO:
#   DONE Record car years
#   DONE Create version for PythonAnywhere (run one location per day)
#   DONE Switch from invalid scrape schema
#   DONE Plot data
#   DONE ISSUE: Data is not clean (averages)
#   ISSUE: Need new csv divider, old one confusing city name, state name
#   Add more datasource: cars.com, carfax.com, carmax.com, carvana.com

csv.field_size_limit(sys.maxsize)
# Open the input CSV file

file_prefix = ['./', './'][PYTHONANYWHERE]

while PYTHONANYWHERE:
    with open(file_prefix + 'track.txt', 'r', encoding='utf-8') as t:
        if t.readline() == str(date.today()):
            print('sleep3')
            time.sleep(3 * 7 * 24 * 60 * 60)
    if date.today().day != 24:
        print('sleep1')
        time.sleep(60 * 60)
    else:
        break

gpt.setup()
scraper.setup()

p_file = open(file_prefix + 'products.txt', 'r', encoding='utf-8')
p_lines = p_file.readlines()
existing_products = []
for l in p_lines:
    existing_products.append(l.replace("\n", "").strip())
ctr = 0
new_p = open(file_prefix + 'products.txt', 'a', encoding='utf-8')
vendors = ['Toyota', 'Ford', 'Chevrolet', 'Honda', 'Nissan', 'BMW', 'Audi', 'Hyundai', 'Kia', 'Subaru', 'Mazda', 'Jeep', 'Rivian', 'Lucid']
temp_urls = ['https://www.facebook.com/marketplace/baltimore/search?query=', 'https://www.facebook.com/marketplace/boston/search?query=']
for i in range(0):
    r_string = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(2, 5)))
    url = random.choice(temp_urls) + 'smartcar' + r_string
    text = scraper.get_raw_text(url)
    soup = BeautifulSoup(text, 'html.parser')
    for i in [d.get('NAME') for d in extract.get_products_car(text, type='FACEBOOK')]:
        if ctr > 10:
            break
        if i not in existing_products and len(i) < 30 and len(i) > 10 and 'yes' in gpt.request(i).lower():
            print(i)
            print('------------------------------')
            new_p.write('{}\n'.format(i.lower()))
            ctr += 1
            time.sleep(0.1)
            new_p.flush()

p_file = open(file_prefix + 'products.txt', 'r', encoding='utf-8')
p_lines = p_file.readlines()
products = []
for l in p_lines:
    products.append(l.replace("\n", "").strip())

l = open(file_prefix + 'locations.txt', encoding='utf-8')
l_lines = l.readlines()
locations = {}
for l in range(len(l_lines)):
    l_parse = re.search(r'^(.*),(.*)', l_lines[l])
    locations[l_parse.group(1)] = l_parse.group(2).split(' ')
    
file_path = file_prefix + 'data/' + str(date.today()) + '.csv'
newfile = False
if not os.path.isfile(file_path):
    f = open(file_path, 'w', newline='', encoding='utf-8')
    f.close()
    newfile = True
csv_file = open(file_path, 'r+', newline='', encoding='utf-8')
csv_writer_dict = csv.DictWriter(csv_file, fieldnames=['NAME', 'MAKE', 'MODEL', 'YEAR', 'TYPE', 'COLOR', 'INTCOLOR', 'MILES', 'PRICE', 'SOURCE'])
csv_writer_list = csv.writer(csv_file)
if newfile:
    csv_writer_dict.writeheader()
    print("FILE: New file created.")

average = 1
ctr = 0
err_ctr = 0
p_err_ctr = 0

for product in products:
    ctr += 1
    if average:
        print(str((ctr / len(p_lines)) * 100)[0:5] + '%', flush=True)
    print(str(datetime.now())[0:19], flush=True)
    for location in locations.keys():
        
        url = 'https://www.autotrader.com/cars-for-sale/all-cars/toyota/camry/clarksville-md??firstRecord=0&zip=21044'

        text = scraper.get_raw_text(url, True)
        print(text)
        print(extract.get_products_car(text, 'AUTOTRADER'))
        with open('re.txt', 'w') as f:
            f.write(text)
        exit()

        url = 'https://www.facebook.com/marketplace/' + locations[location][0].strip() + '/search?query=' + product.replace(' ', '%20')
        
    
        text = scraper.get_raw_text(url)
        
        if len(text) < 30:
            p_err_ctr += 1
            if p_err_ctr > 15:
                raise Exception("PROXY: Proxy is not working.")
        else:
            p_err_ctr = 0

        get_products = extract.get_products_car(text, type='FACEBOOK')
        print(get_products)
        
        if not get_products:
            err_ctr +=1
            continue
        else:
            err_ctr = 0

        if err_ctr > 150:
            raise Exception("EXTRACT: Extract thwarted.")
        elif err_ctr > 75:
            print("-BACKUP-")
            get_products = extract.get_products_car_schema1(text)
        else:
            get_products = extract.get_products_car(text, type='FACEBOOK')

        median = statistics.median([d['PRICE'] for d in get_products])
        get_products = [d for d in get_products if d['PRICE'] > 0.25 * median and d['PRICE'] < 3.0 * median]
        average = round(sum([d['PRICE'] for d in get_products]), 2)
        
        csv_reader = csv.reader((line.replace('\x00', '') for line in csv_file))
        for row in csv_reader:
            for get_product in get_products:
                if row == [get_product['NAME'], get_product['MAKE'], get_product['MODEL'], get_product['YEAR'], get_product['TYPE'], get_product['COLOR'], get_product['INTCOLOR'], get_product['MILES'], get_product['PRICE'], get_product['SOURCE']:
                    get_products.remove(get_product)
        csv_writer_list.writerows([['-', str(product), str(location), str(average), '-', '-', '-', '-', '-']])
        csv_writer_dict.writerows(get_products)
        csv_file.flush()
        
csv_file.close()

# input_csv =get_product['./data/2024-02-23.csv'
# output_csv = './data/2024-02-23 cleaned.csv'

# with open(input_csv, 'r', newline='', encoding='utf-8') as infile:
#     reader = csv.reader(infile)

#     # Open the output CSV file
#     with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
#         writer = csv.writer(outfile)

#         # Iterate over rows in the input CSV file
#         for row in reader:
#             # Remove null characters from each field in the row
#             cleaned_row = [field.replace('\x00', '') for field in row]

#             # Write the cleaned row to the output CSV file
#             writer.writerow(cleaned_row)

if PYTHONANYWHERE:
    with open(file_prefix + 'track.txt', 'w', encoding='utf-8') as t:
        t.write(str(date.today()))