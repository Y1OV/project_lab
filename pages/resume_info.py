import pandas as pd
import streamlit as st
import numpy as np
import json
from datetime import datetime
from collections import Counter
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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

    
    st.markdown(html_code, unsafe_allow_html=True)


    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Зарплатные данных", "Должности кандидатов", "Образовании кандидатов", "Опыт кандидатов",
                             "Skills"])

    with tab1:

        st.title('Анализ зарплатных данных')

        file_path = '/Users/y1ov/Work/project_lab/processed_data_resume.csv'
        data = pd.read_csv(file_path)

        chart_type = st.selectbox(
        "Выберите тип графика",
        ("Распределение зарплат", "Зависимость зарплаты от возраста",
        "Средняя зарплата по должностям", "Средняя зарплата по регионам", "Средняя зарплата по полу")
    )

        if chart_type == "Распределение зарплат":
            fig = px.histogram(data, x='salary', nbins=30, title='Распределение зарплат')
            st.plotly_chart(fig)

        elif chart_type == "Зависимость зарплаты от возраста":
            fig = px.scatter(data, x='age', y='salary', title='Зависимость зарплаты от возраста')
            st.plotly_chart(fig)

        elif chart_type == "Средняя зарплата по должностям":
            position_salary = data.groupby('positionName')['salary'].mean().sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(position_salary, x='positionName', y='salary', title='Средняя зарплата по различным должностям (топ 10)')
            st.plotly_chart(fig)

        elif chart_type == "Средняя зарплата по регионам":
            locality_salary = data.groupby('localityName')['salary'].mean().sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(locality_salary, x='localityName', y='salary', title='Средняя зарплата по регионам (топ 10)')
            st.plotly_chart(fig)

        elif chart_type == "Средняя зарплата по полу":
            gender_salary = data.groupby(['gender_female', 'gender_male'])['salary'].mean().reset_index()
            gender_salary['gender'] = gender_salary.apply(lambda row: 'Female' if row['gender_female'] == 1 else 'Male', axis=1)
            fig = px.bar(gender_salary, x='gender', y='salary', title='Средняя зарплата в зависимости от пола')
            st.plotly_chart(fig)
    
    with tab2:

        file_path = '/Users/y1ov/Work/project_lab/processed_data_resume.csv'
        data = pd.read_csv(file_path)
        data = data[data['positionName'].apply(lambda x: not isinstance(x, float))]
        # Приведение всех значений должностей к нижнему регистру
        data['positionName'] = data['positionName'].astype(str).str.lower()

