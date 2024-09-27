import sqlite3 as sq

db = sq.connect('tasks.db')
cur = db.cursor()

async def db_start():
    global cur, db

    # Создаем таблицу, если ее нет
    cur.execute("CREATE TABLE IF NOT EXISTS profile (user_id TEXT, crypto_name TEXT, crypto_price TEXT, PRIMARY KEY (user_id, crypto_name))")
    db.commit()

async def create_profile(user_id):
    # Проверяем, есть ли уже профиль
    user = cur.execute("SELECT 1 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
    if not user:
        # Вставляем новый профиль
        cur.execute("INSERT INTO profile (user_id) VALUES (?)", (user_id,))
        db.commit()

async def add_task(user_id, crypto_name, crypto_price):
    # Добавляем новую задачу в таблицу для конкретного пользователя
    cur.execute("UPDATE profile SET crypto_name = ?, crypto_price = ? WHERE user_id = ?",
                (crypto_name, crypto_price, user_id))
    db.commit()
