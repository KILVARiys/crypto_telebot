import requests
import sqlite3
from bs4 import BeautifulSoup
import asyncio

# Подключение к базе данных SQLite
connection = sqlite3.connect('tasks.db')
cur = connection.cursor()

# Функция для получения цены криптовалюты
def check_price_coin(crypto_name):
    price = None
    try:
        html_resp = requests.get('https://cryptorank.io').text
        block = BeautifulSoup(html_resp, 'lxml')
        rows = block.find_all('tr', class_='sc-a321a998-0 QrTwc init-scroll')

        if crypto_name == 'coin_btc':
            price = rows[0].find_all('p', class_='sc-b7cd6de0-0 sc-28f598be-1 tEDJi nZrBG')[0].text.strip()
        elif crypto_name == 'coin_eth':
            price = rows[1].find_all('p', class_='sc-b7cd6de0-0 sc-28f598be-1 tEDJi nZrBG')[0].text.strip()
        elif crypto_name == 'coin_ltc':
            ltc_resp = requests.get('https://cryptorank.io/price/litecoin').text
            check = BeautifulSoup(ltc_resp, 'lxml')
            price = check.find_all('div', class_='sc-cb748c3-0 cwWsJH')[0].text.strip()
    except Exception as e:
        print(f"Ошибка при получении цены для {crypto_name}: {e}")

    return price

# Функция для извлечения данных из базы данных
def get_coins_from_db():
    cur.execute("SELECT currency, price FROM tasks")
    return {row[0]: row[1] for row in cur.fetchall()}

async def check_coin_balance(bot):
    while True:
        coins = get_coins_from_db()
        coin_dict = {currency: check_price_coin(currency) for currency in coins.keys()}

        # Если цена соответствует, отправляем уведомление
        for currency, price in coins.items():
            if currency in coin_dict and coin_dict[currency] is not None:
                try:
                    current_price = float(coin_dict[currency].replace('$', '').replace(',', ''))
                    print(f"Текущая цена {currency}: {current_price}, Условия: {current_price <= float(price)}")  # Отладка
                    if current_price <= float(price):
                        await send_notify(bot, f"[{currency}] - buy\nprice: {coin_dict[currency]}")
                except ValueError as ve:
                    print(f"Ошибка преобразования цены для {currency}: {ve}")

        await asyncio.sleep(20)

async def send_notify(bot, message):
    cur.execute("SELECT user_id FROM tasks")
    user_ids = cur.fetchall()

    for row in user_ids:
        user_id = row[0]
        try:
            await bot.send_message(chat_id=user_id, text=message)
            print(f"Уведомление отправлено пользователю {user_id}: {message}")  # Отладка
        except Exception as e:
            print(f"Ошибка отправки сообщения пользователю {user_id}: {e}")
