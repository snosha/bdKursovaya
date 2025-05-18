from hh_api import HeadHunterAPI
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


def insert_vacancies(company_id: int):
    """Получаем вакансии для компании и вставляем в базу данных"""
    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies(company_id)

    connection = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    cursor = connection.cursor()

    for vacancy in vacancies:
        # Извлекаем данные вакансии
        vacancy_id = vacancy["id"]
        vacancy_name = vacancy["name"]
        salary_from = vacancy["salary"]["from"] if vacancy["salary"] else None
        salary_to = vacancy["salary"]["to"] if vacancy["salary"] else None
        salary_currency = vacancy["salary"]["currency"] if vacancy["salary"] else None
        vacancy_url = vacancy["alternate_url"]

        cursor.execute(
            """
            INSERT INTO vacancies (vacancy_id, company_id, vacancy_name, salary_from, salary_to, salary_currency, vacancy_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO NOTHING
            """,
            (vacancy_id, company_id, vacancy_name, salary_from, salary_to, salary_currency, vacancy_url)
        )

    connection.commit()
    cursor.close()
    connection.close()
