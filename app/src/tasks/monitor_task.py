import sys
import requests
import logging
from datetime import datetime
from pymongo import MongoClient
from Domain import Product, History
from html_processing import get_history_from_product_page

def run():
    if len(sys.argv) != 5:
        logging.fatal('Incorrect number of arguments')
        return

    shop = sys.argv[1]
    logging.info('Shop: ' + str(shop))
    db_name = sys.argv[2]
    logging.info('DB name: ' + str(db_name))
    product_table_name = sys.argv[3]
    logging.info('Product table: ' + str(product_table_name))
    price_history_table_name = sys.argv[4]
    logging.info('History table: ' + str(price_history_table_name))

    logging.info('Connecting to database...')
    db_connection = MongoClient()[db_name]
    product_table = db_connection[product_table_name]
    price_history_table = db_connection[price_history_table_name]

    logging.info('Loading products to monitor...')
    monitored_products = []
    for x in product_table.find():
        monitored_products.append(Product(x['_id'], x['title'], x['link'], x['best_price'], x['current_price'],
                                          x['best_price_date'], x['current_price_date'], image_link=x['image_link'],
                                          monitored=bool(x['monitored'])))
    logging.info('Total number of products found: ' + str(len(monitored_products)))

    logging.info('Starting making requests...')
    for product in monitored_products:
        logging.info('Request for product_id: ' + str(product._id))
        response = requests.get(product.link)
        logging.info('Response status code: ' + str(response.status_code))

        if response.status_code == 200:
            prices_dto = get_history_from_product_page(response.content)
            history = History(product._id, prices_dto.old_price, prices_dto.new_price, shop, datetime.now())

            price_history_table.insert_one(history.__dict__)

            my_query = {'_id': history.product_id}

            best = product_table.find_one(my_query)
            best_price = best['best_price']
            current_price = history.new_price
            new_values = {'$set': {'current_price': current_price,
                                   'best_price': best_price if best_price < current_price else current_price,
                                   'current_price_date': history.date,
                                   'best_price_date': best[
                                       'best_price_date'] if best_price <= current_price else history.date}}
            product_table.update_one({'_id': history.product_id}, new_values)

logging.basicConfig(filename='history.logs', level=logging.INFO)
logging.info('Starting monitoring task at ' + str(datetime.now()))
try:
    run()
except Exception as e:
    logging.fatal('Task encountered exception:')
    logging.fatal(e)
logging.info('Exiting monitoring task at ' + str(datetime.now()))
