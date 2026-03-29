import pytest

def find_unique(elements):
    unique = []
    repeats = []

    for num in elements:
        if num not in unique:
            unique.append(num)

    for num in unique:
        if elements.count(num) > 1:
            repeats.append(num)

    result = []
    for num in unique:
        if num not in repeats:
            result.append(num)
    
    return result

def test_find_unique():
    assert find_unique([1, 2, 3, 2, 1]) == [3]
    assert find_unique(['a', 'b', 'a', 'c']) == ['b', 'c']
    assert find_unique([]) == []
    assert find_unique([1, 2, 3]) == [1, 2, 3]
    assert find_unique([1, 1, 1]) == []
    assert find_unique([5]) == [5]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])