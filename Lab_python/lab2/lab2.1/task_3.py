user_input = input("Введите числа через пробел: ")

if not user_input:
    print("Вы ничего не ввели")
else:
    items = user_input.split()
    numbers = []
    
    for item in items:
        if item.replace('.', '').replace('-', '').isdigit():
            if '.' in item:
                numbers.append(float(item))
            else:
                numbers.append(int(item))
        else:
            print(f"'{item}' - не число")
    
    if not numbers:
        print("Нет чисел")
    else:
        if len(numbers) < 2:
            print("Нужно ввести хотя бы 2 числа")
        else:
            unique_sorted = sorted(set(numbers))
            
            if len(unique_sorted) < 2:
                print("Все числа одинаковые")
            else:
                second_largest = unique_sorted[-2]
                print(f"Второе по величине число: {second_largest}")