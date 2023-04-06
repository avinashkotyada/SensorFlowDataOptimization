
def heuristics(no_of_sensors,maximum_capacity_of_sensors,distance_between,base_station_distance,distance_from_a,rx):
    no_of_configurations = no_of_sensors
    prefix_distance = [0]
    ratios = []
    energy = []
    rounds = []
    distance_from_point=[]

    for i in range(no_of_sensors - 1):
        prefix_distance.append(prefix_distance[-1] + distance_between[i])

    allvals = []
    for i in range(no_of_configurations):
        vals = []
        print("sensor "+str(i+1)+": ",end=" ")
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

    print()
    print("distance between nodes : ",distance_between)
    print("prefix distances : ",prefix_distance)
    print("Intial Energy : ",energy)
    print("Ratios : ",ratios)
    print("Intial rounds: ",rounds)
    print("distance from point : ",distance_from_point)

    dict = {}

    for i in range(len(distance_from_point)):
        dict[distance_from_point[i]]=i

    dict1 = sorted(dict.items())
    print("sorting them " ,dict1)

    print()

    for l in range(6):
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
        print("After completing "+str(l+1)+" iterations")
        print()

    print(rounds)
    print(sum(rounds))
    return sum(rounds)


# example we are [5,1,4,4,3] two base stations one base at 9 and 14 diving at till index 2

distance_between = [5,1,4,4,3];
base_station_from_a1 = 3
base_station_from_a2 = 14


print("final from 1 ",heuristics(3,2000,[5, 1],10,3,2))
print()
print("final from 2 ",heuristics(3,2000,[4,3],10,0,2))
print()