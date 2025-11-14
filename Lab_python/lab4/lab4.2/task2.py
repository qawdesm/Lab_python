import numpy as np

print("Введите данные:")

lengths_input = input("Длины участков (через пробел): ")
lengths = np.array(list(map(float, lengths_input.split())))

speeds_input = input("Скорости на участках (через пробел): ")
speeds = np.array(list(map(float, speeds_input.split())))

if len(lengths) != len(speeds):
    print("Ошибка: количество участков длин и скоростей не совпадает!")
    exit()

k = int(input("Номер участка въезда (k): "))
p = int(input("Номер участка выезда (p): "))

if k < 1 or p > len(lengths) or k > p:
    print("Ошибка: некорректные номера участков!")
    exit()

print(f"Анализ участков с {k} по {p}:")

start_index = k - 1
end_index = p - 1

selected_lengths = lengths[start_index:end_index + 1]
total_length = np.sum(selected_lengths)

selected_speeds = speeds[start_index:end_index + 1]
times = selected_lengths / selected_speeds
total_time = np.sum(times)

average_speed = total_length / total_time

print(f"Длина пути: {total_length:.2f} км")
print(f"Время в пути: {total_time:.2f} час") 
print(f"Средняя скорость: {average_speed:.2f} км/ч")

print(f"Детализация:")
print("Участок | Длина (км) | Скорость (км/ч) | Время (ч)")
for i in range(start_index, end_index + 1):
    time_segment = lengths[i] / speeds[i]
    print(f"{i+1:7}   {lengths[i]:10.1f}   {speeds[i]:14.1f}   {time_segment:8.3f}")
