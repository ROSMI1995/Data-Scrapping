import pandas as pd
from bs4 import BeautifulSoup
import requests


base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1_{}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

product_urls = []
product_data = []

start_page = 1
end_page = 5

for page in range(start_page, end_page + 1):
    url = base_url.format(page)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find_all('div', class_='sg-col-inner')

    for result in results:
        link_element = result.find('a',
                                   class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
        if link_element:
            product_url = 'https://www.amazon.in' + link_element['href']
            product_urls.append(product_url)

# Visit each product URL and extract additional information
for url in product_urls:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    asin_element = soup.find('span', string='ASIN')
    if asin_element:
        asin = asin_element.find_next('span').text.strip()
    else:
        asin = ''

    description_element = soup.find('div', id='productDescription')
    if description_element:
        description = description_element.text.strip()
    else:
        description = ''

    manufacturer_element = soup.find('div', id='bylineInfo')
    if manufacturer_element:
        manufacturer = manufacturer_element.get_text(strip=True)
    else:
        manufacturer = ''

    product_data.append({
        'Product URL': url,
        'ASIN': asin,
        'Description': description,
        'Manufacturer': manufacturer
    })

# Create a DataFrame from the product data
df = pd.DataFrame(product_data)

# Reorder the columns
df = df[['Product URL', 'ASIN', 'Description', 'Manufacturer']]

# Save the DataFrame to a CSV file
file_name = 'Amazon_data.csv'
df.to_csv(file_name, index=False)

print("Product details saved in CSV format.")
