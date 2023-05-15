import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from scipy.spatial import Voronoi, voronoi_plot_2d, distance
from shapely.geometry import LineString, Point

configs = {}


def run_for_config(dictionary_info):
    indval = dictionary_info[1]

    distance_between = configs[indval][1]
    no_of_sensors = len(distance_between) + 1
    # prefix_distance = [0]
    energy = configs[indval][4]
    rounds = configs[indval][5]
    distance_from_a = configs[indval][3]
    base_station_distance = configs[indval][2]
    points = configs[indval][0]
    prefix_distance = configs[indval][6]
    rx = 2
    i = points.index(dictionary_info[0])
    # print(configs[indval])
    # print(i)
    can_be = True
    for j in range(no_of_sensors):
        val = 0
        if i == j:
            val = 2*rx + dictionary_info[2]**2
            # val = base_station_distance ** 2 + abs(prefix_distance[j] - distance_from_a) ** 2 + 2 * rx
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
                val = 2 * rx + dictionary_info[2] ** 2
            elif j < i:
                val = distance_between[j] ** 2 + rx
            else:
                val = distance_between[j - 1] ** 2 + rx
            if j != 0 and j != no_of_sensors - 1:
                val += rx

            energy[j] = energy[j] - val
        rounds[i] = rounds[i] + 1

    configs[indval][4] = energy
    configs[indval][5] = rounds
    return can_be


def heuristics(indval, dictionary_info):
    distance_between = configs[indval][1]
    no_of_sensors = len(distance_between) + 1
    no_of_configurations = no_of_sensors
    # prefix_distance = [0]
    ratios = []
    energy = configs[indval][4]
    rounds = configs[indval][5]
    # maximum_capacity_of_sensors = 2000
    distance_from_point = []
    distance_from_a = configs[indval][3]
    base_station_distance = configs[indval][2]
    points = configs[indval][0]
    rx = 2
    prefix_distance = configs[indval][6]

    all_vals = []
    for i in range(no_of_configurations):
        vals = []
        for j in range(no_of_sensors):
            val = 0
            if i == j:
                val = base_station_distance ** 2 + abs(prefix_distance[i] - distance_from_a) ** 2 + 2 * rx
            elif i < j:
                val = distance_between[i] ** 2 + rx
            else:
                val = distance_between[i - 1] ** 2 + rx
            if i != 0 and i != no_of_sensors - 1:
                val += rx
            vals.append(val)
        all_vals.append(vals)
        ratios.append(max(vals) / sum(vals))
        # energy.append(maximum_capacity_of_sensors)
        distance_from_point.append(abs(prefix_distance[i] - distance_from_a))
        # rounds.append(0)

    dict = []
    for i in range(len(distance_from_point)):
        dict.append([distance_from_point[i], i])

    dict1 = sorted(dict)
    for l in range(8):
        for g in dict1:
            i = g[1]
            can_be = True
            upto = energy[i] / max(all_vals[i])
            can_be_rounds = upto * ratios[i]
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

                # if points[i] in dictionary_info:
                #     print(points[i])
                #     if can_be and energy[i]-dictionary_info[points[i]][2]**2-rx>0:
                #         if run_for_config(dictionary_info[points[i]]):
                #             energy[i] = energy[i] - dictionary_info[points[i]][2] ** 2 - rx


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


    configs[indval][4] = energy
    configs[indval][5] = rounds
    return rounds, energy


# edge_points = [(0, 2), (0, 5), (0, 10), (0, 12), (0, 15), (0, 16), (0, 19,), (0, 23), (0, 25), (25, 2), (25, 5),
#                (25, 7), (25, 10), (25, 12), (25, 15), (25, 16), (25, 19,), (25, 23), (25, 25),
#                (2, 0), (5, 0), (10, 0), (12, 0), (15, 0),(17, 0), (19, 0), (23, 0), (25, 0), (2, 25), (5, 25),
#                (10, 25), (12, 25), (15, 25), (16, 25), (19, 25), (23, 25)]
edge_points =[]
num_points = 20
ran = random.sample(range(0, 50), num_points)
for temp in ran:
    edge_points.append((temp, 0))
    edge_points.append((temp, 50))
    edge_points.append((0, temp))
    edge_points.append((50, temp))

# return points
base_stations = [(14, 35), (35, 32), (18, 17), (40, 20)]

intial_energy = 5000
edge_points_map = {i: [] for i in range(len(base_stations))}
point_info = {}
distances = distance.cdist(edge_points, base_stations)
for i, point in enumerate(edge_points):
    region_index = np.argmin(distances[i])
    point_info[point] = [distances[i][region_index], intial_energy]
    edge_points_map[region_index].append(point)

colors = ['magenta', 'g', 'b', 'y']

