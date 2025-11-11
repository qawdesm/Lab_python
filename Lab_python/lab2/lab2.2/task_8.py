import time

def timing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        time_ms = (end - start) * 1000
        print(f"Время выполнения '{func.__name__}': {time_ms:.2f} мс")
        return result
    return wrapper

@timing
def test_slow():
    time.sleep(0.3)
    return

@timing
def test_fast():
    total = 0
    for i in range(100000):
        total += i
    return total

print("Тест замера времени")
test_slow()
test_fast()