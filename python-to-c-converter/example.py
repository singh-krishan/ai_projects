# Example Python code for translation testing

def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def main():
    print("Fibonacci sequence:")
    for i in range(10):
        result = fibonacci(i)
        print(f"F({i}) = {result}")

if __name__ == "__main__":
    main()