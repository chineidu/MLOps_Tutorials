def is_prime(n: int) -> bool:
    """
    Checks if a given number is prime or not.

    Parameters
    ----------
    n : int
        The number to check.

    Returns
    -------
    bool
        True if the number is prime, False otherwise.
    """
    if n <= 1:
        return False
    
    limit = int(n**0.5) + 1
    print(f"Checking if {n} is prime up to {limit}")

    for i in range(2, limit):
        print(f"Checking divisibility by {i} for {n}")
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    print(is_prime(3))
