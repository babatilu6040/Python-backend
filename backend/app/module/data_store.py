from pymongo import MongoClient

# Connect to MongoDB (running locally)
client = MongoClient("mongodb://localhost:27017/")
print("---- Connected to MongoDB ---- \n")
print(client)
print("\n")



db = client["Product_Data"]
collection = db["data"]

user = collection.find_one({"url": "http://mclaughlin.info/"})

print(user)
