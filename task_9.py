ip = input("Введите IP-адрес: ")
parts = ip.split('.')

if len(parts) != 4:
    print("Некорректный IP: должно быть 4 части")
else:
    if all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
        print(f"'{ip}' - корректный IP-адрес!")
    else:
        print(f"'{ip}' - некорректный IP-адрес")