from secret import USER, PASS
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

