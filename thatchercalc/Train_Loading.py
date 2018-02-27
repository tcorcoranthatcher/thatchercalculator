import math
from operator import itemgetter


def train_loading(distance, load, tie_size, elevation):
    surcharge_list = [[0, elevation]]
    for i in range(1, 10001):
        surcharge_list.append([0, round(elevation-i*0.01, 2)])

    cutoff_depth = (distance+tie_size/2-7.75)/1.5

    for i in range(1, len(surcharge_list)):
        depth = round(elevation - surcharge_list[i][1], 2)
        beta = math.atan((distance+tie_size)/depth)-math.atan(distance/depth)
        alpha = math.atan(distance/depth) + beta/2
        surcharge = round((2*load/math.pi)*(beta-math.sin(beta)*math.cos(2*alpha)), 0)
        surcharge_list[i][0] = surcharge
        if depth < cutoff_depth:
            surcharge_list[i][0] = 0

    return surcharge_list


def combine_trains(trains):
    combined_dict = {}
    combined_list = []
    for i in range(len(trains[0])):
        combined_dict[trains[0][i][1]] = trains[0][i][0]
    for i in range(1, len(trains)):
        if trains[i]:
            for j in range(len(trains[i])):
                if trains[i][j][1] not in combined_dict.keys():
                    combined_dict[trains[i][j][1]] = trains[i][j][0]
                else:
                    load = combined_dict[trains[i][j][1]]
                    combined_dict[trains[i][j][1]] = load + trains[i][j][0]

    a = list(combined_dict.items())
    for i in a:
        combined_list.append([i[0], i[1]])
    b = sorted(a, key=itemgetter(0))
    combined_list = []
    for i in reversed(b):
        combined_list.append(i)

    return combined_list


# train_1 = train_loading(77.5, 642, 8.5, 38)
# train_2 = train_loading(87.5, 642, 8.5, 45)
# train_3 = train_loading(97.5, 700, 8.5, 47)
# train_4 = train_loading(107.5, 700, 8.5, 48)
#
# trains = [train_1, train_2, train_3, train_4]
# train_surcharge = combine_trains(trains)
