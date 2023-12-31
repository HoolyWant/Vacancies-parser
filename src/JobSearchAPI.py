from abc import ABC, abstractmethod
from requests import get, request
import json


class JobSearchAPI(ABC):
    """
    Абстрактный класс для классов
    по работе с API
    """
    @abstractmethod
    def get_vacancies(self, specialty):
        pass

    @abstractmethod
    def clear_vacancies_list(self, dirty_list):
        pass


class HeadHunterAPI(JobSearchAPI):
    vacancies_list = [] # Хранит отформатированные вакансии

    def get_vacancies(self, specialty: str):
        """
        Получает информацию о вакансиях по запросу
        :param specialty: запрос
        :return: вакансии
        """
        response = json.loads(get(f'https://api.hh.ru/vacancies?text='
                                  f'{specialty.lower()}&area=113').text)['items']
        return response

    def clear_vacancies_list(self, dirty_list: list):
        """
        Форматирует вакансии в удобочитаемом формате
        :param dirty_list: сырые вакансии с api
        :return: сохраняет в вакансии в списке , который является атрибутом класса
        """
        for item in dirty_list:
            clear_dict = {
                'name': item['name'],
                'url': item['alternate_url'],
                'area': item['area']['name']
            }
            try:
                pay_from = str(item['salary']['from'])
                pay_to = str(item['salary']['to'])
                pay_cur = str(item['salary']['currency'])
                if pay_to == 'None':
                    salary = 'От' + pay_from + ' ' + pay_cur
                elif pay_from == 'None':
                    salary = 'До ' + pay_to + ' ' + pay_cur
                else:
                    salary = 'От ' + pay_from + \
                             ' до ' + pay_to + \
                             ' ' + pay_cur
            except TypeError:
                salary = 'Зарплата не указана'
            clear_dict['salary'] = salary
            self.vacancies_list.append(clear_dict)


class SuperJobAPI(JobSearchAPI):
    vacancies_list = []

    def get_vacancies(self, specialty: str):
        api_key: str = 'v3.r.133047148.427d23ccb2f27d6502291816cda8bb06d7a59f8b.0b1b7c4b645e6846be44e0b0a3e5a6fc34b438ab'
        payload = {}
        url = f'https://api.superjob.ru/2.0/vacancies/search/?keywords={specialty}'
        headers = {
            'X-Api-App-Id': api_key
        }
        response = json.loads(request('GET', url, headers=headers, data=payload).text)['objects']
        return response

    def clear_vacancies_list(self, dirty_list: list):
        for item in dirty_list:
            clear_dict = {
                'name': item['profession'],
                'url': item['link'],
                'area': item['town']['title']
            }
            pay_from = str(item['payment_from'])
            pay_to = str(item['payment_to'])
            if pay_from == '0' and pay_to == '0':
                salary = 'Зарплата не указана'
            elif pay_from == '0' and pay_to != '0':
                salary = 'До ' + pay_to
            elif pay_to == '0' and pay_from != '0':
                salary = 'От ' + pay_from
            else:
                salary = 'От ' + pay_from + ' до ' + pay_to
            clear_dict['salary'] = salary
            self.vacancies_list.append(clear_dict)
