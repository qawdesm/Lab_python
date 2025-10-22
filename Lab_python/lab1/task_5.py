number = int(input("Введите число: "))

if number % 7 == 0:
    print("Магическое число!")
else:
    summa = sum(map(int, str(abs(number))))
    print(f"Сумма цифр: {summa}")