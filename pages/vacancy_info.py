import pandas as pd
import streamlit as st
import json
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

    tab2, tab5 = st.tabs(["Категории вакансий", "Навыки"])
    
    with tab2:
        file_path = '/Users/y1ov/Work/project_lab/processed_data_vacancy.csv'  # Замените на путь к вашему файлу
        data = pd.read_csv(file_path)

        # Классификация профессиональных сфер
        sphere_categories = {
            'управленческие': ['менеджмент', 'управление', 'администрация'],
            'технические': ['инженерия', 'технологии', 'ИТ', 'разработка'],
            'образование и наука': ['образование', 'наука', 'исследования'],
            'финансовые': ['финансы', 'бухгалтерия', 'экономика'],
            'продажи и обслуживание': ['продажи', 'обслуживание', 'маркетинг'],
            'транспорт и логистика': ['транспорт', 'логистика', 'склад'],
            'медицина': ['медицина', 'здравоохранение'],
            'производство': ['производство', 'индустрия'],
            'прочие': ['другое']
        }

        def classify_sphere(sphere):
            for category, keywords in sphere_categories.items():
                if any(keyword in sphere.lower() for keyword in keywords):
                    return category
            return 'прочие'

        data['sphereCategory'] = data['professionalSphereName'].apply(classify_sphere)
        category_counts = data['sphereCategory'].value_counts()

        st.title('Анализ категорий вакансий')
        chart_type = st.selectbox('Выберите тип графика:', [
            'Распределение вакансий по категориям'
        ])

        if chart_type == 'Распределение вакансий по категориям':
            fig = px.bar(category_counts, title='Распределение вакансий по категориям', labels={'index': 'Категория', 'value': 'Количество вакансий'})
            st.plotly_chart(fig)

    with tab5:
        st.title('Анализ профессиональных навыков')
        file_path = '/Users/y1ov/Work/project_lab/processed_data_vacancy.csv'

        data = pd.read_csv(file_path)

        hard_skills_list = []
        soft_skills_list = []

        for item in data['hardSkills']:
            if item:
                skills = json.loads(item)
                for skill in skills:
                    hard_skills_list.append(skill['hard_skill_name'])

        for item in data['softSkills']:
            if item:
                skills = json.loads(item)
                for skill in skills:
                    soft_skills_list.append(skill['soft_skill_name'])

        hard_skills_df = pd.DataFrame(hard_skills_list, columns=['hardSkillName'])
        soft_skills_df = pd.DataFrame(soft_skills_list, columns=['softSkillName'])

        hard_skills_counts = hard_skills_df['hardSkillName'].value_counts()
        soft_skills_counts = soft_skills_df['softSkillName'].value_counts()

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

