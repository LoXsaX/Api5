import os
import requests
from terminaltables import AsciiTable
from dotenv import load_dotenv


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
    vacancies_list = {}
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
        predicted_salary_list = []
        url = 'https://api.hh.ru/vacancies'
        payload = {
            "text": f"программист {language} ",
            "area": 1,
         }
        response = requests.get(url, params = payload)
        response.raise_for_status()
        for salary in response.json()["items"]:
            currency = salary.get("salary")
            if currency and currency["currency"] == "RUR":
                predicted_salary = predict_rub_salary(salary["salary"].get("from"), salary["salary"].get("to"))
                if predicted_salary:
                    predicted_salary_list.append(predicted_salary)
        average_salary_hh = None
        if predicted_salary_list:
            average_salary_hh = int(sum(predicted_salary_list) / len(predicted_salary_list))
        vacancies_list[language] = {
            "vacancies_found": response.json()["found"],
            "vacancies_processed": len(predicted_salary_list),
            "average_salary": average_salary_hh
         }
    return vacancies_list


def get_statistic_sj(sj_token):
    vacancies_list = {}
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
        predicted_salary_list = []
        url = "https://api.superjob.ru/2.0/vacancies/"
        headers = {"X-Api-App-Id": sj_token}
        payload = {"keyword": f"программист {language}", "town": "Moscow"}
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        for salary in response.json()["objects"]:
            predicted_salary = predict_rub_salary(salary["payment_from"], salary["payment_to"])
            if predicted_salary:
                predicted_salary_list.append(predicted_salary)
        average_salary_sj = None
        if predicted_salary_list:
            average_salary_sj = int(sum(predicted_salary_list) / len(predicted_salary_list))
        vacancies_list[language] = {
            "vacancies_found": response.json()["total"],
            "vacancies_processed": len(predicted_salary_list),
            "average_salary": average_salary_sj
         }
    return vacancies_list


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
    sj_token = os.environ['SECRET_KEY_SJ']
    print(get_table_vacancy(get_statistic_sj(sj_token)))
    print(get_table_vacancy(get_statistic_hh())) 

