import math
from sympy import Symbol, solve, re
from .Lateral_Pressures import Layer, active_pressures, passive_pressures, water_pressures, net_pressures


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
#
# # (height of layer, layer, total surcharge(convert soil surcharge height to psf))
# layers = [[670, layer_1, 0, 0],
#           [668, layer_1, 0, 0],
#           [668, layer_2, 0, 0],
#           [666, layer_2, 0, 0],
#           [661, layer_2, 0, 0],
#           [661, layer_3, 0, 0],
#           [658, layer_3, 0, 0],
#           [647, layer_3, 0, 0]]
#
# sheet_type = [6, "MSZ14-312", 19.62, 120.97]


def minimum_length(net_pressures, brace_elev):
    distances = []
    net_slopes = []
    waler_load = 0
    reference_point = ()
    moment_constant = ()
    moment_x_constant = ()
    moment_x2_constant = ()
    moment_x3_constant = ()
    minimum_length = ()
    minimum_length_pressure = ()
    minimum_length_elev = ()

    for i in range(len(net_pressures[1])-1):
        distance = -1*(net_pressures[1][i+1]-net_pressures[1][i])
        distances.append(distance)
        if distance != 0:
            slope = (net_pressures[0][i+1]-net_pressures[0][i])/distance
        else:
            slope = 0
        net_slopes.append(slope)
    for i in range(len(net_pressures[1])-1):
        compute_string = ""
        text_output_moments = []
        if net_pressures[0][i] >= 0 > net_pressures[0][i+1] or net_pressures[0][i] < 0:
            moment_constant = 0
            for j in range(i):
                force_area = 0.5 * (net_pressures[0][j] + net_pressures[0][j + 1]) * distances[j]
                compute_string += "0.5*(" + str(net_pressures[0][j]) + " + " + str(net_pressures[0][j + 1]) + ")*(" + \
                                  str(round(distances[j], 2)) + ")"
                if (3 * (net_pressures[0][j] + net_pressures[0][j + 1])) != 0:
                    moment_arm = brace_elev - (((2 * net_pressures[0][j] + net_pressures[0][j + 1]) * (distances[j]) /
                                                (3 * (net_pressures[0][j] + net_pressures[0][j + 1]))) +
                                               net_pressures[1][j+1])
                    compute_string += "*(" + str(round(moment_arm, 2))+ ")"
                else:
                    moment_arm = brace_elev - net_pressures[1][j+1]
                    compute_string += "*(" + str(round(moment_arm, 2)) + ")"
                moment_constant = moment_constant + force_area*moment_arm
                text_output_moments.append(compute_string)
                compute_string = ""
            moment_x_constant = net_pressures[0][i] * (brace_elev - net_pressures[1][i])
            moment_x2_constant = net_pressures[0][i]/2 + net_slopes[i]*(brace_elev - net_pressures[1][i])/2
            moment_x3_constant = net_slopes[i]/3
            text_output_moments.append(str(round(net_pressures[0][i],2))+
                                       "*(x)*("+str(round(brace_elev - net_pressures[1][i], 2))+" + x/2)")
            text_output_moments.append(
                str(round(net_slopes[i],2)) + "*(x)*(x/2)*(" + str(round(brace_elev - net_pressures[1][i], 2)) +
                " + 2x/3)")

            x = Symbol('x')
            solutions = solve(moment_constant + moment_x_constant*x + moment_x2_constant*x*x + moment_x3_constant*x*x*x,
                              x, complex=False)
            for j in solutions:
                if 0 < re(j) < distances[i]:
                    x_distance = re(j)
                    minimum_length_pressure = net_pressures[0][i]+net_slopes[i]*x_distance
                    minimum_length_elev = net_pressures[1][i] - re(j)
                    minimum_length = re(j)+(net_pressures[1][0]-net_pressures[1][i])
                    reference_point = net_pressures[1][i]
                    break
            else:
                continue  # executed if the loop ended normally (no break)
            break  # executed if 'continue' was skipped (break)

    for i in range(len(net_pressures[1])-1):
        if net_pressures[1][i] >= minimum_length_elev >= net_pressures[1][i+1]:
            waler_load = waler_load + 0.5*net_slopes[i]*x_distance*x_distance + net_pressures[0][i]*x_distance
        elif net_pressures[1][i] >= minimum_length_elev:
            waler_load = waler_load + 0.5*(net_pressures[0][i]+net_pressures[0][i+1])*distances[i]

    output = "With x=0 @ elev. " + \
             str(reference_point) + "': \n" + str(round(moment_constant, 2)) + " + " +\
             str(round(moment_x_constant, 2)) + '*x + ' + str(round(moment_x2_constant, 2)) + "*x^2 + " + str(round(moment_x3_constant, 2)) + \
             '*x^3 = 0.  x = ' + str(round(x_distance, 2)) + "."

    return minimum_length, minimum_length_elev, waler_load, output, minimum_length_pressure, text_output_moments


