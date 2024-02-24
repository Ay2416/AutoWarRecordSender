num = 2

for i in range(-1, 100):
    if i != 0:
        if num == 1:
            if i % 2 != 0:
                print(i)
        else:
            if i % 2 == 0:
                print(i)
    else:
        if num == 2:
                print(i)