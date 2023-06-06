import json

import requests

from src.abtractclasses.abstractapi import AbstractAPI
from src.utils.saver import Saver
from src.utils.vacancy import Vacancy


class SJAPI(AbstractAPI):
    def __init__(self):
        self._base_url = "api.superjob.ru/2.0"
        self._order_by = "date"
        self._headers = {"X-Api-App-Id": "v3.r.126456191.b0a6e65dc6e5d8ab73644149e31fb22052c9ac5b"
                                         ".d2b819c9469d749523027b279998811085d0ee43"}

    def get_vacancies(self, text, salary, per_page):
        list_of_vacansy = []
        no_agreement = ''
        if self._order_by == "payment":
            no_agreement = '&no_agreement=1'
        data = requests.get(headers=self._headers, url=f"https://{self._base_url}/vacancies/?"
                                                       f"&keyword={text}"
                                                       f"&payment_from={salary}"
                                                       f"&order_field={self._order_by}"
                                                       f"&count={per_page}"
                                                       f"{no_agreement}").json()
        for vacancy in data["objects"]:
            title = vacancy["profession"]
            published_time = self.conv_unixtime(vacancy["date_published"])
            url = vacancy["link"]
            try:
                if vacancy["payment_from"] in [0, None]:
                    salary_from = 0
                else:
                    salary_from = int(vacancy["payment_from"])
                if vacancy["payment_to"] in [0, None]:
                    salary_to = 0
                else:
                    salary_to = int(vacancy["payment_to"])
            except Exception:
                salary_from = 0
                salary_to = 0
            description = vacancy["candidat"]
            vacancy_x = Vacancy(title=title,
                                published_time=published_time,
                                url=url,
                                salary_from=salary_from,
                                salary_to=salary_to,
                                description=description)
            list_of_vacansy.append(vacancy_x)
        # Saver.save_in_json(list_of_vacansy, "json")
        return list_of_vacansy

    def order_by(self, param: int):
        if param in [0, 1]:
            if param == 0:
                self._order_by = "date"
            elif param == 1:
                self._order_by = "payment"

    @staticmethod
    def conv_unixtime(unixtime):
        import datetime
        # Преобразование Unixtime в объект datetime
        datetime_obj = datetime.datetime.fromtimestamp(unixtime)
        # Получение строкового представления даты и времени
        formatted_time = datetime_obj.strftime("%H:%M:%S %d.%m.%Y")
        return formatted_time
