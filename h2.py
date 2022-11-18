import numpy as np
from scipy.optimize import linprog
import random

no_of_sensors = 100
no_of_configurations = no_of_sensors
maximum_capacity_of_sensors = 2000
distance_between = [5, 1, 4, 4]
prefix_distance = [0]
ratios = []
energy = []
rounds = []
max_distance = 5
base_station_distance = 10
rx = 2

for i in range(no_of_sensors - 1):
    prefix_distance.append(prefix_distance[-1] + distance_between[i])

allvals=[]
for i in range(no_of_configurations):
    vals=[]
    for j in range(no_of_sensors):
        val = 0
        if i == j:
            val = base_station_distance ** 2 + prefix_distance[i] ** 2 + 2 * rx
        elif i < j:
            val = distance_between[i] ** 2 + rx
        else:
            val = distance_between[i - 1] ** 2 + rx
        if i != 0 and i != no_of_sensors - 1:
            val += rx
        vals.append(val)
        print(val, end=" ")
    allvals.append(vals)
    ratios.append(max(vals)/sum(vals))
    energy.append(maximum_capacity_of_sensors)
    rounds.append(0)
    print()

# print(ratios)

# sumvalue = sum(ratios)
# for i in range(no_of_sensors):
#     ratios[i] = ratios[i]/sumvalue

print(distance_between)
print(prefix_distance)
print(energy)
print(ratios)
print(rounds)

print()
for l in range(2):
    for i in range(no_of_configurations):
        can_be = True
        upto = energy[i]/max(allvals[i])
        can_be_rounds = upto*ratios[i]
        print(can_be_rounds)
        k=0
        while(k<can_be_rounds and can_be):
            k=k+1
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
        print(rounds)
        print(energy)
        print()

    print()
    print()
    print()

print(rounds)
print(sum(rounds))

