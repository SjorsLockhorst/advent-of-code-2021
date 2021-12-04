f = open("input.txt")

inputs = [line.strip() for line in f]


half = len(inputs) / 2
bits = [0 for _ in range(len(inputs[0]))]

for entry in inputs:
    for i, bit in enumerate(entry):
        bits[i] += int(bit)

gamma_bits = [int(bit_count >= half) for bit_count in bits]
epsilon_bits = [1 - bit for bit in gamma_bits]

gamma_dec = int("".join([str(bit) for bit in gamma_bits]), 2)
epsilon_dec = int("".join([str(bit) for bit in epsilon_bits]), 2)

print(gamma_dec * epsilon_dec)
