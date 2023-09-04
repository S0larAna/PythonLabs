list = [1, -2, 1, 1, 1, -10, 2, 2]
for i in range (0, len(list)-1):
    if (list[i]*list[i+1]>0):
        print(f'{list[i]} {list[i+1]}')
        break


