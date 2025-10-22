day = int(input("Введите день рождения (число): "))
month = int(input("Введите месяц рождения (число от 1 до 12): "))

user_day = day
user_month = month

if (month == 12 and day >= 23) or (month == 1 and day <= 20):
    sign = "Козерог"
elif (month == 1 and day >= 21) or (month == 2 and day <= 19):
    sign = "Водолей"
elif (month == 2 and day >= 20) or (month == 3 and day <= 20):
    sign = "Рыбы"
elif (month == 3 and day >= 21) or (month == 4 and day <= 20):
    sign = "Овен"
elif (month == 4 and day >= 21) or (month == 5 and day <= 21):
    sign = "Телец"
elif (month == 5 and day >= 22) or (month == 6 and day <= 21):
    sign = "Близнецы"
elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
    sign = "Рак"
elif (month == 7 and day >= 23) or (month == 8 and day <= 23):
    sign = "Лев"
elif (month == 8 and day >= 24) or (month == 9 and day <= 23):
    sign = "Дева"
elif (month == 9 and day >= 24) or (month == 10 and day <= 23):
    sign = "Весы"
elif (month == 10 and day >= 24) or (month == 11 and day <= 22):
    sign = "Скорпион"
elif (month == 11 and day >= 23) or (month == 12 and day <= 21):
    sign = "Стрелец"
else:
    sign = "Неверная дата"

print(f"Введенная дата: {user_day} день {user_month} месяц в году ")
print(f"Ваш знак зодиака: {sign}")