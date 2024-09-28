import time
import requests
import sqlite3
from bs4 import BeautifulSoup

async def send_notify(message):
    await message.answer(text=message)

# Подключение к базе данных SQLite
connection = sqlite3.connect('tasks.db')
cur = connection.cursor()

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

# Функция для извлечения данных из базы данных
def get_coins_from_db():
    cur.execute("SELECT currency, price FROM tasks")
    return {row[0]: row[1] for row in cur.fetchall()}

# Если цена достигает цели, отправляем уведомление в телегу

while True:
    coins = get_coins_from_db()  # Получаем данные о криптовалютах из БД
    coin_dict = {name: check_price_coin(name) for name in coins.keys()}  # Получаем текущие цены криптовалют

    # Если цена соответствует, отправляем уведомление
    for name, target_price in coins.items():
        if name in coin_dict and coin_dict[name] is not None:
            current_price = float(coin_dict[name].replace('$', '').replace(',', ''))  # Преобразуем текущую цену в float
            if current_price <= float(target_price):
                send_notify(f"[{name}] - buy, price: {coin_dict[name]}")

    time.sleep(20)