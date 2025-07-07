import pandas as pd
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '', 
    'database': 'sarbtm_db'
}

PRICE_CSV = 'sarbtm_price_history.csv'
NEWS_CSV = 'sarbtm_news.csv'

def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(" Connection error:", e)
        return None

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Date DATE,
            LTP FLOAT,
            Open FLOAT,
            High FLOAT,
            Low FLOAT,
            Volume BIGINT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Date DATE,
            Headline TEXT,
            Source VARCHAR(255)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

def insert_price_data():
    df = pd.read_csv(PRICE_CSV)
    df.fillna(0, inplace=True)

    conn = connect_db()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO price_history (Date, LTP, Open, High, Low, Volume)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, tuple(row))

    conn.commit()
    cursor.close()
    conn.close()

def insert_news_data():
    df = pd.read_csv(NEWS_CSV)
    df.fillna('', inplace=True)

    conn = connect_db()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO news (Date, Headline, Source)
            VALUES (%s, %s, %s)
        """, tuple(row))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    create_tables()
    insert_price_data()
    insert_news_data()
    print("Data inserted into XAMPP MySQL successfully!")
