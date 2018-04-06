import math


class Layer:
    def __init__(self, name, type, gamma, qu, ka, kp):
        self.name = name  # String of designation of soil (fill, soft clay, dense sand, etc)
        self.type = type  # 0 for granular, 1 for cohesive
        self.gamma = gamma  # Unit weight of soil in units pounds per cubic foot.
        self.sub = gamma - 62.4  # Submerged unit weight
        self.qu = qu  # Unconfined compressive strength in units of tons per square foot.
        self.ka = ka  # Active lateral earth pressure coefficient (determined outside of program)
        self.kp = kp  # Passive lateral earth pressure coefficient (determined outside of program)


def active_pressures(layers, water_elev, total_weights):
    active_pressures = []
    for i in range(len(layers)):
        vert_pressure = layers[i][2]+layers[i][3]
        for k in range(i+1):
            if k != 0:
                if layers[k-1][0] != layers[k][0]:
                    if layers[k][0] < water_elev:
                        if i <= total_weights:
                            vert_pressure = vert_pressure + (layers[k-1][0]-layers[k][0])*layers[k][1].sub
                        else:
                            vert_pressure = vert_pressure + (layers[k-1][0]-layers[k][0])*layers[k][1].gamma
                    else:
                        vert_pressure = vert_pressure + (layers[k-1][0]-layers[k][0])*layers[k][1].gamma
        active_pressure = math.ceil(vert_pressure*layers[i][1].ka - layers[i][1].qu*2000)+layers[i][4]
        if layers[i][1].type == 1 and \
                        math.ceil(vert_pressure*layers[i][1].ka - layers[i][1].qu*2000) <= vert_pressure * 0.25:
            active_pressure = math.ceil(vert_pressure * 0.25) + layers[i][4]
        active_pressures.insert(i, (layers[i][0], active_pressure))
    return active_pressures


def passive_pressures(layers, water_elev, cut_elev, total_weights):
    passive_pressures = []
    for i in range(len(layers)):
        vert_pressure = 0
        for k in range(i+1):
            if k != 0 and layers[k][0] < cut_elev:
                if layers[k-1][0] != layers[k][0]:
                    if layers[k][0] < water_elev:
                        if i <= total_weights:
                            vert_pressure = vert_pressure + (layers[k-1][0]-layers[k][0])*(layers[k][1].sub - layers[k][-1])
                        else:
                            vert_pressure = vert_pressure + (layers[k-1][0]-layers[k][0])*(layers[k][1].gamma - layers[k][-1])
                    else:
                        vert_pressure = vert_pressure + (layers[k-1][0]-layers[k][0])*(layers[k][1].gamma - layers[k][-1])
        passive_pressure = 0
        if layers[i][0] <= cut_elev:
            passive_pressure = math.floor(vert_pressure * layers[i][1].kp + layers[i][1].qu * 2000)
        passive_pressures.insert(i, (layers[i][0], passive_pressure))
    return passive_pressures


def active_pressures_front(layers, water_elev, cut_elev, total_weights):
    active_pressures_front = []
    for i in range(len(layers)):
        vert_pressure = 0
        for k in range(i + 1):
            if k != 0 and layers[k][0] < cut_elev:
                if layers[k - 1][0] != layers[k][0]:
                    if layers[k][0] < water_elev:
                        if i <= total_weights:
                            vert_pressure = vert_pressure + (layers[k-1][0]-layers[k][0])*layers[k][1].sub
                        else:
                            vert_pressure = vert_pressure + (layers[k-1][0]-layers[k][0])*layers[k][1].gamma
                    else:
                        vert_pressure = vert_pressure + (layers[k-1][0]-layers[k][0])*layers[k][1].gamma
        active_pressure = 0
        if layers[i][0] <= cut_elev:
            active_pressure = math.ceil(vert_pressure * layers[i][1].ka - layers[i][1].qu * 2000)
        if layers[i][1].type == 1 and \
                        math.ceil(vert_pressure * layers[i][1].ka - layers[i][1].qu * 2000) <= vert_pressure * 0.25:
            active_pressure = math.ceil(vert_pressure * 0.25)
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
                            vert_pressure = vert_pressure + (layers[k-1][0]-layers[k][0])*layers[k][1].sub
                        else:
                            vert_pressure = vert_pressure + (layers[k-1][0]-layers[k][0])*layers[k][1].gamma
                    else:
                        vert_pressure = vert_pressure + (layers[k-1][0]-layers[k][0])*layers[k][1].gamma
        if layers[i][0] > cut_elev:
            passive_pressure = 0
        else:
            passive_pressure = math.floor(vert_pressure * layers[i][1].kp + layers[i][1].qu * 2000)
        passive_pressures_back.insert(i, (layers[i][0], passive_pressure))
    layers[0][0] = temp
    return passive_pressures_back


