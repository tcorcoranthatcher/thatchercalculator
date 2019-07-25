import math


class Layer:
    def __init__(self, name, type, gamma, qu, ka, kp, phi):
        self.name = name  # String of designation of soil (fill, soft clay, dense sand, etc)
        self.type = type  # 0 for granular, 1 for cohesive
        self.gamma = gamma  # Unit weight of soil in units pounds per cubic foot.
        self.sub = gamma - 62.4  # Submerged unit weight
        self.qu = qu  # Unconfined compressive strength in units of tons per square foot.
        self.ka = ka  # Active lateral earth pressure coefficient (determined outside of program)
        self.kp = kp  # Passive lateral earth pressure coefficient (determined outside of program)
        self.phi = phi  # Friction angle


def active_pressures(layers, water_elev, total_weights):
    active_pressures = []
    for i in range(len(layers)):
        vert_pressure = layers[i][2] + layers[i][3]
        for k in range(i + 1):
            if k != 0:
                if layers[k - 1][0] != layers[k][0]:
                    if layers[k][0] < water_elev:
                        if i <= total_weights:
                            vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].sub
                        else:
                            vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].gamma
                    else:
                        vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].gamma
        if layers[i][1].type == 0:
            active_pressure = math.ceil(vert_pressure * layers[i][1].ka) + layers[i][4]
        if layers[i][1].type == 1:
            active_pressure = math.ceil(vert_pressure - layers[i][1].qu * 2000) + layers[i][4]
        ka_min = 0.25
        if layers[i][1].type == 1 and layers[i][1].ka != 1:
            ka_min = layers[i][1].ka
        if layers[i][1].type == 1 and active_pressure <= vert_pressure * ka_min:
            active_pressure = math.ceil(vert_pressure * ka_min) + layers[i][4]
        active_pressures.insert(i, (layers[i][0], active_pressure))

    return active_pressures


def passive_pressures(layers, water_elev, cut_elev, total_weights):
    passive_pressures = []
    for i in range(len(layers)):
        vert_pressure = 0
        for k in range(i + 1):
            if k != 0 and layers[k][0] < cut_elev:
                if layers[k - 1][0] != layers[k][0]:
                    if layers[k][0] < layers[i][5]:
                        if layers[k][0] < water_elev:
                            if i <= total_weights:
                                if layers[k - 1][0] > layers[i][5] > layers[k][0]:
                                    vert_pressure = vert_pressure + (layers[i][5] - layers[k][0]) * (
                                                layers[k][1].sub - layers[k][-1])
                                else:
                                    vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * (
                                                layers[k][1].sub - layers[k][-1])
                            else:
                                if layers[k - 1][0] > layers[i][5] > layers[k][0]:
                                    vert_pressure = vert_pressure + (layers[i][5] - layers[k][0]) * (
                                                layers[k][1].gamma - layers[k][-1])
                                else:
                                    vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * (
                                                layers[k][1].gamma - layers[k][-1])
                        else:
                            if layers[k - 1][0] > layers[i][5] > layers[k][0]:
                                vert_pressure = vert_pressure + (layers[i][5] - layers[k][0]) * (
                                            layers[k][1].gamma - layers[k][-1])
                            else:
                                vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * (
                                            layers[k][1].gamma - layers[k][-1])
        passive_pressure = 0
        if layers[i][0] <= cut_elev:
            passive_pressure = math.floor(vert_pressure * layers[i][1].kp + layers[i][1].qu * 2000)
        passive_pressures.insert(i, (layers[i][0], passive_pressure))
    return passive_pressures
    # passive_pressures = []
    # for i in range(len(layers)):
    #     vert_pressure = 0
    #     for k in range(i + 1):
    #         if k != 0 and layers[k][0] < cut_elev:
    #             if layers[k - 1][0] != layers[k][0]:
    #                 if layers[k][0] < water_elev:
    #                     if i <= total_weights:
    #                         vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * (
    #                         layers[k][1].sub - layers[k][-1])
    #                     else:
    #                         vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * (
    #                         layers[k][1].gamma - layers[k][-1])
    #                 else:
    #                     vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * (
    #                     layers[k][1].gamma - layers[k][-1])
    #     passive_pressure = 0
    #     if layers[i][0] <= cut_elev:
    #         passive_pressure = math.floor(vert_pressure * layers[i][1].kp + layers[i][1].qu * 2000)
    #     passive_pressures.insert(i, (layers[i][0], passive_pressure))
    # return passive_pressures


def active_pressures_front(layers, water_elev, cut_elev, total_weights):
    active_pressures_front = []
    for i in range(len(layers)):
        vert_pressure = 0
        for k in range(i + 1):
            if k != 0 and layers[k][0] < cut_elev:
                if layers[k - 1][0] != layers[k][0]:
                    if layers[k][0] < water_elev:
                        if i <= total_weights:
                            vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].sub
                        else:
                            vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].gamma
                    else:
                        vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].gamma
        active_pressure = 0
        ka_min = 0.25
        if layers[i][1].type == 1 and layers[i][1].ka != 1:
            ka_min = layers[i][1].ka
        if layers[i][0] <= cut_elev:
            if layers[i][1].type == 0:
                active_pressure = math.ceil(vert_pressure * layers[i][1].ka)
            if layers[i][1].type == 1:
                active_pressure = math.ceil(vert_pressure - layers[i][1].qu * 2000)
        if layers[i][1].type == 1 and active_pressure <= vert_pressure * ka_min:
            active_pressure = math.ceil(vert_pressure * ka_min)
        active_pressures_front.insert(i, (layers[i][0], active_pressure))
    return active_pressures_front


def passive_pressures_back(layers, water_elev, cut_elev, surface_elev, total_weights):
    passive_pressures_back = []
    temp = layers[0][0]
    layers[0][0] = surface_elev
    for i in range(len(layers)):
        vert_pressure = 0
        for k in range(i + 1):
            if k != 0:
                if layers[k - 1][0] != layers[k][0]:
                    if layers[k][0] < water_elev:
                        if i <= total_weights:
                            vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].sub
                        else:
                            vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].gamma
                    else:
                        vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].gamma
        if layers[i][0] > cut_elev:
            passive_pressure = 0
        else:
            passive_pressure = math.floor(vert_pressure * layers[i][1].kp + layers[i][1].qu * 2000)
        passive_pressures_back.insert(i, (layers[i][0], passive_pressure))
    layers[0][0] = temp
    return passive_pressures_back


