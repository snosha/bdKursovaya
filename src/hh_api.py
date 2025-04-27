import requests

def get_companies_vacancies():
    companies = []
    vacancies = []

    company_ids = ['123', '456', '789']  # Попробуй использовать другие ID компаний

    for company_id in company_ids:
        url = f'https://api.hh.ru/vacancies?employer_id={company_id}'
        response = requests.get(url)
        data = response.json()

        # Выводим весь ответ для проверки
        print(f"Ответ от API для компании {company_id}: {data}")

        # Проверим, есть ли вакансии для данной компании
        if 'items' in data and data['items']:
            for vacancy in data['items']:
                vacancy_info = {
                    'title': vacancy['name'],
                    'salary': vacancy['salary']['from'] if vacancy['salary'] else None,
                    'company_id': company_id,
                    'url': vacancy['alternate_url']
                }
                vacancies.append(vacancy_info)

            # Добавим информацию о компании, если она присутствует
            if 'employer' in data:
                company_info = {
                    'company_id': company_id,
                    'title': data['employer']['name'],
                    'salary': data['employer'].get('salary', 'N/A'),
                    'url': data['employer'].get('site', 'N/A'),
                }
                companies.append(company_info)

    return companies, vacancies
