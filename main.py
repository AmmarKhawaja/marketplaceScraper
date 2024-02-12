import requests
import random
import re
from datetime import date, datetime
import string
from bs4 import BeautifulSoup
from secret import USER, PASS
from urllib3.exceptions import InsecureRequestWarning


def get_raw_text(url='test'):
    proxies = {
        'http': 'http://' + USER + ':' + PASS + '@unblock.oxylabs.io:60000',
        'https': 'http://' + USER + ':' + PASS + '@unblock.oxylabs.io:60000',
    }
    headers_list = [{ 
        'authority': 'in.hotjar.com',
        'method': 'POST',
        'path': '/api/v2/client/sites/2829708/visit-data?sv=7',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,it;q=0.8,es;q=0.7',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Microsoft Edge";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "macOS",
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Edg/101.0.1210.47',
    }] 
    return requests.request('GET', url, headers=random.choice(headers_list), verify=False, proxies=proxies).text

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

p_file = open('products.txt', 'r', encoding='utf-8')
p_lines = p_file.readlines()
existing_products = []
for l in p_lines:
    existing_products.append(l.replace("\n", "").strip())

new_p = open('products.txt', 'a', encoding='utf-8')
for i in range(0):
    r_string = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(1, 3)))
    url = 'https://www.facebook.com/marketplace/nyc/search?query=' + r_string
    text = get_raw_text(url)
    soup = BeautifulSoup(text, 'html.parser')
    p = soup.find_all("span", class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
    for i in p:
        if i.text not in existing_products:
            new_p.write('{}\n'.format(i.text))

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
    
        text = get_raw_text(url)
        
        if len(text) < 30:
            raise Exception("PROXY: Proxy is not working.")
        
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
