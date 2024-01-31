import sqlite3


def setup_database():
    conn = sqlite3.connect('bot_interactions.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            user_id TEXT,
            image_path TEXT,
            question TEXT,
            answer TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()


setup_database()
