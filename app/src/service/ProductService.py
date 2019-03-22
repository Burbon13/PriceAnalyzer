from obs.Observable import Observable
from obs.Events import Events
import logging
from text_processing import *
from html_processing import get_history_from_product_page
from Domain import History
import requests
from datetime import datetime

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