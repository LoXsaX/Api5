import os
import requests
from terminaltables import AsciiTable
from dotenv import load_dotenv
from itertools import count

def predict_rub_salary(salary_from = None, salary_to = None):
    if salary_from and salary_to:
        average_salary = int((salary_from * salary_to) / 2)
    elif salary_from:
        average_salary = int(salary_from * 1.2)
    elif salary_to:
        average_salary = int(salary_to * 0.8)
    else:
        average_salary = None
    return average_salary


def get_statistic_hh():
    vacancies = {}
    languages = [
        "JavaScript",
        "Java", 
        "Python", 
        "Ruby",
        "PHP",
        "C++",
        "CSS",
        "C#",
        "C",
        "Go"
    ]
    for language in languages:
        predicted_salaries = []
        for page in count(0, 1):
            url = 'https://api.hh.ru/vacancies'
            payload = {
                "text": f"программист {language} ",
                "city_code": 1,
                "page": page
             }
            response = requests.get(url, params = payload)
            response.raise_for_status()
            vacancies = response.json()
            if page >= vacancies["pages"]-1:
                    break
            for salary in vacancies["items"]:
                salary_hh = salary.get("salary")
                if salary_hh and salary_hh["currency"] == "RUR":
                    predicted_salary = predict_rub_salary(salary["salary"].get("from"), salary["salary"].get("to"))
                    if predicted_salary:
                        predicted_salaries.append(predicted_salary)
        average_salary_hh = None
        if predicted_salary:
            average_salary_hh = int(sum(predicted_salaries) / len(predicted_salaries))
        vacancies[language] = {
            "vacancies_found": vacancies["found"],
            "vacancies_processed": len(predicted_salaries),
            "average_salary": average_salary_hh
         }
    return vacancies


def get_statistic_sj(sj_token):
    vacancies = {}
    languages = [
        "JavaScript",
        "Java",
        "Python",
        "Ruby",
        "PHP",
        "C++",
        "CSS",
        "C#",
        "C",
        "Go"
    ]
    for language in languages:
        predicted_salaries = []
        for page in count(0, 1):
            url = "https://api.superjob.ru/2.0/vacancies/"
            headers = {"X-Api-App-Id": sj_token}
            payload = {"keyword": f"программист {language}", "town": "Moscow", "page": page}
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            vacancies = response.json()
            if not vacancies["objects"]:
                break
            for salary in vacancies["objects"]:
                predicted_salary = predict_rub_salary(salary["payment_from"], salary["payment_to"])
                if predicted_salary:
                    predicted_salaries.append(predicted_salary)
        average_salary_sj = None
        if predicted_salary:
            average_salary_sj = int(sum(predicted_salaries) / len(predicted_salaries))
        vacancies[language] = {
            "vacancies_found": vacancies["total"],
            "vacancies_processed": len(predicted_salaries),
            "average_salary": average_salary_sj
         }
    return vacancies


def get_table_vacancy(statistic):
    table_data = [
        [
            'Язык программирования', 
            'Вакансий найдено', 
            'Вакансий обработано', 
            'Средняя зарплата'
        ]
     ]
    for language, vacancy in statistic.items():
        table_data.append(
            [
                language,
                vacancy['vacancies_found'], 
                vacancy['vacancies_processed'],
                vacancy['average_salary']
            ]
        )    
    table = AsciiTable(table_data)
    return table.table

if __name__ == '__main__':
    load_dotenv()
    superjob_token = os.environ['SECRET_KEY_SJ']
    print(get_table_vacancy(get_statistic_sj(SuperJob_token)))
    print(get_table_vacancy(get_statistic_hh())) 