def net_pressures(active_pressures, passive_pressures, water_pressures,
                  cut_elev, ers_type, beam_spacing, zero_length,
                  beam_type):
    net_pressures = []
    heights = []
    if len(active_pressures) != len(passive_pressures):
        return("error")
    else:
        for i in range(len(active_pressures)):
            net_pressure = active_pressures[i][1] + water_pressures[i][1]- passive_pressures[i][1]
            if active_pressures[i][0] == cut_elev:
                net_pressures.append(active_pressures[i][1]+water_pressures[i][1])
                heights.append(active_pressures[i][0])
            net_pressures.append(net_pressure)
            heights.append(active_pressures[i][0])

    if ers_type == 1:
        for i in range(len(heights)):
            if heights[i] > cut_elev:
                net_pressures[i] = round(net_pressures[i]*beam_spacing, 0)
            if heights[i] == cut_elev and heights[i+1] == heights[i]:
                if net_pressures[i] >= 0:
                    net_pressures[i] = net_pressures[i]*beam_spacing
                else:
                    net_pressures[i] = 0
            if heights[i] == cut_elev and heights[i+1] != heights[i]:
                if net_pressures[i] >= 0:
                    net_pressures[i] = net_pressures[i]*beam_type[4]
                else:
                    net_pressures[i] = 0
            if cut_elev > heights[i] > cut_elev - zero_length+0.01:
                if net_pressures[i] <= 0:
                    net_pressures[i] = 0
            if cut_elev - zero_length + 0.01 >= heights[i] >= cut_elev - zero_length - 0.01 and heights[i+1] == heights[i]:
                temp = net_pressures[i]
                if net_pressures[i] >= 0:
                    net_pressures[i] = temp
                else:
                    net_pressures[i] = 0
            if cut_elev - zero_length + 0.01 >= heights[i] >= cut_elev - zero_length - 0.01 and heights[i + 1] != \
                    heights[i]:
                net_pressures[i] = round(3 * beam_type[4] * temp, 0)
            if heights[i] < (cut_elev - zero_length):
                net_pressures[i] = round(3*beam_type[4]*net_pressures[i], 0)

    return net_pressures, heights


def cant_pressures(active_pressures, passive_pressures, water_pressures,
                   cut_elev, ers_type, beam_spacing, zero_length, beam_type ):
    net_pressures = []
    heights = []
    if len(active_pressures) != len(passive_pressures):
        return("error")
    else:
        for i in range(len(active_pressures)):
            net_pressure = active_pressures[i][1] - water_pressures[i][1] - passive_pressures[i][1]
            net_pressures.append(net_pressure)
            heights.append(active_pressures[i][0])
    if ers_type == 1:
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
                    net_pressures[i] = net_pressures[i]*beam_type[4]
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
                net_pressures[i] = 3 * beam_type[4] * temp
            if heights[i] < (cut_elev - zero_length):
                net_pressures[i] = 3 * beam_type[4] * net_pressures[i]
        for i in range(len(heights)):
            if heights[i] == cut_elev - zero_length:
                heights.insert(i + 1, heights[i])
                net_pressures.insert(i + 1, 3 * beam_type[4] * net_pressures[i])
                break
        for i in range(len(heights)):
            if heights[i] == cut_elev - zero_length:
                heights.insert(i+1, heights[i])
                net_pressures.insert(i+1, 3*beam_type[4]*net_pressures[i])
                break
    new_nets = []
    new_heights = []
    for i in range(len(net_pressures)):
        if net_pressures[i] != 0:
            new_nets.append(-1*net_pressures[i])
            new_heights.append(heights[i])

    return new_nets, new_heights


