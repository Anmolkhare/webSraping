import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://www.amazon.in"
search_query = "bags"
total_products = 200
products_per_page = 48  
current_product_count = 0
product_links = []

while current_product_count < total_products:
    page_number = (current_product_count // products_per_page) + 1
    params = {
        "k": search_query,
        "page": page_number
    }
    response = requests.get(base_url + "/s", params=params)
    soup = BeautifulSoup(response.content, "html.parser")
    products = soup.find_all("div", class_="s-result-item")
    for product in products:
        product_url_elem = product.find("a", class_="a-link-normal")
        if product_url_elem:
            product_url = base_url + product_url_elem.get("href")
            product_links.append(product_url)
            current_product_count += 1
            if current_product_count >= total_products:
                break
    
    if current_product_count >= total_products:
        break


csv_file = open("amazon_products.csv", "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Product URL", "Description", "ASIN", "Product Description", "Manufacturer"])

for product_url in product_links:
    response = requests.get(product_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    description_elem = soup.find("div", id="productDescription")
    description = description_elem.get_text(separator="\n").strip() if description_elem else "N/A"
    
    asin_elem = soup.find("th", text="ASIN")
    asin = asin_elem.find_next("td").text.strip() if asin_elem else "N/A"
    
    product_description_elem = soup.find("h1", class_="a-size-large")
    product_description = product_description_elem.text.strip() if product_description_elem else "N/A"
    
    manufacturer_elem = soup.find("a", id="bylineInfo")
    manufacturer = manufacturer_elem.text.strip() if manufacturer_elem else "N/A"
    
    csv_writer.writerow([product_url, description, asin, product_description, manufacturer])


csv_file.close()
print("CSV file 'amazon_products.csv' created successfully.")
