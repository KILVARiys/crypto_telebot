import requests
import sqlite3
from bs4 import BeautifulSoup
import asyncio

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
    try:
        if crypto_name == 'coin_btc':
            price = rows[0].findAll('p', class_='sc-b7cd6de0-0 sc-28f598be-1 tEDJi nZrBG')[0].text.strip()
        elif crypto_name == 'coin_eth':
            price = rows[1].findAll('p', class_='sc-b7cd6de0-0 sc-28f598be-1 tEDJi nZrBG')[0].text.strip()
        elif crypto_name == 'coin_ltc':
            ltc_resp = requests.get('https://cryptorank.io/price/litecoin').text
            check = BeautifulSoup(ltc_resp, 'lxml')
            price = check.findAll('div', class_='sc-cb748c3-0 cwWsJH')[0].text.strip()
    except Exception as e:
        print(f"Ошибка при получении цены для {crypto_name}: {e}")

    return price

# Функция для извлечения данных из базы данных
def get_coins_from_db():
    cur.execute("SELECT currency, price FROM tasks")
    return {row[0]: row[1] for row in cur.fetchall()}

async def check_coin_balance(bot):
    while True:
        coins = get_coins_from_db()  # Получаем данные о криптовалютах из БД
        coin_dict = await asyncio.gather(*(check_price_coin(currency) for currency in coins.keys()))  # Получаем текущие цены криптовалют
        # Если цена соответствует, отправляем уведомление
        for currency, price in coins.items():
            if currency in coin_dict and coin_dict[currency] is not None:
                current_price = float(coin_dict[currency].replace('$', '').replace(',', ''))  # Преобразуем текущую цену в float
                if current_price <= float(price):
                    await send_notify(bot, f"[{currency}] - buy\nprice: {coin_dict[currency]}")

        await asyncio.sleep(20)  # Не блокируем поток

async def send_notify(bot, message):
    cur.execute("SELECT user_id FROM tasks")
    user_ids = cur.fetchall()  # Получаем все user_id из базы данных

    for row in user_ids:
        user_id = row[0]
        await bot.send_message(chat_id=user_id, text=message)  # Используем метод send_message объекта bot
