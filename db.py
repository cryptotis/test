import sqlite3


conn = sqlite3.connect("users_info.db")
cursor = conn.cursor()

def add_user(user_info) -> None:
    """Добавляем имя и телефон пользователя в БД"""
    name = user_info.name if user_info.name else "Без имени"
    phone = user_info.phone
    cursor.execute(f"INSERT INTO `users` (`u_name`, `u_phone`) VALUES (?, ?)", (name, phone))
    conn.commit()


def _init_db():
    """Инициализирует БД"""
    with open("createtable.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='users'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()

check_db_exists()
