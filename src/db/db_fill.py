from src.db.db_manager import DBManager
from src.hh_api import get_companies_vacancies


def fill_companies_and_vacancies():
    """Заполняем таблицы companies и vacancies данными с HeadHunter."""
    db_manager = DBManager()
    companies, vacancies = get_companies_vacancies()

    # Заполняем таблицу companies
    for company in companies:
        query = """
            INSERT INTO companies (company_id, title, salary, url)
            VALUES (%s, %s, %s, %s);
        """
        db_manager.cursor.execute(query, (
            company['company_id'],
            company['title'],
            company['salary'],
            company['url']
        ))

    # Заполняем таблицу vacancies
    for vacancy in vacancies:
        query = """
            INSERT INTO vacancies (title, salary, company_id, url)
            VALUES (%s, %s, %s, %s);
        """
        db_manager.cursor.execute(query, (
            vacancy['title'],
            vacancy['salary'],
            vacancy['company_id'],
            vacancy['url']
        ))

    db_manager.connection.commit()
    db_manager.close()


if __name__ == "__main__":
    fill_companies_and_vacancies()
    print("Данные успешно загружены.")
