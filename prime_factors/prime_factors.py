

def prime_factors(number):
    if not isinstance(number,int):
        raise ValueError('Input must be an integer')
    result = []
    for i in range(number + 1):
        while number % i == 0:
            result.append(i)
            number = number / i

    return result



