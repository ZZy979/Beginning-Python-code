def power(x, n):
    """Calculate x to the power of n (n >= 0)."""
    if n == 0:
        return 1
    else:
        return x * power(x, n - 1)
