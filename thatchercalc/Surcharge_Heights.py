from shapely.geometry import LineString, Polygon
import math
import numpy

surface_side = -1
work_points = [(0.0, 0), (0.0, -3), (0.0, -20)]
surface_array = [(0, 0),
                 (-5, -5),
                 (-10, -8),
                 (-50, -20)]

angle = 55
angle_change_type = 0
angle_change_elev = []
min_surcharge_height = []


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
