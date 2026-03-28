import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.linear_model import LinearRegression

plt.style.use('default')
sns.set_palette("husl")

df = pd.read_excel('s7_data_sample_rev4_50k.xlsx', sheet_name='DATA')
df['FLIGHT_DATE_LOC'] = pd.to_datetime(df['FLIGHT_DATE_LOC'])
df['FLIGHT_MONTH'] = df['FLIGHT_DATE_LOC'].dt.to_period('M')

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

n, bins, patches = axes[0,0].hist(df['REVENUE_AMOUNT'], bins=40, color='lightblue', alpha=0.7)
axes[0,0].set_xlabel('Выручка')
axes[0,0].set_ylabel('Частота')
axes[0,0].set_title('Распределение выручки')
axes[0,0].grid(True, alpha=0.3)

for i in range(len(n)):
    if n[i] > 0:
        axes[0,0].text(bins[i] + (bins[i+1]-bins[i])/2, n[i] + 10,
                      f'{int(n[i])}', ha='center', va='bottom', fontsize=7)

top_airports = df['ORIG_CITY_CODE'].value_counts().head(6)
bars = axes[0,1].bar(top_airports.index, top_airports.values, color='coral')
axes[0,1].set_xlabel('Аэропорт')
axes[0,1].set_ylabel('Вылеты')
axes[0,1].set_title('Топ аэропортов')
axes[0,1].tick_params(axis='x', rotation=45)
axes[0,1].grid(True, alpha=0.3, axis='y')

for bar in bars:
    height = bar.get_height()
    axes[0,1].text(bar.get_x() + bar.get_width()/2., height + max(top_airports.values)*0.01,
                   f'{int(height):,}', ha='center', va='bottom', fontsize=9)

monthly_counts = df.groupby('FLIGHT_MONTH').size()
axes[1,0].plot(monthly_counts.index.astype(str), monthly_counts.values, marker='o')
axes[1,0].set_xlabel('Месяц')
axes[1,0].set_ylabel('Перелеты')
axes[1,0].set_title('Перелеты по месяцам')
axes[1,0].tick_params(axis='x', rotation=90)
axes[1,0].grid(True, alpha=0.3)

for i, (month, count) in enumerate(zip(monthly_counts.index.astype(str), monthly_counts.values)):
    axes[1,0].text(i, count + max(monthly_counts.values)*0.01, f'{int(count):,}', 
                   ha='center', va='bottom', fontsize=8, rotation=0)

pax_data = df['PAX_TYPE'].value_counts()
wedges, texts, autotexts = axes[1,1].pie(pax_data.values, labels=pax_data.index, autopct='%1.1f%%')
axes[1,1].set_title('Типы пассажиров')

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

fop_data = df['FOP_TYPE_CODE'].value_counts().head(5)
bars = axes[0].bar(fop_data.index, fop_data.values, color='lightgreen')
axes[0].set_xlabel('Способ оплаты')
axes[0].set_ylabel('Транзакции')
axes[0].set_title('Топ способы оплаты')
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(True, alpha=0.3, axis='y')

for bar in bars:
    height = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2., height + max(fop_data.values)*0.01,
                 f'{int(height):,}', ha='center', va='bottom', fontsize=9)

monthly_counts = df.groupby('FLIGHT_MONTH').size()
monthly_revenue = df.groupby('FLIGHT_MONTH')['REVENUE_AMOUNT'].sum()

revenue_normalized = monthly_revenue.values / 100 

X = np.array(range(len(monthly_counts))).reshape(-1, 1)
y_counts = monthly_counts.values
model_counts = LinearRegression().fit(X, y_counts)

y_revenue = monthly_revenue.values
model_revenue = LinearRegression().fit(X, y_revenue)

future_months = 3
X_future = np.array(range(len(monthly_counts), len(monthly_counts) + future_months)).reshape(-1, 1)
predictions_counts = model_counts.predict(X_future)
predictions_revenue = model_revenue.predict(X_future)

axes[1].plot(range(len(monthly_counts)), monthly_counts.values, 'bo-', 
             label='Перелеты (факт)', linewidth=2, markersize=5)
axes[1].plot(range(len(monthly_counts)), revenue_normalized, 'gs-',
             label=f'Выручка (факт, ×1000 руб)', linewidth=2, markersize=5)
axes[1].plot(range(len(monthly_counts), len(monthly_counts) + future_months), 
             predictions_counts, 'ro--', label='Перелеты (прогноз)', linewidth=2, markersize=7)
axes[1].plot(range(len(monthly_counts), len(monthly_counts) + future_months),
             predictions_revenue/100, 'rs--', label='Выручка (прогноз, ×1000 руб)', linewidth=2, markersize=7)

axes[1].set_xlabel('Период (месяцы)')
axes[1].set_ylabel('Перелеты / Выручка (×1000 руб)')
axes[1].set_title('Прогноз перелетов и выручки')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

for i, count in enumerate(monthly_counts.values):
   # if i % 3 == 0:
        axes[1].text(i, count + max(monthly_counts.values)*0.03, f'{int(count):,}', 
                     ha='center', va='bottom', fontsize=8, color='blue')

for i, revenue in enumerate(revenue_normalized):
   # if i % 3 == 0:
        axes[1].text(i, revenue + max(revenue_normalized)*0.03, f'{int(monthly_revenue.values[i]/1000):,}K', 
                     ha='center', va='bottom', fontsize=8, color='green')

for i, pred in enumerate(predictions_counts):
    axes[1].text(len(monthly_counts) + i, pred, f'{int(pred):,}', 
                 ha='center', va='bottom', fontsize=9, color='red', fontweight='bold')

for i, pred in enumerate(predictions_revenue):
    axes[1].text(len(monthly_counts) + i, pred/100, f'{int(pred/1000):,}K', 
                 ha='center', va='bottom', fontsize=9, color='red', fontweight='bold')

plt.tight_layout()
plt.show()

print(f"Общая выручка: {df['REVENUE_AMOUNT'].sum():,.0f}")
print(f"Средний чек: {df['REVENUE_AMOUNT'].mean():.0f}")
print(f"Всего перелетов: {len(df):,}")
print(f"Главные аэропорты: {', '.join(top_airports.head(3).index.tolist())}")
print(f"Основные пассажиры: {pax_data.index[0]} ({pax_data.iloc[0]} билетов)")
print(f"Популярная оплата: {fop_data.index[0]}")
print(f"\nПрогноз на следующие {future_months} месяца:")
for i in range(future_months):
    avg_check = predictions_revenue[i] / predictions_counts[i] if predictions_counts[i] > 0 else 0
    print(f"  Месяц {i+1}: {predictions_counts[i]:.0f} перелетов, {predictions_revenue[i]:,.0f} руб (ср. чек: {avg_check:.0f} руб)")