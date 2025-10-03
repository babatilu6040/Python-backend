import random
from datetime import datetime, timedelta
from pymongo import MongoClient

# 1. Function to generate random price history
def generate_random_price_history(start_date, end_date, count=10):
    history = []
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    current = start
    while current <= end:
        # random price between 850 and 2000
        prices = [800,900,1000,950,850,1050]  # your array
        price = random.choice(prices)

        history.append({
            "date": current.strftime("%Y-%m-%d"),
            "price": f"₹{price}"
        })

        current += timedelta(days=1)

    return history

# 2. Generate new history
new_history = generate_random_price_history("2025-01-1", "2025-12-31", 10)
print("Generated Price History:", new_history)

# 3. Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # change URI if needed
db = client["Product_Data"]  # replace with your DB name
collection = db["data"]   # replace with your collection name

# 4. Update the document
result = collection.update_one(
    {"Product_id": "SMWHB4YTZGUZTF4K"},
    {"$push": {"price_history": {"$each": new_history}}}
)

print("Matched:", result.matched_count, "Modified:", result.modified_count)
