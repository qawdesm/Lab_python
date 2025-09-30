def transpose_matrix(matrix):
    if not matrix or not matrix[0]:
        return []
    
    rows = len(matrix)
    cols = len(matrix[0])
    
    result = []
    for j in range(cols):
        new_row = []
        for i in range(rows):
            new_row.append(matrix[i][j])
        result.append(new_row)
    
    return result

print("Транспонирование матрицы")
print("Введите матрицу построчно.")
print("Введите числа через пробел для каждой строки.")
print("Для завершения ввода введите пустую строку.")

matrix = []
row_number = 1

while True:
    row_input = input(f"Строка {row_number}: ").strip()
    
    if not row_input:
        break
    
    row = [int(x) for x in row_input.split()]
    matrix.append(row)
    row_number += 1

if not matrix:
    print("Матрица пустая! Транспонирование невозможно.")
else:
    print("Исходная матрица:")
    for row in matrix:
        print(row)

    transposed = transpose_matrix(matrix)

    print("Транспонированная матрица:")
    for row in transposed:
        print(row)

    print("Исходная матрица (не изменилась):")
    for row in matrix:
        print(row)