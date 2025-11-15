import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

plt.rcParams['font.size'] = 12

print("Анализ продаж")

try:
    df = pd.read_excel('lab_4_part_5.xlsx')
    print("Данные загружены")
    if 'Товар' not in df.columns:
        products = ['Телевизоры', 'Смартфоны', 'Ноутбуки', 'Планшеты']
        df['Товар'] = np.random.choice(products, len(df))

    if 'Точка' not in df.columns:
        stores = ['Магазин А', 'Магазин Б', 'Магазин В']
        df['Точка'] = np.random.choice(stores, len(df))

    if 'Количество' not in df.columns:
        df['Количество'] = np.random.randint(1, 20, len(df))

    if 'Продажи' not in df.columns:
        df['Продажи'] = np.random.randint(5000, 50000, len(df))

    if 'Себестоимость' not in df.columns:
        df['Себестоимость'] = df['Продажи'] * 0.6

    if 'Дата' not in df.columns:
        dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
        df['Дата'] = np.random.choice(dates, len(df))

    df['Прибыль'] = df['Продажи'] - df['Себестоимость']
    df['Цена'] = df['Продажи'] / df['Количество']
    df['Месяц'] = pd.to_datetime(df['Дата']).dt.month

    monthly_by_product = df.groupby(['Товар', 'Месяц']).agg({
        'Количество': 'sum',
        'Продажи': 'sum',
        'Себестоимость': 'sum',
        'Цена': 'mean'
    }).reset_index().sort_values(['Товар', 'Месяц'])

    monthly_by_store = df.groupby(['Точка', 'Месяц']).agg({
        'Количество': 'sum',
        'Продажи': 'sum',
        'Себестоимость': 'sum',
        'Цена': 'mean'
    }).reset_index().sort_values(['Точка', 'Месяц'])

    store_monthly_avg_sales = (monthly_by_store
                               .groupby('Точка')['Продажи']
                               .mean()
                               .rename('Средние продажи на точку в месяц')
                               .round(0))

    def growth_summary(group):
        g = group.sort_values('Месяц')
        first_sales, last_sales = g['Продажи'].iloc[0], g['Продажи'].iloc[-1]
        first_qty, last_qty = g['Количество'].iloc[0], g['Количество'].iloc[-1]
        sales_growth = ((last_sales - first_sales) / first_sales * 100) if first_sales != 0 else np.nan
        qty_growth = ((last_qty - first_qty) / first_qty * 100) if first_qty != 0 else np.nan
        return pd.Series({'Рост/спад продаж %': sales_growth, 'Рост/спад количества %': qty_growth})

    growth_by_product = (monthly_by_product
                         .groupby('Товар')
                         .apply(growth_summary)
                         .round(1))

    growth_by_store = (monthly_by_store
                       .groupby('Точка')
                       .apply(growth_summary)
                       .round(1))

    monthly_total_sales = df.groupby('Месяц')['Продажи'].sum().sort_index()

    max_month = df['Месяц'].max()
    next_month = max_month + 1 if max_month < 12 else 13 

    forecasts = []
    for product in df['Товар'].unique():
        series = (df[df['Товар'] == product]
                  .groupby('Месяц')['Продажи'].sum()
                  .sort_index())
        if len(series) > 1:
            X = np.array(series.index).reshape(-1, 1)
            y = series.values
            model = LinearRegression().fit(X, y)
            fc = float(model.predict([[next_month]])[0])
            last_sales = series.iloc[-1]
            change = ((fc - last_sales) / last_sales * 100) if last_sales != 0 else np.nan
            forecasts.append({'Товар': product, 'Последние продажи': last_sales, 'Прогноз': fc, 'Изм.%': change})

    forecast_df = pd.DataFrame(forecasts).round({'Последние продажи': 0, 'Прогноз': 0, 'Изм.%': 1})

    plt.figure(figsize=(12, 6))
    plt.plot(monthly_total_sales.index, monthly_total_sales.values, 'bo-', linewidth=2, label='Продажи')
    plt.title('Общий товарооборот по месяцам')
    plt.xlabel('Месяц')
    plt.ylabel('Продажи')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 6))
    for product in df['Товар'].unique():
        s = (df[df['Товар'] == product]
             .groupby('Месяц')['Продажи'].sum()
             .sort_index())
        plt.plot(s.index, s.values, marker='o', linewidth=2, label=product)
    plt.title('Динамика продаж по месяцам для каждого товара')
    plt.xlabel('Месяц')
    plt.ylabel('Продажи')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 6))
    for store in df['Точка'].unique():
        s = (df[df['Точка'] == store]
             .groupby('Месяц')['Продажи'].sum()
             .sort_index())
        plt.plot(s.index, s.values, marker='o', linewidth=2, label=store)
    plt.title('Динамика продаж по месяцам для каждой точки')
    plt.xlabel('Месяц')
    plt.ylabel('Продажи')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

    avg_price_by_product = df.groupby('Товар')['Цена'].mean().round(0)
    plt.figure(figsize=(10, 6))
    plt.bar(avg_price_by_product.index, avg_price_by_product.values, color='gold')
    plt.title('Средняя цена по товарам')
    plt.xlabel('Товар')
    plt.ylabel('Средняя цена')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.bar(store_monthly_avg_sales.index, store_monthly_avg_sales.values, color='mediumseagreen')
    plt.title('Средние продажи на точку в месяц')
    plt.xlabel('Точка')
    plt.ylabel('Продажи/мес.')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 6))
    for product in df['Товар'].unique():
        s = (df[df['Товар'] == product]
             .groupby('Месяц')['Продажи'].sum()
             .sort_index())
        plt.plot(s.index, s.values, marker='o', linewidth=2, label=f'{product} (факт)')
        if len(s) > 1:
            X = np.array(s.index).reshape(-1, 1)
            y = s.values
            fc = LinearRegression().fit(X, y).predict([[next_month]])[0]
            plt.scatter([next_month], [fc], marker='x', s=120, label=f'{product} (прогноз)')
    plt.title('Факт vs прогноз продаж по товарам')
    plt.xlabel('Месяц')
    plt.ylabel('Продажи')
    plt.grid(True, alpha=0.3)
    plt.legend(ncol=2)
    plt.tight_layout()
    plt.show()

    summary_products = df.groupby('Товар').agg({
        'Количество': 'sum',
        'Продажи': ['sum', 'mean'],
        'Себестоимость': 'sum',
        'Цена': 'mean',
        'Прибыль': 'sum'
    }).round(0)

    print("\nСВОДКА ПО ТОВАРАМ:")
    print(summary_products)

    print("\nРОСТ/СПАД ПО ТОВАРАМ (%):")
    print(growth_by_product)

    print("\nРОСТ/СПАД ПО ТОЧКАМ (%):")
    print(growth_by_store)

    print("\nСРЕДНИЕ ПРОДАЖИ НА ТОЧКУ В МЕСЯЦ:")
    print(store_monthly_avg_sales)

    print("\nПРОГНОЗ НА СЛЕДУЮЩИЙ МЕСЯЦ (по товарам):")
    print(forecast_df)


    df.to_excel('анализ_продаж.xlsx', index=False)
    growth_by_product.to_excel('рост_по_товарам.xlsx')
    growth_by_store.to_excel('рост_по_точкам.xlsx')
    forecast_df.to_excel('прогноз_по_товарам.xlsx', index=False)
    print("\nФайлы сохранены: анализ_продаж.xlsx, рост_по_товарам.xlsx, рост_по_точкам.xlsx, прогноз_по_товарам.xlsx")

except FileNotFoundError:
    print("Файл не найден")
except Exception as e:
    print(f"Ошибка: {e}")
