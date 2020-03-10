from threading import Thread
from bs4 import BeautifulSoup
import datetime
from queue import Queue
import time
import random

from Mixins import *


class DomofondManager(Thread):
    def __init__(self, data, threads_amount_urls_finder, threads_amount_current):
        super(DomofondManager, self).__init__()
        self._data_queue = data
        self._threads_amount_urls_finder = threads_amount_urls_finder
        self._threads_amount_current = threads_amount_current
        self._url_queue = Queue()

    def run(self):
        for type_ in ['prodazha', 'arenda']:
            for i in range(self._threads_amount_urls_finder):
                worker = DomofondUrlsFinder(self._url_queue, type_)
                worker.start()

        for i in range(self._threads_amount_current):
            worker = DomofondCurrent(self._url_queue, self._data_queue)
            worker.start()


class DomofondUrlsFinder(Thread):
    def __init__(self, url_queue, type_):
        super(DomofondUrlsFinder, self).__init__()
        self._type = type_
        self._menu_url = 'https://www.domofond.ru/{}-nedvizhimosti/search?PropertyTypeDescription=kvartiry&Page={}'
        self._main_url = 'https://www.domofond.ru'
        self._url_queue = url_queue
        print('URL finder start ', type_)

    def get_amount_pages(self):
        result = get_page(self._menu_url.format(self._type, 1))
        soup = BeautifulSoup(result, 'html.parser')
        all = soup.find_all('li', {'class': 'pagination__page___2dfw0'})[-1].text
        try:
            all = int(all)
        except ValueError:
            print('Колво страниц не получено. ОШИБКА.')
        print(all)
        return all

    def get_urls(self):
        for i in range(1, self.get_amount_pages()):
            print('Get ', i, ' page, ', self._type)
            result = get_page(self._menu_url.format(self._type, i))
            soup = BeautifulSoup(result, 'lxml')
            urls = soup.find_all('a', {'class': 'long-item-card__item___ubItG search-results__itemCardNotFirst___3fei6'})
            urls = list(map(lambda a: a.get('href', ''), urls))
            for url in urls:
                self._url_queue.put(self._main_url+url)
            time.sleep(8)

    def run(self):
        self.get_urls()


class DomofondCurrent(Thread):
    def __init__(self, urls, data):
        self._name = 'domofond.ru'
        super(DomofondCurrent, self).__init__()
        self._urls = urls
        self._data_queue = data
        print('Start domofond thread')
        with open('cities.txt', 'r') as f:
            self._cities = f.read().split('\n')
        self._ALIASES = {
            'Город': 'city',
            'Тип': 'object_type',
            'Тип объекта': 'object_old_type',
            'Комнаты': 'room',
            'Этаж': 'floor',
            'Площадь': 'square_all',
            'Площадь кухни': 'square_kitchen',
            'Жилая площадь': 'square_live',
            'Материал здания': 'material'
        }

    def get_info(self, url):
        page = get_page(url)
        soup = BeautifulSoup(page, 'lxml')
        data = {}
        data['site'] = self._name
        data['last_seen'] = datetime.datetime.timestamp(datetime.datetime.now())
        try:
            data['img'] = list(set(re.findall('"url":"(https://st[0-9]*.domofond.ru/1280x960_dom/[0-9]*.jpg)"}', page)))[0]
        except IndexError:
            data['img'] = ''
        data['ad_type'] = get_ad_type(url)
        data['url'] = url
        data['object_old_type'] = 'Вторичная'
        try:
            data['price'] = clear_nums(soup.find('div', {'class': 'information__price___2Lpc0'}).text.replace('₽', '').replace(' ', ''))
        except AttributeError:
            return

        city_raw = soup.find('a', {'class': 'information__address___1ZM6d'}).text
        city_raw = city_raw.replace(',', ' ')
        data['city'] = get_city(city_raw)
        try:
            info = soup.find('div', {'class': 'detail-information__wrapper___FRRqm'}).find_all('div')
        except AttributeError:
            return

        for row in info:
            tmp = row.find_all('span')
            index = self._ALIASES.get(clear_str(tmp[0].text), None)
            if index:
                data[index] = clear_str_and_nums(tmp[1].text)
        self._data_queue.put(data)
        print(data)

    def run(self):
        while iter(self._urls.get, False):
            url = self._urls.get()
            self.get_info(url)
            time.sleep(random.randint(1, 3))
