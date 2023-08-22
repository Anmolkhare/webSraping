import requests
from bs4 import BeautifulSoup

base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
search_query = "bags"
total_pages = 20

for page_number in range(1, total_pages + 1):
    params = {
        "k": search_query,
        "page": page_number
    }
    
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")
    
    products = soup.find_all("div", class_="s-result-item")
    
    for product in products:
        product_url_elem = product.find("a", class_="a-link-normal")
        if product_url_elem:
            product_url = product_url_elem.get("href")
        else:
            continue  
        
        product_name_elem = product.find("span", class_="a-text-normal")
        if product_name_elem:
            product_name = product_name_elem.text
        else:
            product_name = "N/A"
        
        price_elem = product.find("span", class_="a-price")
        if price_elem:
            product_price = price_elem.find("span", class_="a-offscreen").text
        else:
            product_price = "N/A"
        
        rating_elem = product.find("span", class_="a-icon-alt")
        if rating_elem:
            product_rating = rating_elem.text
        else:
            product_rating = "N/A"
        
        reviews_count_elem = product.find("span", class_="a-size-base")
        if reviews_count_elem:
            reviews_count = reviews_count_elem.text
        else:
            reviews_count = "N/A"
        
        print("Product URL:", product_url)
        print("Product Name:", product_name)
        print("Product Price:", product_price)
        print("Rating:", product_rating)
        print("Number of Reviews:", reviews_count)
        print("=" * 50)
