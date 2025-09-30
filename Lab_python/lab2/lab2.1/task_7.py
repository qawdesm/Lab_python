text = input("Введите строку: ")

if not text:
    print("Вы ничего не ввели!")
else:
    if len(text) == 1:
        print(f"Результат: {text}1")
    else:
        result = ""
        count = 1
        
        for i in range(len(text) - 1):
            if text[i] == text[i + 1]:
                count += 1
            else:
                result += text[i] + str(count)
                count = 1
                
        result += text[-1] + str(count)
        
        print(f"Исходная строка: {text}")
        print(f"Сжатая строка: {result}")