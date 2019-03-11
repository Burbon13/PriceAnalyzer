from url_generator import url_search_generator
from shops_data import *
from Domain import Product, History
from html_processing import scan_html_for_products, get_history_from_product_page
# from MongoDB import get_db_connection, get_db_table, save_one_to_table
import requests
from MongoDB import MongoDB
import logging
from datetime import datetime


def save_to_db(product_data_list, mongo_db):
    logging.info('Saving ProductDatas to DB')
    for item in product_data_list:
        mongo_db.save_one_product(Product(item.id, item.title, item.link))
        mongo_db.save_one_history(History(item.id, item.old_price, item.new_price, item.shop, item.date_time))


def scan(mongo_db):
    product_name = 'nokia'
    product_category = shops['emag']['categories']['phones']
    shop = 'emag'
    url = url_search_generator(shop, product_category, product_name)

    try:
        logging.info('Sending http request')
        response = requests.get(url)
        logging.info('Http request response status code %d' % response.status_code)
        html_data = response.content
        product_data_list = scan_html_for_products(html_data, shop, product_name)
        save_to_db(product_data_list, mongo_db)
    except ConnectionError as e:
        logging.critical(e)


# for monitor checked products, the program will execute a price scan
def monitor(mongo_db):
    shop = 'emag'
    logging.info('Monitoring scan initializing')
    data = mongo_db.get_all_monitored_products()
    for product in data:
        response = requests.get(product['link'])
        pricesDTO = get_history_from_product_page(response.content)
        history = History(product['_id'], pricesDTO.old_price, pricesDTO.new_price, shop, datetime.now())
        mongo_db.save_one_history(history)


def main():
    logging.basicConfig(format='%(levelname)s|%(asctime)s|%(filename)s:%(funcName)s:%(lineno)d|%(message)s', level=logging.INFO)
    logging.info('Application started')
    mongo_db = MongoDB('price_manager')
    # scan(mongo_db)
    monitor(mongo_db)


main()