def water_pressures(layers, water_elev, cut_elev, total_weights, supplied_elev):
    water_pressures = []
    for i in range(len(layers)):
        if i <= total_weights:
            if layers[i][0] >= water_elev:
                water_pressure = 0
            elif water_elev >= layers[i][0] >= cut_elev:
                water_pressure = math.ceil((water_elev - layers[i][0])*62.4)
            elif water_elev >= cut_elev >= layers[i][0]:
                water_pressure = math.ceil((water_elev - cut_elev)*62.4)
            else:
                water_pressure = 0
        else:
            water_pressure = 0
        water_pressures.append([layers[i][0], water_pressure])

    check = 0
    for i in range(len(layers)):
        if layers[i][5] != 0:
            check = 1
            break

    if check == 1:
        max_water_pressure = (water_elev - cut_elev)*62.4
        for i in range(len(water_pressures)):
            if cut_elev >= water_pressures[i][0] >= supplied_elev:
                water_pressures[i][1] = math.ceil(max_water_pressure - \
                                        max_water_pressure*(cut_elev-water_pressures[i][0])/(cut_elev - supplied_elev))
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
        active_pressure = math.ceil(vert_pressure * layers[i][1].ka - layers[i][1].qu * 2000)
        if layers[i][1].type == 1 and active_pressure <= vert_pressure * 0.25:
            active_pressure = math.ceil(vert_pressure * 0.25)
            active_pressure_string += ")-2*" + str(layers[i][1].qu*1000) + "psf = (-) => "  + str(vert_pressure) + "psf*0.25"
        elif layers[i][1].type == 1 and not active_pressure <= vert_pressure * 0.25:
            active_pressure_string += ")-2*" + str(layers[i][1].qu*1000) + "psf"
        else:
            active_pressure_string += ")*" + str(layers[i][1].ka)
        active_pressures.insert(i, (layers[i][0], active_pressure))
        active_pressure_string += " = " + (str(active_pressure))+" psf"
        output_string.append(active_pressure_string)
    return output_string


def passive_pressures_output(layers, water_elev, cut_elev, total_weights):
    passive_pressures = []
    output_string = []
    for i in range(len(layers)):
        vert_pressure = 0
        passive_pressure_string = "Pp @ " + str(layers[i][0]) + "' = (" + str(layers[i][5]) + "psf"
        for k in range(i + 1):
            if k != 0 and layers[k][0] < cut_elev:
                if layers[k - 1][0] != layers[k][0]:
                    if layers[k][0] < water_elev:
                        if i <= total_weights:
                            vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * (layers[k][1].sub - layers[k][-1])
                            passive_pressure_string += " + " + str(layers[k][1].sub - layers[k][-1]) + "pcf*" + str(
                                round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
                        else:
                            vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * (layers[k][1].gamma - layers[k][-1])
                            passive_pressure_string += " + " + str(layers[k][1].gamma - layers[k][-1]) + "pcf*" + str(
                                round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
                    else:
                        vert_pressure = vert_pressure + (layers[k - 1][0] - layers[k][0]) * (layers[k][1].gamma - layers[k][-1])
                        passive_pressure_string += " + " + str(layers[k][1].gamma - layers[k][-1]) + "pcf*" + str(
                            round((layers[k - 1][0] - layers[k][0]), 2)) + "'"
        passive_pressure = 0
        if layers[i][0] <= cut_elev:
            passive_pressure = math.floor(vert_pressure * layers[i][1].kp + layers[i][1].qu * 2000)
        if layers[i][1].type == 1:
            passive_pressure_string += ")+2*" + str(layers[i][1].qu*1000) + "psf"
        else:
            passive_pressure_string += ")*" + str(layers[i][1].kp)
        passive_pressures.insert(i, (layers[i][0], passive_pressure))
        passive_pressure_string += " = " + (str(passive_pressure))+" psf"
        if layers[i][0] <= cut_elev:
            output_string.append(passive_pressure_string)
    return output_string


def water_pressures_output(water_pressures):
    output_string = []
    for i in range(len(water_pressures)):
        output_string.append('Pw @ ' + str(water_pressures[i][0]) + "' = " + str(math.ceil(water_pressures[i][1])) + " psf")

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
        active_pressure_string += " 0psf "
        if layers[i][0] <= cut_elev:
            active_pressure = math.ceil(vert_pressure * layers[i][1].ka - layers[i][1].qu * 2000)
        if layers[i][1].type == 1 and active_pressure <= vert_pressure * 0.25:
            active_pressure = math.ceil(vert_pressure * 0.25)
            active_pressure_string += ")-2*" + str(layers[i][1].qu * 1000) + "psf = (-) => " + str(
                vert_pressure) + "psf*0.25"
        elif layers[i][1].type == 1 and not active_pressure <= vert_pressure * 0.25:
            active_pressure_string += ")-2*" + str(layers[i][1].qu*1000) + "psf"
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
                       ("Hu = " + str(water_elev) + "' - " + str(cut_elev) + "' = " + str(water_elev-cut_elev) + "'."),
                       ("D = " + str(cut_elev) + "' - " + str(supplied_elev) + "' = " + str(cut_elev - supplied_elev) +
                        "'."),
                       (chr(916))+chr(947) + "' = 20 * Hu/D = 20 * " + str(water_elev-cut_elev) + "/" +
                       str(cut_elev - supplied_elev) + " = " + (str(20*(water_elev-cut_elev)/(cut_elev - supplied_elev))
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
        delta = 20*h/d
        for i in range(len(layers)):
            if cut_elev >= layers[i][0] >= supplied_elev:
                layers[i][-1] = delta


    return layers, text_output