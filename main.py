import numpy as np
import math
from scipy.optimize import linprog

no_of_sensors = 5
no_of_configurations = no_of_sensors
maximum_capacity_of_sensors = 10000
distance_between = 5
base_station_distance = 10
rx = 2

inequalities_lhs = []
inequalities_rhs = []
bound_values = []

for i in range(1, no_of_sensors + 1):

    # calculating for each sensor in different configuration
    each_sensor_diff_config = []
    for j in range(1, no_of_sensors + 1):
        # looping on configurations
        if i == j:
            each_sensor_diff_config.append(base_station_distance ** 2 + ((j - 1) * 5) ** 2 + 2 * rx)
        else:
            each_sensor_diff_config.append(distance_between ** 2 + 2 * rx)
    inequalities_lhs.append(each_sensor_diff_config)

    # max battery for each sensor
    inequalities_rhs.append(maximum_capacity_of_sensors)

    # bounds for each sensor , should greater than or equal to zero
    bound_values.append((0, None))

print(inequalities_lhs)
print(inequalities_rhs)
print(bound_values)

coefficient_of_rounds = [-1] * no_of_configurations
print(coefficient_of_rounds)

res = linprog(coefficient_of_rounds, A_ub=inequalities_lhs, b_ub=inequalities_rhs, bounds=bound_values,
              integrality=np.ones_like(coefficient_of_rounds))
print(res.x)

print(int(sum(res.x)))