fig, ax = plt.subplots()
vor = Voronoi(base_stations, furthest_site=False)
voronoi_plot_2d(vor, ax=ax, show_vertices=False)
# plt.annotate(str(rounds[i]), (point[0], point[1]), ha='center', textcoords="offset points", xytext=(0, 6),
#                      fontsize=6)
# for point in edge_points:
#     ax.scatter(point[0],point[1],color='b',s=17)
#     plt.annotate("("+str(point[0])+","+str(point[1])+")", (point[0], point[1]), ha='center', textcoords="offset points", xytext=(10, 5),
#                  fontsize=6)
#
# for point in base_stations:
#     ax.scatter(point[0],point[1],color='b',s=17)
#     plt.annotate("("+str(point[0])+","+str(point[1])+")", (point[0], point[1]), ha='center', textcoords="offset points", xytext=(10, 5),
#                  fontsize=6)

for i, points in edge_points_map.items():
    x, y = zip(*points)
    ax.scatter(x, y, color=colors[i], s=17)

lines = [LineString([(0.0, 0.0), (0.0, 50.0)]), LineString([(0.0, 50.0), (50.0, 50.0)]),
         LineString([(50.0, 50.0), (50.0, 0.0)]), LineString([(50.0, 0.0), (0.0, 0.0)])]

line_axis = [1, 0, 1, 0]

for line in lines:
    ax.plot(line.xy[0], line.xy[1], '-r', label='Line')

# ax.set_xlim(0 - 3, 25 + 3)
# ax.set_ylim(0 - 3, 25 + 3)
#
# plt.show()


x_axis_p_dict = {}
y_axis_p_dict = {}

for key, points in edge_points_map.items():
    x_axis_parallel_points = []
    y_axis_parallel_points = []

    for point in points:
        if any(point[1] == p[1] for p in points if p != point) and point not in y_axis_parallel_points:
            x_axis_parallel_points.append(point)
        if any(point[0] == p[0] for p in points if p != point) and point not in x_axis_parallel_points:
            y_axis_parallel_points.append(point)

    x_axis_p_dict[key] = sorted(x_axis_parallel_points)
    y_axis_p_dict[key] = sorted(y_axis_parallel_points)

dictionary_info = {(15, 25): [(16, 25), 1, 1], (16, 25): [(15, 25), 0, 1],
                   (15, 0): [(17, 0), 2, 2], (17, 0): [(15, 0), 3, 2],
                   (0, 10): [(0, 12), 4, 2], (0, 12): [(0, 10), 7, 2],
                   (25,10): [(25,12), 5,2],(25,12): [(25,10),6,2]
                   }

print(x_axis_p_dict)
print(y_axis_p_dict)

config_val = 0

for key, points in x_axis_p_dict.items():
    info = []
    rounds = []
    distance_between = []
    base_station_distance = abs(points[0][1] - base_stations[key][1])
    distance_from_a = abs(points[0][0] - base_stations[key][0])
    energy = []
    prefix_distance =[0]
    for i in range(len(points)-1):
        distance_between.append(points[i+1][0] - points[i][0])
        prefix_distance.append(prefix_distance[-1] + distance_between[i])
    for i in range(len(points)):
        energy.append(intial_energy)
        rounds.append(0)
    info.append(points)
    info.append(distance_between)
    info.append(base_station_distance)
    info.append(distance_from_a)
    info.append(energy)
    info.append(rounds)
    info.append(prefix_distance)
    configs[config_val] = info
    config_val = config_val + 1

for key, points in y_axis_p_dict.items():
    info = []
    rounds = []
    distance_between = []
    prefix_distance = [0]
    base_station_distance = abs(points[0][0] - base_stations[key][0])
    distance_from_a = abs(points[0][1] - base_stations[key][1])
    energy = []
    for i in range(len(points)-1):
        distance_between.append(points[i+1][1] - points[i][1])
        prefix_distance.append(prefix_distance[-1] + distance_between[i])
    for i in range(len(points)):
        energy.append(intial_energy)
        rounds.append(0)
    info.append(points)
    info.append(distance_between)
    info.append(base_station_distance)
    info.append(distance_from_a)
    info.append(energy)
    info.append(rounds)
    info.append(prefix_distance)
    configs[config_val] = info
    config_val = config_val + 1

# print(configs)
# print(dictionary_info)

indval = 0

roun =[]
for key, points in x_axis_p_dict.items():
    rounds, energy = heuristics(indval, dictionary_info)
    print(rounds)
    print(sum(rounds))
    roun.append(sum(rounds))
    for i, point in enumerate(points):
        plt.annotate(str(rounds[i]), (point[0], point[1]), ha='center', textcoords="offset points", xytext=(0, 6),
                     fontsize=6)

    # print()
    indval += 1

for key, points in y_axis_p_dict.items():
    rounds, energy = heuristics(indval, dictionary_info)
    print(rounds)
    print(sum(rounds))
    roun.append(sum(rounds))
    for i, point in enumerate(points):
        plt.annotate(str(rounds[i]), (point[0], point[1]), ha='center', textcoords="offset points", xytext=(8, 6),
                     fontsize=6)
    # print(sum(rounds))
    # print()
    indval += 1
print(roun)
print(min(roun))
# print(configs)
ax.set_xlim(0 - 3, 50 + 3)
ax.set_ylim(0 - 3, 50 + 3)

plt.show()
