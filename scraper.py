from secret import USER, PASS, SCRAPEOPS_API_KEY
from urllib3.exceptions import InsecureRequestWarning
import requests
from requests_html import HTMLSession
import random
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

def selenium_get_raw_text(url='test'):
    wire_options = {
        "proxy": {
            "http": f'http://' + USER + ':' + PASS + '@unblock.oxylabs.io:60000',
            "https": f'http://' + USER + ':' + PASS + '@unblock.oxylabs.io:60000',
        }
    }
    options = webdriver.ChromeOptions()
    options.add_argument('--user-agent=' + str(random.choice(requests.get('http://headers.scrapeops.io/v1/browser-headers?api_key=' + SCRAPEOPS_API_KEY).json().get('result', []))))
    options.add_argument('--enable-javascript')
    seleniumwire_options = {
        **wire_options,
        "driver_path": ChromeDriverManager().install(),
        'disable_capture': True,
    }
    driver = webdriver.Chrome(
        options=options,
        seleniumwire_options=seleniumwire_options,
    )
    driver.header_overrides = {'x-oxylabs-geo-location': 'Texas,United States'}
    
    driver.get(url)
    print('written')
    time.sleep(5)
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='x1i10hfl x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x14yjl9h xudhj91 x18nykt9 xww2gxu x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xl56j7k xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xc9qbxq x14qfxbe x1qhmfi1']"))).click()
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='x1i10hfl x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x14yjl9h xudhj91 x18nykt9 xww2gxu x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xl56j7k xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xc9qbxq x14qfxbe x1qhmfi1']"))).click()

    #x1i10hfl x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz x6s0dn4 x14yjl9h xudhj91 x18nykt9 xww2gxu x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xl56j7k xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xc9qbxq x14qfxbe x1qhmfi1
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xmjcpbm x1n2xptk xkbpzyx xdppsyt x1rr5fae xhk9q7s x1otrzb0 x1i1ezom x1o6z2jb x9f619 xzsf02u x1qlqyl8 xk50ysn x1y1aw1k xn6708d xwib8y2 x1ye3gou xh8yej3 xha3pab xyc4ar7 x10lcxz4 xzt8jt4 xiighnt xviufn9 x1b3pals x10bruuh x1yc453h xc9qbxq' and @placeholder='Min']"))).send_keys('1')
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='x1i10hfl xggy1nq x1s07b3s x1kdt53j x1a2a7pz xmjcpbm x1n2xptk xkbpzyx xdppsyt x1rr5fae xhk9q7s x1otrzb0 x1i1ezom x1o6z2jb x9f619 xzsf02u x1qlqyl8 xk50ysn x1y1aw1k xn6708d xwib8y2 x1ye3gou xh8yej3 xha3pab xyc4ar7 x10lcxz4 xzt8jt4 xiighnt xviufn9 x1b3pals x10bruuh x1yc453h xc9qbxq' and @placeholder='Max']"))).send_keys('999999')
    
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x78zum5 x1a2a7pz xqvfhly x1emribx xdj266r']"))).click()
    f = open('test.txt', 'w', newline='', encoding='utf-8')
    f.write(driver.page_source)
    time.sleep(200)

    return driver.page_source
