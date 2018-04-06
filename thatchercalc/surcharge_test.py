import math
from fractions import Fraction


def isprime(n):
    '''check if integer n is a prime'''

    # make sure n is a positive integer
    n = abs(int(n))

    # 0 and 1 are not primes
    if n < 2:
        return False

    # 2 is the only even prime number
    if n == 2:
        return True

    # all other even numbers are not primes
    if not n & 1:
        return False

    # range starts with 3 and only needs to go up
    # the square root of n for all odd numbers
    for x in range(3, int(n**0.5) + 1, 2):
        if n % x == 0:
            return False

    return True


def prime_factors(number):
    work_number = number
    prime_factor_list = []
    i = 1
    while not isprime(work_number):
        if isprime(i):
            if work_number % i == 0:
                if i not in prime_factor_list:
                    prime_factor_list.append(i)
                work_number = work_number/i
                i = 1
        i += 1
    if int(work_number) not in prime_factor_list:
        prime_factor_list.append(int(work_number))

    return sorted(prime_factor_list)









