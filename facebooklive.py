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
import markets
import scraper
import extract


#have a list of search terms and filters. Let users choose search terms, mileage, pricing, profit %, highlighted kws, etc.

url = 'https://www.facebook.com/marketplace/dc/search/?daysSinceListed=1&query=2020%20toyota%20camry&exact=false'
for i in range(3):
    text = scraper.get_raw_text(url)
    if len(text) > 50:
        break

#check that these items are new, facebook products are put into usercache file
# read(cacheddata/date) file that contains entries containing information about search term and underneath that outputs, this
# is so that we do not have to keep scraping sites for the same input, and also so that we can save a lot of data.
print(extract.get_facebook_live(text))

# new items are then compared by either making request for data or reading data from file (files newer than 2 weeks).
# it looks at items and compare with market data of similar cars (similar year, miles).

# if listing is found with price x% below market, then add to pushed products.

# create email that advertises pushed products with all these details and email to user.

# run this script every 30 minutes


    # Create an interface where you can have watched keywords, as well as keyword descriptions. View listings in the
    # watched keywords section every 24 hours. Look for keyword description matches and price matches from markets.py,
    # recommending data that satisfies demands. Products that satisfy demands should be emailed to the user. Furthermore
    # user can have hardcoded alerts setup as well.