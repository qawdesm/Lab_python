import datetime

def log_calls(filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            time = datetime.datetime.now().strftime("%H:%M:%S")
            args_str = str(args)[1:-1]
            log_line = f"{time} - {func.__name__}({args_str})\n"
            
            with open(filename, 'a') as f:
                f.write(log_line)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_calls("log.txt")
def calculate(a, b, op='+'):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    return a / b

calculate(10, 15, '+')