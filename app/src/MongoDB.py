from pymongo import MongoClient
from ProductData import ProductData
from datetime import datetime
import bson


# Use param!
def get_db_connection(db_name: str):
    return MongoClient('mongodb://localhost:27017').price_manager


# Use param!
def get_db_table(table_name: str, db):
    return db.test_table


# Saved BSON encoded file to DB and returns the result
def save_one_to_table(db_table, dict_object):
    return db_table.insert_one(dict_object)



# pd = ProductData('iPhone', 4000, 3700, 1234, 'www.apple.com', str(datetime.now()))
# conn = get_db_connection('')
# table = get_db_table('', conn)
# save_one_to_table(table, pd.__dict__)