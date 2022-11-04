import math
import numpy as np

x = np.array([[1, 2, 3], [4, 5, 6]], np.int32)


def is_prime(n):
    if n <= 1:
        return False
    max_div = math.floor(math.sqrt(n))
    for i in range(2, 1 + max_div):
        if n % i == 0:
            return False
    return True


def my_generator(lst_to_check):
    primes_in_range = [num for num in range(2, max([abs(num) for num in lst_to_check]) + 1) if is_prime(num)]
    all_possibilities = np.array([prime, num] for prime in primes_in_range for num in lst_to_check if num % prime == 0)
    all_possibilities2 = map(lambda x: [x[0], x[1]] if x[1] % x[0] == 0 and x[1] != 0 else None,
                             ([prime, num] for prime in primes_in_range for num in lst_to_check if num % prime == 0))
    for j in all_possibilities:
        if j is not None:
            yield j


def sum_for_list(lst_to_check):
    result, previous_prime = [], 0
    all_results = my_generator(lst_to_check)

    for j in all_results:
        if not result:
            result.append(j)
        elif previous_prime != j[0]:
            result.append(j)
        else:
            result[-1][1] += j[1]
        previous_prime = j[0]
    return result


def profiling(lst_to_time):
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        sum_for_list(lst_to_time)
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename="obliczenia.prof")


lst = [x for x in range(30000)]
profiling(lst)
# sum_for_list(lst)
