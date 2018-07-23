from .Lateral_Pressures import Layer, active_pressures, passive_pressures, water_pressures, \
    net_pressures, active_pressures_front, passive_pressures_back, cant_pressures
from scipy.optimize import fsolve
from sympy import Symbol, solve, re
from shapely.geometry import LineString
import numpy, math, operator

#
# layer_1 = Layer("sand", 0, 120, 0, 0.28, 5.7)
# layer_2 = Layer("sand", 0, 115, 0, 0.36, 4.0)
# layer_3 = Layer("sand", 0, 125, 0, 0.24, 7.5)
#
# # Section elevation parameters
# surface_elev = 602  # Used for computing backside passive pressures
# cut_elev = 600  # Elevation at bottom of excavation
# water_elev = 602  # Elevation of water
# total_weights = 200  # INDEX in the layers list below in which total weight analysis is switched to if necessary
#
# # (height of layer, layer, soil surcharge, footing surcharge, rail surcharge)
# layers = [[602, layer_1, 1000, 0, 0],
#           [600, layer_1, 1000, 0, 0],
#           [588, layer_1, 1000, 0, 0],
#           [588, layer_2, 1000, 0, 0],
#           [584, layer_2, 1000, 0, 0],
#           [584, layer_3, 1000, 0, 0]]
#
# sheet_type = [1, "MSZ18-312", 34.49, 296.05]
#

def cantilever_solver(force_constant, force_z_constant, force_xz_constant, force_x_constant, force_x2_constant,
                      moment_constant, moment_x_constant, moment_z2_constant, moment_xz2_constant, moment_x2_constant,
                      moment_x3_constant):

    x_list = list(numpy.linspace(0, 20, 2001))
    moment_constant_list = []
    force_constant_list = []
    z2_list = []
    z_list = []
    moment_z_list = []
    force_z_list = []

    for x in x_list:
        m_constant = moment_x3_constant*x**3+moment_x2_constant*x**2+moment_x_constant*x+moment_constant
        f_constant = force_x2_constant*x**2+force_x_constant*x+force_constant
        z2 = moment_xz2_constant*x + moment_z2_constant
        z = force_xz_constant*x + force_z_constant
        if m_constant > 0:
            moment_z = 10
        else:
            moment_z = (-1*m_constant/z2)**0.5
        force_z = (-1*f_constant)/z

        moment_constant_list.append(m_constant)
        force_constant_list.append(f_constant)
        z2_list.append(z2)
        moment_z_list.append(moment_z)
        z_list.append(z)
        force_z_list.append(force_z)

    for i in range(len(x_list)-1):
        m_constant = moment_constant_list[i]
        f_constant = force_constant_list[i]
        z2 = z2_list[i]
        z = z_list[i]
        moment_z = moment_z_list[i]
        force_z = force_z_list[i]

        z_diff = abs(moment_z - force_z)
        next_z_diff = abs(moment_z_list[i+1]-force_z_list[i+1])

        if next_z_diff > z_diff:
            x = round(x_list[i], 2)
            z = round(moment_z_list[i], 2)
            break

    return x, z


