text = input("Введите строку: ")
cleaned_text = text.replace(" ", "").lower()
if cleaned_text == cleaned_text[::-1]:
    print(f" {text} - это палиндром!")
else:
    print(f" {text} - это не палиндром")