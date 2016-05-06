import csv
import math as m


def distance(length, width):
    """
        функция считает расстояние(условное) до аптеки(по теореме пифагора)
    """
    return m.sqrt(length ** 2 + width ** 2)


def regrouping():
    """
        сортировка аптек методом пузырька(одна итерация)
    """
    global apt_1, apt_2, apt_3
    if apt_3[2] < apt_2[2]:
        var = apt_3
        apt_3 = apt_2
        apt_2 = var
    if apt_2[2] < apt_1[2]:
        var = apt_2
        apt_2 = apt_1
        apt_1 = var

    """
        идет построчное считывание файла, с нахождением у каждой аптеки растояния до нее(условного),
        отсортировка и запоминание трех аптек с наименьшим из них расстоянием
    """

data = input("write to a file path, longitude and latitude separated by a space")
file = data[:data.find(' ')]
longitude = float(data[data.find(' '):data.rfind(' ')])
latitude = float(data[data.rfind(' '):])
reader = csv.reader(open(file), delimiter='|')

apt_1 = ['', '', 0]
apt_2 = ['', '', 0]
apt_3 = ['', '', 0]
i = 0
for row in reader:
    if i > 3:
        leng = longitude - float(row[2])
        wid = latitude - float(row[3])
        dis = distance(leng, wid)
        if dis < apt_3[2]:
            apt_3 = [row[0], row[1], dis]
            regrouping()
        continue
    if 0 < i < 4:
        leng = longitude - float(row[2])
        wid = latitude - float(row[3])
        dis = distance(leng, wid)
        apt_1 = [row[0], row[1], dis]
        regrouping()
        if i == 3:
            regrouping()
        i += 1
        continue
    if i == 0:
        i += 1

print(apt_1[0] + ', ' + apt_1[1])
print(apt_2[0] + ', ' + apt_2[1])
print(apt_3[0] + ', ' + apt_3[1])
