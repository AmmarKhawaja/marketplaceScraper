from bs4 import BeautifulSoup
import re
import scraper

def validate(e, type):
    if not e:
        if type == 'int':
            return -1
        elif type == 'str':
            return '-1'
    else:
        if type == 'int':
            return int(float(''.join(re.findall(r'\d', e[0]))))
        elif type == 'str':
            return str(e[0])

def get_facebook_live(text, min_year=None, max_year=None, min_price=None, max_price=None, min_miles=None, max_miles=None,
                      highlighted_keywords=[]):
    #   wrapper name year miles price story_id
    re_codes = [r'"node":(.*?)"MarketplaceSearchFeedStoriesEdge"}', r'"custom_title":"(.*?)"',
                r'(\d{4})', r'"subtitle":"(.*?) miles"', r'"amount":"(.*?)\.', 
                r'"story_key":"(.*?)",', r'<meta name="description" content="(.*?)"']
    wrappers = re.findall(re_codes[0], text)
    products = []
    for wrapper in wrappers:
        name = re.findall(re_codes[1], wrapper)
        if name and len(name[0]) < 40:
            name = name[0]
            year = validate(re.findall(re_codes[2], name), 'int')
            miles = validate(re.findall(re_codes[3], wrapper), 'str')
            if '.' in miles:
                miles = int(miles.replace('.', '').replace('K', '00').replace('M', '00000').replace(',', ''))
            else:
                miles = int(miles.replace('K', '000').replace('M', '000000').replace(',', ''))
            price = validate(re.findall(re_codes[4], wrapper), 'int')
            id = validate(re.findall(re_codes[5], wrapper), 'str')

            item_text = scraper.get_raw_text('https://www.facebook.com/marketplace/item/' + id + '/?ref=search&referral_code=null&referral_story_type=post&tracking=browse_serp%3A7ff9fd3e-8db0-4e24-a21c-64ee65e8ab3a')
            desc = validate(re.findall(re_codes[6], item_text), 'str')
            if ((min_year != None and year != -1 and min_year > year) or (max_year != None and year != -1 and max_year > year) or
                (min_price != None and price != -1 and min_price > price) or (max_price != None and price != -1 and max_price > price)
                or (min_miles != None and miles != -1 and min_miles > miles) or (max_miles != None and miles != -1 and max_miles > miles)):
                continue
            highlighted = False
            for w in highlighted_keywords:
                if w in desc:
                    highlighted = True
                    break
            products.append({"NAME": name, "YEAR": year, "MILES": miles, "PRICE": price, 'DESC': desc, 'HL': highlighted, 'ID': id,})
    return products


def get_products_car(text, source, des_make=None, des_model=None, min_year=None, max_year=None, min_price=None, 
                     max_price=None, min_miles=None, max_miles=None, des_color=None, des_intcolor=None):
    re_codes = []
    #    wrapper, name, make, model, year, type, color, intcolor, miles, price
    if source == 'FACEBOOK':
        re_codes = [r'"node":(.*?)"MarketplaceSearchFeedStoriesEdge"}', r'"custom_title":"(.*?)"', r'^$', r'^$', 
                    r'(\d{4})', r'^$', r'^$', r'^$', r'"subtitle":"(.*?) miles"', r'"amount":"(.*?)\.']
    elif source == 'AUTOTRADER':
        re_codes = [r'"vehicleIdentificationNumber":(.*?),"fuelEfficiency"', r'"name":"(.*?)","mpn"', 
                    r'{"code".*?"name":"(.*?)"}},"model"', r'"model":{"code".*?"name":"(.*?)"},"manufacturer"', 
                    r'(\d{4})', r'"vehicleEngine":"(.*?)"', r'"color":"(.*?)"', r'"vehicleInteriorColor":"(.*?)"', 
                    r'"value":"(.*?)"', r'"price":(.*?),']
    elif source == 'CARFAX':
        re_codes = [r'"@type":"Vehicle"(.*?){"@context"', r'"name":"(.*?)"', r'^$', r'^$', r'(\d{4})', r'"vehicleEngine":"(.*?)"',
                    r'"color":"(.*?)"', r'^$', r'"mileageFromOdometer":(.*?),"', r'"price":(.*?),']
    elif source == 'CARS.COM':
        re_codes = [r'{"name":"Used\s(.*?){"name":"Used', r'(.*?)","description"', r'"brand":{"name":"(.*?)",', r'^$',
                    r'(\d{4})', r'"vehicleTransmission":"(.*?)"}', r'"color":"(.*?)"', r'"vehicleInteriorColor":"(.*?)",',
                    r'"mileageFromOdometer":"(.*?)"', r'"price":"(.*?)"']

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
            if ((des_make != None and make != '-1' and (des_make != make or make not in name)) or (des_model != None and model != '-1' and (des_model != model or model not in name)) or 
                (min_year != None and year != -1 and year < min_year) or (max_year != None and year != -1 and year > max_year) or 
                (min_price != None and price != -1 and price < min_price) or (max_price != None and price != -1 and price > max_price) or 
                (min_miles != None and miles != -1 and miles < min_miles) or (max_miles != None and miles != -1 and miles > max_miles) or 
                (des_color != None and color != '-1' and des_color != color) or (des_intcolor != None and intcolor != '-1' and des_intcolor != intcolor)):
                continue
            products.append({"NAME": name, "MAKE": make, "MODEL": model, "YEAR": year, "TYPE": type, "COLOR": color, "INTCOLOR": intcolor, "MILES": miles, "PRICE": price, 'SOURCE': source})
    return products