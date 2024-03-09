import sqlite3 as sq
import time
import re
from flask import url_for


class DataBase():
    def __init__(self, db):
        self._db = db
        self._cur = db.cursor()

    def get_objects(self, table):
        sql = f'SELECT * FROM {table}'
        try:
            self._cur.execute(sql)
            res = self._cur.fetchall()
            if res:
                return res
        except IOError:
            print('Ошибка прочтения дазы банных')
        return []

    def add_shoes(self, name, description, size, price, url):
        try:
            self._cur.execute(f'SELECT COUNT() as "count" FROM shoes WHERE name LIKE "{name}" AND size LIKE "{size}"')
            res = self._cur.fetchone()
            if res['count'] > 0:
                print('Эта пара обуви уже добавлена')
                return False

            base = url_for('static', filename='images')
            description = re.sub(r'(?P<tag><img\s+[^>]*src=)(?P<quote>[\'"])(?P<url>.*)(?P=quote)>',
                          r'\g<tag>' + base + r'/\g<url>>', description)

            sql = 'INSERT INTO shoes VALUES(NULL, ?, ?, ?, ?, ?)'
            self._cur.execute(sql, (name, description, size, price, url))
            self._db.commit()
        except sq.Error:
            print('Ошибка добавления обуви в базу данных')
            return False
        return True

    def get_shoe(self, shoe_id):
        try:
            self._cur.execute(f'SELECT name, description FROM shoes WHERE url == "{shoe_id}"')
            res = self._cur.fetchone()
            if res:
                return res
        except sq.Error as e:
            print('Ошибка получения обуви из базы данных', str(e))
        return None, None
