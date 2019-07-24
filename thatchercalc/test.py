triangle_numbers = []
square_numbers = []
pentagonal_numbers = []
hexagonal_numbers = []
heptagonal_numbers = []
octagonal_numbers = []

for n in range(141):
    triangle = n*(n+1)/2
    if len(str(int(triangle))) == 4:
        triangle_numbers.append(str(int(triangle)))
    square = n**2
    if len(str(int(square))) == 4:
        square_numbers.append(str(int(square)))
    pentagonal = n*(3*n-1)/2
    if len(str(int(pentagonal))) == 4:
        pentagonal_numbers.append(str(int(pentagonal)))
    hexagonal = n*(2*n-1)
    if len(str(int(hexagonal))) == 4:
        hexagonal_numbers.append(str(int(hexagonal)))
    heptagonal = n*(5*n-3)/2
    if len(str(int(heptagonal))) == 4:
        heptagonal_numbers.append(str(int(heptagonal)))
    octagonal = n*(3*n-2)
    if len(str(int(octagonal))) == 4:
        octagonal_numbers.append(str(int(octagonal)))

iterations = []
for triangle in triangle_numbers:
    for square in square_numbers:
        for pentagonal in pentagonal_numbers:
            for hexagonal in hexagonal_numbers:
                for heptagonal in heptagonal_numbers:
                    for octagonal in octagonal_numbers:
                        iterations.append([triangle, square, pentagonal, hexagonal, heptagonal, octagonal])


print(iterations)

