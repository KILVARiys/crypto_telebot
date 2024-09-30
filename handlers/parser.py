import requests
import sqlite3
from bs4 import BeautifulSoup
import asyncio

# Подключение к базе данных SQLite
connection = sqlite3.connect('tasks.db')
cur = connection.cursor()

# Функция для получения цены криптовалюты
def check_price_coin(currency):
    price = None
    try:
        html_resp = requests.get('https://cryptorank.io').text
        block = BeautifulSoup(html_resp, 'lxml')
        rows = block.find_all('tr', class_='sc-a321a998-0 QrTwc init-scroll')

        if currency == 'coin_btc':
            price = rows[0].find_all('p', class_='sc-b7cd6de0-0 sc-28f598be-1 tEDJi nZrBG')[0].text.strip()
        elif currency == 'coin_eth':
            price = rows[1].find_all('p', class_='sc-b7cd6de0-0 sc-28f598be-1 tEDJi nZrBG')[0].text.strip()
        elif currency == 'coin_ltc':
            ltc_resp = requests.get('https://cryptorank.io/price/litecoin').text
            check = BeautifulSoup(ltc_resp, 'lxml')
            price = check.find_all('div', class_='sc-cb748c3-0 cwWsJH')[0].text.strip()
    except Exception as e:
        print(f"Ошибка при получении цены для {currency}: {e}")

    return price

# Функция для извлечения данных из базы данных
def get_coins_from_db():
    cur.execute("SELECT currency, price FROM tasks")
    return {row[0]: row[1] for row in cur.fetchall()}

async def check_coin_balance(bot, user_id):
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
                        result_message = f"Условия для [{currency}] были соблюдены\n Нынешняя цена: {coin_dict[currency]}"
                        await send_notify(bot, result_message)  # Здесь передаем объект бота
                except ValueError as ve:
                    print(f"Ошибка преобразования цены для {currency}: {ve}")

        await asyncio.sleep(20)


async def send_notify(bot, message):
    cur.execute("SELECT user_id FROM tasks")
    user_ids = cur.fetchall()

    for row in user_ids:
        user_id = row[0]
        try:
            await bot.send_message(chat_id=user_id, text=message)  # Передаем user_id как chat_id
            print(f"Уведомление отправлено пользователю {user_id}: {message}")  # Отладка
        except Exception as e:
            print(f"Ошибка отправки сообщения пользователю {user_id}: {e}")

