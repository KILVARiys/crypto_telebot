import sqlite3 as sq

# Создаем подключение к базе данных
db = sq.connect('users.db')
cur = db.cursor()

def db_start():
    # Создаем таблицу, если ее нет
    cur.execute("CREATE TABLE IF NOT EXISTS profile (user_id TEXT PRIMARY KEY, username TEXT)")
    db.commit()

def create_profile(user_id, username):
    # Проверяем, есть ли уже профиль
    user = cur.execute("SELECT 1 FROM profile WHERE user_id = ?", (user_id,)).fetchone()
    if not user:
        # Вставляем новый профиль
        cur.execute("INSERT INTO profile (user_id, username) VALUES (?, ?)", (user_id, username))
        db.commit()