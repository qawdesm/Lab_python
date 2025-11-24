import pytest

def combine_dicts(dict_a, dict_b):
    result = dict_a.copy()
    
    for key, value in dict_b.items():
        if key in result:
            if isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = combine_dicts(result[key], value)
            else:
                result[key] = value
        else:
            result[key] = value
    
    return result

def test_combine_dicts():
    dict1 = {"a": 1, "b": 2}
    dict2 = {"c": 3, "d": 4}
    expected = {"a": 1, "b": 2, "c": 3, "d": 4}
    assert combine_dicts(dict1, dict2) == expected

    dict1 = {"a": 1, "b": 2}
    dict2 = {"b": 3, "c": 4}
    expected = {"a": 1, "b": 3, "c": 4}
    assert combine_dicts(dict1, dict2) == expected

    dict1 = {"a": 1, "b": {"c": 1, "f": 4}}
    dict2 = {"d": 1, "b": {"c": 2, "e": 3}}
    expected = {"a": 1, "b": {"c": 2, "f": 4, "e": 3}, "d": 1}
    assert combine_dicts(dict1, dict2) == expected

    assert combine_dicts({}, {"a": 1}) == {"a": 1}
    assert combine_dicts({"a": 1}, {}) == {"a": 1}
    assert combine_dicts({}, {}) == {}

if __name__ == "__main__":
    pytest.main([__file__, "-v"])