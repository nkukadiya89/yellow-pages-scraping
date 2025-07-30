from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Setup headless Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

category = "restaurant"
city = "Toronto"
all_data = []
page = 1
max_pages = 10  # Limit to first 10 pages

while page <= max_pages:
    print(f"Scraping page {page}...")
    url = f"https://www.yellowpages.ca/search/si/{page}/{category}/{city}"
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', class_='listing__content__wrapper')

    if not results:
        print("No more results found.")
        break

    for result in results:
        name = result.find('a', class_='listing__name--link')
        name_text = name.get_text(strip=True) if name else ''

        # Address (fallback to both span/div)
        address_tag = result.find(['span', 'div'], class_='listing__address')
        address = address_tag.get_text(strip=True) if address_tag else ''

        # Phone number
        phone_tag = result.find('a', class_='mlr__item__cta jsMlrMenu')
        phone = phone_tag['data-phone'] if phone_tag and phone_tag.has_attr('data-phone') else ''

        # Ratings
        rating_span = result.find('span', class_='ypStars jsReviewsChart')
        rating = rating_span['title'].replace("Ratings: ", "").replace(" out of 5 stars", "") if rating_span and rating_span.has_attr('title') else 'N/A'

        # Review count
        review_count_tag = result.find('a', class_='listing__ratings__count listing__link')
        review_count = review_count_tag.text.strip("()") if review_count_tag else '0'

        all_data.append({
            'Restaurants Name': name_text,
            'Address': address,
            'Phone': phone,
            'Rating': rating,
            'Review Count': review_count
        })

    page += 1
    time.sleep(2)

driver.quit()

# Save to CSV
try:
    filename = f'{category}_{city}_businesses.csv'
    df = pd.DataFrame(all_data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f" Done! CSV file created successfully: {filename}")
except PermissionError:
    print(" Error: Please close the CSV file if it's already open and try again.")
