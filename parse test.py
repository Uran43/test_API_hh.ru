# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH
import requests

# Пакет для удобной работы с данными в формате json
import json

# Модуль для работы со значением времени
import time

# Модуль для работы с операционной системой. Будем использовать для работы с файлами
import os

# Модуль работы со словарями
from ndicts import DataDict, NestedDict

# Модули для вывода словарей
import pprint
import inspect

# Подмодуль для работы с аргументами командной строки
from sys import argv

#script, job_title, city = argv # Входные параметры: job_title - название вакансии (ключевое слово для поиска) city - город поиска

city = 1
job_title = 'Аналитик'

job_title = 'NAME:' + job_title

# Функция поиска значения по ключу
def search_key(dict_, key_):
    for key, value in dict_.items():
        if key == key_:
            return value
        
 
def getPage(page = 0):
    """
    Создаем метод для получения страницы со списком вакансий.
    """
    
    # Справочник для параметров GET-запроса
    params = {
        'text': job_title, # Текст фильтра. В имени должно быть слово "Аналитик" + доступен язык запросов
        'area': city, # Поиск ощуществляется по вакансиям 1 - Москва 77 - Рязань  Необходимо передавать id из справочника /areas. Можно указать несколько значений
        
        #'text': 'NAME:Аналитик', # Текст фильтра. В имени должно быть слово "Аналитик" + доступен язык запросов
        #'area': 1, # Поиск ощуществляется по вакансиям 1 - Москва 77 - Рязань  Необходимо передавать id из справочника /areas. Можно указать несколько значений

        
        'page': page, # Номер страницы def=0
        'per_page': 100 # Кол-во вакансий на 1 странице
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
    
    
    req = requests.get('https://api.hh.ru/vacancies', params) # Посылаем запрос к API
    data = req.content.decode() # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))
#os.remove(path+r"\vacancies.json")

# Считываем первые 2000 вакансий - ограничение API hh.ru - глубина взапроса не более 2000 вакансий - огганичение API
for page in range(0, 2000):
    
    # Преобразуем текст ответа запроса в справочник Python
    
    jsObj = json.loads(getPage(page))

    res_jsObj = {}
    res0_jsObj = {}
    id = 0
    for sub_dict in search_key(jsObj,'items'): # Перебираем списки внутри блока items
        nd = NestedDict(sub_dict)

        id = sub_dict.get('id')
        res_jsObj[id] = {}
        res_jsObj[id]['name'] = sub_dict.get('name')
        res_jsObj[id]['city'] = nd.get(("address", "city"), "NULL")
        res_jsObj[id]['salary_to'] = nd.get(("salary", "to"), "NULL")

    # Сохраняем файлы в папку {путь до текущего документа со скриптом}\docs\pagination
    # Определяем количество файлов в папке для сохранения документа с ответом запроса
    # Полученное значение используем для формирования имени документа
    #nextFileName = './docs/pagination/vacancies.json'#.format(len(os.listdir('./docs/pagination')))
    #nextFileName = r"C:\Users\Shved\Desktop\parcer_HHru\docs\pagination\vacancies.json"

    
    nextFileName = path+r"\vacancies.json"

    
    # Создаем новый документ, записываем в него ответ запроса, после закрываем
    f = open(nextFileName, mode='a+', encoding='utf8') # через W получается норм файл. через A получается "некрасивый" файл
    f.write(json.dumps(res_jsObj, ensure_ascii=False))
    f.close()
    
    # Проверка на последнюю страницу, если вакансий меньше 2000
    if (jsObj['pages'] - page) <= 1:
        break
    
    # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
    #time.sleep(0.25)
    
print('<<<<<<Страницы поиска собраны>>>>>')
