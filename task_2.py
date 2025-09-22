input_string = input("Введите строку: ")
remove = 'aeiou'
translation_table = str.maketrans('', '', remove)
result = input_string.translate(translation_table)
print(f"Строка после удаления гласных {remove}: {result}")