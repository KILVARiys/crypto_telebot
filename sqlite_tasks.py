import sqlite3

conn = sqlite3.connect('tasks.db')

cur = conn.cursor()

# Создаем таблицы
cur.execute('''  
CREATE TABLE IF NOT EXISTS users (  
    user_id INTEGER PRIMARY KEY,  
    user_name TEXT NOT NULL  
)  
''')

cur.execute('''  
CREATE TABLE IF NOT EXISTS tasks (  
    task_id INTEGER PRIMARY KEY,  
    user_id INTEGER,  
    currency TEXT NOT NULL,  
    FOREIGN KEY (user_id) REFERENCES users (user_id)  
)  
''')
async def ent_info_db(user_id, task_id, currency):
    cur.execute('INSERT INTO tasks (task_id, user_id, currency) VALUES (?, ?, ?)', (task_id, user_id, currency))

# Сохраняем изменения
conn.commit()

# Выполняем запрос для получения задач пользователя с user_id = 1
async def give_tasks(user_id):
    cur.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))