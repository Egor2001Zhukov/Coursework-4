from src.utils.functions import user_interaction, get_vacancies

if __name__ == "__main__":
    print("Добро пожаловать в Агрегатор вакансий им. Егора Жукова")
    user_interaction(get_vacancies())
