import random
import time

import numpy as np
from matplotlib import pyplot as plt

from modeling2d.common import find_max_derivative

size = 5
repeat_count = 10000
probability_variants_count = 101
mid = int(size / 2)
prob_arr = np.linspace(0, 1, probability_variants_count)

start_Set = set()

start_Set.add((mid + 1, mid))
start_Set.add((mid - 1, mid))
start_Set.add((mid, mid + 1))
start_Set.add((mid, mid - 1))

clusterArr = []
timeArr = []
start = time.time()

for probability in prob_arr:
    sizeSumm = 0
    timeSumm = 0
    print(f"probability: \t{probability}, \ntime spent: \t{time.time() - start}\n")

    for i in range(repeat_count):
        stepStart = time.time()
        arr = np.zeros((size, size), float)
        arr[mid][mid] = 1
        mySet = start_Set

        while len(mySet) != 0:
            newSet = set()
            for each in mySet:
                if random.random() < probability:
                    arr[each[0]][each[1]] = 1
                    if each[0] != (size - 1) and arr[each[0] + 1][each[1]] == 0:
                        newSet.add((each[0] + 1, each[1]))
                    if each[0] != 0 and arr[each[0] - 1][each[1]] == 0:
                        newSet.add((each[0] - 1, each[1]))
                    if each[1] != (size - 1) and arr[each[0]][each[1] + 1] == 0:
                        newSet.add((each[0], each[1] + 1))
                    if each[1] != 0 and arr[each[0]][each[1] - 1] == 0:
                        newSet.add((each[0], each[1] - 1))
                else:
                    arr[each[0]][each[1]] = -1
            mySet = newSet
        uniq, counts = np.unique(arr, return_counts=True)
        uniq_dict = dict(zip(uniq, counts))
        sizeSumm += uniq_dict[1]
        stepEnd = time.time()
        timeSumm += stepEnd - stepStart

    timeArr.append(timeSumm / repeat_count)
    clusterArr.append(sizeSumm / repeat_count)

PATH_PATTERN = "/Users/me/PycharmProjects/percolation/modeling2d/corn/{}/size={}|repeat_count={}.txt"

with open(PATH_PATTERN.format("time", size, repeat_count), "w") as timeFile:
    timeFile.write(str(timeArr))

with open(PATH_PATTERN.format("graphic", size, repeat_count), "w") as graphicFile:
    graphicFile.write(str(clusterArr))

max_der = find_max_derivative(clusterArr, probability_variants_count)
print(f"max_der: {max_der}")
plt.axvline(x=max_der, color='r', linestyle='-')
plt.subplot(2, 1, 1)
plt.plot(prob_arr, clusterArr)
plt.subplot(2, 1, 2)
plt.plot(prob_arr, timeArr)

plt.show()