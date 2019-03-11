from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.zoo
animals = db.animals

animal = {
    'name': 'cat',
    'height': 100,
    'price': 500,
    'food': 7
}

print(animals.find_one())

# result = animals.insert_one(animal)
# print(result)