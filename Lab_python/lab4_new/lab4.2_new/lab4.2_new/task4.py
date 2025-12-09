import numpy as np
from scipy import integrate

print("Вычисление интегралов")
print("Определенные интегралы:")

def f1(x):
    return x**2 + 3*x - 2

result1 = integrate.quad(f1, 1, 4)[0]
print(f"1. интеграл(x² + 3x - 2) dx от 1 до 4 = {result1:.6f}")

def f2(x):
    return np.sin(x)

result2 = integrate.quad(f2, 0, np.pi)[0]
print(f"2. интеграл sin(x) dx от 0 до пи = {result2:.6f}")

print("Двочные интегралы:")

def f_double1(x, y):
    return x + y

result_d1 = integrate.dblquad(f_double1, 0, 2, lambda x: 1, lambda x: 3)[0]
print(f"1. двойнлй интеграл (x + y) dxdy, x принадлежит[0,2], y принадлежит [1,3] = {result_d1:.6f}")

def f_double2(x, y):
    return x**2 + y**2

result_d2 = integrate.dblquad(f_double2, 0, 1, lambda x: 0, lambda x: 1)[0]
print(f"2. двойной интеграл (x² + y²) dxdy, x принадлежит [0,1], y принадлежит [0,1] = {result_d2:.6f}")
