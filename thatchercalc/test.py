text_file = open("p059_cipher.txt", "r")
lines = text_file.read().split(',')
conversions = []
for line in lines:
    conversions.append(int(line))
keys = []
for i in range(97, 123):
    for j in range(97, 123):
        for k in range(97, 123):
            number_string = int(str(i) + str(j) + str(k))
            keys.append(number_string)

iteration = []
conversions
