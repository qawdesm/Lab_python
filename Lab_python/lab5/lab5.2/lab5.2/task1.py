import pytest

def count_words(sentence):
    if not sentence or sentence.isspace():
        return 0
    words = sentence.split()
    return len(words)

def test_count_words_basic():
    assert count_words("Hello world") == 2
    assert count_words("This is a test") == 4

def test_count_words_empty():
    assert count_words("") == 0
    assert count_words("   ") == 0

def test_count_words_multiple_spaces():
    assert count_words("Hello    world") == 2
    assert count_words("  Start  middle  end  ") == 3

def test_count_words_single_word():
    assert count_words("Hello") == 1
    assert count_words("  Python  ") == 1

def test_count_words_with_punctuation():
    assert count_words("Hello, world!") == 2
    assert count_words("Test... sentence.") == 2

if __name__ == "__main__":
    pytest.main([__file__, "-v"])