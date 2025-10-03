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


def handle_amazon():
    product_price = None
    product_details = None
    Product_id = None

    query = f"https://www.amazon.in/Acer-Predator-Monitor-FreeSync-Speakers/dp/B0DQLBTDCJ/ref=pd_ci_mcx_mh_mcx_views_1_image?pd_rd_w=6vWc6&content-id=amzn1.sym.04d3fdac-1b15-414f-91d2-0c9aaaf137d6%3Aamzn1.symc.30e3dbb4-8dd8-4bad-b7a1-a45bcdbc49b8&pf_rd_p=04d3fdac-1b15-414f-91d2-0c9aaaf137d6&pf_rd_r=5NT6P0JEEF5M1D54VA33&pd_rd_wg=zpbM7&pd_rd_r=0a387300-51a2-456c-a162-76cf964835a9&pd_rd_i=B0DQLBTDCJ"

     # Setup Selenium Chrome driver with headless mode
    service = Service(ChromeDriverManager().install())                      
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")                  # ✅ Enable modern headless mode
    # options.add_argument("--disable-gpu")                   # Optional: better compatibility
    options.add_argument("--window-size=1920,1080")         # Optional: set full HD viewport

    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("----------------------------------- Amazon --------------------------------------")
        print("\n")
        print(f">>> Fetching URL: {query}")
        driver.get(query)
        time.sleep(5)  # Wait for page to load

        

        try:
            container = driver.find_element(By.ID, "ppd")
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
            product_name = soup.find_all(id="productTitle")[0].text
        except IndexError:
            product_name = soup.title.string or "Unknown Product"
        
        product_name = re.sub(r'\xa0+', ' ', product_name)

        # Extract product price
        try:
            product_price = soup.find_all(class_="a-price-whole")[0].text
        except IndexError:
            product_price = "N/A"

        # Extract pid from query string
        try:
            Product_id = query.split("/dp/")[1].split("/")[0]
        except IndexError:       
            Product_id = "N/A"

        # Remove commas from price for consistency
        product_name = " ".join(product_name.split())
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
                    product.pop("_id", None) # Remove MongoDB internal ID for cleaner output
                    product.pop("Product_id",None)  # Remove Product_id for cleaner output
                    return product
                else:
                    product.pop("_id", None) # Remove MongoDB internal ID for cleaner output
                    product.pop("Product_id",None) # Remove Product_id for cleaner output
                    return product
            except Exception as e:
                print(f"⚠️ MongoDB insert failed: {e}")    
    


handle_amazon()