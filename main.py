import requests
import random
import re
from datetime import date
import string
from bs4 import BeautifulSoup

def get_raw_text(url='test'):
    proxies = ['http://51.15.242.202', 'http://47.74.152.29', 'http://134.209.29.120', 'http://162.223.94.164', 'http://167.71.5.83', 'http://209.97.150.167', 'http://20.111.54.16', 'http://20.210.113.32', 'http://94.100.26.202'] 
    proxy = {'http': random.choice(proxies)} 
    headers_list = [{ 
        'authority': 'httpbin.org', 
        'cache-control': 'max-age=0', 
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"', 
        'sec-ch-ua-mobile': '?0', 
        'upgrade-insecure-requests': '1', 
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
        'sec-fetch-site': 'none', 
        'sec-fetch-mode': 'navigate', 
        'sec-fetch-user': '?1', 
        'sec-fetch-dest': 'document', 
        'accept-language': 'en-US,en;q=0.9', 
    }] 
    headers = random.choice(headers_list) 
    return requests.get(url, headers=headers, proxies=proxy).text

p_file = open('products.txt', 'r')
p_lines = p_file.readlines()
existing_products = []
for l in p_lines:
    existing_products.append(l.replace("\n", "").strip())

new_p = open('products.txt', 'a')
for i in range(0):
    r_string = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(1, 3)))
    url = 'https://www.facebook.com/marketplace/nyc/search?query=' + r_string
    text = get_raw_text(url)
    soup = BeautifulSoup(text, 'html.parser')
    p = soup.find_all("span", class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
    for i in p:
        if i.text not in existing_products:
            new_p.write('{}\n'.format(i.text))

p_file = open('products.txt', 'r')
p_lines = p_file.readlines()
products = []
for l in p_lines:
    products.append(l.replace("\n", "").strip())
l = open('locations.txt')
l_lines = l.readlines()
locations = {}
for l in l_lines:
    l_parse = re.search(r'^(.*),(.*)', l)
    locations[l_parse.group(1)] = l_parse.group(2)
f = open('data' + str(date.today()) + '.txt', 'w')

for product in products:
    prices = []
    print("-")
    for location in locations.keys():
        url = 'https://www.facebook.com/marketplace/' + locations[location].strip() + '/search?query=' + product.replace(' ', '%20')
    
        text = get_raw_text(url)
        print(text)
        prices = re.findall(r'\$[\d]+,?[\d]+', text)[0:15]
        
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
