import numpy as np

expenses = []
months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
          'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

print("Введите расходы на проезд за каждый месяц:")
for i, month in enumerate(months, 1):
    expense = float(input(f"{month}: "))
    expenses.append(expense)

expenses = np.array(expenses)


winter_indices = [11, 0, 1]
summer_indices = [5, 6, 7]

winter_expenses = np.sum(expenses[winter_indices])
summer_expenses = np.sum(expenses[summer_indices])

print(f"Результаты анализа:")
print(f"Зимние месяцы: {winter_expenses:.2f} руб.")
print(f"Летние месяцы: {summer_expenses:.2f} руб.")

if winter_expenses > summer_expenses:
    print("Больше тратится в зимний период")
elif summer_expenses > winter_expenses:
    print("Больше тратится в летний период")
else:
    print("Расходы равны в оба периода")

max_value = np.max(expenses)
max_months_indices = np.where(expenses == max_value)[0]

print(f"\nМаксимальные расходы: {max_value:.2f} руб.")
print("Месяцы с максимальными расходами:")
for idx in max_months_indices:
    print(f"{months[idx]} ({idx + 1})")
