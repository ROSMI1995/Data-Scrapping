import csv
from bs4 import BeautifulSoup
import requests


base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1_{}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

product_url = []
product_name = []
product_price = []
rating = []
number_reviews = []

start_page = 1
end_page = 25

for page in range(start_page, end_page + 1):
    url = base_url.format(page)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find_all('div', class_='sg-col-inner')

    for result in results:
        link_element = result.find('a',
                                   class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
        if link_element:
            product_name.append(link_element.text.strip())
            product_url.append('https://www.amazon.in' + link_element['href'])

            price_element = result.find('span', class_='a-price-whole')
            if price_element:
                product_price.append(price_element.text.strip())
            else:
                product_price.append("N/A")

            rating_element = result.find('span', class_='a-icon-alt')
            if rating_element:
                rating.append(rating_element.text.strip())
            else:
                rating.append("N/A")

            num_reviews_element = result.find('span', class_='a-size-base s-underline-text')
            if num_reviews_element:
                number_reviews.append(num_reviews_element.text.strip())
            else:
                number_reviews.append("N/A")

# Combine and filter unique data
unique_data = set(zip(product_name, product_price, product_url, rating, number_reviews))
filtered_data = filter(lambda x: all(x) and x[0] != '' and x[1] != '' and x[2] != '', unique_data)

file_name = 'Amazon_data.csv'
with open(file_name, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Sl. No', 'Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews'])

    for i, data in enumerate(filtered_data, start=1):
        product_name, product_price, product_url, rating, number_reviews = data
        writer.writerow([i, product_url, product_name, product_price, rating, number_reviews])

print("Product details saved in CSV format.")
