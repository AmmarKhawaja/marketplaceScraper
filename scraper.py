from secret import USER, PASS, SCRAPEOPS_API_KEY
from urllib3.exceptions import InsecureRequestWarning
import requests
import random

def setup():
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def get_raw_text(url='test'):
    proxies = {
        'http': 'http://' + USER + ':' + PASS + '@unblock.oxylabs.io:60000',
        'https': 'http://' + USER + ':' + PASS + '@unblock.oxylabs.io:60000',
    }
    retrieve_headers = requests.get('http://headers.scrapeops.io/v1/browser-headers?api_key=' + SCRAPEOPS_API_KEY).json().get('result', [])
    return requests.request('GET', url, headers=random.choice(retrieve_headers), verify=False, proxies=proxies).text

