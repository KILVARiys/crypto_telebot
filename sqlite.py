import sqlite3 as sq

db = sq.connect('tasks.db')
cur = db.cursor()

async def db_start():
    global cur, db

    # Создаем таблицу, если ее нет
    cur.execute("CREATE TABLE IF NOT EXISTS profile (user_id TEXT PRIMARY KEY, crypto_name TEXT, crypto_price TEXT)")
    db.commit()

async def create_profile(user_id):
    # Проверяем, есть ли уже профиль
    user = cur.execute("SELECT 1 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
    if not user:
        # Вставляем новый профиль
        cur.execute("INSERT INTO profile (user_id) VALUES (?)", (user_id,))
        db.commit()

async def add_task(crypto_name, crypto_price):
    # Добавляем новую задачу в таблицу (предполагается, что таблица уже существует)
    cur.execute("INSERT INTO profile (crypto_name, crypto_price) VALUES (?, ?)", (crypto_name, crypto_price))
    db.commit()
