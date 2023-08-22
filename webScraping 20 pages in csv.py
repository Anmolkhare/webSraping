import requests
from bs4 import BeautifulSoup
import csv

base_url = "https://www.amazon.in"
search_query = "bags"
total_pages = 20


csv_file = open("amazon_products.csv", "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"])

for page_number in range(1, total_pages + 1):
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
        else:
            continue
        
        product_name_elem = product.find("span", class_="a-text-normal")
        if product_name_elem:
            product_name = product_name_elem.text.strip()
        else:
            product_name = "N/A"
        
        price_elem = product.find("span", class_="a-price")
        if price_elem:
            product_price = price_elem.find("span", class_="a-offscreen").text.strip()
        else:
            product_price = "N/A"
        
        rating_elem = product.find("span", class_="a-icon-alt")
        if rating_elem:
            product_rating = rating_elem.text.strip()
        else:
            product_rating = "N/A"
        
        reviews_count_elem = product.find("span", class_="a-size-base")
        if reviews_count_elem:
            reviews_count = reviews_count_elem.text.strip()
        else:
            reviews_count = "N/A"
        
       
        csv_writer.writerow([product_url, product_name, product_price, product_rating, reviews_count])


csv_file.close()
print("CSV file 'amazon_products.csv' created successfully.")
