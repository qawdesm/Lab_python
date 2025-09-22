seconds = int(input("Введите количество секунд: "))
minutes = seconds // 60
new_seconds = seconds % 60
print(f"{seconds} секунд - это {minutes} минут {new_seconds} секунд")