surname = input("Введите фамилию: ")
name = input("Введите имя: ")
patronymic = input("Введите отчество: ")
fio = f"{surname} {name[0]}.{patronymic[0]}." if name and patronymic else f"{surname} {name[0]}." if name else surname
print(f"Результат форматирования: {fio}")