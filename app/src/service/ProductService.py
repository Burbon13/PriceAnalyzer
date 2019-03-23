from obs.Observable import Observable
from obs.Events import Events
import logging

from shops_data import shops
from text_processing import *
from html_processing import get_history_from_product_page, scan_html_for_products
from Domain import History
import requests
from datetime import datetime

from url_generator import url_search_generator


class ProductService(Observable):
    def __init__(self, product_repo):
        Observable.__init__(self)
        self.product_repo = product_repo
    
    def find_all_products(self):
        return self.product_repo.get_all_products()

    def save(self, *products):
        pass

    def set_monitoring(self, product, state: bool):
        pass

    def delete(self, *products):
        pass

    def current_price(self, product_id: int):
        return self.product_repo.get_current_price(product_id)

    def lowest_price(self, product_id: int):
        return self.product_repo.get_min_price(product_id)

    def get_all_history(self, product_id: int):
        return self.product_repo.get_all_history(product_id)

    def set_monitoring_product(self, product_id, to_monitor=True):
        self.product_repo.set_monitoring_product(product_id, to_monitor)
        self.notify_observers((product_id, to_monitor), Events.MONITORING)

    def monitor(self):
        shop = 'emag'
        logging.info('Monitoring scan initializing')
        data = self.product_repo.get_all_monitored_products()

        for product in data:
            response = requests.get(product['link'])
            pricesDTO = get_history_from_product_page(response.content)
            history = History(product['_id'], pricesDTO.old_price, pricesDTO.new_price, shop, datetime.now())
            self.product_repo.save_one_history(history)

    def search_products(self, product_name, category, shop):
        # product_name = 'iphone'
        product_category = shops[shop]['categories'][category]
        # shop = 'emag'
        url = url_search_generator(shop, product_category, product_name)

        try:
            logging.info('Sending http request')
            response = requests.get(url)
            logging.info('Http request response status code %d' % response.status_code)
            html_data = response.content
            product_data_list = scan_html_for_products(html_data, shop, product_name)
            #save_to_db(product_data_list, mongo_db)
            return product_data_list
        except ConnectionError as e:
            logging.critical(e)
        return None

    def product_already_exists(self, product_id):
        return self.product_repo.find_product(product_id) is not None