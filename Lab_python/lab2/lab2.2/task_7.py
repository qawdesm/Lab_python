def merge_sorted_list(list1, list2):
    result = []
    i = 0
    j = 0
    
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1
    
    while i < len(list1):
        result.append(list1[i])
        i += 1
        
    while j < len(list2):
        result.append(list2[j])
        j += 1
    
    return result

print("Введите первый отсортированный список (числа через пробел):")
input1 = input("Первый список: ")
list_a = [int(x) for x in input1.split()]

print("Введите второй отсортированный список (числа через пробел):")
input2 = input("Второй список: ")
list_b = [int(x) for x in input2.split()]

print("Первый список:", list_a)
print("Второй список:", list_b)

merged = merge_sorted_list(list_a, list_b)

print("Результат слияния:", merged)