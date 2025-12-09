import numpy as np

A = np.array([
    [-2, -8.5, -3.4, 3.5],
    [0, 2.4, 0, 8.2],
    [2.5, 1.6, 2.1, 3],
    [0.3, -0.4, -4.8, 4.6]
])

B = np.array([-1.88, -3.28, -0.5, -2.83])

print("Матрица коэффициентов A:")
print(A)
print("Вектор правых частей B:")
print(B)


if np.linalg.det(A) == 0:
    print("Матрица A вырождена, система не имеет единственного решения")
else:
   
    X = np.linalg.inv(A) @ B
    
    print("Решение системы уравнений:")
    print(f"x1 = {X[0]:.1f}")
    print(f"x2 = {X[1]:.1f}")
    print(f"x3 = {X[2]:.1f}")
    print(f"x4 = {X[3]:.1f}")
    
    print(f"Вектор решения X (округленный до одного знака):")
    print(np.round(X, 1))
    
    print("\nПроверка: A * X =")
    check = A @ X
    print(check)
    print("Должно быть равно B:")
    print(B)
