from bokeh.plotting import figure
from bokeh.models import Label, Arrow, NormalHead


def braced_pressure_plot(layers, net, brace_elev, min_length_pressure, min_length_elev, min_length,
                         deflection, scale_factor, multi_pressure, multi_elev, multiplier, zero_point):
    axis_size = max([max(net[0]), -1 * min(net[0])])
    p = figure(
        x_range=[-axis_size-1000, axis_size*2.5],
        y_range=[net[1][-1]-1, net[1][0]+3],
        title="Lateral Pressure Diagram",
        plot_width=900,
        plot_height=1200
    )
    p.xaxis.bounds = (0, 0)
    p.yaxis.bounds = (0, 0)
    p.line(net[0], net[1], line_width=2, color='black')
    p.line([0, 0], [layers[0][0], layers[-1][0]], color='black')
    p.line([float(min_length_pressure), 0], [float(min_length_elev), float(min_length_elev)], line_width=2,
           color="black")
    p.add_layout(Label(x=1.5*axis_size, y=float(min_length_elev), text=str(round(min_length_pressure, 2)),
                       text_font_size='12pt'))
    p.add_layout(Label(x=200, y=float(min_length_elev), text="Lmin = " + str(round(min_length, 2)) + "'",
                       text_font_size='12pt'))
    p.add_layout(Label(x=2*axis_size, y=net[1][0]+2, text="Deflection"))
    p.add_layout(Label(x=1.5*axis_size, y=net[1][0] + 2, text="Pressure"))
    for i in range(len(layers)):
        p.line([-axis_size-1000, axis_size*2.5], [layers[i][0], layers[i][0]],
               color='dimgray', alpha=0.7)
        work_point_label = Label(x=-axis_size-1000, y=layers[i][0], text=str(layers[i][0]), text_font_size='12pt')
        p.add_layout(work_point_label)
        for j in range(len(deflection[0])):
            if deflection[0][j][1] == layers[i][0] and deflection[0][j][1] != deflection[0][j-1][1]:
                p.add_layout(Label(x=2*axis_size, y=layers[i][0], text=str(round(deflection[0][j][0], 3))+'"',
                                   text_font_size='12pt'))
    x, y = 0, 0
    for k in range(len(net[0])):
        i = net[0][k]
        j = net[1][k]
        if j == y and i != x:
            pressure_label = Label(x=axis_size*1.5, y=j-0.5, text=str(i), text_font_size='12pt')
        else:
            pressure_label = Label(x=axis_size*1.5, y=j, text=str(i), text_font_size='12pt')
        x, y = i, j
        p.add_layout(pressure_label)
    p.add_layout(Arrow(end=NormalHead(size=10),
                       x_start=-0.25*axis_size, y_start=brace_elev, x_end=00, y_end=brace_elev))
    p.add_layout(Arrow(end=NormalHead(size=5),
                       x_start=-0.75 * axis_size, y_start=zero_point, x_end=-0.75 * axis_size, y_end=zero_point-1))
    waler_label = Label(x=-0.4*axis_size, y=brace_elev-0.5, text='T')
    p.add_layout(Label(x=-0.80*axis_size, y=zero_point, text='x=0'))
    p.add_layout(waler_label)
    if multi_pressure:
        p.line([round(float(multi_pressure), 2), 0], [round(float(multi_elev), 2),
                                                      round(float(multi_elev), 2)], line_width=2, color="black")
        p.add_layout(Label(x=200, y=float(multi_elev), text="Mult @ " + str(net[1][0]-multi_elev) + "' long = " +
                                                            str(round(multiplier, 2)), text_font_size='12pt'))
        # p.add_layout(Label(x=1.5 * axis_size, y=float(multi_elev), text=str(round(multi_pressure, 2)),
        #                    text_font_size='12pt'))
    deflection_x = []
    deflection_y = []
    for i in range(len(deflection[0])):
        deflection_x.append(deflection[0][i][0])
        deflection_y.append(deflection[0][i][1])

    deflection_shape = [-1*scale_factor*x for x in deflection_x]
    p.line(deflection_shape, deflection_y, color='green', line_width=1)
    deflection_label = Label(x=-axis_size, y=net[1][0]+2, text='Max Deflection = ' + str(deflection[1]) + '" at Elev. ' + str(deflection[2]) + "'.")
    p.add_layout(deflection_label)

    return p


