import numpy as np
from scipy.optimize import linprog
import random

no_of_sensors = 5
no_of_configurations = no_of_sensors
maximum_capacity_of_sensors = 2000
distance_between = [5, 1, 4, 4]
prefix_distance = [0]
prefix_distance_squares = []
ratios = []
energy = []
rounds = []
max_distance = 5
base_station_distance = 10
rx = 2

for i in range(no_of_sensors - 1):
    prefix_distance.append(prefix_distance[-1] + distance_between[i])

for i in range(no_of_sensors):
    prefix_distance_squares.append(prefix_distance[i] ** 2 + base_station_distance ** 2);
    energy.append(maximum_capacity_of_sensors)
    rounds.append(0)

sumvalue = sum(prefix_distance_squares)

for i in range(no_of_sensors):
    ratios.append((1 - ((prefix_distance_squares[i]) / sumvalue))*0.6)

print(sumvalue)
print(distance_between)
print(prefix_distance)
print(prefix_distance_squares)
print(energy)
print(ratios)
print(rounds)


# for i in range(no_of_configurations):
#     for j in range(no_of_sensors):
#         val = 0
#         if i == j:
#             val = base_station_distance ** 2 + prefix_distance[j] ** 2 + 2 * rx
#         elif j < i:
#             val = distance_between[j] ** 2 + rx
#         else:
#             val = distance_between[j - 1] ** 2 + rx
#         if j != 0 and j != no_of_sensors - 1:
#             val += rx
#         print(val, end=" ")
#     print()

for l in range(4):
    for i in range(no_of_configurations):
        can_be = True
        upto = energy[i] * ratios[i]
        energyleft = energy[i] - upto
        # print(energyleft)
        energy[i] = upto

        while can_be:
            for j in range(no_of_sensors):
                val = 0
                if i == j:
                    val = base_station_distance ** 2 + prefix_distance[j] ** 2 + 2 * rx
                elif j < i:
                    val = distance_between[j] ** 2 + rx
                else:
                    val = distance_between[j - 1] ** 2 + rx
                if j != 0 and j != no_of_sensors - 1:
                    val += rx

                if energy[j] < val:
                    can_be = False
                    break
            # print(energy)

            if can_be:
                for j in range(no_of_sensors):
                    val = 0
                    if i == j:
                        val = base_station_distance ** 2 + prefix_distance[j] ** 2 + 2 * rx
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
        energy[i] = energy[i] + energyleft
    # print()
    # print()
    # print()

print(rounds)
print(sum(rounds))

