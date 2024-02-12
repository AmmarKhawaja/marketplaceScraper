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
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-site": "none",
        "sec-fetch-mod": "",
        "sec-fetch-user": "?1",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "bg-BG,bg;q=0.9,en-US;q=0.8,en;q=0.7"
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
    print(date.datetime())
    prices = []
    print("-")
    for location in locations.keys():
        url = 'https://www.facebook.com/marketplace/' + locations[location].strip() + '/search?query=' + product.replace(' ', '%20')
    
        text = get_raw_text(url)
        
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
