def sum_for_list(lst):
    primes_in_range, result, previous_prime = [], [], 0
    for num in range(2, lst[-1]):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                primes_in_range.append(num)

    all_poss = ([[prime, num] for prime in primes_in_range for num in lst if num % prime == 0])
    for i, j in enumerate(all_poss):
        if not result:
            result.append(j)
        elif previous_prime != j[0]:
            result.append(j)
        else:
            result[-1][1] += j[1]
        previous_prime = j[0]

    return result
