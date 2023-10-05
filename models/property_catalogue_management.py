# reference: https://yurimkoo.github.io/python/2019/09/14/connect-db-with-python.html

import mysql.connector
import pymysql


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
            with db.cursor() as cs:
                cs.execute(sql)
                db.commit()

    def find_all_properties_by_tenant(self):
        sql = f'select * from {PropertyCatalogue.table};'

        with self.connect_db() as db:
            with db.cursor(pymysql.cursors.DictCursor) as cs:
                cs.execute(sql)
                result = cs.fetchall()

        return result

    def find_all_properties_by_agent(self, agent_id):
        sql = f'select * from {PropertyCatalogue.table} where agent_id={agent_id}'

        with self.connect_db() as db:
            with db.cursor(pymysql.cursors.DictCursor) as cs:
                cs.execute(sql)
                result = cs.fetchall()

        return result

    def find_all_properties_by_landlord(self, landlord_id):
        sql = f'select * from {PropertyCatalogue.table} where landlord_id={landlord_id}'

        with self.connect_db() as db:
            with db.cursor(pymysql.cursors.DictCursor) as cs:
                cs.execute(sql)
                result = cs.fetchall()

        return result

    # search keywords are 'address' or 'price' or both
    def sort_property_by_search_keywords(self, **search_keywords):
        condition = 'where'
        for column_name, value in search_keywords.items():
            if column_name == 'address':
                condition = condition + f' {column_name}="{value}" and'
            else:
                condition = condition + f' {column_name}<={value} and'

        # remove and in the condition statement
        length = len(condition)
        length_ = length - 3
        if condition[length_:] == 'and':
            condition = condition[:length_]

        sql = f'select * from {PropertyCatalogue.table} {condition};'

        with self.connect_db() as db:
            with db.cursor(pymysql.cursors.DictCursor) as cs:
                cs.execute(sql)
                result = cs.fetchall()

        print(sql)
        return result

    def update_property(self):
        pass

    def delete_property(self):
        pass

if __name__ == '__main__':
    db_test = PropertyCatalogue()
    # result = db_test.sort_property_by_search_keywords(address='NSW', price=1500)
    result = db_test.sort_property_by_search_keywords(address='NSW')
    print(result)