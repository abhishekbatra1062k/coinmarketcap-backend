from playwright.sync_api import sync_playwright
import time
import requests

def scrape_coin_data(page):
    tr_selector = 'div.cmc-body-wrapper table tbody tr'
    tr_list = page.query_selector_all(tr_selector)
    coin_data = []
    for tr in tr_list:
        rank = tr.query_selector('td:nth-child(2) p').inner_text()
        name = tr.query_selector('td:nth-child(3) p').inner_text()
        symbol = tr.query_selector('td:nth-child(3) p[color = "text3"]').inner_text()
        price = tr.query_selector('td:nth-child(4) span').inner_text()
        perc1HrChange = tr.query_selector('td:nth-child(5) span').inner_text()
        perc24HrChange = tr.query_selector('td:nth-child(6) span').inner_text()
        perc7DayChange = tr.query_selector('td:nth-child(7) span').inner_text()
        marketCap = tr.query_selector('td:nth-child(8) p').inner_text()
        volume24Hr = tr.query_selector('td:nth-child(9) p').inner_text()
        circulatingSupply = tr.query_selector('td:nth-child(10) p').inner_text()
        coin_data.append({
            'rank': rank,
            'name': name,
            'price': price,
            'one_hour_change': perc1HrChange,
            'twenty_four_hour_change': perc24HrChange,
            'seven_day_change': perc7DayChange,
            'market_cap': marketCap,
            'volume_24h': volume24Hr,
            'circulating_supply': circulatingSupply
        })
    return coin_data

def send_data_to_django(data):
    django_url = 'http://127.0.0.1:8000/receive-data'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(django_url, json=data, headers=headers)
    print(response.text)

if __name__ == '__main__':
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        while True:
            page = browser.new_page()
            page.goto("https://coinmarketcap.com/")
            page.wait_for_timeout(2)

            for _ in range(5):
                page.mouse.wheel(0, 2000)
                page.wait_for_timeout(2)
                
            coin_data = scrape_coin_data(page)
            send_data_to_django(coin_data)
            time.sleep(5)