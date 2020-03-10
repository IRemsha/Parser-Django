from threading import Thread
import os
from Database import Database


class DatabaseManager(Thread):
    def __init__(self, data):
        super(DatabaseManager, self).__init__()
        self._data_queue = data
        self._db = Database()

    def _add_row(self, row):
        self._db.add_ad(row)

    def run(self):
        while iter(self._data_queue.get, False):
            row = self._data_queue.get()
            self._add_row(row)