def minimum_length_cantilever(net_pressures, cant_pressures, cut_elev):
    distances = []
    net_slopes = []
    cant_slopes = []
    solutions = []
    size_dif = len(net_pressures[0]) - len(cant_pressures[0])
    reference_point = ()
    for i in range(size_dif):
        cant_pressures[0].insert(0, 0)
        cant_pressures[1].insert(i, net_pressures[1][i])

    for i in range(len(net_pressures[1])-1):
        distance = -1*(net_pressures[1][i+1]-net_pressures[1][i])
        distances.append(distance)
        if distance != 0:
            net_slope = (net_pressures[0][i+1]-net_pressures[0][i])/distance
            cant_slope = (cant_pressures[0][i+1]-cant_pressures[0][i])/distance
        else:
            net_slope = 0
            cant_slope = 0
        net_slopes.append(net_slope)
        cant_slopes.append(cant_slope)

    for i in range(len(net_pressures[1])-1):
        if net_pressures[1][i] <= cut_elev:
            force_constant = 0
            moment_constant = 0
            for j in range(i):
                force_area = 0.5 * (net_pressures[0][j] + net_pressures[0][j + 1]) * distances[j]
                if 3 * (net_pressures[0][j] + net_pressures[0][j + 1]) != 0:
                    moment_arm = (((2 * net_pressures[0][j] + net_pressures[0][j + 1]) * (distances[j]) /
                                   (3 * (net_pressures[0][j] + net_pressures[0][j + 1])))) + (
                        net_pressures[1][j + 1] - net_pressures[1][i])
                else:
                    moment_arm = (net_pressures[1][j + 1] - net_pressures[1][i])
                force_constant += force_area
                moment_constant += force_area * moment_arm
            for k in range(i, len(net_pressures[1])-1):

                force_x_constant = net_pressures[0][i]
                force_x2_constant = net_slopes[i]/2
                force_xz_constant = (-1*net_slopes[i]+cant_slopes[k])/2
                force_z_constant = (-1 * net_pressures[0][i] +
                                    (cant_pressures[0][k] -
                                     (cant_pressures[1][i] - cant_pressures[1][k]) * cant_slopes[k])) / 2
                moment_x_constant = force_constant
                moment_x2_constant = net_pressures[0][i]/2
                moment_x3_constant = net_slopes[i]/6
                moment_z2_constant = (-1*net_pressures[0][i]+(cant_pressures[0][k] -
                                                              (cant_pressures[1][i] - cant_pressures[1][k]) *
                                                              cant_slopes[k]))/6
                moment_xz2_constant = (-1*net_slopes[i]+cant_slopes[k])/6

                x, z = cantilever_solver(force_constant, force_z_constant, force_xz_constant, force_x_constant,
                                         force_x2_constant, moment_constant, moment_x_constant, moment_z2_constant,
                                         moment_xz2_constant, moment_x2_constant, moment_x3_constant)

                if (net_pressures[1][i]-net_pressures[1][k]) < x < (net_pressures[1][i]-net_pressures[1][k+1]) and 0 < z < x:
                    minimum_length_net_pressure = net_pressures[0][i] + net_slopes[i]*(x-z)
                    minimum_length_cant_pressure = cant_pressures[0][k]\
                                                   + cant_slopes[k]*(x - (net_pressures[1][i]-net_pressures[1][k]))
                    minimum_length_elev = net_pressures[1][i] - x
                    z_elev = minimum_length_elev + z
                    min_length = x + (net_pressures[1][0] - net_pressures[1][i])
                    reference_point = net_pressures[1][i]
                    net_pairs = []
                    cant_pairs = []
                    for h in range(len(net_pressures[1])):
                        net_pairs.append((net_pressures[0][h], net_pressures[1][h]))
                        cant_pairs.append((cant_pressures[0][h], cant_pressures[1][h]))
                    net_linestring = LineString(net_pairs)
                    cant_linestring = LineString(cant_pairs)
                    cross_linestring = LineString([(minimum_length_cant_pressure-5, minimum_length_elev),
                                                   (minimum_length_net_pressure+5, z_elev)])
                    if cross_linestring.crosses(net_linestring) != True:
                        if cross_linestring.crosses(net_linestring) != True:
                            solutions.append([x, z, min_length, minimum_length_elev, minimum_length_net_pressure,
                                              minimum_length_cant_pressure, reference_point, force_constant, force_z_constant,
                                              force_xz_constant, force_x_constant, force_x2_constant, moment_constant,
                                              moment_x_constant, moment_z2_constant, moment_xz2_constant, moment_x2_constant,
                                              moment_x3_constant])
    solutions.sort(key=lambda y: y[0])
    minimum_length = solutions[0][2]
    minimum_length_elev = solutions[0][3]
    minimum_length_net_pressure = solutions[0][4]
    minimum_length_cant_pressure = solutions[0][5]
    output = [("With x=0 @ elev. " + str(solutions[0][6]) + "':"),
              ("Forces: " + str(round(solutions[0][7], 2)) + " + " + str(round(solutions[0][8], 2)) + '*z + ' +
               str(round(solutions[0][9], 2)) + "*x*z + " + str(round(solutions[0][10], 2)) +
               '*x + ' + str(round(solutions[0][11], 2)) + "*x^2 = 0."),
              ("Moments: " + str(round(solutions[0][12], 2)) + " + " + str(round(solutions[0][13], 2)) + '*x + ' +
               str(round(solutions[0][14], 2)) + "*z^2 + " + str(round(solutions[0][15], 2)) +
               '*x*z^2 + ' + str(round(solutions[0][16], 2)) + "*x^2 + " + str(round(solutions[0][17], 2)) + "*x^3 = 0."
               ),
              ("x = " + str(round(solutions[0][0], 2))),
              ("z = " + str(round(solutions[0][1], 2)))
              ]

    return minimum_length, minimum_length_elev, output, minimum_length_net_pressure, minimum_length_cant_pressure, \
           solutions[0][1], solutions[0]


