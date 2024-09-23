import sqlite3 as sq

async def db_start():
    global db, cur

    db = sq.connect('tasks.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, crypto_name TEXT, crypto_price TEXT)")
    db.commit()

async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?)", (user_id, '', ''))
        db.commit()

async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE profile WHERE user_id == '{}' SET crypto_name = '{}', crypto_price = '{}'".format(
            user_id, data['crypto_name'], data['crypto_price']
        ))
        db.commit()