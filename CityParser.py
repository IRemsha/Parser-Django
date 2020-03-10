import requests
from bs4 import BeautifulSoup


def get_cities():
    res = requests.get('https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8').text
    soup = BeautifulSoup(res)
    table = soup.find_all('table')[1]
    for tr in table.find_all('tr'):
        try:
            city = tr.find_all('td')[2].text.strip(' ')
            region = tr.find_all('td')[3].text.strip(' ')
            print(city, region)
            with open('cities.txt', 'a') as f:
                print(city, file=f)
            with open('regions.txt', 'a') as f:
                print(region, file=f)

        except IndexError:
            continue

get_cities()