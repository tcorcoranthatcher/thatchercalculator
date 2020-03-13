import math

# Micropile Joint Bending Capacity #

# Casing format
# [name, L (in), h (in), D (in), α (°), ID (in), OD (in), OD @ tension area (in)]
# [['casing', 1.75, 0.1218, 9.324, 30, 8.625, 9.715, 9.080]]

def micropile_joint_bending_capacity(L, h, D, alpha, ID, OD, D_female, Yp, Up, corrosion_reduction):
    casings = [['casing', L, h, D, alpha, ID, OD, D_female]]
    casing = casings[0]
    a = 2.39
    b = 0.59
    psi = 14.35
    L = casing[1]  # length from first complete thread to last complete thread
    h = casing[2]  # height of the pin threads
    D = casing[3]  # outside diameter of the pin measured from the top of the first thread from the shoulder
    alpha = casing[4]  # load bearing flank angle of the threads
    ID = casing[5]
    OD = casing[6]
    OD_joint = round(D - 2*h, 3)
    D_female = casing[7]
    ro = OD/2
    ri = ID/2
    ro_joint = OD_joint/2
    OD_no_corrosion = casing[6]+2*corrosion_reduction


    Ap = round((math.pi/4)*((D-h)**2-ID**2), 3)
    Ab = round((math.pi/4)*(OD**2-(D_female+h)**2), 3)
    A1_correction = round(math.pi*((D-2*h)**2-ID**2)/4,2)
    A2_correction = round(math.pi*(OD**2-(D_female+2*h)**2)/4, 2)
    Pi = round(A1_correction*((a*(2*h/D)**b*Up)/(0.5+(D/(2*L))*math.tan(math.radians(alpha-psi))) + Yp/(1+(D/(2*L))*math.tan(math.radians(alpha-psi)))), 2)
    Pfr = round((Up*(math.pi*((D-2*h)**2-ID**2))/4), 2)
    Pi_box = round(A2_correction*((a*(2*h/D_female)**b*Up)/(0.5+(D_female/(2*L))*math.tan(math.radians(alpha-psi))) + Yp/(1+(D_female/(2*L))*math.tan(math.radians(alpha-psi)))), 2)
    Pfr_box = round((Up*(math.pi*((OD)**2-(D_female+2*h)**2))/4), 2)

    limit_load = min(Pi, Pfr, Pi_box, Pfr_box)
    limit_load_description = ""
    if limit_load == Pi:
        limit_load_description = "Jump out of the pin controls."
    elif limit_load == Pfr:
        limit_load_description = "Fracture of the pin controls."
    elif limit_load == Pi_box:
        limit_load_description = "Jump out of the box controls."
    else:
        limit_load_description = "Fracture of the box controls."

    centroid_data = []
    if limit_load == Pi or limit_load == Pfr:
        image_check = 0
        for x_prime in range(1, round(1000*round(ID/2, 1))):
            x_prime = x_prime/1000
            theta_0 = math.radians(180 - 2*math.degrees(math.asin(x_prime/ro)))
            Ixo = (ro ** 4 / 8) * (theta_0 - math.sin(theta_0) + 2 * math.sin(theta_0) * math.sin(theta_0 / 2) ** 2)
            Ao = (ro**2/2)*(theta_0 - math.sin(theta_0))
            Cyo = (4*ro/3)*(math.sin(theta_0/2)**3)/(theta_0-math.sin(theta_0))
            Ixco = Ixo - Ao*Cyo**2
            Ixo_prime = Ixco + Ao*(Cyo-x_prime)**2
            centroid_data.append(Ao)
            centroid_data.append(Cyo)

            theta_1 = math.radians(180 - 2 * math.degrees(math.asin(x_prime / ri)))
            Ixi = (ri ** 4 / 8) * (theta_1 - math.sin(theta_1) + 2 * math.sin(theta_1) * math.sin(theta_1 / 2) ** 2)
            Ai = (ri**2/2)*(theta_1 - math.sin(theta_1))
            Cyi = (4 * ri / 3) * (math.sin(theta_1 / 2) ** 3) / (theta_1 - math.sin(theta_1))
            Ixci = Ixi - Ai * Cyi ** 2
            Ixi_prime = Ixci + Ai * (Cyi - x_prime) ** 2
            centroid_data.append(Ai)
            centroid_data.append(Cyi)

            I_above = round(Ixo_prime - Ixi_prime, 2)

            theta_2 = math.radians(180 - 2 * math.degrees(math.asin(x_prime / ro_joint)))
            Ixo = (ro_joint ** 4 / 8) * (theta_2 - math.sin(theta_2) + 2 * math.sin(theta_2) * math.sin(theta_2 / 2) ** 2)
            Ao = (ro_joint ** 2 / 2) * (theta_2 - math.sin(theta_2))
            Cyo = (4 * ro_joint / 3) * (math.sin(theta_2 / 2) ** 3) / (theta_2 - math.sin(theta_2))
            Ixco = Ixo - Ao * Cyo ** 2
            Ixo_prime = Ixco + Ao * (Cyo - x_prime) ** 2
            centroid_data.append(Ao)
            centroid_data.append(Cyo)

            I_below = round(math.pi*(OD_joint**4 - ID**4)/64 + math.pi*(OD_joint**2-ID**2)/4*x_prime**2 - (Ixo_prime-Ixi_prime), 2)

            if I_above == I_below or I_above-I_below <= 0.01:
                break
            else:
                centroid_data = []

        I_reduced = 2*I_below
        I_full = math.pi*(OD**4-ID**4)/64
        I_gross = math.pi*(OD_no_corrosion**4 - ID**4)/64
        intact_stiffness_percentage = round(I_reduced/I_full*100, 1)
        gross_stiffness_percentage = round(I_reduced/I_gross*100, 1)

        pin_stress = limit_load/(math.pi*((D-2*h)**2-ID**2)/4)

        area_compression = (ro**2*math.acos(x_prime/ro)-(x_prime*(2*ro*(ro-x_prime)-(ro-x_prime)**2)**0.5)) - \
                           (ri**2*math.acos(x_prime/ri)-(x_prime*(2*ri*(ri-x_prime)-(ri-x_prime)**2)**0.5))

        area_tension = (math.pi*(OD_joint**2 - ID**2)/4) - \
                       ((ro_joint**2*math.acos(x_prime/ro_joint)-(x_prime*(2*ro_joint*(ro_joint-x_prime) -
                                                                           (ro_joint-x_prime)**2)**0.5)) -
                        (ri**2*math.acos(x_prime/ri)-(x_prime*(2*ri*(ri-x_prime)-(ri-x_prime)**2)**0.5)))

        Cc = (centroid_data[0]*centroid_data[1] - centroid_data[2]*centroid_data[3])/(centroid_data[0]-centroid_data[2])-x_prime
        A_missing = centroid_data[4] - centroid_data[2]
        y_missing = (centroid_data[4]*centroid_data[5] - centroid_data[2]*centroid_data[3])/(centroid_data[4]-centroid_data[2])
        At = math.pi*(OD_joint**2-ID**2)/4
        A_remaining = At-A_missing
        Ct = A_missing*y_missing/A_remaining+x_prime

        Mt = limit_load*Ct
        Mc = limit_load*Cc
        Mtotal = Mt + Mc
        Mmax = Yp*I_full/ro
        Mgross= Yp*I_gross/(OD_no_corrosion/2)
        intact_moment_percentage = Mtotal/Mmax
        gross_moment_percentage = Mtotal/Mgross
        allowable_capacity = Mtotal/12/1.67


    else:
        image_check = 1
        for x_prime in range(1, round(1000 * round(ID / 2, 1))):
            x_prime = x_prime / 1000
            theta_0 = math.radians(180 - 2 * math.degrees(math.asin(x_prime / ro)))
            Ixo = (ro ** 4 / 8) * (theta_0 - math.sin(theta_0) + 2 * math.sin(theta_0) * math.sin(theta_0 / 2) ** 2)
            Ao = (ro ** 2 / 2) * (theta_0 - math.sin(theta_0))
            Cyo = (4 * ro / 3) * (math.sin(theta_0 / 2) ** 3) / (theta_0 - math.sin(theta_0))
            Ixco = Ixo - Ao * Cyo ** 2
            Ixo_prime = Ixco + Ao * (Cyo - x_prime) ** 2
            centroid_data.append(Ao)
            centroid_data.append(Cyo)

            theta_1 = math.radians(180 - 2 * math.degrees(math.asin(x_prime / ri)))
            Ixi = (ri ** 4 / 8) * (theta_1 - math.sin(theta_1) + 2 * math.sin(theta_1) * math.sin(theta_1 / 2) ** 2)
            Ai = (ri ** 2 / 2) * (theta_1 - math.sin(theta_1))
            Cyi = (4 * ri / 3) * (math.sin(theta_1 / 2) ** 3) / (theta_1 - math.sin(theta_1))
            Ixci = Ixi - Ai * Cyi ** 2
            Ixi_prime = Ixci + Ai * (Cyi - x_prime) ** 2
            centroid_data.append(Ai)
            centroid_data.append(Cyi)

            I_above = round(Ixo_prime - Ixi_prime, 2)

            theta_2 = math.radians(180 - 2 * math.degrees(math.asin(x_prime / ro_joint)))
            Ixi = (ro_joint ** 4 / 8) * (
                        theta_2 - math.sin(theta_2) + 2 * math.sin(theta_2) * math.sin(theta_2 / 2) ** 2)
            Ai = (ro_joint ** 2 / 2) * (theta_2 - math.sin(theta_2))
            Cyi = (4 * ro_joint / 3) * (math.sin(theta_2 / 2) ** 3) / (theta_2 - math.sin(theta_2))
            Ixci = Ixi - Ai * Cyi ** 2
            Ixi_prime = Ixci + Ai * (Cyi - x_prime) ** 2
            centroid_data.append(Ai)
            centroid_data.append(Cyi)

            I_below = round(
                math.pi * (OD ** 4 - OD_joint ** 4) / 64 + math.pi * (OD ** 2 - OD_joint ** 2) / 4 * x_prime ** 2 - (
                            Ixo_prime - Ixi_prime), 2)

            if I_above == I_below or I_above - I_below <= 0.01:
                break
            else:
                centroid_data = []

        I_reduced = 2 * I_below
        I_full = math.pi * (OD ** 4 - ID ** 4) / 64
        I_gross = math.pi * (OD_no_corrosion ** 4 - ID ** 4) / 64
        intact_stiffness_percentage = round(I_reduced / I_full * 100, 1)
        gross_stiffness_percentage = round(I_reduced / I_gross * 100, 1)

        pin_stress = limit_load / (math.pi * (OD_joint ** 2 - ID ** 2) / 4)

        area_compression = (ro ** 2 * math.acos(x_prime / ro) - (
                    x_prime * (2 * ro * (ro - x_prime) - (ro - x_prime) ** 2) ** 0.5)) - \
                           (ri ** 2 * math.acos(x_prime / ri) - (
                                       x_prime * (2 * ri * (ri - x_prime) - (ri - x_prime) ** 2) ** 0.5))

        area_tension = (math.pi * (OD ** 2 - OD_joint ** 2) / 4) - \
                       ((ro ** 2 * math.acos(x_prime / ro) - (
                                   x_prime * (2 * ro * (ro - x_prime) -
                                              (ro - x_prime) ** 2) ** 0.5)) -
                        (ro_joint ** 2 * math.acos(x_prime / ro_joint) - (
                                    x_prime * (2 * ro_joint * (ro_joint - x_prime) - (ro_joint - x_prime) ** 2) ** 0.5)))

        Cc = (centroid_data[0] * centroid_data[1] - centroid_data[2] * centroid_data[3]) / (
                    centroid_data[0] - centroid_data[2]) - x_prime
        A_missing = centroid_data[0] - centroid_data[4]
        y_missing = (centroid_data[0] * centroid_data[1] - centroid_data[4] * centroid_data[5]) / (
                    A_missing)
        At = math.pi * (OD ** 2 - OD_joint ** 2) / 4
        A_remaining = At - A_missing
        Ct = A_missing * y_missing / A_remaining + x_prime

        Mt = limit_load * Ct
        Mc = limit_load * Cc
        Mtotal = Mt + Mc
        Mmax = Yp * I_full / ro
        Mgross = Yp * I_gross / (OD_no_corrosion / 2)
        intact_moment_percentage = Mtotal / Mmax
        gross_moment_percentage = Mtotal / Mgross
        allowable_capacity = Mtotal / 12 / 1.67

    return Pi, Pfr, limit_load, limit_load_description, x_prime, theta_0, theta_1, theta_2, I_above, I_below, \
           I_reduced, I_full, intact_stiffness_percentage, pin_stress, area_compression, area_tension, Cc, Ct, Mc, Mt, \
           Mtotal, Mmax, intact_moment_percentage, allowable_capacity, I_gross, gross_stiffness_percentage, Mgross, \
           gross_moment_percentage, Ap, Ab, Pi_box, Pfr_box, image_check, A1_correction, A2_correction



