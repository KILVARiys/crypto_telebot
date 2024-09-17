import requests
from bs4 import BeautifulSoup

def get_crypto_price(coins):
    result = {}
    html_resp = requests.get('https://cryptorank.io/ru').text
    block = BeautifulSoup(html_resp, 'lxml')
    rows = block.find_all('tr', class_='sc-a321a998-0 QrTwc init-scroll')

    for row in rows:
        ticker = row.find('span', class_='sc-b7cd6de0-0 eJnMXZ')
        if ticker:
            ticker = ticker.text.strip().lower()

            if ticker in coins:
                price = row.find('td', class_='sc-4b43e9a5-0 gORhsl sc-28f598be-0 hlJJZE')

def check_coins_balance():
    while True:
        coins =