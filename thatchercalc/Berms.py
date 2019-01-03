from .Lateral_Pressures import Layer, passive_pressures
from .Surcharge_Heights import passive_heights
from shapely.geometry import LineString, Polygon
import math

# berm_array = [(0, 0),
#               (4, 0),
#               (8, -4),
#               (12, -4),
#               (16, -8),
#               (20, -8),
#               (24, -12),
#               (28, -12),
#               (32, -16)]
#
# layer_1 = Layer("sand", 0, 120, 0, 0.33, 4.0, 30)
# layer_2 = Layer("clay", 1, 130, 2.0, 1, 1, 0)
#
# layers = [[10, layer_1, 0, 0, 0, 10000, 0],
#           [0, layer_1, 0, 0, 0, 10000, 0],
#           [-4, layer_1, 0, 0, 0, 10000, 0],
#           [-4, layer_2, 0, 0, 0, 10000, 0],
#           [-8, layer_2, 0, 0, 0, 10000, 0],
#           [-8, layer_1, 0, 0, 0, 10000, 0],
#           [-16, layer_1, 0, 0, 0, 10000, 0],
#           [-16, layer_2, 0, 0, 0, 10000, 0]]
#
# work_points =[[0, 10],
#               [0, 0],
#               [0, -4],
#               [0, -4],
#               [0, -8],
#               [0, -8],
#               [0, -16],
#               [0, -16]]
#
# cut_elev = 0


def berm_workpoints(layers, work_points, berm_array, cut_elev):
    y_list = [cut_elev]
    for i in range(len(berm_array)):
        y = berm_array[i][1]
        if y not in y_list and y < min(y_list):
            y_list.append(y)
    y_list.remove(cut_elev)

    for y in y_list:
        for i in range(len(work_points)):
            if work_points[i][1] > y > work_points[i+1][1]:
                work_points.insert(i+1, [0, y])
                break
        for i in range(len(layers)):
            if layers[i][0] > y > layers[i+1][0]:
                new_layer = [y, layers[i][1], 0, 0, 0, 10000]
                layers.insert(i+1, new_layer)
                break

    return layers, work_points


