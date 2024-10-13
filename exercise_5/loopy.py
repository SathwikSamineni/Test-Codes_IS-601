# case 1
i = 0
while i<=10:
    i += 1
    if i == 5:
        continue
    print(f"i = {i}")

# case 2
i = 0
x = 0
while i < 10:
    i += 1
    x += 1
    if x % 2 == 0:
        x -= 1

print(f"x = {x}")

# case 3
i = 0
x = 0
while i < 10:
    i += 1
    x += 1
    if i % 2 == 0:
        x -= 1
    if x % 2 == 0:
        x -= 1

print(f"x = {x}")

# case 4
i = 0
x = 0
while i < 10:
    i += 1
    x += 1
    print(f"iteration = {i}")
    print(f"increment = {x}")
    if i % 2 == 0:
        x -= 1
    if x % 2 == 0:
        x -= 1

print(f"x = {x}")