import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
# from . import data_store

executed = False  # Global flag to avoid double execution

def fetch_data_from_query(query):
    global executed
    if executed:
        print(">>> fetch_data_from_query() has already run. Skipping...")
        return
    executed = True

    print(">>> Starting product data fetch...")

    # Setup Selenium Chrome driver with headless mode
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")         # ✅ Enable modern headless mode
    options.add_argument("--disable-gpu")           # Optional: better compatibility
    options.add_argument("--window-size=1920,1080") # Optional: set full HD viewport

    driver = webdriver.Chrome(service=service, options=options)

    try:
        print(f">>> Fetching URL: {query}")
        driver.get(query)
        time.sleep(5)

        # Close any popup if exists
        try:
            element = driver.find_element(By.CLASS_NAME, "_30XB9F")
            element.click()
            print(">>> Popup closed.")
        except NoSuchElementException:
            print(">>> No popup found.")

        # Parse the HTML
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

        print(f">>> Product Name: {product_name}")
        print(f">>> Product Price: {product_price}")

        # Save product details
        product_details = {
            "Name": product_name,
            "price": product_price,
            "url": query
        }

        print(">>> Inserting product into database...")
        # data_store.data_insert(product_details)

    finally:
        driver.quit()
        print(">>> Browser closed.")
