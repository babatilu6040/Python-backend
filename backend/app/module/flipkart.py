import sys
import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from pymongo import MongoClient

# executed = False   Global flag to avoid double execution

def handle_flipkart(query):
    product_price = None
    product_details = None
    Product_id = None
    
    # global executed
    # if executed:
    #     print(">>> fetch_data_from_query() has already run. Skipping...")
    #     return
    # executed = True
    query = f"https://www.flipkart.com/redmi-watch-move-1-85-premium-amoled-14-day-battery-best-accuracy-dual-core-processor-smartwatch/p/itm901593e8dc1e1?pid=SMWHB4YTZGUZTF4K&lid=LSTSMWHB4YTZGUZTF4KINGE7K&marketplace=FLIPKART&store=ajy%2Fbuh&srno=b_1_1&otracker=browse&fm=organic&iid=en_WzUbIwOVD6NR3nxVqilG5oVWxeJwgl-dnffdc4kusPHeAeJ89Eu0Xy5OhF2vIcXz-Fa4UECfF1CgNiSo7IYfWA%3D%3D&ppt=None&ppn=None&ssid=q5szc0jbj40000001757698702521"
    
    # query = f"https://www.flipkart.com/XGmXw0jvU8%2Fq4jz0pA%3D%3D.MOBG6VF5GZKXHYZK.SEARCH&ppt=hp&ppn=homepage&ssid=qaa2wewwn40000001757690858247"

    print(">>> Starting product data fetch...")

    # Setup Selenium Chrome driver with headless mode
    service = Service(ChromeDriverManager().install())                      
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")                  # ✅ Enable modern headless mode
    options.add_argument("--disable-gpu")                   # Optional: better compatibility
    options.add_argument("--window-size=1920,1080")         # Optional: set full HD viewport

    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("----------------------------- Filpkart --------------------------------------------")
        print("\n")
        print(f">>> Fetching URL: {query}")
        driver.get(query)
        time.sleep(5)  # Wait for page to load

        

        try:
            container = driver.find_element(By.CLASS_NAME, "YJG4Cf")
            print(">>> Page loaded successfully.", container)
        except Exception as e:
            print(f"----- ERROR = Page load failed: {e}  ---")
            return "invalid url"
        # Close any popup if exists
        try:
            Popup = driver.find_element(By.CLASS_NAME, "_30XB9F")
            Popup.click()
            print(">>> Popup closed.")
        except NoSuchElementException:
            print(">>> No popup found.")

        full_html = driver.page_source
        soup = BeautifulSoup(full_html, 'html.parser')
        # Extract product name
        try:
            product_name = soup.find_all(class_="VU-ZEz")[0].text
        except IndexError:
            product_name = soup.title.string or "Unknown Product"
        
        product_name = re.sub(r'\xa0+', ' ', product_name)

        # Extract product price
        try:
            product_price = soup.find_all(class_="Nx9bqj")[0].text
        except IndexError:
            product_price = "N/A"

        # Extract pid from query string
        Product_id = re.search(r"pid=([A-Z0-9]+)", query)
        Product_id = Product_id.group(1) if Product_id else None

        print(f">>> Product Name: {product_name}")
        print(f">>> Product Price: {product_price}")
        print(f">>> Product ID: {Product_id}")

        date_str = datetime.now().strftime("%d-%m-%y")
        # Save product details
        product_details = {
            "Name": product_name,
            "price_history": [{"price":product_price , "data": date_str}],
            "url": query,
            "Product_id": Product_id
        }
        

    finally:
        driver.quit()
        print(">>> Browser closed.")
        if product_details:
            try:
                client = MongoClient("mongodb://localhost:27017/")
                db = client["Product_Data"]
                collection = db["data"]
                product = collection.find_one({"Product_id": Product_id},{ "_id":0})

                if product == None:
                    collection.insert_one(product_details)
                    print("-->>>✅ Product inserted into MongoDB.")
                    product = product_details
                    product.pop("_id", None)        # Remove MongoDB internal ID for cleaner output
                    product.pop("Product_id",None)  # Remove Product_id for cleaner output
                    return product
                
                else:
                    product.pop("_id", None)        # Remove MongoDB internal ID for cleaner output
                    product.pop("Product_id",None)  # Remove Product_id for cleaner output
                    return product
                
            except Exception as e:
                print(f"⚠️ MongoDB insert failed: {e}")    
    


# handle_flipkart()