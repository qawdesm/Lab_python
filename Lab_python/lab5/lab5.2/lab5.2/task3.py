import pytest

def is_palindrome(word):
    cleaned_text = str(word).replace(" ", "").lower()
    return cleaned_text == cleaned_text[::-1]


def test_is_palindrome():
    assert is_palindrome("radar") == True
    assert is_palindrome("А роза упала на лапу Азора") == True
    assert is_palindrome("racecar") == True

    assert is_palindrome("hello") == False
    assert is_palindrome("python") == False

    assert is_palindrome(12321) == True
    assert is_palindrome(1221) == True

    assert is_palindrome(12345) == False

    assert is_palindrome("") == True
    assert is_palindrome("a") == True
    assert is_palindrome("   ") == True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])