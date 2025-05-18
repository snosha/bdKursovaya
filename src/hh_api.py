import requests
import time
from typing import List, Dict, Optional


class HeadHunterAPI:
    BASE_URL = "https://api.hh.ru"

    def __init__(self, delay: float = 0.3):
        self.delay = delay

    def get_employer_info(self, employer_id: str) -> Optional[Dict]:
        """Получить информацию о работодателе"""
        url = f"{self.BASE_URL}/employers/{employer_id}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Ошибка при получении работодателя {employer_id}")
            return None
        return response.json()

    def get_vacancies(self, employer_id: str) -> List[Dict]:
        """Получить список вакансий работодателя"""
        url = f"{self.BASE_URL}/vacancies?employer_id={employer_id}&per_page=100"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Ошибка при получении вакансий для {employer_id}")
            return []
        return response.json().get('items', [])

    def get_companies_and_vacancies(self, employer_ids: List[str]) -> tuple[List[Dict], List[Dict]]:
        """Получить информацию по всем компаниям и их вакансиям"""
        companies = []
        vacancies = []

        for employer_id in employer_ids:
            # Получаем информацию о работодателе
            employer = self.get_employer_info(employer_id)
            if employer:
                companies.append({
                    'company_id': employer['id'],
                    'name': employer['name'],
                    'url': employer.get('alternate_url', ''),
                })

            # Получаем вакансии для работодателя
            vacancy_items = self.get_vacancies(employer_id)
            for vacancy in vacancy_items:
                vacancies.append({
                    'title': vacancy['name'],
                    'salary': vacancy['salary']['from'] if vacancy['salary'] else None,
                    'company_id': employer_id,
                    'url': vacancy.get('alternate_url', '')
                })

            # Задержка, чтобы избежать спама API
            time.sleep(self.delay)

        return companies, vacancies