def cant_pressure_plot(layers, net, min_length_cant_pressure, min_length_net_pressure, min_length_elev, min_length, z,
                       deflection, scale_factor, cant, multi_x, multi_y, multiplier, zero_point):
    axis_size = max([max(net[0]), -1 * min(net[0]), max(cant[0]), -1*min(cant[0])])
    p = figure(
        x_range=[-axis_size - 1000, axis_size*4.0],
        y_range=[net[1][-1] - 1, net[1][0] + 4],
        title="Lateral Pressure Diagram",
        plot_width=900,
        plot_height=1200
    )
    p.xaxis.bounds = (0, 0)
    p.yaxis.bounds = (0, 0)

    new_cant = [[], []]
    for i in range(len(cant[0])):
        if cant[0][i] != 0:
            new_cant[0].append(cant[0][i])
            new_cant[1].append(cant[1][i])
    cant = new_cant

    p.line(net[0], net[1], line_width=2, color='black')
    p.line(cant[0], cant[1], line_width=1, color='gray')
    p.line([0, 0], [layers[0][0], layers[-1][0]], color='black')
    p.line([float(min_length_net_pressure), float(min_length_cant_pressure)],
           [float(min_length_elev+z), float(min_length_elev)], line_width=2, color="black")
    p.line([0, float(min_length_cant_pressure)], [float(min_length_elev), float(min_length_elev)],
           line_width=2, color="black")

    p.add_layout(Label(x=1.25*axis_size, y=float(min_length_elev+z),
                       text=str(round(min_length_net_pressure, 2)), text_font_size='12pt'))
    p.add_layout(Label(x=2.25*axis_size, y=float(min_length_elev),
                       text=str(round(min_length_cant_pressure, 2)), text_font_size='12pt'))
    p.add_layout(Label(x=-axis_size, y=float(net[1][0] + 2), text="Lmin = " + str(round(min_length, 2)) + "'",
                       text_font_size='12pt'))
    p.add_layout(Label(x=3.25 * axis_size, y=net[1][0] + 2, text="Deflection", text_font_size='14pt'))
    p.add_layout(Label(x=1.25 * axis_size, y=net[1][0] + 2, text="Net Pressure", text_font_size='14pt'))
    p.add_layout(Label(x=2.25 * axis_size, y=net[1][0] + 2, text="Cant Pressure", text_font_size='14pt'))
    p.add_layout(Arrow(end=NormalHead(size=5),
                       x_start=-0.75 * axis_size, y_start=zero_point, x_end=-0.75 * axis_size, y_end=zero_point - 0.5))
    p.add_layout(Label(x=-0.80 * axis_size, y=zero_point, text="x=0'"))

    x, y = 0, 0
    for k in range(len(net[0])):
        i = net[0][k]
        j = net[1][k]
        if j == y and i != x:
            pressure_label = Label(x=1.25*axis_size, y=j-0.5, text=str(i), text_font_size='12pt')
        else:
            pressure_label = Label(x=1.25*axis_size, y=j, text=str(i), text_font_size='12pt')
        x, y = i, j
        p.add_layout(pressure_label)
    x, y = 0, 0
    for k in range(len(cant[0])):
        i = cant[0][k]
        j = cant[1][k]
        if j == y and i != x:
            pressure_label = Label(x=2.25*axis_size, y=j-0.5, text=str(i), text_font_size='12pt')
        else:
            pressure_label = Label(x=2.25*axis_size, y=j, text=str(i), text_font_size='12pt')
        x, y = i, j
        p.add_layout(pressure_label)

    for i in range(len(layers)):
        p.line([-axis_size-1000, 4.0*axis_size], [layers[i][0], layers[i][0]],
               color='dimgray', alpha=0.7)
        work_point_label = Label(x=-axis_size-500, y=layers[i][0], text=str(layers[i][0]), text_font_size='12pt')
        p.add_layout(work_point_label)
        for j in range(len(deflection[0])):
            if deflection[0][j][1] == layers[i][0] and deflection[0][j][1] != deflection[0][j-1][1]:
                p.add_layout(Label(x=3.25*axis_size, y=layers[i][0], text=str(round(deflection[0][j][0], 3))+'"',
                                   text_font_size='12pt'))
    if multi_x:
        p.line([round(float(multi_x[0]), 2), round(float(multi_x[1]), 2)],
               [round(float(multi_y[0]), 2), round(float(multi_y[1]), 2)], line_width=2, color="black")
        p.line([0, round(float(multi_x[1]), 2)],
               [round(float(multi_y[1]), 2), round(float(multi_y[1]), 2)], line_width=2, color="black")
        p.add_layout(Label(x=-axis_size, y=net[1][0] + 1, text="Mult @ " + str(net[1][0] - multi_y[1]) + "' long = " +
                                                            str(round(multiplier, 2)), text_font_size='12pt'))
        p.add_layout(Label(x=1.25 * axis_size, y=float(multi_y[0]), text=str(round(multi_x[0], 2)),
                           text_font_size='12pt'))
        p.add_layout(Label(x=2.25 * axis_size, y=float(multi_y[1]), text=str(round(multi_x[1], 2)),
                           text_font_size='12pt'))
    deflection_x = []
    deflection_y = []
    for i in range(len(deflection[0])):
        deflection_x.append(deflection[0][i][0])
        deflection_y.append(deflection[0][i][1])

    deflection_shape = [-1 * scale_factor * x for x in deflection_x]
    p.line(deflection_shape, deflection_y, color='green', line_width=1)
    deflection_label = Label(x=-axis_size, y=net[1][0] + 3, text='Max Deflection = ' + str(deflection[1]) +
                                                                 '" at Elev. ' + str(deflection[2]) + "'.",
                             text_font_size='12pt')
    p.add_layout(deflection_label)

    return p


