import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('tasks.db')

cur = conn.cursor()

# Создаем таблицу, если она еще не существует
cur.execute('''  
CREATE TABLE IF NOT EXISTS tasks (  
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,  
    user_id INTEGER,  
    currency TEXT NOT NULL,  
    price TEXT,  
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)  
''')

# Функция для добавления новой задачи
def ent_info_db(user_id, currency, price):
    cur.execute('INSERT INTO tasks (user_id, currency, price) VALUES (?, ?, ?)', (user_id, currency, price))
    # Сохраняем изменения
    conn.commit()

def give_tasks(user_id):
    cur.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
    tasks = cur.fetchall()  # Получаем все результаты запроса
    return tasks  # Возвращаем список задач