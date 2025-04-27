import psycopg2
from psycopg2 import sql
from utils.config import DB_CONFIG


def create_database():
    """Создание базы данных."""
    connection = psycopg2.connect(**DB_CONFIG)
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE headhunter_db;")
    connection.close()


def create_tables():
    """Создание таблиц в БД."""
    connection = psycopg2.connect(dbname="headhunter_db", **DB_CONFIG)
    cursor = connection.cursor()

    # Создание таблицы companies
    cursor.execute("""
        CREATE TABLE companies (
            id SERIAL PRIMARY KEY,
            company_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            salary INTEGER,
            url TEXT
        );
    """)

    # Создание таблицы vacancies
    cursor.execute("""
        CREATE TABLE vacancies (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            salary INTEGER,
            company_id INTEGER,
            url VARCHAR(255),
            FOREIGN KEY (company_id) REFERENCES companies(id)
        );
    """)

    connection.commit()
    connection.close()