def maximum_moment_cantilever(net_pressures):
    distances = []
    net_slopes = []
    net_pressures_sectioned_pressures = []
    net_pressures_sectioned_elevations = []
    for i in range(len(net_pressures[1]) - 1):
        distance = -1 * (net_pressures[1][i + 1] - net_pressures[1][i])
        distances.append(distance)
        if distance != 0:
            slope = (net_pressures[0][i + 1] - net_pressures[0][i]) / distance
        else:
            slope = 0
        net_slopes.append(slope)
    for i in range(len(net_pressures[0]) - 1):
        p_0 = net_pressures[0][i]
        e_0 = net_pressures[1][i]
        net_pressures_sectioned_pressures.append(p_0)
        net_pressures_sectioned_elevations.append(e_0)
        for j in range(100):
            p_1 = p_0 + net_slopes[i] * distances[i] * (1 / 100)
            e_1 = e_0 - distances[i] * (1 / 100)
            net_pressures_sectioned_pressures.append(p_1)
            net_pressures_sectioned_elevations.append(e_1)
            e_0 = e_1
            p_0 = p_1
    net_pressures = [net_pressures_sectioned_pressures, net_pressures_sectioned_elevations]

    distances = []
    net_slopes = []

    for i in range(len(net_pressures[1]) - 1):
        distance = -1 * (net_pressures[1][i + 1] - net_pressures[1][i])
        distances.append(distance)
        if distance != 0:
            slope = (net_pressures[0][i + 1] - net_pressures[0][i]) / distance
        else:
            slope = 0
        net_slopes.append(slope)
    shear = 0

    for i in range(len(net_pressures[1])-1):
        shear_unit = 0.5*(net_pressures[0][i]+net_pressures[0][i+1])*distances[i]
        old_shear = shear
        shear = shear + shear_unit
        if shear_unit < 0 and old_shear > 0:
            y = Symbol('y')
            answers = solve(old_shear + net_pressures[0][i]*y + net_slopes[i]*y*y/2)
            for j in answers:
                if re(j) > 0 and re(j) < distances[i]:
                    y = j
                    zero_shear_point = net_pressures[1][0] - (net_pressures[1][0] - net_pressures[1][i] + y)

    moment = 0
    for i in range(len(net_pressures[1])-1):
        force = 0.5 * (net_pressures[0][i] + net_pressures[0][i + 1]) * distances[i]
        if 3*(net_pressures[0][i] + net_pressures[0][i+1]) != 0:
            moment_arm = ((2*net_pressures[0][i]+net_pressures[0][i+1])*(distances[i]) /
                          (3*(net_pressures[0][i] + net_pressures[0][i+1]))) + (net_pressures[1][i+1]-zero_shear_point)
        else:
            moment_arm = (net_pressures[1][i+1]-zero_shear_point)
        if y-0.01 < moment_arm < y+0.01:
            moment = moment + net_pressures[0][i+1]*y*y/2 + net_slopes[i+1]*y*y*y/6
        elif moment_arm > 0 and moment_arm != y:
            moment = moment + force*moment_arm

    return moment


