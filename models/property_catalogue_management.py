# reference: https://yurimkoo.github.io/python/2019/09/14/connect-db-with-python.html

import mysql.connector
import pymysql
import random
import string


class PropertyCatalogue:
    table = 'property'

    def __init__(self):
        self.python_db = None
        self.cursor = None

    def connect_db(self):
        self.python_db = pymysql.connect(
            user='root',
            password='root1234',
            host='127.0.0.1',
            db='python_db',
            charset='utf8'
        )

    def connect_cursor(self):
        self.connect_db()
        self.cursor = self.python_db.cursor(pymysql.cursors.DictCursor)
        return self.cursor

    def add_property(self, landlord_id, agent_id, tenant_id, address, price, description, status):
        sql = f'insert into {PropertyCatalogue.table} values (null, {landlord_id}, {agent_id}, ' \
              f'{tenant_id}, "{address}", {price}, "{description}", {status});'

        with self.connect_cursor() as cs:
            cs.execute(sql)
            self.python_db.commit()

    def find_property(self):
        pass

    def update_property(self):
        pass

    def delete_property(self):
        pass

