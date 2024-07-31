import streamlit as st

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

if __name__ == "__main__":
    main()
