def sum_for_list(lst):
    primes_in_range = []
    for num in range(2, lst[-1]):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                primes_in_range.append(num)
    print(primes_in_range)

lst = [15, 21, 24, 30, 45]
sum_for_list(lst)