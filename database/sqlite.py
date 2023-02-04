import sqlite3

db = sqlite3.connect('bot.db')
cur = db.cursor()


async def connect() -> None:
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER NOT NULL UNIQUE,
    street TEXT NOT NULL,
    el_o INTEGER NULL,
    el_d INTEGER NULL,
    el_n INTEGER NULL,
    hvs INTEGER NULL,
    gvs INTEGER NULL)
    """)
    db.commit()


async def status(user_id):
    stat = cur.execute("""SELECT * FROM users WHERE user_id=?""", (user_id,)).fetchone()
    return stat


async def all_users():
    stat = cur.execute("""SELECT user_id FROM users""").fetchall()
    return stat


async def register(user_id, data):
    if data.get('info') == 'sin':
        cur.execute("""INSERT INTO users (user_id, street) VALUES (?, ?) """, (user_id, 'Синопская'))
        db.commit()

    elif data.get('info') == 'fas':
        cur.execute("""INSERT INTO users (user_id, street) VALUES (?, ?) """, (user_id, 'Фасоль'))
        db.commit()

    elif data.get('info') == 'lif':
        cur.execute("""INSERT INTO users (user_id, street) VALUES (?, ?) """, (user_id, 'Лифляндская'))
        db.commit()

    elif data.get('info') == 'rk':
        cur.execute("""INSERT INTO users (user_id, street) VALUES (?, ?) """,
                    (user_id, 'Римского-Корсакова'))
        db.commit()

    elif data.get('info') == 'st':
        cur.execute("""INSERT INTO users (user_id, street) VALUES (?, ?) """, (user_id, 'Стачек'))
        db.commit()


async def cur_status(message):
    stat = cur.execute("""SELECT street FROM users WHERE user_id=?""", (message.chat.id,)).fetchone()
    return stat


async def approve_RC(message, cost):
    cur.execute("""UPDATE users SET el_o=? WHERE user_id=?""", (cost, message.chat.id))
    db.commit()


async def approve_LIF(message, cost):
    cur.execute("""UPDATE users SET el_o=? WHERE user_id=?""", (cost, message.chat.id))
    db.commit()


async def approve_FAS(message, cost1, cost2):
    cur.execute("""UPDATE users SET el_d=?, el_n=? WHERE user_id=?""", (cost1, cost2, message.chat.id))
    db.commit()


async def approve_ST(message, cost1, cost2):
    cur.execute("""UPDATE users SET el_d=?, el_n=? WHERE user_id=?""", (cost1, cost2, message.chat.id))
    db.commit()


async def approve_SIN(message, cost1, cost2, cost3):
    cur.execute("""UPDATE users SET el_o=?, hvs=?, gvs=? WHERE user_id=?""", (cost1, cost2, cost3, message.chat.id))
    db.commit()
