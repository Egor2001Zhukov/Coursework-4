from src.api.aggregator import Aggregator
from src.api.hhapi import HHAPI
from src.api.sjapi import SJAPI
from src.utils.saver import Saver


def save_(list_):
    save_to = int(input("В json(0) или csv(1)\n"))
    if save_to:
        Saver.save_in_csv(list_, input("Как назвать файл?"))
    else:
        Saver.save_in_json(list_, input("Как назвать файл?"))


def continue_or_not(all_vacancies):
    cont = int(input("Продолжить работу с вакансиями?(нет(0),да(1))\n"))
    if cont:
        user_interaction(all_vacancies)
        return True
    else:
        print("Приходите снова")
        return True


def salary(v):
    if v["salary_from"] == 0 and v["salary_to"] == 0:
        salary_ = 'не указана'
    elif v["salary_from"] == v["salary_to"]:
        salary_ = f'{v["salary_from"]}'
    elif v["salary_from"] > 0 and v["salary_to"] > 0:
        salary_ = f'{v["salary_from"]} - {v["salary_to"]}'
    elif v["salary_from"] > 0:
        salary_ = f'от {v["salary_from"]}'
    elif v["salary_to"] > 0:
        salary_ = f'до {v["salary_to"]}'
    return salary_


def print_all_vacancy(v):
    print(f'Название: {v["title"]}\n'
          f'Ссылка на вакансию: {v["url"]}\n'
          f'Зарплата: {salary(v)}\n'
          f'Время публикации: {v["published_time"]}\n'
          f'Описание: {v["description"]}\n')


def print_vacancy(list_of_vacancy):
    x = 1
    for v in list_of_vacancy:
        print(f'{x}: {v["title"]}, {salary(v)}, {v["published_time"]}')
        x += 1


def user_interaction_get_vacancies():
    text = input("Введите текст запроса\n")
    salary = int(input("Введите желаемую зарплату (при сортировке по дате поля зарплаты могут быть пустыми)\n"))
    per_page = int(input("Введите желаемое кол-во результатов (до 100)\n"))
    sort_key = int(input("Как сортировать список? Введите 0 или 1 (0 - по дате, 1 - по зарплате)\n"))
    aggregator = Aggregator()
    aggregator.order_by(sort_key)
    all_vacancies = aggregator.get_vacancies(text, salary, per_page)[:per_page]
    print_vacancy(all_vacancies)
    return all_vacancies


def user_interaction(all_vacancies):
    exit_ = False
    while not exit_:
        inter = int(input("Можете сделать новый поиск(0), сохранить(1), сравнить(2), поподробнее о вакансии(3), "
                          "выйти(9) (при сортировке по дате"
                          "поля зарплаты могут"
                          "быть пустыми)\n"))
        # Выход из приложения
        if inter == 9:
            print("Приходите снова")
            exit_ = True
        # Новый поиск
        elif inter == 0:
            exit_ = True
            user_interaction(user_interaction_get_vacancies())
        # Со
        elif inter == 1:
            save_list = []
            save = input("Для сохранения выберите 2 или более вакансий (введите цифры через запятую)\n")
            for x in save.split(", "):
                save_list.append(all_vacancies[int(x) - 1])
            save_(save_list)
            exit_ = continue_or_not(all_vacancies)
        elif inter == 2:
            compare = input("Для сравнения выберите 2 или более вакансий (введите цифры через запятую) \n")
            compare_list = []
            for x in compare.split(", "):
                compare_list.append(all_vacancies[int(x) - 1])
            for v in compare_list:
                print_all_vacancy(v)
            save = int(input("Сохранить сравниваемые вакансии?(нет(0),да(1))\n"))
            if save:
                save_(compare_list)
            exit_ = continue_or_not(all_vacancies)
        elif inter == 3:
            number = int(input("Какую вакансию нужно посмотреть?(введите номер вакансии)\n"))
            v = all_vacancies[int(number) - 1]
            print_all_vacancy(v)
            exit_ = continue_or_not(all_vacancies)
        else:
            print("Введите только цифры возможных операций")
