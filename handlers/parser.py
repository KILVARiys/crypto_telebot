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
    return cur.fetchall()  # Изменяем для возврата всех строк


async def check_coin_balance(bot):
    while True:
        coins = get_coins_from_db()  # Получаем список задач
        coin_dict = {currency: check_price_coin(currency) for currency, _ in coins}

        # Если цена соответствует, отправляем уведомление
        for index, (currency, price) in enumerate(coins):  # Изменяем для получения индекса
            if currency in coin_dict and coin_dict[currency] is not None:
                try:
                    current_price = float(coin_dict[currency].replace('$', '').replace(',', ''))
                    print(f"Текущая цена {currency}: {current_price}, Условия: {float(price) <= current_price}")  # Отладка
                    if float(price) <= current_price:
                        result_message = (f"Условия для [{currency}] были соблюдены \n Нынешняя цена: {coin_dict[currency]}")
                        await send_notify(bot, result_message, currency)  # Передаем также валюту для удаления
                except ValueError as ve:
                    print(f"Ошибка преобразования цены для {currency}: {ve}")
        await asyncio.sleep(10)


async def send_notify(bot, message, currency):
    cur.execute("SELECT user_id FROM tasks WHERE currency=?", (currency,))
    user_ids = cur.fetchall()

    for row in user_ids:
        user_id = row[0]
        try:
            await bot.send_message(chat_id=user_id, text=message)  # Передаем user_id как chat_id
            print(f"Уведомление отправлено пользователю {user_id}: {message}")  # Отладка

            # Удаляем задачу после отправки уведомления
            cur.execute("DELETE FROM tasks WHERE currency=?", (currency,))
            connection.commit()  # Сохраняем изменения в базе данных
            print(f"Задача для {currency} удалена из базы данных.")

        except Exception as e:
            print(f"Ошибка отправки сообщения пользователю {user_id}: {e}")

# Не забудьте закрыть соединение при завершении работы программы
# connection.close() в соответствующем месте вашего кода