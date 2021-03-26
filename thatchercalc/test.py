import math

N = int(math.sqrt(10**12))
square_numbers = []
for i in range(N):
    square_numbers.append(i**2)

print(len(square_numbers))
for square in square_numbers:
    square_text = str(square)