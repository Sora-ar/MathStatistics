import numpy as np

Sympthoms = np.zeros((7, 5))

# Open the file with read only permit
text_file = open("Example.csv", "r")
lin = text_file.readlines()
text_file.close()

D1Size = len(lin)
Diagnose = D1Size - 1
print(Diagnose)

for i in range(1, D1Size):
    print(lin[i])
    data = lin[i].split(';')

    Age = int(data[0])
    if Age < 20:
        Sympthoms[1, 1] += 1
    elif (Age >= 20) and (Age < 40):
        Sympthoms[1, 2] += 1
    elif (Age >= 40) and (Age < 60):
        Sympthoms[1, 3] += 1
    else:
        Sympthoms[1, 4] += 1

    if data[2] == 'eye':
        Sympthoms[3, 1] += 1
    elif data[2] == 'skin':
        Sympthoms[3, 2] += 1
    else:
        Sympthoms[3, 3] += 1

PrKD = Sympthoms / Diagnose
print(PrKD)
