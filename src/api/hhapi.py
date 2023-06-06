import json

import requests

from src.abtractclasses.abstractapi import AbstractAPI
from src.utils.saver import Saver
from src.utils.vacancy import Vacancy


class HHAPI(AbstractAPI):
    def __init__(self):
        self._base_url = "api.hh.ru"
        self._order_by = "publication_time"
        self._headers = {"User - Agent": "MyApp / 1.0(my - app - feedback @ example.com)}"}

    def get_vacancies(self, text, salary, per_page):
        list_of_vacansy = []
        no_agreement = ''
        if self._order_by == "salary_desc":
            no_agreement = '&only_with_salary=true'
        data = requests.get(headers=self._headers, url=f"https://{self._base_url}/vacancies/"
                                                       f"?text={text}"
                                                       f"&salary={salary}"
                                                       f"&per_page={per_page}"
                                                       f"&order_by={self._order_by}"
                                                       f"{no_agreement}").json()
        for vacancy in data["items"]:
            title = vacancy["name"]
            published_time = self.conv_time(vacancy["published_at"])
            url = vacancy["alternate_url"]
            try:
                if vacancy["salary"]["from"] in [0, None]:
                    salary_from = 0
                else:
                    salary_from = int(vacancy["salary"]["from"])
                if vacancy["salary"]["to"] in [0, None]:
                    salary_to = 0
                else:
                    salary_to = int(vacancy['salary']['to'])
            except Exception:
                salary_from = 0
                salary_to = 0
            description = vacancy["snippet"]["responsibility"]
            vacancy_x = Vacancy(title=title,
                                published_time=published_time,
                                url=url,
                                salary_from=salary_from,
                                salary_to=salary_to,
                                description=description)
            list_of_vacansy.append(vacancy_x)
        return list_of_vacansy

    def order_by(self, param: int):
        if param in [0, 1]:
            if param == 0:
                self._order_by = "publication_time"
            elif param == 1:
                self._order_by = "salary_desc"

    @staticmethod
    def conv_time(time):
        import datetime
        datetime_obj = datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S%z")
        formatted_time = datetime_obj.strftime("%H:%M:%S %d.%m.%Y")
        return formatted_time
