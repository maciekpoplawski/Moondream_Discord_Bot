import json
import sqlite3
from datetime import datetime


def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_from_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def insert_interaction(user_id, image_path, question, answer):
    conn = sqlite3.connect('bot_interactions.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO interactions (user_id, image_path, question, answer, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, image_path, question, answer, timestamp))
    conn.commit()
    conn.close()
