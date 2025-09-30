user_input = input("Введите числа через пробел: ")

if not user_input:
    print("Вы ничего не ввели!")
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
            print(f"'{item}' - не число, пропускаем")
    
    if not numbers:
        print("Нет чисел для анализа!")
    else:
        print("РЕЗУЛЬТАТЫ:")
        
        unique = []
        for num in numbers:
            if num not in unique:
                unique.append(num)
        print(f"1. Уникальные числа: {unique}")
        
        repeats = []
        for num in unique:
            if numbers.count(num) > 1:
                repeats.append(num)
        print(f"2. Повторяющиеся: {repeats if repeats else 'нет'}")
        
        even = []
        odd = []
        for num in numbers:
            if isinstance(num, int):
                if num % 2 == 0:
                    even.append(num)
                else:
                    odd.append(num)
        print(f"3. Четные: {even if even else 'нет'}")
        print(f"   Нечетные: {odd if odd else 'нет'}")
        
        negative = []
        for num in numbers:
         if num < 0:
          negative.append(num)
        print(f"4. Отрицательные: {negative if negative else 'нет'}")
        
        floats = []
        for num in numbers:
         if isinstance(num, float):
          floats.append(num)
        print(f"5. Дробные: {floats if floats else 'нет'}")
        
        multiples_5 = []
        for num in numbers:
         if num % 5 == 0:
          multiples_5.append(num)
        total_5 = sum(multiples_5)
        print(f"6. Сумма кратных 5: {total_5}")
        print(f"   Числа: {multiples_5}")
        
        print(f"7. Самое большое: {max(numbers)}")
        print(f"8. Самое маленькое: {min(numbers)}")
        
        print(f"\nВсе числа: {numbers}")