def surface_plot(surface_array, work_points):
    p = figure(
        tools="pan,box_zoom,reset,save",
        title="Surface Plot",
        sizing_mode="stretch_both"
    )

    surface_x = []
    surface_y = []
    for i in range(len(surface_array)):
        surface_x.append(surface_array[i][0])
        surface_y.append(surface_array[i][1])

    p.line([0,0], [work_points[0][1], work_points[-1][1]], line_width=2, color='black')
    p.line(surface_x, surface_y, line_width=3, color='dimgray')

    for i in range(len(surface_array)):
        surface_label = Label(x=surface_x[i], y=surface_y[i], text="(" + str(surface_x[i]) + ", " + str(surface_y[i]) + ")")
        p.add_layout(surface_label)

    return p

def multi_layer_pressure_plot(layers, net, brace_elev, min_length_pressure, min_length_elev, min_length,
                         deflection, scale_factor, multi_pressure, multi_elev, multiplier, zero_point):
    axis_size = max([max(net[0]), -1 * min(net[0])])
    p = figure(
        x_range=[-axis_size-1000, axis_size*2.5],
        y_range=[net[1][-1]-1, net[1][0]+3],
        title="Wall Pressure Diagram",
        plot_width=900,
        plot_height=1200
    )
    p.xaxis.bounds = (0, 0)
    p.yaxis.bounds = (0, 0)
    p.line(net[0], net[1], line_width=2, color='black')
    p.line([0, 0], [layers[0][0], layers[-1][0]], color='black')
    p.line([float(min_length_pressure), 0], [float(min_length_elev), float(min_length_elev)], line_width=2,
           color="black")
    p.add_layout(Label(x=1.5*axis_size, y=float(min_length_elev), text=str(round(min_length_pressure, 2)),
                       text_font_size='12pt'))
    p.add_layout(Label(x=200, y=float(min_length_elev), text="Lmin = " + str(round(min_length, 2)) + "'",
                       text_font_size='12pt'))
    p.add_layout(Label(x=2*axis_size, y=net[1][0]+2, text="Deflection"))
    p.add_layout(Label(x=1.5*axis_size, y=net[1][0] + 2, text="Pressure"))
    for i in range(len(layers)):
        p.line([-axis_size-1000, axis_size*2.5], [layers[i][0], layers[i][0]],
               color='dimgray', alpha=0.7)
        work_point_label = Label(x=-axis_size-1000, y=layers[i][0], text=str(layers[i][0]), text_font_size='12pt')
        p.add_layout(work_point_label)
        for j in range(len(deflection[0])):
            if deflection[0][j][1] == layers[i][0] and deflection[0][j][1] != deflection[0][j-1][1]:
                p.add_layout(Label(x=2*axis_size, y=layers[i][0], text=str(round(deflection[0][j][0], 3))+'"',
                                   text_font_size='12pt'))
    x, y = 0, 0
    for k in range(len(net[0])):
        i = net[0][k]
        j = net[1][k]
        if j == y and i != x:
            pressure_label = Label(x=axis_size*1.5, y=j-0.5, text=str(i), text_font_size='12pt')
        else:
            pressure_label = Label(x=axis_size*1.5, y=j, text=str(i), text_font_size='12pt')
        x, y = i, j
        p.add_layout(pressure_label)
    p.add_layout(Arrow(end=NormalHead(size=10),
                       x_start=-0.25*axis_size, y_start=brace_elev[0], x_end=00, y_end=brace_elev[0]))
    p.add_layout(Arrow(end=NormalHead(size=10),
                       x_start=-0.25 * axis_size, y_start=brace_elev[1], x_end=00, y_end=brace_elev[1]))
    p.add_layout(Arrow(end=NormalHead(size=5),
                       x_start=-0.75 * axis_size, y_start=zero_point, x_end=-0.75 * axis_size, y_end=zero_point-1))
    top_waler_label = Label(x=-0.4*axis_size, y=brace_elev[0]-0.5, text='T1')
    bot_waler_label = Label(x=-0.4*axis_size, y=brace_elev[1]-0.5, text='T2')
    p.add_layout(Label(x=-0.80*axis_size, y=zero_point, text='x=0'))
    p.add_layout(top_waler_label)
    p.add_layout(bot_waler_label)
    if multi_pressure:
        p.line([round(float(multi_pressure), 2), 0], [round(float(multi_elev), 2),
                                                      round(float(multi_elev), 2)], line_width=2, color="black")
        p.add_layout(Label(x=200, y=float(multi_elev), text="Mult @ " + str(net[1][0]-multi_elev) + "' long = " +
                                                            str(round(multiplier, 2)), text_font_size='12pt'))
        # p.add_layout(Label(x=1.5 * axis_size, y=float(multi_elev), text=str(round(multi_pressure, 2)),
        #                    text_font_size='12pt'))
    deflection_x = []
    deflection_y = []
    for i in range(len(deflection[0])):
        deflection_x.append(deflection[0][i][0])
        deflection_y.append(deflection[0][i][1])

    deflection_shape = [-1*scale_factor*x for x in deflection_x]
    p.line(deflection_shape, deflection_y, color='green', line_width=1)
    deflection_label = Label(x=-axis_size, y=net[1][0]+2, text='Max Deflection = ' + str(deflection[1]) + '" at Elev. ' + str(deflection[2]) + "'.")
    p.add_layout(deflection_label)

    return p


