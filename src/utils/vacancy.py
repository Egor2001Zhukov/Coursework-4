class Vacancy:
    all_vacancy = []

    def __init__(self, title, published_time, url, salary_from, salary_to, description):
        self.title = title
        self.published_time = published_time
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = description
        self.all_vacancy.append({"title": title,
                                 "published_time": published_time,
                                 "url": url,
                                 "salary_from": salary_from,
                                 "salary_to": salary_to,
                                 "description": description})
