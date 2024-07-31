import pandas as pd
import streamlit as st
import numpy as np



# HTML-код для логотипа
html_code = '''
<div style="text-align: center;">
    <a href="https://raw.githubusercontent.com/Y1OV/project_lab/main/data/ranepa.png">
        <img src="https://raw.githubusercontent.com/Y1OV/project_lab/main/data/ranepa.png" alt="Foo" style="width: 50%; height: auto;">
    </a>
</div>
'''



# Основная функция Streamlit приложения
def main():
    st.title("Разработка модели автоматического определения карьерных параметров")

    st.markdown(html_code, unsafe_allow_html=True)

    text = "1) Основная почиташка  - MAIN\n2) Визуализашка по резюме - resume info\n3) Визуализашка по вакансиям - vacancy info\n4) Информация по HeadHunter API"
    st.text_area("Что можно найти на этом streamlit-е?", text)

    tab1, tab2 = st.tabs(["Почиташка", "Тут тоже что-то будет"])

    with tab1:
        st.title("`Начало`")

        # st.write("Это пример использования `st.write` для вывода текста.")
        # st.markdown("### Это заголовок с использованием `st.markdown`")
        # st.text("Простой текст, выведенный с использованием `st.text`.")

        st.write("Основная информация бралась из такого документа: `НИР (25.06.2024).pdf`",
            "Посмотрели на данные, какие-то простые штуки по типу <зависимости ожидаемой з/п "
            "от возраста> можно увидеть во вкладочке `resume info`. В этой вкладке различные графики по датасету с резюмехами. "
            "Точно также можно изучить и всякие штуки из датасета с вакансиями: `vacancy info`.")




        st.write("""
### `Рассмотрим предложенные задачи:`:
- Автоматизация анализа карьерных траекторий и подготовки отчетов с рекомендациями по управлению карьерой;
- Описание возможных вариантов развития карьеры на основе сопоставления карьерных ожиданий с результатами личной профессиональной деятельности;
- Подготовка рекомендаций по развитию конкретных качеств и использованию личностных ресурсов для реализации карьерных планов;
- Разработка индивидуальных рекомендаций по развитию за счёт участия в конкретных образовательных программах.
""")

        st.write("### `Анализ задач и данных`")

        st.write("##### Задача 1: Автоматизация анализа карьерных траекторий и подготовки отчетов с рекомендациями по управлению карьерой")
        st.write("""
**Данные**: Резюме содержит информацию о местоположении, возрасте, опыте работы, навыках и других характеристиках кандидатов. Вакансии содержат информацию о профессиональных сферах, требуемых навыках (hard и soft skills).

**Что можно сделать**:
- Создать профили кандидатов на основе их навыков и опыта работы.
- Сопоставить эти профили с требуемыми навыками и требованиями вакансий, чтобы идентифицировать соответствия и пробелы.
- Использовать алгоритмы машинного обучения для прогнозирования возможных карьерных траекторий.

**Недостатки данных**:
- Возможно, недостаточно информации о предыдущем опыте работы и достижениях, чтобы точно прогнозировать карьерные траектории.
- Необходимость уточнения и стандартизации данных о навыках.
""")

        st.write("##### Задача 2: Описание возможных вариантов развития карьеры на основе сопоставления карьерных ожиданий с результатами личной профессиональной деятельности")
        st.write("""
**Данные**: Резюме и вакансии могут быть использованы для анализа текущих навыков и сопоставления с требованиями рынка.

**Что можно сделать**:
- Сравнение навыков кандидатов с наиболее востребованными навыками на рынке труда.
- Определение необходимых для развития навыков, которые кандидату нужно улучшить или приобрести.

**Недостатки данных**:
- Отсутствие данных о карьерных ожиданиях (например, целевые должности или отрасли).
- Неясность в деталях текущих профессиональных навыков.
""")

        st.write("##### Задача 3: Подготовка рекомендаций по развитию конкретных качеств и использованию личностных ресурсов для реализации карьерных планов")
        st.write("""
**Данные**: Информация о soft и hard skills из резюме и требования вакансий.

**Что можно сделать**:
- Анализ soft и hard skills и сопоставление с требованиями рынка.
- Рекомендации по развитию soft и hard skills, основываясь на текущих и будущих потребностях.

**Недостатки данных**:
- Отсутствие подробной информации о текущем уровне развития soft и hard skills у кандидатов.
""")

        st.write("##### Задача 4: Разработка индивидуальных рекомендаций по развитию за счёт участия в конкретных образовательных программах")
        st.write("""
**Данные**: Опять же, навыки и опыт кандидатов, а также требования вакансий.

**Что можно сделать**:
- Идентификация образовательных программ, которые могут помочь закрыть выявленные пробелы в навыках.
- Рекомендации по профессиональному обучению и сертификации.

**Недостатки данных**:
- Нет данных о доступных образовательных программах.
- Отсутствие информации о предыдущем образовании и курсовых программах кандидатов.
""")

        st.write("### `Выводы`")

        st.write("**Краткосрочные возможности (1-2 месяца):**")
        st.write("""
1. **Анализ текущих навыков и их соответствие требованиям рынка:**
   - Провести анализ имеющихся навыков кандидатов и сопоставить их с востребованными на рынке труда.
   - Создать простые профили кандидатов, чтобы идентифицировать основные пробелы в навыках и предложить первичные рекомендации.

2. **Разработка первичных рекомендаций по улучшению навыков:**
   - На основе анализа, дать рекомендации по развитию soft skills и hard skills, которые можно улучшить самостоятельно или через короткие образовательные курсы.

3. **Сбор и стандартизация данных:**
   - Улучшение качества и структуры данных, включая стандартизацию навыков, улучшение записи данных о профессиональном опыте и образовании.
""")

        st.write("**Долгосрочные возможности (6 месяцев и более):**")
        st.write("""
1. **Разработка системы автоматизированного анализа и прогнозирования:**
   - Создание системы, которая автоматически анализирует карьерные траектории и предлагает рекомендации по управлению карьерой, основанные на машинном обучении и прогнозировании.

2. **Создание детализированных карьерных рекомендаций:**
   - Разработка детализированных рекомендаций по развитию карьеры, включая участие в образовательных программах, на основе долгосрочного мониторинга данных.

3. **Расширение базы данных о карьерных ожиданиях и образовательных возможностях:**
   - Включение данных о карьерных целях кандидатов и доступных образовательных программах для более точного соответствия предложений карьерным траекториям.
""")



    with tab2:

         st.write('`Ведутся технические работы`')





if __name__ == "__main__":
    main()
