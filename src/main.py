from db_fill import fill_companies, fill_vacancies
from db_manager import DBManager

if __name__ == '__main__':
    # Заполнение таблиц
    fill_companies()
    fill_vacancies()

    # Пример использования DBManager
    db_manager = DBManager()

    print("Все вакансии:")
    for vacancy in db_manager.get_all_vacancies():
        print(vacancy)

    print("\nВакансии с зарплатой выше средней:")
    for vacancy in db_manager.get_vacancies_with_higher_salary():
        print(vacancy)

    print("\nВсе компании и количество вакансий:")
    for company in db_manager.get_companies_and_vacancies_count():
        print(company)

    db_manager.close()
