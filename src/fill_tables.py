from hh_api import HeadHunterAPI
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def insert_companies():
    """Добавление компаний в таблицу companies через API"""
    hh_api = HeadHunterAPI()
    company_ids = [
        '5004072', '5775464', '4748227', '36227', '3172102',
        '11388989', '3643187', '9066698', '10609539', '988247'
    ]

    companies, _ = hh_api.get_companies_and_vacancies(company_ids)  # Получаем данные о компаниях

    connection = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cursor = connection.cursor()

    for company in companies:
        cursor.execute(
            """
            INSERT INTO companies (company_id, company_name, url)
            VALUES (%s, %s, %s)
            ON CONFLICT (company_id) DO NOTHING
            """,
            (company['company_id'], company['name'], company['url'])
        )

    connection.commit()
    cursor.close()
    connection.close()


def insert_vacancies():
    """Добавление вакансий в таблицу vacancies через API"""
    hh_api = HeadHunterAPI()  # Создаем экземпляр API
    company_ids = [
        '5004072', '5775464', '4748227', '36227', '3172102',
        '11388989', '3643187', '9066698', '10609539', '988247'
    ]

    _, vacancies = hh_api.get_companies_and_vacancies(company_ids)  # Получаем вакансии

    connection = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cursor = connection.cursor()

    for vacancy in vacancies:
        cursor.execute(
            """
            INSERT INTO vacancies (vacancy_id, company_id, vacancy_name, salary_from, salary_to, salary_currency, vacancy_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO NOTHING
            """,
            (vacancy['vacancy_id'], vacancy['company_id'], vacancy['title'],
             vacancy['salary_from'], vacancy['salary_to'], vacancy['salary_currency'], vacancy['url'])
        )

    connection.commit()
    cursor.close()
    connection.close()

# Функция для добавления данных в обе таблицы


def fill_tables():
    insert_companies()
    insert_vacancies()
