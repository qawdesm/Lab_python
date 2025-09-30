word1 = input("Введите первое слово: ").strip().lower()
word2 = input("Введите второе слово: ").strip().lower()

if word1 and word2:
    if sorted(word1) == sorted(word2):
        print("True")
        print(f"Слова '{word1}' и '{word2}' являются анаграммами!")
    else:
        print("False")
        print(f"Слова '{word1}' и '{word2}' НЕ являются анаграммами")
else:
    print("Нужно ввести оба слова!")