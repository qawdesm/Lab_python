import matplotlib.pyplot as plt
import math

x_degrees = range(-360, 361)

def to_radians(degrees):
    return degrees * math.pi / 180


def f(x_deg):
    x_rad = to_radians(x_deg)
    part1 = math.exp(math.cos(x_rad))
    part2 = math.log(math.cos(0.6 * x_rad)**2 + 1) * math.sin(x_rad)
    return part1 + part2


def h(x_deg):
    x_rad = to_radians(x_deg)
    cos_val = math.cos(x_rad)
    sin_val = math.sin(x_rad)
    inner = (cos_val + sin_val)**2 + 2.5
    return -math.log(inner) + 10


f_values = [f(x) for x in x_degrees]
h_values = [h(x) for x in x_degrees]


plt.figure(figsize=(12, 6))


plt.subplot(1, 2, 1)
plt.plot(x_degrees, f_values, 'b-', linewidth=2)
plt.title('Функция f(x)')
plt.xlabel('Градусы')
plt.ylabel('f(x)')
plt.grid(True)


plt.subplot(1, 2, 2)
plt.plot(x_degrees, h_values, 'r-', linewidth=2)
plt.title('Функция h(x)')
plt.xlabel('Градусы')
plt.ylabel('h(x)')
plt.grid(True)

plt.tight_layout()
plt.show()
