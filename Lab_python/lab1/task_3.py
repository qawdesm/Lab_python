password = input("Введите пароль:")
if len(password) < 16:
    print("Слишком короткий")
else:
    if password.isalpha():
        print("Пароль содержит только буквы!Ненадежный пароль!")
    elif password.isdigit():
        print("Пароль содержит только цифры!Ненадежный пароль!")
    else:
        print("Надежный пароль")