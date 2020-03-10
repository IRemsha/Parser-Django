import requests
import json


class Proxy:
    def __init__(self):
        with open('code.txt', 'r') as f:
            code = f.read()
        #self._url = 'http://hidemy.name/ru/api/proxylist.php?out=plain&code={}'.format(code)
        self._url = 'http://hidemy.name/ru/api/proxylist.php?out=js'
        print(self._url)

    def cache_proxy(self):
        data = json.loads(requests.get(self._url).text)
        clean_data = []
        for row in data:
            if row.get('ssl') == '1':
                type_ ='https'
            elif row.get('socks4') == '1':
                type_ ='socks4'
            elif row.get('socks5') == '1':
                type_ = 'socks5'
            else:
                continue
            clean_data.append({type_: row.get('host')+':'+row.get('port')})
        with open('proxy.txt', 'w') as f:
            f.write(json.dumps(clean_data))

    def get_proxy(self):
        with open('proxy.txt', 'r') as f:
            data = json.loads(f.read())
        return data
