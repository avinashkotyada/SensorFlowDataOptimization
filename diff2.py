import numpy as np
from scipy.optimize import linprog
import random

no_of_sensors = 6
no_of_configurations = no_of_sensors
maximum_capacity_of_sensors = 2000
distance_between = [2, 3, 5, 2, 3]
prefix_distance = [0]
# max_distance = 5
base_station_distance = 7
distance_from_a = 7
rx = 2

for i in range(no_of_sensors - 1):
    prefix_distance.append(prefix_distance[-1] + distance_between[i])
#
# [2, 3, 5, 2, 3]
# 7
# 7
# [13, 15, 12, 10, 14, 8]
# random.seed(10)
# for i in range(no_of_sensors - 1):
#     ran = random.randint(1, max_distance)
#     distance_between.append(ran)
#     prefix_distance.append(ran)
#
# for i in range(1, no_of_sensors - 1):
#     prefix_distance[i] += prefix_distance[i - 1]

# prefix_distance.insert(0, 0)

print(distance_between)
print(prefix_distance)

inequalities_lhs = []
inequalities_rhs = []
bound_values = []

for i in range(no_of_sensors):
    each_sensor_diff_config = []
    for j in range(no_of_configurations):
        val = 0
        if i == j:
            val = base_station_distance ** 2 + abs(prefix_distance[i]-distance_from_a)** 2 + 2 * rx
        elif i < j:
            val = distance_between[i] ** 2 + rx
        else:
            val = distance_between[i - 1] ** 2 + rx
        if i != 0 and i != no_of_sensors - 1:
            val += rx
        each_sensor_diff_config.append(val)

    inequalities_lhs.append(each_sensor_diff_config)

    inequalities_rhs.append(maximum_capacity_of_sensors)

    # bounds for each sensor , should greater than or equal to zero
    bound_values.append((0, None))

print(inequalities_lhs)
print(inequalities_rhs)
print(bound_values)

coefficient_of_rounds = [-1] * no_of_configurations
print(coefficient_of_rounds)

res = linprog(coefficient_of_rounds, A_ub=inequalities_lhs, b_ub=inequalities_rhs, bounds=bound_values, method='highs',
              integrality=np.ones_like(coefficient_of_rounds))
# print(res)
print(res.x)
print(int(sum(res.x)))