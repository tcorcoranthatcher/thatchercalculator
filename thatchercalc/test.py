import math

# Micropile Joint Bending Capacity #

# Casing format
# [name, L (in), h (in), D (in), α (°), ID (in), OD (in), OD @ tension area (in)]

casings = [['9 7/8"ɸ x 0.472', 1.75, 0.1218, 9.324, 30, 8.625, 9.715, 9.080]]
casing = casings[0]
a = 2.39
b = 0.59
psi = 14.35
Yp = 80
Up = 100
L = casing[1]
h = casing[2]
D = casing[3]
alpha = casing[4]
ID = casing[5]
OD = casing[6]
OD_joint = casing[7]
ro = OD/2
ri = ID/2
ro_joint = OD_joint/2

Ap = round((math.pi/4)*((D-h)**2-ID**2), 3)
Pi = round(Ap*((a*(2*h/D)**b*Up)/(0.5+(D/(2*L))*math.tan(math.radians(alpha-psi))) + Yp/(1+(D/(2*L))*math.tan(math.radians(alpha-psi)))), 2)
Pfr = round((Up*(math.pi*((D-2*h)**2-ID**2))/4), 2)

if Pi >= Pfr:
    limit_load = Pfr
else:
    limit_load = Pi

centroid_data = []

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
    print(x_prime, I_above-I_below, I_below-I_above)

    if I_above == I_below or I_above-I_below <= 0.01:
        break
    else:
        centroid_data = []

I_reduced = 2*I_below
I_full = math.pi*(OD**4-ID**4)/64
intact_stiffness_percentage = round(I_reduced/I_full*100, 1)

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

Mt = pin_stress*area_tension*Ct
Mc = pin_stress*area_tension*Cc
Mtotal = Mt + Mc
Mmax = Yp*I_full/ro

intact_moment_percentage = Mtotal/Mmax
allowable_capacity = Mtotal/12/1.67

print(intact_moment_percentage, allowable_capacity)

