import requests
from datetime import datetime
from pymongo import MongoClient
from Domain import Product, History
from html_processing import get_history_from_product_page

# TODO: Handle exceptions, check for connectivity issues

print('Initializing monitoring')

shop = 'emag'
db_name = 'price_manager'
product_table_name = 'product'
price_history_table_name = 'price_history'

print('Connecting to database')
db_connection = MongoClient()[db_name]
product_table = db_connection[product_table_name]
price_history_table = db_connection[price_history_table_name]

print('Finding products to monitor')
monitored_products = []
for x in product_table.find():
    monitored_products.append(Product(x['_id'], x['title'], x['link'], x['best_price'], x['current_price'],
                            x['best_price_date'], x['current_price_date'], image_link=x['image_link'],
                            monitored=bool(x['monitored'])))

print('Finding current prices')
for product in monitored_products:
    response = requests.get(product.link)
    pricesDTO = get_history_from_product_page(response.content)
    history = History(product._id, pricesDTO.old_price, pricesDTO.new_price, shop, datetime.now())

    #self.product_repo.save_one_history(history)
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

print('Monitoring finished')
input('Press enter to finish')