# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests

# Пакет для удобной работы с данными в формате json
import json

# Модуль для работы со значением времени
import time
import datetime

# Модуль для работы с операционной системой. Будем использовать для работы с файлами
import os

# Модуль работы со словарями
from ndicts import DataDict, NestedDict

# Модули для вывода словарей
import pprint
import inspect

# Модуль для работы с логгами
import logging

# Подмодуль для работы с аргументами командной строки
from sys import argv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
# script, job_title, city = argv # Входные параметры: job_title - название вакансии (ключевое слово для поиска) city - город поиска

city = 1
job_title = 'Аналитик'

job_title = 'NAME:' + job_title


# Функция поиска значения по ключу
def search_key(dict_, key_):
    for key, value in dict_.items():
        if key == key_:
            return value


def getPage(page=0):
    """
    Создаем метод для получения страницы со списком вакансий.
    """
    global params
    try:
        # Справочник для параметров GET-запроса
        params = {
            'text': job_title,  # Текст фильтра. В имени должно быть слово "Аналитик" + доступен язык запросов
            'area': city,
            # Поиск ощуществляется по вакансиям 1 - Москва 77 - Рязань  Необходимо передавать id из справочника /areas. Можно указать несколько значений

            # 'text': 'NAME:Аналитик', # Текст фильтра. В имени должно быть слово "Аналитик" + доступен язык запросов
            # 'area': 1, # Поиск ощуществляется по вакансиям 1 - Москва 77 - Рязань  Необходимо передавать id из справочника /areas. Можно указать несколько значений

            'page': page,  # Номер страницы def=0
            'per_page': 100  # Кол-во вакансий на 1 странице
            # 'search_field': # string Область поиска. Значение из справочника vacancy_search_fields
            # 'experience': # string Опыт работы. Необходимо передавать id из справочника experience в /dictionaries. Можно указать несколько значений
            # 'employment': # string Тип занятости. Необходимо передавать id из справочника employment в /dictionaries. Можно указать несколько значений
            # 'schedule': # string График работы. Необходимо передавать id из справочника schedule в /dictionaries. Можно указать несколько значений
            # 'professional_role': # string Профессиональная область. Необходимо передавать id из справочника /professional_roles
            # 'industry': # string Индустрия компании, разместившей вакансию. Необходимо передавать id из справочника /industries. Можно указать несколько значений
            # 'salary': # number Размер заработной платы. Если указано это поле, но не указано currency, то для currency используется значение RUR
            # 'label': # string Фильтр по меткам вакансий. Необходимо передавать id из справочника vacancy_label в /dictionaries. Можно указать несколько значений
            # 'date_from': # string Дата, которая ограничивает снизу диапазон дат публикации вакансий. Нельзя передавать вместе с параметром period. Значение указывается в формате ISO 8601 - YYYY-MM-DD или с точность до секунды YYYY-MM-DDThh:mm:ss±hhmm. Указанное значение будет округлено до ближайших пяти минут
            # 'date_to': # string Дата, которая ограничивает сверху диапазон дат публикации вакансий. Нельзя передавать вместе с параметром period. Значение указывается в формате ISO 8601 - YYYY-MM-DD или с точность до секунды YYYY-MM-DDThh:mm:ss±hhmm. Указанное значение будет округлено до ближайших пяти минут
            # 'clusters': # boolean Возвращать ли кластеры для данного поиска. По умолчанию — false
        }
    except Exception as e:
        logging.exception("Ошибка в передаче параметров", exc_info=True)

    logging.info(f"Страница - {page}. Параметры в GET-запрос переданы успешно")
    logging.info(f"Ключевое слово поиска - {job_title}")

    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    logging.info("Посылаем запрос к API")
    try:
        data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        logging.info("Декодируем ответ")
        req.close()
        return data
    except Exception as e:
        logging.exception("Ошибка декодирования", exc_info=True)


# Получаем путь к файлу скрипта
filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))
# os.remove(path+r"\vacancies.json")

logging.info("НАЧИНАЕМ ВЫПОЛНЕНИЕ ОПЕРАЦИИ")
# Считываем первые 2000 вакансий - ограничение API hh.ru - глубина взапроса не более 2000 вакансий - огганичение API
for page in range(0, 2000):

    # Преобразуем текст ответа запроса в справочник Python
    jsObj = json.loads(getPage(page))
    # Создаем временные словари
    res_jsObj, res0_jsObj = {}, {}
    id = 0
    logging.info("Фильтруем данные от API")
    try:
        for sub_dict in search_key(jsObj, 'items'):  # Перебираем списки внутри блока items
            nd = NestedDict(sub_dict)

            id = sub_dict.get('id')
            res_jsObj[id] = {}
            res_jsObj[id]['name'] = sub_dict.get('name')
            res_jsObj[id]['city'] = nd.get(("address", "city"), "NULL")
            res_jsObj[id]['salary_to'] = nd.get(("salary", "to"), "NULL")
    except Exception as e:
        logging.exception("Ошибка фильтрации", exc_info=True)
    # Сохраняем файлы в папку {путь до текущего документа со скриптом}\docs\pagination
    # Определяем количество файлов в папке для сохранения документа с ответом запроса
    # Полученное значение используем для формирования имени документа
    # nextFileName = './docs/pagination/vacancies.json'#.format(len(os.listdir('./docs/pagination')))
    # nextFileName = r"C:\Users\Shved\Desktop\parcer_HHru\docs\pagination\vacancies.json"
    try:
        nextFileName = path + r"\vacancies.json"

        # Создаем новый документ, записываем в него ответ запроса, после закрываем
        f = open(nextFileName, mode='a+',
                 encoding='utf8')  # через W получается норм файл. через A получается "некрасивый" файл
        logging.info("Записываем данные в JSON")
        f.write(json.dumps(res_jsObj, ensure_ascii=False))
        f.close()
    except Exception as e:
        logging.exception("Ошибка записи в JSON", exc_info=True)
    # Проверка на последнюю страницу, если вакансий меньше 2000
    if (jsObj['pages'] - page) <= 1:
        break

    # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы можем подождать
    # time.sleep(0.25)
current_time = datetime.datetime.now()
timestr = time.strftime("%Y%m%d-%H%M%S")
os.rename(path + r"\vacancies.json", path + r"\vacancies_" + timestr + ".json")

logging.info("ОПЕРАЦИЯ ЗАВЕРШЕНА")
