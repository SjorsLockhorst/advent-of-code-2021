file = open("input.txt")

x = 0
y = 0

for line in file:
    split_line = line.strip().split(" ")
    direction = split_line[0]
    amount = int(split_line[1])
    if direction == "forward":
        x += amount
    elif direction == "down":
        y += amount
    elif direction == "up":
        y -= amount
    else:
        raise Exception("Unknown command")

print(x * y)