def strut_pressure_plot(layers, net, brace_elev):
    axis_size = max([max(net[0]), -1 * min(net[0])])
    p = figure(
        x_range=[-axis_size-1000, axis_size*2.5],
        y_range=[net[1][-1]-3, net[1][0]+3],
        title="Strut Pressure Diagram",
        plot_width=800,
        plot_height=1200
    )
    p.xaxis.bounds = (0, 0)
    p.yaxis.bounds = (0, 0)
    p.line(net[0], net[1], line_width=2, color='black')
    p.line([0, 0], [layers[0][0], layers[-1][0]], color='black')
    p.add_layout(Label(x=1.5*axis_size, y=net[1][0] + 2, text="Pressure"))
    for i in range(len(layers)):
        p.line([-axis_size-1000, axis_size*2.5], [layers[i][0], layers[i][0]],
               color='dimgray', alpha=0.7)
        work_point_label = Label(x=-axis_size-1000, y=layers[i][0], text=str(layers[i][0]), text_font_size='12pt')
        p.add_layout(work_point_label)

    x, y = 0, 0
    for k in range(len(net[0])):
        i = net[0][k]
        j = net[1][k]
        if j == y and i != x:
            pressure_label = Label(x=axis_size*1.5, y=j-0.5, text=str(i), text_font_size='12pt')
        else:
            pressure_label = Label(x=axis_size*1.5, y=j, text=str(i), text_font_size='12pt')
        x, y = i, j
        p.add_layout(pressure_label)
    p.add_layout(Arrow(end=NormalHead(size=10),
                       x_start=-0.25*axis_size, y_start=brace_elev[0], x_end=00, y_end=brace_elev[0]))
    p.add_layout(Arrow(end=NormalHead(size=10),
                       x_start=-0.25 * axis_size, y_start=brace_elev[1], x_end=00, y_end=brace_elev[1]))
    top_waler_label = Label(x=-0.4*axis_size, y=brace_elev[0]-0.5, text='T1')
    bot_waler_label = Label(x=-0.4*axis_size, y=brace_elev[1]-0.5, text='T2')
    p.add_layout(top_waler_label)
    p.add_layout(bot_waler_label)

    return p
