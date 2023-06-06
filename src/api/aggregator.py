from src.api.hhapi import HHAPI
from src.api.sjapi import SJAPI
from src.utils.vacancy import Vacancy


class Aggregator:
    def __init__(self):
        self.sj = SJAPI()
        self.hh = HHAPI()
        self._order_by = 0

    def get_vacancies(self, text: str, salary: int, per_page: int):
        self.sj.get_vacancies(text, salary, per_page)
        self.hh.get_vacancies(text, salary, per_page)

        if self._order_by == 1:
            Vacancy.all_vacancy.sort(key=lambda x: x["salary_from"], reverse=True)
        else:
            Vacancy.all_vacancy.sort(key=lambda x: x["published_time"], reverse=True)
        return Vacancy.all_vacancy

    def order_by(self, param: int):
        self._order_by = param
        self.sj.order_by(param)
        self.hh.order_by(param)
