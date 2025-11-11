def cache(func):
    cache_dict = {}
    
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key in cache_dict:
            print(f"Результат взят из кэша для аргументов {args}")
            return cache_dict[key]
        else:
            print(f"Вычисляем результат для аргументов {args}")
            result = func(*args, **kwargs)
            cache_dict[key] = result
            print(f"Результат сохранен в кэш: {result}")
            return result
    
    return wrapper

@cache
def multiply(a, b):
    result = a * b
    print(f"   Вычисление: {a} * {b} = {result}")
    return result

print("Демонстрация кэширования")

print("Первый вызов multiply(5, 3):")
result1 = multiply(5, 3)
print(f"Результат: {result1}")

print("Второй вызов multiply(5, 3):")
result2 = multiply(5, 3)
print(f"Результат: {result2}")

print("Вызов multiply(4, 7):")
result3 = multiply(4, 7)
print(f"Результат: {result3}")

print("Снова multiply(4, 7):")
result4 = multiply(4, 7)
print(f"Результат: {result4}")