# Создание словаря для классификации должностей
        position_categories = {
            'управленческие': ['менеджер', 'администратор', 'директор', 'руководитель'],
            'технические': ['инженер', 'техник', 'разработчик', 'программист', 'специалист'],
            'рабочие': ['подсобный рабочий', 'разнорабочий', 'рабочий', 'уборщик', 'грузчик'],
            'финансовые': ['бухгалтер', 'экономист', 'финансист', 'казначей'],
            'продажи и обслуживание': ['продавец', 'кассир', 'официант', 'бармен', 'повар', 'охранник'],
            'транспорт': ['водитель', 'машинист', 'оператор', 'экспедитор'],
            'образование': ['учитель', 'воспитатель', 'преподаватель'],
            'медицина': ['врач', 'медсестра', 'санитар'],
            'прочие': ['контролёр', 'консультант', 'секретарь']
        }

        # Функция для классификации должностей
        def classify_position(position):
            for category, positions in position_categories.items():
                if any(pos in position for pos in positions):
                    return category
            return 'прочие'

        # Применение классификации к данным
        data['positionCategory'] = data['positionName'].apply(classify_position)

        # Распределение должностей по возрастным группам
        age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
        age_labels = ['0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '66+']
        data['ageGroup'] = pd.cut(data['age'], bins=age_bins, labels=age_labels, right=False)

        # Распределение должностей по полу
        gender_position_distribution = data.groupby(['gender_female', 'gender_male'])['positionCategory'].value_counts().unstack().fillna(0)
        gender_position_distribution.index = ['Female', 'Male']

        # Частота встречаемости должностей
        position_counts_normalized = data['positionName'].value_counts()

        # 10 самых редких должностей
        rare_positions = position_counts_normalized.tail(10)

        # Распределение должностей по категориям
        category_counts = data['positionCategory'].value_counts()

        # Выбор графика
        st.title('Анализ должностей кандидатов')
        chart_type = st.selectbox('Выберите тип графика:', [
            'Распределение должностей по возрастным группам',
            'Распределение должностей по полу',
            '10 редких должностей',
            'Распределение должностей по категориям'
        ])

        if chart_type == 'Распределение должностей по возрастным группам':
            age_position_distribution = data.groupby('ageGroup')['positionCategory'].value_counts().unstack().fillna(0)
            fig = px.bar(age_position_distribution, barmode='stack', title='Распределение должностей по возрастным группам')
            st.plotly_chart(fig)
        elif chart_type == 'Распределение должностей по полу':
            fig = px.bar(gender_position_distribution, barmode='stack', title='Распределение должностей по полу')
            st.plotly_chart(fig)
        elif chart_type == '10 редких должностей':
            fig = px.bar(rare_positions, title='10 редких должностей')
            st.plotly_chart(fig)
        elif chart_type == 'Распределение должностей по категориям':
            fig = px.bar(category_counts, title='Распределение должностей по категориям')
            st.plotly_chart(fig)

    with tab3:
        file_path = '/Users/y1ov/Work/project_lab/processed_data_resume.csv'
        data = pd.read_csv(file_path)

        # Удаление всех значений типа float из колонки educationList
        data = data[data['educationList'].apply(lambda x: isinstance(x, str))]

# Функция для распарсивания строки JSON и извлечения информации
        def parse_education_list(education_str):
            try:
                education_list = json.loads(education_str.replace("'", '"'))
                return education_list
            except:
                return []

        # Применим функцию к колонке educationList
        data['parsedEducationList'] = data['educationList'].apply(parse_education_list)

        # Извлечем ключевую информацию из распарсенных данных
        education_records = []

        for index, row in data.iterrows():
            for education in row['parsedEducationList']:
                education_record = {
                    'candidateId': row['candidateId'],
                    'instituteName': education.get('instituteName', 'Не указано'),
                    'faculty': education.get('faculty', 'Не указано'),
                    'graduateYear': education.get('graduateYear', 'Не указано'),
                    'educationType': education.get('type', 'Не указано')
                }
                education_records.append(education_record)

        # Создадим датафрейм из списка записей об образовании
        education_df = pd.DataFrame(education_records)

        # Уберем записи с "Не указано" в поле graduateYear и преобразуем к числовому типу
        education_df_filtered = education_df[education_df['graduateYear'] != 'Не указано']
        education_df_filtered['graduateYear'] = pd.to_numeric(education_df_filtered['graduateYear'], errors='coerce').dropna().astype(int)

        # Фильтрация данных, чтобы рассматривать только значения с 1900 года
        education_df_filtered = education_df_filtered[education_df_filtered['graduateYear'] >= 1900]

        # Распределение уровней образования
        education_type_counts = education_df['educationType'].value_counts()

        # Частота упоминания различных учебных заведений
        institute_counts = education_df['instituteName'].value_counts().head(10)

        # Распределение годов окончания учебных заведений
        graduate_year_counts = education_df_filtered['graduateYear'].value_counts().sort_index()

        # Выбор графика
        st.title('Анализ данных об образовании кандидатов')
        chart_type = st.selectbox('Выберите тип графика:', [
            'Распределение уровней образования',
            'Топ-10 учебных заведений по частоте упоминания',
            'Распределение годов окончания учебных заведений'
        ])

        if chart_type == 'Распределение уровней образования':
            fig = px.bar(education_type_counts, title='Распределение уровней образования', labels={'index': 'Тип образования', 'value': 'Количество'})
            st.plotly_chart(fig)
        elif chart_type == 'Топ-10 учебных заведений по частоте упоминания':
            fig = px.bar(institute_counts, title='Топ-10 учебных заведений по частоте упоминания', labels={'index': 'Учебные заведения', 'value': 'Количество упоминаний'})
            st.plotly_chart(fig)
        elif chart_type == 'Распределение годов окончания учебных заведений':
            fig = px.line(graduate_year_counts, title='Распределение годов окончания учебных заведений', labels={'index': 'Год окончания', 'value': 'Количество'}, markers=True)
            st.plotly_chart(fig)

    with tab4:
        file_path = '/Users/y1ov/Work/project_lab/processed_data_resume.csv'
        data = pd.read_csv(file_path)

        # Удаление всех значений типа float из колонки workExperienceList
        data = data[data['workExperienceList'].apply(lambda x: isinstance(x, str))]

        # Функция для распарсивания строки JSON и извлечения информации
        def parse_work_experience_list(work_experience_str):
            try:
                work_experience_list = json.loads(work_experience_str.replace("'", '"'))
                return work_experience_list
            except:
                return []

        # Применим функцию к колонке workExperienceList
        data['parsedWorkExperienceList'] = data['workExperienceList'].apply(parse_work_experience_list)

        # Извлечем ключевую информацию из распарсенных данных
        work_experience_records = []

        for index, row in data.iterrows():
            for experience in row['parsedWorkExperienceList']:
                date_from = experience.get('dateFrom', 'Не указано')
                date_to = experience.get('dateTo', 'Не указано')
                duration = 0
                if date_from != 'Не указано' and date_to != 'Не указано':
                    try:
                        date_from_dt = datetime.strptime(date_from.split('T')[0], '%Y-%m-%d')
                        date_to_dt = datetime.strptime(date_to.split('T')[0], '%Y-%m-%d')
                        duration = (date_to_dt - date_from_dt).days / 365.25
                        if duration < 0:
                            duration = 0  # Убираем отрицательные значения
                    except:
                        pass
                experience_record = {
                    'candidateId': row['candidateId'],
                    'companyName': experience.get('companyName', 'Не указано'),
                    'position': experience.get('position', 'Не указано'),
                    'dateFrom': date_from,
                    'dateTo': date_to,
                    'duration': duration
                }
                work_experience_records.append(experience_record)

        # Создадим датафрейм из списка записей о рабочем опыте
        work_experience_df = pd.DataFrame(work_experience_records)

        # Удалим записи с None в колонке duration и преобразуем к числовому типу
        work_experience_df_filtered = work_experience_df.dropna(subset=['duration'])
        work_experience_df_filtered['duration'] = work_experience_df_filtered['duration'].astype(float)

        # Добавим отсутствующие значения 0 лет опыта в набор данных
        if 0 not in work_experience_df_filtered['duration'].values:
            work_experience_df_filtered = work_experience_df_filtered.append({'duration': 0}, ignore_index=True)

        # Фильтруем отрицательные значения продолжительности
        work_experience_df_filtered = work_experience_df_filtered[work_experience_df_filtered['duration'] >= 0]

        # Распределение по количеству лет опыта
        experience_duration_counts = work_experience_df_filtered['duration'].value_counts().sort_index()

        # Частота упоминания различных компаний
        company_counts = work_experience_df['companyName'].value_counts().head(10)

        # Частота упоминания различных должностей
        position_counts = work_experience_df['position'].value_counts().head(10)

        # Выбор графика
        st.title('Анализ данных о рабочем опыте кандидатов')
        chart_type = st.selectbox('Выберите тип графика:', [
            'Распределение по количеству лет опыта',
            'Топ-10 компаний по частоте упоминания',
            'Топ-10 должностей по частоте упоминания'
        ])

        if chart_type == 'Распределение по количеству лет опыта':
            fig = px.line(experience_duration_counts, title='Распределение по количеству лет опыта', labels={'index': 'Количество лет', 'value': 'Количество'}, markers=True)
            st.plotly_chart(fig)
        elif chart_type == 'Топ-10 компаний по частоте упоминания':
            fig = px.bar(company_counts, title='Топ-10 компаний по частоте упоминания', labels={'index': 'Компании', 'value': 'Количество упоминаний'})
            st.plotly_chart(fig)
        elif chart_type == 'Топ-10 должностей по частоте упоминания':
            fig = px.bar(position_counts, title='Топ-10 должностей по частоте упоминания', labels={'index': 'Должности', 'value': 'Количество упоминаний'})
            st.plotly_chart(fig)


    with tab5:

        data = pd.read_csv('/Users/y1ov/Work/project_lab/processed_data_resume.csv')


        # Извлечение и обработка данных для hardSkills
        hard_skills_list = []

        for item in data['hardSkills']:
            if item:  # Проверка на пустую строку или список
                skills = json.loads(item)
                for skill in skills:
                    hard_skills_list.append(skill['hardSkillName'])

        hard_skills_df = pd.DataFrame(hard_skills_list, columns=['hardSkillName'])
        hard_skills_counts = hard_skills_df['hardSkillName'].value_counts()

        # Извлечение и обработка данных для softSkills
        soft_skills_list = []

        for item in data['softSkills']:
            if item:  # Проверка на пустую строку или список
                skills = json.loads(item)
                for skill in skills:
                    soft_skills_list.append(skill['softSkillName'])

        soft_skills_df = pd.DataFrame(soft_skills_list, columns=['softSkillName'])
        soft_skills_counts = soft_skills_df['softSkillName'].value_counts()

        # Интерфейс пользователя
        st.title('Анализ профессиональных навыков')

        skill_type = st.selectbox('Выберите тип навыков:', ['Hard Skills', 'Soft Skills'])

        if skill_type == 'Hard Skills':
            chart_type = st.selectbox('Выберите тип графика:', [
                'Топ-10 навыков (Бар-чарт)',
                'Облако слов',
                'Топ-10 навыков (Круговая диаграмма)'
            ])
            
            if chart_type == 'Топ-10 навыков (Бар-чарт)':
                fig_bar = px.bar(hard_skills_counts.head(10), 
                                x=hard_skills_counts.head(10).index, 
                                y=hard_skills_counts.head(10), 
                                labels={'x': 'Навык', 'y': 'Количество упоминаний'},
                                title='Топ-10 профессиональных навыков')
                st.plotly_chart(fig_bar)

            elif chart_type == 'Облако слов':
                st.header('Облако слов профессиональных навыков')
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(hard_skills_counts)
                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                st.pyplot(plt)

            elif chart_type == 'Топ-10 навыков (Круговая диаграмма)':
                fig_pie = px.pie(hard_skills_counts.head(10), 
                                names=hard_skills_counts.head(10).index, 
                                values=hard_skills_counts.head(10),
                                title='Распределение топ-10 навыков')
                st.plotly_chart(fig_pie)

        elif skill_type == 'Soft Skills':
            chart_type = st.selectbox('Выберите тип графика:', [
                'Топ-10 навыков (Бар-чарт)',
                'Облако слов',
                'Топ-10 навыков (Круговая диаграмма)'
            ])
            
            if chart_type == 'Топ-10 навыков (Бар-чарт)':
                fig_bar = px.bar(soft_skills_counts.head(10), 
                                x=soft_skills_counts.head(10).index, 
                                y=soft_skills_counts.head(10), 
                                labels={'x': 'Навык', 'y': 'Количество упоминаний'},
                                title='Топ-10 мягких навыков')
                st.plotly_chart(fig_bar)

            elif chart_type == 'Облако слов':
                st.header('Облако слов мягких навыков')
                wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(soft_skills_counts)
                plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')
                st.pyplot(plt)

            elif chart_type == 'Топ-10 навыков (Круговая диаграмма)':
                fig_pie = px.pie(soft_skills_counts.head(10), 
                                names=soft_skills_counts.head(10).index, 
                                values=soft_skills_counts.head(10),
                                title='Распределение топ-10 мягких навыков')
                st.plotly_chart(fig_pie)





    
if __name__ == "__main__":
    main()