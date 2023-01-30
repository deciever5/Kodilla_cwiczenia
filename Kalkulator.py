def prime_factors(number):
    factors = []
    for i in range(2, number + 1):
        while number % i == 0:
            factors.append(i)
            number = number / i
    return factors

print(prime_factors(325))