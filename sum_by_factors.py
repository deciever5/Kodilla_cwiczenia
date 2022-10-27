import math
import sys

def is_prime(n):
    if n <= 1:
        return False
    max_div = math.floor(math.sqrt(n))
    for i in range(2, 1 + max_div):
        if n % i == 0:
            return False
    return True

def sum_for_list(lst_to_check):
    primes_in_range, result, previous_prime = [], [], 0
    primes_in_range  = [num for num in range(2, max([abs(num) for num in lst_to_check]) + 1) if is_prime(num)]
    all_poss = [[prime, num] for prime in primes_in_range for num in lst_to_check if num % prime == 0]
    all_poss2 = enumerate(([prime, num] for prime in primes_in_range for num in lst_to_check if num % prime == 0))
    print(sys.getsizeof(all_poss), sys.getsizeof(all_poss2), type(all_poss), type(all_poss2))


    for i, j in all_poss2:
        if not result:
            result.append(j)
        elif previous_prime != j[0]:
            result.append(j)
        else:
            result[-1][1] += j[1]
        previous_prime = j[0]


    return result

def profiling(lst):
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        sum_for_list(lst)
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename="obliczenia.prof")

lst = [x for x in range(30000)]
profiling(lst)
