import sqlite3

conn = sqlite3.connect('tasks.db')

cur = conn.cursor()

# Создаем таблицы
cur.execute('''  
CREATE TABLE IF NOT EXISTS tasks (  
    task_id INTEGER PRIMARY KEY,  
    user_id INTEGER,  
    currency TEXT NOT NULL,  
    FOREIGN KEY (user_id) REFERENCES users (user_id)  
)  
''')
def ent_info_db(user_id, task_id, currency, price):
    cur.execute('INSERT INTO tasks (task_id, user_id, currency, price) VALUES (?, ?, ?, ?)', (task_id, user_id, currency, price))

# Сохраняем изменения
conn.commit()

# Выполняем запрос для получения задач пользователя с user_id = 1
def give_tasks(user_id):
    cur.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))