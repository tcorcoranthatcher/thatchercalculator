from .Lateral_Pressures import Layer
from operator import itemgetter
import math

# INPUTS (Define soil layers)
# Input by user in some way (HTML?)
# Must be ordered from top to bottom elevation wise
#
# layer_1 = Layer("Clay", 1, 130, 2.0, 1, 1)
# layer_2 = Layer("Sand 30", 0, 120, 0, 0.33, 4.45)
# layer_3 = Layer("Sand 33", 0, 125, 0, 0.29, 5.092)
#
# # Section elevation parameters
# surface_elev = 670  # Used for computing backside passive pressures
# cut_elev = 658  # Elevation at bottom of excavation
# water_elev = 666  # Elevation of water
# brace_elev = 666  # Elevation of single level brace
# total_weights = 200  # INDEX in the layers list below in which total weight analysis is switched to if necessary

# layers = [[670, layer_1, 0, 0, 0],
#           [668, layer_1, 0, 0, 0],
#           [668, layer_2, 0, 0, 0],
#           [666, layer_2, 0, 0, 0],
#           [661, layer_2, 0, 0, 0],
#           [661, layer_3, 0, 0, 0],
#           [658, layer_3, 0, 0, 0],
#           [647, layer_3, 0, 0, 0]]
#
# work_points = [[0, 670],
#                [0, 668],
#                [0, 668],
#                [0, 666],
#                [0, 661],
#                [0, 661],
#                [0, 658],
#                [0, 647]]


def footing_surcharge(type, width, distance, elevation, load, spacing_1, spacing_2):

    #  Declaration of variables
    a = distance-width/2
    b_1 = a/1.5
    b_2 = a
    b_3 = 2*a
    elev_1 = round(elevation - b_1, 2)
    elev_2 = round(elevation - b_2, 2)
    elev_3 = round(elevation - b_3, 2)

    #  Data manipulation
    calc_elev_list = []
    for i in range(10001):
        calc_elev = elevation - i*0.01
        calc_elev_list.append(round(calc_elev, 2))

    if type == 0:
        qeq_max = math.ceil(load / (2 * distance))
        case = 1
    elif type == 1 and distance <= spacing_1/2:
        qeq_max = math.ceil(load/((2*distance)*(2*distance)))
        case = 2
    elif type == 1 and spacing_1/2 < distance <= spacing_2/2:
        qeq_max = math.ceil(load/((2*distance)*(distance+spacing_1/2)))
        case = 3
    else:
        qeq_max = math.ceil(load/((2*distance)*(spacing_1/2+spacing_2/2)))
        case = 4

    footing_surcharges = []
    for elev in calc_elev_list:
        if elev > elev_1:
            footing_surcharges.append([elev, 0])
        elif elev_1 >= elev > elev_2:
            footing_surcharges.append([elev, math.ceil(qeq_max*((elev_1 - elev)/(elev_1-elev_2)))])
        elif elev_2 >= elev >= elev_3:
            footing_surcharges.append([elev, math.ceil(qeq_max)])
        else:
            delta = elev_3 - elev
            if type == 0:
                footing_surcharges.append([elev, math.ceil(load/(2*distance+delta/2))])
            else:
                if distance+delta/2 <= spacing_1/2:
                    footing_surcharges.append([elev, math.ceil(load/((2*distance+delta/2)*(2*distance+delta)))])
                if spacing_1/2 <= distance+delta/2 <= spacing_2/2:
                    footing_surcharges.append([elev, math.ceil(load/((2*distance+delta/2)*(distance+delta/2+spacing_1/2)))])
                if spacing_1/2 <= spacing_2/2 <= distance+delta/2:
                    footing_surcharges.append([elev, math.ceil(load/((2*distance+delta/2)*(spacing_1/2+spacing_2/2)))])

    return elev_1, elev_2, elev_3, footing_surcharges, load, distance, type, qeq_max, elevation, spacing_1, spacing_2, \
           case


def combine_footings(footings):
    combined_footing_dict = {}
    combined_footing_list = []
    for i in range(len(footings[0][3])):
        combined_footing_dict[footings[0][3][i][0]] = footings[0][3][i][1]
    for i in range(1, len(footings)):
        if footings[i]:
            for j in range(len(footings[i][3])):
                if footings[i][3][j][0] not in combined_footing_dict.keys():
                    combined_footing_dict[footings[i][3][j][0]] = (footings[i][3][j][1])
                else:
                    load = combined_footing_dict[footings[i][3][j][0]]
                    combined_footing_dict[footings[i][3][j][0]] = load + footings[i][3][j][1]
    a = list(combined_footing_dict.items())
    for i in a:
        combined_footing_list.append([i[0], i[1]])
    b = sorted(a, key=itemgetter(0))
    combined_footing_list = []
    for i in reversed(b):
        combined_footing_list.append(i)

    return combined_footing_list