def multiplier_cantilever(net_pressures, cant_pressures, minimum_length_data, cut_elev, supplied_length):
    minimum_length = minimum_length_data[0]
    minimum_length_elev = minimum_length_data[1]
    distances = []
    net_slopes = []
    cant_slopes = []
    output = []
    size_dif = len(net_pressures[0]) - len(cant_pressures[0])

    for i in range(size_dif):
        cant_pressures[0].insert(0, 0)
        cant_pressures[1].insert(i, net_pressures[1][i])

    multiplier_length = math.ceil(minimum_length)
    limit = max(net_pressures[1][-1], net_pressures[1][0]-supplied_length-5)
    multiplier_elev = net_pressures[1][0] - multiplier_length
    multiplier_length_list = [multiplier_length]
    multiplier_elev_list = [multiplier_elev]
    while multiplier_elev > limit:
        multiplier_elev += -1
        multiplier_length += 1
        multiplier_length_list.append(multiplier_length)
        multiplier_elev_list.append(multiplier_elev)
    multiplier_list = []

    for i in range(len(net_pressures[1]) - 1):
        distance = -1 * (net_pressures[1][i + 1] - net_pressures[1][i])
        distances.append(distance)
        if distance != 0:
            net_slope = (net_pressures[0][i + 1] - net_pressures[0][i]) / distance
            cant_slope = (cant_pressures[0][i + 1] - cant_pressures[0][i]) / distance
        else:
            net_slope = 0
            cant_slope = 0
        net_slopes.append(net_slope)
        cant_slopes.append(cant_slope)

    for i in range(len(net_pressures[1]) - 1):
        if net_pressures[1][i] <= cut_elev:
            force_constant = 0
            for j in range(i):
                force_area = 0.5 * (net_pressures[0][j] + net_pressures[0][j + 1]) * distances[j]
                force_constant += force_area
            for j in range(i, len(net_pressures[1]) - 1):
                force_x_constant = net_pressures[0][i]
                force_x2_constant = net_slopes[i] / 2
                force_xz_constant = (-1 * net_slopes[i] + cant_slopes[j]) / 2
                force_z_constant = (-1 * net_pressures[0][i] + (cant_pressures[0][j]-(cant_pressures[1][i]-cant_pressures[1][j])*cant_slopes[j])) / 2

                for k in range(len(multiplier_length_list)):
                    x = net_pressures[1][i]-multiplier_elev_list[k]
                    z = Symbol('z')
                    if not force_x_constant == force_xz_constant == force_z_constant == force_x2_constant == 0:
                        z = solve(force_constant+force_z_constant*z+force_xz_constant*x*z + force_x_constant*x +
                                  force_x2_constant*x**2, z)[0]
                    if net_pressures[1][i]-net_pressures[1][j] <= x <= net_pressures[1][i]-net_pressures[1][j+1]:
                        if 0 < x-z <= net_pressures[1][i]-net_pressures[1][i+1]:
                            iter_net_pressure = net_pressures[0][i] + net_slopes[i]*(x-z)
                            iter_cant_elev = net_pressures[1][i] - x
                            iter_cant_pressure = cant_pressures[0][j] + \
                                            cant_slopes[j]*(x - (net_pressures[1][i]-net_pressures[1][j]))
                            iter_net_elev = iter_cant_elev + z
                            net_pairs = []
                            for h in range(len(net_pressures[1])):
                                net_pairs.append((net_pressures[0][h], net_pressures[1][h]))
                            net_linestring = LineString(net_pairs)
                            cross_linestring = LineString([(iter_cant_pressure - 5, iter_cant_elev),
                                                           (iter_net_pressure + 5, iter_net_elev)])
                            if cross_linestring.crosses(net_linestring) != True:
                                ## make new pressure diagram that is the current one
                                pressure_diagram = [[], []]
                                for h in range(len(net_pressures[1])):
                                    if net_pressures[1][h] > iter_net_elev:
                                        pressure_diagram[0].append(net_pressures[0][h])
                                        pressure_diagram[1].append(net_pressures[1][h])
                                pressure_diagram[0].append(iter_net_pressure)
                                pressure_diagram[1].append(iter_net_elev)
                                pressure_diagram[0].append(iter_cant_pressure)
                                pressure_diagram[1].append(iter_cant_elev)
                                pressure_slopes = []
                                pressure_distances = []
                                for m in range(len(pressure_diagram[1]) - 1):
                                    distance = -1 * (pressure_diagram[1][m + 1] - pressure_diagram[1][m])
                                    pressure_distances.append(distance)
                                    if distance != 0:
                                        slope = (pressure_diagram[0][m + 1] - pressure_diagram[0][m]) / distance
                                    else:
                                        slope = 0
                                    pressure_slopes.append(slope)

                                net_pressures_sectioned_pressures = []
                                net_pressures_sectioned_elevations = []
                                for m in range(len(pressure_diagram[0]) - 1):
                                    p_0 = pressure_diagram[0][m]
                                    e_0 = pressure_diagram[1][m]
                                    net_pressures_sectioned_pressures.append(p_0)
                                    net_pressures_sectioned_elevations.append(e_0)
                                    for n in range(100):
                                        p_1 = p_0 + pressure_slopes[m] * pressure_distances[m] * (1 / 100)
                                        e_1 = e_0 - pressure_distances[m] * (1 / 100)
                                        net_pressures_sectioned_pressures.append(p_1)
                                        net_pressures_sectioned_elevations.append(e_1)
                                        e_0 = e_1
                                        p_0 = p_1
                                pressure_diagram = [net_pressures_sectioned_pressures,
                                                    net_pressures_sectioned_elevations]
                                positive_moments = 0
                                negative_moments = 0
                                for m in range(len(pressure_diagram[0])-1):
                                    h = pressure_diagram[1][m] - pressure_diagram[1][m+1]
                                    a = pressure_diagram[0][m]
                                    b = pressure_diagram[0][m+1]
                                    force_area = 0.5 * (a + b) * h
                                    if 3 * (a + b) != 0:
                                        moment_arm = (h*(2*a + b)/(3*(a+b))) + pressure_diagram[1][m+1] - \
                                                     pressure_diagram[1][-1]
                                    else:
                                        moment_arm = pressure_diagram[1][m+1] - pressure_diagram[1][-1]
                                    moment = force_area * moment_arm
                                    if moment >= 0:
                                        positive_moments += moment
                                    else:
                                        negative_moments += moment
                                multiplier = -1 * negative_moments / positive_moments
                                multiplier_list.append((multiplier_length_list[k], multiplier_elev_list[k], multiplier,
                                                        x, z, iter_net_pressure, iter_cant_pressure, positive_moments, negative_moments, force_constant, force_z_constant, force_xz_constant, force_x_constant, force_x2_constant, net_pressures[0][i], cant_pressures[0][j]))

    print(multiplier_list)
    multiplier_list = sorted(multiplier_list, key=operator.itemgetter(0, 2))
    new_list = []
    check = []
    for i in range(len(multiplier_list)):
        if multiplier_list[i][0] not in check:
            new_list.append(multiplier_list[i])
            check.append(multiplier_list[i][0])
    multiplier_list = new_list
    multi_x = []
    multi_y = []
    multi = []
    if supplied_length != []:
        for i in range(len(multiplier_list)):
            if multiplier_list[i][0] == supplied_length:
                multi_x = [multiplier_list[i][5], multiplier_list[i][6]]
                multi_y = [multiplier_list[i][1]+multiplier_list[i][4], multiplier_list[i][1]]
                multi = multiplier_list[i][2]
                break
    for i in range(len(multiplier_list)):
        if multiplier_list[i][2] <= 50:
            output_string = "With " + str(multiplier_list[i][0]) + "' long ERS tipped @ Elev. " + str(multiplier_list[i][1])\
                            + "': Mult = " + str(round(multiplier_list[i][2], 2))
            output.append(output_string)
    print(multiplier_list)

    return output, multi_x, multi_y, multi


