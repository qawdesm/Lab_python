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

axes[0,0].hist(df['REVENUE_AMOUNT'], bins=40, color='lightblue', alpha=0.7)
axes[0,0].set_xlabel('Выручка')
axes[0,0].set_ylabel('Частота')
axes[0,0].set_title('Распределение выручки')

top_airports = df['ORIG_CITY_CODE'].value_counts().head(6)
axes[0,1].bar(top_airports.index, top_airports.values, color='coral')
axes[0,1].set_xlabel('Аэропорт')
axes[0,1].set_ylabel('Вылеты')
axes[0,1].set_title('Топ аэропортов')
axes[0,1].tick_params(axis='x', rotation=45)

monthly_counts = df.groupby('FLIGHT_MONTH').size()
axes[1,0].plot(monthly_counts.index.astype(str), monthly_counts.values, marker='o')
axes[1,0].set_xlabel('Месяц')
axes[1,0].set_ylabel('Перелеты')
axes[1,0].set_title('Перелеты по месяцам')
axes[1,0].tick_params(axis='x', rotation=90)

pax_data = df['PAX_TYPE'].value_counts()
axes[1,1].pie(pax_data.values, labels=pax_data.index, autopct='%1.1f%%')
axes[1,1].set_title('Типы пассажиров')

plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

fop_data = df['FOP_TYPE_CODE'].value_counts().head(5)
axes[0].bar(fop_data.index, fop_data.values, color='lightgreen')
axes[0].set_xlabel('Способ оплаты')
axes[0].set_ylabel('Транзакции')
axes[0].set_title('Топ способы оплаты')
axes[0].tick_params(axis='x', rotation=45)

monthly_forecast = df.groupby('FLIGHT_MONTH').size()
X = np.array(range(len(monthly_forecast))).reshape(-1, 1)
y = monthly_forecast.values
model = LinearRegression().fit(X, y)
future = [[len(monthly_forecast)]]
pred = model.predict(future)

axes[1].plot(range(len(monthly_forecast)), monthly_forecast.values, 'bo-', label='Факт')
axes[1].plot(len(monthly_forecast), pred[0], 'ro', markersize=8, label='Прогноз')
axes[1].set_xlabel('Период')
axes[1].set_ylabel('Перелеты')
axes[1].set_title('Прогноз перелетов')
axes[1].legend()

plt.tight_layout()
plt.show()

print(f"Общая выручка: {df['REVENUE_AMOUNT'].sum():,.0f}")
print(f"Средний чек: {df['REVENUE_AMOUNT'].mean():.0f}")
print(f"Всего перелетов: {len(df):,}")
print(f"Главные аэропорты: {', '.join(top_airports.head(3).index.tolist())}")
print(f"Основные пассажиры: {pax_data.index[0]} ({pax_data.iloc[0]} билетов)")
print(f"Популярная оплата: {fop_data.index[0]}")
print(f"Прогноз: {pred[0]:.0f} перелетов")