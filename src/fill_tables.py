import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def insert_companies():
    """Добавление 10 компаний в таблицу companies"""
    connection = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cursor = connection.cursor()

    companies = [
        (80, 'Яндекс'),
        (15478, 'Сбербанк'),
        (2748, 'Тинькофф'),
        (78638, 'VK'),
        (3529, 'Альфа-Банк'),
        (3776, 'Почта России'),
        (39305, 'OZON'),
        (907345, 'Wildberries'),
        (1122462, 'Лаборатория Касперского'),
        (2180, 'РЖД')
    ]

    for company_id, company_name in companies:
        cursor.execute(
            """
            INSERT INTO companies (company_id, company_name)
            VALUES (%s, %s)
            ON CONFLICT (company_id) DO NOTHING
            """,
            (company_id, company_name)
        )

    connection.commit()
    cursor.close()
    connection.close()
