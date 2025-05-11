import psycopg2
from src.db_config import DB_CONFIG


class DBManager:
    def __init__(self):

        self.connection = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.connection.cursor()


    def get_companies_and_vacancies_count(self):
        """Получить список всех компаний и количество вакансий у каждой компании."""
        query = """
            SELECT c.title, COUNT(v.id) 
            FROM companies c 
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.id;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        """Получить список всех вакансий с указанием названия компании, вакансии и зарплаты."""
        query = """
            SELECT v.title, v.salary, c.title, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """Получить среднюю зарплату по вакансиям."""
        query = "SELECT AVG(salary) FROM vacancies;"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Получить вакансии с зарплатой выше средней."""
        avg_salary = self.get_avg_salary()
        query = """
            SELECT v.title, v.salary, c.title, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE v.salary > %s;
        """
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получить вакансии, в названии которых встречается переданное слово."""
        query = """
            SELECT v.title, v.salary, c.title, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE v.title LIKE %s;
        """
        self.cursor.execute(query, ('%' + keyword + '%',))
        return self.cursor.fetchall()

    def close(self):
        """Закрыть соединение с базой данных."""
        self.connection.close()
