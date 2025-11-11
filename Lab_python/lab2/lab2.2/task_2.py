def merge_dicts(dict_a, dict_b):
    for key, value in dict_b.items():
        if key in dict_a:
            if isinstance(dict_a[key], dict) and isinstance(value, dict):
                merge_dicts(dict_a[key], value)
            else:
                dict_a[key] = value
        else:
            dict_a[key] = value

def main():
    print("Слияние словарей")
    dict_a = {"a": 1, "b": {"c": 1, "f": 4}}
    dict_b = {"d": 1, "b": {"c": 2, "e": 3}}
    
    print("Первый словарь (dict_a):")
    print(dict_a)
    print("Второй словарь (dict_b):")
    print(dict_b)
    
    merge_dicts(dict_a, dict_b)
    
    print("Результат слияния (dict_a после объединения):")
    print(dict_a)

main()