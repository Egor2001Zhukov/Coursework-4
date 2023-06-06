import csv
import json
import os


class Saver:
    @staticmethod
    def save_in_json(data, filename_for_save: str):
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file = os.path.join(path, f"save_vacancy/{filename_for_save}.json")
        with open(file, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def save_in_csv(data, filename_for_save: str):
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file = os.path.join(path, f"save_vacancy/{filename_for_save}.csv")
        fieldnames = ['title', 'published_time', 'url', 'salary_from', 'salary_to', 'description', 'requirements']
        with open(file, "w") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    # @staticmethod
    # def save_in_txt(data, filename_for_save: str):
    #     path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    #     file = os.path.join(path, f"save_vacancy/{filename_for_save}.txt")
    #     with open(file, "w") as f:
    #         f.writelines(f"{data}")
