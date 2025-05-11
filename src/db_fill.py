from src.db_manager import DBManager
from src.hh_api import HeadHunterAPI


def fill_companies_and_vacancies():
    """Заполняем таблицы companies и vacancies данными с HeadHunter."""
    db_manager = DBManager()

    # Создаем объект API
    hh_api = HeadHunterAPI()

    # Список идентификаторов компаний для запроса
    employer_ids = ['5004072', '5775464', '4748227', '36227', '3172102', '11388989', '3643187', '9066698', '10609539',
                    '988247']

    # Получаем компании и вакансии
    companies, vacancies = hh_api.get_companies_and_vacancies(employer_ids)

    # Заполняем таблицу companies
    for company in companies:
        query = """
            INSERT INTO companies (company_id, title, url)
            VALUES (%s, %s, %s)
            ON CONFLICT (company_id) DO NOTHING;  -- Вставляем данные, если такой компании еще нет
        """
        db_manager.cursor.execute(query, (
            company['company_id'],
            company['name'],
            company['url']
        ))

    # Заполняем таблицу vacancies
    for vacancy in vacancies:
        query = """
            INSERT INTO vacancies (title, salary, company_id, url)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO NOTHING;  -- Вставляем данные, если такая вакансия уже есть
        """
        db_manager.cursor.execute(query, (
            vacancy['title'],
            vacancy['salary'],
            vacancy['company_id'],
            vacancy['url']
        ))

    db_manager.connection.commit()  # Подтверждаем изменения
    db_manager.close()  # Закрываем соединение


if __name__ == "__main__":
    fill_companies_and_vacancies()
    print("Данные успешно загружены.")
