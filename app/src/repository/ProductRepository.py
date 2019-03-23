from pymongo import MongoClient
import logging
from Domain import Product, Avatar


class ProductMongoDbRepository:
    def __init__(self, db_name):
        logging.info('Initializing DB connection with %s' % db_name)
        self.__db_name = db_name
        self.__db_connection = MongoClient()['price_manager']
        logging.info('Initializing tables connections')
        self.__product_table = self.__db_connection['product']
        self.__price_history_table = self.__db_connection['price_history']
        self.__avatar_table = self.__db_connection['avatar']
        logging.info('DB connection succeeded')

    # TODO: Make transactional
    def save_one_product(self, product_obj, bin_img):
        self.__product_table.insert_one(product_obj.__dict__)
        avatar = Avatar(bin_img, product_obj._id)
        self.__avatar_table.insert_one(avatar.__dict__)

    def get_image(self, product_id):
        return self.__avatar_table.find_one({'product_id': product_id})['img_data']

    def save_one_history(self, history_obj):
        self.__price_history_table.insert_one(history_obj.__dict__)

        my_query = {'_id': history_obj.product_id}

        best = self.__product_table.find_one(my_query)
        best_price = best['best_price']
        current_price = history_obj.new_price
        new_values = {'$set': {'current_price': current_price,
                               'best_price': best_price if best_price < current_price else current_price,
                               'current_price_date': history_obj.date,
                               'best_price_date': best[
                                   'best_price_date'] if best_price < current_price else history_obj.date}}
        self.__product_table.update_one({'_id': history_obj.product_id}, new_values)

    def set_monitoring_product(self, product_id, to_monitor=True):
        new_values = {"$set": {"monitored": to_monitor}}
        filter = {'_id': product_id}
        self.__product_table.update_one(filter, new_values)

    def get_all_products(self):
        products = []
        for x in self.__product_table.find():
            products.append(Product(x['_id'], x['title'], x['link'], x['best_price'], x['current_price'],
                                    x['best_price_date'], x['current_price_date'], image_link=x['image_link'],
                                    monitored=bool(x['monitored'])))
        return products

    def get_min_price(self, product_id: int):
        # val = self.__price_history_table.aggregate([
        #     { "$match" : { "product_id": product_id }},
        #     { "$group": { "_id": "$product_id", "min_price": {"$min": "$new_price"} }}])
        val = self.__price_history_table.find({'product_id': product_id}).sort([('new_price', 1)]).limit(1)

        for price_obj in val:
            return price_obj['new_price'], price_obj['date']

        return -1, 'n/a'

    def get_current_price(self, product_id: int):
        val = self.__price_history_table.find({'product_id': product_id}).sort([('date', -1)]).limit(1)

        for price_obj in val:
            return price_obj['new_price'], price_obj['date']

        return -1, 'n/a'

    def get_all_monitored_products(self):
        logging.info('DB query to find all products')
        filter = {'monitored': True}
        return self.__product_table.find(filter)

        # Returns a list of touples (date, price)

    def get_all_history(self, product_id: int):
        return [(h['date'], h['new_price']) for h in
                self.__price_history_table.find({'product_id': product_id}).sort([('date', 1)])]

    def find_product(self, product_id: int):
        x = self.__product_table.find_one({'_id': product_id})
        if x is None:
            return None
        return Product(int(x['_id']), x['title'], x['link'],
                       x['best_price'], x['current_price'], x['best_price_date'], x['current_price_date'],
                       image_link=x['image_link'], monitored=bool(x['monitored']))
