input1 = input("Введите первый набор чисел через пробел: ")
input2 = input("Введите второй набор чисел через пробел: ")

numbers1 = []
for item in input1.split():
    if item.replace('.', '').replace('-', '').isdigit():
        numbers1.append(float(item) if '.' in item else int(item))

numbers2 = []
for item in input2.split():
    if item.replace('.', '').replace('-', '').isdigit():
        numbers2.append(float(item) if '.' in item else int(item))

if numbers1 and numbers2:
    print("\nРЕЗУЛЬТАТЫ:")
    
    common = []
    for num in numbers1:
        if num in numbers2 and num not in common:
            common.append(num)
    print(f"1. Общие числа: {common}")
    
    only1 = []
    for num in numbers1:
        if num not in numbers2:
            only1.append(num)
    
    only2 = []
    for num in numbers2:
        if num not in numbers1:
            only2.append(num)
    
    print(f"2. Только в первом: {only1}")
    print(f"   Только во втором: {only2}")
    
    all_except_common = only1 + only2
    print(f"3. Все кроме общих: {all_except_common}")

else:
    print("Нужно ввести числа в оба набора!")