import requests
import random
import re
from datetime import date

def get_raw_text(url='test'):
    proxies = ['http://159.203.3.234', 'http://164.132.170.100', 'http://146.59.2.185', 'http://137.74.65.101', ] 
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

locations = {'Columbia, MD': '103106366396503', 'Washington, DC': 'dc', 'Alexandria, VA': '109360339083522', 'Virginia Beach, VA': 'virginiabeach', 'Richmond, VA': 'richmond', 'Philadelphia, PA': 'philly', 'Baltimore, MD': 'baltimore', 'New York City, NY': 'nyc', 'Rochester, NY': 'rochester', 'Columbus, OH': 'columbus', 'Cleveland, OH': 'cleveland', 'York, PA': '108944152458332', 'Dover, DE': '112348422111140'}
products = ['Kawasaki Ninja 300', 'Yamaha R3', 'Yamaha R6', 'Onewheel Pint', 'Onewheel XR', 'Onewheel GT', 'Snowboard', 'Skis', 'Miata', ]
f = open('data.txt', 'a')

for product in products:
    for location in locations:
        url = 'https://www.facebook.com/marketplace/' + locations[location] + '/search?query=' + product.replace(' ', '%20')
    
        text = get_raw_text(url)
        
        prices = re.findall(r'\$[\d]+,?[\d]+', text)[0:12]
        miles = re.findall(r'[\d]+[.\d]?[K]? miles', text)[0:12]

        average = 0
        for price in prices:
            price = int(price.replace('$', '').replace(',', ''))
            average += price
        average /= len(prices)
        average = round(average, 2)

        # for p in range(len(prices)):
        #     price = int(prices[p].replace('$', '').replace(',', ''))
        #     if price < 0.6 * average or price > 2.0 * average:
        #         prices.pop(price)
        for p in prices:
            price = int(p.replace('$', '').replace(',', ''))
            if price < 0.6 * average or price > 1.5 * average:
                prices.remove(p)

        average = 0
        for price in prices:
            price = int(price.replace('$', '').replace(',', ''))
            average += price
        average /= len(prices)
        average = round(average, 2)

        summary = ("\n{} -- {}, {}. Average: ${}".format(date.today(), product, location, average))

        print(summary)
        print(prices)
        print(miles)
        f.write(summary + '\n' + ', '.join(prices) + '\n')
    f.write("-------------------------")
