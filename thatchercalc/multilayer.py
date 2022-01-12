import math
from sympy import Symbol, solve, re


def two_layer_minimum_length(net_pressures, brace_elevations):
    wall_distances = []
    wall_slopes = []
    strut_distances = []
    strut_slopes = []
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
        wall_distances.append(distance)
        if distance != 0:
            slope = (net_pressures[0][i+1]-net_pressures[0][i])/distance
        else:
            slope = 0
        wall_slopes.append(slope)
    for i in range(len(net_pressures[3])-1):
        distance = -1*(net_pressures[3][i+1]-net_pressures[3][i])
        strut_distances.append(distance)
        if distance != 0:
            slope = (net_pressures[2][i+1]-net_pressures[2][i])/distance
        else:
            slope = 0
        strut_slopes.append(slope)

    waler_load_top = []
    waler_load_bot = []
    # strut diagram sum of forces
    top_force_sum = 0
    bot_force_sum = 0
    t1_half_elevation = (brace_elevations[0] + brace_elevations[1]) / 2
    t2_half_elevation = (brace_elevations[1] + net_pressures[3][-1]) / 2
    for i in range(len(net_pressures[2])-1):
        if net_pressures[3][i] and net_pressures[3][i+1] >= t1_half_elevation:
            top_force_sum += 0.5*(net_pressures[2][i] + net_pressures[2][i+1])*strut_distances[i]
        elif net_pressures[3][i] > t1_half_elevation >= net_pressures[3][i+1]:
            half_distance = net_pressures[3][i] - t1_half_elevation
            t1_half_pressure = net_pressures[2][i] + strut_slopes[i]*half_distance
            top_force_sum += 0.5*(net_pressures[2][i]+t1_half_pressure)*half_distance
            bot_force_sum += 0.5*(net_pressures[2][i+1]+t1_half_pressure)*(net_pressures[3][i]-net_pressures[3][i+1] -
                                                                           half_distance)
        elif net_pressures[3][i] and net_pressures[3][i+1] >= t2_half_elevation:
            bot_force_sum += 0.5*(net_pressures[2][i] + net_pressures[2][i+1])*strut_distances[i]
        elif net_pressures[3][i] > t2_half_elevation >= net_pressures[3][i+1]:
            half_distance = net_pressures[3][i] - t2_half_elevation
            t2_half_pressure = net_pressures[2][i] + strut_slopes[i] * half_distance
            bot_force_sum += 0.5 * (net_pressures[2][i] + t2_half_pressure) * half_distance
    waler_load_top.append(math.ceil(top_force_sum))
    waler_load_bot.append(math.ceil(bot_force_sum))

    # strut diagram sum of moments
    t1_moment = 0
    cut_moment = 0
    for i in range(len(net_pressures[2])-1):
        if net_pressures[3][i+1] >= brace_elevations[1]:
            force = 0.5*(net_pressures[2][i]+net_pressures[2][i+1])*strut_distances[i]
            if 3*(net_pressures[2][i+1]+net_pressures[2][i]) != 0:
                t1_distance = (net_pressures[3][i+1] - brace_elevations[1]) + (net_pressures[3][i]-net_pressures[3][i+1])*(net_pressures[2][i+1]+2*net_pressures[2][i])/(3*(net_pressures[2][i+1]+net_pressures[2][i]))
                cut_distance = (net_pressures[3][i+1] - net_pressures[3][-1]) + (net_pressures[3][i]-net_pressures[3][i+1])*(net_pressures[2][i+1]+2*net_pressures[2][i])/(3*(net_pressures[2][i+1]+net_pressures[2][i]))
            else:
                t1_distance = (net_pressures[3][i + 1] - brace_elevations[1])
                cut_distance = (net_pressures[3][i + 1] - net_pressures[3][-1])
            t1_moment += force*t1_distance
            cut_moment += force*cut_distance
        else:
            force = 0.5 * (net_pressures[2][i] + net_pressures[2][i + 1]) * strut_distances[i]
            cut_distance = (net_pressures[3][i + 1] - net_pressures[3][-1]) + (net_pressures[3][i] - net_pressures[3][i+1]) * (net_pressures[2][i + 1] + 2 * net_pressures[2][i]) / (3 * (net_pressures[2][i + 1] + net_pressures[2][i]))
            cut_moment += force * cut_distance
    t1 = math.ceil(t1_moment/(brace_elevations[0]-brace_elevations[1]))
    t2 = math.ceil((cut_moment-t1*(brace_elevations[0]-net_pressures[3][-1]))/(brace_elevations[1]-net_pressures[3][-1]))
    waler_load_top.append(t1)
    waler_load_bot.append(t2)

    # wall diagram solve for t1
    t1_moment = 0
    for i in range(len(net_pressures[0]) - 1):
        if net_pressures[1][i + 1] >= brace_elevations[1]:
            force = 0.5 * (net_pressures[0][i] + net_pressures[0][i + 1]) * wall_distances[i]
            if 3 * (net_pressures[0][i + 1] + net_pressures[0][i]) != 0:
                t1_distance = (net_pressures[1][i + 1] - brace_elevations[1]) + (net_pressures[1][i] - net_pressures[1][i + 1]) * (net_pressures[0][i + 1] + 2 * net_pressures[0][i]) / (3 * (net_pressures[0][i + 1] + net_pressures[0][i]))
            else:
                t1_distance = (net_pressures[1][i + 1] - brace_elevations[1])
            t1_moment += force * t1_distance
    t1 = math.ceil(t1_moment/(brace_elevations[0]-brace_elevations[1]))
    waler_load_top.append(t1)

    # wall diagram minimum length and t2 solve
    for i in range(len(net_pressures[1])-1):
        compute_string = ""
        text_output_moments = []
        if net_pressures[0][i] >= 0 > net_pressures[0][i+1] or net_pressures[0][i] < 0:
            moment_constant = t1*(brace_elevations[0]-brace_elevations[1])
            for j in range(i):
                force_area = 0.5 * (net_pressures[0][j] + net_pressures[0][j + 1]) * wall_distances[j]
                compute_string += "0.5*(" + str(net_pressures[0][j]) + " + " + str(net_pressures[0][j + 1]) + ")*(" + \
                                  str(round(wall_distances[j], 2)) + ")"
                if (3 * (net_pressures[0][j] + net_pressures[0][j + 1])) != 0:
                    moment_arm = brace_elevations[1] - (((2 * net_pressures[0][j] + net_pressures[0][j + 1]) *
                                                         (wall_distances[j]) /
                                                         (3 * (net_pressures[0][j] + net_pressures[0][j + 1]))) +
                                                        net_pressures[1][j+1])
                    compute_string += "*(" + str(round(moment_arm, 2)) + ")"
                else:
                    moment_arm = brace_elevations[1] - net_pressures[1][j+1]
                    compute_string += "*(" + str(round(moment_arm, 2)) + ")"
                moment_constant = moment_constant + force_area*moment_arm
                text_output_moments.append(compute_string)
                compute_string = ""
            moment_x_constant = net_pressures[0][i] * (brace_elevations[1] - net_pressures[1][i])
            moment_x2_constant = net_pressures[0][i]/2 + wall_slopes[i]*(brace_elevations[1] - net_pressures[1][i])/2
            moment_x3_constant = wall_slopes[i]/3
            text_output_moments.append(str(round(net_pressures[0][i], 2)) +
                                       "*(x)*("+str(round(brace_elevations[1] - net_pressures[1][i], 2))+" + x/2)")
            text_output_moments.append(
                str(round(wall_slopes[i], 2)) + "*(x)*(x/2)*(" + str(round(brace_elevations[1] - net_pressures[1][i], 2)) +
                " + 2x/3)")

            x = Symbol('x')
            solutions = solve(moment_constant + moment_x_constant*x + moment_x2_constant*x*x + moment_x3_constant*x*x*x,
                              x, complex=False)
            for j in solutions:
                if 0 < re(j) < wall_distances[i]:
                    x_distance = re(j)
                    minimum_length_pressure = net_pressures[0][i]+wall_slopes[i]*x_distance
                    minimum_length_elev = net_pressures[1][i] - re(j)
                    minimum_length = re(j)+(net_pressures[1][0]-net_pressures[1][i])
                    reference_point = net_pressures[1][i]
                    break
            else:
                continue  # executed if the loop ended normally (no break)
            break  # executed if 'continue' was skipped (break)

    t2 = -t1
    for i in range(len(net_pressures[1])-1):
        if net_pressures[1][i] >= minimum_length_elev >= net_pressures[1][i+1]:
            t2 = t2 + 0.5*wall_slopes[i]*x_distance*x_distance + net_pressures[0][i]*x_distance
        elif net_pressures[1][i] >= minimum_length_elev:
            t2 = t2 + 0.5*(net_pressures[0][i]+net_pressures[0][i+1])*wall_distances[i]
    waler_load_bot.append(math.ceil(t2))

    output = "With x=0 @ elev. " + \
             str(reference_point) + "': \n" + str(round(moment_constant, 2)) + " + " + \
             str(round(moment_x_constant, 2)) + '*x + ' + str(round(moment_x2_constant, 2)) + "*x^2 + " + str(
        round(moment_x3_constant, 2)) + \
             '*x^3 = 0.  x = ' + str(round(x_distance, 2)) + "."

    waler_loads = [waler_load_top, waler_load_bot]
    waler_load_output = []
    waler_load_output.append("Summing forces on the strut diagram:")
    waler_load_output.append("T1 = " + str(waler_loads[0][0]) + "#/'")
    waler_load_output.append("T2 = " + str(waler_loads[1][0]) + "#/'")
    waler_load_output.append("Summing moments on the strut diagram:")
    waler_load_output.append("T1 = " + str(waler_loads[0][1]) + "#/'")
    waler_load_output.append("T2 = " + str(waler_loads[1][1]) + "#/'")
    waler_load_output.append("Summing forces and moments on the wall diagram:")
    waler_load_output.append("T1 = " + str(waler_loads[0][2]) + "#/'")
    waler_load_output.append("T2 = " + str(waler_loads[1][2]) + "#/'")
    waler_load_output.append("Max T1 Load = " + str(max(waler_loads[0])) + "#/'")
    waler_load_output.append("Max T2 Load = " + str(max(waler_loads[1])) + "#/'")

    return minimum_length, minimum_length_elev, waler_loads, output, minimum_length_pressure, \
           text_output_moments, reference_point, waler_load_output


