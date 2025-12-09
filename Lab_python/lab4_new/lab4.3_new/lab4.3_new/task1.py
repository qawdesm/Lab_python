import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from faker import Faker
import random
from datetime import datetime

fake = Faker('ru_RU')
np.random.seed(42)
random.seed(42)

print("Генерация данных о вступительной кампании")

years = [2019, 2020, 2021, 2022, 2023]
specialties = [
    'Прикладная математика', 'Прикладная информатика', 'Кибербезопасность', 
    'Лечебное дело', 'Психология', 'Философия', 'Радиофизика', 
    'Международные отношения', 'Информатика', 'История'
]
subjects = ['Математика', 'Физика', 'Химия', 'Биология', 'История', 'Русский язык']
study_forms = ['Бюджет', 'Платка', 'Целевое']
regions = ['Минск', 'Гродно', 'Брест', 'Витебск', 'Гомель', 'Могилев', 'Минская обл.']

def generate_student_data(num_students=1000):
    data = []
    
    for _ in range(num_students):
        year = random.choice(years)
        fio = fake.name()
        study_form = random.choice(study_forms)
        
        base_score = np.random.normal(70, 15) + (year - 2019) * 2

        selected_subjects = random.sample(subjects, 3)
        
        ct_scores = {subject: min(100, max(0, int(np.random.normal(base_score, 10)))) 
                    for subject in selected_subjects}
        
        certificate_score = min(10, max(4, np.random.normal(7.5, 1.2)))
        
        specialty = random.choice(specialties)

        if specialty in ['Прикладная математика', 'Прикладная информатика', 'Кибербезопасность', 'Информатика']:
            if 'Математика' in ct_scores:
                ct_scores['Математика'] = min(100, ct_scores['Математика'] + 12)
            if 'Физика' in ct_scores:
                ct_scores['Физика'] = min(100, ct_scores['Физика'] + 8)
        elif specialty == 'Радиофизика':
            if 'Физика' in ct_scores:
                ct_scores['Физика'] = min(100, ct_scores['Физика'] + 15)
            if 'Математика' in ct_scores:
                ct_scores['Математика'] = min(100, ct_scores['Математика'] + 10)
        elif specialty == 'Лечебное дело':
            if 'Химия' in ct_scores:
                ct_scores['Химия'] = min(100, ct_scores['Химия'] + 15)
            if 'Биология' in ct_scores:
                ct_scores['Биология'] = min(100, ct_scores['Биология'] + 12)
        elif specialty in ['Психология', 'Философия']:
            if 'История' in ct_scores:
                ct_scores['История'] = min(100, ct_scores['История'] + 10)
            if 'Русский язык' in ct_scores:
                ct_scores['Русский язык'] = min(100, ct_scores['Русский язык'] + 8)
        elif specialty == 'Международные отношения':
            if 'История' in ct_scores:
                ct_scores['История'] = min(100, ct_scores['История'] + 12)
            if 'Русский язык' in ct_scores:
                ct_scores['Русский язык'] = min(100, ct_scores['Русский язык'] + 10)
        elif specialty == 'История':
            if 'История' in ct_scores:
                ct_scores['История'] = min(100, ct_scores['История'] + 15)
            if 'Русский язык' in ct_scores:
                ct_scores['Русский язык'] = min(100, ct_scores['Русский язык'] + 10)
        
        total_score = sum(ct_scores.values()) + certificate_score * 10
        
        student = {
            'ФИО': fio,
            'Год_поступления': year,
            'Форма_обучения': study_form,
            'Средний_балл_аттестата': round(certificate_score, 1),
            'Общий_балл': round(total_score, 1),
            'Специальность': specialty,
            'Адрес_регистрации': fake.city(),
            'Телефон': fake.phone_number()
        }
        
        student.update({f'ЦТ_{subject}': score for subject, score in ct_scores.items()})
        data.append(student)
    
    return pd.DataFrame(data)


df = generate_student_data(1500)
print(f"Сгенерировано записей: {len(df)}")
print("\nПервые 5 записей:")
print(df.head())

print("\nОсновная статистика:")
print(df.describe())

print("Отображение данных")


plt.figure(figsize=(15, 12))
plt.subplot(3, 2, 1)
ct_columns = [f'ЦТ_{subject}' for subject in subjects]
ct_yearly = df.groupby('Год_поступления')[ct_columns].mean()

for subject in subjects:
    plt.plot(ct_yearly.index, ct_yearly[f'ЦТ_{subject}'], 
             marker='o', label=subject, linewidth=2)

plt.title('Динамика среднего балла ЦТ по предметам', fontsize=12, fontweight='bold')
plt.xlabel('Год')
plt.ylabel('Средний балл')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.xticks(years)

plt.subplot(3, 2, 2)
certificate_yearly = df.groupby('Год_поступления')['Средний_балл_аттестата'].mean()
plt.plot(certificate_yearly.index, certificate_yearly.values, 
         marker='o', color='red', linewidth=2, markersize=8)
plt.title('Динамика среднего балла аттестата', fontsize=12, fontweight='bold')
plt.xlabel('Год')
plt.ylabel('Средний балл аттестата')
plt.grid(True, alpha=0.3)
plt.xticks(years)

plt.subplot(3, 2, 3)
top_specialties = df['Специальность'].value_counts().head(5).index
passing_scores = df.groupby(['Год_поступления', 'Специальность'])['Общий_балл'].min().reset_index()

for specialty in top_specialties:
    specialty_data = passing_scores[passing_scores['Специальность'] == specialty]
    plt.plot(specialty_data['Год_поступления'], specialty_data['Общий_балл'], 
             marker='s', label=specialty, linewidth=2)

plt.title('Динамика проходного балла', fontsize=12, fontweight='bold')
plt.xlabel('Год')
plt.ylabel('Проходной балл')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.xticks(years)

plt.subplot(3, 2, 4)
specialty_counts = df['Специальность'].value_counts()
colors = plt.cm.Set3(np.linspace(0, 1, len(specialty_counts)))

bars = plt.bar(specialty_counts.index, specialty_counts.values, color=colors)
plt.title('Количество поступивших по специальностям', fontsize=12, fontweight='bold')
plt.xlabel('Специальность')
plt.ylabel('Количество студентов')
plt.xticks(rotation=45, ha='right')

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}', ha='center', va='bottom')

plt.subplot(3, 2, 5)
study_form_counts = df['Форма_обучения'].value_counts()
plt.pie(study_form_counts.values, labels=study_form_counts.index, autopct='%1.1f%%',
        colors=['#ff9999', '#66b3ff','#99ff99'])
plt.title('Распределение по формам обучения', fontsize=12, fontweight='bold')

plt.subplot(3, 2, 6)
box_data = [df[df['Год_поступления'] == year]['Общий_балл'] for year in years]
plt.boxplot(box_data, labels=years)
plt.title('Распределение общего балла по годам', fontsize=12, fontweight='bold')
plt.xlabel('Год поступления')
plt.ylabel('Общий балл')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

df.to_csv('admission_data_2019_2023.csv', index=False, encoding='utf-8-sig')
print(f"\nДанные сохранены в файл: admission_data_2019_2023.csv")
