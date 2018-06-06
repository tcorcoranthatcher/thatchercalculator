from shapely.geometry import LineString, Polygon
import math
import numpy
# from Lateral_Pressures import Layer, passive_pressures
#
#
# layer_1 = Layer("sand", 0, 120, 0, 0.33, 4.0, 30)
# layer_2 = Layer("clay", 1, 130, 2.0, 1, 1, 0)
#
#
#
# surface_side = -1
# layers = [[10, layer_1, 0, 0, 0, 0, 0],
#           [0, layer_1, 0, 0, 0, 0, 0],
#           [-4, layer_1, 0, 0, 0, 0, 0],
#           [-4, layer_2, 0, 0, 0, 0, 0],
#           [-8, layer_2, 0, 0, 0, 0, 0],
#           [-8, layer_1, 0, 0, 0, 0, 0],
#           [-12, layer_1, 0, 0, 0, 0, 0],
#           [-16, layer_1, 0, 0, 0, 0, 0],
#           [-16, layer_2, 0, 0, 0, 0, 0]]
#
# surface_array = [(0, 0),
#                  (4, 0),
#                  (8, -4),
#                  (12, -4),
#                  (16, -8),
#                  (20, -8),
#                  (24, -12),
#                  (28, -12),
#                  (32, -16)]
#
# # surface_array = [(0,0),
# #                  (100, 0)]
#
# cut_elev = 0
#
# angle = 55
# angle_change_type = 0
# angle_change_elev = []
# min_surcharge_height = []
#

def surcharge_heights(surface_side, surface_array, work_points, angle, angle_change_elev, angle_change_type,
                      min_surcharge_height):
    output = []
    y_coords = []

    for i in range(len(surface_array)):
        y_coords.append(surface_array[i][1])

    search_heights = []
    search_heights = list(numpy.linspace(min(y_coords), max(y_coords), num=(max(y_coords)-min(y_coords))*100+1))
    for i in range(len(search_heights)):
        search_heights[i] = round(search_heights[i], 2)

    for work_point in work_points:
        if angle_change_type == 0 or work_point[1] >= angle_change_elev:
            failure_line = LineString([work_point, (surface_side*1000, 1000*math.tan(math.radians(angle)) +
                                                    work_point[1])])
        if angle_change_type == 1 and work_point[1] < angle_change_elev:
            l = angle_change_elev - work_point[1]
            x = l*math.tan(math.radians(55))-l
            new_work_point = (work_point[0], work_point[1]-x)
            failure_line = LineString([new_work_point, (surface_side*1000, 1000*math.tan(math.radians(angle)) +
                                                        new_work_point[1])])
        if angle_change_type == 2 and work_point[1] < angle_change_elev:
            l = angle_change_elev - work_point[1]
            x = l-l/math.tan(math.radians(55))
            new_work_point = (work_point[0], work_point[1]+x)
            failure_line = LineString([new_work_point, (surface_side*1000, 1000*math.tan(math.radians(angle)) +
                                                        new_work_point[1])])

        for i in range(len(search_heights)):
            search_line = ((-1000, search_heights[i]), (1000, search_heights[i]))

            search_linestring = LineString([(search_line[0]), (search_line[1])])
            area_1_points = [(surface_array[0])]
            area_2_points = []

            for j in range(len(surface_array)-1):

                surface_segment = LineString([surface_array[j], surface_array[j+1]])
                int_1 = search_linestring.intersection(surface_segment)
                if int_1:
                    if j >= 1:
                        for k in range(j):
                            area_1_points.append(surface_array[k+1])
                    area_1_points.append((int_1.bounds[0], int_1.bounds[1]))
                    area_1_points.append((int_1.bounds[2], int_1.bounds[3]))
                    area_1_points.append((0, search_heights[i]))
                    if surface_side == -1:
                        area_2_points.append((int_1.bounds[0], int_1.bounds[1]))
                    else:
                        area_2_points.append((int_1.bounds[2], int_1.bounds[3]))

                    int_2 = failure_line.intersection(search_linestring)
                    for k in range(j, len(surface_array)-1):
                        surface_segment = LineString([surface_array[k], surface_array[k + 1]])
                        int_3 = failure_line.intersection(surface_segment)
                        if int_3 and int_2:
                            height = surface_array[k + 1][1] - surface_array[k][1]
                            for l in range(j, k):
                                area_2_points.append(surface_array[l+1])
                            area_2_points.append((int_3.bounds[0], int_3.bounds[1]))
                            area_2_points.append((int_3.bounds[2], int_3.bounds[3]))
                            area_2_points.append((int_2.bounds[0], int_2.bounds[1]))
                            area_2_points.append((int_2.bounds[2], int_2.bounds[3]))
                            break
                    break

            if len(area_1_points) and len(area_2_points) > 3:
                area_1 = Polygon(area_1_points)
                area_2 = Polygon(area_2_points)
                if height >= 0:
                    if area_1.area >= area_2.area:
                        if min_surcharge_height:
                            if round(search_heights[i] * 4) / 4.0 > min_surcharge_height:
                                output.append((work_point[1], round(search_heights[i]*4)/4.0))
                            else:
                                output.append((work_point[1], min_surcharge_height))
                        else:
                            output.append((work_point[1], round(search_heights[i] * 4) / 4.0))
                        break
                else:
                    if area_1.area <= area_2.area:
                        if min_surcharge_height:
                            if round(search_heights[i] * 4) / 4.0 > min_surcharge_height:
                                output.append((work_point[1], round(search_heights[i]*4)/4.0))
                            else:
                                output.append((work_point[1], min_surcharge_height))
                        else:
                            output.append((work_point[1], round(search_heights[i] * 4) / 4.0))
                        break

    return output


def passive_heights(surface_side, surface_array, layers, cut_elev):
    output = []
    y_coords = []

    for i in range(len(surface_array)):
        y_coords.append(surface_array[i][1])

    surface_linestring = LineString(surface_array)

    for layer in layers:
        if layer[0] > cut_elev:
            layer[5] = cut_elev
        else:
            failure_line = LineString([(0, layer[0]), (-1*surface_side * 1000, 1000 * math.tan(math.radians(45-layer[1].phi/2)) + layer[0])])
            intersection = failure_line.intersection(surface_linestring)
            layer[5] = (round(intersection.bounds[1] * 4) / 4.0)

    return layers

#
# print(passive_heights(surface_side, surface_array, layers, cut_elev))