def maximum_moment(net_pressures, waler_load, brace_elev):
    distances = []
    net_slopes = []
    net_pressures_sectioned_pressures = []
    net_pressures_sectioned_elevations = []
    for i in range(len(net_pressures[1])-1):
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

    for i in range(len(net_pressures[1])-1):
        distance = -1 * (net_pressures[1][i + 1] - net_pressures[1][i])
        distances.append(distance)
        if distance != 0:
            slope = (net_pressures[0][i + 1] - net_pressures[0][i]) / distance
        else:
            slope = 0
        net_slopes.append(slope)
    shear = waler_load

    for i in range(len(net_pressures[1])-1):
        shear_unit = 0.5*(net_pressures[0][i]+net_pressures[0][i+1])*distances[i]
        old_shear = shear
        shear = shear - shear_unit
        if old_shear >= 0 and shear <= 0:
            y = Symbol('y')
            answers = solve(-old_shear + net_pressures[0][i]*y + net_slopes[i]*y*y/2)
            for j in answers:
                if j > 0 and j < distances[i]:
                    y = j
                    zero_shear_point = net_pressures[1][0] - (net_pressures[1][0] - net_pressures[1][i] + y)
    moment = waler_load*(brace_elev-zero_shear_point)
    max_elevation = zero_shear_point
    for i in range(len(net_pressures[1])-1):
        force = 0.5 * (net_pressures[0][i] + net_pressures[0][i + 1]) * distances[i]
        if 3*(net_pressures[0][i]+net_pressures[0][i+1]) != 0:
            moment_arm = ((2*net_pressures[0][i]+net_pressures[0][i+1])*(distances[i]) /
                          (3*(net_pressures[0][i]+net_pressures[0][i+1]))) + (net_pressures[1][i+1]-zero_shear_point)
        else:
            moment_arm = net_pressures[1][i+1]-zero_shear_point
        if y-0.01 < moment_arm < y+0.01:
            moment = moment - net_pressures[0][i+1]*y*y/2 + net_slopes[i+1]*y*y*y/6
        elif moment_arm > 0 and moment_arm != y:
            moment = moment - force*moment_arm

    return moment, max_elevation


def multiplier(net_pressures, brace_elev, minimum_length_data, supplied_length):
    minimum_length = minimum_length_data[0]
    minimum_length_elev = minimum_length_data[1]
    distances = []
    net_slopes = []
    multiplier_length = math.ceil(minimum_length)
    multiplier_elev = net_pressures[1][0] - multiplier_length
    multiplier_length_list = [multiplier_length]
    multiplier_elev_list = [multiplier_elev]
    while multiplier_elev > net_pressures[1][-1]:
        multiplier_elev += -1
        multiplier_length += 1
        multiplier_length_list.append(multiplier_length)
        multiplier_elev_list.append(multiplier_elev)
    multiplier_list = []
    output = []
    for i in range(len(net_pressures[1])-1):
        distance = -1*(net_pressures[1][i+1]-net_pressures[1][i])
        distances.append(distance)
        if distance != 0:
            slope = (net_pressures[0][i+1]-net_pressures[0][i])/distance
        else:
            slope = 0
        net_slopes.append(slope)

    net_pressures_sectioned_pressures = []
    net_pressures_sectioned_elevations = []
    slope_list = []
    for i in range(len(net_pressures[0]) - 1):
        p_0 = net_pressures[0][i]
        e_0 = net_pressures[1][i]
        net_pressures_sectioned_pressures.append(p_0)
        net_pressures_sectioned_elevations.append(e_0)
        for j in range(100):
            p_1 = p_0+net_slopes[i]*distances[i]*(1/100)
            e_1 = e_0 - distances[i]*(1/100)
            net_pressures_sectioned_pressures.append(p_1)
            net_pressures_sectioned_elevations.append(e_1)
            slope_list.append(net_slopes[i])
            e_0 = e_1
            p_0 = p_1

    net_pressures = [net_pressures_sectioned_pressures, net_pressures_sectioned_elevations, slope_list]

    for i in range(len(multiplier_elev_list)):
        negative_moments = 0
        positive_moments = 0
        multiplier_compute_list = []
        for j in range(len(net_pressures[1])):
            if net_pressures[1][j] >= multiplier_elev_list[i]:
                multiplier_compute_list.append((net_pressures[0][j], net_pressures[1][j]))
            if net_pressures[1][j] < multiplier_elev_list[i]:
                y1 = net_pressures[1][j-1]
                y2 = multiplier_elev_list[i]
                d = y1-y2
                slope = net_pressures[2][i]
                mult_pressure = net_pressures[0][j-1] + d*slope
                multiplier_compute_list.append((mult_pressure, multiplier_elev_list[i]))
                break
        for j in range(len(multiplier_compute_list)-1):
            h = multiplier_compute_list[j][1]-multiplier_compute_list[j+1][1]
            a = multiplier_compute_list[j][0]
            b = multiplier_compute_list[j+1][0]
            force_area = 0.5 * (a+b) * h
            if 3*(a+b) != 0:
                moment_arm = brace_elev - ((h*(2*a+b)/(3*(a+b))) + multiplier_compute_list[j+1][1])
            else:
                moment_arm = brace_elev - multiplier_compute_list[j+1][1]
            moment = force_area*moment_arm
            if moment >= 0:
                positive_moments += moment
            else:
                negative_moments += moment
        multiplier = -1 * negative_moments/positive_moments
        multiplier_list.append((multiplier_length_list[i], multiplier_elev_list[i], multiplier,
                                multiplier_compute_list[-1][0], negative_moments, positive_moments))

    multi_pressure = []
    multi_elev = []
    mult = 0
    if supplied_length != []:
        for i in range(len(multiplier_list)):
            if multiplier_list[i][0] == supplied_length:
                multi_pressure = multiplier_list[i][3]
                multi_elev = multiplier_list[i][1]
                mult = multiplier_list[i][2]
                break

    text_output = []
    for i in range(len(multiplier_list)):
        if multiplier_list[i][2] <= 50:
            if multiplier_list[i][0] != supplied_length:
                output_string = "With " + str(multiplier_list[i][0]) + "' long ERS tipped @ Elev. " + \
                                str(multiplier_list[i][1]) + "': Mult = " + str(round(multiplier_list[i][2], 2))
            else:
                output_string = "With " + str(multiplier_list[i][0]) + "' long ERS tipped @ Elev. " + \
                                str(multiplier_list[i][1]) + "': Mult = " + str(round(multiplier_list[i][2], 2))
                text_output = "With supplied length = " + str(supplied_length) + "': Resisting moment = " + str(-1*round(multiplier_list[i][4],2)) + "#'.  Driving moment = "\
                                + str(round(multiplier_list[i][5], 2)) + "#'"

            output.append(output_string)

    return output, multi_pressure, multi_elev, mult, text_output


