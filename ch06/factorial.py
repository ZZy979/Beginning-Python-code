def factorial(n):
    """Compute the factorial of n (n >= 1)."""
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)
