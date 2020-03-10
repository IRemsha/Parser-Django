from bs4 import BeautifulSoup
from threading import Thread
from Mixins import *
from queue import Queue
from Errors import IpBlocked, DeletedAd
import time
import requests
import re
from Driver import Driver
import datetime

class DomClickManager(Thread):
	def __init__(self, data, threads_amount_current):
		super(DomClickManager, self).__init__()
		self._ads_list_url_pattern = "https://domclick.ru/search?offset={}&limit=10&sort_dir=desc"
		
		self._data = data
		
	def run(self) -> None:
		driver = Driver()
		driver = driver.get_driver()
		driver.get('https://domclick.ru/search?offset=10&limit=10&sort_dir=desc')
		html = driver.page_source
		soup = BeautifulSoup(html)
		
		max_ads = re.search('(\d*)', soup.find('div', {'class': 'listing-title'}).text.replace(' ', '')).group(1)
		for i in range(0, int(max_ads), 100):
			soup = BeautifulSoup(requests.get(self._ads_list_url_pattern.format(i)).text)
			hrefs = list(map(lambda a: a.get('href', ''), soup.find_all('a')))
			for href in hrefs:
				if href.find('card') != -1:
					self._data.put(href)


class DomClickCurrent(Thread):
	def __init__(self, urls, data):
		super(DomClickCurrent, self).__init__()
		self._url = 'https://domclick.ru'
		self._urls = urls
		self._data = data
		
	def get_page(self, url):
		d = Driver().get_driver()
		d.get(url)
		return BeautifulSoup(d.page_source)

	def get_params(self, soup):
		data = {}
		params = {
			'Площадь': ['square_all', clear_nums],
			'Комнат': ['room', clear_nums],
			'Жилая': ['square_live',clear_nums],
			'Кухня': ['square_kitchen',clear_nums],
			'Этаж': ['floor', clear_nums],
			'Тип сделки': ['ad_type', clear_str]
		}

		for section in soup.find_all('section'):
			for li in section.find_all('li'):
				for key, value in params.items():
					if li.text.find(key) != -1:
						data[value[0]] = value[1](li.text.replace(key, ''))
		return data

	def parse(self, url):
		soup = self.get_page(url)
		data = self.get_params(soup)
		data['site'] = 'domclick.ru'
		data['city'] = get_city()
		data['url'] = url
		data['material'] = -1
		data['object_old_type'] = -1
		data['object_type'] = -1
		data['room'] = data.get('room') or -1
		data['last_seen'] = datetime.datetime.timestamp(datetime.datetime.now())
	
		for img in soup.find_all('meta'):
			if img.get('content', '').find('https://img01.domclick.ru') != -1:
				data['img'] = img.get('content')
				break
		self._data.put(data)

	def run(self):
		while iter(self._urls.get, False):
			self.parse(self._url + self._urls.get())
