from bs4 import BeautifulSoup
import re

def get_new_products(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6')

def get_product_prices(text):
    return re.findall(r'\$[\d]+,?[\d]+', text)[0:15]