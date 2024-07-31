import streamlit as st
import json

html_code = '''
<div style="text-align: center;">
    <a href="https://raw.githubusercontent.com/Y1OV/project_lab/main/data/ranepa.png">
        <img src="https://raw.githubusercontent.com/Y1OV/project_lab/main/data/ranepa.png" alt="Foo" style="width: 50%; height: auto;">
    </a>
</div>
'''

def main():

    st.title("HeadHunter API")

    st.markdown(html_code, unsafe_allow_html=True)
    
    st.write("""HeadHunter API — это инструментарий для интеграции [HeadHunter](http://hh.ru/) в ваш продукт.""")

    st.write("""Для использования методов, требующих авторизацию пользователя или приложения, вам необходимо
зарегистрировать приложение по адресу [https://dev.hh.ru](https://dev.hh.ru)
и настроить процесс [авторизации](docs/authorization.md).""")

    st.write("""
### `Общая информация:`:
- Всё API работает по протоколу HTTPS.
- Авторизация осуществляется по протоколу OAuth2.
- Все данные доступны только в формате JSON.
- Базовый URL — `https://api.hh.ru/`
- Возможны запросы к данным любого сайта группы компаний HeadHunter
- Даты форматируются в соответствии с ISO 8601: `YYYY-MM-DDThh:mm:ss±hhmm`.
""")

    st.write("---")

    st.write("""
### `Поиск вакансий:`:
Возвращает список вакансий, размещенных в сервисе. Список вакансий фильтруется согласно переданным параметрам запроса.
""")


    st.write("""
    ###### QUERY PARAMETERS
    
    **page**  
    number  
    _Default: 0_  
    Номер страницы  
    
    ---
    
    **per_page**  
    number  
    _<= 100_  
    _Default: 10_  
    Количество элементов  
    
    ---
    
    **text**  
    string  
    Переданное значение ищется в полях вакансии, указанных в параметре `search_field`. Доступен [язык запросов](#). Специально для этого поля есть [автодополнение](#).
    
    ---
    
    **search_field**  
    string  
    Область поиска. Справочник с возможными значениями: `vacancy_search_fields` в `/dictionaries`. По умолчанию, используются все поля. Можно указать несколько значений.
    
    ---
    
    **experience**  
    string  
    Опыт работы. Необходимо передавать `id` из справочника experience в `/dictionaries`. Можно указать несколько значений.
    
    ---
    
    **employment**  
    string  
    Тип занятости. Необходимо передавать `id` из справочника employment в `/dictionaries`. Можно указать несколько значений.
    
    ---
    
    **schedule**  
    string  
    График работы. Необходимо передавать `id` из справочника schedule в `/dictionaries`. Можно указать несколько значений.
    
    ---
    
    **area**  
    string  
    Регион. Необходимо передавать `id` из справочника `/areas`. Можно указать несколько значений.
    
    ---
    
    **metro**  
    string  
    Ветка или станция метро. Необходимо передавать `id` из справочника `/metro`. Можно указать несколько значений.
    
    ---
    
    **professional_role**  
    string  
    Профессиональная область. Необходимо передавать `id` из справочника `/professional_roles`.
    
    ---
    
    **industry**  
    string  
    Индустрия компании, разместившей вакансию. Необходимо передавать `id` из справочника `/industries`. Можно указать несколько значений.
    
    ---
    
    **employer_id**  
    string  
    Идентификатор работодателя. Можно указать несколько значений.
    
    ---
    
    **currency**  
    string  
    Код валюты. Справочник с возможными значениями: `currency` (ключ code) в `/dictionaries`. Имеет смысл указывать только совместно с параметром salary.
    
    ---
    
    **salary**  
    number  
    Размер заработной платы. Если указано это поле, но не указано currency, то для currency используется значение RUR. При указании значения будут найдены вакансии, в которых вилка зарплаты близка к указанной в запросе. При этом значения пересчитываются по текущим курсам ЦБ РФ. Например, при указании salary=100&currency=EUR будут найдены вакансии, где вилка зарплаты указана в рублях и после пересчёта в Евро близка к 100 EUR. По умолчанию будут также найдены вакансии, в которых вилка зарплаты не указана, чтобы такие вакансии отфильтровать, используйте `only_with_salary=true`.
    
    ---
    
    **label**  
    string  
    Фильтр по меткам вакансий. Необходимо передавать `id` из справочника `vacancy_label` в `/dictionaries`. Можно указать несколько значений.
    
    ---
    
    **only_with_salary**  
    boolean  
    Показывать вакансии только с указанием зарплаты. По умолчанию false.
    
    ---
    
    **period**  
    number  
    Количество дней, в пределах которых производится поиск по вакансиям.
    
    ---
    
    **date_from**  
    string  
    Дата, которая ограничивает снизу диапазон дат публикации вакансий. Нельзя передавать вместе с параметром `period`. Значение указывается в формате ISO 8601 - YYYY-MM-DD или с точностью до секунды YYYY-MM-DDThh:mm:ss±hhmm. Указанное значение будет округлено до ближайших пяти минут.
    
    ---
    
    **date_to**  
    string  
    Дата, которая ограничивает сверху диапазон дат публикации вакансий. Нельзя передавать вместе с параметром `period`. Значение указывается в формате ISO 8601 - YYYY-MM-DD или с точностью до секунды YYYY-MM-DDThh:mm:ss±hhmm. Указанное значение будет округлено до ближайших пяти минут.
    
    ---
    
    **top_lat**  
    number  
    Верхняя граница широты. При поиске используется значение указанного в вакансии адреса. Принимаемое значение — градусы в виде десятичной дроби. Необходимо передавать одновременно все четыре параметра гео-координат, иначе вернется ошибка.
    
    ---
    
    **bottom_lat**  
    number  
    Нижняя граница широты. При поиске используется значение указанного в вакансии адреса. Принимаемое значение — градусы в виде десятичной дроби. Необходимо передавать одновременно все четыре параметра гео-координат, иначе вернется ошибка.
    
    ---
    
    **left_lng**  
    number  
    Левая граница долготы. При поиске используется значение указанного в вакансии адреса. Принимаемое значение — градусы в виде десятичной дроби. Необходимо передавать одновременно все четыре параметра гео-координат, иначе вернется ошибка.
    
    ---
    
    **right_lng**  
    number  
    Правая граница долготы. При поиске используется значение указанного в вакансии адреса. Принимаемое значение — градусы в виде десятичной дроби. Необходимо передавать одновременно все четыре параметра гео-координат, иначе вернется ошибка.
    
    ---
    
    **order_by**  
    string  
    Сортировка списка вакансий. Справочник с возможными значениями: `vacancy_search_order` в `/dictionaries`. Если выбрана сортировка по удалённости от гео-точки `distance`, необходимо также задать её координаты: `sort_point_lat`, `sort_point_lng`.
    
    ---
    
    **sort_point_lat**  
    number  
    Значение географической широты точки, по расстоянию от которой будут отсортированы вакансии. Необходимо указывать только, если `order_by` установлено в `distance`.
    
    ---
    
    **sort_point_lng**  
    number  
    Значение географической долготы точки, по расстоянию от которой будут отсортированы вакансии. Необходимо указывать только, если `order_by` установлено в `distance`.
    
    ---
    
    **clusters**  
    boolean  
    Возвращать ли кластеры для данного поиска. По умолчанию — false.
    
    ---
    
    **describe_arguments**  
    boolean  
    Возвращать ли описание использованных параметров поиска (массив `arguments`). По умолчанию — false.
    
    ---
    
    **no_magic**  
    boolean  
    Если значение true — автоматическое преобразование вакансий отключено. По умолчанию – false. При включённом автоматическом преобразовании, будет предпринята попытка изменить текстовый запрос пользователя на набор параметров. Например, запрос text=москва бухгалтер 100500 будет преобразован в text=бухгалтер&only_with_salary=true&area=1&salary=100500.
    
    ---
    
    **premium**  
    boolean  
    Если значение true — в сортировке вакансий будет учтены премиум вакансии. Такая сортировка используется на сайте. По умолчанию — false.
    
    ---
    
    **responses_count_enabled**  
    boolean  
    Если значение true — дополнительное поле `counters` с количеством откликов для вакансии включено. По-умолчанию — false.
    
    ---
    
    **part_time**  
    string  
    Вакансии для подработки. Возможные значения:  
    - Все элементы из `working_days` в `/dictionaries`.  
    - Все элементы из `working_time_intervals` в `/dictionaries`.  
    - Все элементы из `working_time_modes` в `/dictionaries`.  
    - Элементы `part` или `project` из `employment` в `/dictionaries`.  
    - Элемент `accept_temporary`, показывает вакансии только с временным трудоустройством. Можно указать несколько значений.
    
    ---
    
    **accept_temporary**  
    boolean  
    Если значение true — то поиск происходит только по вакансиям временной работы. По-умолчанию — false.
    
    ---
    
    **locale**  
    string  
    _Default: "RU"_  
    Example: locale=EN  
    Идентификатор локали (см. Локализация).
    
    ---
    
    **host**  
    string  
    _Default: "hh.ru"_  
    Enum: "hh.ru" "rabota.by" "hh1.az" "hh.uz" "hh.kz" "headhunter.ge" "headhunter.kg"  
    Example: host=hh.ru  
    Доменное имя сайта (см. Выбор сайта).
    """)

    st.write("---")

    st.write("""
    ### `Просмотр резюме:`:
    Возвращает информацию об указанном резюме.
    """)



    st.write("""
    ###### QUERY PARAMETERS

    **with_negotiations_history**  
    boolean  
    В случае, если передан данный параметр, в ответе добавится поле `negotiations_history.vacancies`. Его формат подробно описан в методе полной истории откликов/приглашений по резюме и различается лишь тем, что в данном случае список будет ограничен тремя вакансиями данного работодателя и последним изменением состояния отклика/приглашения по каждой из этих вакансий.

    ---

    **with_creds**  
    boolean  
    В случае, если передан данный параметр, в ответе добавится поле `creds`.

    ---

    **with_job_search_status**  
    boolean  
    Параметр для просмотра в резюме статуса поиска кандидата.

    ---

    **locale**  
    string  
    _Default: "RU"_  
    Example: locale=EN  
    Идентификатор локали (см. Локализация).

    ---

    **host**  
    string  
    _Default: "hh.ru"_  
    Enum: "hh.ru", "rabota.by", "hh1.az", "hh.uz", "hh.kz", "headhunter.ge", "headhunter.kg"  
    Example: host=hh.ru  
    Доменное имя сайта (см. Выбор сайта).
    """)


    data = {
    "_progress": {
        "mandatory": [],
        "percentage": 55,
        "recommended": []
    },
    "access": {
        "type": {}
    },
    "actions": {
        "download": {}
    },
    "age": None,
    "alternate_url": "https://hh.ru/resume/ca9fb415848",
    "area": {
        "id": "1",
        "name": "Москва",
        "url": "https://api.hh.ru/areas/1"
    },
    "birth_date": None,
    "blocked": False,
    "business_trip_readiness": {
        "id": "never",
        "name": "не готов к командировкам"
    },
    "can_publish_or_update": False,
    "certificate": [],
    "citizenship": [{}],
    "contact": [{}, {}],
    "created_at": "2023-05-25T14:19:02+0300",
    "creds": {
        "answers": {},
        "question_to_answer_map": {},
        "questions": {}
    },
    "download": {
        "pdf": {},
        "rtf": {}
    },
    "driver_license_types": [],
    "education": {
        "additional": [],
        "attestation": [],
        "elementary": [],
        "level": {},
        "primary": []
    },
    "employment": {
        "id": "full",
        "name": "Полная занятость"
    },
    "employments": [{}],
    "experience": [{}],
    "finished": True,
    "first_name": "Иван",
    "gender": {
        "id": "male",
        "name": "Мужской"
    },
    "has_vehicle": None,
    "hidden_fields": [],
    "id": "ca9fb415848",
    "language": [{}],
    "last_name": "Иванов",
    "metro": None,
    "middle_name": None,
    "moderation_note": [],
    "new_views": 0,
    "next_publish_at": "2023-05-25T18:19:03+0300",
    "paid_services": [{}, {}],
    "photo": None,
    "platform": {
        "id": "headhunter"
    },
    "portfolio": [],
    "professional_roles": [{}],
    "progress": {
        "mandatory": [],
        "percentage": 55,
        "recommended": []
    },
    "publish_url": "https://api.hh.ru/resumes/ca9fb415848/publish",
    "recommendation": [],
    "relocation": {
        "area": [],
        "district": [],
        "type": {}
    },
    "resume_locale": {
        "id": "RU",
        "name": "Русский"
    },
    "salary": {
        "amount": 10000,
        "currency": "USD"
    },
    "schedule": {
        "id": "fullDay",
        "name": "Полный день"
    },
    "schedules": [{}],
    "site": [],
    "skill_set": [],
    "skills": "Руководство большой командой",
    "status": {
        "id": "published",
        "name": "опубликовано"
    },
    "tags": [{}],
    "title": "API Test Resume",
    "total_experience": {
        "months": 14
    },
    "total_views": 0,
    "travel_time": {
        "id": "any",
        "name": "Не имеет значения"
    },
    "updated_at": "2023-05-25T14:19:03+0300",
    "views_url": "https://api.hh.ru/resumes/ca9fb415848/views",
    "work_ticket": []
}

    json_str = json.dumps(data, indent=4, ensure_ascii=False)

    st.write(f"```json\n{json_str}\n```")



if __name__ == "__main__":
    main()
