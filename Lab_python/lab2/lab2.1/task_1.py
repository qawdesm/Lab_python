text = input("Введите текст: ").strip()

if not text:
    print("Текст не введен!")
else:
   
    words = text.split()
    word_count = {}
    
    for word in words:
        word_lower = word.lower()
        if word_lower in word_count:
            word_count[word_lower] += 1
        else:
            word_count[word_lower] = 1
    
    unique_words_count = len(word_count)
    
    print("Словарь {слово: количество}:")
    for word, count in word_count.items():
        print(f"   '{word}': {count}")
    
    print(f"Количество уникальных слов: {unique_words_count}")