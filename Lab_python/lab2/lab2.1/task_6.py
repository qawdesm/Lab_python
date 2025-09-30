user_input = input("Введите элементы списка через пробел: ")

if not user_input:
    print("Вы ничего не ввели!")
else:
    items = user_input.split()
    unique_items = []
    
    for item in items:
        if item not in unique_items:
            unique_items.append(item)
    
    print(f"Исходный список: {items}")
    print(f"Список без дубликатов: {unique_items}")