def net_pressures(active_pressures, passive_pressures, water_pressures, cut_elev, ers_type, beam_spacing, zero_length,
                  beam_type, soldier_beam_method):
    net_pressures = []
    heights = []
    text_output = []
    if len(active_pressures) != len(passive_pressures):
        return ("error")
    else:
        for i in range(len(active_pressures)):
            net_pressure = active_pressures[i][1] + water_pressures[i][1] - passive_pressures[i][1]
            text_output.append("Pnet @ " + str(active_pressures[i][0]) + "' (Pa+Pw-Pp) = " + str(active_pressures[i][1])
                               + "psf + " + str(water_pressures[i][1]) + "psf - " + str(passive_pressures[i][1]) +
                               "psf = " + str(net_pressure) + " psf")
            if active_pressures[i][0] == cut_elev:
                net_pressures.append(active_pressures[i][1] + water_pressures[i][1])
                heights.append(active_pressures[i][0])
                text_output.insert(len(text_output) - 1,
                                   ("Pnet @ " + str(active_pressures[i][0]) + "' (Pa+Pw-Pp) = " + str(
                                       active_pressures[i][1]) + "psf + " + str(
                                       water_pressures[i][1]) + "psf - 0psf = " +
                                    str(active_pressures[i][1] + water_pressures[i][1]) + " psf"))
            net_pressures.append(net_pressure)
            heights.append(active_pressures[i][0])

    if ers_type == 1 and soldier_beam_method == 0:
        for i in range(len(heights)):
            if heights[i] > cut_elev:
                net_pressures[i] = round(net_pressures[i] * beam_spacing, 0)
            if heights[i] == cut_elev and heights[i + 1] == heights[i]:
                if net_pressures[i] >= 0:
                    net_pressures[i] = net_pressures[i] * beam_spacing
                else:
                    net_pressures[i] = 0
            if heights[i] == cut_elev and heights[i + 1] != heights[i]:
                if net_pressures[i] >= 0:
                    net_pressures[i] = net_pressures[i] * beam_type[4]
                else:
                    net_pressures[i] = 0
            if cut_elev > heights[i] > cut_elev - zero_length + 0.01:
                if net_pressures[i] <= 0:
                    net_pressures[i] = 0
            if cut_elev - zero_length + 0.01 >= heights[i] >= cut_elev - zero_length - 0.01 and heights[i + 1] == \
                    heights[i]:
                if net_pressures[i] >= 0:
                    pass
                else:
                    net_pressures[i] = 0
            if cut_elev - zero_length + 0.01 >= heights[i] >= cut_elev - zero_length - 0.01 and heights[i + 1] != \
                    heights[i]:
                if net_pressures[i] >= 0:
                    net_pressures[i] = round(net_pressures[i] * beam_spacing, 0)
                else:
                    net_pressures[i] = round(3 * beam_type[4] * net_pressures[i], 0)
            if heights[i] < (cut_elev - zero_length - 0.01):
                if net_pressures[i] >= 0:
                    net_pressures[i] = round(net_pressures[i] * beam_spacing, 0)
                else:
                    net_pressures[i] = round(3 * beam_type[4] * net_pressures[i], 0)

    if ers_type == 1 and soldier_beam_method == 1:
        for i in range(len(heights)):
            if heights[i] > cut_elev:
                # NO CHANGE
                net_pressures[i] = round(net_pressures[i] * beam_spacing, 0)
            if heights[i] == cut_elev and heights[i + 1] == heights[i]:
                # NO CHANGE
                if net_pressures[i] >= 0:
                    net_pressures[i] = net_pressures[i] * beam_spacing
                else:
                    net_pressures[i] = 0
            if heights[i] == cut_elev and heights[i + 1] != heights[i]:
                # NO CHANGE
                if net_pressures[i] >= 0:
                    net_pressures[i] = net_pressures[i] * beam_type[4]
                else:
                    net_pressures[i] = 0
            if cut_elev > heights[i] > cut_elev - zero_length + 0.01:
                # NO CHANGE
                if net_pressures[i] <= 0:
                    net_pressures[i] = 0
            if cut_elev - zero_length + 0.01 >= heights[i] >= cut_elev - zero_length - 0.01 and heights[i + 1] == \
                    heights[i]:
                # NO CHANGE
                if net_pressures[i] >= 0:
                    pass
                else:
                    net_pressures[i] = 0
            if cut_elev - zero_length + 0.01 >= heights[i] >= cut_elev - zero_length - 0.01 and heights[i + 1] != \
                    heights[i]:
                # net_pressures[i] = round(3 * beam_type[4] * net_pressures[i], 0)
                net_pressure = beam_type[4] * (active_pressures[i - 1][1] + water_pressures[i - 1][1]) - 3 * beam_type[
                    4] * passive_pressures[i - 1][1]
                passive_limit = (active_pressures[i - 1][1] + water_pressures[i - 1][1] - passive_pressures[i - 1][
                    1]) * beam_spacing
                if net_pressure >= passive_limit:
                    net_pressures[i] = round(net_pressure, 0)
                else:
                    net_pressures[i] = round(passive_limit, 0)

            if heights[i] < (cut_elev - zero_length - 0.01):
                # net_pressures[i] = round(3 * beam_type[4] * net_pressures[i], 0)
                net_pressure = beam_type[4] * (active_pressures[i - 1][1] + water_pressures[i - 1][1]) - 3 * beam_type[
                    4] * passive_pressures[i - 1][1]
                passive_limit = (active_pressures[i - 1][1] + water_pressures[i - 1][1] - passive_pressures[i - 1][
                    1]) * beam_spacing
                if net_pressure >= passive_limit:
                    net_pressures[i] = round(net_pressure, 0)
                else:
                    net_pressures[i] = round(passive_limit, 0)

    return net_pressures, heights, text_output


def cant_pressures(active_pressures, passive_pressures, water_pressures,
                   cut_elev, ers_type, beam_spacing, zero_length, beam_type, soldier_beam_method):
    net_pressures = []
    heights = []
    text_output = []
    if len(active_pressures) != len(passive_pressures):
        return ("error")
    else:
        for i in range(len(active_pressures)):
            net_pressure = active_pressures[i][1] - water_pressures[i][1] - passive_pressures[i][1]
            net_pressures.append(net_pressure)
            heights.append(active_pressures[i][0])
            text_output.append(
                "Pnet @ " + str(active_pressures[i][0]) + "' (PpBS+Pw-PaFS) = " + str(passive_pressures[i][1])
                + "psf + " + str(water_pressures[i][1]) + "psf - " + str(active_pressures[i][1]) +
                "psf = " + str(-1 * net_pressure) + " psf")
    if ers_type == 1 and soldier_beam_method == 0:
        for i in range(len(heights)):
            if heights[i] > cut_elev:
                net_pressures[i] = net_pressures[i] * beam_spacing
            if heights[i] == cut_elev and heights[i + 1] == heights[i]:
                if net_pressures[i] >= 0:
                    net_pressures[i] = net_pressures[i] * beam_spacing
                else:
                    net_pressures[i] = 0
            if heights[i] == cut_elev and heights[i + 1] != heights[i]:
                if net_pressures[i] >= 0:
                    net_pressures[i] = net_pressures[i] * beam_type[4]
                else:
                    net_pressures[i] = 0
            if cut_elev > heights[i] > cut_elev - zero_length + 0.01:
                if net_pressures[i] <= 0:
                    net_pressures[i] = 0
            if cut_elev - zero_length + 0.01 >= heights[i] >= cut_elev - zero_length - 0.01 and heights[i + 1] == \
                    heights[i]:
                temp = net_pressures[i]
                if net_pressures[i] >= 0:
                    net_pressures[i] = temp
                else:
                    net_pressures[i] = 0
            if cut_elev - zero_length + 0.01 >= heights[i] >= cut_elev - zero_length - 0.01 and heights[i + 1] != \
                    heights[i]:
                if net_pressures[i] >= 0:
                    net_pressures[i] = round(net_pressures[i] * beam_spacing, 0)
                else:
                    net_pressures[i] = round(3 * beam_type[4] * net_pressures[i], 0)
            if heights[i] < (cut_elev - zero_length - 0.01):
                if net_pressures[i] >= 0:
                    net_pressures[i] = round(net_pressures[i] * beam_spacing, 0)
                else:
                    net_pressures[i] = round(3 * beam_type[4] * net_pressures[i], 0)
        for i in range(len(heights)):
            if heights[i] == cut_elev - zero_length:
                heights.insert(i + 1, heights[i])
                net_pressures.insert(i + 1, 3 * beam_type[4] * net_pressures[i])
                break
        for i in range(len(heights)):
            if heights[i] == cut_elev - zero_length:
                heights.insert(i + 1, heights[i])
                net_pressures.insert(i + 1, 3 * beam_type[4] * net_pressures[i])
                break
    if ers_type == 1 and soldier_beam_method == 1:
        for i in range(len(heights)):
            if heights[i] > cut_elev:
                net_pressures[i] = net_pressures[i] * beam_spacing
            if heights[i] == cut_elev and heights[i + 1] == heights[i]:
                if net_pressures[i] >= 0:
                    net_pressures[i] = net_pressures[i] * beam_spacing
                else:
                    net_pressures[i] = 0
            if heights[i] == cut_elev and heights[i + 1] != heights[i]:
                if net_pressures[i] >= 0:
                    net_pressures[i] = net_pressures[i] * beam_type[4]
                else:
                    net_pressures[i] = 0
            if cut_elev > heights[i] > cut_elev - zero_length + 0.01:
                if net_pressures[i] <= 0:
                    net_pressures[i] = 0
            if cut_elev - zero_length + 0.01 >= heights[i] >= cut_elev - zero_length - 0.01 and heights[i + 1] == \
                    heights[i]:
                temp = net_pressures[i]
                if net_pressures[i] >= 0:
                    net_pressures[i] = temp
                else:
                    net_pressures[i] = 0
            if cut_elev - zero_length + 0.01 >= heights[i] >= cut_elev - zero_length - 0.01 and heights[i + 1] != \
                    heights[i]:
                # net_pressures[i] = round(3 * beam_type[4] * net_pressures[i], 0)
                net_pressure = beam_type[4] * (active_pressures[i][1] - water_pressures[i][1]) - 3 * beam_type[
                    4] * passive_pressures[i][1]
                passive_limit = (active_pressures[i][1] - water_pressures[i][1] - passive_pressures[i][
                    1]) * beam_spacing
                if net_pressure >= passive_limit:
                    net_pressures[i] = round(net_pressure, 0)
                else:
                    net_pressures[i] = round(passive_limit, 0)
            if heights[i] < (cut_elev - zero_length - 0.01):
                # net_pressures[i] = round(3 * beam_type[4] * net_pressures[i], 0)
                net_pressure = beam_type[4] * (active_pressures[i][1] - water_pressures[i][1]) - 3 * beam_type[
                    4] * passive_pressures[i][1]
                passive_limit = (active_pressures[i][1] - water_pressures[i][1] - passive_pressures[i][
                    1]) * beam_spacing
                if net_pressure >= passive_limit:
                    net_pressures[i] = round(net_pressure, 0)
                else:
                    net_pressures[i] = round(passive_limit, 0)
        for i in range(len(heights)):
            if heights[i] == cut_elev - zero_length:
                heights.insert(i + 1, heights[i])
                net_pressures.insert(i + 1, 3 * beam_type[4] * net_pressures[i])
                break
        for i in range(len(heights)):
            if heights[i] == cut_elev - zero_length:
                heights.insert(i + 1, heights[i])
                net_pressures.insert(i + 1, 3 * beam_type[4] * net_pressures[i])
                break

    new_nets = []
    new_heights = []
    for i in range(len(net_pressures)):
        if net_pressures[i] != 0:
            new_nets.append(-1 * net_pressures[i])
            new_heights.append(heights[i])

    return new_nets, new_heights, text_output