def deflection_calc(net_pressures, brace_elev, minimum_length_data, sheet_type):
    distances = []
    net_slopes = []
    modulus = 29000000
    inertia = sheet_type[3]
    def_list = [[0, brace_elev]]
    max_deflection = 0
    max_deflection_elev = 0
    minimum_length_elev = minimum_length_data[1]

    for i in range(len(net_pressures[1])-1):
        distance = -1*(net_pressures[1][i+1]-net_pressures[1][i])
        distances.append(distance)
        if distance != 0:
            slope = (net_pressures[0][i+1]-net_pressures[0][i])/distance
        else:
            slope = 0
        net_slopes.append(slope)

    net_pressures_sectioned_pressures = []
    net_pressures_sectioned_elevations = []
    for i in range(len(net_pressures[0])-1):
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
        if minimum_length_elev < net_pressures[1][i] < brace_elev:
            def_list.append([0, net_pressures[1][i]])

    net_pressures_sectioned_pressures = []
    net_pressures_sectioned_elevations = []
    for i in range(len(net_pressures[1])):
        if net_pressures[1][i] >= minimum_length_elev:
            net_pressures_sectioned_pressures.append(net_pressures[0][i])
            net_pressures_sectioned_elevations.append(net_pressures[1][i])
    net_pressures = [net_pressures_sectioned_pressures, net_pressures_sectioned_elevations]

    for i in range(len(net_pressures[0])-1):
        p = 0.5*(net_pressures[0][i]+net_pressures[0][i+1])*(net_pressures[1][i]-net_pressures[1][i+1])
        p_elev = 0.5 * (net_pressures[1][i]+net_pressures[1][i+1])
        l = brace_elev - net_pressures[1][-1]
        if p_elev > brace_elev:
            for j in range(len(def_list)):
                a = p_elev - brace_elev
                x = def_list[j][1] - net_pressures[1][-1]
                deflect = p*a*x*(l*l-x*x)/(6*l)
                def_list[j][0] += deflect

        if p_elev < brace_elev:
            for j in range(len(def_list)):
                a = p_elev - net_pressures[1][-1]
                b = l-a
                x = def_list[j][1] - net_pressures[1][-1]
                if x <= a:
                    # print(2, p_elev, def_list[j][1], x, a)
                    deflect = p*b*x*(l*l-b*b-x*x)/(6*l)
                if x > a:
                    # print(3, p_elev, def_list[j][1], x, a)
                    deflect = p*a*(l-x)*(2*l*x-x*x-a*a)/(6*l)
                def_list[j][0] += deflect
    for i in range(len(def_list)):
        deflect = def_list[i][0]
        def_list[i][0] = deflect*1728/(modulus*inertia)
    max_def_list = sorted(def_list, key=lambda x: x[0], reverse=True)
    return def_list, round(max_def_list[0][0], 3), round(max_def_list[0][1], 2)


# active = active_pressures(layers, water_elev, total_weights)
# passive = passive_pressures(layers, water_elev, cut_elev, total_weights)
# water = water_pressures(layers, water_elev, cut_elev, total_weights)
# net = net_pressures(active, passive, water, cut_elev)
# min_length = minimum_length(net, brace_elev)
# multi = multiplier(net, brace_elev, min_length)
# moment = maximum_moment(net, min_length[2], brace_elev)
# deflection = deflection_calc(net, brace_elev, min_length)


