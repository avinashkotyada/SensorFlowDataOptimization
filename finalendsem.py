import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from scipy.spatial import Voronoi, voronoi_plot_2d, distance
from shapely.geometry import LineString, Point


def heuristics(distance_between, base_station_distance, distance_from_a):
    no_of_sensors = len(distance_between) + 1
    no_of_configurations = no_of_sensors
    maximum_capacity_of_sensors = 2000
    prefix_distance = [0]
    ratios = []
    energy = []
    rounds = []
    distance_from_point = []
    rx = 2

    for i in range(no_of_sensors - 1):
        prefix_distance.append(prefix_distance[-1] + distance_between[i])

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
        energy.append(maximum_capacity_of_sensors)
        distance_from_point.append(abs(prefix_distance[i] - distance_from_a))
        rounds.append(0)

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
    return rounds, energy


edge_points = [(0, 2), (0, 5), (0, 10), (0, 12), (0, 15), (0, 16), (0, 19,), (0, 23), (0, 25), (25, 2), (25, 5),
               (25, 7), (25, 10), (25, 12), (25, 15), (25, 16), (25, 19,), (25, 23), (25, 25),
               (2, 0), (5, 0), (10, 0), (12, 0), (15, 0), (16, 0),(17,0), (19, 0), (23, 0), (25, 0), (2, 25), (5, 25),
               (10, 25), (12, 25), (15, 25), (16, 25), (19, 25), (23, 25)]
base_stations = [(7, 18), (19, 15), (8, 7), (18, 10)]


#
#
edge_points_map = {i: [] for i in range(len(base_stations))}

for point in edge_points:
    distances = distance.cdist([point], base_stations)
    region_index = np.argmin(distances)
    edge_points_map[region_index].append(point)

colors = ['magenta', 'g', 'b', 'y']

fig, ax = plt.subplots()
vor = Voronoi(base_stations, furthest_site=False)
voronoi_plot_2d(vor, ax=ax, show_vertices=False)
rect = Rectangle((0, 0), 25, 25, linewidth=2, edgecolor='r', facecolor='none')
plt.gca().add_patch(rect)

for i, points in edge_points_map.items():
    x, y = zip(*points)
    ax.scatter(x, y, color=colors[i], s=17)

# plt.xlabel('X')
# plt.ylabel('Y')
# plt.title('2D Points')

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

print(x_axis_p_dict)
print(y_axis_p_dict)




for key, points in x_axis_p_dict.items():
    distance_between = []
    base_station_distance = abs(points[0][1] - base_stations[key][1])
    distance_from_a = abs(points[0][0] - base_stations[key][0])
    for i in range(1, len(points)):
        distance_between.append(points[i][0] - points[i - 1][0])
    print(distance_between)
    print(base_station_distance)
    print(distance_from_a)
    rounds, energy = heuristics(distance_between, base_station_distance, distance_from_a)
    print(rounds)
    for i, point in enumerate(points):
        plt.annotate(str(rounds[i]), (point[0], point[1]), ha='center', textcoords="offset points", xytext=(0, 6),
                     fontsize=6)
    print(sum(rounds))
    print()

for key, points in y_axis_p_dict.items():
    distance_between = []
    base_station_distance = abs(points[0][0] - base_stations[key][0])
    distance_from_a = abs(points[0][1] - base_stations[key][1])
    for i in range(1, len(points)):
        distance_between.append(points[i][1] - points[i - 1][1])
    print(distance_between)
    print(base_station_distance)
    print(distance_from_a)
    rounds, energy = heuristics(distance_between, base_station_distance, distance_from_a)
    for i, point in enumerate(points):
        plt.annotate(str(rounds[i]), (point[0], point[1]), textcoords="offset points", xytext=(8, 6), ha='center',
                     fontsize=6)
    print(sum(rounds))
    print()




# print(vor.vertices)
# print(vor.points)
print(vor.ridge_vertices)


ax.set_xlim(0 - 3, 25 + 3)
ax.set_ylim(0 - 3, 25 + 3)

plt.show()