def deflection_calc_cantilever(net_pressures, minimum_length_data, sheet_type):
    distances = []
    net_slopes = []
    modulus = 29000000
    inertia = sheet_type[3]
    def_list = []
    max_deflection = 0
    max_deflection_elev = 0
    minimum_length_elev = minimum_length_data[1]
    x_elev = minimum_length_elev
    z_elev = x_elev + minimum_length_data[5]
    x_pressure = minimum_length_data[4]
    z_pressure = minimum_length_data[3]

    new_net_pressures = []
    new_net_elevations = []
    for i in range(len(net_pressures[0])):
        if net_pressures[1][i] >= z_elev:
            new_net_pressures.append(net_pressures[0][i])
            new_net_elevations.append(net_pressures[1][i])
    new_net_pressures.append(z_pressure)
    new_net_pressures.append(x_pressure)
    new_net_elevations.append(z_elev)
    new_net_elevations.append(x_elev)
    net_pressures = [new_net_pressures, new_net_elevations]

    for i in range(len(net_pressures[1]) - 1):
        distance = -1 * (net_pressures[1][i + 1] - net_pressures[1][i])
        distances.append(distance)
        if distance != 0:
            slope = (net_pressures[0][i + 1] - net_pressures[0][i]) / distance
        else:
            slope = 0
        net_slopes.append(slope)

    net_pressures_sectioned_pressures = []
    net_pressures_sectioned_elevations = []
    for i in range(len(net_pressures[0]) - 1):
        p_0 = net_pressures[0][i]
        e_0 = net_pressures[1][i]
        net_pressures_sectioned_pressures.append(p_0)
        net_pressures_sectioned_elevations.append(e_0)
        for j in range(100):
            p_1 = p_0 + net_slopes[i] * distances[i] * (1 / 100)
            e_1 = e_0 - distances[i] * (1 / 100)
            net_pressures_sectioned_pressures.append(p_1)
            net_pressures_sectioned_elevations.append(e_1)
            e_0 = e_1
            p_0 = p_1
    net_pressures = [net_pressures_sectioned_pressures, net_pressures_sectioned_elevations]

    for i in range(len(net_pressures[1])):
        def_list.append([0, net_pressures[1][i]])

    for i in range(len(net_pressures[0])-1):
        p = 0.5*(net_pressures[0][i]+net_pressures[0][i+1])*(net_pressures[1][i]-net_pressures[1][i+1])
        p_elev = 0.5 * (net_pressures[1][i]+net_pressures[1][i+1])
        l = net_pressures[1][0] - net_pressures[1][-1]
        for j in range(len(def_list)):
            b = net_pressures[1][0] - p_elev
            a = l-b
            x = l - (net_pressures[1][0] - def_list[j][1])
            if x <= a:
                deflect = p*x*x*(3*a-x)/6
            else:
                deflect = p*a*a*(3*x-a)/6
            def_list[j][0] += deflect
    for i in range(len(def_list)):
        deflect = def_list[i][0]
        def_list[i][0] = deflect*1728/(modulus*inertia)

    max_deflection = round(def_list[0][0], 3)
    max_deflection_elev = round(def_list[0][1], 2)


    return def_list, max_deflection, max_deflection_elev


