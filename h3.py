from time import time

import numpy as np
from scipy.optimize import linprog
import random

no_of_sensors = 6
no_of_configurations = no_of_sensors
maximum_capacity_of_sensors = 2000
distance_between = [5, 1, 4, 4, 3]
prefix_distance = [0]
ratios = []
energy = []
rounds = []
distance_from_point=[]
# max_distance = 5
base_station_distance = 10
distance_from_a = 3
rx = 2

for i in range(no_of_sensors - 1):
    prefix_distance.append(prefix_distance[-1] + distance_between[i])

allvals = []
for i in range(no_of_configurations):
    vals = []
    for j in range(no_of_sensors):
        val = 0
        if i == j:
            val = base_station_distance ** 2 + abs(prefix_distance[i]-distance_from_a)** 2 + 2 * rx
        elif i < j:
            val = distance_between[i] ** 2 + rx
        else:
            val = distance_between[i - 1] ** 2 + rx
        if i != 0 and i != no_of_sensors - 1:
            val += rx
        vals.append(val)
        print(val, end=" ")
    allvals.append(vals)
    ratios.append(max(vals) / sum(vals))
    energy.append(maximum_capacity_of_sensors)
    distance_from_point.append(abs(prefix_distance[i]-distance_from_a))
    rounds.append(0)
    print()

# print(ratios)
# print(allvals)
# sumvalue = sum(ratios)
# for i in range(no_of_sensors):
#     ratios[i] = ratios[i]/sumvalue

print(distance_between)
print(prefix_distance)
print(energy)
print(ratios)
print(rounds)
print(distance_from_point)

from collections import OrderedDict

dict = {}
dict1 = OrderedDict(sorted(dict.items()))

for i in range(len(distance_from_point)):
    dict[distance_from_point[i]]=i

dict1 = sorted(dict.items())
print(dict1)

print()

for l in range(3):
    for g in dict1:
        i = g[1]
        can_be = True
        upto = energy[i] / max(allvals[i])
        can_be_rounds = upto * ratios[i]
        print(can_be_rounds)
        k = 0
        while (k < can_be_rounds and can_be):
            k = k + 1
            for j in range(no_of_sensors):
                val = 0
                if i == j:
                    val = base_station_distance ** 2 + abs(prefix_distance[j] - distance_from_a) ** 2 + 2 * rx
                elif j < i:
                    val = distance_between[j] ** 2 + rx
                else:
                    val = distance_between[j - 1] ** 2 + rx
                if j != 0 and j != no_of_sensors - 1:
                    val += rx

                if energy[j] < val:
                    can_be = False
                    break

            if can_be:
                for j in range(no_of_sensors):
                    val = 0
                    if i == j:
                        val = base_station_distance ** 2 + abs(prefix_distance[j] - distance_from_a) ** 2 + 2 * rx
                    elif j < i:
                        val = distance_between[j] ** 2 + rx
                    else:
                        val = distance_between[j - 1] ** 2 + rx
                    if j != 0 and j != no_of_sensors - 1:
                        val += rx

                    energy[j] = energy[j] - val

                rounds[i] = rounds[i] + 1
            else:
                break
        print(rounds)
        print(energy)
        print()
    print(sum(rounds))
    print()
    print()
    print()

print(rounds)
print(sum(rounds))