def berm_reduction(layers, berm_array, cut_elev, passive_pressure, water_elev, total_weights):
    old_passive_pressure = passive_pressure
    y_list = []
    for berm_point in berm_array:
        y_list.append(berm_point[1])
    berm_bottom = min(y_list)

    # BEGIN FINDING WEIGHT OF BERM AT EACH WORK POINT
    unit_weights = []
    for i in range(len(layers)):
        if layers[i][0] < water_elev:
            if i <= total_weights:
                unit_weight = layers[i][1].sub - layers[i][-1]
            else:
                unit_weight = layers[i][1].gamma - layers[i][-1]
        else:
            unit_weight = layers[i][1].gamma - layers[i][-1]
        unit_weights.append([layers[i][0], unit_weight])

    berm_weights = []
    weight = 0
    for i in range(len(layers)):
        if layers[i][0] >= cut_elev:
            weight += 0
        elif layers[i][0] < berm_bottom:
            weight = 0
        else:
            area_points = [(0, layers[i][0]), (0, layers[i-1][0])]
            for area_point in berm_array:
                if layers[i-1][0] >= area_point[1] >= layers[i][0]:
                    area_points.append(area_point)
            if layers[i][0] != layers[i-1][0]:
                weight_poly = Polygon(area_points)
                area = weight_poly.area
                weight += area * unit_weights[i][1]


        berm_weights.append([layers[i][0], weight])
    # FIND LENGTH l AT EACH WORKPOINT
    berm_line = LineString(berm_array)
    length_list = []
    for i in range(len(layers)):
        if layers[i][0] >= cut_elev:
            length_list.append((layers[i][0], 0))
        elif layers[i][0] < berm_bottom:
            length_list.append(1000000000)
        else:
            search_line = LineString([(-1000, layers[i][0]), (1000, layers[i][0])])
            intersection = search_line.intersection(berm_line)
            length = abs(intersection.bounds[0])
            length_list.append([layers[i][0], length])

    limiters = []
    for i in range(len(layers)):
        if layers[i][0] >= berm_bottom:
            if layers[i][1].type == 0:
                limiter = berm_weights[i][1]*math.tan(math.radians(layers[i][1].phi))
            else:
                limiter = length_list[i][1]*layers[i][1].qu*1000
        else:
            limiter = 10000000000000000
        limiters.append([layers[i][0], math.ceil(limiter)])

    new_passives = []
    for i in range(len(passive_pressure)):
        new_passives.append([passive_pressure[i][0], passive_pressure[i][1]])
    passive_pressure = new_passives

    slopes = []
    for i in range(len(passive_pressure)-1):
        distance = -1*(passive_pressure[i+1][0]-passive_pressure[i][0])
        if distance != 0:
            slope = (passive_pressure[i+1][1]-passive_pressure[i][1])/distance
        else:
            slope = 0
        slopes.append(slope)

    total_passives = []
    for i in range(len(layers)):
        if layers[i][0] >= cut_elev:
            total_passives.append([layers[i][0], 0])
        else:
            if layers[i][0] != layers[i-1][0]:
                total_passive = 0
                for j in range(1, i+1):
                    if layers[j-1][0] <= cut_elev:
                        total_passive += (passive_pressure[j-1][1] + passive_pressure[j][1])/2 * (passive_pressure[j-1][0] - passive_pressure[j][0])
                total_passives.append([layers[i][0], total_passive])
                if total_passive > limiters[i][1]:
                    current_passive = 0
                    for j in range(1, i):
                        if layers[j - 1][0] <= cut_elev:
                            current_passive += (passive_pressure[j-1][1] + passive_pressure[j][1])/2 * (passive_pressure[j-1][0] - passive_pressure[j][0])
                    limit = limiters[i][1] - current_passive
                    p0 = passive_pressure[i-1]
                    p1 = passive_pressure[i]
                    length = -1*(p1[0] - p0[0])
                    slope = slopes[i-1]
                    np0 = limit/length - slope*length/2
                    if np0 < 0:
                        np0 = 0
                        np1 = 2*limit/length
                    elif np0 > p0[1]:
                        np0 = p0[1]
                        np1 = 2*limit/length - p0[1]
                        if np1 > p1[1]:
                            np1 = p1[1]
                    else:
                        np1 = slope*length + np0
                    passive_pressure[i-1][1] = math.floor(np0)
                    passive_pressure[i][1] = math.floor(np1)
                else:
                    pass
            else:
                total_passive = 0
                for j in range(1, i+1):
                    if layers[j - 1][0] <= cut_elev:
                        total_passive += (passive_pressure[j - 1][1] + passive_pressure[j][1]) / 2 * (passive_pressure[j - 1][0] - passive_pressure[j][0])
                total_passives.append([layers[i][0], total_passive])
                if total_passive > limiters[i][1]:
                    current_passive = 0
                    for j in range(1, i - 1):
                        if layers[j - 1][0] <= cut_elev:
                            current_passive += (passive_pressure[j - 1][1] + passive_pressure[j][1]) / 2 * \
                                               (passive_pressure[j - 1][0] - passive_pressure[j][0])
                    limit = limiters[i][1] - current_passive
                    p0 = passive_pressure[i-2]
                    p1 = passive_pressure[i-1]
                    length = -1*(p1[0] - p0[0])
                    slope = slopes[i-2]
                    np0 = limit/length - slope*length/2
                    if np0 < 0:
                        np0 = 0
                        np1 = 2*limit/length
                    elif np0 > p0[1]:
                        np0 = p0[1]
                        np1 = 2*limit/length - p0[1]
                        if np1 > p1[1]:
                            np1 = p1[1]
                    else:
                        np1 = slope*length + np0
                    passive_pressure[i-2][1] = math.floor(np0)
                    passive_pressure[i-1][1] = math.floor(np1)
                else:
                    pass
    new_passives = []
    for i in range(len(passive_pressure)):
        new_passives.append((passive_pressure[i][0], passive_pressure[i][1]))
    passive_pressure = new_passives
    output = []
    for i in range(len(layers)):
        output_string = ""
        if layers[i][0] >= cut_elev or layers[i][0] < berm_bottom:
            pass
        else:
            if layers[i][0] != layers[i - 1][0]:
                if total_passives[i][1] > limiters[i][1]:
                    output_string += "At elev. " + str(layers[i][0]) + "', total passive of " + str(total_passives[i][1]) + " #/' is greater than the shear limiter of "
                    if layers[i][1].type == 0:
                        output_string += "σ'tan(ϕ) = " + str(limiters[i][1]) + " #/'"
                    else:
                        output_string += "c*l = " + str(limiters[i][1]) + " #/'"
                    output.append(output_string)
                    output_string = ""
                    output_string += "      Change Pp @ " + str(layers[i-1][0]) + "' from " + str(old_passive_pressure[i-1][1]) + " psf to " + str(passive_pressure[i-1][1]) + " psf "
                    output.append(output_string)
                    output_string = ""
                    output_string += "      Change Pp @ " + str(layers[i][0]) + "' from " + str(
                        old_passive_pressure[i][1]) + " psf to " + str(passive_pressure[i][1]) + " psf "
                    output.append(output_string)
            else:
                if total_passives[i][1] > limiters[i][1]:
                    output_string += "At elev. " + str(layers[i][0]) + "', total passive of " + str(
                        total_passives[i][1]) + " #/' is greater than the shear limiter of "
                    if layers[i][1].type == 0:
                        output_string += "σ'tan(ϕ) = " + str(limiters[i][1]) + " #/'"
                    else:
                        output_string += "c*l = " + str(limiters[i][1]) + " #/'"
                    output.append(output_string)
                    output_string = ""
                    output_string += "      Change Pp @ " + str(layers[i - 2][0]) + "' from " + str(
                        old_passive_pressure[i - 2][1]) + " psf to " + str(passive_pressure[i - 2][1]) + " psf "
                    output.append(output_string)
                    output_string = ""
                    output_string += "      Change Pp @ " + str(layers[i - 1][0]) + "' from " + str(
                        old_passive_pressure[i-1][1]) + " psf to " + str(passive_pressure[i-1][1]) + " psf "
                    output.append(output_string)

    if old_passive_pressure != passive_pressure:
        output.append("")
        output.append("Revised passive pressures due to the berm:")
        for i in range(len(passive_pressure)):
            if passive_pressure[i][0] <= cut_elev:
                output.append("Pp @ " + str(passive_pressure[i][0]) + "' = " + str(passive_pressure[i][1]) + " psf")
    return passive_pressure, output