# net = [[35, 292, 631, 539, 1106, 1096, -3366, -5077, -4886, -6314,-10006, -5791, -6141, -10175],
#        [740, 734, 730, 730, 724.17, 723.25, 718, 716, 716, 714.33, 710, 710, 703, 703]]
# cant = [[0, 0, 250, 250, 614, 5745, 6050, 6166, 10527, 10984, 12169, 8448, 8829, 16835],
#         [740, 734, 730, 730, 724.17, 723.25, 718, 716, 716, 714.33, 710, 710, 703, 703]]
# cut_elev = 723.25
# active = active_pressures(layers, water_elev, total_weights)
# passive = passive_pressures(layers, water_elev, cut_elev, total_weights)
# water = water_pressures(layers, water_elev, cut_elev, total_weights)
# net = net_pressures(active, passive, water, cut_elev)
# active_front = active_pressures_front(layers, water_elev, cut_elev, total_weights)
# passive_back = passive_pressures_back(layers, water_elev, cut_elev, surface_elev, total_weights)
# cant = cant_pressures(active_front, passive_back, water)
# min = minimum_length_cantilever(net, cant, cut_elev)
# mult = multiplier_cantilever(net, cant, min, cut_elev, 30)
# deflect = deflection_calc_cantilever(net, min, [64, "SKZ 38", 62.32, 560.85])
# print(min)
# print(mult)
# print(deflect)
