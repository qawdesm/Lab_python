import pytest

def are_anagrams(word1, word2):
    word1_clean = word1.strip().lower()
    word2_clean = word2.strip().lower()
    
    if not word1_clean or not word2_clean:
        return False
    
    return sorted(word1_clean) == sorted(word2_clean)

def test_are_anagrams():

    assert are_anagrams("listen", "silent") == True
    assert are_anagrams("triangle", "integral") == True
    assert are_anagrams("debit card", "bad credit") == True

    assert are_anagrams("hello", "world") == False
    assert are_anagrams("python", "java") == False
    assert are_anagrams("test", "tests") == False

    assert are_anagrams("State", "Taste") == True
    assert are_anagrams("School master", "The classroom") == True

    assert are_anagrams("", "test") == False
    assert are_anagrams("", "") == False
    assert are_anagrams("a", "a") == True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])