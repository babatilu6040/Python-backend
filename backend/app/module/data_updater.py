from datetime import datetime
import time
import re
from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


client = MongoClient("mongodb://localhost:27017/")
db = client["Product_Data"]
collection = db["data"]
data = collection.find()

service = Service(ChromeDriverManager().install())                      
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")                  # ✅ Enable modern headless mode
options.add_argument("--disable-gpu")                   # Optional: better compatibility
options.add_argument("--window-size=1920,1080")         # Optional: set full HD viewport

driver = webdriver.Chrome(service=service, options=options)

for product in data:
    product_id = product["Product_id"]
    url = product["url"]

    try:

        print(">>> Launching headless browser...")
        print(f">>>> url {url}\n")
        driver.get(url)
        time.sleep(3)  # Wait for page to load
        
        try:
            Popup = driver.find_element(By.CLASS_NAME, "_30XB9F")
            Popup.click()
            print(">>> Popup closed.")
        except NoSuchElementException:
            print(">>> No popup found.")

        full_html = driver.page_source
        soup = BeautifulSoup(full_html, 'html.parser')  

        try:
            product_price = soup.find_all(class_="Nx9bqj")[0].text
        except IndexError:
            product_price = "N/A" 

        print(f">>>Extracted Price: {product_price}") 

        today = datetime.now().strftime("%d-%m-%y")
        new_price_entry = {"price": product_price, "data": today}

        collection.update_one({"Product_id": product_id},{"$push": {"price_history": new_price_entry}})   
        print(f"✅ Updated {product_id} with price {product_price} on {today}")
    except Exception as e:
        print(f"❌ Error updating {product_id}: {e}")    



driver.quit()    
print(">>> Browser closed.")