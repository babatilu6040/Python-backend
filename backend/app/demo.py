from urllib.parse import urlparse

def check_site(url):
    sites = ["flipkart", "amazon", "meesho"]  # add more if needed
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()  # domain part of the URL

    for site in sites:
        if site in domain:
            return f"{site.capitalize()} found in URL"
    return "No match found"

# Test cases
urls = [
    "https://www.flispkart.com/some-product",
    "https://www.amsazon.in/gp/product/B0XYZ",
    "https://www.meessho.com/category/xyz",
    "https://www.ebay.com/item/123"
]

for u in urls:
    print(u, "->", check_site(u))
