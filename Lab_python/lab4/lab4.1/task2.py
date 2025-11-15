import matplotlib.pyplot as plt
import math


x_values = []
for i in range(-1000, 1001):
    x = i * 0.01  
    if abs(x - 3) > 0.1 and abs(x + 3) > 0.1:  
        x_values.append(x)


def f(x):
    return 5 / (x**2 - 9)


y_values = [f(x) for x in x_values]


plt.figure(figsize=(10, 6))
plt.plot(x_values, y_values, 'b-', linewidth=2)
plt.title('График функции f(x) = 5 / (x² - 9)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True, alpha=0.3)
plt.axhline(y=0, color='k', linewidth=0.5)
plt.axvline(x=0, color='k', linewidth=0.5)
plt.xlim(-10, 10)
plt.ylim(-10, 10)  
plt.show()
