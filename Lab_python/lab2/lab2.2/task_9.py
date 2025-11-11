def type_check(*expected_types):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if len(args) != len(expected_types):
                raise TypeError(
                    f"Функция '{func.__name__}' ожидает {len(expected_types)} "
                    f"аргументов, но получено {len(args)}"
                )
            
            for i, (arg, expected_type) in enumerate(zip(args, expected_types)):
                if type(arg) is not expected_type:
                    raise TypeError(
                        f"Аргумент {i+1} функции '{func.__name__}' должен быть "
                        f"{expected_type.__name__}, получен {type(arg).__name__}"
                    )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@type_check(int, int)
def multiply(a, b):
    result = a * b
    print(f"Результат: {a} * {b} = {result}")
    return result

print("Проверка типов параметров")

print("Корректный вызов:")
multiply(4, 5)

print("Некорректный вызов:")
multiply(4, "5")