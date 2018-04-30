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

# def prime_factorization(number):
#     factors = []
#     i = 2
#     while i * i <= number:
#         while number % i == 0:
#             factors.append(i)
#             number = number / i
#         i += 1
#     if number != 1:
#         factors.append(int(number))
#     return factors
#
#
# print(prime_factorization(600851475143)[-1])
#
# def euler4():
#     solutions = []
#     for first in range(100, 1000):
#         for second in range(100, 1000):
#             number = first*second
#             number_string = str(number)
#             reverse_string = number_string[::-1]
#             if number_string == reverse_string:
#                 solutions.append(number)
#     return max(solutions)
#
# print(euler4())


# def euler6():
#     squares = 0
#     sum = 0
#     for number in range(1,101):
#         squares += number**2
#         sum += number
#     sum = sum**2
#
#     return sum - squares
#
# def euler7():
#     prime_count = 0
#     i = 0
#     while prime_count <= 10000:
#         i+=1
#         if isprime(i):
#             prime_count+=1
#     return i

# def euler8():
#     number = 7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450
#     products = []
#     number_string = str(number)
#     for i in range(len(number_string)-13):
#         product = int(number_string[i])
#         for j in range(1, 13):
#             product *= int(number_string[i+j])
#         products.append(product)
#
#     return max(products)
#
# print(euler8())

# def euler9():
#     for c in range(1, 1000):
#         for b in range(1, c):
#             for a in range(c-b, b):
#                 if a + b + c == 1000 and a**2 + b**2 == c**2:
#                     print(a*b*c)
#
# def euler10():
#     count = 0
#     for number in range(2, 2000000):
#         if isprime(number):
#             count += number
#     print(count)

def euler11():
    triangle_numbers = []
    for number in range(1,1000):
        triangle_number = 0
        for sub_number in range(1, number):
            triangle_number += sub_number
        triangle_numbers.append(triangle_number)

euler11()


