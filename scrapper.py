import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import json

def scrape_coin_data():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    url = 'https://coinmarketcap.com/'
    driver.get(url)

    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cmc-table')))

    wait.until_not(EC.visibility_of_element_located((By.CLASS_NAME, 'loader')))

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    coin_data = []

    table = soup.find('table', class_='cmc-table')
    rows = table.find_all('tr')
    try:
        for row in rows[1:]:
            columns = row.find_all('td')
            name = columns[2].text.strip()
            price = columns[3].text.strip()
            one_hour_change = columns[4].text.strip()
            twenty_four_hour_change = columns[5].text.strip()
            seven_day_change = columns[6].text.strip()
            market_cap = columns[7].text.strip()
            volume_24h = columns[8].text.strip()
            circulating_supply = columns[9].text.strip()

            coin_data.append({
                'name': name,
                'price': price,
                'one_hour_change': one_hour_change,
                'twenty_four_hour_change': twenty_four_hour_change,
                'seven_day_change': seven_day_change,
                'market_cap': market_cap,
                'volume_24h': volume_24h,
                'circulating_supply': circulating_supply
            })
    except:
        pass
    driver.quit()
    return coin_data

def send_data_to_django(data):
    django_url = 'http://127.0.0.1:8000/receive-data'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(django_url, json=data, headers=headers)
    print(response.text)

if __name__ == '__main__':
    while True:
        coin_data = scrape_coin_data()
        send_data_to_django(coin_data)
        time.sleep(1)
