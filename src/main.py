from create_tables import create_tables
from src.db_fill import fill_companies_and_vacancies
from src.db_manager import DBManager


if __name__ == '__main__':
    # Создание таблиц
    create_tables()

    # Заполнение таблиц
    fill_companies_and_vacancies()

    # Работа с базой данных
    db_manager = DBManager()

    # Получаем и выводим все вакансии
    print("Все вакансии:")
    for vacancy in db_manager.get_all_vacancies():
        print(vacancy)

    print("\nВакансии с зарплатой выше средней:")
    for vacancy in db_manager.get_vacancies_with_higher_salary():
        print(vacancy)

    print("\nВсе компании и количество вакансий:")
    for company in db_manager.get_companies_and_vacancies_count():
        print(company)

    # Закрываем соединение с базой данных
    db_manager.close()
