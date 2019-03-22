from pymongo import MongoClient
import logging
from Domain import Product

class ProductMongoDbRepository:
    def __init__(self, db_name):
        logging.info('Initializing DB connection with %s' % db_name)
        self.__db_name = db_name
        self.__db_connection = MongoClient()['price_manager']
        logging.info('Initializing tables connections')
        self.__product_table = self.__db_connection['product']
        self.__price_history_table = self.__db_connection['price_history']
        logging.info('DB connection succeeded')

    def save_one_product(self, product_obj):
        result = self.__product_table.insert_one(product_obj.__dict__)
        logging.info('Product saved with id %d' % result.inserted_id)

    def save_one_history(self, history_obj):
        result = self.__price_history_table.insert_one(history_obj.__dict__)
        logging.info('History saved with id %s' % str(result.inserted_id))

    def get_all_monitored_products(self):
        logging.info('DB query to find all products')
        filter = {'monitored' : True}
        return self.__product_table.find(filter)

    def set_monitoring_product(self, product_id, to_monitor=True):
        new_values = { "$set": { "monitored": to_monitor } }
        filter = {'_id' : product_id}
        self.__product_table.update_one(filter, new_values)

    def get_all_products(self):
        products = []
        for x in self.__product_table.find():
            products.append(Product(int(x['_id']), x['title'], x['link'], image_link=x['image_link'], monitored=bool(x['monitored'])))
        return products

    # Returns a touple (price, date)
    def get_min_price(self, product_id: int):
        # val = self.__price_history_table.aggregate([
        #     { "$match" : { "product_id": product_id }},
        #     { "$group": { "_id": "$product_id", "min_price": {"$min": "$new_price"} }}])
        val = self.__price_history_table.find({'product_id' : product_id}).sort([('new_price', 1)]).limit(1)

        for price_obj in val:
            return (price_obj['new_price'], price_obj['date'])

        return (-1,'n/a')

    # Returns a touple (price, date)
    def get_current_price(self, product_id: int):
        val = self.__price_history_table.find({'product_id' : product_id}).sort([('date', -1)]).limit(1)

        for price_obj in val:
            return (price_obj['new_price'], price_obj['date'])

        return (-1,'n/a')

    # Returns a list of touples (date, price)
    def get_all_history(self, product_id: int):
        return [(h['date'], h['new_price']) for h in self.__price_history_table.find({'product_id' : product_id}).sort([('date', 1)])]