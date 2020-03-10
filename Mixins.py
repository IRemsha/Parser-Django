import re
import requests
import random
from Proxy import Proxy


def get_city(city_raw='Москва'):
    with open('cities.txt', 'r', encoding='utf-8') as f:
        cities = f.read().split('\n')
    for city in cities:
        if city_raw.find(city) != -1:
            return city


def clear_floor(floor):
    return floor.replace(' из ', '/')


def get_ad_type(row):
    SELL_KEY_WORDS = ['prodazh', 'Продажа']
    for word in SELL_KEY_WORDS:
        if re.search(word, row):
            return 'sell'
    return 'rent'


def get_page(url):
    headers = {
        'user-agent': 'Mozilla/4.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3904.97 Safari/537.36'
    }

    proxy_manager = Proxy()
    proxy_list = proxy_manager.get_proxy()

    session = requests.Session()
    session.headers.update(headers)

    while True:
        try:
            proxy = proxy_list[random.randint(0, len(proxy_list) - 1)]
            session.proxies = proxy
            result = session.get(url)
            result.encoding = 'cp-1250'
            result = result.text
            return result
        except Exception:
            print('IP blocked or other error, ', )
    # with open('test.html', 'r', encoding='utf-8') as f:
    #     return f.read()


def clear_nums(num):
    #num = clear_floor(num)
    try:
        num = re.sub('\s*', '', num)
        num = int(re.search('([0-9]*)', num).group(1))
        return num
    except ValueError as err:
        return 0


def clear_str(string):
    try:
        string = str(re.search('([a-zA-Zа-яА-Я\s]*)', string).group(1))
        return string
    except IndexError:
        return ''


def clear_str_and_nums(string):
    try:
        string = str(re.search('([a-zA-Zа-яА-Я0-9/./,]*)', string).group(1))
        return string
    except IndexError:
        return ''


def strip_spaces(row):
    return row#.strip(' ')
