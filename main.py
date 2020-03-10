from Domofond import DomofondManager
from Cian import CianManager
from Domclick import DomClickManager, DomClickCurrent
from DatabaseManager import DatabaseManager
from Proxy import Proxy
from queue import Queue

data = Queue()

#proxy_manager = Proxy()
#proxy_manager.cache_proxy()

#d = DomofondManager(data, 1, 40)
#cian = CianManager(data, 100)
urls = Queue()
dc = DomClickCurrent(urls, data)
dm = DomClickManager(urls, 5)

dm.start()
dc.start()

db = DatabaseManager(data)

#d.start()
#cian.start()

db.start()

