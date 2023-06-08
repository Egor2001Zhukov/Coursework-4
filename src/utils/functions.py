from src.api.aggregator import Aggregator
from src.utils.errors import FewParamError, ValueInputError, is_any_pos_number_to, is_0_or_1, is_list_indexes
from src.utils.saver import Saver


def user_interaction(all_vacancies):
    if not all_vacancies:
        try:
            cont = is_0_or_1(input("Вакансий с такими параметрами нет. Начать новый поиск?(нет(0),да(1))\n"))
            if cont:
                user_interaction(get_vacancies())
            else:
                print("Приходите снова")
        except ValueInputError:
            print("Нужно ввести цифру (1 или 0)")
    else:
        print(f"Найдено {len(all_vacancies)}")
        exit_ = False
        while not exit_:
            try:
                inter = is_any_pos_number_to(
                    input("Можете сделать новый поиск(1), сохранить(2), сравнить(3), поподробнее о вакансии(4),"
                          "выйти(9)\n"))
                # Выход из приложения
                if inter == 9:
                    print("Приходите снова")
                    break
                # Новый поиск
                elif inter == 1:
                    exit_ = True
                    user_interaction(get_vacancies())
                # Сохранение
                elif inter == 2:
                    if len(all_vacancies) < 2:
                        save_func(all_vacancies[0])
                    else:
                        save_in(all_vacancies)
                        exit_ = continue_or_not(all_vacancies)
                # Сравнение
                elif inter == 3:
                    if len(all_vacancies) < 2:
                        print("Недостаточно вакансий для сравнения")
                    else:
                        compare_func(all_vacancies)
                        exit_ = continue_or_not(all_vacancies)
                # Поподробнее о вакансии
                elif inter == 4:
                    if len(all_vacancies) < 2:
                        print_all_vacancy(all_vacancies[0])
                    else:
                        show_vacancy(all_vacancies)
                        exit_ = continue_or_not(all_vacancies)
                else:
                    print("Введите только цифры возможных операций")
            except ValueInputError:
                print("Введите только цифры возможных операций")
                user_interaction(all_vacancies)


def save_func(list_):
    try:
        save_to = is_0_or_1(input("В json(0) или csv(1)\n"))
        if save_to:
            Saver.save_in_csv(list_, input("Как назвать файл?"))
        else:
            Saver.save_in_json(list_, input("Как назвать файл?"))
    except ValueInputError:
        print("Введите число (0 или 1)")
        save_in(list_)


def continue_or_not(all_vacancies):
    try:
        cont = is_0_or_1(input("Продолжить работу с вакансиями?(нет(0),да(1))\n"))
        if cont:
            user_interaction(all_vacancies)
            return True
        else:
            print("Приходите снова")
            return True
    except ValueInputError:
        print("Введите число (0 или 1)")
        continue_or_not(all_vacancies)


def salary_func(v):
    salary_ = ""
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
          f'Зарплата: {salary_func(v)}\n'
          f'Время публикации: {v["published_time"]}\n'
          f'Описание: {v["description"]}\n')


def print_vacancy(list_of_vacancy):
    x = 1
    for v in list_of_vacancy:
        print(f'{x}: {v["title"]}, {salary_func(v)}, {v["published_time"]}')
        x += 1


def get_vacancies():
    text = input("Введите текст запроса\n")
    salary = 0
    per_page = 0
    sort_key = 0
    exit_ = False
    while not exit_:
        try:
            salary = is_any_pos_number_to(input("Введите желаемую зарплату (при сортировке по дате поля зарплаты "
                                                "могут быть пустыми)\n"))
            exit_ = True
        except ValueInputError:
            print("Нужно ввести цифру больше 0 (пример: 80000)")
    exit_ = False
    while not exit_:
        try:
            per_page = is_any_pos_number_to(input("Введите желаемое кол-во результатов (до 100)\n"), to=100)
            exit_ = True
        except ValueInputError:
            print("Нужно ввести цифру больше 0 и меньше 100 (пример: 5)")
    exit_ = False
    while not exit_:
        try:
            sort_key = is_0_or_1(input("Как сортировать список? Введите 0 или 1 (0 - по дате, 1 - по зарплате)\n"))
            exit_ = True
        except ValueInputError:
            print("Нужно ввести цифру (1 или 0)")
    aggregator = Aggregator()
    aggregator.order_by(sort_key)
    all_vacancies = aggregator.get_vacancies(text, salary, per_page)[:per_page]
    print_vacancy(all_vacancies)
    return all_vacancies


def compare_func(all_vacancies):
    try:
        compare = is_list_indexes(input("Для сравнения выберите 2 или более вакансий (введите цифры через запятую) \n"),
                                  len(all_vacancies))
        compare_list = []
        for x in compare.split(", "):
            compare_list.append(all_vacancies[int(x) - 1])
        if len(compare_list) < 2:
            raise FewParamError
        for v in compare_list:
            print_all_vacancy(v)
        save = int(input("Сохранить сравниваемые вакансии?(нет(0),да(1))\n"))
        if save:
            save_in(compare_list)
    except FewParamError:
        print("Слишком мало значений")
        compare_func(all_vacancies)
    except ValueInputError:
        print("Нужно ввести цифру или цифры через запятую (пример: 1, 2, 4)")
        save_in(all_vacancies)


def save_in(all_vacancies):
    try:
        save_list = []
        save = is_list_indexes(input("Выберите вакансии для сохранения (введите цифру или цифры через запятую)\n"),
                               len(all_vacancies))
        for x in save:
            save_list.append(all_vacancies[int(x) - 1])
        save_in(save_list)
    except ValueInputError:
        print("Нужно ввести цифру или цифры через запятую (пример: 1, 2, 4)")
        save_in(all_vacancies)


def show_vacancy(all_vacancies):
    try:
        number = is_any_pos_number_to(input("Какую вакансию нужно посмотреть?(введите номер вакансии)\n"),
                                      to=len(all_vacancies)+1)
        v = all_vacancies[number - 1]
        print_all_vacancy(v)
    except ValueInputError:
        print("Нужно ввести цифру из возможных (пример: 1)")
        show_vacancy(all_vacancies)