def water_pressures(layers, water_elev, cut_elev, total_weights, supplied_elev):
    water_pressures = []
    for i in range(len(layers)):
        if i <= total_weights:
            if layers[i][0] >= water_elev:
                water_pressure = 0
            elif water_elev >= layers[i][0] >= cut_elev:
                water_pressure = math.ceil((water_elev - layers[i][0]) * 62.4)
            elif water_elev >= cut_elev >= layers[i][0]:
                water_pressure = math.ceil((water_elev - cut_elev) * 62.4)
            else:
                water_pressure = 0
        else:
            water_pressure = 0
        water_pressures.append([layers[i][0], water_pressure])

    check = 0
    for i in range(len(layers)):
        if layers[i][-1] != 0:
            check = 1
            break

    if check == 1:
        max_water_pressure = (water_elev - cut_elev) * 62.4
        for i in range(len(water_pressures)):
            if cut_elev >= water_pressures[i][0] >= supplied_elev:
                water_pressures[i][1] = math.ceil(max_water_pressure - \
                                                  max_water_pressure * (cut_elev - water_pressures[i][0]) / (
                                                              cut_elev - supplied_elev))
            if supplied_elev > water_pressures[i][0]:
                water_pressures[i][1] = 0

    return water_pressures


def active_pressures_output(layers, water_elev, total_weights):
    active_pressures = []
    output_string = []
    for i in range(len(layers)):
        vert_pressure = layers[i][2] + layers[i][3]
        active_pressure_string = "Pa @ " + str(layers[i][0]) + "' = (" + str(layers[i][3]) + "psf + " + \
                                 str(layers[i][2]) + "psf "
        for k in range(i + 1):
            if k != 0:
                if layers[k - 1][0] != layers[k][0]:
                    if layers[k][0] < water_elev:
                        if i <= total_weights:
                            vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].sub
                            active_pressure_string += " + " + str(layers[k][1].sub) + "pcf*" + str(
                                round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
                        else:
                            vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].gamma
                            active_pressure_string += " + " + str(layers[k][1].gamma) + "pcf*" + str(
                                round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
                    else:
                        vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].gamma
                        active_pressure_string += " + " + str(layers[k][1].gamma) + "pcf*" + str(
                            round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
        if layers[i][1].type == 0:
            active_pressure = math.ceil(vert_pressure * layers[i][1].ka)
        if layers[i][1].type == 1:
            active_pressure = math.ceil(vert_pressure - layers[i][1].qu * 2000)
        ka_min = 0.25
        if layers[i][1].type == 1 and layers[i][1].ka != 1:
            ka_min = layers[i][1].ka
        if layers[i][1].type == 1 and active_pressure <= vert_pressure * ka_min:
            active_pressure = math.ceil(vert_pressure * ka_min)
            active_pressure_string += ")-2*" + str(layers[i][1].qu * 1000) + "psf = (-) => " + str(
                vert_pressure) + "psf*" + str(ka_min)
        elif layers[i][1].type == 1 and not active_pressure <= vert_pressure * ka_min:
            active_pressure_string += ")-2*" + str(layers[i][1].qu * 1000) + "psf"
        else:
            active_pressure_string += ")*" + str(layers[i][1].ka)
        active_pressures.insert(i, (layers[i][0], active_pressure))
        active_pressure_string += " = " + (str(active_pressure)) + " psf"
        output_string.append(active_pressure_string)
    return output_string


def passive_pressures_output(layers, water_elev, cut_elev, total_weights):
    passive_pressures = []
    output_string = []
    for i in range(len(layers)):
        vert_pressure = 0
        passive_pressure_string = "Pp @ " + str(layers[i][0]) + "' = (" + str(0) + "psf"
        for k in range(i + 1):
            if k != 0 and layers[k][0] < cut_elev:
                if layers[k - 1][0] != layers[k][0]:
                    if layers[k][0] < layers[i][5]:
                        if layers[k][0] < water_elev:
                            if i <= total_weights:
                                if layers[k - 1][0] > layers[i][5] > layers[k][0]:
                                    vert_pressure = vert_pressure + (layers[i][5] - layers[k][0]) * (
                                                layers[k][1].sub - layers[k][-1])
                                    passive_pressure_string += " + " + str(
                                        layers[k][1].sub - layers[k][-1]) + "pcf*" + str(
                                        round((layers[i][5] - layers[k][0]), 2)) + "'"
                                else:
                                    vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * (
                                                layers[k][1].sub - layers[k][-1])
                                    passive_pressure_string += " + " + str(
                                        layers[k][1].sub - layers[k][-1]) + "pcf*" + str(
                                        round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
                            else:
                                if layers[k - 1][0] > layers[i][5] > layers[k][0]:
                                    vert_pressure = vert_pressure + (layers[i][5] - layers[k][0]) * (
                                                layers[k][1].gamma - layers[k][-1])
                                    passive_pressure_string += " + " + str(
                                        layers[k][1].gamma - layers[k][-1]) + "pcf*" + str(
                                        round((layers[i][5] - layers[k][0]), 2)) + "'"
                                else:
                                    vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * (
                                                layers[k][1].gamma - layers[k][-1])
                                    passive_pressure_string += " + " + str(
                                        layers[k][1].gamma - layers[k][-1]) + "pcf*" + str(
                                        round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
                        else:
                            if layers[k - 1][0] > layers[i][5] > layers[k][0]:
                                vert_pressure = vert_pressure + (layers[i][5] - layers[k][0]) * (
                                            layers[k][1].gamma - layers[k][-1])
                                passive_pressure_string += " + " + str(
                                    layers[k][1].gamma - layers[k][-1]) + "pcf*" + str(
                                    round((layers[i][5] - layers[k][0]), 2)) + "'"
                            else:
                                vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * (
                                            layers[k][1].gamma - layers[k][-1])
                                passive_pressure_string += " + " + str(
                                    layers[k][1].gamma - layers[k][-1]) + "pcf*" + str(
                                    round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
        passive_pressure = 0
        if layers[i][0] <= cut_elev:
            passive_pressure = math.floor(vert_pressure * layers[i][1].kp + layers[i][1].qu * 2000)
        if layers[i][1].type == 1:
            passive_pressure_string += ")+2*" + str(layers[i][1].qu * 1000) + "psf"
        else:
            passive_pressure_string += ")*" + str(layers[i][1].kp)
        passive_pressures.insert(i, (layers[i][0], passive_pressure))
        passive_pressure_string += " = " + (str(passive_pressure)) + " psf"
        if layers[i][0] <= cut_elev:
            output_string.append(passive_pressure_string)
    return output_string
    # passive_pressures = []
    # output_string = []
    # for i in range(len(layers)):
    #     vert_pressure = 0
    #     passive_pressure_string = "Pp @ " + str(layers[i][0]) + "' = (" + str(0) + "psf"
    #     for k in range(i + 1):
    #         if k != 0 and layers[k][0] < cut_elev:
    #             if layers[k - 1][0] != layers[k][0]:
    #                 if layers[k][0] < water_elev:
    #                     if i <= total_weights:
    #                         vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * (
    #                         layers[k][1].sub - layers[k][-1])
    #                         passive_pressure_string += " + " + str(layers[k][1].sub - layers[k][-1]) + "pcf*" + str(
    #                             round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
    #                     else:
    #                         vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * (
    #                         layers[k][1].gamma - layers[k][-1])
    #                         passive_pressure_string += " + " + str(layers[k][1].gamma - layers[k][-1]) + "pcf*" + str(
    #                             round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
    #                 else:
    #                     vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * (
    #                     layers[k][1].gamma - layers[k][-1])
    #                     passive_pressure_string += " + " + str(layers[k][1].gamma - layers[k][-1]) + "pcf*" + str(
    #                         round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
    #     passive_pressure = 0
    #     if layers[i][0] <= cut_elev:
    #         passive_pressure = math.floor(vert_pressure * layers[i][1].kp + layers[i][1].qu * 2000)
    #     if layers[i][1].type == 1:
    #         passive_pressure_string += ")+2*" + str(layers[i][1].qu * 1000) + "psf"
    #     else:
    #         passive_pressure_string += ")*" + str(layers[i][1].kp)
    #     passive_pressures.insert(i, (layers[i][0], passive_pressure))
    #     passive_pressure_string += " = " + (str(passive_pressure)) + " psf"
    #     if layers[i][0] <= cut_elev:
    #         output_string.append(passive_pressure_string)
    # return output_string


def water_pressures_output(water_pressures):
    output_string = []
    for i in range(len(water_pressures)):
        output_string.append(
            'Pw @ ' + str(water_pressures[i][0]) + "' = " + str(math.ceil(water_pressures[i][1])) + " psf")

    # water_pressures = []
    # output_string = []
    # for i in range(len(layers)):
    #     water_pressure_string = 'Pw @ ' + str(layers[i][0]) + "' = "
    #     if i <= total_weights:
    #         if layers[i][0] >= water_elev:
    #             water_pressure = 0
    #         elif water_elev >= layers[i][0] >= cut_elev:
    #             water_pressure = math.ceil((water_elev - layers[i][0]) * 62.4)
    #             water_pressure_string += "62.4pcf*" + str((water_elev - layers[i][0]))\
    #                                      + "' = " + str(water_pressure) + " psf"
    #         elif water_elev >= cut_elev >= layers[i][0]:
    #             water_pressure = math.ceil((water_elev - cut_elev) * 62.4)
    #             water_pressure_string += "62.4pcf*" + str((water_elev - cut_elev))\
    #                                      + "' = " + str(water_pressure) + " psf"
    #         else:
    #             water_pressure = 0
    #     else:
    #         water_pressure = 0
    #         water_pressure_string += "0 psf"
    #     water_pressures.append((layers[i][0], water_pressure))
    #     if water_pressure_string != 'Pw @ ' + str(layers[i][0]) + "' = ":
    #         output_string.append(water_pressure_string)
    return output_string


def active_pressures_front_output(layers, water_elev, cut_elev, total_weights):
    active_pressures_front = []
    output_string = []
    for i in range(len(layers)):
        vert_pressure = 0
        active_pressure_string = "PaFS @ " + str(layers[i][0]) + "' = ("
        for k in range(i + 1):
            if k != 0 and layers[k][0] < cut_elev:
                if layers[k - 1][0] != layers[k][0]:
                    if layers[k][0] < water_elev:
                        if i <= total_weights:
                            vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].sub
                            active_pressure_string += str(layers[k][1].sub) + "pcf*" + str(
                                round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
                        else:
                            vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].gamma
                            active_pressure_string += str(layers[k][1].gamma) + "pcf*" + str(
                                round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
                    else:
                        vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].gamma
                        active_pressure_string += str(layers[k][1].gamma) + "pcf*" + str(
                            round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
                    active_pressure_string += " + "
        active_pressure = 0
        ka_min = 0.25
        if layers[i][1].type == 1 and layers[i][1].ka != 1:
            ka_min = layers[i][1].ka
        active_pressure_string += " 0psf "
        if layers[i][0] <= cut_elev:
            if layers[i][1].type == 0:
                active_pressure = math.ceil(vert_pressure * layers[i][1].ka)
            if layers[i][1].type == 1:
                active_pressure = math.ceil(vert_pressure - layers[i][1].qu * 2000)
        if layers[i][1].type == 1 and active_pressure <= vert_pressure * ka_min:
            active_pressure = math.ceil(vert_pressure * ka_min)
            active_pressure_string += ")-2*" + str(layers[i][1].qu * 1000) + "psf = (-) => " + str(
                vert_pressure) + "psf*" + str(ka_min)
        elif layers[i][1].type == 1 and not active_pressure <= vert_pressure * ka_min:
            active_pressure_string += ")-2*" + str(layers[i][1].qu * 1000) + "psf"
        else:
            active_pressure_string += ")*" + str(layers[i][1].ka)
        active_pressures_front.insert(i, (layers[i][0], active_pressure))
        active_pressure_string += " = " + (str(active_pressure)) + " psf"
        if layers[i][0] <= cut_elev:
            output_string.append(active_pressure_string)
    return output_string


def passive_pressures_back_output(layers, water_elev, cut_elev, surface_elev, total_weights):
    passive_pressures_back = []
    output_string = []
    temp = layers[0][0]
    layers[0][0] = surface_elev
    for i in range(len(layers)):
        vert_pressure = 0
        passive_pressure_string = "PpBS @ " + str(layers[i][0]) + "' = ("
        for k in range(i + 1):
            if k != 0:
                if layers[k - 1][0] != layers[k][0]:
                    if layers[k][0] < water_elev:
                        if i <= total_weights:
                            vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].sub
                            passive_pressure_string += str(layers[k][1].sub) + "pcf*" + str(
                                round((layers[k - 1][0] - layers[k][0]), 2)) + "' + "
                        else:
                            vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].gamma
                            passive_pressure_string += str(layers[k][1].gamma) + "pcf*" + str(
                                round((layers[k - 1][0] - layers[k][0]), 2)) + "' + "
                    else:
                        vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].gamma
                        passive_pressure_string += str(layers[k][1].gamma) + "pcf*" + str(
                            round((layers[k - 1][0] - layers[k][0]), 2)) + "' + "
        passive_pressure = math.floor(vert_pressure * layers[i][1].kp + layers[i][1].qu * 2000)
        passive_pressure_string += " 0psf "
        if layers[i][1].type == 1:
            passive_pressure_string += ")+2*" + str(layers[i][1].qu * 1000) + "psf"
        else:
            passive_pressure_string += ")*" + str(layers[i][1].kp)
        passive_pressures_back.insert(i, (layers[i][0], passive_pressure))
        passive_pressure_string += " = " + (str(passive_pressure)) + " psf"
        if layers[i][0] <= cut_elev:
            output_string.append(passive_pressure_string)

    return output_string


def water_around_toe(layers, water_elev, cut_elev, supplied_elev):
    check = 0
    text_output = []
    for i in range(len(layers)):
        layers[i].append(0)

    if water_elev > cut_elev:
        check = 1
        text_output = [("No water seal, reduce passive soil unit weight for work points"),
                       ("between cut and toe to account for water flowing around toe"),
                       ("Hu = " + str(water_elev) + "' - " + str(cut_elev) + "' = " + str(
                           water_elev - cut_elev) + "'."),
                       ("D = " + str(cut_elev) + "' - " + str(supplied_elev) + "' = " + str(cut_elev - supplied_elev) +
                        "'."),
                       (chr(916)) + chr(947) + "' = 20 * Hu/D = 20 * " + str(water_elev - cut_elev) + "/" +
                       str(cut_elev - supplied_elev) + " = " + (
                           str(20 * (water_elev - cut_elev) / (cut_elev - supplied_elev))
                           )
                       ]
        for i in range(len(layers)):
            if cut_elev >= layers[i][0] >= supplied_elev and layers[i][1].type == 1:
                check = 0
                text_output = []
                break

    if check == 1:
        h = water_elev - cut_elev
        d = cut_elev - supplied_elev
        delta = 20 * h / d
        for i in range(len(layers)):
            if cut_elev >= layers[i][0] >= supplied_elev:
                layers[i][-1] = delta

    return layers, text_output


def net_pressure_output(active_pressures, passive_pressures, water_pressures, net_pressures):
    output = []
    # for i in range(len(net_pressures[1])-1):
    #     output_string = "Pnet @ " + str(net_pressures[1][i]) + "' (Pa+Pw-Pp) = " + str(active_pressures[i][1]) + \
    #                     "psf + " + str(water_pressures[i][1]) + "psf - " + str(passive_pressures[i][1]) + "psf = " + \
    #                     str(net_pressures[0][i]) + " psf"
    #     output.append(output_string)

    return output


def cant_pressure_output(active_pressures, passive_pressures, water_pressures, cant_pressures):
    output = []
    for i in range(len(cant_pressures[1])):
        output_string = "Pnet @ " + str(cant_pressures[1][i]) + "' (PpBS-PaFS-Pw) = " + str(passive_pressures[i][1]) + \
                        "psf - " + str(active_pressures[i][1]) + "psf - " + str(water_pressures[i][1]) + "psf = " + \
                        str(cant_pressures[0][i]) + " psf"
        output.append(output_string)

    return output


def apparent_pressures(active_pressures, passive_pressures, water_pressures, cut_elev, diagram_type, backside_x,
                       backside_y, layers, water_elev, total_weights, ers_type, beam_spacing, zero_length,
                       beam_type, soldier_beam_method):
    text_output = []
    if diagram_type == 1:
        text_output.append("Using soft clay apparent pressure diagram:")
        text_output.append("")
    if diagram_type == 2:
        text_output.append("Using stiff clay apparent pressure diagram:")
        text_output.append("")
    if diagram_type == 3:
        text_output.append("Using sand apparent pressure diagram:")
        text_output.append("")
    # diagram type: 1 for soft clay, 2 for stiff clay, 3 for sand
    # begin setting up apparent pressure diagram by taking elevations from active pressure calcs
    apparent_pressure_elevations = []
    apparent_pressure_wall_pressures = []
    apparent_pressure_strut_pressures = []
    for i in range(len(active_pressures)):
        apparent_pressure_elevations.append(active_pressures[i][0])

    # determine total active force
    total_active = 0
    for i in range(len(active_pressures) - 1):
        if active_pressures[i][0] > cut_elev:
            total_active += 0.5 * (active_pressures[i][1] + active_pressures[i+1][1]) * \
                            (active_pressures[i][0] - active_pressures[i+1][0])
    total_active = math.ceil(total_active)
    text_output.append("Total active from elevation " + str(active_pressures[0][0]) + "' to elevation " + str(cut_elev)
                       + "' = " + str(total_active) + "#/'")
    # determine apparent pressure diagrams for walls and struts ABOVE THE CUT
    H = active_pressures[0][0] - cut_elev
    text_output.append("H = " + str(active_pressures[0][0]) + "' - " + str(cut_elev) + "' = " + str(H) + "'")
    if diagram_type == 1:
        # ordinate calcs/checks go here
        strut_ordinate = math.ceil(1.4 * total_active / (round(0.25 * H / 2, 2) + round(0.75 * H, 2)))
        wall_ordinate = math.ceil(1.2 * total_active / (round(0.25 * H / 2, 2) + round(0.75 * H, 2)))
        text_output.append(
            'Pbs = 1.4*' + str(total_active) + "#/' / (0.875*" + str(H) + "') = " + str(strut_ordinate) + " psf")
        text_output.append(
            'Pbw = 1.2*' + str(total_active) + "#/' / (0.875*" + str(H) + "') = " + str(wall_ordinate) + " psf")
        for i in range(len(apparent_pressure_elevations)):
            if apparent_pressure_elevations[i] >= round(apparent_pressure_elevations[0] - 0.25 * H, 1):
                apparent_pressure_wall_pressures.append(math.ceil(
                    wall_ordinate * (apparent_pressure_elevations[0] - apparent_pressure_elevations[i]) / (round(0.25 * H, 1))))
                apparent_pressure_strut_pressures.append(math.ceil(
                    strut_ordinate * (apparent_pressure_elevations[0] - apparent_pressure_elevations[i]) / (round(0.25 * H, 1))))
            if round(apparent_pressure_elevations[0] - 0.25 * H, 1) > apparent_pressure_elevations[i] >= cut_elev:
                apparent_pressure_wall_pressures.append(wall_ordinate)
                apparent_pressure_strut_pressures.append(strut_ordinate)
    if diagram_type == 2:
        # ordinate calcs/checks go here
        strut_ordinate = math.ceil(1.4 * total_active / (round(0.75 * H, 2)))
        wall_ordinate = math.ceil(1.2 * total_active / (round(0.75 * H, 2)))
        text_output.append(
            'Pbs = 1.4*' + str(total_active) + "#/' / (0.75*" + str(H) + "') = " + str(strut_ordinate) + " psf")
        text_output.append(
            'Pbw = 1.2*' + str(total_active) + "#/' / (0.75*" + str(H) + "') = " + str(wall_ordinate) + " psf")
        for i in range(len(apparent_pressure_elevations)):
            if apparent_pressure_elevations[i] >= round(apparent_pressure_elevations[0] - 0.25 * H, 1):
                apparent_pressure_wall_pressures.append(math.ceil(
                    wall_ordinate * (apparent_pressure_elevations[0] - apparent_pressure_elevations[i]) / (round(0.25 * H, 1))))
                apparent_pressure_strut_pressures.append(math.ceil(
                    strut_ordinate * (apparent_pressure_elevations[0] - apparent_pressure_elevations[i]) / (round(0.25 * H, 1))))
            if round(apparent_pressure_elevations[0] - 0.25 * H, 1) > apparent_pressure_elevations[i] >= \
                    round(apparent_pressure_elevations[0] - 0.75 * H, 1):
                apparent_pressure_wall_pressures.append(wall_ordinate)
                apparent_pressure_strut_pressures.append(strut_ordinate)
            if round(apparent_pressure_elevations[0] - 0.25 * H, 1) > apparent_pressure_elevations[i] >= cut_elev:
                apparent_pressure_wall_pressures.append(math.ceil(wall_ordinate - wall_ordinate * (
                            (apparent_pressure_elevations[0] - 0.75 * H) - apparent_pressure_elevations[i]) / (
                                                                              0.25 * H)))
                apparent_pressure_strut_pressures.append(math.ceil(strut_ordinate - strut_ordinate * (
                            (apparent_pressure_elevations[0] - 0.75 * H) - apparent_pressure_elevations[i]) / (
                                                                               0.25 * H)))
    if diagram_type == 3:
        # ordinate calcs/checks go here
        strut_ordinate = math.ceil(1.4 * total_active / (round(H, 2)))
        wall_ordinate = math.ceil(1.2 * total_active / (round(H, 2)))
        text_output.append(
            'Pbs = 1.4*' + str(total_active) + "#/' / (" + str(H) + "') = " + str(strut_ordinate) + " psf")
        text_output.append(
            'Pbw = 1.2*' + str(total_active) + "#/' / (" + str(H) + "') = " + str(wall_ordinate) + " psf")

        for i in range(len(apparent_pressure_elevations)):
            apparent_pressure_wall_pressures.append(math.ceil(wall_ordinate))
            apparent_pressure_strut_pressures.append(math.ceil(strut_ordinate))
    # calculating qequiv, begin by getting backside friction.
    # trying to account for if the height of failure plane is above top of sheet and below top of sheet
    text_output.append("")
    text_output.append("Width of failure plane = " + str(backside_x) + "'")
    text_output.append("Elevation @ failure plane = " + str(backside_y) + "'")
    text_output.append("")
    text_output.append("Backside Shear:")
    backside_friction = 0
    N = 0
    if backside_y >= layers[0][0]:
        if layers[0][0] < water_elev:
            if total_weights != -1:
                weight = (backside_y - layers[0][0]) * layers[0][1].sub
            else:
                weight = (backside_y - layers[0][0]) * layers[0][1].gamma
        else:
            weight = (backside_y - layers[0][0]) * layers[0][1].gamma
        if layers[0][1].type == 0:
            backside_friction = weight * 0.5 * layers[0][1].ka * (backside_y - layers[0][0]) * math.tan(math.radians(layers[0][1].phi))
            text_output.append(str(weight) + "psf * 0.5 * " + str(layers[0][1].ka) + " * (" + str(backside_y) + "' - " + str(layers[0][0]) + "') * tan(" +
                               str(layers[0][1].phi) + "°) = " + str(round(backside_friction, 2)) + "#/'")
        else:
            backside_friction = (backside_y - layers[0][0]) * layers[0][1].qu * 1000
            text_output.append("(" + str(backside_y) + "' - " + str(layers[0][0]) + "') * " +
                               str(layers[0][1].qu * 1000) + "psf = " + str(round(backside_friction, 2)) + "#/'")
        old_active = weight * layers[0][1].ka
        new_active = 0
        for i in range(len(layers) - 1):
            if layers[i + 1][0] >= cut_elev:
                if layers[i][0] <= water_elev:
                    if total_weights != -1:
                        weight += (layers[i][0] - layers[i + 1][0]) * layers[i][1].sub
                    else:
                        weight += (layers[i][0] - layers[i + 1][0]) * layers[i][1].gamma
                else:
                    weight += (layers[i][0] - layers[i + 1][0]) * layers[i][1].gamma
                new_active = weight * layers[i+1][1].ka
                print(weight, old_active, new_active, layers[i][0], layers[i+1][0])
                if layers[i][1].type == 0:
                    backside_friction += 0.5 * (new_active + old_active) * (layers[i][0] - layers[i + 1][0]) * math.tan(
                        math.radians(layers[i][1].phi))
                    text_output.append(str(new_active + old_active) + "psf * 0.5 * (" + str(layers[i][0]) + "' - " + str(layers[i+1][0]) + "') * tan(" +
                               str(layers[i][1].phi) + "°) = " + str(round(0.5 * (new_active + old_active) * (layers[i][0] - layers[i + 1][0]) * math.tan(
                        math.radians(layers[i][1].phi)), 2)) + "#/'")
                else:
                    backside_friction += (layers[i][0] - layers[i + 1][0]) * layers[i][1].qu * 1000
                    text_output.append("(" + str(layers[i][0]) + "' - " + str(layers[i+1][0]) + "') * " +
                               str(layers[i][1].qu * 1000) + "psf = " + str(round(
                        (layers[i][0] - layers[i + 1][0]) * layers[i][1].qu * 1000, 2)) + "#/'")
            old_active = new_active
    if backside_y < layers[0][0]:
        weight = 0
        for i in range(len(layers)-1):
            if layers[i][0] > backside_y > layers[i+1][0]:
                if layers[i][0] <= water_elev:
                    if total_weights != -1:
                        weight += (backside_y - layers[i + 1][0]) * layers[i][1].sub
                    else:
                        weight += (backside_y - layers[i + 1][0]) * layers[i][1].gamma
                else:
                    weight += (backside_y - layers[i + 1][0]) * layers[i][1].gamma

                if layers[i][1].type == 0:
                    backside_friction += 0.5 * weight * layers[i][1].ka * (backside_y - layers[i + 1][0]) * math.tan(
                        math.radians(layers[i][1].phi))
                    text_output.append(str(weight) + "psf * 0.5 *" + str(layers[i][1].ka) + " (" + str(backside_y) + "' - " + str(
                        layers[i + 1][0]) + "') * tan(" +
                                       str(layers[i][1].phi) + "°) = " + str(
                        round(0.5 * weight * layers[i][1].ka * (backside_y - layers[i + 1][0]) * math.tan(
                            math.radians(layers[i][1].phi)), 2)) + "#/'")
                else:
                    backside_friction += (backside_y - layers[i + 1][0]) * layers[i][1].qu * 1000
                    text_output.append("(" + str(backside_y) + "' - " + str(layers[i + 1][0]) + "') * " +
                                       str(layers[i][1].qu * 1000) + "psf = " + str(round(
                        (backside_y - layers[i + 1][0]) * layers[i][1].qu * 1000, 2)) + "#/'")
                    break
            old_active = weight * layers[0][1].ka
        for i in range(len(layers) - 1):
            if layers[i][0] <= backside_y:
                if layers[i + 1][0] >= cut_elev:
                    if layers[i][0] < water_elev:
                        if total_weights != -1:
                            weight += (layers[i][0] - layers[i + 1][0]) * layers[i][1].sub
                        else:
                            weight += (layers[i][0] - layers[i + 1][0]) * layers[i][1].gamma
                    else:
                        weight += (layers[i][0] - layers[i + 1][0]) * layers[i][1].gamma
                    new_active = weight * layers[i + 1][1].ka
                    if layers[i][1].type == 0:
                        backside_friction += 0.5 * (old_active + new_active) * (layers[i][0] - layers[i + 1][0]) * math.tan(
                            math.radians(layers[i][1].phi))
                        text_output.append(str(old_active + new_active) + "psf * 0.5 * (" + str(layers[i][0]) + "' - " + str(
                            layers[i + 1][0]) + "') * tan(" +
                                           str(layers[i][1].phi) + "°) = " + str(
                            round(0.5 * (old_active + new_active) * (layers[i][0] - layers[i + 1][0]) * math.tan(
                                math.radians(layers[i][1].phi)), 2)) + "#/'")
                    else:
                        backside_friction += (layers[i][0] - layers[i + 1][0]) * layers[i][1].qu * 1000
                        text_output.append("(" + str(layers[i][0]) + "' - " + str(layers[i + 1][0]) + "') * " +
                                           str(layers[i][1].qu * 1000) + "psf = " + str(round(
                            (layers[i][0] - layers[i + 1][0]) * layers[i][1].qu * 1000, 2)) + "#/'")

    text_output.append("Backside Shear = " + str(math.ceil(backside_friction)) + "#/'")
    text_output.append("")
    text_output.append("ƔH @ Elev. " + str(cut_elev) + "':")
    # now calculating gamma*H at bottom of cut.  start by calculating surcharge at failure plane
    vert_pressure = 0
    for i in range(len(layers)):
        if layers[i][0] == cut_elev:
            vert_pressure = layers[i][2] + layers[i][3]
            text_output.append(str(layers[i][2] + layers[i][3]) + "psf")
            break
    count = 0
    for i in range(len(layers)):
        if layers[i][0] == cut_elev:
            break
        count += 1
    if count == len(layers):
        count -= 1
    for i in range(len(layers) - 1):
        if layers[i+1][0] >= cut_elev:
            if layers[i][0] <= water_elev:
                if i <= total_weights and count != total_weights:
                    vert_pressure = vert_pressure + (layers[i][0] - layers[i + 1][0]) * layers[i][1].sub
                    text_output.append(
                        str("(" + str(layers[i][0]) + "' - " + str(layers[i+1][0]) + "')*" + str(
                            layers[i][1].sub) + "psf"))
                else:
                    vert_pressure = vert_pressure + (layers[i][0] - layers[i + 1][0]) * layers[i][1].gamma
                    text_output.append(
                        str("(" + str(layers[i][0]) + "' - " + str(layers[i + 1][0]) + "')*" + str(
                            layers[i][1].gamma) + "psf"))
            else:
                vert_pressure = vert_pressure + (layers[i][0] - layers[i + 1][0]) * layers[i][1].gamma
                text_output.append(
                    str("(" + str(layers[i][0]) + "' - " + str(layers[i + 1][0]) + "')*" + str(
                        layers[i][1].gamma) + "psf"))
    text_output.append("ƔH @ Elev. " + str(cut_elev) + "'=" + str(math.ceil(vert_pressure)) + " psf ")
    text_output.append("")

    q_equiv = math.ceil((vert_pressure * backside_x - backside_friction) / backside_x)
    text_output.append("q_equiv = (" + str(math.ceil(vert_pressure)) + "psf * " + str(backside_x) + "' - " + str(math.ceil(backside_friction)) + "#/') / " + str(backside_x) + "' = " + str(q_equiv) + " psf")
    text_output.append("")

    # compute active pressures below cut
    # going to need an extra work point at the cut, save active pressure at that point as cut_active
    cut_active = 0
    active_pressure_string = ""
    for i in range(len(layers)-1):
        if layers[i][0] == cut_elev and layers[i + 1][0] != cut_elev:
            vert_pressure = q_equiv + layers[i][3]
            active_pressure_string = "Pa @ " + str(cut_elev) + "' = (" + str(q_equiv + layers[i][3]) + "psf"
            if layers[i][1].type == 0:
                cut_active = math.ceil(vert_pressure * layers[i][1].ka) + layers[i][4]
            if layers[i][1].type == 1:
                cut_active = math.ceil(vert_pressure - layers[i][1].qu * 2000) + layers[i][4]
            ka_min = 0.25
            if layers[i][1].type == 1 and layers[i][1].ka != 1:
                ka_min = layers[i][1].ka
            if layers[i][1].type == 1 and cut_active <= vert_pressure * ka_min:
                cut_active = math.ceil(vert_pressure * ka_min) + layers[i][4]
                active_pressure_string += ")-2*" + str(layers[i][1].qu * 1000) + "psf = (-) => " + str(
                    vert_pressure) + "psf*" + str(ka_min)
            elif layers[i][1].type == 1 and not cut_active <= vert_pressure * ka_min:
                active_pressure_string += ")-2*" + str(layers[i][1].qu * 1000) + "psf"
            else:
                active_pressure_string += ")*" + str(layers[i][1].ka)
    active_pressure_string += " = " + (str(cut_active)) + " psf"
    text_output.append(active_pressure_string)

    # compute apparent pressures below cut
    for i in range(len(layers)):
        if layers[i][0] < cut_elev:
            vert_pressure = q_equiv + layers[i][3]
            active_pressure_string = "Pa @ " + str(layers[i][0]) + "' = (" + str(q_equiv + layers[i][3]) + "psf"
            for k in range(i + 1):
                if k != 0:
                    if layers[k - 1][0] != layers[k][0]:
                        if layers[k - 1][0] <= cut_elev:
                            if layers[k][0] < water_elev:
                                if i <= total_weights:
                                    vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].sub
                                    active_pressure_string += " + " + str(layers[k][1].sub) + "pcf*" + str(
                                        round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
                                else:
                                    vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][
                                        1].gamma
                                    active_pressure_string += " + " + str(layers[k][1].gamma) + "pcf*" + str(
                                        round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
                            else:
                                vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * layers[k][1].gamma
                                active_pressure_string += " + " + str(layers[k][1].gamma) + "pcf*" + str(
                                    round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
            if layers[i][1].type == 0:
                active_pressure = math.ceil(vert_pressure * layers[i][1].ka) + layers[i][4]
            if layers[i][1].type == 1:
                active_pressure = math.ceil(vert_pressure - layers[i][1].qu * 2000) + layers[i][4]
            ka_min = 0.25
            if layers[i][1].type == 1 and layers[i][1].ka != 1:
                ka_min = layers[i][1].ka
            if layers[i][1].type == 1 and active_pressure <= vert_pressure * ka_min:
                active_pressure = math.ceil(vert_pressure * ka_min) + layers[i][4]
                active_pressure_string += ")-2*" + str(layers[i][1].qu * 1000) + "psf = (-) => " + str(
                    vert_pressure) + "psf*" + str(ka_min)
            elif layers[i][1].type == 1 and not active_pressure <= vert_pressure * ka_min:
                active_pressure_string += ")-2*" + str(layers[i][1].qu * 1000) + "psf"
            else:
                active_pressure_string += ")*" + str(layers[i][1].ka)
            active_pressure_string += " = " + (str(active_pressure)) + " psf"
            text_output.append(active_pressure_string)
            apparent_pressure_wall_pressures.append(active_pressure)
            apparent_pressure_strut_pressures.append(0)

    # now make the wall "actives" and strut "actives"
    apparent_wall_actives = []
    apparent_strut_actives = []
    for i in range(len(apparent_pressure_elevations)-1):
        apparent_wall_actives.append((apparent_pressure_elevations[i], apparent_pressure_wall_pressures[i]))
        if apparent_pressure_elevations[i] >= cut_elev and not apparent_pressure_elevations[i-1] == apparent_pressure_elevations[i] == cut_elev:
            apparent_strut_actives.append((apparent_pressure_elevations[i], apparent_pressure_strut_pressures[i]))


    net_pressures = []
    heights = []
    text_output.append("")

    for i in range(len(apparent_wall_actives)):
        check = 0
        net_pressure = apparent_wall_actives[i][1] + water_pressures[i][1] - passive_pressures[i][1]
        net_string = "Pnet @ " + str(apparent_wall_actives[i][0]) + "' (Pa+Pw-Pp) = " + \
                     str(apparent_wall_actives[i][1]) + "psf + " + str(water_pressures[i][1]) + "psf - " + \
                     str(passive_pressures[i][1]) + "psf = " + str(net_pressure) + " psf"
        if apparent_wall_actives[i][0] == cut_elev:
            net_pressures.append(math.ceil(apparent_wall_actives[i][1] + water_pressures[i][1]))
            heights.append(apparent_wall_actives[i][0])
            text_output.append("Pnet @ " + str(apparent_wall_actives[i][0]) + "' (Pa+Pw-Pp) = " + str(apparent_wall_actives[i][1]) +
                               "psf + " + str(water_pressures[i][1]) + "psf - 0 psf = "  + str(math.ceil(apparent_wall_actives[i][1] + water_pressures[i][1])) + " psf")
            check = 1
        if check == 0:
            net_pressures.append(net_pressure)
            heights.append(active_pressures[i][0])
            text_output.append(net_string)
        if check == 1:
            net_pressures.append(cut_active + water_pressures[i][1] - passive_pressures[i][1])
            heights.append(active_pressures[i][0])
            text_output.append("Pnet @ " + str(apparent_wall_actives[i][0]) + "' (Pa+Pw-Pp) = " + str(cut_active) +
                               "psf + " + str(water_pressures[i][1]) + "psf - " + str(passive_pressures[i][1]) +
                               "psf = " + str(cut_active + water_pressures[i][1] - passive_pressures[i][1]) + " psf")

    if ers_type == 1 and soldier_beam_method == 0:
        for i in range(len(heights)):
            if heights[i] > cut_elev:
                net_pressures[i] = round(net_pressures[i] * beam_spacing, 0)
            if heights[i] == cut_elev and heights[i + 1] == heights[i]:
                if net_pressures[i] >= 0:
                    net_pressures[i] = net_pressures[i] * beam_spacing
                else:
                    net_pressures[i] = 0
            if heights[i] == cut_elev and heights[i + 1] != heights[i]:
                if net_pressures[i] >= 0:
                    net_pressures[i] = net_pressures[i] * beam_type[4]
                else:
                    net_pressures[i] = 0
            if cut_elev > heights[i] > cut_elev - zero_length + 0.01:
                if net_pressures[i] <= 0:
                    net_pressures[i] = 0
            if cut_elev - zero_length + 0.01 >= heights[i] >= cut_elev - zero_length - 0.01 and heights[i + 1] == \
                    heights[i]:
                if net_pressures[i] >= 0:
                    pass
                else:
                    net_pressures[i] = 0
            if cut_elev - zero_length + 0.01 >= heights[i] >= cut_elev - zero_length - 0.01 and heights[i + 1] != \
                    heights[i]:
                net_pressures[i] = round(3 * beam_type[4] * net_pressures[i], 0)

            if heights[i] < (cut_elev - zero_length - 0.01):
                net_pressures[i] = round(3 * beam_type[4] * net_pressures[i], 0)

    if ers_type == 1 and soldier_beam_method == 1:
        for i in range(len(heights)):
            if heights[i] > cut_elev:
                # NO CHANGE
                net_pressures[i] = round(net_pressures[i] * beam_spacing, 0)
            if heights[i] == cut_elev and heights[i + 1] == heights[i]:
                # NO CHANGE
                if net_pressures[i] >= 0:
                    net_pressures[i] = net_pressures[i] * beam_spacing
                else:
                    net_pressures[i] = 0
            if heights[i] == cut_elev and heights[i + 1] != heights[i]:
                # NO CHANGE
                if net_pressures[i] >= 0:
                    net_pressures[i] = net_pressures[i] * beam_type[4]
                else:
                    net_pressures[i] = 0
            if cut_elev > heights[i] > cut_elev - zero_length + 0.01:
                # NO CHANGE
                if net_pressures[i] <= 0:
                    net_pressures[i] = 0
            if cut_elev - zero_length + 0.01 >= heights[i] >= cut_elev - zero_length - 0.01 and heights[i + 1] == \
                    heights[i]:
                # NO CHANGE
                if net_pressures[i] >= 0:
                    pass
                else:
                    net_pressures[i] = 0
            if cut_elev - zero_length + 0.01 >= heights[i] >= cut_elev - zero_length - 0.01 and heights[i + 1] != \
                    heights[i]:
                # net_pressures[i] = round(3 * beam_type[4] * net_pressures[i], 0)
                net_pressure = beam_type[4] * (active_pressures[i - 1][1] + water_pressures[i - 1][1]) - 3 * beam_type[
                    4] * passive_pressures[i - 1][1]
                passive_limit = (active_pressures[i - 1][1] + water_pressures[i - 1][1] - passive_pressures[i - 1][
                    1]) * beam_spacing
                if net_pressure >= passive_limit:
                    net_pressures[i] = round(net_pressure, 0)
                else:
                    net_pressures[i] = round(passive_limit, 0)

            if heights[i] < (cut_elev - zero_length - 0.01):
                # net_pressures[i] = round(3 * beam_type[4] * net_pressures[i], 0)
                net_pressure = beam_type[4] * (active_pressures[i - 1][1] + water_pressures[i - 1][1]) - 3 * beam_type[
                    4] * passive_pressures[i - 1][1]
                passive_limit = (active_pressures[i - 1][1] + water_pressures[i - 1][1] - passive_pressures[i - 1][
                    1]) * beam_spacing
                if net_pressure >= passive_limit:
                    net_pressures[i] = round(net_pressure, 0)
                else:
                    net_pressures[i] = round(passive_limit, 0)

    strut_pressures = []
    strut_heights = []
    if ers_type == 0:
        for i in range(len(apparent_strut_actives)):
            strut_pressures.append(apparent_strut_actives[i][1]+water_pressures[i][1])
            strut_heights.append(apparent_strut_actives[i][0])
    if ers_type == 1:
        for i in range(len(apparent_strut_actives)):
            strut_pressures.append((apparent_strut_actives[i][1]+water_pressures[i][1])*beam_spacing)
            strut_heights.append(apparent_strut_actives[i][0])

    return net_pressures, heights, strut_pressures, strut_heights, text_output


def apparent_pressures_output():
    return


# layer_1 = Layer('sand', 0, 120, 0, 0.30, 3, 32)
# layer_2 = Layer('clay', 1, 135, 1, 0.30, 1, 0)
# layer_3 = Layer('clay', 1, 125, 0.6, 0.3, 1, 0)
# layer_4 = Layer('clay', 1, 125, 0.55, 1, 1, 0)
# layer_5 = Layer('clay', 1, 125, 0.8, 1, 1, 0)
# layer_6 = Layer('clay', 1, 125, 1.75, 1, 1, 0)
#
# layers = [[13, layer_1, 0, 0, 0, 0],
#           [8.1, layer_1, 30, 0, 0, 0],
#           [8, layer_1, 30, 0, 0, 0],
#           [8, layer_2, 30, 0, 0, 0],
#           [6.5, layer_2, 90, 0, 0, 0],
#           [2, layer_2, 210, 0, 0, 0],
#           [2, layer_3, 210, 0, 0, 0],
#           [-1, layer_3, 240, 0, 0, 0],
#           [-3, layer_3, 270, 0, 0, 0],
#           [-3, layer_4, 270, 0, 0, 0],
#           [-6.5, layer_4, 300, 0, 0, 0],
#           [-9, layer_4, 300, 0, 0, 0],
#           [-15, layer_4, 330, 0, 0, 0],
#           [-15, layer_3, 330, 0, 0, 0],
#           [-19, layer_3, 330, 0, 0, 0],
#           [-19, layer_5, 330, 0, 0, 0],
#           [-26, layer_5, 330, 0, 0, 0],
#           [-26, layer_6, 330, 0, 0, 0]]
#
# water_elev = -10000
# cut_elev = -6.5
# active = active_pressures(layers, water_elev, 10000)
# water = water_pressures(layers, water_elev, cut_elev, 10000, 30)
# passive = passive_pressures(layers, water_elev, cut_elev, 10000)
# x = apparent_pressures(active, passive, water, cut_elev, 1, 19.5, 14, layers, -10000, 10000, 0, 0, 0, 0, 0)
# print(x)
