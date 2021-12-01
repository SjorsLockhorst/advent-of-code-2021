file = open("input.txt")  # read file
inputs = [int(line.strip()) for line in file]  # Parse strings to list of ints

rolling_sums = []

for idx, entry in enumerate(inputs):  # Loop over all inputs

    if idx + 3 <= len(inputs):  # Only create a new 'batch' if 3 more entries in inputs
        rolling_sums.append(entry)

    for i in range((idx - 2), idx):  # Loop over all indices 2 lower than current

        if i >= 0 and i < len(rolling_sums):  # Make sure in index is within range
            rolling_sums[i] += entry  # Add current entry to that sum

total = 0

for i in range(1, len(rolling_sums)):
    if rolling_sums[i] > rolling_sums[i - 1]:
        total += 1  # Add 1 to total when current sum is bigger than previous

print(total)  # Print answer!
