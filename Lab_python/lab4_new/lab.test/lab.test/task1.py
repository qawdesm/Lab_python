# новая ветка новое вирт окруж питон 3.10 сгенерируем данные виды украшений(верьги кольца повески и т д )
# стрна производитель материалл(золото серебро белое золото красное золото )с драгоценными камнями или без цена за один грамь металла
# считаю стоимоть увелирного изделия(вес на цену за грам)если есть дроагоценный камень умножаем на 2 
# визуализация по распределение по виду украшений(какие и сколько)
# распределение которые имеет дарагоценнве камни или нет для каждого вида изделия
# по стране производства по каждому вижу
# все проданное(цена) по видам типо (одна ось количество) вторая цена  
from faker import Faker
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

fake=Faker('ru_RU')

np.random.seed(42)
random.seed(42)

ykr = ["серьги", "кольца", "подвески", "браслеты", "колье"]
#country = ["Россия", "Турция", "Беларусь", "Греция", "Болгария"]
material = ["золото", "белое золото", "красное золото", "серебро"]
stones = ["фианит", "изумруд", "бриллиант", "нет", "нет"]
price = {"золото": 250, "белое золото": 350, "красное золото": 300, "серебро": 5}
n = 10

data = {
    "вид украшения": [fake.random_element(ykr) for _ in range(n)],
    "страна производства": [fake.country() for _ in range(n)],
    "материал": [fake.random_element(material) for _ in range(n)],
    "драгоценный камень": [fake.random_element(stones) for _ in range(n)],
    "вес": [round(fake.pyfloat(min_value=1, max_value=50, right_digits=2), 2) for _ in range(n)]
}

df = pd.DataFrame(data)

df["цена за грамм"] = df["материал"].map(price)
df["стоимость металла"] = df["вес"] * df["цена за грамм"]
df["есть камень"] = df["драгоценный камень"] != "нет"
df["итоговая стоимость"] = df.apply(
    lambda row: row["стоимость металла"] * 2 if row["есть камень"] else row["стоимость металла"],
    axis=1
)

print("Сгенерированные данные:")
print(df.head(10))

fig, axs = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Анализ ювелирных изделий', fontsize=16)

ax1 = axs[0, 0]
type_counts = df['вид украшения'].value_counts()
wedges, texts, autotexts = ax1.pie(type_counts.values, labels=type_counts.index, 
                                   autopct='%1.1f%%', startangle=90)

ax1.set_title('1. Распределение по виду украшений (круговая диаграмма)', fontsize=12)
ax1.axis('equal')

ax2 = axs[0, 1]
stone_by_type = pd.crosstab(df['вид украшения'], df['есть камень'])
stone_by_type.columns = ['Без камней', 'С камнями']
bars = stone_by_type.plot(kind='bar', ax=ax2, color=['red', 'green'])
ax2.set_title('2. Наличие драгоценных камней по видам украшений', fontsize=12)
ax2.set_xlabel('Вид украшения')
ax2.set_ylabel('Количество')
ax2.tick_params(axis='x', rotation=45)
ax2.legend(title='Наличие камня')
ax2.grid(axis='y', alpha=0.3)

for container in ax2.containers:
    ax2.bar_label(container, fmt='%d', padding=3, fontsize=9)

ax3 = axs[1, 0]
country_by_type = pd.crosstab(df['вид украшения'], df['страна производства'])
bars = country_by_type.plot(kind='bar', ax=ax3, width=0.8)
ax3.set_title('3. Страны производства по видам украшений', fontsize=12)
ax3.set_xlabel('Вид украшения')
ax3.set_ylabel('Количество')
ax3.tick_params(axis='x', rotation=45)
ax3.legend(title='Страна производства', fontsize=8)
ax3.grid(axis='y', alpha=0.3)

for container in ax3.containers:
    ax3.bar_label(container, fmt='%d', padding=3, fontsize=8)

ax4 = axs[1, 1]
summary = df.groupby('вид украшения').agg({
    'итоговая стоимость': 'sum',
    'вид украшения': 'count'
}).rename(columns={'вид украшения': 'количество', 'итоговая стоимость': 'общая стоимость'})

ax4_primary = ax4
bars4 = ax4_primary.bar(summary.index, summary['количество'], alpha=0.7, 
                        color='gold', label='Количество', width=0.4)
ax4_primary.set_xlabel('Вид украшения')
ax4_primary.set_ylabel('Количество', color='darkgoldenrod')
ax4_primary.tick_params(axis='y', labelcolor='darkgoldenrod')
ax4_primary.tick_params(axis='x', rotation=45)

for bar in bars4:
    height = bar.get_height()
    ax4_primary.text(bar.get_x() + bar.get_width()/2, height + 0.1, 
                     f'{int(height)}', ha='center', va='bottom', color='darkgoldenrod')

ax4_secondary = ax4_primary.twinx()
line4 = ax4_secondary.plot(summary.index, summary['общая стоимость'], color='darkred', 
                           marker='o', linewidth=2, markersize=8, label='Общая стоимость')
ax4_secondary.set_ylabel('Общая стоимость (руб)', color='darkred')
ax4_secondary.tick_params(axis='y', labelcolor='darkred')

ax4.set_title('4. Количество и общая стоимость по видам украшений', fontsize=12)

lines1, labels1 = ax4_primary.get_legend_handles_labels()
lines2, labels2 = ax4_secondary.get_legend_handles_labels()
ax4_secondary.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

for idx, (type_name, cost) in enumerate(zip(summary.index, summary['общая стоимость'])):
    ax4_secondary.text(idx, cost + max(summary['общая стоимость']) * 0.02, 
                      f'{cost:,.0f}', ha='center', va='bottom', color='darkred', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.show()

