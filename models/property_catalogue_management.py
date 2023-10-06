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

    def search_property_by_address_tenant(self, address):
        sql = f'select * from {PropertyCatalogue.table} where' \
              f' address like "%{address}%";'

        with self.connect_db() as db:
            with db.cursor(pymysql.cursors.DictCursor) as cs:
                cs.execute(sql)
                result = cs.fetchall()

        return result

    def search_property_by_address_agent(self, address, agent_id):
        sql = f'select * from {PropertyCatalogue.table} where' \
              f' agent_id={agent_id} and address like "%{address}%";'

        with self.connect_db() as db:
            with db.cursor(pymysql.cursors.DictCursor) as cs:
                cs.execute(sql)
                result = cs.fetchall()

        return result

    def search_property_by_property_id_agent(self, property_id, agent_id):
        sql = f'select * from {PropertyCatalogue.table} where' \
              f' property_id={property_id} and agent_id={agent_id};'

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

    # could update landlord_id, agent_id, tenant_id, address, price, description, status
    def update_property_landlord_id(self, property_id, agent_id, update_id):
        sql = f'update {PropertyCatalogue.table} set landlord_id={update_id} ' \
              f'where property_id={property_id} and agent_id={agent_id};'

        with self.connect_db() as db:
            with db.cursor() as cs:
                cs.execute(sql)
                db.commit()

    def update_property_agent_id(self, property_id, previous_id, update_id):
        sql = f'update {PropertyCatalogue.table} set agent_id={update_id} ' \
              f'where property_id={property_id} and agent_id={previous_id};'

        with self.connect_db() as db:
            with db.cursor() as cs:
                cs.execute(sql)
                db.commit()

    def update_property_tenant_id(self, property_id, agent_id, update_id):
        sql = f'update {PropertyCatalogue.table} set tenant_id={update_id} ' \
              f'where property_id={property_id} and agent_id={agent_id};'

        with self.connect_db() as db:
            with db.cursor() as cs:
                cs.execute(sql)
                db.commit()

    def update_property_address(self, property_id, agent_id, update_address):
        sql = f'update {PropertyCatalogue.table} set address="{update_address}" ' \
              f'where property_id={property_id} and agent_id={agent_id};'

        with self.connect_db() as db:
            with db.cursor() as cs:
                cs.execute(sql)
                db.commit()

    def update_property_price(self, property_id, agent_id, update_price):
        sql = f'update {PropertyCatalogue.table} set price={update_price} ' \
              f'where property_id={property_id} and agent_id={agent_id};'

        with self.connect_db() as db:
            with db.cursor() as cs:
                cs.execute(sql)
                db.commit()

    def update_property_description(self, property_id, agent_id, update_desc):
        sql = f'update {PropertyCatalogue.table} set description="{update_desc}" ' \
              f'where property_id={property_id} and agent_id={agent_id};'

        with self.connect_db() as db:
            with db.cursor() as cs:
                cs.execute(sql)
                db.commit()

    def update_property_status(self, property_id, agent_id, update_status):
        sql = f'update {PropertyCatalogue.table} set status={update_status} ' \
              f'where property_id={property_id} and agent_id={agent_id};'

        with self.connect_db() as db:
            with db.cursor() as cs:
                cs.execute(sql)
                db.commit()

    def update_property_all(self, property_id, landlord_id, agent_id, tenant_id, address, price
                            , description, status):

        sql = f'update {PropertyCatalogue.table} set landlord_id={landlord_id}, agent_id={agent_id}'\
              f', tenant_id={tenant_id}, address="{address}", price={price}, description="{description}",' \
              f'status={status} ' \
              f'where property_id={property_id} and agent_id={agent_id};'

        with self.connect_db() as db:
            with db.cursor() as cs:
                cs.execute(sql)
                db.commit()

    def delete_property(self, property_id, agent_id):
        sql = f'delete from {PropertyCatalogue.table} where property_id={property_id} ' \
              f'and agent_id={agent_id};'

        with self.connect_db() as db:
            with db.cursor() as cs:
                cs.execute(sql)
                db.commit()


if __name__ == '__main__':
    db_test = PropertyCatalogue()
    # result = db_test.sort_property_by_search_keywords(address='NSW', price=1500)
    # result = db_test.sort_property_by_search_keywords(address='NSW')
    # print(result)
    # db_test.delete_property(2, 23)
    db_test.update_property_description(5, 40, 'remodelling house')