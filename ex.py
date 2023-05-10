from scipy.spatial import Voronoi, voronoi_plot_2d, distance
import matplotlib.pyplot as plt
import numpy as np
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
               (2, 0), (5, 0), (10, 0), (12, 0), (15, 0), (16, 0), (17, 0), (19, 0), (23, 0), (25, 0), (2, 25), (5, 25),
               (10, 25), (12, 25), (15, 25), (16, 25), (19, 25), (23, 25)]

base_stations = np.array([(7, 18), (19, 15), (8, 7), (18, 10)])

# x_edge, y_edge = zip(*edge_points)
fig, ax = plt.subplots()

# ax.scatter(x_edge, y_edge, color='g', s=16)

vor = Voronoi(base_stations, incremental=True)
voronoi_plot_2d(vor, ax=ax, show_vertices=False)

lines = [LineString([(0.0, 0.0), (0.0, 25.0)]), LineString([(0.0, 25.0), (25.0, 25.0)]),
         LineString([(25.0, 25.0), (25.0, 0.0)]), LineString([(25.0, 0.0), (0.0, 0.0)])]

for line in lines:
    ax.plot(line.xy[0], line.xy[1], '-r', label='Line')

intersection_points = {}

for ridge_vertices, ridge_points in zip(vor.ridge_vertices, vor.ridge_points):
    if -1 in ridge_vertices:
        v = ridge_vertices[0] if ridge_vertices[0] != -1 else ridge_vertices[1]
        x1, y1 = vor.vertices[v]
        x2, y2 = vor.points[ridge_points[0]]
        x3, y3 = vor.points[ridge_points[1]]
        slope1 = (y2 - y1) / (x2 - x1)
        slope2 = (y3 - y1) / (x3 - x1)
        cal_m = -(x3 - x2) / (y3 - y2)
        x_p = (x2 + (x3 - x2) / 2)
        if (x1 < x_p):
            x_p = x_p * 10
        else:
            x_p = -x_p * 10
        ray_start = Point(x1, y1)
        y_p = y1 + cal_m * (x_p - x1)
        ray_direction = Point(x_p, y_p)
        ray = LineString([ray_start, ray_direction])
        ax.plot(ray.xy[0], ray.xy[1], '-r', label='Ray')

        for line in lines:
            intersection = ray.intersection(line)
            if isinstance(intersection, Point):
                intersection_points[intersection] = ridge_points[0]

            # print(intersection)

print(intersection_points)



boundary_points = []
for point in intersection_points.keys():
    boundary_points_temp = []
    for ep in edge_points:
        if point.distance(Point(ep[0], ep[1])) < 3:
            boundary_points_temp.append(ep)
            boundary_points.append(ep)
            ax.scatter(ep[0], ep[1], color='black', s=10)
            ax.annotate("B", ep)
    boundary_points_temp = sorted(boundary_points_temp)

    print("boundary_points_temp", boundary_points_temp)

    x_axis_parallel_points = []
    y_axis_parallel_points = []

    for bpt in boundary_points_temp:
        if any(bpt[1] == p[1] for p in boundary_points_temp if p != bpt) and bpt not in y_axis_parallel_points:
            x_axis_parallel_points.append(bpt)
        if any(bpt[0] == p[0] for p in boundary_points_temp if p != bpt) and bpt not in x_axis_parallel_points:
            y_axis_parallel_points.append(bpt)

    print("x_axis_parallel_points", x_axis_parallel_points)
    print("y_axis_parallel_points", y_axis_parallel_points)

    if len(x_axis_parallel_points):
        base_station_distance = abs(boundary_points_temp[0][1] - base_stations[intersection_points[point]][1])
        distance_between = []
        distance_from_a = -abs(boundary_points_temp[0][0] - base_stations[intersection_points[point]][0])
        for i in range(1, len(boundary_points_temp)):
            distance_between.append(boundary_points_temp[i][0] - boundary_points_temp[i - 1][0])
        rounds, energy = heuristics(distance_between, base_station_distance, distance_from_a)
        print("rounds", rounds)
        for i, bpt in enumerate(boundary_points_temp):
            plt.annotate(str(rounds[i]), (bpt[0], bpt[1]), ha='center', textcoords="offset points", xytext=(6, 9),
                         fontsize=9)
        print("distance_between", distance_between)
        print("distance_from_a", distance_from_a)
        print("nearest distance", base_stations[intersection_points[point]])
        print()
    else:
        distance_between = []
        base_station_distance = abs(boundary_points_temp[0][0] - base_stations[intersection_points[point]][0])
        distance_from_a = -abs(boundary_points_temp[0][1] - base_stations[intersection_points[point]][1])
        for i in range(1, len(boundary_points_temp)):
            distance_between.append(boundary_points_temp[i][1] - boundary_points_temp[i - 1][1])
        rounds, energy = heuristics(distance_between, base_station_distance, distance_from_a)
        print("rounds", rounds)
        for i, bpt in enumerate(boundary_points_temp):
            plt.annotate(str(rounds[i]), (bpt[0], bpt[1]), ha='center', textcoords="offset points", xytext=(14, 2),
                         fontsize=9)
        print("distance_between", distance_between)
        print("distance_from_a", distance_from_a)
        print("nearest distance", base_stations[intersection_points[point]])
        print()


edge_points_ref = []
for ep in edge_points:
    if ep not in boundary_points:
        edge_points_ref.append(ep)

edge_points_map = {i: [] for i in range(len(base_stations))}

for point in edge_points_ref:
    distances = distance.cdist([point], base_stations)
    region_index = np.argmin(distances)
    edge_points_map[region_index].append(point)

colors = ['magenta', 'r', 'b', 'y']

for i, points in edge_points_map.items():
    x, y = zip(*points)
    ax.scatter(x, y, color=colors[i], s=17)

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

for key, points in x_axis_p_dict.items():
    distance_between = []
    base_station_distance = abs(points[0][1] - base_stations[key][1])
    distance_from_a = abs(points[0][0] - base_stations[key][0])
    for i in range(1, len(points)):
        distance_between.append(points[i][0] - points[i - 1][0])
    print(points)
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
    print(points)
    print(distance_between)
    print(base_station_distance)
    print(distance_from_a)
    rounds, energy = heuristics(distance_between, base_station_distance, distance_from_a)
    for i, point in enumerate(points):
        plt.annotate(str(rounds[i]), (point[0], point[1]), textcoords="offset points", xytext=(8, 6), ha='center',
                     fontsize=6)
    print(sum(rounds))
    print()

additional_base_points=[]
for point in intersection_points.keys():
    additional_base_points.append((point.x,point.y))

# print(additional_base_points);
# print(intersection_points)
# vor.add_points(additional_base_points)
# voronoi_plot_2d(vor, ax=ax,show_vertices=False)


ax.set_xlim(0 - 3, 25 + 3)
ax.set_ylim(0 - 3, 25 + 3)

plt.show()