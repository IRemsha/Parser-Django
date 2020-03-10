from bs4 import BeautifulSoup
from threading import Thread
from Mixins import *
from queue import Queue
from Errors import IpBlocked, DeletedAd
import time


class CianIdGenerator(Thread):
    def __init__(self, data):
        super(CianIdGenerator, self).__init__()
        self._data = data

    def run(self):
        i = 220100010
        while i < 299999999:
            self._data.put(i)
            i += 1


class CianManager(Thread):
    def __init__(self, data, threads_amount_current):
        super(CianManager, self).__init__()
        self._threads_amount_current = threads_amount_current
        self._data_queue = data
        self._url_queue = Queue()

    def run(self):
        c = CianIdGenerator(self._url_queue)
        c.start()

        for i in range(0, self._threads_amount_current):
            print('cian start ', i)
            c = CianCurrent(self._url_queue, self._data_queue)
            c.start()


class CianCurrent(Thread):
    def __init__(self, urls, data):
        super(CianCurrent, self).__init__()
        self._url = 'https://cian.ru/{}/flat/{}/'
        self._name = 'cian.ru'
        self._data = data
        self._urls = urls

    def get_page(self, url):
        page = get_page(url)
        soup = BeautifulSoup(page, 'html.parser')
        if page.find('Объявление снято с публикации') !=-1 or page.find('Страница не найдена') !=-1:
            raise DeletedAd
        if soup.text.find('Captcha') != -1:
            raise IpBlocked
        return soup

    def get_params(self, rows):
        params = {
            'square_all': [clear_nums, 'Общая'],
            'floor': [clear_nums, 'Этаж'],
            'material': [clear_str, 'Тип дома'],
            'square_kitchen': [clear_nums, 'Кухня'],
            'square_live': [clear_nums, 'Жилая']
        }

        data = {}
        for key, value in params.items():
            data[key] = -1

        for key, value in params.items():
            for row in rows.find_all('div', {'class': 'a10a3f92e9--info--2ywQI'}):
                if row.text.find(value[1]) != -1:
                    data[key] = value[0](row.find('div', {'class': 'a10a3f92e9--info-text--2uhvD'}).text)
                    break
        return data

    def parse(self, soup, url):
        data = {}
        ids = {

            'price': {'block': 'span', 'id': 'itemprop', 'name': 'price', 'handler': clear_nums},
            'ad_type': {'block': 'div', 'id': 'data-name', 'name': 'OfferBreadcrumbs', 'handler': get_ad_type},

        }
        for key, value in ids.items():
            try:
                data[key] = value.get('handler', strip_spaces)(soup.find(value.get('block'), {value.get('id'): value.get('name')}).text)
            except AttributeError:
                continue
        data.update(self.get_params(soup.find('div', {'class': 'a10a3f92e9--info-block--3hCay'})))
        data['url'] = url
        data['site'] = self._name
        h1 = soup.find('h1', {'class': 'a10a3f92e9--title--2Widg'}).text
        try:
            data['room'] = clear_nums(re.search('([0-9]*)-комн', h1).group(1))
        except AttributeError:
            if h1.find('Комната') != -1 or h1.find('Студия'):
                data['room'] = 1
            else:
                data['room'] = -1

        city = soup.find('address', {'class', 'a10a3f92e9--address--140Ec'}).text
        data['city'] = ''
        city = city.split(',')
        for row in city:
            city_name = get_city(row)
            if city_name != '':
                data['city'] = city_name
                break
        if data['city'] == '':
            return

        data['object_type'] = -1
        data['object_old_type'] = -1
        data['img'] = soup.find('img', {'class':  'a10a3f92e9--photo--3ybE1'}).get('src')
        self._data.put(data)
        print(data)
        #636 430

    def run(self):
        while iter(self._urls.get, False):
            for type_ in ['sell', 'rent']:
                url = self._url.format(type_, self._urls.get())
                try:
                    page = self.get_page(url)
                    print('url ', url, ' ok')
                    time.sleep(0.9)
                except DeletedAd:
                    print('url ', url, ' снят')
                    continue
                except IpBlocked:
                    print('IP BLOCKED')
                    continue
                try:
                    self.parse(page, url)
                except AttributeError:
                    continue
                    #https://www.proxy-list.download/api/v1/get?type=http&anon=elite&country=US
# c = CianCurrent()
# page = (c.get_page('188100010'))

# c.parse(page)

