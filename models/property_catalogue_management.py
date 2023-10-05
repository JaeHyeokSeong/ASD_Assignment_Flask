# reference: https://yurimkoo.github.io/python/2019/09/14/connect-db-with-python.html

import mysql.connector
import pymysql
import random
import string


class PropertyCatalogue:
    table = 'property'

    def __init__(self):
        self.python_db = None

    def connect_db(self):
        self.python_db = pymysql.connect(
            user='root',
            password='root1234',
            host='127.0.0.1',
            db='python_db',
            charset='utf8'
        )
        return self.python_db

    def add_property(self, landlord_id, agent_id, tenant_id, address, price, description, status):
        sql = f'insert into {PropertyCatalogue.table} values (null, {landlord_id}, {agent_id}, ' \
              f'{tenant_id}, "{address}", {price}, "{description}", {status});'

        with self.connect_db() as db:
            with db.cursor(pymysql.cursors.DictCursor) as cs:
                cs.execute(sql)
                db.commit()

    def find_property(self):
        pass

    def update_property(self):
        pass

    def delete_property(self):
        pass

