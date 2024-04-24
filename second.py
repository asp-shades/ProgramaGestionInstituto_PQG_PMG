import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

print(client.list_database_names())

database = client["General"]

print(database.list_collection_names())

collection = database["Trabajos"]
results = collection.find()
for result in results:
    print(result)