def incorporate_footings(footings, combined_footing_load, layers, work_points, supplied_elev):
    footing_work_points = []
    for footing in footings:
        if footing[0] > supplied_elev - 10:
            footing_work_points.append(footing[0])
        if footing[1] > supplied_elev - 10:
            footing_work_points.append(footing[1])
        if footing[2] > supplied_elev - 10:
            footing_work_points.append(footing[2])
    footing_work_points = list(set(footing_work_points))
    footing_work_points = sorted(footing_work_points, reverse=True)
    for footing_work_point in footing_work_points:
        for j in range(len(work_points)-1):
            if [0, footing_work_point] not in work_points:
                work_points.append([0, footing_work_point])
    b = sorted(work_points, key=itemgetter(1))
    work_points = []
    for i in reversed(b):
        work_points.append(i)

    layer_elevations = []
    for i in range(len(layers)):
        layer_elevations.append(layers[i][0])
    for i in range(len(footing_work_points)):
        if footing_work_points[i] not in layer_elevations:
            if footing_work_points[i] > layer_elevations[0]:
                layers.insert(i, [footing_work_points[i], layers[0][1], 0, 0, 0, 10000, layers[0][6]])
                break
            elif layers[0][0] > footing_work_points[i] > layers[-1][0]:
                for j in range(len(layers)-1):
                    if layers[j][0] > footing_work_points[i] > layers[j+1][0]:
                        layers.insert(j+1, [footing_work_points[i], layers[j][1], 0, 0, 0, 10000, layers[j][6]])
            else:
                layers.append([footing_work_points[i], layers[-1][1], 0, 0, 0, 10000, layers[-1][6]])

    for i in range(len(layers)):
        for j in range(len(combined_footing_load)):
            if layers[i][0] == combined_footing_load[j][0]:
                layers[i][3] = round(combined_footing_load[j][1], 2)
                break

    return layers, work_points


def text_output(footing, footing_number):
    elev_1 = footing[0]
    elev_2 = footing[1]
    elev_3 = footing[2]
    load = footing[4]
    distance = footing[5]
    type = footing[6]
    qeq_max = footing[7]
    elevation = footing[8]
    spacing_1 = footing[9]
    spacing_2 = footing[10]
    case = footing[11]

    output = []
    output.append('At Footing ' + str(footing_number) + ":")
    output.append('Elevation of bottom of footing = ' + str(elevation) + "'")
    output.append('Distance from center line of footing to wall = ' + str(distance) + "'")
    if type == 0:
        output.append('Type = Continuous footing')
        output.append('Load = ' + str(load) + " plf")
    if type == 1:
        output.append('Type = Spread footing')
        output.append('Load = ' + str(load) + " pounds")
        output.append('Spacing to closest footings in plane = ' + str(spacing_1) + "', " + str(spacing_2) + "'")
    if case == 1:
        output.append("Max Footing Load = " + str(load) + " plf/(2*" + str(distance)+"') = " + str(qeq_max) + " psf")
        # qeq_max = math.ceil(load / (2 * distance))
    elif case == 2:
        output.append("Max Footing Load = " + str(load) + "#/(2*" + str(distance) + "')^2 = " + str(qeq_max) + " psf")
        # qeq_max = math.ceil(load/((2*distance)*(2*distance)))
    elif case == 3:
        output.append("Max Footing Load = " + str(load) + "#/((2*" + str(distance) + "')*(" + str(distance) + "' + " +
                      str(spacing_1) + "'/2)) = " + str(qeq_max) + " psf")
        # qeq_max = math.ceil(load/((2*distance)*(distance+spacing_1/2)))
    elif case == 4:
        output.append("Max Footing Load = " + str(load) + "#/((2*" + str(distance) + "')*(" + str(spacing_1) + "'/2 + " +
                      str(spacing_2) + "'/2)) = " + str(qeq_max) + " psf")
        # qeq_max = math.ceil(load/((2*distance)*(spacing_1/2+spacing_2/2)))

    output.append('At elevation ' + str(elev_1) + "' (above 1.5:1 slope), footing surcharge = 0 psf.")
    output.append('At elevation ' + str(elev_2) + "' (below 1:1 slope), footing surcharge = " + str(qeq_max) + " psf.")
    output.append('At elevation ' + str(elev_3) + "' (below 1:2 slope), footing surcharge = " + str(qeq_max) + " psf.")
    output.append('')

    return output


#
# footing_1 = footing_surcharge(1, 6, 5, 670, 15000, 20, 30)
# footing_2 = footing_surcharge(1, 6, 15, 668, 15000, 20, 30)
# footing_3 = footing_surcharge(1, 6, 25, 666, 15000, 20, 30)
# footing_4 = footing_surcharge(1, 6, 35, 664, 15000, 20, 30)
# footings = [footing_1, footing_2, footing_3, footing_4]
#
#
# print(combine_footings(footings))
# print(incorporate_footings(footings, combine_footings(footings), layers, work_points))
