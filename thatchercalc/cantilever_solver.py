import numpy
import math

force_constant = -1328.67
moment_constant = 6532.23
force_x_constant = -1370
force_x2_constant = 36.43
force_z_constant = 2143.5
force_xz_constant = -12.97
moment_x_constant = -1328.67
moment_x2_constant = -685
moment_x3_constant = 12.14
moment_z2_constant = 714.5
moment_xz2_constant = -4.32


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


print(cantilever_solver(force_constant, force_z_constant, force_xz_constant, force_x_constant, force_x2_constant,
                        moment_constant, moment_x_constant, moment_z2_constant, moment_xz2_constant, moment_x2_constant,
                        moment_x3_constant))