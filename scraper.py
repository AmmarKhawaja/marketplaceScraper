from secret import USER, PASS, SCRAPEOPS_API_KEY
from urllib3.exceptions import InsecureRequestWarning
import requests
from requests_html import HTMLSession
import random

def setup():
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def get_raw_text(url='test', proxy_rotation=True, dynamic=False):
    if proxy_rotation:
        proxies = {
            'http': 'http://' + USER + ':' + PASS + '@unblock.oxylabs.io:60000',
            'https': 'http://' + USER + ':' + PASS + '@unblock.oxylabs.io:60000',
        }
    else:
        proxies = {}
    
    retrieve_headers = requests.get('http://headers.scrapeops.io/v1/browser-headers?api_key=' + SCRAPEOPS_API_KEY).json().get('result', [])
    if dynamic:
        r = HTMLSession().get(url)
        return r.html.render().text
    else:
        return requests.request('GET', url, headers=random.choice(retrieve_headers), verify=False, proxies=proxies).text

