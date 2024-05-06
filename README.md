# Сравниваем вакансии программистов
## Описание
Проект создан для прогрузки данных о зарплатах различных программистов, в зависимости от языка программирования. Поиск производится по [hh.ru](https://dev.hh.ru/) и [SuperJob](https://api.superjob.ru/).
## Установка
Скачайте необходимые файлы, затем используйте `pip` (или`pip3`, если есть конфликт с Python2) для установки зависимостей и установить зависимости. Зависимости можно установить командой, представленной ниже. 

Установите зависимость командой: 

```
pip install -r requirements.txt
```

## Пример запуска скрипта
Для запуска скрипта у вас уже долженбыть установлен Python3.

Для получения таблиц с вакансиями и заработной платой необходимо написать:

```
python main.py
```
## Переменные окружения 
Часть настроек проекта берется из переменных окружения. Переменные окружения - это переменные, значения которых присваиваются программе Python извне. Чтобы их определить, создайте файл `.env` рядом с `main.py` и запишите туда данные в таком формате: ПЕРЕМЕННАЯ=значение.

Пример срдержания файла `.env`:
```
superjob_token="SECRET_KEY_SJ"
```
Получить токен `SJ_TOKEN` можно на сайте [API SuperJob](https://api.superjob.ru/)
## Цель проекта
Код написан в образоваетльных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/modules/)


