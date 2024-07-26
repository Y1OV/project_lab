import pandas as pd
import streamlit as st
import numpy as np



# HTML-код для логотипа
html_code = '''
<div style="text-align: center;">
    <a href="https://raw.githubusercontent.com/Y1OV/DFO_front/main/lct/rosatom-logo-brandlogos.net.png">
        <img src="https://raw.githubusercontent.com/Y1OV/DFO_front/main/lct/rosatom-logo-brandlogos.net.png" alt="Foo" style="width: 50%; height: auto;">
    </a>
</div>
'''



# Основная функция Streamlit приложения
def main():
    st.title("Разработка модели автоматического определения карьерных параметров")

    st.markdown(html_code, unsafe_allow_html=True)

    st.text_area(
        "⚙️ Что можно найти на этом streamlit-е?",
        "1) Основная почиташка MAIN"
        "2) "
        "3) ",
        height=100
    )

    tab1, tab2 = st.tabs(["С чего начали", "К чему можно прийти"])

    with tab1:
        st.title("Начало")
        
        st.text_area(
            "Основная информация бралась из такого документа: <НИР (25.06.2024).pdf>",
            "Посмотрели на данные, какие-то простые штуки по типу <зависимости ожидаемой з/п"
            "от возраста> можно увидеть во вкладочке resume info. В этой вкладке различные графики по датасету с резюмезами."
            "Точно также можно изучить и всякие штуки из датасета с вакансиями: vacancy info.",
            height=100
        )

        st.text_area(
            "Основная информация бралась из такого документа: <НИР (25.06.2024).pdf>",
            "Посмотрели на данные, какие-то простые штуки по типу <зависимости ожидаемой з/п"
            "от возраста> можно увидеть во вкладочке resume info. В этой вкладке различные графики по датасету с резюмезами."
            "Точно также можно изучить и всякие штуки из датасета с вакансиями: vacancy info.",
            height=100
        )




        # if st.button("Распознать дефекты", key="single_button_1"):



    with tab2:

        st.title("Загрузка и отображение изображения")

        # if st.button("Распознать дефекты", key="single_button_2"):





if __name__ == "__main__":
    main()
