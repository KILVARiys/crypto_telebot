import requests
from bs4 import BeautifulSoup

# Получаем html-ответ от сайта
html_resp = requests.get('https://cryptorank.io').text
block = BeautifulSoup(html_resp, 'lxml')
# Находим строки с ценами криптовалют
rows = block.find_all('tr', class_='sc-a321a998-0 QrTwc init-scroll')


# Функция для получения цены криптовалюты
def check_price_coin(crypto_name):
    price = None  # Устанавливаем price по умолчанию как None
    if crypto_name == 'coin_btc':
        price = rows[0].findAll('p', class_='sc-b7cd6de0-0 sc-28f598be-1 tEDJi nZrBG')[0].text.strip()
    elif crypto_name == 'coin_eth':
        price = rows[1].findAll('p', class_='sc-b7cd6de0-0 sc-28f598be-1 tEDJi nZrBG')[0].text.strip()
    elif crypto_name == 'coin_ltc':
        ltc_resp = requests.get('https://cryptorank.io/price/litecoin').text
        check = BeautifulSoup(ltc_resp, 'lxml')
        price = check.findAll('div', class_='sc-cb748c3-0 cwWsJH')[0].text.strip()

    return price