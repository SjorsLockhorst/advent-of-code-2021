file = open("input.txt")  # Load inputs from file
inputs = [int(line.strip()) for line in file]  # Read lines and parse to int

total = 0

for i in range(1, len(inputs)):
    if inputs[i - 1] < inputs[i]:
        total += 1  # Add 1 to total if current input is bigger than previous

print(total)  # Print out the answer
