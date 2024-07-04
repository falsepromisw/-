import sqlite3

# Создание базы данных и таблицы
def create_database():
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        job_name TEXT,
        company TEXT,
        salary TEXT,
        experience TEXT,
        city TEXT,
        job_link TEXT
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()