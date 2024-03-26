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

scraper.setup()

PYTHONANYWHERE = False
file_prefix = ['./', './'][PYTHONANYWHERE]

def collect_data(make=None,model=None,year_min='0',year_max='99999',color=None,intcolor=None,miles_min='0',miles_max='99999',price_min='0',price_max='99999',slocation='Washington, DC'):
    locations = {}
    l = open(file_prefix + 'locations.txt', encoding='utf-8')
    l_lines = l.readlines()
    for l in range(len(l_lines)):
        l_parse = re.search(r'^(.*),(.*)', l_lines[l])
        locations[l_parse.group(1)] = l_parse.group(2).split(' ')

    location = locations[slocation]

    h = 'https:\/\/www.'

    sources = ['FACEBOOK', 'CARS.COM', 'AUTOTRADER', 'CARFAX',]
    sources_url = [h+'facebook.com', h+'cars.com', h+'autotrader.com', h+'carfax.com',]

    file_path = file_prefix + 'data/' + 'apitest' + '.csv'
    newfile = False
    if not os.path.isfile(file_path):
        print("FILE: New csv created.")
    csv_file = open(file_path, 'w', newline='', encoding='utf-8').close()
    csv_file = open(file_path, 'r+', newline='', encoding='utf-8')
    csv_writer_dict = csv.DictWriter(csv_file, fieldnames=['NAME', 'MAKE', 'MODEL', 'YEAR', 'TYPE', 'COLOR', 'INTCOLOR', 'MILES', 'PRICE', 'SOURCE'])
    csv_writer_list = csv.writer(csv_file)
    csv_writer_dict.writeheader()

    for i in range(len(sources)):
        # https://ip.oxylabs.io/location
        indirect_sources = ['CARFAX', 'CARS.COM']
        if sources[i] in indirect_sources:
            base_url = 'https://www.google.com/search?q=' + sources[i].lower() + '+' + year_min.lower() + '+' + make.lower() + '+' + model.lower() + '+' + slocation + '+for sale'
            text = scraper.get_raw_text(base_url)
            regex = r'href="(' + sources_url[i] + r'.*?)"'

            base_url = re.findall(regex, text)[:2]
        else:
            if sources[i] == 'FACEBOOK':
                base_url = ['https://www.facebook.com/marketplace/' + location[0].strip() + '/search/?query=' + year_min.lower() + '%20' + make.lower() + '%20' + model.lower() + '&exact=true']
            elif sources[i] == 'AUTOTRADER':
                base_url = ['https://www.autotrader.com/cars-for-sale/all-cars/' + year_min.lower() + '/' + make.lower() + '/' + model.lower() + '/?newSearch=true&zip=' + location[1].strip()]

        for url in base_url:
            print(url)
            for y in range(3):
                text = scraper.get_raw_text(url)
                if sources[i] == 'CARFAX':
                    with open('test.txt', 'w', encoding='utf-8') as f:
                        f.write(text)
                get_products = extract.get_products_car(text, sources[i], 
                                                        des_make=make, des_model=model, 
                                                        min_price=int(price_min), max_price=int(price_max), 
                                                        min_miles=int(miles_min), max_miles=int(miles_max), 
                                                        des_color=color, des_intcolor=intcolor, 
                                                        min_year=int(year_min), max_year=int(year_max)
                                                        )
                if get_products != []:
                    print('suc')
                    break
                else:
                    print('err')
            
            csv_writer_dict.writerows(get_products)
            csv_file.flush()
            csv_reader = csv.reader((line.replace('\x00', '') for line in csv_file))
            for row in csv_reader:
                for get_product in get_products:
                    if row == [get_product['NAME'], get_product['MAKE'], get_product['MODEL'], get_product['YEAR'], get_product['TYPE'], get_product['COLOR'], get_product['INTCOLOR'], get_product['MILES'], get_product['PRICE'], get_product['SOURCE']]:
                        get_products.remove(get_product)
    return file_path

#collect_data(make='Toyota', model='Camry', slocation='Washington, DC')