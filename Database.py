import sqlite3


class Database:
    def __init__(self):
        self._conn = sqlite3.connect('db.sqlite3', check_same_thread=False)
        self._cursor = self._conn.cursor()

    def _execute(self, sql, data):
        while True:
            try:
                if sql.find('INSERT') != -1 or sql.find('UPDATE') != -1 or sql.find('DELETE') != -1:
                    self._cursor.execute(sql, data)
                    self._conn.commit()
                    return self._cursor.lastrowid

                if sql.find('SELECT') != -1:
                    self._cursor.execute(sql, data)
                    res = self._cursor.fetchall()
                    try:
                        return res[0]
                    except IndexError:
                        return None
                break
            except sqlite3.OperationalError as err:
                print(err)
                break
#                continue

    def _add_param(self, table, data):
        table_old = table
        table = table.replace('_', '')
        try:
            sql = 'INSERT INTO pint_{}(name) VALUES(?)'.format(table)
            res = self._execute(sql, (data,))
        except sqlite3.IntegrityError:
            sql = 'SELECT `id` FROM pint_{} WHERE name=?'.format(table)
            res = self._execute(sql, (data, ))[0]
        return {table_old+'_id': res}

    def _add_imgs(self, data, ad_id):
        sql_img = 'INSERT INTO pint_image(name) VALUES(?)'
        sql_link = 'INSERT INTO pint_ad_imgs(ad_id, image_id) VALUES(?,?)'

        for row in data.get('imgs'):
            try:
                img_id = self._execute(sql_img, (row,))
                self._execute(sql_link, (ad_id, img_id,))
            except sqlite3.IntegrityError:
                continue

    def add_ad(self, data):
        NOT_TABLES = ['square_all', 'square_live', 'url', 'last_seen', 'price', 'square_kitchen', 'img']
        params = ''
        values = ''
        for key, value in data.items():
            if key in NOT_TABLES:
                continue
            id_ = self._add_param(key, value)
            for key, value in id_.items():
                params +=key+','
                values +=str(value)+','
        for not_table in NOT_TABLES:
            values += '"'+str(data.get(not_table, '0'))+'"'+','
            params += str(not_table)+','
        values = values[:-1]
        params = params[:-1]
        sql_main = 'INSERT INTO pint_ad({}) VALUES({});'.format(params, values)
        try:
            ad_id = self._execute(sql_main, ())
        except sqlite3.IntegrityError as err:
            try:
                sql = 'SELECT id FROM `pint_ad` WHERE url = ?'
                id_ = self._execute(sql, (data.get('url'),))[0]
                sql = 'UPDATE pint_ad SET last_seen = ? WHERE id =?'
                self._execute(sql, (data.get('last_seen', ''), id_,))
                print('upd last seen')
            except:
                pass