def two_layer_maximum_moment(net_pressures, waler_load, brace_elev):
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
    waler_load_top = waler_load[0][2]
    waler_load_bot = waler_load[1][2]
    shear = waler_load_top + waler_load_bot

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

    moment = waler_load_top*(brace_elev[0]-zero_shear_point) + waler_load_bot*(brace_elev[1]-zero_shear_point)
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


def two_layer_multiplier(net_pressures, brace_elev, minimum_length_data, supplied_length):
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
            if net_pressures[1][j] <= brace_elev:
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


def two_layer_deflection_calc(net_pressures, brace_elev, minimum_length_data, sheet_type):
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
        if p_elev < brace_elev:
            for j in range(len(def_list)):
                a = p_elev - net_pressures[1][-1]
                b = l-a
                x = def_list[j][1] - net_pressures[1][-1]
                if x <= a:
                    # print(2, p_elev, def_list[j][1], x, a)
                    deflect = p*b*x*(l*l-b*b-x*x)/(6*l)
                if x > a:
                    deflect = p*a*(l-x)*(2*l*x-x*x-a*a)/(6*l)
                def_list[j][0] += deflect
    for i in range(len(def_list)):
        deflect = def_list[i][0]
        def_list[i][0] = deflect*1728/(modulus*inertia)
    max_def_list = sorted(def_list, key=lambda x: x[0], reverse=True)
    return def_list, round(max_def_list[0][0], 3), round(max_def_list[0][1], 2)


wall_pressures = [0, 0, 432, 603, 603, 9603, 5103, 1361, 572, 1454, 1201, 97, -385, -674, -867, -927, -1004]
wall_elevations = [3, 2.5, 1.5, 1.1, 1.01, 1, -3, -3, -4.2, -4.2, -5, -10, -15, -20, -25, -27, -30]
strut_pressures = [0, 0, 504, 704, 704, 9704, 8504, 1388]
strut_elevations = [3, 2.5, 1.5, 1.1, 1.01, 1, -3, -3]
brace_elevations = [3, 1.5]
#

# x = two_layer_minimum_length([wall_pressures, wall_elevations, strut_pressures, strut_elevations], brace_elevations)
# print(x)
# y = two_layer_maximum_moment([wall_pressures, wall_elevations], x[2], brace_elevations)
# print(y)
# z = two_layer_multiplier([wall_pressures, wall_elevations], -0.5, x, 30)
# print(z)
#
# aa = two_layer_deflection_calc([wall_pressures, wall_elevations], brace_elevations[1], x, [6, "MSZ14-312", 16.7, 160.8])
# print(aa)



