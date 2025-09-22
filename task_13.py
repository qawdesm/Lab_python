import random
print("Поиграем в игру.Я загадал число от 1 до 100. Попробуй угадать!")
secret_number = random.randint(1, 100)
while True:
    guess = int(input("Твоя догадка: "))
    if guess < secret_number:
        print("Больше!")
    elif guess > secret_number:
        print("Меньше!")
    else:
        print(f"Поздравляю! Ты угадал число")
        break