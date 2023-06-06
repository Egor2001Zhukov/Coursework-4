from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    """Абстрактный класс АПИ"""

    @abstractmethod
    def __init__(self):
        """Инициализация абстрактного АПИ"""
        self._base_url = ""
        self._order_by = ""
        self.headers = {}

    @abstractmethod
    def get_vacancies(self, text: str, salary: int, per_page: int):
        pass

    def order_by(self, param):
        if param in ["date", "salary"]:
            pass
