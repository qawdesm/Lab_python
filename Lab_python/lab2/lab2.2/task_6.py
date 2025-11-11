def unique_elements(nested_list):
    result = []
    
    def extract_elements(lst):
        for item in lst:
            if isinstance(item, list):
                extract_elements(item)
            else:
                is_duplicate = False
                for existing_item in result:
                    if existing_item == item:
                        is_duplicate = True
                        break
                if not is_duplicate:
                    result.append(item)
    
    extract_elements(nested_list)
    return result

list_a = [1, 2, 3, [4, 3, 1], 5, [6, [7, [10], 8, [9, 2, 3]]]]

print("Исходный список:")
print(list_a)

unique = unique_elements(list_a)

print("Уникальные элементы:")
print(unique)