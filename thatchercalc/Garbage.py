# def minimum_length(net_pressures, cant_pressures):
#     distances = []
#     net_slopes = []
#     cant_slopes = []
#     for i in range(len(net_pressures[1])-1):
#         distance = -1*(net_pressures[1][i+1]-net_pressures[1][i])
#         distances.append(distance)
#         if distance != 0:
#             slope = (net_pressures[0][i+1]-net_pressures[0][i])/distance
#         else:
#             slope = 0
#         net_slopes.append(slope)
#     for i in range(len(cant_pressures[1])-1):
#         distance = -1*(cant_pressures[1][i+1] - cant_pressures[1][i])
#         if distance != 0:
#             slope = (cant_pressures[0][i+1]-cant_pressures[0][i])/distance
#         else:
#             slope = 0
#         cant_slopes.append(slope)
#     for i in range(len(cant_pressures[1])-1):
#         force_constant = 0
#         moment_constant = 0
#         for j in range(len(net_pressures[1])-1):
#             if net_pressures[1][j] > cant_pressures[1][i]:
#                 force_area = 0.5*(net_pressures[0][j]+net_pressures[0][j+1])*distances[j]
#                 if net_pressures[0][j] == net_pressures[0][j+1] == 0:
#                     moment_arm = (net_pressures[1][j+1]-cant_pressures[1][i])
#                 else:
#                     moment_arm =((2*net_pressures[0][j]+net_pressures[0][j+1])*(distances[j]) /
#                                 (3*(net_pressures[0][j]+net_pressures[0][j+1])))+(net_pressures[1][j+1]-cant_pressures[1][i])
#                 moment = force_area*moment_arm
#                 force_constant = force_constant + force_area
#                 moment_constant = moment_constant + moment
#         net_below_i = []
#         net_slope_below_i = []
#         for j in range(len(cant_pressures[1])):
#             net_below_i.append(0)
#         for j in range(len(cant_pressures[1])-1):
#             net_slope_below_i.append(0)
#         for j in range(len(cant_pressures[1])-i):
#             net_end = len(net_pressures[1])-1
#             net_below_i[-1-j] = net_pressures[0][net_end-j]
#         for j in range(len(cant_pressures[1])-1-i):
#             slope_end = len(net_slopes)-1
#             net_slope_below_i[-1-j] = net_slopes[slope_end-j]
#         force_z_term = (cant_pressures[0][i]-net_below_i[i])/2
#         force_xz_term = (cant_slopes[i]-net_slope_below_i[i])/2
#         force_x_term = net_below_i[i]
#         force_x2_term = 0.5*(net_slope_below_i[i])
#         moment_z2_term = (cant_pressures[0][i]-net_below_i[i])/6
#         moment_xz2_term = (cant_slopes[i]-net_slope_below_i[i])/6
#         moment_x_term = force_constant
#         moment_x2_term = net_below_i[i]/2
#         moment_x3_term = net_slope_below_i[i]/6
#         x = Symbol('x')
#         z = Symbol('z')
#         a = nsolve(
#             (force_constant + z * force_z_term + x * z * force_xz_term + x * force_x_term + x * x * force_x2_term,
#              moment_constant + x * moment_x_term + z * z * moment_z2_term + x * z * z * moment_xz2_term + x * x * moment_x2_term + x * x * x * moment_x3_term),
#             (x, z), ((cant_pressures[1][i] - cant_pressures[1][i + 1]), 0), verify=False)
#         x = a[0]
#         z = a[1]
#         x_pressure = cant_pressures[0][i]+cant_slopes[i]*x
#         z_pressure = net_below_i[i]+net_slope_below_i[i]*(x-z)
#         if 0<=x<=(cant_pressures[1][i]-cant_pressures[1][i+1]) and 0<=z<=(cant_pressures[1][i]-cant_pressures[1][i+1]):
#             Lmin=(net_pressures[1][0]-cant_pressures[1][i])+x
#             break
#     output = [round(x, 2), round(z, 2), round(Lmin, 2), x_pressure, z_pressure]
#
#     return output
#
#
# def maximum_moment(net_pressures):
#     distances = []
#     net_slopes = []
#     for i in range(len(net_pressures[1]) - 1):
#         distance = -1 * (net_pressures[1][i + 1] - net_pressures[1][i])
#         distances.append(distance)
#         if distance != 0:
#             slope = (net_pressures[0][i + 1] - net_pressures[0][i]) / distance
#         else:
#             slope = 0
#         net_slopes.append(slope)
#     shear = 0
#     moment = 0
#
#     for i in range(len(net_pressures[1])-1):
#         shear_unit = 0.5*(net_pressures[0][i]+net_pressures[0][i+1])*distances[i]
#         old_shear = shear
#         shear = shear + shear_unit
#         if old_shear >= 0 and shear <= 0:
#             y = Symbol('y')
#             answers = solve(old_shear + net_pressures[0][i]*y + net_slopes[i]*y*y/2)
#             for j in answers:
#                 if j > 0 and j < distances[i]:
#                     y = j
#                     zero_shear_point = net_pressures[1][0] - (net_pressures[1][0] - net_pressures[1][i] + y)
#
#     for i in range(len(net_pressures[1])-1):
#         force = 0.5 * (net_pressures[0][i] + net_pressures[0][i + 1]) * distances[i]
#         moment_arm = ((2*net_pressures[0][i]+net_pressures[0][i+1])*(distances[i]) / (3*(net_pressures[0][i]+net_pressures[0][i+1]))) + (net_pressures[1][i+1]-zero_shear_point)
#         if y-0.01 < moment_arm < y+0.01:
#             moment = moment + net_pressures[0][i+1]*y*y/2 + net_slopes[i+1]*y*y*y/6
# #         elif moment_arm > 0 and moment_arm != y:
# #             moment = moment + force*moment_arm
# #
# #     return moment
# def net_override(net_pressure):
#     net_pressure_edit = net_pressure
#     override = 0
#     if override != 0:
#         for i in override:
#             net_pressure_edit[0][i[0]] = i[1]
#     return (net_pressure_edit)
#
#
# def cant_override(cant_pressure):
#     cant_pressure_edit = cant_pressure
#     override = 0
#     if override != 0:
#         for i in override:
#             cant_pressure_edit[0][i[0]] = i[1]
#     return (cant_pressure_edit)
