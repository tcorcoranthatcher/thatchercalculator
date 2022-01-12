from django.http import HttpResponse
from django.shortcuts import render
from .Surcharge_Heights import surcharge_heights, passive_heights
from .Lateral_Pressures import Layer, active_pressures_output, passive_pressures_output, water_pressures_output, \
    active_pressures, passive_pressures, water_pressures, net_pressures, active_pressures_front,\
    passive_pressures_back, cant_pressures, active_pressures_front_output, passive_pressures_back_output, \
    water_around_toe, apparent_pressures, apparent_pressures_output
from .Pressure_Plot import braced_pressure_plot, surface_plot, cant_pressure_plot, multi_layer_pressure_plot, \
    strut_pressure_plot, ap_plot, water_plot
from bokeh.io import save
from .Braced import minimum_length, multiplier, maximum_moment, deflection_calc, multiplier_optimizer
from .Footings import footing_surcharge, combine_footings, incorporate_footings, text_output
from .sheet_database import sheet_database, beam_database
from .Train_Loading import train_loading, combine_trains
from .Cantilever import minimum_length_cantilever, maximum_moment_cantilever, multiplier_cantilever, \
    deflection_calc_cantilever, multiplier_cantilever_optimizer
from .Berms import berm_workpoints, berm_reduction
from .multilayer import two_layer_minimum_length, two_layer_maximum_moment, two_layer_multiplier, \
    two_layer_deflection_calc
from .three_layer import three_layer_minimum_length, three_layer_maximum_moment, three_layer_multiplier, \
    three_layer_deflection_calc
from.micropile_joint_bending_capacity import micropile_joint_bending_capacity as joint_capacity_function
from timeit import default_timer as timer
from savedcalcs.models import SavedCalc
import math
import itertools
import ast


def home(request):
    return render(request, 'home.html')


def cantilever(request):
    saved_calc_input = []
    saved_calc_load_check = int(request.GET['saved_calc_load_check'])
    if saved_calc_load_check == 1:
        saved_calc_input = request.GET['saved_calc_input']
        saved_calc_input = ast.literal_eval(saved_calc_input)
        saved_variables = []
        count = 0
        for variable in saved_calc_input:
            if variable == "":
                saved_variables.append([count, variable])
            else:
                saved_variables.append([count, float(variable)])
            count += 1
        saved_sheet_pile = sheet_database[int(saved_variables[297][1]) - 1][1]
        saved_soldier_pile = beam_database[int(saved_variables[298][1]) - 1][1]

        return render(request, 'cantilever.html', {'footing_1_type': saved_variables[0][1],
                                                   'footing_1_width': saved_variables[1][1],
                                                   'footing_1_distance': saved_variables[2][1],
                                                   'footing_1_elevation': saved_variables[3][1],
                                                   'footing_1_load': saved_variables[4][1],
                                                   'footing_1_spacing_1': saved_variables[5][1],
                                                   'footing_1_spacing_2': saved_variables[6][1],
                                                   'footing_2_type': saved_variables[7][1],
                                                   'footing_2_width': saved_variables[8][1],
                                                   'footing_2_distance': saved_variables[9][1],
                                                   'footing_2_elevation': saved_variables[10][1],
                                                   'footing_2_load': saved_variables[11][1],
                                                   'footing_2_spacing_1': saved_variables[12][1],
                                                   'footing_2_spacing_2': saved_variables[13][1],
                                                   'footing_3_type': saved_variables[14][1],
                                                   'footing_3_width': saved_variables[15][1],
                                                   'footing_3_distance': saved_variables[16][1],
                                                   'footing_3_elevation': saved_variables[17][1],
                                                   'footing_3_load': saved_variables[18][1],
                                                   'footing_3_spacing_1': saved_variables[19][1],
                                                   'footing_3_spacing_2': saved_variables[20][1],
                                                   'footing_4_type': saved_variables[21][1],
                                                   'footing_4_width': saved_variables[22][1],
                                                   'footing_4_distance': saved_variables[23][1],
                                                   'footing_4_elevation': saved_variables[24][1],
                                                   'footing_4_load': saved_variables[25][1],
                                                   'footing_4_spacing_1': saved_variables[26][1],
                                                   'footing_4_spacing_2': saved_variables[27][1],
                                                   'train_1_distance': saved_variables[28][1],
                                                   'train_1_load': saved_variables[29][1],
                                                   'train_1_tie_size': saved_variables[30][1],
                                                   'train_1_elevation': saved_variables[31][1],
                                                   'train_2_distance': saved_variables[32][1],
                                                   'train_2_load': saved_variables[33][1],
                                                   'train_2_tie_size': saved_variables[34][1],
                                                   'train_2_elevation': saved_variables[35][1],
                                                   'train_3_distance': saved_variables[36][1],
                                                   'train_3_load': saved_variables[37][1],
                                                   'train_3_tie_size': saved_variables[38][1],
                                                   'train_3_elevation': saved_variables[39][1],
                                                   'train_4_distance': saved_variables[40][1],
                                                   'train_4_load': saved_variables[41][1],
                                                   'train_4_tie_size': saved_variables[42][1],
                                                   'train_4_elevation': saved_variables[43][1],
                                                   'surface_side': saved_variables[44][1],
                                                   'point0x': saved_variables[45][1],
                                                   'point0y': saved_variables[46][1],
                                                   'point1x': saved_variables[47][1],
                                                   'point1y': saved_variables[48][1],
                                                   'point2x': saved_variables[49][1],
                                                   'point2y': saved_variables[50][1],
                                                   'point3x': saved_variables[51][1],
                                                   'point3y': saved_variables[52][1],
                                                   'point4x': saved_variables[53][1],
                                                   'point4y': saved_variables[54][1],
                                                   'point5x': saved_variables[55][1],
                                                   'point5y': saved_variables[56][1],
                                                   'point6x': saved_variables[57][1],
                                                   'point6y': saved_variables[58][1],
                                                   'point7x': saved_variables[59][1],
                                                   'point7y': saved_variables[60][1],
                                                   'point8x': saved_variables[61][1],
                                                   'point8y': saved_variables[62][1],
                                                   'point9x': saved_variables[63][1],
                                                   'point9y': saved_variables[64][1],
                                                   'point10x': saved_variables[65][1],
                                                   'point10y': saved_variables[66][1],
                                                   'point11x': saved_variables[67][1],
                                                   'point11y': saved_variables[68][1],
                                                   'point12x': saved_variables[69][1],
                                                   'point12y': saved_variables[70][1],
                                                   'point13x': saved_variables[71][1],
                                                   'point13y': saved_variables[72][1],
                                                   'berm0x': saved_variables[73][1],
                                                   'berm0y': saved_variables[74][1],
                                                   'berm1x': saved_variables[75][1],
                                                   'berm1y': saved_variables[76][1],
                                                   'berm2x': saved_variables[77][1],
                                                   'berm2y': saved_variables[78][1],
                                                   'berm3x': saved_variables[79][1],
                                                   'berm3y': saved_variables[80][1],
                                                   'berm4x': saved_variables[81][1],
                                                   'berm4y': saved_variables[82][1],
                                                   'berm5x': saved_variables[83][1],
                                                   'berm5y': saved_variables[84][1],
                                                   'berm6x': saved_variables[85][1],
                                                   'berm6y': saved_variables[86][1],
                                                   'berm7x': saved_variables[87][1],
                                                   'berm7y': saved_variables[88][1],
                                                   'berm8x': saved_variables[89][1],
                                                   'berm8y': saved_variables[90][1],
                                                   'berm9x': saved_variables[91][1],
                                                   'berm9y': saved_variables[92][1],
                                                   'berm10x': saved_variables[93][1],
                                                   'berm10y': saved_variables[94][1],
                                                   'berm11x': saved_variables[95][1],
                                                   'berm11y': saved_variables[96][1],
                                                   'berm12x': saved_variables[97][1],
                                                   'berm12y': saved_variables[98][1],
                                                   'berm13x': saved_variables[99][1],
                                                   'berm13y': saved_variables[100][1],
                                                   'onename': saved_variables[101][1],
                                                   'onetype': saved_variables[102][1],
                                                   'onegamma': saved_variables[103][1],
                                                   'onequ': saved_variables[104][1],
                                                   'oneka': saved_variables[105][1],
                                                   'onekp': saved_variables[106][1],
                                                   'onephi': saved_variables[107][1],
                                                   'twoname': saved_variables[108][1],
                                                   'twotype': saved_variables[109][1],
                                                   'twogamma': saved_variables[110][1],
                                                   'twoqu': saved_variables[111][1],
                                                   'twoka': saved_variables[112][1],
                                                   'twokp': saved_variables[113][1],
                                                   'twophi': saved_variables[114][1],
                                                   'threename': saved_variables[115][1],
                                                   'threetype': saved_variables[116][1],
                                                   'threegamma': saved_variables[117][1],
                                                   'threequ': saved_variables[118][1],
                                                   'threeka': saved_variables[119][1],
                                                   'threekp': saved_variables[120][1],
                                                   'threephi': saved_variables[121][1],
                                                   'fourname': saved_variables[122][1],
                                                   'fourtype': saved_variables[123][1],
                                                   'fourgamma': saved_variables[124][1],
                                                   'fourqu': saved_variables[125][1],
                                                   'fourka': saved_variables[126][1],
                                                   'fourkp': saved_variables[127][1],
                                                   'fourphi': saved_variables[128][1],
                                                   'fivename': saved_variables[129][1],
                                                   'fivetype': saved_variables[130][1],
                                                   'fivegamma': saved_variables[131][1],
                                                   'fivequ': saved_variables[132][1],
                                                   'fiveka': saved_variables[133][1],
                                                   'fivekp': saved_variables[134][1],
                                                   'fivephi': saved_variables[135][1],
                                                   'sixname': saved_variables[136][1],
                                                   'sixtype': saved_variables[137][1],
                                                   'sixgamma': saved_variables[138][1],
                                                   'sixqu': saved_variables[139][1],
                                                   'sixka': saved_variables[140][1],
                                                   'sixkp': saved_variables[141][1],
                                                   'sixphi': saved_variables[142][1],
                                                   'sevenname': saved_variables[143][1],
                                                   'seventype': saved_variables[144][1],
                                                   'sevengamma': saved_variables[145][1],
                                                   'sevenqu': saved_variables[146][1],
                                                   'sevenka': saved_variables[147][1],
                                                   'sevenkp': saved_variables[148][1],
                                                   'sevenphi': saved_variables[149][1],
                                                   'eightname': saved_variables[150][1],
                                                   'eighttype': saved_variables[151][1],
                                                   'eightgamma': saved_variables[152][1],
                                                   'eightqu': saved_variables[153][1],
                                                   'eightka': saved_variables[154][1],
                                                   'eightkp': saved_variables[155][1],
                                                   'eightphi': saved_variables[156][1],
                                                   'ninename': saved_variables[157][1],
                                                   'ninetype': saved_variables[158][1],
                                                   'ninegamma': saved_variables[159][1],
                                                   'ninequ': saved_variables[160][1],
                                                   'nineka': saved_variables[161][1],
                                                   'ninekp': saved_variables[162][1],
                                                   'ninephi': saved_variables[163][1],
                                                   'tenname': saved_variables[164][1],
                                                   'tentype': saved_variables[165][1],
                                                   'tengamma': saved_variables[166][1],
                                                   'tenqu': saved_variables[167][1],
                                                   'tenka': saved_variables[168][1],
                                                   'tenkp': saved_variables[169][1],
                                                   'tenphi': saved_variables[170][1],
                                                   'elevenname': saved_variables[171][1],
                                                   'eleventype': saved_variables[172][1],
                                                   'elevengamma': saved_variables[173][1],
                                                   'elevenqu': saved_variables[174][1],
                                                   'elevenka': saved_variables[175][1],
                                                   'elevenkp': saved_variables[176][1],
                                                   'elevenphi': saved_variables[177][1],
                                                   'twelvename': saved_variables[178][1],
                                                   'twelvetype': saved_variables[179][1],
                                                   'twelvegamma': saved_variables[180][1],
                                                   'twelvequ': saved_variables[181][1],
                                                   'twelveka': saved_variables[182][1],
                                                   'twelvekp': saved_variables[183][1],
                                                   'twelvephi': saved_variables[184][1],
                                                   'thirteenname': saved_variables[185][1],
                                                   'thirteentype': saved_variables[186][1],
                                                   'thirteengamma': saved_variables[187][1],
                                                   'thirteenqu': saved_variables[188][1],
                                                   'thirteenka': saved_variables[189][1],
                                                   'thirteenkp': saved_variables[190][1],
                                                   'thirteenphi': saved_variables[191][1],
                                                   'fourteenname': saved_variables[192][1],
                                                   'fourteentype': saved_variables[193][1],
                                                   'fourteengamma': saved_variables[194][1],
                                                   'fourteenqu': saved_variables[195][1],
                                                   'fourteenka': saved_variables[196][1],
                                                   'fourteenkp': saved_variables[197][1],
                                                   'fourteenphi': saved_variables[198][1],
                                                   'wp1': saved_variables[199][1],
                                                   'wp1_layer': saved_variables[200][1],
                                                   'wp1_layer_front': saved_variables[201][1],
                                                   'wp2': saved_variables[202][1],
                                                   'wp2_layer': saved_variables[203][1],
                                                   'wp2_layer_front': saved_variables[204][1],
                                                   'wp3': saved_variables[205][1],
                                                   'wp3_layer': saved_variables[206][1],
                                                   'wp3_layer_front': saved_variables[207][1],
                                                   'wp4': saved_variables[208][1],
                                                   'wp4_layer': saved_variables[209][1],
                                                   'wp4_layer_front': saved_variables[210][1],
                                                   'wp5': saved_variables[211][1],
                                                   'wp5_layer': saved_variables[212][1],
                                                   'wp5_layer_front': saved_variables[213][1],
                                                   'wp6': saved_variables[214][1],
                                                   'wp6_layer': saved_variables[215][1],
                                                   'wp6_layer_front': saved_variables[216][1],
                                                   'wp7': saved_variables[217][1],
                                                   'wp7_layer': saved_variables[218][1],
                                                   'wp7_layer_front': saved_variables[219][1],
                                                   'wp8': saved_variables[220][1],
                                                   'wp8_layer': saved_variables[221][1],
                                                   'wp8_layer_front': saved_variables[222][1],
                                                   'wp9': saved_variables[223][1],
                                                   'wp9_layer': saved_variables[224][1],
                                                   'wp9_layer_front': saved_variables[225][1],
                                                   'wp10': saved_variables[226][1],
                                                   'wp10_layer': saved_variables[227][1],
                                                   'wp10_layer_front': saved_variables[228][1],
                                                   'wp11': saved_variables[229][1],
                                                   'wp11_layer': saved_variables[230][1],
                                                   'wp11_layer_front': saved_variables[231][1],
                                                   'wp12': saved_variables[232][1],
                                                   'wp12_layer': saved_variables[233][1],
                                                   'wp12_layer_front': saved_variables[234][1],
                                                   'wp13': saved_variables[235][1],
                                                   'wp13_layer': saved_variables[236][1],
                                                   'wp13_layer_front': saved_variables[237][1],
                                                   'wp14': saved_variables[238][1],
                                                   'wp14_layer': saved_variables[239][1],
                                                   'wp14_layer_front': saved_variables[240][1],
                                                   'wp15': saved_variables[241][1],
                                                   'wp15_layer': saved_variables[242][1],
                                                   'wp15_layer_front': saved_variables[243][1],
                                                   'wp16': saved_variables[244][1],
                                                   'wp16_layer': saved_variables[245][1],
                                                   'wp16_layer_front': saved_variables[246][1],
                                                   'wp17': saved_variables[247][1],
                                                   'wp17_layer': saved_variables[248][1],
                                                   'wp17_layer_front': saved_variables[249][1],
                                                   'wp18': saved_variables[250][1],
                                                   'wp18_layer': saved_variables[251][1],
                                                   'wp18_layer_front': saved_variables[252][1],
                                                   'wp19': saved_variables[253][1],
                                                   'wp19_layer': saved_variables[254][1],
                                                   'wp19_layer_front': saved_variables[255][1],
                                                   'wp20': saved_variables[256][1],
                                                   'wp20_layer': saved_variables[257][1],
                                                   'wp20_layer_front': saved_variables[258][1],
                                                   'wp21': saved_variables[259][1],
                                                   'wp21_layer': saved_variables[260][1],
                                                   'wp21_layer_front': saved_variables[261][1],
                                                   'wp22': saved_variables[262][1],
                                                   'wp22_layer': saved_variables[263][1],
                                                   'wp22_layer_front': saved_variables[264][1],
                                                   'wp23': saved_variables[265][1],
                                                   'wp23_layer': saved_variables[266][1],
                                                   'wp23_layer_front': saved_variables[267][1],
                                                   'wp24': saved_variables[268][1],
                                                   'wp24_layer': saved_variables[269][1],
                                                   'wp24_layer_front': saved_variables[270][1],
                                                   'wp25': saved_variables[271][1],
                                                   'wp25_layer': saved_variables[272][1],
                                                   'wp25_layer_front': saved_variables[273][1],
                                                   'wp26': saved_variables[274][1],
                                                   'wp26_layer': saved_variables[275][1],
                                                   'wp26_layer_front': saved_variables[276][1],
                                                   'wp27': saved_variables[277][1],
                                                   'wp27_layer': saved_variables[278][1],
                                                   'wp27_layer_front': saved_variables[279][1],
                                                   'wp28': saved_variables[280][1],
                                                   'wp28_layer': saved_variables[281][1],
                                                   'wp28_layer_front': saved_variables[282][1],
                                                   'wp29': saved_variables[283][1],
                                                   'wp29_layer': saved_variables[284][1],
                                                   'wp29_layer_front': saved_variables[285][1],
                                                   'wp30': saved_variables[286][1],
                                                   'wp30_layer': saved_variables[287][1],
                                                   'wp30_layer_front': saved_variables[288][1],
                                                   'surcharge_unit_weight': saved_variables[289][1],
                                                   'min_surcharge_height': saved_variables[290][1],
                                                   'angle': saved_variables[291][1],
                                                   'angle_change_elev': saved_variables[292][1],
                                                   'water_elev': saved_variables[293][1],
                                                   'cut_elev': saved_variables[294][1],
                                                   'total_weights': saved_variables[295][1],
                                                   'scale_factor': saved_variables[296][1],
                                                   'sheet_type': saved_variables[297][1],
                                                   'beam_type': saved_variables[298][1],
                                                   'water_cut_elev': saved_variables[299][1],
                                                   'top_sheet': saved_variables[300][1],
                                                   'beam_spacing': saved_variables[301][1],
                                                   'beam_size_override': saved_variables[302][1],
                                                   'beam_override': saved_variables[303][1],
                                                   'beam_modulus_override': saved_variables[304][1],
                                                   'beam_inertia_override': saved_variables[305][1],
                                                   'ers_type': saved_variables[306][1],
                                                   'soldier_beam_method': saved_variables[307][1],
                                                   'supplied_length': saved_variables[308][1],
                                                   'wat_check': saved_variables[309][1],
                                                   'angle_change_type': saved_variables[310][1],
                                                   'surface_elev': saved_variables[311][1],
                                                   'saved_sheet_pile': saved_sheet_pile,
                                                   'saved_soldier_pile': saved_soldier_pile}

                      )
    return render(request, 'cantilever.html')


def braced(request):
    saved_calc_input = []
    saved_calc_load_check = int(request.GET['saved_calc_load_check'])
    if saved_calc_load_check == 1:
        saved_calc_input = request.GET['saved_calc_input']
        saved_calc_input = ast.literal_eval(saved_calc_input)
        saved_variables = []
        count = 0
        for variable in saved_calc_input:
            if variable == "":
                saved_variables.append([count, variable])
            else:
                saved_variables.append([count, float(variable)])
            count += 1
        saved_sheet_pile = sheet_database[int(saved_variables[328][1])-1][1]
        saved_soldier_pile = beam_database[int(saved_variables[329][1])-1][1]

        return render(request, 'braced.html', {'footing_1_type': saved_variables[0][1],
                                               'footing_1_width': saved_variables[1][1],
                                               'footing_1_distance': saved_variables[2][1],
                                               'footing_1_elevation': saved_variables[3][1],
                                               'footing_1_load': saved_variables[4][1],
                                               'footing_1_spacing_1': saved_variables[5][1],
                                               'footing_1_spacing_2': saved_variables[6][1],
                                               'footing_2_type': saved_variables[7][1],
                                               'footing_2_width': saved_variables[8][1],
                                               'footing_2_distance': saved_variables[9][1],
                                               'footing_2_elevation': saved_variables[10][1],
                                               'footing_2_load': saved_variables[11][1],
                                               'footing_2_spacing_1': saved_variables[12][1],
                                               'footing_2_spacing_2': saved_variables[13][1],
                                               'footing_3_type': saved_variables[14][1],
                                               'footing_3_width': saved_variables[15][1],
                                               'footing_3_distance': saved_variables[16][1],
                                               'footing_3_elevation': saved_variables[17][1],
                                               'footing_3_load': saved_variables[18][1],
                                               'footing_3_spacing_1': saved_variables[19][1],
                                               'footing_3_spacing_2': saved_variables[20][1],
                                               'footing_4_type': saved_variables[21][1],
                                               'footing_4_width': saved_variables[22][1],
                                               'footing_4_distance': saved_variables[23][1],
                                               'footing_4_elevation': saved_variables[24][1],
                                               'footing_4_load': saved_variables[25][1],
                                               'footing_4_spacing_1': saved_variables[26][1],
                                               'footing_4_spacing_2': saved_variables[27][1],
                                               'train_1_distance': saved_variables[28][1],
                                               'train_1_load': saved_variables[29][1],
                                               'train_1_tie_size': saved_variables[30][1],
                                               'train_1_elevation': saved_variables[31][1],
                                               'train_2_distance': saved_variables[32][1],
                                               'train_2_load': saved_variables[33][1],
                                               'train_2_tie_size': saved_variables[34][1],
                                               'train_2_elevation': saved_variables[35][1],
                                               'train_3_distance': saved_variables[36][1],
                                               'train_3_load': saved_variables[37][1],
                                               'train_3_tie_size': saved_variables[38][1],
                                               'train_3_elevation': saved_variables[39][1],
                                               'train_4_distance': saved_variables[40][1],
                                               'train_4_load': saved_variables[41][1],
                                               'train_4_tie_size': saved_variables[42][1],
                                               'train_4_elevation': saved_variables[43][1],
                                               'surface_side': saved_variables[44][1],
                                               'point0x': saved_variables[45][1],
                                               'point0y': saved_variables[46][1],
                                               'point1x': saved_variables[47][1],
                                               'point1y': saved_variables[48][1],
                                               'point2x': saved_variables[49][1],
                                               'point2y': saved_variables[50][1],
                                               'point3x': saved_variables[51][1],
                                               'point3y': saved_variables[52][1],
                                               'point4x': saved_variables[53][1],
                                               'point4y': saved_variables[54][1],
                                               'point5x': saved_variables[55][1],
                                               'point5y': saved_variables[56][1],
                                               'point6x': saved_variables[57][1],
                                               'point6y': saved_variables[58][1],
                                               'point7x': saved_variables[59][1],
                                               'point7y': saved_variables[60][1],
                                               'point8x': saved_variables[61][1],
                                               'point8y': saved_variables[62][1],
                                               'point9x': saved_variables[63][1],
                                               'point9y': saved_variables[64][1],
                                               'point10x': saved_variables[65][1],
                                               'point10y': saved_variables[66][1],
                                               'point11x': saved_variables[67][1],
                                               'point11y': saved_variables[68][1],
                                               'point12x': saved_variables[69][1],
                                               'point12y': saved_variables[70][1],
                                               'point13x': saved_variables[71][1],
                                               'point13y': saved_variables[72][1],
                                               'berm0x': saved_variables[73][1],
                                               'berm0y': saved_variables[74][1],
                                               'berm1x': saved_variables[75][1],
                                               'berm1y': saved_variables[76][1],
                                               'berm2x': saved_variables[77][1],
                                               'berm2y': saved_variables[78][1],
                                               'berm3x': saved_variables[79][1],
                                               'berm3y': saved_variables[80][1],
                                               'berm4x': saved_variables[81][1],
                                               'berm4y': saved_variables[82][1],
                                               'berm5x': saved_variables[83][1],
                                               'berm5y': saved_variables[84][1],
                                               'berm6x': saved_variables[85][1],
                                               'berm6y': saved_variables[86][1],
                                               'berm7x': saved_variables[87][1],
                                               'berm7y': saved_variables[88][1],
                                               'berm8x': saved_variables[89][1],
                                               'berm8y': saved_variables[90][1],
                                               'berm9x': saved_variables[91][1],
                                               'berm9y': saved_variables[92][1],
                                               'berm10x': saved_variables[93][1],
                                               'berm10y': saved_variables[94][1],
                                               'berm11x': saved_variables[95][1],
                                               'berm11y': saved_variables[96][1],
                                               'berm12x': saved_variables[97][1],
                                               'berm12y': saved_variables[98][1],
                                               'berm13x': saved_variables[99][1],
                                               'berm13y': saved_variables[100][1],
                                               'onename': saved_variables[101][1],
                                               'onetype': saved_variables[102][1],
                                               'onegamma': saved_variables[103][1],
                                               'onequ': saved_variables[104][1],
                                               'oneka': saved_variables[105][1],
                                               'onekp': saved_variables[106][1],
                                               'onephi': saved_variables[107][1],
                                               'twoname': saved_variables[108][1],
                                               'twotype': saved_variables[109][1],
                                               'twogamma': saved_variables[110][1],
                                               'twoqu': saved_variables[111][1],
                                               'twoka': saved_variables[112][1],
                                               'twokp': saved_variables[113][1],
                                               'twophi': saved_variables[114][1],
                                               'threename': saved_variables[115][1],
                                               'threetype': saved_variables[116][1],
                                               'threegamma': saved_variables[117][1],
                                               'threequ': saved_variables[118][1],
                                               'threeka': saved_variables[119][1],
                                               'threekp': saved_variables[120][1],
                                               'threephi': saved_variables[121][1],
                                               'fourname': saved_variables[122][1],
                                               'fourtype': saved_variables[123][1],
                                               'fourgamma': saved_variables[124][1],
                                               'fourqu': saved_variables[125][1],
                                               'fourka': saved_variables[126][1],
                                               'fourkp': saved_variables[127][1],
                                               'fourphi': saved_variables[128][1],
                                               'fivename': saved_variables[129][1],
                                               'fivetype': saved_variables[130][1],
                                               'fivegamma': saved_variables[131][1],
                                               'fivequ': saved_variables[132][1],
                                               'fiveka': saved_variables[133][1],
                                               'fivekp': saved_variables[134][1],
                                               'fivephi': saved_variables[135][1],
                                               'sixname': saved_variables[136][1],
                                               'sixtype': saved_variables[137][1],
                                               'sixgamma': saved_variables[138][1],
                                               'sixqu': saved_variables[139][1],
                                               'sixka': saved_variables[140][1],
                                               'sixkp': saved_variables[141][1],
                                               'sixphi': saved_variables[142][1],
                                               'sevenname': saved_variables[143][1],
                                               'seventype': saved_variables[144][1],
                                               'sevengamma': saved_variables[145][1],
                                               'sevenqu': saved_variables[146][1],
                                               'sevenka': saved_variables[147][1],
                                               'sevenkp': saved_variables[148][1],
                                               'sevenphi': saved_variables[149][1],
                                               'eightname': saved_variables[150][1],
                                               'eighttype': saved_variables[151][1],
                                               'eightgamma': saved_variables[152][1],
                                               'eightqu': saved_variables[153][1],
                                               'eightka': saved_variables[154][1],
                                               'eightkp': saved_variables[155][1],
                                               'eightphi': saved_variables[156][1],
                                               'ninename': saved_variables[157][1],
                                               'ninetype': saved_variables[158][1],
                                               'ninegamma': saved_variables[159][1],
                                               'ninequ': saved_variables[160][1],
                                               'nineka': saved_variables[161][1],
                                               'ninekp': saved_variables[162][1],
                                               'ninephi': saved_variables[163][1],
                                               'tenname': saved_variables[164][1],
                                               'tentype': saved_variables[165][1],
                                               'tengamma': saved_variables[166][1],
                                               'tenqu': saved_variables[167][1],
                                               'tenka': saved_variables[168][1],
                                               'tenkp': saved_variables[169][1],
                                               'tenphi': saved_variables[170][1],
                                               'elevenname': saved_variables[171][1],
                                               'eleventype': saved_variables[172][1],
                                               'elevengamma': saved_variables[173][1],
                                               'elevenqu': saved_variables[174][1],
                                               'elevenka': saved_variables[175][1],
                                               'elevenkp': saved_variables[176][1],
                                               'elevenphi': saved_variables[177][1],
                                               'twelvename': saved_variables[178][1],
                                               'twelvetype': saved_variables[179][1],
                                               'twelvegamma': saved_variables[180][1],
                                               'twelvequ': saved_variables[181][1],
                                               'twelveka': saved_variables[182][1],
                                               'twelvekp': saved_variables[183][1],
                                               'twelvephi': saved_variables[184][1],
                                               'thirteenname': saved_variables[185][1],
                                               'thirteentype': saved_variables[186][1],
                                               'thirteengamma': saved_variables[187][1],
                                               'thirteenqu': saved_variables[188][1],
                                               'thirteenka': saved_variables[189][1],
                                               'thirteenkp': saved_variables[190][1],
                                               'thirteenphi': saved_variables[191][1],
                                               'fourteenname': saved_variables[192][1],
                                               'fourteentype': saved_variables[193][1],
                                               'fourteengamma': saved_variables[194][1],
                                               'fourteenqu': saved_variables[195][1],
                                               'fourteenka': saved_variables[196][1],
                                               'fourteenkp': saved_variables[197][1],
                                               'fourteenphi': saved_variables[198][1],
                                               'wp1': saved_variables[199][1],
                                               'wp1_layer': saved_variables[200][1],
                                               'wp1_layer_front': saved_variables[201][1],
                                               'wp2': saved_variables[202][1],
                                               'wp2_layer': saved_variables[203][1],
                                               'wp2_layer_front': saved_variables[204][1],
                                               'wp3': saved_variables[205][1],
                                               'wp3_layer': saved_variables[206][1],
                                               'wp3_layer_front': saved_variables[207][1],
                                               'wp4': saved_variables[208][1],
                                               'wp4_layer': saved_variables[209][1],
                                               'wp4_layer_front': saved_variables[210][1],
                                               'wp5': saved_variables[211][1],
                                               'wp5_layer': saved_variables[212][1],
                                               'wp5_layer_front': saved_variables[213][1],
                                               'wp6': saved_variables[214][1],
                                               'wp6_layer': saved_variables[215][1],
                                               'wp6_layer_front': saved_variables[216][1],
                                               'wp7': saved_variables[217][1],
                                               'wp7_layer': saved_variables[218][1],
                                               'wp7_layer_front': saved_variables[219][1],
                                               'wp8': saved_variables[220][1],
                                               'wp8_layer': saved_variables[221][1],
                                               'wp8_layer_front': saved_variables[222][1],
                                               'wp9': saved_variables[223][1],
                                               'wp9_layer': saved_variables[224][1],
                                               'wp9_layer_front': saved_variables[225][1],
                                               'wp10': saved_variables[226][1],
                                               'wp10_layer': saved_variables[227][1],
                                               'wp10_layer_front': saved_variables[228][1],
                                               'wp11': saved_variables[229][1],
                                               'wp11_layer': saved_variables[230][1],
                                               'wp11_layer_front': saved_variables[231][1],
                                               'wp12': saved_variables[232][1],
                                               'wp12_layer': saved_variables[233][1],
                                               'wp12_layer_front': saved_variables[234][1],
                                               'wp13': saved_variables[235][1],
                                               'wp13_layer': saved_variables[236][1],
                                               'wp13_layer_front': saved_variables[237][1],
                                               'wp14': saved_variables[238][1],
                                               'wp14_layer': saved_variables[239][1],
                                               'wp14_layer_front': saved_variables[240][1],
                                               'wp15': saved_variables[241][1],
                                               'wp15_layer': saved_variables[242][1],
                                               'wp15_layer_front': saved_variables[243][1],
                                               'wp16': saved_variables[244][1],
                                               'wp16_layer': saved_variables[245][1],
                                               'wp16_layer_front': saved_variables[246][1],
                                               'wp17': saved_variables[247][1],
                                               'wp17_layer': saved_variables[248][1],
                                               'wp17_layer_front': saved_variables[249][1],
                                               'wp18': saved_variables[250][1],
                                               'wp18_layer': saved_variables[251][1],
                                               'wp18_layer_front': saved_variables[252][1],
                                               'wp19': saved_variables[253][1],
                                               'wp19_layer': saved_variables[254][1],
                                               'wp19_layer_front': saved_variables[255][1],
                                               'wp20': saved_variables[256][1],
                                               'wp20_layer': saved_variables[257][1],
                                               'wp20_layer_front': saved_variables[258][1],
                                               'wp21': saved_variables[259][1],
                                               'wp21_layer': saved_variables[260][1],
                                               'wp21_layer_front': saved_variables[261][1],
                                               'wp22': saved_variables[262][1],
                                               'wp22_layer': saved_variables[263][1],
                                               'wp22_layer_front': saved_variables[264][1],
                                               'wp23': saved_variables[265][1],
                                               'wp23_layer': saved_variables[266][1],
                                               'wp23_layer_front': saved_variables[267][1],
                                               'wp24': saved_variables[268][1],
                                               'wp24_layer': saved_variables[269][1],
                                               'wp24_layer_front': saved_variables[270][1],
                                               'wp25': saved_variables[271][1],
                                               'wp25_layer': saved_variables[272][1],
                                               'wp25_layer_front': saved_variables[273][1],
                                               'wp26': saved_variables[274][1],
                                               'wp26_layer': saved_variables[275][1],
                                               'wp26_layer_front': saved_variables[276][1],
                                               'wp27': saved_variables[277][1],
                                               'wp27_layer': saved_variables[278][1],
                                               'wp27_layer_front': saved_variables[279][1],
                                               'wp28': saved_variables[280][1],
                                               'wp28_layer': saved_variables[281][1],
                                               'wp28_layer_front': saved_variables[282][1],
                                               'wp29': saved_variables[283][1],
                                               'wp29_layer': saved_variables[284][1],
                                               'wp29_layer_front': saved_variables[285][1],
                                               'wp30': saved_variables[286][1],
                                               'wp30_layer': saved_variables[287][1],
                                               'wp30_layer_front': saved_variables[288][1],
                                               'wp31': saved_variables[289][1],
                                               'wp31_layer': saved_variables[290][1],
                                               'wp31_layer_front': saved_variables[291][1],
                                               'wp32': saved_variables[292][1],
                                               'wp32_layer': saved_variables[293][1],
                                               'wp32_layer_front': saved_variables[294][1],
                                               'wp33': saved_variables[295][1],
                                               'wp33_layer': saved_variables[296][1],
                                               'wp33_layer_front': saved_variables[297][1],
                                               'wp34': saved_variables[298][1],
                                               'wp34_layer': saved_variables[299][1],
                                               'wp34_layer_front': saved_variables[300][1],
                                               'wp35': saved_variables[301][1],
                                               'wp35_layer': saved_variables[302][1],
                                               'wp35_layer_front': saved_variables[303][1],
                                               'wp36': saved_variables[304][1],
                                               'wp36_layer': saved_variables[305][1],
                                               'wp36_layer_front': saved_variables[306][1],
                                               'wp37': saved_variables[307][1],
                                               'wp37_layer': saved_variables[308][1],
                                               'wp37_layer_front': saved_variables[309][1],
                                               'wp38': saved_variables[310][1],
                                               'wp38_layer': saved_variables[311][1],
                                               'wp38_layer_front': saved_variables[312][1],
                                               'wp39': saved_variables[313][1],
                                               'wp39_layer': saved_variables[314][1],
                                               'wp39_layer_front': saved_variables[315][1],
                                               'wp40': saved_variables[316][1],
                                               'wp40_layer': saved_variables[317][1],
                                               'wp40_layer_front': saved_variables[318][1],
                                               'surcharge_unit_weight': saved_variables[319][1],
                                               'min_surcharge_height': saved_variables[320][1],
                                               'angle': saved_variables[321][1],
                                               'angle_change_elev': saved_variables[322][1],
                                               'water_elev': saved_variables[323][1],
                                               'cut_elev': saved_variables[324][1],
                                               'total_weights': saved_variables[325][1],
                                               'brace_elev': saved_variables[326][1],
                                               'scale_factor': saved_variables[327][1],
                                               'sheet_type': saved_variables[328][1],
                                               'beam_type': saved_variables[329][1],
                                               'water_cut_elev': saved_variables[330][1],
                                               'top_sheet': saved_variables[331][1],
                                               'beam_spacing': saved_variables[332][1],
                                               'beam_size_override': saved_variables[333][1],
                                               'beam_override': saved_variables[334][1],
                                               'beam_modulus_override': saved_variables[335][1],
                                               'beam_inertia_override': saved_variables[336][1],
                                               'ers_type': saved_variables[337][1],
                                               'soldier_beam_method': saved_variables[338][1],
                                               'supplied_length': saved_variables[339][1],
                                               'wat_check': saved_variables[340][1],
                                               'angle_change_type': saved_variables[341][1],
                                               'saved_sheet_pile': saved_sheet_pile,
                                               'saved_soldier_pile': saved_soldier_pile}
                      )
    return render(request, 'braced.html')


def multilayer(request):
    saved_calc_input = []
    saved_calc_load_check = int(request.GET['saved_calc_load_check'])
    if saved_calc_load_check == 1:
        saved_calc_input = request.GET['saved_calc_input']
        saved_calc_input = ast.literal_eval(saved_calc_input)
        saved_variables = []
        count = 0
        for variable in saved_calc_input:
            if variable == "":
                saved_variables.append([count, variable])
            else:
                saved_variables.append([count, float(variable)])
            count += 1
            print(count, variable)
        saved_sheet_pile = sheet_database[int(saved_variables[373][1]) - 1][1]
        saved_soldier_pile = beam_database[int(saved_variables[374][1]) - 1][1]

        return render(request, 'multilayer.html', {'footing_1_type': saved_variables[0][1],
                                                   'footing_1_width': saved_variables[1][1],
                                                   'footing_1_distance': saved_variables[2][1],
                                                   'footing_1_elevation': saved_variables[3][1],
                                                   'footing_1_load': saved_variables[4][1],
                                                   'footing_1_spacing_1': saved_variables[5][1],
                                                   'footing_1_spacing_2': saved_variables[6][1],
                                                   'footing_2_type': saved_variables[7][1],
                                                   'footing_2_width': saved_variables[8][1],
                                                   'footing_2_distance': saved_variables[9][1],
                                                   'footing_2_elevation': saved_variables[10][1],
                                                   'footing_2_load': saved_variables[11][1],
                                                   'footing_2_spacing_1': saved_variables[12][1],
                                                   'footing_2_spacing_2': saved_variables[13][1],
                                                   'footing_3_type': saved_variables[14][1],
                                                   'footing_3_width': saved_variables[15][1],
                                                   'footing_3_distance': saved_variables[16][1],
                                                   'footing_3_elevation': saved_variables[17][1],
                                                   'footing_3_load': saved_variables[18][1],
                                                   'footing_3_spacing_1': saved_variables[19][1],
                                                   'footing_3_spacing_2': saved_variables[20][1],
                                                   'footing_4_type': saved_variables[21][1],
                                                   'footing_4_width': saved_variables[22][1],
                                                   'footing_4_distance': saved_variables[23][1],
                                                   'footing_4_elevation': saved_variables[24][1],
                                                   'footing_4_load': saved_variables[25][1],
                                                   'footing_4_spacing_1': saved_variables[26][1],
                                                   'footing_4_spacing_2': saved_variables[27][1],
                                                   'train_1_distance': saved_variables[28][1],
                                                   'train_1_load': saved_variables[29][1],
                                                   'train_1_tie_size': saved_variables[30][1],
                                                   'train_1_elevation': saved_variables[31][1],
                                                   'train_2_distance': saved_variables[32][1],
                                                   'train_2_load': saved_variables[33][1],
                                                   'train_2_tie_size': saved_variables[34][1],
                                                   'train_2_elevation': saved_variables[35][1],
                                                   'train_3_distance': saved_variables[36][1],
                                                   'train_3_load': saved_variables[37][1],
                                                   'train_3_tie_size': saved_variables[38][1],
                                                   'train_3_elevation': saved_variables[39][1],
                                                   'train_4_distance': saved_variables[40][1],
                                                   'train_4_load': saved_variables[41][1],
                                                   'train_4_tie_size': saved_variables[42][1],
                                                   'train_4_elevation': saved_variables[43][1],
                                                   'surface_side': saved_variables[44][1],
                                                   'point0x': saved_variables[45][1],
                                                   'point0y': saved_variables[46][1],
                                                   'point1x': saved_variables[47][1],
                                                   'point1y': saved_variables[48][1],
                                                   'point2x': saved_variables[49][1],
                                                   'point2y': saved_variables[50][1],
                                                   'point3x': saved_variables[51][1],
                                                   'point3y': saved_variables[52][1],
                                                   'point4x': saved_variables[53][1],
                                                   'point4y': saved_variables[54][1],
                                                   'point5x': saved_variables[55][1],
                                                   'point5y': saved_variables[56][1],
                                                   'point6x': saved_variables[57][1],
                                                   'point6y': saved_variables[58][1],
                                                   'point7x': saved_variables[59][1],
                                                   'point7y': saved_variables[60][1],
                                                   'point8x': saved_variables[61][1],
                                                   'point8y': saved_variables[62][1],
                                                   'point9x': saved_variables[63][1],
                                                   'point9y': saved_variables[64][1],
                                                   'point10x': saved_variables[65][1],
                                                   'point10y': saved_variables[66][1],
                                                   'point11x': saved_variables[67][1],
                                                   'point11y': saved_variables[68][1],
                                                   'point12x': saved_variables[69][1],
                                                   'point12y': saved_variables[70][1],
                                                   'point13x': saved_variables[71][1],
                                                   'point13y': saved_variables[72][1],
                                                   'berm0x': saved_variables[73][1],
                                                   'berm0y': saved_variables[74][1],
                                                   'berm1x': saved_variables[75][1],
                                                   'berm1y': saved_variables[76][1],
                                                   'berm2x': saved_variables[77][1],
                                                   'berm2y': saved_variables[78][1],
                                                   'berm3x': saved_variables[79][1],
                                                   'berm3y': saved_variables[80][1],
                                                   'berm4x': saved_variables[81][1],
                                                   'berm4y': saved_variables[82][1],
                                                   'berm5x': saved_variables[83][1],
                                                   'berm5y': saved_variables[84][1],
                                                   'berm6x': saved_variables[85][1],
                                                   'berm6y': saved_variables[86][1],
                                                   'berm7x': saved_variables[87][1],
                                                   'berm7y': saved_variables[88][1],
                                                   'berm8x': saved_variables[89][1],
                                                   'berm8y': saved_variables[90][1],
                                                   'berm9x': saved_variables[91][1],
                                                   'berm9y': saved_variables[92][1],
                                                   'berm10x': saved_variables[93][1],
                                                   'berm10y': saved_variables[94][1],
                                                   'berm11x': saved_variables[95][1],
                                                   'berm11y': saved_variables[96][1],
                                                   'berm12x': saved_variables[97][1],
                                                   'berm12y': saved_variables[98][1],
                                                   'berm13x': saved_variables[99][1],
                                                   'berm13y': saved_variables[100][1],
                                                   'onename': saved_variables[101][1],
                                                   'onetype': saved_variables[102][1],
                                                   'onegamma': saved_variables[103][1],
                                                   'onequ': saved_variables[104][1],
                                                   'oneka': saved_variables[105][1], 'onekp': saved_variables[106][1],
                                                   'onephi': saved_variables[107][1],
                                                   'twoname': saved_variables[108][1],
                                                   'twotype': saved_variables[109][1],
                                                   'twogamma': saved_variables[110][1],
                                                   'twoqu': saved_variables[111][1],
                                                   'twoka': saved_variables[112][1], 'twokp': saved_variables[113][1],
                                                   'twophi': saved_variables[114][1],
                                                   'threename': saved_variables[115][1],
                                                   'threetype': saved_variables[116][1],
                                                   'threegamma': saved_variables[117][1],
                                                   'threequ': saved_variables[118][1],
                                                   'threeka': saved_variables[119][1],
                                                   'threekp': saved_variables[120][1],
                                                   'threephi': saved_variables[121][1],
                                                   'fourname': saved_variables[122][1],
                                                   'fourtype': saved_variables[123][1],
                                                   'fourgamma': saved_variables[124][1],
                                                   'fourqu': saved_variables[125][1],
                                                   'fourka': saved_variables[126][1], 'fourkp': saved_variables[127][1],
                                                   'fourphi': saved_variables[128][1],
                                                   'fivename': saved_variables[129][1],
                                                   'fivetype': saved_variables[130][1],
                                                   'fivegamma': saved_variables[131][1],
                                                   'fivequ': saved_variables[132][1],
                                                   'fiveka': saved_variables[133][1], 'fivekp': saved_variables[134][1],
                                                   'fivephi': saved_variables[135][1],
                                                   'sixname': saved_variables[136][1],
                                                   'sixtype': saved_variables[137][1],
                                                   'sixgamma': saved_variables[138][1],
                                                   'sixqu': saved_variables[139][1],
                                                   'sixka': saved_variables[140][1], 'sixkp': saved_variables[141][1],
                                                   'sixphi': saved_variables[142][1],
                                                   'sevenname': saved_variables[143][1],
                                                   'seventype': saved_variables[144][1],
                                                   'sevengamma': saved_variables[145][1],
                                                   'sevenqu': saved_variables[146][1],
                                                   'sevenka': saved_variables[147][1],
                                                   'sevenkp': saved_variables[148][1],
                                                   'sevenphi': saved_variables[149][1],
                                                   'eightname': saved_variables[150][1],
                                                   'eighttype': saved_variables[151][1],
                                                   'eightgamma': saved_variables[152][1],
                                                   'eightqu': saved_variables[153][1],
                                                   'eightka': saved_variables[154][1],
                                                   'eightkp': saved_variables[155][1],
                                                   'eightphi': saved_variables[156][1],
                                                   'ninename': saved_variables[157][1],
                                                   'ninetype': saved_variables[158][1],
                                                   'ninegamma': saved_variables[159][1],
                                                   'ninequ': saved_variables[160][1],
                                                   'nineka': saved_variables[161][1], 'ninekp': saved_variables[162][1],
                                                   'ninephi': saved_variables[163][1],
                                                   'tenname': saved_variables[164][1],
                                                   'tentype': saved_variables[165][1],
                                                   'tengamma': saved_variables[166][1],
                                                   'tenqu': saved_variables[167][1], 'tenka': saved_variables[168][1],
                                                   'tenkp': saved_variables[169][1], 'tenphi': saved_variables[170][1],
                                                   'elevenname': saved_variables[171][1],
                                                   'eleventype': saved_variables[172][1],
                                                   'elevengamma': saved_variables[173][1],
                                                   'elevenqu': saved_variables[174][1],
                                                   'elevenka': saved_variables[175][1],
                                                   'elevenkp': saved_variables[176][1],
                                                   'elevenphi': saved_variables[177][1],
                                                   'twelvename': saved_variables[178][1],
                                                   'twelvetype': saved_variables[179][1],
                                                   'twelvegamma': saved_variables[180][1],
                                                   'twelvequ': saved_variables[181][1],
                                                   'twelveka': saved_variables[182][1],
                                                   'twelvekp': saved_variables[183][1],
                                                   'twelvephi': saved_variables[184][1],
                                                   'thirteenname': saved_variables[185][1],
                                                   'thirteentype': saved_variables[186][1],
                                                   'thirteengamma': saved_variables[187][1],
                                                   'thirteenqu': saved_variables[188][1],
                                                   'thirteenka': saved_variables[189][1],
                                                   'thirteenkp': saved_variables[190][1],
                                                   'fourteenphi': saved_variables[191][1],
                                                   'fourteenname': saved_variables[192][1],
                                                   'fourteentype': saved_variables[193][1],
                                                   'fourteengamma': saved_variables[194][1],
                                                   'fourteenqu': saved_variables[195][1],
                                                   'fourteenka': saved_variables[196][1],
                                                   'fourteenkp': saved_variables[197][1],
                                                   'fifteenphi': saved_variables[198][1],
                                                   'fifteenname': saved_variables[199][1],
                                                   'fifteentype': saved_variables[200][1],
                                                   'fifteengamma': saved_variables[201][1],
                                                   'fifteenqu': saved_variables[202][1],
                                                   'fifteenka': saved_variables[203][1],
                                                   'fifteenkp': saved_variables[204][1],
                                                   'sixteenphi': saved_variables[205][1],
                                                   'sixteenname': saved_variables[206][1],
                                                   'sixteentype': saved_variables[207][1],
                                                   'sixteengamma': saved_variables[208][1],
                                                   'sixteenqu': saved_variables[209][1],
                                                   'sixteenka': saved_variables[210][1],
                                                   'sixteenkp': saved_variables[211][1],
                                                   'seventeenphi': saved_variables[212][1],
                                                   'seventeenname': saved_variables[213][1],
                                                   'seventeentype': saved_variables[214][1],
                                                   'seventeengamma': saved_variables[215][1],
                                                   'seventeenqu': saved_variables[216][1],
                                                   'seventeenka': saved_variables[217][1],
                                                   'seventeenkp': saved_variables[218][1],
                                                   'eighteenphi': saved_variables[219][1],
                                                   'eighteenname': saved_variables[220][1],
                                                   'eighteentype': saved_variables[221][1],
                                                   'eighteengamma': saved_variables[222][1],
                                                   'eighteenqu': saved_variables[223][1],
                                                   'eighteenka': saved_variables[224][1],
                                                   'eighteenkp': saved_variables[225][1],
                                                   'nineteenphi': saved_variables[226][1],
                                                   'nineteenname': saved_variables[227][1],
                                                   'nineteentype': saved_variables[228][1],
                                                   'nineteengamma': saved_variables[229][1],
                                                   'nineteenqu': saved_variables[230][1],
                                                   'nineteenka': saved_variables[231][1],
                                                   'nineteenkp': saved_variables[232][1],
                                                   'twentyphi': saved_variables[233][1],
                                                   'twentyname': saved_variables[234][1],
                                                   'twentytype': saved_variables[235][1],
                                                   'twentygamma': saved_variables[236][1],
                                                   'twentyqu': saved_variables[237][1],
                                                   'twentyka': saved_variables[238][1],
                                                   'twentykp': saved_variables[239][1],
                                                   'wp1': saved_variables[240][1],
                                                   'wp1_layer': saved_variables[241][1],
                                                   'wp1_layer_front': saved_variables[242][1],
                                                   'wp2': saved_variables[243][1],'wp2_layer': saved_variables[244][1],'wp2_layer_front': saved_variables[245][1],'wp3': saved_variables[246][1],'wp3_layer': saved_variables[247][1],'wp3_layer_front': saved_variables[248][1],'wp4': saved_variables[249][1],'wp4_layer': saved_variables[250][1],'wp4_layer_front': saved_variables[251][1],'wp5': saved_variables[252][1],'wp5_layer': saved_variables[253][1],'wp5_layer_front': saved_variables[254][1],'wp6': saved_variables[255][1],'wp6_layer': saved_variables[256][1],'wp6_layer_front': saved_variables[257][1],'wp7': saved_variables[258][1],'wp7_layer': saved_variables[259][1],'wp7_layer_front': saved_variables[260][1],'wp8': saved_variables[261][1],'wp8_layer': saved_variables[262][1],'wp8_layer_front': saved_variables[263][1],'wp9': saved_variables[264][1],'wp9_layer': saved_variables[265][1],'wp9_layer_front': saved_variables[266][1],'wp10': saved_variables[267][1],'wp10_layer': saved_variables[268][1],'wp10_layer_front': saved_variables[269][1],'wp11': saved_variables[270][1],'wp11_layer': saved_variables[271][1],'wp11_layer_front': saved_variables[272][1],'wp12': saved_variables[273][1],'wp12_layer': saved_variables[274][1],'wp12_layer_front': saved_variables[275][1],'wp13': saved_variables[276][1],'wp13_layer': saved_variables[277][1],'wp13_layer_front': saved_variables[278][1],'wp14': saved_variables[279][1],'wp14_layer': saved_variables[280][1],'wp14_layer_front': saved_variables[281][1],'wp15': saved_variables[282][1],'wp15_layer': saved_variables[283][1],'wp15_layer_front': saved_variables[284][1],'wp16': saved_variables[285][1],'wp16_layer': saved_variables[286][1],'wp16_layer_front': saved_variables[287][1],'wp17': saved_variables[288][1],'wp17_layer': saved_variables[289][1],'wp17_layer_front': saved_variables[290][1],'wp18': saved_variables[291][1],'wp18_layer': saved_variables[292][1],'wp18_layer_front': saved_variables[293][1],'wp19': saved_variables[294][1],'wp19_layer': saved_variables[295][1],'wp19_layer_front': saved_variables[296][1],'wp20': saved_variables[297][1],'wp20_layer': saved_variables[298][1],'wp20_layer_front': saved_variables[299][1],'wp21': saved_variables[300][1],'wp21_layer': saved_variables[301][1],'wp21_layer_front': saved_variables[302][1],'wp22': saved_variables[303][1],'wp22_layer': saved_variables[304][1],'wp22_layer_front': saved_variables[305][1],'wp23': saved_variables[306][1],'wp23_layer': saved_variables[307][1],'wp23_layer_front': saved_variables[308][1],'wp24': saved_variables[309][1],'wp24_layer': saved_variables[310][1],'wp24_layer_front': saved_variables[311][1],'wp25': saved_variables[312][1],'wp25_layer': saved_variables[313][1],'wp25_layer_front': saved_variables[314][1],'wp26': saved_variables[315][1],'wp26_layer': saved_variables[316][1],'wp26_layer_front': saved_variables[317][1],'wp27': saved_variables[318][1],'wp27_layer': saved_variables[319][1],'wp27_layer_front': saved_variables[320][1],'wp28': saved_variables[321][1],'wp28_layer': saved_variables[322][1],'wp28_layer_front': saved_variables[323][1],'wp29': saved_variables[324][1],'wp29_layer': saved_variables[325][1],'wp29_layer_front': saved_variables[326][1],'wp30': saved_variables[327][1],'wp30_layer': saved_variables[328][1],'wp30_layer_front': saved_variables[329][1],'wp31': saved_variables[330][1],'wp31_layer': saved_variables[331][1],'wp31_layer_front': saved_variables[332][1],'wp32': saved_variables[333][1],'wp32_layer': saved_variables[334][1],'wp32_layer_front': saved_variables[335][1],'wp33': saved_variables[336][1],'wp33_layer': saved_variables[337][1],'wp33_layer_front': saved_variables[338][1],'wp34': saved_variables[339][1],'wp34_layer': saved_variables[340][1],'wp34_layer_front': saved_variables[341][1],'wp35': saved_variables[342][1],'wp35_layer': saved_variables[343][1],'wp35_layer_front': saved_variables[344][1],'wp36': saved_variables[345][1],'wp36_layer': saved_variables[346][1],'wp36_layer_front': saved_variables[347][1],'wp37': saved_variables[348][1],'wp37_layer': saved_variables[349][1],'wp37_layer_front': saved_variables[350][1],'wp38': saved_variables[351][1],'wp38_layer': saved_variables[352][1],'wp38_layer_front': saved_variables[353][1],'wp39': saved_variables[354][1],'wp39_layer': saved_variables[355][1],'wp39_layer_front': saved_variables[356][1],'wp40': saved_variables[357][1],'wp40_layer': saved_variables[358][1],'wp40_layer_front': saved_variables[359][1],'surcharge_unit_weight': saved_variables[360][1],'min_surcharge_height': saved_variables[361][1],'angle': saved_variables[362][1],'angle_change_elev': saved_variables[363][1],'water_elev': saved_variables[364][1],'cut_elev': saved_variables[365][1],'total_weights': saved_variables[366][1],'top_brace_elev': saved_variables[367][1],'bot_brace_elev': saved_variables[368][1],'diagram_type': saved_variables[369][1],'backside_x': saved_variables[370][1],'backside_y': saved_variables[371][1],'scale_factor': saved_variables[372][1],'sheet_type': saved_variables[373][1],'beam_type': saved_variables[374][1],'water_cut_elev': saved_variables[375][1],'top_sheet': saved_variables[376][1],'beam_spacing': saved_variables[377][1],'beam_size_override': saved_variables[378][1],'beam_override': saved_variables[379][1],'beam_modulus_override': saved_variables[380][1],'beam_inertia_override': saved_variables[381][1],'ers_type': saved_variables[382][1],'soldier_beam_method': saved_variables[383][1],'supplied_length': saved_variables[384][1],'wat_check': saved_variables[385][1],'angle_change_type': saved_variables[386][1],'saved_sheet_pile': saved_sheet_pile,'saved_sheet_pile': saved_sheet_pile,'saved_soldier_pile': saved_soldier_pile}

                                                  )

    return render(request, 'multilayer.html')


def three_layer(request):
    saved_calc_input = []
    saved_calc_load_check = int(request.GET['saved_calc_load_check'])
    if saved_calc_load_check == 1:
        saved_calc_input = request.GET['saved_calc_input']
        saved_calc_input = ast.literal_eval(saved_calc_input)
        saved_variables = []
        count = 0
        for variable in saved_calc_input:
            if variable == "":
                saved_variables.append([count, variable])
            else:
                saved_variables.append([count, float(variable)])
            count += 1
        saved_sheet_pile = sheet_database[int(saved_variables[374][1]) - 1][1]
        saved_soldier_pile = beam_database[int(saved_variables[375][1]) - 1][1]

        return render(request, 'three_layer.html', {'footing_1_type': saved_variables[0][1],
                                                   'footing_1_width': saved_variables[1][1],
                                                   'footing_1_distance': saved_variables[2][1],
                                                   'footing_1_elevation': saved_variables[3][1],
                                                   'footing_1_load': saved_variables[4][1],
                                                   'footing_1_spacing_1': saved_variables[5][1],
                                                   'footing_1_spacing_2': saved_variables[6][1],
                                                   'footing_2_type': saved_variables[7][1],
                                                   'footing_2_width': saved_variables[8][1],
                                                   'footing_2_distance': saved_variables[9][1],
                                                   'footing_2_elevation': saved_variables[10][1],
                                                   'footing_2_load': saved_variables[11][1],
                                                   'footing_2_spacing_1': saved_variables[12][1],
                                                   'footing_2_spacing_2': saved_variables[13][1],
                                                   'footing_3_type': saved_variables[14][1],
                                                   'footing_3_width': saved_variables[15][1],
                                                   'footing_3_distance': saved_variables[16][1],
                                                   'footing_3_elevation': saved_variables[17][1],
                                                   'footing_3_load': saved_variables[18][1],
                                                   'footing_3_spacing_1': saved_variables[19][1],
                                                   'footing_3_spacing_2': saved_variables[20][1],
                                                   'footing_4_type': saved_variables[21][1],
                                                   'footing_4_width': saved_variables[22][1],
                                                   'footing_4_distance': saved_variables[23][1],
                                                   'footing_4_elevation': saved_variables[24][1],
                                                   'footing_4_load': saved_variables[25][1],
                                                   'footing_4_spacing_1': saved_variables[26][1],
                                                   'footing_4_spacing_2': saved_variables[27][1],
                                                   'train_1_distance': saved_variables[28][1],
                                                   'train_1_load': saved_variables[29][1],
                                                   'train_1_tie_size': saved_variables[30][1],
                                                   'train_1_elevation': saved_variables[31][1],
                                                   'train_2_distance': saved_variables[32][1],
                                                   'train_2_load': saved_variables[33][1],
                                                   'train_2_tie_size': saved_variables[34][1],
                                                   'train_2_elevation': saved_variables[35][1],
                                                   'train_3_distance': saved_variables[36][1],
                                                   'train_3_load': saved_variables[37][1],
                                                   'train_3_tie_size': saved_variables[38][1],
                                                   'train_3_elevation': saved_variables[39][1],
                                                   'train_4_distance': saved_variables[40][1],
                                                   'train_4_load': saved_variables[41][1],
                                                   'train_4_tie_size': saved_variables[42][1],
                                                   'train_4_elevation': saved_variables[43][1],
                                                   'surface_side': saved_variables[44][1],
                                                   'point0x': saved_variables[45][1], 'point0y': saved_variables[46][1],
                                                   'point1x': saved_variables[47][1], 'point1y': saved_variables[48][1],
                                                   'point2x': saved_variables[49][1], 'point2y': saved_variables[50][1],
                                                   'point3x': saved_variables[51][1], 'point3y': saved_variables[52][1],
                                                   'point4x': saved_variables[53][1], 'point4y': saved_variables[54][1],
                                                   'point5x': saved_variables[55][1], 'point5y': saved_variables[56][1],
                                                   'point6x': saved_variables[57][1], 'point6y': saved_variables[58][1],
                                                   'point7x': saved_variables[59][1], 'point7y': saved_variables[60][1],
                                                   'point8x': saved_variables[61][1], 'point8y': saved_variables[62][1],
                                                   'point9x': saved_variables[63][1], 'point9y': saved_variables[64][1],
                                                   'point10x': saved_variables[65][1],
                                                   'point10y': saved_variables[66][1],
                                                   'point11x': saved_variables[67][1],
                                                   'point11y': saved_variables[68][1],
                                                   'point12x': saved_variables[69][1],
                                                   'point12y': saved_variables[70][1],
                                                   'point13x': saved_variables[71][1],
                                                   'point13y': saved_variables[72][1], 'berm0x': saved_variables[73][1],
                                                   'berm0y': saved_variables[74][1], 'berm1x': saved_variables[75][1],
                                                   'berm1y': saved_variables[76][1], 'berm2x': saved_variables[77][1],
                                                   'berm2y': saved_variables[78][1], 'berm3x': saved_variables[79][1],
                                                   'berm3y': saved_variables[80][1], 'berm4x': saved_variables[81][1],
                                                   'berm4y': saved_variables[82][1], 'berm5x': saved_variables[83][1],
                                                   'berm5y': saved_variables[84][1], 'berm6x': saved_variables[85][1],
                                                   'berm6y': saved_variables[86][1], 'berm7x': saved_variables[87][1],
                                                   'berm7y': saved_variables[88][1], 'berm8x': saved_variables[89][1],
                                                   'berm8y': saved_variables[90][1], 'berm9x': saved_variables[91][1],
                                                   'berm9y': saved_variables[92][1], 'berm10x': saved_variables[93][1],
                                                   'berm10y': saved_variables[94][1], 'berm11x': saved_variables[95][1],
                                                   'berm11y': saved_variables[96][1], 'berm12x': saved_variables[97][1],
                                                   'berm12y': saved_variables[98][1], 'berm13x': saved_variables[99][1],
                                                   'berm13y': saved_variables[100][1],
                                                   'onename': saved_variables[101][1],
                                                   'onetype': saved_variables[102][1],
                                                   'onegamma': saved_variables[103][1],
                                                   'onequ': saved_variables[104][1],
                                                   'oneka': saved_variables[105][1], 'onekp': saved_variables[106][1],
                                                   'onephi': saved_variables[107][1],
                                                   'twoname': saved_variables[108][1],
                                                   'twotype': saved_variables[109][1],
                                                   'twogamma': saved_variables[110][1],
                                                   'twoqu': saved_variables[111][1],
                                                   'twoka': saved_variables[112][1], 'twokp': saved_variables[113][1],
                                                   'twophi': saved_variables[114][1],
                                                   'threename': saved_variables[115][1],
                                                   'threetype': saved_variables[116][1],
                                                   'threegamma': saved_variables[117][1],
                                                   'threequ': saved_variables[118][1],
                                                   'threeka': saved_variables[119][1],
                                                   'threekp': saved_variables[120][1],
                                                   'threephi': saved_variables[121][1],
                                                   'fourname': saved_variables[122][1],
                                                   'fourtype': saved_variables[123][1],
                                                   'fourgamma': saved_variables[124][1],
                                                   'fourqu': saved_variables[125][1],
                                                   'fourka': saved_variables[126][1], 'fourkp': saved_variables[127][1],
                                                   'fourphi': saved_variables[128][1],
                                                   'fivename': saved_variables[129][1],
                                                   'fivetype': saved_variables[130][1],
                                                   'fivegamma': saved_variables[131][1],
                                                   'fivequ': saved_variables[132][1],
                                                   'fiveka': saved_variables[133][1], 'fivekp': saved_variables[134][1],
                                                   'fivephi': saved_variables[135][1],
                                                   'sixname': saved_variables[136][1],
                                                   'sixtype': saved_variables[137][1],
                                                   'sixgamma': saved_variables[138][1],
                                                   'sixqu': saved_variables[139][1],
                                                   'sixka': saved_variables[140][1], 'sixkp': saved_variables[141][1],
                                                   'sixphi': saved_variables[142][1],
                                                   'sevenname': saved_variables[143][1],
                                                   'seventype': saved_variables[144][1],
                                                   'sevengamma': saved_variables[145][1],
                                                   'sevenqu': saved_variables[146][1],
                                                   'sevenka': saved_variables[147][1],
                                                   'sevenkp': saved_variables[148][1],
                                                   'sevenphi': saved_variables[149][1],
                                                   'eightname': saved_variables[150][1],
                                                   'eighttype': saved_variables[151][1],
                                                   'eightgamma': saved_variables[152][1],
                                                   'eightqu': saved_variables[153][1],
                                                   'eightka': saved_variables[154][1],
                                                   'eightkp': saved_variables[155][1],
                                                   'eightphi': saved_variables[156][1],
                                                   'ninename': saved_variables[157][1],
                                                   'ninetype': saved_variables[158][1],
                                                   'ninegamma': saved_variables[159][1],
                                                   'ninequ': saved_variables[160][1],
                                                   'nineka': saved_variables[161][1], 'ninekp': saved_variables[162][1],
                                                   'ninephi': saved_variables[163][1],
                                                   'tenname': saved_variables[164][1],
                                                   'tentype': saved_variables[165][1],
                                                   'tengamma': saved_variables[166][1],
                                                   'tenqu': saved_variables[167][1], 'tenka': saved_variables[168][1],
                                                   'tenkp': saved_variables[169][1], 'tenphi': saved_variables[170][1],
                                                   'elevenname': saved_variables[171][1],
                                                   'eleventype': saved_variables[172][1],
                                                   'elevengamma': saved_variables[173][1],
                                                   'elevenqu': saved_variables[174][1],
                                                   'elevenka': saved_variables[175][1],
                                                   'elevenkp': saved_variables[176][1],
                                                   'elevenphi': saved_variables[177][1],
                                                   'twelvename': saved_variables[178][1],
                                                   'twelvetype': saved_variables[179][1],
                                                   'twelvegamma': saved_variables[180][1],
                                                   'twelvequ': saved_variables[181][1],
                                                   'twelveka': saved_variables[182][1],
                                                   'twelvekp': saved_variables[183][1],
                                                   'twelvephi': saved_variables[184][1],
                                                   'thirteenname': saved_variables[185][1],
                                                   'thirteentype': saved_variables[186][1],
                                                   'thirteengamma': saved_variables[187][1],
                                                   'thirteenqu': saved_variables[188][1],
                                                   'thirteenka': saved_variables[189][1],
                                                   'thirteenkp': saved_variables[190][1],
                                                   'fourteenphi': saved_variables[191][1],
                                                   'fourteenname': saved_variables[192][1],
                                                   'fourteentype': saved_variables[193][1],
                                                   'fourteengamma': saved_variables[194][1],
                                                   'fourteenqu': saved_variables[195][1],
                                                   'fourteenka': saved_variables[196][1],
                                                   'fourteenkp': saved_variables[197][1],
                                                   'fifteenphi': saved_variables[198][1],
                                                   'fifteenname': saved_variables[199][1],
                                                   'fifteentype': saved_variables[200][1],
                                                   'fifteengamma': saved_variables[201][1],
                                                   'fifteenqu': saved_variables[202][1],
                                                   'fifteenka': saved_variables[203][1],
                                                   'fifteenkp': saved_variables[204][1],
                                                   'sixteenphi': saved_variables[205][1],
                                                   'sixteenname': saved_variables[206][1],
                                                   'sixteentype': saved_variables[207][1],
                                                   'sixteengamma': saved_variables[208][1],
                                                   'sixteenqu': saved_variables[209][1],
                                                   'sixteenka': saved_variables[210][1],
                                                   'sixteenkp': saved_variables[211][1],
                                                   'seventeenphi': saved_variables[212][1],
                                                   'seventeenname': saved_variables[213][1],
                                                   'seventeentype': saved_variables[214][1],
                                                   'seventeengamma': saved_variables[215][1],
                                                   'seventeenqu': saved_variables[216][1],
                                                   'seventeenka': saved_variables[217][1],
                                                   'seventeenkp': saved_variables[218][1],
                                                   'eighteenphi': saved_variables[219][1],
                                                   'eighteenname': saved_variables[220][1],
                                                   'eighteentype': saved_variables[221][1],
                                                   'eighteengamma': saved_variables[222][1],
                                                   'eighteenqu': saved_variables[223][1],
                                                   'eighteenka': saved_variables[224][1],
                                                   'eighteenkp': saved_variables[225][1],
                                                   'nineteenphi': saved_variables[226][1],
                                                   'nineteenname': saved_variables[227][1],
                                                   'nineteentype': saved_variables[228][1],
                                                   'nineteengamma': saved_variables[229][1],
                                                   'nineteenqu': saved_variables[230][1],
                                                   'nineteenka': saved_variables[231][1],
                                                   'nineteenkp': saved_variables[232][1],
                                                   'twentyphi': saved_variables[233][1],
                                                   'twentyname': saved_variables[234][1],
                                                   'twentytype': saved_variables[235][1],
                                                   'twentygamma': saved_variables[236][1],
                                                   'twentyqu': saved_variables[237][1],
                                                   'twentyka': saved_variables[238][1],
                                                   'twentykp': saved_variables[239][1],
                                                    'wp1': saved_variables[240][1],
                                                    'wp1_layer': saved_variables[241][1],
                                                    'wp1_layer_front': saved_variables[242][1],
                                                    'wp2': saved_variables[243][1],
                                                    'wp2_layer': saved_variables[244][1],
                                                    'wp2_layer_front': saved_variables[245][1],
                                                    'wp3': saved_variables[246][1],
                                                    'wp3_layer': saved_variables[247][1],
                                                    'wp3_layer_front': saved_variables[248][1],
                                                    'wp4': saved_variables[249][1],
                                                    'wp4_layer': saved_variables[250][1],
                                                    'wp4_layer_front': saved_variables[251][1],
                                                    'wp5': saved_variables[252][1],
                                                    'wp5_layer': saved_variables[253][1],
                                                    'wp5_layer_front': saved_variables[254][1],
                                                    'wp6': saved_variables[255][1],
                                                    'wp6_layer': saved_variables[256][1],
                                                    'wp6_layer_front': saved_variables[257][1],
                                                    'wp7': saved_variables[258][1],
                                                    'wp7_layer': saved_variables[259][1],
                                                    'wp7_layer_front': saved_variables[260][1],
                                                    'wp8': saved_variables[261][1],
                                                    'wp8_layer': saved_variables[262][1],
                                                    'wp8_layer_front': saved_variables[263][1],
                                                    'wp9': saved_variables[264][1],
                                                    'wp9_layer': saved_variables[265][1],
                                                    'wp9_layer_front': saved_variables[266][1],
                                                    'wp10': saved_variables[267][1],
                                                    'wp10_layer': saved_variables[268][1],
                                                    'wp10_layer_front': saved_variables[269][1],
                                                    'wp11': saved_variables[270][1],
                                                    'wp11_layer': saved_variables[271][1],
                                                    'wp11_layer_front': saved_variables[272][1],
                                                    'wp12': saved_variables[273][1],
                                                    'wp12_layer': saved_variables[274][1],
                                                    'wp12_layer_front': saved_variables[275][1],
                                                    'wp13': saved_variables[276][1],
                                                    'wp13_layer': saved_variables[277][1],
                                                    'wp13_layer_front': saved_variables[278][1],
                                                    'wp14': saved_variables[279][1],
                                                    'wp14_layer': saved_variables[280][1],
                                                    'wp14_layer_front': saved_variables[281][1],
                                                    'wp15': saved_variables[282][1],
                                                    'wp15_layer': saved_variables[283][1],
                                                    'wp15_layer_front': saved_variables[284][1],
                                                    'wp16': saved_variables[285][1],
                                                    'wp16_layer': saved_variables[286][1],
                                                    'wp16_layer_front': saved_variables[287][1],
                                                    'wp17': saved_variables[288][1],
                                                    'wp17_layer': saved_variables[289][1],
                                                    'wp17_layer_front': saved_variables[290][1],
                                                    'wp18': saved_variables[291][1],
                                                    'wp18_layer': saved_variables[292][1],
                                                    'wp18_layer_front': saved_variables[293][1],
                                                    'wp19': saved_variables[294][1],
                                                    'wp19_layer': saved_variables[295][1],
                                                    'wp19_layer_front': saved_variables[296][1],
                                                    'wp20': saved_variables[297][1],
                                                    'wp20_layer': saved_variables[298][1],
                                                    'wp20_layer_front': saved_variables[299][1],
                                                    'wp21': saved_variables[300][1],
                                                    'wp21_layer': saved_variables[301][1],
                                                    'wp21_layer_front': saved_variables[302][1],
                                                    'wp22': saved_variables[303][1],
                                                    'wp22_layer': saved_variables[304][1],
                                                    'wp22_layer_front': saved_variables[305][1],
                                                    'wp23': saved_variables[306][1],
                                                    'wp23_layer': saved_variables[307][1],
                                                    'wp23_layer_front': saved_variables[308][1],
                                                    'wp24': saved_variables[309][1],
                                                    'wp24_layer': saved_variables[310][1],
                                                    'wp24_layer_front': saved_variables[311][1],
                                                    'wp25': saved_variables[312][1],
                                                    'wp25_layer': saved_variables[313][1],
                                                    'wp25_layer_front': saved_variables[314][1],
                                                    'wp26': saved_variables[315][1],
                                                    'wp26_layer': saved_variables[316][1],
                                                    'wp26_layer_front': saved_variables[317][1],
                                                    'wp27': saved_variables[318][1],
                                                    'wp27_layer': saved_variables[319][1],
                                                    'wp27_layer_front': saved_variables[320][1],
                                                    'wp28': saved_variables[321][1],
                                                    'wp28_layer': saved_variables[322][1],
                                                    'wp28_layer_front': saved_variables[323][1],
                                                    'wp29': saved_variables[324][1],
                                                    'wp29_layer': saved_variables[325][1],
                                                    'wp29_layer_front': saved_variables[326][1],
                                                    'wp30': saved_variables[327][1],
                                                    'wp30_layer': saved_variables[328][1],
                                                    'wp30_layer_front': saved_variables[329][1],
                                                    'wp31': saved_variables[330][1],
                                                    'wp31_layer': saved_variables[331][1],
                                                    'wp31_layer_front': saved_variables[332][1],
                                                    'wp32': saved_variables[333][1],
                                                    'wp32_layer': saved_variables[334][1],
                                                    'wp32_layer_front': saved_variables[335][1],
                                                    'wp33': saved_variables[336][1],
                                                    'wp33_layer': saved_variables[337][1],
                                                    'wp33_layer_front': saved_variables[338][1],
                                                    'wp34': saved_variables[339][1],
                                                    'wp34_layer': saved_variables[340][1],
                                                    'wp34_layer_front': saved_variables[341][1],
                                                    'wp35': saved_variables[342][1],
                                                    'wp35_layer': saved_variables[343][1],
                                                    'wp35_layer_front': saved_variables[344][1],
                                                    'wp36': saved_variables[345][1],
                                                    'wp36_layer': saved_variables[346][1],
                                                    'wp36_layer_front': saved_variables[347][1],
                                                    'wp37': saved_variables[348][1],
                                                    'wp37_layer': saved_variables[349][1],
                                                    'wp37_layer_front': saved_variables[350][1],
                                                    'wp38': saved_variables[351][1],
                                                    'wp38_layer': saved_variables[352][1],
                                                    'wp38_layer_front': saved_variables[353][1],
                                                    'wp39': saved_variables[354][1],
                                                    'wp39_layer': saved_variables[355][1],
                                                    'wp39_layer_front': saved_variables[356][1],
                                                    'wp40': saved_variables[357][1],
                                                    'wp40_layer': saved_variables[358][1],
                                                    'wp40_layer_front': saved_variables[359][1],
                                                    'surcharge_unit_weight': saved_variables[360][1],
                                                    'min_surcharge_height': saved_variables[361][1],
                                                    'angle': saved_variables[362][1],
                                                    'angle_change_elev': saved_variables[363][1],
                                                    'water_elev': saved_variables[364][1],
                                                    'cut_elev': saved_variables[365][1],
                                                    'total_weights': saved_variables[366][1],
                                                    'top_brace_elev': saved_variables[367][1],
                                                    'mid_brace_elev': saved_variables[368][1],
                                                    'bot_brace_elev': saved_variables[369][1],
                                                    'diagram_type': saved_variables[370][1],
                                                    'backside_x': saved_variables[371][1],
                                                    'backside_y': saved_variables[372][1],
                                                    'scale_factor': saved_variables[373][1],
                                                    'sheet_type': saved_variables[374][1],
                                                    'beam_type': saved_variables[375][1],
                                                    'water_cut_elev': saved_variables[376][1],
                                                    'top_sheet': saved_variables[377][1],
                                                    'beam_spacing': saved_variables[378][1],
                                                    'beam_size_override': saved_variables[379][1],
                                                    'beam_override': saved_variables[380][1],
                                                    'beam_modulus_override': saved_variables[381][1],
                                                    'beam_inertia_override': saved_variables[382][1],
                                                    'ers_type': saved_variables[383][1],
                                                    'soldier_beam_method': saved_variables[384][1],
                                                    'supplied_length': saved_variables[385][1],
                                                    'wat_check': saved_variables[386][1],
                                                    'angle_change_type': saved_variables[387][1],
                                                    '13.phi': saved_variables[388][1],
                                                    'saved_sheet_pile': saved_sheet_pile,
                                                    'saved_soldier_pile': saved_soldier_pile}

        )

    return render(request, 'three_layer.html')


def micropile_joint_bending_capacity(request):
    return render(request, 'micropile_joint_bending_capacity.html')


def one_layer_optimizer(request):
    return render(request, 'one_layer_optimizer.html')


def output(request):
    # TAKE INPUT DATA FROM USER
    footings = []
    trains = []
    # footing_surcharge(type, width, distance, elevation, load, spacing_1, spacing_2)
    if request.GET['footing_1_type'] != '':
        footing_1 = footing_surcharge(float(request.GET['footing_1_type']),
                                      float(request.GET['footing_1_width']),
                                      float(request.GET['footing_1_distance']),
                                      float(request.GET['footing_1_elevation']),
                                      float(request.GET['footing_1_load']),
                                      float(request.GET['footing_1_spacing_1']),
                                      float(request.GET['footing_1_spacing_2']))
        footings.append(footing_1)
    if request.GET['footing_2_type'] != '':
        footing_2 = footing_surcharge(float(request.GET['footing_2_type']),
                                      float(request.GET['footing_2_width']),
                                      float(request.GET['footing_2_distance']),
                                      float(request.GET['footing_2_elevation']),
                                      float(request.GET['footing_2_load']),
                                      float(request.GET['footing_2_spacing_1']),
                                      float(request.GET['footing_2_spacing_2']))
        footings.append(footing_2)
    if request.GET['footing_3_type'] != '':
        footing_3 = footing_surcharge(float(request.GET['footing_3_type']),
                                      float(request.GET['footing_3_width']),
                                      float(request.GET['footing_3_distance']),
                                      float(request.GET['footing_3_elevation']),
                                      float(request.GET['footing_3_load']),
                                      float(request.GET['footing_3_spacing_1']),
                                      float(request.GET['footing_3_spacing_2']))
        footings.append(footing_3)
    if request.GET['footing_4_type'] != '':
        footing_4 = footing_surcharge(float(request.GET['footing_4_type']),
                                      float(request.GET['footing_4_width']),
                                      float(request.GET['footing_4_distance']),
                                      float(request.GET['footing_4_elevation']),
                                      float(request.GET['footing_4_load']),
                                      float(request.GET['footing_4_spacing_1']),
                                      float(request.GET['footing_4_spacing_2']))
        footings.append(footing_4)

    if request.GET['train_1_distance'] != '':
        train_1 = train_loading(float(request.GET['train_1_distance']),
                                float(request.GET['train_1_load']),
                                float(request.GET['train_1_tie_size']),
                                float(request.GET['train_1_elevation'])
                                )
        trains.append(train_1)
    if request.GET['train_2_distance'] != '':
        train_2 = train_loading(float(request.GET['train_2_distance']),
                                float(request.GET['train_2_load']),
                                float(request.GET['train_2_tie_size']),
                                float(request.GET['train_2_elevation'])
                                )
        trains.append(train_2)
    if request.GET['train_3_distance'] != '':
        train_3 = train_loading(float(request.GET['train_3_distance']),
                                float(request.GET['train_3_load']),
                                float(request.GET['train_3_tie_size']),
                                float(request.GET['train_3_elevation'])
                                )
        trains.append(train_3)
    if request.GET['train_4_distance'] != '':
        train_4 = train_loading(float(request.GET['train_4_distance']),
                                float(request.GET['train_4_load']),
                                float(request.GET['train_4_tie_size']),
                                float(request.GET['train_4_elevation'])
                                )
        trains.append(train_4)

    surface_side = float(request.GET['surface_side'])

    surface_array = [(request.GET['point0x'], request.GET['point0y']),
                     (request.GET['point1x'], request.GET['point1y']),
                     (request.GET['point2x'], request.GET['point2y']),
                     (request.GET['point3x'], request.GET['point3y']),
                     (request.GET['point4x'], request.GET['point4y']),
                     (request.GET['point5x'], request.GET['point5y']),
                     (request.GET['point6x'], request.GET['point6y']),
                     (request.GET['point7x'], request.GET['point7y']),
                     (request.GET['point8x'], request.GET['point8y']),
                     (request.GET['point9x'], request.GET['point9y']),
                     (request.GET['point10x'], request.GET['point10y']),
                     (request.GET['point11x'], request.GET['point11y']),
                     (request.GET['point12x'], request.GET['point12y']),
                     (request.GET['point13x'], request.GET['point13y'])]
    new_surface_array = []  # Remove all points with no entries

    # Pare down surface array points to just the ones that were entered
    for i in range(len(surface_array)):
        if surface_array[i] != ('', ''):
            new_surface_array.append(surface_array[i])
    surface_array = []
    for i in range(len(new_surface_array)):
        surface_array.append(((float(new_surface_array[i][0])), float(new_surface_array[i][1])))

    berm_array = []
    if request.GET['berm0x'] != '':
        berm_array = [(request.GET['berm0x'], request.GET['berm0y']),
                         (request.GET['berm1x'], request.GET['berm1y']),
                         (request.GET['berm2x'], request.GET['berm2y']),
                         (request.GET['berm3x'], request.GET['berm3y']),
                         (request.GET['berm4x'], request.GET['berm4y']),
                         (request.GET['berm5x'], request.GET['berm5y']),
                         (request.GET['berm6x'], request.GET['berm6y']),
                         (request.GET['berm7x'], request.GET['berm7y']),
                         (request.GET['berm8x'], request.GET['berm8y']),
                         (request.GET['berm9x'], request.GET['berm9y']),
                         (request.GET['berm10x'], request.GET['berm10y']),
                         (request.GET['berm11x'], request.GET['berm11y']),
                         (request.GET['berm12x'], request.GET['berm12y']),
                         (request.GET['berm13x'], request.GET['berm13y'])]
        new_berm_array = []  # Remove all points with no entries

        # Pare down surface array points to just the ones that were entered
        for i in range(len(berm_array)):
            if berm_array[i] != ('', ''):
                new_berm_array.append(berm_array[i])
        berm_array = []
        for i in range(len(new_berm_array)):
            berm_array.append(((float(new_berm_array[i][0])), float(new_berm_array[i][1])))

    if request.GET['1.name'] != '':  # If layer doesn't have a name, assume it does not exist and do not input it.
        layer_1 = Layer(request.GET['1.name'], float(request.GET['1.type']), float(request.GET['1.gamma']),
                        float(request.GET['1.qu']),
                        float(request.GET['1.ka']), float(request.GET['1.kp']),
                        float(request.GET['1.phi']))
    if request.GET['2.name'] != '':
        layer_2 = Layer(request.GET['2.name'], float(request.GET['2.type']), float(request.GET['2.gamma']),
                        float(request.GET['2.qu']),
                        float(request.GET['2.ka']), float(request.GET['2.kp']),
                        float(request.GET['2.phi']))
    if request.GET['3.name'] != '':
        layer_3 = Layer(request.GET['3.name'], float(request.GET['3.type']), float(request.GET['3.gamma']),
                        float(request.GET['3.qu']),
                        float(request.GET['3.ka']), float(request.GET['3.kp']),
                        float(request.GET['3.phi']))
    if request.GET['4.name'] != '':
        layer_4 = Layer(request.GET['4.name'], float(request.GET['4.type']), float(request.GET['4.gamma']),
                        float(request.GET['4.qu']),
                        float(request.GET['4.ka']), float(request.GET['4.kp']),
                        float(request.GET['4.phi']))
    if request.GET['5.name'] != '':
        layer_5 = Layer(request.GET['5.name'], float(request.GET['5.type']), float(request.GET['5.gamma']),
                        float(request.GET['5.qu']),
                        float(request.GET['5.ka']), float(request.GET['5.kp']),
                        float(request.GET['5.phi']))
    if request.GET['6.name'] != '':
        layer_6 = Layer(request.GET['6.name'], float(request.GET['6.type']), float(request.GET['6.gamma']),
                        float(request.GET['6.qu']),
                        float(request.GET['6.ka']), float(request.GET['6.kp']),
                        float(request.GET['6.phi']))
    if request.GET['7.name'] != '':
        layer_7 = Layer(request.GET['7.name'], float(request.GET['7.type']), float(request.GET['7.gamma']),
                        float(request.GET['7.qu']),
                        float(request.GET['7.ka']), float(request.GET['7.kp']),
                        float(request.GET['7.phi']))
    if request.GET['8.name'] != '':
        layer_8 = Layer(request.GET['8.name'], float(request.GET['8.type']), float(request.GET['8.gamma']),
                        float(request.GET['8.qu']),
                        float(request.GET['8.ka']), float(request.GET['8.kp']),
                        float(request.GET['8.phi']))
    if request.GET['9.name'] != '':
        layer_9 = Layer(request.GET['9.name'], float(request.GET['9.type']), float(request.GET['9.gamma']),
                        float(request.GET['9.qu']),
                        float(request.GET['9.ka']), float(request.GET['9.kp']),
                        float(request.GET['9.phi']))
    if request.GET['10.name'] != '':
        layer_10 = Layer(request.GET['10.name'], float(request.GET['10.type']), float(request.GET['10.gamma']),
                        float(request.GET['10.qu']),
                        float(request.GET['10.ka']), float(request.GET['10.kp']),
                        float(request.GET['10.phi']))
    if request.GET['11.name'] != '':
        layer_11 = Layer(request.GET['11.name'], float(request.GET['11.type']), float(request.GET['11.gamma']),
                        float(request.GET['11.qu']),
                        float(request.GET['11.ka']), float(request.GET['11.kp']),
                        float(request.GET['11.phi']))
    if request.GET['12.name'] != '':
        layer_12 = Layer(request.GET['12.name'], float(request.GET['12.type']), float(request.GET['12.gamma']),
                        float(request.GET['12.qu']),
                        float(request.GET['12.ka']), float(request.GET['12.kp']),
                        float(request.GET['12.phi']))
    if request.GET['13.name'] != '':
        layer_13 = Layer(request.GET['13.name'], float(request.GET['13.type']), float(request.GET['13.gamma']),
                        float(request.GET['13.qu']),
                        float(request.GET['13.ka']), float(request.GET['13.kp']),
                        float(request.GET['13.phi']))
    if request.GET['14.name'] != '':
        layer_14 = Layer(request.GET['14.name'], float(request.GET['14.type']), float(request.GET['14.gamma']),
                        float(request.GET['14.qu']),
                        float(request.GET['14.ka']), float(request.GET['14.kp']),
                        float(request.GET['14.phi']))

    # elevation, layer, soil surcharge placeholder, footing placeholder, train placeholder, passive height placeholder
    layers = [[request.GET['wp1'], request.GET['wp1_layer'], 0, 0, 0, 10000, request.GET['wp1_layer_front']],
              [request.GET['wp2'], request.GET['wp2_layer'], 0, 0, 0, 10000, request.GET['wp2_layer_front']],
              [request.GET['wp3'], request.GET['wp3_layer'], 0, 0, 0, 10000, request.GET['wp3_layer_front']],
              [request.GET['wp4'], request.GET['wp4_layer'], 0, 0, 0, 10000, request.GET['wp4_layer_front']],
              [request.GET['wp5'], request.GET['wp5_layer'], 0, 0, 0, 10000, request.GET['wp5_layer_front']],
              [request.GET['wp6'], request.GET['wp6_layer'], 0, 0, 0, 10000, request.GET['wp6_layer_front']],
              [request.GET['wp7'], request.GET['wp7_layer'], 0, 0, 0, 10000, request.GET['wp7_layer_front']],
              [request.GET['wp8'], request.GET['wp8_layer'], 0, 0, 0, 10000, request.GET['wp8_layer_front']],
              [request.GET['wp9'], request.GET['wp9_layer'], 0, 0, 0, 10000, request.GET['wp9_layer_front']],
              [request.GET['wp10'], request.GET['wp10_layer'], 0, 0, 0, 10000, request.GET['wp10_layer_front']],
              [request.GET['wp11'], request.GET['wp11_layer'], 0, 0, 0, 10000, request.GET['wp11_layer_front']],
              [request.GET['wp12'], request.GET['wp12_layer'], 0, 0, 0, 10000, request.GET['wp12_layer_front']],
              [request.GET['wp13'], request.GET['wp13_layer'], 0, 0, 0, 10000, request.GET['wp13_layer_front']],
              [request.GET['wp14'], request.GET['wp14_layer'], 0, 0, 0, 10000, request.GET['wp14_layer_front']],
              [request.GET['wp15'], request.GET['wp15_layer'], 0, 0, 0, 10000, request.GET['wp15_layer_front']],
              [request.GET['wp16'], request.GET['wp16_layer'], 0, 0, 0, 10000, request.GET['wp16_layer_front']],
              [request.GET['wp17'], request.GET['wp17_layer'], 0, 0, 0, 10000, request.GET['wp17_layer_front']],
              [request.GET['wp18'], request.GET['wp18_layer'], 0, 0, 0, 10000, request.GET['wp18_layer_front']],
              [request.GET['wp19'], request.GET['wp19_layer'], 0, 0, 0, 10000, request.GET['wp19_layer_front']],
              [request.GET['wp20'], request.GET['wp20_layer'], 0, 0, 0, 10000, request.GET['wp20_layer_front']],
              [request.GET['wp21'], request.GET['wp21_layer'], 0, 0, 0, 10000, request.GET['wp21_layer_front']],
              [request.GET['wp22'], request.GET['wp22_layer'], 0, 0, 0, 10000, request.GET['wp22_layer_front']],
              [request.GET['wp23'], request.GET['wp23_layer'], 0, 0, 0, 10000, request.GET['wp23_layer_front']],
              [request.GET['wp24'], request.GET['wp24_layer'], 0, 0, 0, 10000, request.GET['wp24_layer_front']],
              [request.GET['wp25'], request.GET['wp25_layer'], 0, 0, 0, 10000, request.GET['wp25_layer_front']],
              [request.GET['wp26'], request.GET['wp26_layer'], 0, 0, 0, 10000, request.GET['wp26_layer_front']],
              [request.GET['wp27'], request.GET['wp27_layer'], 0, 0, 0, 10000, request.GET['wp27_layer_front']],
              [request.GET['wp28'], request.GET['wp28_layer'], 0, 0, 0, 10000, request.GET['wp28_layer_front']],
              [request.GET['wp29'], request.GET['wp29_layer'], 0, 0, 0, 10000, request.GET['wp29_layer_front']],
              [request.GET['wp30'], request.GET['wp30_layer'], 0, 0, 0, 10000, request.GET['wp30_layer_front']],
              [request.GET['wp31'], request.GET['wp31_layer'], 0, 0, 0, 10000, request.GET['wp31_layer_front']],
              [request.GET['wp32'], request.GET['wp32_layer'], 0, 0, 0, 10000, request.GET['wp32_layer_front']],
              [request.GET['wp33'], request.GET['wp33_layer'], 0, 0, 0, 10000, request.GET['wp33_layer_front']],
              [request.GET['wp34'], request.GET['wp34_layer'], 0, 0, 0, 10000, request.GET['wp34_layer_front']],
              [request.GET['wp35'], request.GET['wp35_layer'], 0, 0, 0, 10000, request.GET['wp35_layer_front']],
              [request.GET['wp36'], request.GET['wp36_layer'], 0, 0, 0, 10000, request.GET['wp36_layer_front']],
              [request.GET['wp37'], request.GET['wp37_layer'], 0, 0, 0, 10000, request.GET['wp37_layer_front']],
              [request.GET['wp38'], request.GET['wp38_layer'], 0, 0, 0, 10000, request.GET['wp38_layer_front']],
              [request.GET['wp39'], request.GET['wp39_layer'], 0, 0, 0, 10000, request.GET['wp39_layer_front']],
              [request.GET['wp40'], request.GET['wp40_layer'], 0, 0, 0, 10000, request.GET['wp40_layer_front']]]

    new_layers = []  # Remove all layers with no entries
    for i in range(len(layers)):
        if layers[i] != ['', '', 0, 0, 0, 10000, '']:
            new_layers.append(layers[i])
    layers = []
    for i in range(len(new_layers)):
        layers.append([float(new_layers[i][0]), float(new_layers[i][1]), float(new_layers[i][2]),
                       float(new_layers[i][3]), float(new_layers[i][4]), float(new_layers[i][5]),
                       float(new_layers[i][6])])

    work_points = [[0, request.GET['wp1']],
                   [0, request.GET['wp2']],
                   [0, request.GET['wp3']],
                   [0, request.GET['wp4']],
                   [0, request.GET['wp5']],
                   [0, request.GET['wp6']],
                   [0, request.GET['wp7']],
                   [0, request.GET['wp8']],
                   [0, request.GET['wp9']],
                   [0, request.GET['wp10']],
                   [0, request.GET['wp11']],
                   [0, request.GET['wp12']],
                   [0, request.GET['wp13']],
                   [0, request.GET['wp14']],
                   [0, request.GET['wp15']],
                   [0, request.GET['wp16']],
                   [0, request.GET['wp17']],
                   [0, request.GET['wp18']],
                   [0, request.GET['wp19']],
                   [0, request.GET['wp20']],
                   [0, request.GET['wp21']],
                   [0, request.GET['wp22']],
                   [0, request.GET['wp23']],
                   [0, request.GET['wp24']],
                   [0, request.GET['wp25']],
                   [0, request.GET['wp26']],
                   [0, request.GET['wp27']],
                   [0, request.GET['wp28']],
                   [0, request.GET['wp29']],
                   [0, request.GET['wp30']],
                   [0, request.GET['wp31']],
                   [0, request.GET['wp32']],
                   [0, request.GET['wp33']],
                   [0, request.GET['wp34']],
                   [0, request.GET['wp35']],
                   [0, request.GET['wp36']],
                   [0, request.GET['wp37']],
                   [0, request.GET['wp38']],
                   [0, request.GET['wp39']],
                   [0, request.GET['wp40']]
                   ]
    
    new_work_points = []  # Remove all points with no entries
    for i in range(len(work_points)):
        if work_points[i] != [0, '']:
            new_work_points.append(work_points[i])
    work_points = []
    for i in range(len(new_work_points)):
        work_points.append([(float(new_work_points[i][0])), float(new_work_points[i][1])])

    surcharge_unit_weight = float(request.GET['surcharge_unit_weight'])
    min_surcharge_height = request.GET['min_surcharge_height']
    if min_surcharge_height:
        min_surcharge_height = float(min_surcharge_height)
    else:
        min_surcharge_height = []
    angle = float(request.GET['angle'])

    angle_change_elev = request.GET['angle_change_elev']
    if angle_change_elev:
        angle_change_elev = float(angle_change_elev)
    else:
        angle_change_elev = []

    angle_change_type = float(request.GET['angle_change_type'])

    water_elev = request.GET['water_elev']
    if water_elev:
        water_elev = float(water_elev)
    else:
        water_elev = float(-10000)

    cut_elev = float(request.GET['cut_elev'])
    total_weights = float(request.GET['total_weights'])
    brace_elev = float(request.GET['brace_elev'])
    scale_factor = float(request.GET['scale_factor'])
    sheet_type = float(request.GET['sheet_type'])
    beam_type = float(request.GET['beam_type'])
    beam_spacing = []

    water_cut_elev = cut_elev
    if water_elev == float(-10000):
        water_cut_elev = float(-10000)
    if request.GET['water_cut_elev'] != '':
        water_cut_elev = float(request.GET['water_cut_elev'])

    top_sheet = [layers[0][0]]
    if request.GET['top_sheet'] != '':
        top_sheet = [float(request.GET['top_sheet'])]

    for i in range(len(sheet_database)):
        if sheet_type == sheet_database[i][0]:
            sheet_type = sheet_database[i]
    for i in range(len(beam_database)):
        if beam_type == beam_database[i][0]:
            beam_type = beam_database[i]

    if request.GET['beam_spacing'] != '':
        beam_spacing = float(request.GET['beam_spacing'])
    if request.GET['beam_size_override'] != '':
        beam_type[4] = float(request.GET['beam_size_override'])/12
    if request.GET['beam_override'] != '':
        beam_type[1] = request.GET['beam_override']
    if request.GET['beam_modulus_override'] != '':
        beam_type[2] = float(request.GET["beam_modulus_override"])
    if request.GET['beam_inertia_override'] != '':
        beam_type[3] = float(request.GET["beam_inertia_override"])

    ers_type = float(request.GET['ers_type'])
    if ers_type == 1:
        sheet_type = beam_type

    soldier_beam_method = float(request.GET['soldier_beam_method'])

    supplied_length = float(request.GET['supplied_length'])
    supplied_elev = top_sheet[0] - supplied_length

    save_calculation_name = request.GET['save_calculation_name']

    #  MANIPULATE USER DATA
    for i in range(len(layers)):  # Assign layer properties to work points
        if layers[i][1] == 1.0:
            layers[i][1] = layer_1
        if layers[i][1] == 2.0:
            layers[i][1] = layer_2
        if layers[i][1] == 3.0:
            layers[i][1] = layer_3
        if layers[i][1] == 4.0:
            layers[i][1] = layer_4
        if layers[i][1] == 5.0:
            layers[i][1] = layer_5
        if layers[i][1] == 6.0:
            layers[i][1] = layer_6
        if layers[i][1] == 7.0:
            layers[i][1] = layer_7
        if layers[i][1] == 8.0:
            layers[i][1] = layer_8
        if layers[i][1] == 9.0:
            layers[i][1] = layer_9
        if layers[i][1] == 10.0:
            layers[i][1] = layer_10
        if layers[i][1] == 11.0:
            layers[i][1] = layer_11
        if layers[i][1] == 12.0:
            layers[i][1] = layer_12
        if layers[i][1] == 13.0:
            layers[i][1] = layer_13
        if layers[i][1] == 14.0:
            layers[i][1] = layer_14
    for i in range(len(layers)):  # Assign layer properties to work points
        if layers[i][6] == 1.0:
            layers[i][6] = layer_1
        if layers[i][6] == 2.0:
            layers[i][6] = layer_2
        if layers[i][6] == 3.0:
            layers[i][6] = layer_3
        if layers[i][6] == 4.0:
            layers[i][6] = layer_4
        if layers[i][6] == 5.0:
            layers[i][6] = layer_5
        if layers[i][6] == 6.0:
            layers[i][6] = layer_6
        if layers[i][6] == 7.0:
            layers[i][6] = layer_7
        if layers[i][6] == 8.0:
            layers[i][6] = layer_8
        if layers[i][6] == 9.0:
            layers[i][6] = layer_9
        if layers[i][6] == 10.0:
            layers[i][6] = layer_10
        if layers[i][6] == 11.0:
            layers[i][6] = layer_11
        if layers[i][6] == 12.0:
            layers[i][6] = layer_12
        if layers[i][6] == 13.0:
            layers[i][6] = layer_13
        if layers[i][6] == 14.0:
            layers[i][6] = layer_14


    for i in range(len(layers)-1):
        if layers[i][0] >= supplied_elev >= layers[i+1][0]:
            layers.insert(i + 1, [round(supplied_elev, 2), layers[i][1], 0.0, 0.0, 0.0, 10000, layers[i][6]])
            work_points.insert(i + 1, [0, round(supplied_elev, 2)])
            break

    zero_length = []
    if ers_type == 1.0:
        for i in range(len(layers)-1):
            if layers[i][0] >= cut_elev >= layers[i+1][0]:
                if layers[i][1].type == 0:
                    layers.insert(i+2, [round(cut_elev-beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 2, [0, round(cut_elev - beam_type[4], 2)])
                    layers.insert(i + 3, [round(cut_elev - beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 3, [0, round(cut_elev - beam_type[4], 2)])
                    zero_length = beam_type[4]
                    break
                if layers[i][1].type == 1:
                    layers.insert(i+2, [round(cut_elev - 1.5*beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i+2, [0, round(cut_elev - 1.5*beam_type[4], 2)])
                    layers.insert(i + 3, [round(cut_elev - 1.5 * beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 3, [0, round(cut_elev - 1.5 * beam_type[4], 2)])
                    zero_length = 1.5*beam_type[4]
                    break

    # zero_length = []
    # if ers_type == 1.0:
    #     for i in range(len(layers) - 1):
    #         if layers[i][0] >= cut_elev >= layers[i + 1][0]:
    #             if layers[i][1].type == 0:
    #                 new_elev = round(cut_elev-beam_type[4], 2)
    #                 for j in range(len(layers) - 1):
    #                     if layers[j][0] > new_elev > layers[j + 1][0]:
    #                         layers.insert(j+1, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j+1, [0, new_elev])
    #                         layers.insert(j+2, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j+2, [0, new_elev])
    #                         zero_length = beam_type[4]
    #                         break
    #                 else:
    #                     continue  # executed if the loop ended normally (no break)
    #                 break  # executed if 'continue' was skipped (break)
    #             if layers[i][1].type == 1:
    #                 new_elev = round(cut_elev - 1.5*beam_type[4], 2)
    #                 for j in range(len(layers) - 1):
    #                     if layers[j][0] > new_elev > layers[j + 1][0]:
    #                         layers.insert(j+1, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j+1, [0, new_elev])
    #                         layers.insert(j+2, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j+2, [0, new_elev])
    #                         zero_length = 1.5*beam_type[4]
    #                         break
    #                 else:
    #                     continue  # executed if the loop ended normally (no break)
    #                 break  # executed if 'continue' was skipped (break)

    if berm_array != []:
        layers, work_points = berm_workpoints(layers, work_points, berm_array, cut_elev)

    if request.GET['footing_1_type'] != '':
        combined_footing_load = combine_footings(footings)
        layers, work_points = incorporate_footings(footings, combined_footing_load, layers, work_points, supplied_elev)

    if berm_array != []:
        layers = passive_heights(surface_side, berm_array, layers, cut_elev)

    if request.GET['train_1_distance'] != '':
        train_surcharge = combine_trains(trains)
        for i in range(len(layers)):
            for j in range(len(train_surcharge)):
                if layers[i][0] == train_surcharge[j][0]:
                    layers[i][4] = train_surcharge[j][1]

    wat_check = float(request.GET['wat_check'])
    if wat_check == 0:
        wat_output = []
        for i in range(len(layers)):
            layers[i].append(0)
    else:
        layers, wat_output = water_around_toe(layers, water_elev, cut_elev, supplied_elev)

    layers.sort(key=lambda x: x[0], reverse=True)

    footing_output = []
    for i in range(len(footings)):
        footing_output.append(text_output(footings[i], i+1))
    footing_output = list(itertools.chain.from_iterable(footing_output))
    total_footing_surcharge = []
    for i in range(len(layers)):
        total_footing_surcharge.append("At elevation " + str(layers[i][0]) + "', total footing surcharge = " +
                                       str(layers[i][3]) + " psf.")
    if footings == []:
        total_footing_surcharge = []
    train_output = ["All rail surcharges calculated using the Cooper E80 method."]
    for i in range(len(layers)):
        train_output.append("At elevation " + str(layers[i][0]) + "', total lateral rail surcharge = " +
                            str(layers[i][4]) + " psf.")
    if trains == []:
        train_output = []

    surcharge = surcharge_heights(surface_side, surface_array, work_points, angle, angle_change_elev, angle_change_type,
                                  min_surcharge_height)
    for i in range(len(surcharge)):
        layers[i][2] = surcharge_unit_weight*(surcharge[i][1] - layers[0][0])
    surcharge_output = []
    for i in range(len(surcharge)):
        surcharge_string = "At elevation " + str(surcharge[i][0]) + "', assume design soil height at elevation " + \
                           str(surcharge[i][1]) + "'."
        surcharge_output.append(surcharge_string)

    berm_output = []
    if berm_array != []:
        for i in range(len(layers)):
            berm_string = "At elevation " + str(layers[i][0]) + "', assume passive soil height at elevation " + \
                          str(layers[i][5]) + "'."
            berm_output.append(berm_string)
    berm_reduction_output = []

    active = active_pressures(layers, water_elev, total_weights)
    passive = passive_pressures(layers, water_cut_elev, cut_elev, total_weights)
    if berm_array != []:
        passive, berm_reduction_output = berm_reduction(layers, berm_array, cut_elev, passive, water_cut_elev,
                                                        total_weights)
    water = water_pressures(layers, water_elev, water_cut_elev, total_weights, supplied_elev)
    active_pressure = active_pressures_output(layers, water_elev, total_weights)
    passive_pressure = passive_pressures_output(layers, water_cut_elev, cut_elev, total_weights)
    water_pressure = water_pressures_output(water)
    net = net_pressures(active, passive, water, cut_elev, ers_type, beam_spacing, zero_length, beam_type,
                        soldier_beam_method)
    net_output = net[2]
    if top_sheet[0] != layers[0][0]:
        net[0].insert(0, 0)
        net[1].insert(0, net[1][0])
        net[0].insert(0, 0)
        net[1].insert(0, top_sheet[0])
    beam_output = []
    if ers_type == 1 and soldier_beam_method == 0:
        beam_output = [("Soldier Beam Analysis Effective Widths : " + beam_type[1] + " @ " + str(beam_spacing) +
                        "' spacing"),
                       ("From elevation " + str(net[1][0]) + "' to elevation " + str(cut_elev)+"': W = " +
                        str(beam_spacing) + "'"),
                       ("From elevation " + str(cut_elev) + "' to elevation " + str(round(cut_elev-zero_length, 2)) +
                        "': W = 0 (net active W =" + str(beam_type[4])+ "')"),
                       ("At elevation " + str(round(cut_elev-zero_length, 2)) + "' and below: W = 3*" +
                        str(beam_type[4]) + "' = " + str(round(3*beam_type[4], 2)) + "'")
                       ]
    if ers_type == 1 and soldier_beam_method == 1:
        beam_output = [("Soldier Beam Analysis Effective Widths : " + beam_type[1] + " @ " + str(beam_spacing) + "' spacing"),
                       ("From elevation " + str(net[1][0]) + "' to elevation " + str(cut_elev)+"': W = " + str(beam_spacing) + "'"),
                       ("From elevation " + str(cut_elev) + "' to elevation " + str(round(cut_elev-zero_length, 2)) +
                        "': W = 0 (net active W =" + str(beam_type[4]) + "')"),
                       ("At elevation " + str(round(cut_elev-zero_length, 2)) + "' and below: W = 3*" + str(beam_type[4]) +
                        "' = " + str(round(3*beam_type[4], 2)) + "' for the passive pressures, and W = " + str(beam_type[4]) +
                        "' for the active pressures.  Net pressure is limited negatively (passive side) by "
                        "(Pa-Pp)*beam spacing")
                       ]

    data = minimum_length(net, brace_elev)
    min_length = str(round(data[0], 2)) + "'"
    min_length_elev = str(round(data[1], 2)) + "'"
    waler_load = str(math.ceil(data[2])) + "#/'"
    design_text = data[3]
    min_length_pressure = data[4]
    multi = multiplier(net, brace_elev, data, supplied_length)
    moment = maximum_moment(net, data[2], brace_elev)
    max_moment_elevation = round(moment[1], 2)
    moment = math.ceil(moment[0])
    deflection = deflection_calc(net, brace_elev, data, sheet_type)
    zero_point = data[6]
    pressure_plot = braced_pressure_plot(layers, net, brace_elev, min_length_pressure, data[1], data[0], deflection,
                                         scale_factor, multi[1], multi[2], multi[3], zero_point)
    active_passive_plot = ap_plot(layers, active, passive, cut_elev, 0)
    water_pressure_plot = water_plot(layers, water)
    surface = surface_plot(surface_array, work_points)
    bending_stress = round(moment*12/1000/sheet_type[2], 2)
    save(pressure_plot, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/pressure_plot.html')
    save(active_passive_plot, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/active_passive_plot.html')
    save(water_pressure_plot, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/water_pressure_plot.html')
    save(surface, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/surface.html')

    if save_calculation_name != '':
        url_output = str(request.build_absolute_uri)
        saved_calc = SavedCalc(name=save_calculation_name, data=(request.GET['footing_1_type'],request.GET['footing_1_width'],request.GET['footing_1_distance'],request.GET['footing_1_elevation'],request.GET['footing_1_load'],request.GET['footing_1_spacing_1'],request.GET['footing_1_spacing_2'],request.GET['footing_2_type'],request.GET['footing_2_width'],request.GET['footing_2_distance'],request.GET['footing_2_elevation'],request.GET['footing_2_load'],request.GET['footing_2_spacing_1'],request.GET['footing_2_spacing_2'],request.GET['footing_3_type'],request.GET['footing_3_width'],request.GET['footing_3_distance'],request.GET['footing_3_elevation'],request.GET['footing_3_load'],request.GET['footing_3_spacing_1'],request.GET['footing_3_spacing_2'],request.GET['footing_4_type'],request.GET['footing_4_width'],request.GET['footing_4_distance'],request.GET['footing_4_elevation'],request.GET['footing_4_load'],request.GET['footing_4_spacing_1'],request.GET['footing_4_spacing_2'],request.GET['train_1_distance'],request.GET['train_1_load'],request.GET['train_1_tie_size'],request.GET['train_1_elevation'],request.GET['train_2_distance'],request.GET['train_2_load'],request.GET['train_2_tie_size'],request.GET['train_2_elevation'],request.GET['train_3_distance'],request.GET['train_3_load'],request.GET['train_3_tie_size'],request.GET['train_3_elevation'],request.GET['train_4_distance'],request.GET['train_4_load'],request.GET['train_4_tie_size'],request.GET['train_4_elevation'],request.GET['surface_side'],request.GET['point0x'],request.GET['point0y'],request.GET['point1x'],request.GET['point1y'],request.GET['point2x'],request.GET['point2y'],request.GET['point3x'],request.GET['point3y'],request.GET['point4x'],request.GET['point4y'],request.GET['point5x'],request.GET['point5y'],request.GET['point6x'],request.GET['point6y'],request.GET['point7x'],request.GET['point7y'],request.GET['point8x'],request.GET['point8y'],request.GET['point9x'],request.GET['point9y'],request.GET['point10x'],request.GET['point10y'],request.GET['point11x'],request.GET['point11y'],request.GET['point12x'],request.GET['point12y'],request.GET['point13x'],request.GET['point13y'],request.GET['berm0x'],request.GET['berm0y'],request.GET['berm1x'],request.GET['berm1y'],request.GET['berm2x'],request.GET['berm2y'],request.GET['berm3x'],request.GET['berm3y'],request.GET['berm4x'],request.GET['berm4y'],request.GET['berm5x'],request.GET['berm5y'],request.GET['berm6x'],request.GET['berm6y'],request.GET['berm7x'],request.GET['berm7y'],request.GET['berm8x'],request.GET['berm8y'],request.GET['berm9x'],request.GET['berm9y'],request.GET['berm10x'],request.GET['berm10y'],request.GET['berm11x'],request.GET['berm11y'],request.GET['berm12x'],request.GET['berm12y'],request.GET['berm13x'],request.GET['berm13y'],request.GET['1.name'],request.GET['1.type'],request.GET['1.gamma'],request.GET['1.qu'],request.GET['1.ka'],request.GET['1.kp'],request.GET['1.phi'],request.GET['2.name'],request.GET['2.type'],request.GET['2.gamma'],request.GET['2.qu'],request.GET['2.ka'],request.GET['2.kp'],request.GET['2.phi'],request.GET['3.name'],request.GET['3.type'],request.GET['3.gamma'],request.GET['3.qu'],request.GET['3.ka'],request.GET['3.kp'],request.GET['3.phi'],request.GET['4.name'],request.GET['4.type'],request.GET['4.gamma'],request.GET['4.qu'],request.GET['4.ka'],request.GET['4.kp'],request.GET['4.phi'],request.GET['5.name'],request.GET['5.type'],request.GET['5.gamma'],request.GET['5.qu'],request.GET['5.ka'],request.GET['5.kp'],request.GET['5.phi'],request.GET['6.name'],request.GET['6.type'],request.GET['6.gamma'],request.GET['6.qu'],request.GET['6.ka'],request.GET['6.kp'],request.GET['6.phi'],request.GET['7.name'],request.GET['7.type'],request.GET['7.gamma'],request.GET['7.qu'],request.GET['7.ka'],request.GET['7.kp'],request.GET['7.phi'],request.GET['8.name'],request.GET['8.type'],request.GET['8.gamma'],request.GET['8.qu'],request.GET['8.ka'],request.GET['8.kp'],request.GET['8.phi'],request.GET['9.name'],request.GET['9.type'],request.GET['9.gamma'],request.GET['9.qu'],request.GET['9.ka'],request.GET['9.kp'],request.GET['9.phi'],request.GET['10.name'],request.GET['10.type'],request.GET['10.gamma'],request.GET['10.qu'],request.GET['10.ka'],request.GET['10.kp'],request.GET['10.phi'],request.GET['11.name'],request.GET['11.type'],request.GET['11.gamma'],request.GET['11.qu'],request.GET['11.ka'],request.GET['11.kp'],request.GET['11.phi'],request.GET['12.name'],request.GET['12.type'],request.GET['12.gamma'],request.GET['12.qu'],request.GET['12.ka'],request.GET['12.kp'],request.GET['12.phi'],request.GET['13.name'],request.GET['13.type'],request.GET['13.gamma'],request.GET['13.qu'],request.GET['13.ka'],request.GET['13.kp'],request.GET['13.phi'],request.GET['14.name'],request.GET['14.type'],request.GET['14.gamma'],request.GET['14.qu'],request.GET['14.ka'],request.GET['14.kp'],request.GET['14.phi'],request.GET['wp1'],request.GET['wp1_layer'],request.GET['wp1_layer_front'],request.GET['wp2'],request.GET['wp2_layer'],request.GET['wp2_layer_front'],request.GET['wp3'],request.GET['wp3_layer'],request.GET['wp3_layer_front'],request.GET['wp4'],request.GET['wp4_layer'],request.GET['wp4_layer_front'],request.GET['wp5'],request.GET['wp5_layer'],request.GET['wp5_layer_front'],request.GET['wp6'],request.GET['wp6_layer'],request.GET['wp6_layer_front'],request.GET['wp7'],request.GET['wp7_layer'],request.GET['wp7_layer_front'],request.GET['wp8'],request.GET['wp8_layer'],request.GET['wp8_layer_front'],request.GET['wp9'],request.GET['wp9_layer'],request.GET['wp9_layer_front'],request.GET['wp10'],request.GET['wp10_layer'],request.GET['wp10_layer_front'],request.GET['wp11'],request.GET['wp11_layer'],request.GET['wp11_layer_front'],request.GET['wp12'],request.GET['wp12_layer'],request.GET['wp12_layer_front'],request.GET['wp13'],request.GET['wp13_layer'],request.GET['wp13_layer_front'],request.GET['wp14'],request.GET['wp14_layer'],request.GET['wp14_layer_front'],request.GET['wp15'],request.GET['wp15_layer'],request.GET['wp15_layer_front'],request.GET['wp16'],request.GET['wp16_layer'],request.GET['wp16_layer_front'],request.GET['wp17'],request.GET['wp17_layer'],request.GET['wp17_layer_front'],request.GET['wp18'],request.GET['wp18_layer'],request.GET['wp18_layer_front'],request.GET['wp19'],request.GET['wp19_layer'],request.GET['wp19_layer_front'],request.GET['wp20'],request.GET['wp20_layer'],request.GET['wp20_layer_front'],request.GET['wp21'],request.GET['wp21_layer'],request.GET['wp21_layer_front'],request.GET['wp22'],request.GET['wp22_layer'],request.GET['wp22_layer_front'],request.GET['wp23'],request.GET['wp23_layer'],request.GET['wp23_layer_front'],request.GET['wp24'],request.GET['wp24_layer'],request.GET['wp24_layer_front'],request.GET['wp25'],request.GET['wp25_layer'],request.GET['wp25_layer_front'],request.GET['wp26'],request.GET['wp26_layer'],request.GET['wp26_layer_front'],request.GET['wp27'],request.GET['wp27_layer'],request.GET['wp27_layer_front'],request.GET['wp28'],request.GET['wp28_layer'],request.GET['wp28_layer_front'],request.GET['wp29'],request.GET['wp29_layer'],request.GET['wp29_layer_front'],request.GET['wp30'],request.GET['wp30_layer'],request.GET['wp30_layer_front'],request.GET['wp31'],request.GET['wp31_layer'],request.GET['wp31_layer_front'],request.GET['wp32'],request.GET['wp32_layer'],request.GET['wp32_layer_front'],request.GET['wp33'],request.GET['wp33_layer'],request.GET['wp33_layer_front'],request.GET['wp34'],request.GET['wp34_layer'],request.GET['wp34_layer_front'],request.GET['wp35'],request.GET['wp35_layer'],request.GET['wp35_layer_front'],request.GET['wp36'],request.GET['wp36_layer'],request.GET['wp36_layer_front'],request.GET['wp37'],request.GET['wp37_layer'],request.GET['wp37_layer_front'],request.GET['wp38'],request.GET['wp38_layer'],request.GET['wp38_layer_front'],request.GET['wp39'],request.GET['wp39_layer'],request.GET['wp39_layer_front'],request.GET['wp40'],request.GET['wp40_layer'],request.GET['wp40_layer_front'],request.GET['surcharge_unit_weight'],request.GET['min_surcharge_height'],request.GET['angle'],request.GET['angle_change_elev'],request.GET['water_elev'],request.GET['cut_elev'],request.GET['total_weights'],request.GET['brace_elev'],request.GET['scale_factor'],request.GET['sheet_type'],request.GET['beam_type'],request.GET['water_cut_elev'],request.GET['top_sheet'],request.GET['beam_spacing'],request.GET['beam_size_override'],request.GET['beam_override'],request.GET['beam_modulus_override'],request.GET['beam_inertia_override'],request.GET['ers_type'],request.GET['soldier_beam_method'],request.GET['supplied_length'],request.GET['wat_check'], request.GET['angle_change_type'], request.GET['13.phi']),
                               type="One Layer Braced")
        saved_calc.save()

    return render(request, "output.html", {"surcharge": surcharge_output,
                                           "layers": layers,
                                           "active_pressures": active_pressure,
                                           "passive_pressures": passive_pressure,
                                           "water_pressures": water_pressure,
                                           "min_length": min_length,
                                           "min_length_elev": min_length_elev,
                                           "waler_load": waler_load,
                                           "design_text": design_text,
                                           "multiplier": multi[0],
                                           "moment": moment,
                                           "deflection": deflection[1],
                                           "deflection_elev": deflection[2],
                                           "footing_output": footing_output,
                                           "total_footing_surcharge": total_footing_surcharge,
                                           "sheet_type": sheet_type[1],
                                           "bending_stress": bending_stress,
                                           "train_output": train_output,
                                           "beam_output": beam_output,
                                           "wat_output": wat_output,
                                           "berm_output": berm_output,
                                           "berm_reduction_output": berm_reduction_output,
                                           "soldier_beam_method": soldier_beam_method,
                                           "net_output": net_output,
                                           "max_moment_elevation": max_moment_elevation,
                                           "min_length_work_moments": data[5],
                                           "multiplier_supplied_length": multi[4],
                                           "multiplier_value": round(multi[3], 2),
                                           "I": sheet_type[3],
                                           "Sx": sheet_type[2]
                                           })


def pressure_plot(request):
    return render(request, 'pressure_plot.html')


def active_passive_plot(request):
    return render(request, 'active_passive_plot.html')


def water_pressure_plot(request):
    return render(request, 'water_pressure_plot.html')


def cant_pp(request):
    return render(request, 'cant_pp.html')


def surface(request):
    return render(request, 'surface.html')


def strut_diagram(request):
    return render(request, 'strut_diagram.html')


def cant_output(request):
    # TAKE INPUT DATA FROM USER
    footings = []
    trains = []
    # footing_surcharge(type, width, distance, elevation, load, spacing_1, spacing_2)
    if request.GET['footing_1_type'] != '':
        footing_1 = footing_surcharge(float(request.GET['footing_1_type']),
                                      float(request.GET['footing_1_width']),
                                      float(request.GET['footing_1_distance']),
                                      float(request.GET['footing_1_elevation']),
                                      float(request.GET['footing_1_load']),
                                      float(request.GET['footing_1_spacing_1']),
                                      float(request.GET['footing_1_spacing_2']))
        footings.append(footing_1)
    if request.GET['footing_2_type'] != '':
        footing_2 = footing_surcharge(float(request.GET['footing_2_type']),
                                      float(request.GET['footing_2_width']),
                                      float(request.GET['footing_2_distance']),
                                      float(request.GET['footing_2_elevation']),
                                      float(request.GET['footing_2_load']),
                                      float(request.GET['footing_2_spacing_1']),
                                      float(request.GET['footing_2_spacing_2']))
        footings.append(footing_2)
    if request.GET['footing_3_type'] != '':
        footing_3 = footing_surcharge(float(request.GET['footing_3_type']),
                                      float(request.GET['footing_3_width']),
                                      float(request.GET['footing_3_distance']),
                                      float(request.GET['footing_3_elevation']),
                                      float(request.GET['footing_3_load']),
                                      float(request.GET['footing_3_spacing_1']),
                                      float(request.GET['footing_3_spacing_2']))
        footings.append(footing_3)
    if request.GET['footing_4_type'] != '':
        footing_4 = footing_surcharge(float(request.GET['footing_4_type']),
                                      float(request.GET['footing_4_width']),
                                      float(request.GET['footing_4_distance']),
                                      float(request.GET['footing_4_elevation']),
                                      float(request.GET['footing_4_load']),
                                      float(request.GET['footing_4_spacing_1']),
                                      float(request.GET['footing_4_spacing_2']))
        footings.append(footing_4)

    if request.GET['train_1_distance'] != '':
        train_1 = train_loading(float(request.GET['train_1_distance']),
                                float(request.GET['train_1_load']),
                                float(request.GET['train_1_tie_size']),
                                float(request.GET['train_1_elevation'])
                                )
        trains.append(train_1)
    if request.GET['train_2_distance'] != '':
        train_2 = train_loading(float(request.GET['train_2_distance']),
                                float(request.GET['train_2_load']),
                                float(request.GET['train_2_tie_size']),
                                float(request.GET['train_2_elevation'])
                                )
        trains.append(train_2)
    if request.GET['train_3_distance'] != '':
        train_3 = train_loading(float(request.GET['train_3_distance']),
                                float(request.GET['train_3_load']),
                                float(request.GET['train_3_tie_size']),
                                float(request.GET['train_3_elevation'])
                                )
        trains.append(train_3)
    if request.GET['train_4_distance'] != '':
        train_4 = train_loading(float(request.GET['train_4_distance']),
                                float(request.GET['train_4_load']),
                                float(request.GET['train_4_tie_size']),
                                float(request.GET['train_4_elevation'])
                                )
        trains.append(train_4)

    surface_side = float(request.GET['surface_side'])

    surface_array = [(request.GET['point0x'], request.GET['point0y']),
                     (request.GET['point1x'], request.GET['point1y']),
                     (request.GET['point2x'], request.GET['point2y']),
                     (request.GET['point3x'], request.GET['point3y']),
                     (request.GET['point4x'], request.GET['point4y']),
                     (request.GET['point5x'], request.GET['point5y']),
                     (request.GET['point6x'], request.GET['point6y']),
                     (request.GET['point7x'], request.GET['point7y']),
                     (request.GET['point8x'], request.GET['point8y']),
                     (request.GET['point9x'], request.GET['point9y']),
                     (request.GET['point10x'], request.GET['point10y']),
                     (request.GET['point11x'], request.GET['point11y']),
                     (request.GET['point12x'], request.GET['point12y']),
                     (request.GET['point13x'], request.GET['point13y'])]
    new_surface_array = []  # Remove all points with no entries
    for i in range(len(surface_array)):
        if surface_array[i] != ('', ''):
            new_surface_array.append(surface_array[i])
    surface_array = []
    for i in range(len(new_surface_array)):
        surface_array.append(((float(new_surface_array[i][0])), float(new_surface_array[i][1])))

    berm_array = []
    if request.GET['berm0x'] != '':
        berm_array = [(request.GET['berm0x'], request.GET['berm0y']),
                      (request.GET['berm1x'], request.GET['berm1y']),
                      (request.GET['berm2x'], request.GET['berm2y']),
                      (request.GET['berm3x'], request.GET['berm3y']),
                      (request.GET['berm4x'], request.GET['berm4y']),
                      (request.GET['berm5x'], request.GET['berm5y']),
                      (request.GET['berm6x'], request.GET['berm6y']),
                      (request.GET['berm7x'], request.GET['berm7y']),
                      (request.GET['berm8x'], request.GET['berm8y']),
                      (request.GET['berm9x'], request.GET['berm9y']),
                      (request.GET['berm10x'], request.GET['berm10y']),
                      (request.GET['berm11x'], request.GET['berm11y']),
                      (request.GET['berm12x'], request.GET['berm12y']),
                      (request.GET['berm13x'], request.GET['berm13y'])]
        new_berm_array = []  # Remove all points with no entries

        # Pare down surface array points to just the ones that were entered
        for i in range(len(berm_array)):
            if berm_array[i] != ('', ''):
                new_berm_array.append(berm_array[i])
        berm_array = []
        for i in range(len(new_berm_array)):
            berm_array.append(((float(new_berm_array[i][0])), float(new_berm_array[i][1])))

    if request.GET['1.name'] != '':  # If layer doesn't have a name, assume it does not exist and do not input it.
        layer_1 = Layer(request.GET['1.name'], float(request.GET['1.type']), float(request.GET['1.gamma']),
                        float(request.GET['1.qu']),
                        float(request.GET['1.ka']), float(request.GET['1.kp']),
                        float(request.GET['1.phi']))
    if request.GET['2.name'] != '':
        layer_2 = Layer(request.GET['2.name'], float(request.GET['2.type']), float(request.GET['2.gamma']),
                        float(request.GET['2.qu']),
                        float(request.GET['2.ka']), float(request.GET['2.kp']),
                        float(request.GET['2.phi']))
    if request.GET['3.name'] != '':
        layer_3 = Layer(request.GET['3.name'], float(request.GET['3.type']), float(request.GET['3.gamma']),
                        float(request.GET['3.qu']),
                        float(request.GET['3.ka']), float(request.GET['3.kp']),
                        float(request.GET['3.phi']))
    if request.GET['4.name'] != '':
        layer_4 = Layer(request.GET['4.name'], float(request.GET['4.type']), float(request.GET['4.gamma']),
                        float(request.GET['4.qu']),
                        float(request.GET['4.ka']), float(request.GET['4.kp']),
                        float(request.GET['4.phi']))
    if request.GET['5.name'] != '':
        layer_5 = Layer(request.GET['5.name'], float(request.GET['5.type']), float(request.GET['5.gamma']),
                        float(request.GET['5.qu']),
                        float(request.GET['5.ka']), float(request.GET['5.kp']),
                        float(request.GET['5.phi']))
    if request.GET['6.name'] != '':
        layer_6 = Layer(request.GET['6.name'], float(request.GET['6.type']), float(request.GET['6.gamma']),
                        float(request.GET['6.qu']),
                        float(request.GET['6.ka']), float(request.GET['6.kp']),
                        float(request.GET['6.phi']))
    if request.GET['7.name'] != '':
        layer_7 = Layer(request.GET['7.name'], float(request.GET['7.type']), float(request.GET['7.gamma']),
                        float(request.GET['7.qu']),
                        float(request.GET['7.ka']), float(request.GET['7.kp']),
                        float(request.GET['7.phi']))
    if request.GET['8.name'] != '':
        layer_8 = Layer(request.GET['8.name'], float(request.GET['8.type']), float(request.GET['8.gamma']),
                        float(request.GET['8.qu']),
                        float(request.GET['8.ka']), float(request.GET['8.kp']),
                        float(request.GET['8.phi']))
    if request.GET['9.name'] != '':
        layer_9 = Layer(request.GET['9.name'], float(request.GET['9.type']), float(request.GET['9.gamma']),
                        float(request.GET['9.qu']),
                        float(request.GET['9.ka']), float(request.GET['9.kp']),
                        float(request.GET['9.phi']))
    if request.GET['10.name'] != '':
        layer_10 = Layer(request.GET['10.name'], float(request.GET['10.type']), float(request.GET['10.gamma']),
                        float(request.GET['10.qu']),
                        float(request.GET['10.ka']), float(request.GET['10.kp']),
                        float(request.GET['10.phi']))
    if request.GET['11.name'] != '':
        layer_11 = Layer(request.GET['11.name'], float(request.GET['11.type']), float(request.GET['11.gamma']),
                        float(request.GET['11.qu']),
                        float(request.GET['11.ka']), float(request.GET['11.kp']),
                        float(request.GET['11.phi']))
    if request.GET['12.name'] != '':
        layer_12 = Layer(request.GET['12.name'], float(request.GET['12.type']), float(request.GET['12.gamma']),
                        float(request.GET['12.qu']),
                        float(request.GET['12.ka']), float(request.GET['12.kp']),
                        float(request.GET['12.phi']))
    if request.GET['13.name'] != '':
        layer_13 = Layer(request.GET['13.name'], float(request.GET['13.type']), float(request.GET['13.gamma']),
                        float(request.GET['13.qu']),
                        float(request.GET['13.ka']), float(request.GET['13.kp']),
                        float(request.GET['13.phi']))

    layers = [[request.GET['wp1'], request.GET['wp1_layer'], 0, 0, 0, 10000, request.GET['wp1_layer_front']],
              [request.GET['wp2'], request.GET['wp2_layer'], 0, 0, 0, 10000, request.GET['wp2_layer_front']],
              [request.GET['wp3'], request.GET['wp3_layer'], 0, 0, 0, 10000, request.GET['wp3_layer_front']],
              [request.GET['wp4'], request.GET['wp4_layer'], 0, 0, 0, 10000, request.GET['wp4_layer_front']],
              [request.GET['wp5'], request.GET['wp5_layer'], 0, 0, 0, 10000, request.GET['wp5_layer_front']],
              [request.GET['wp6'], request.GET['wp6_layer'], 0, 0, 0, 10000, request.GET['wp6_layer_front']],
              [request.GET['wp7'], request.GET['wp7_layer'], 0, 0, 0, 10000, request.GET['wp7_layer_front']],
              [request.GET['wp8'], request.GET['wp8_layer'], 0, 0, 0, 10000, request.GET['wp8_layer_front']],
              [request.GET['wp9'], request.GET['wp9_layer'], 0, 0, 0, 10000, request.GET['wp9_layer_front']],
              [request.GET['wp10'], request.GET['wp10_layer'], 0, 0, 0, 10000, request.GET['wp10_layer_front']],
              [request.GET['wp11'], request.GET['wp11_layer'], 0, 0, 0, 10000, request.GET['wp11_layer_front']],
              [request.GET['wp12'], request.GET['wp12_layer'], 0, 0, 0, 10000, request.GET['wp12_layer_front']],
              [request.GET['wp13'], request.GET['wp13_layer'], 0, 0, 0, 10000, request.GET['wp13_layer_front']],
              [request.GET['wp14'], request.GET['wp14_layer'], 0, 0, 0, 10000, request.GET['wp14_layer_front']],
              [request.GET['wp15'], request.GET['wp15_layer'], 0, 0, 0, 10000, request.GET['wp15_layer_front']],
              [request.GET['wp16'], request.GET['wp16_layer'], 0, 0, 0, 10000, request.GET['wp16_layer_front']],
              [request.GET['wp17'], request.GET['wp17_layer'], 0, 0, 0, 10000, request.GET['wp17_layer_front']],
              [request.GET['wp18'], request.GET['wp18_layer'], 0, 0, 0, 10000, request.GET['wp18_layer_front']],
              [request.GET['wp19'], request.GET['wp19_layer'], 0, 0, 0, 10000, request.GET['wp19_layer_front']],
              [request.GET['wp20'], request.GET['wp20_layer'], 0, 0, 0, 10000, request.GET['wp20_layer_front']],
              [request.GET['wp21'], request.GET['wp21_layer'], 0, 0, 0, 10000, request.GET['wp21_layer_front']],
              [request.GET['wp22'], request.GET['wp22_layer'], 0, 0, 0, 10000, request.GET['wp22_layer_front']],
              [request.GET['wp23'], request.GET['wp23_layer'], 0, 0, 0, 10000, request.GET['wp23_layer_front']],
              [request.GET['wp24'], request.GET['wp24_layer'], 0, 0, 0, 10000, request.GET['wp24_layer_front']],
              [request.GET['wp25'], request.GET['wp25_layer'], 0, 0, 0, 10000, request.GET['wp25_layer_front']],
              [request.GET['wp26'], request.GET['wp26_layer'], 0, 0, 0, 10000, request.GET['wp26_layer_front']],
              [request.GET['wp27'], request.GET['wp27_layer'], 0, 0, 0, 10000, request.GET['wp27_layer_front']],
              [request.GET['wp28'], request.GET['wp28_layer'], 0, 0, 0, 10000, request.GET['wp28_layer_front']],
              [request.GET['wp29'], request.GET['wp29_layer'], 0, 0, 0, 10000, request.GET['wp29_layer_front']],
              [request.GET['wp30'], request.GET['wp30_layer'], 0, 0, 0, 10000, request.GET['wp30_layer_front']]]


    new_layers = []  # Remove all layers with no entries
    for i in range(len(layers)):
        if layers[i] != ['', '', 0, 0, 0, 10000, '']:
            new_layers.append(layers[i])
    layers = []
    for i in range(len(new_layers)):
        layers.append([float(new_layers[i][0]), float(new_layers[i][1]), float(new_layers[i][2]),
                       float(new_layers[i][3]), float(new_layers[i][4]), float(new_layers[i][5]),
                       float(new_layers[i][6])])

    work_points = [[0, request.GET['wp1']],
                   [0, request.GET['wp2']],
                   [0, request.GET['wp3']],
                   [0, request.GET['wp4']],
                   [0, request.GET['wp5']],
                   [0, request.GET['wp6']],
                   [0, request.GET['wp7']],
                   [0, request.GET['wp8']],
                   [0, request.GET['wp9']],
                   [0, request.GET['wp10']],
                   [0, request.GET['wp11']],
                   [0, request.GET['wp12']],
                   [0, request.GET['wp13']],
                   [0, request.GET['wp14']],
                   [0, request.GET['wp15']],
                   [0, request.GET['wp16']],
                   [0, request.GET['wp17']],
                   [0, request.GET['wp18']],
                   [0, request.GET['wp21']],
                   [0, request.GET['wp22']],
                   [0, request.GET['wp23']],
                   [0, request.GET['wp24']],
                   [0, request.GET['wp25']],
                   [0, request.GET['wp26']],
                   [0, request.GET['wp27']],
                   [0, request.GET['wp28']],
                   [0, request.GET['wp29']],
                   [0, request.GET['wp30']]]


    new_work_points = []  # Remove all points with no entries
    for i in range(len(work_points)):
        if work_points[i] != [0, '']:
            new_work_points.append(work_points[i])
    work_points = []
    for i in range(len(new_work_points)):
        work_points.append([(float(new_work_points[i][0])), float(new_work_points[i][1])])

    surcharge_unit_weight = float(request.GET['surcharge_unit_weight'])

    min_surcharge_height = request.GET['min_surcharge_height']
    if min_surcharge_height:
        min_surcharge_height = float(min_surcharge_height)
    else:
        min_surcharge_height = []

    angle = float(request.GET['angle'])

    angle_change_elev = request.GET['angle_change_elev']
    if angle_change_elev:
        angle_change_elev = float(angle_change_elev)
    else:
        angle_change_elev = []

    angle_change_type = float(request.GET['angle_change_type'])

    water_elev = request.GET['water_elev']
    if water_elev:
        water_elev = float(water_elev)
    else:
        water_elev = float(-10000)

    cut_elev = float(request.GET['cut_elev'])
    total_weights = float(request.GET['total_weights'])
    surface_elev = float(request.GET['surface_elev'])
    scale_factor = float(request.GET['scale_factor'])
    sheet_type = float(request.GET['sheet_type'])
    beam_type = float(request.GET['beam_type'])
    beam_spacing = []

    water_cut_elev = cut_elev
    if water_elev == float(-10000):
        water_cut_elev = float(-10000)
    if request.GET['water_cut_elev'] != '':
        water_cut_elev = float(request.GET['water_cut_elev'])

    top_sheet = [layers[0][0]]
    if request.GET['top_sheet'] != '':
        top_sheet = [float(request.GET['top_sheet'])]
    for i in range(len(sheet_database)):
        if sheet_type == sheet_database[i][0]:
            sheet_type = sheet_database[i]
    for i in range(len(beam_database)):
        if beam_type == beam_database[i][0]:
            beam_type = beam_database[i]

    if request.GET['beam_spacing'] != '':
        beam_spacing = float(request.GET['beam_spacing'])
    if request.GET['beam_size_override'] != '':
        beam_type[4] = float(request.GET['beam_size_override'])/12
    if request.GET['beam_override'] != '':
        beam_type[1] = request.GET['beam_override']
    if request.GET['beam_modulus_override'] != '':
        beam_type[2] = float(request.GET["beam_modulus_override"])
    if request.GET['beam_inertia_override'] != '':
        beam_type[3] = float(request.GET["beam_inertia_override"])

    ers_type = float(request.GET['ers_type'])
    if ers_type == 1:
        sheet_type = beam_type

    soldier_beam_method = float(request.GET['soldier_beam_method'])

    supplied_length = float(request.GET['supplied_length'])
    supplied_elev = top_sheet[0] - supplied_length

    multiplier_skip = float(request.GET['multiplier_skip'])

    save_calculation_name = request.GET['save_calculation_name']

    # MANIPULATE USER DATA
    for i in range(len(layers)):  # Assign layer properties to work points
        if layers[i][1] == 1.0:
            layers[i][1] = layer_1
        if layers[i][1] == 2.0:
            layers[i][1] = layer_2
        if layers[i][1] == 3.0:
            layers[i][1] = layer_3
        if layers[i][1] == 4.0:
            layers[i][1] = layer_4
        if layers[i][1] == 5.0:
            layers[i][1] = layer_5
        if layers[i][1] == 6.0:
            layers[i][1] = layer_6
        if layers[i][1] == 7.0:
            layers[i][1] = layer_7
        if layers[i][1] == 8.0:
            layers[i][1] = layer_8
        if layers[i][1] == 9.0:
            layers[i][1] = layer_9
        if layers[i][1] == 10.0:
            layers[i][1] = layer_10
        if layers[i][1] == 11.0:
            layers[i][1] = layer_11
        if layers[i][1] == 12.0:
            layers[i][1] = layer_12
        if layers[i][1] == 13.0:
            layers[i][1] = layer_13

    for i in range(len(layers)):  # Assign layer properties to work points
        if layers[i][6] == 1.0:
            layers[i][6] = layer_1
        if layers[i][6] == 2.0:
            layers[i][6] = layer_2
        if layers[i][6] == 3.0:
            layers[i][6] = layer_3
        if layers[i][6] == 4.0:
            layers[i][6] = layer_4
        if layers[i][6] == 5.0:
            layers[i][6] = layer_5
        if layers[i][6] == 6.0:
            layers[i][6] = layer_6
        if layers[i][6] == 7.0:
            layers[i][6] = layer_7
        if layers[i][6] == 8.0:
            layers[i][6] = layer_8
        if layers[i][6] == 9.0:
            layers[i][6] = layer_9
        if layers[i][6] == 10.0:
            layers[i][6] = layer_10
        if layers[i][6] == 11.0:
            layers[i][6] = layer_11
        if layers[i][6] == 12.0:
            layers[i][6] = layer_12
        if layers[i][6] == 13.0:
            layers[i][6] = layer_13

    for i in range(len(layers)-1):
        if layers[i][0] >= supplied_elev >= layers[i+1][0]:
            layers.insert(i + 1, [round(supplied_elev, 2), layers[i][1], 0.0, 0.0, 0.0, 10000, layers[i][6]])
            work_points.insert(i + 1, [0, round(supplied_elev, 2)])
            break

    zero_length = []
    if ers_type == 1.0:
        for i in range(len(layers) - 1):
            if layers[i][0] >= cut_elev >= layers[i + 1][0]:
                if layers[i][1].type == 0:
                    layers.insert(i + 2, [round(cut_elev - beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 2, [0, round(cut_elev - beam_type[4], 2)])
                    layers.insert(i + 3, [round(cut_elev - beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 3, [0, round(cut_elev - beam_type[4], 2)])
                    zero_length = beam_type[4]
                    break
                if layers[i][1].type == 1:
                    layers.insert(i + 2, [round(cut_elev - 1.5 * beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 2, [0, round(cut_elev - 1.5 * beam_type[4], 2)])
                    layers.insert(i + 3, [round(cut_elev - 1.5 * beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 3, [0, round(cut_elev - 1.5 * beam_type[4], 2)])
                    zero_length = 1.5 * beam_type[4]
                    break

    # zero_length = []
    # if ers_type == 1.0:
    #     for i in range(len(layers) - 1):
    #         if layers[i][0] >= cut_elev >= layers[i + 1][0]:
    #             if layers[i][1].type == 0:
    #                 new_elev = round(cut_elev - beam_type[4], 2)
    #                 for j in range(len(layers) - 1):
    #                     if layers[j][0] > new_elev > layers[j + 1][0]:
    #                         layers.insert(j + 1, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j + 1, [0, new_elev])
    #                         layers.insert(j + 2, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j + 2, [0, new_elev])
    #                         zero_length = beam_type[4]
    #                         break
    #                 else:
    #                     continue  # executed if the loop ended normally (no break)
    #                 break  # executed if 'continue' was skipped (break)
    #             if layers[i][1].type == 1:
    #                 new_elev = round(cut_elev - 1.5 * beam_type[4], 2)
    #                 for j in range(len(layers) - 1):
    #                     if layers[j][0] > new_elev > layers[j + 1][0]:
    #                         layers.insert(j + 1, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j + 1, [0, new_elev])
    #                         layers.insert(j + 2, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j + 2, [0, new_elev])
    #                         zero_length = 1.5*beam_type[4]
    #                         break
    #                 else:
    #                     continue  # executed if the loop ended normally (no break)
    #                 break  # executed if 'continue' was skipped (break)

    if berm_array != []:
        layers, work_points = berm_workpoints(layers, work_points, berm_array, cut_elev)

    if request.GET['footing_1_type'] != '':
        combined_footing_load = combine_footings(footings)
        layers, work_points = incorporate_footings(footings, combined_footing_load, layers, work_points, supplied_elev)

    if berm_array != []:
        layers = passive_heights(surface_side, berm_array, layers, cut_elev)

    if request.GET['train_1_distance'] != '':
        train_surcharge = combine_trains(trains)
        for i in range(len(layers)):
            for j in range(len(train_surcharge)):
                if layers[i][0] == train_surcharge[j][0]:
                    layers[i][4] = train_surcharge[j][1]

    wat_check = float(request.GET['wat_check'])
    if wat_check == 0:
        wat_output = []
        for i in range(len(layers)):
            layers[i].append(0)
    else:
        layers, wat_output = water_around_toe(layers, water_elev, cut_elev, supplied_elev)

    layers.sort(key=lambda x: x[0], reverse=True)

    footing_output = []
    for i in range(len(footings)):
        footing_output.append(text_output(footings[i], i + 1))
    footing_output = list(itertools.chain.from_iterable(footing_output))
    total_footing_surcharge = []
    for i in range(len(layers)):
        total_footing_surcharge.append("At elevation " + str(layers[i][0]) + "', total footing surcharge = " +
                                       str(layers[i][3]) + " psf.")

    if footings == []:
        total_footing_surcharge = []
    train_output = ["All rail surcharges calculated using the Cooper E80 method."]
    for i in range(len(layers)):
        train_output.append("At elevation " + str(layers[i][0]) + "', total lateral rail surcharge = " +
                            str(layers[i][4]) + " psf.")
    if trains == []:
        train_output = []

    surcharge = surcharge_heights(surface_side, surface_array, work_points, angle, angle_change_elev, angle_change_type,
                                  min_surcharge_height)
    for i in range(len(surcharge)):
        layers[i][2] = surcharge_unit_weight * (surcharge[i][1] - layers[0][0])
    surcharge_output = []
    for i in range(len(surcharge)):
        surcharge_string = "At elevation " + str(surcharge[i][0]) + "', assume design soil height at elevation " + \
                           str(surcharge[i][1]) + "'."
        surcharge_output.append(surcharge_string)

    berm_output = []
    if berm_array != []:
        for i in range(len(layers)):
            berm_string = "At elevation " + str(layers[i][0]) + "', assume passive soil height at elevation " + \
                           str(layers[i][5]) + "'."
            berm_output.append(berm_string)
    berm_reduction_output = []

    active = active_pressures(layers, water_elev, total_weights)
    passive = passive_pressures(layers, water_cut_elev, cut_elev, total_weights)
    if berm_array != []:
        passive, berm_reduction_output = berm_reduction(layers, berm_array, cut_elev, passive, water_cut_elev, total_weights)
    water = water_pressures(layers, water_elev, water_cut_elev, total_weights, supplied_elev)
    active_pressure = active_pressures_output(layers, water_elev, total_weights)
    passive_pressure = passive_pressures_output(layers, water_cut_elev, cut_elev, total_weights)
    water_pressure = water_pressures_output(water)
    active_cant = active_pressures_front(layers, water_cut_elev, cut_elev, total_weights)
    passive_cant = passive_pressures_back(layers, water_elev, cut_elev, surface_elev, total_weights)
    active_pressure_front = active_pressures_front_output(layers, water_cut_elev, cut_elev, total_weights)
    passive_pressure_back = passive_pressures_back_output(layers, water_elev, cut_elev, surface_elev, total_weights)
    net = net_pressures(active, passive, water, cut_elev, ers_type, beam_spacing, zero_length, beam_type,
                        soldier_beam_method)
    net_output = net[2]
    if top_sheet[0] != layers[0][0]:
        net[0].insert(0, 0)
        net[1].insert(0, net[1][0])
        net[0].insert(0, 0)
        net[1].insert(0, top_sheet[0])
    beam_output = []
    if ers_type == 1 and soldier_beam_method == 0:
        beam_output = [("Soldier Beam Analysis Effective Widths : " + beam_type[1] + " @ " + str(beam_spacing) + "' spacing"),
                       ("From elevation " + str(net[1][0]) + "' to elevation " + str(cut_elev)+"': W = " + str(beam_spacing) + "'"),
                       ("From elevation " + str(cut_elev) + "' to elevation " + str(round(cut_elev-zero_length, 2)) +
                        "': W = 0 (net active W ="+ str(beam_type[4])+ "')"),
                       ("At elevation " + str(round(cut_elev-zero_length, 2)) + "' and below: W = 3*" + str(beam_type[4]) +
                        "' = " + str(round(3*beam_type[4], 2)) + "'")
                       ]
    if ers_type == 1 and soldier_beam_method == 1:
        beam_output = [("Soldier Beam Analysis Effective Widths : " + beam_type[1] + " @ " + str(beam_spacing) + "' spacing"),
                       ("From elevation " + str(net[1][0]) + "' to elevation " + str(cut_elev)+"': W = " + str(beam_spacing) + "'"),
                       ("From elevation " + str(cut_elev) + "' to elevation " + str(round(cut_elev-zero_length, 2)) +
                        "': W = 0 (net active W =" + str(beam_type[4]) + "')"),
                       ("At elevation " + str(round(cut_elev-zero_length, 2)) + "' and below: W = 3*" + str(beam_type[4]) +
                        "' = " + str(round(3*beam_type[4], 2)) + "' for the passive pressures, and W = " + str(beam_type[4]) +
                        "' for the active pressures.  Net pressure is limited negatively (passive side) by "
                        "(Pa-Pp)*beam spacing")
                       ]
    cant = cant_pressures(active_cant, passive_cant, water, cut_elev, ers_type, beam_spacing, zero_length, beam_type, soldier_beam_method)
    cant_output = cant[2]
    data = minimum_length_cantilever(net, cant, cut_elev)
    min_length = str(round(data[0], 2)) + "'"
    min_length_elev = str(round(data[1], 2)) + "'"
    design_text = data[2]
    min_length_net_pressure = round(data[3])
    min_length_cant_pressure = round(data[4])
    if multiplier_skip == 0:
        multi = multiplier_cantilever(net, cant, data, cut_elev, supplied_length)
    else:
        multi = [[], [], [], 0, []]
    moment = maximum_moment_cantilever(net)
    max_moment_elevation = round(moment[1],2)
    moment = math.ceil(moment[0])
    deflection = deflection_calc_cantilever(net, data, sheet_type)
    zero_point = data[9]
    pressure_plot = cant_pressure_plot(layers, net, min_length_cant_pressure, min_length_net_pressure, data[1], data[0],
                                       data[5], deflection, scale_factor, cant, multi[1], multi[2], multi[3], zero_point)
    active_passive_plot = ap_plot(layers, active, passive, cut_elev, 0)
    cantilever_pressure_plot = ap_plot(layers, active_cant, passive_cant, cut_elev, 1)
    water_pressure_plot = water_plot(layers, water)
    surface = surface_plot(surface_array, work_points)
    bending_stress = round(moment * 12 / 1000 / sheet_type[2], 2)
    save(pressure_plot, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/pressure_plot.html')
    save(active_passive_plot, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/active_passive_plot.html')
    save(cantilever_pressure_plot, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/cant_pp.html')
    save(water_pressure_plot, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/water_pressure_plot.html')
    save(surface, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/surface.html')

    if save_calculation_name != '':
        url_output = str(request.build_absolute_uri)
        saved_calc = SavedCalc(name=save_calculation_name, data=(request.GET['footing_1_type'],request.GET['footing_1_width'],request.GET['footing_1_distance'],request.GET['footing_1_elevation'],request.GET['footing_1_load'],request.GET['footing_1_spacing_1'],request.GET['footing_1_spacing_2'],request.GET['footing_2_type'],request.GET['footing_2_width'],request.GET['footing_2_distance'],request.GET['footing_2_elevation'],request.GET['footing_2_load'],request.GET['footing_2_spacing_1'],request.GET['footing_2_spacing_2'],request.GET['footing_3_type'],request.GET['footing_3_width'],request.GET['footing_3_distance'],request.GET['footing_3_elevation'],request.GET['footing_3_load'],request.GET['footing_3_spacing_1'],request.GET['footing_3_spacing_2'],request.GET['footing_4_type'],request.GET['footing_4_width'],request.GET['footing_4_distance'],request.GET['footing_4_elevation'],request.GET['footing_4_load'],request.GET['footing_4_spacing_1'],request.GET['footing_4_spacing_2'],request.GET['train_1_distance'],request.GET['train_1_load'],request.GET['train_1_tie_size'],request.GET['train_1_elevation'],request.GET['train_2_distance'],request.GET['train_2_load'],request.GET['train_2_tie_size'],request.GET['train_2_elevation'],request.GET['train_3_distance'],request.GET['train_3_load'],request.GET['train_3_tie_size'],request.GET['train_3_elevation'],request.GET['train_4_distance'],request.GET['train_4_load'],request.GET['train_4_tie_size'],request.GET['train_4_elevation'],request.GET['surface_side'],request.GET['point0x'],request.GET['point0y'],request.GET['point1x'],request.GET['point1y'],request.GET['point2x'],request.GET['point2y'],request.GET['point3x'],request.GET['point3y'],request.GET['point4x'],request.GET['point4y'],request.GET['point5x'],request.GET['point5y'],request.GET['point6x'],request.GET['point6y'],request.GET['point7x'],request.GET['point7y'],request.GET['point8x'],request.GET['point8y'],request.GET['point9x'],request.GET['point9y'],request.GET['point10x'],request.GET['point10y'],request.GET['point11x'],request.GET['point11y'],request.GET['point12x'],request.GET['point12y'],request.GET['point13x'],request.GET['point13y'],request.GET['berm0x'],request.GET['berm0y'],request.GET['berm1x'],request.GET['berm1y'],request.GET['berm2x'],request.GET['berm2y'],request.GET['berm3x'],request.GET['berm3y'],request.GET['berm4x'],request.GET['berm4y'],request.GET['berm5x'],request.GET['berm5y'],request.GET['berm6x'],request.GET['berm6y'],request.GET['berm7x'],request.GET['berm7y'],request.GET['berm8x'],request.GET['berm8y'],request.GET['berm9x'],request.GET['berm9y'],request.GET['berm10x'],request.GET['berm10y'],request.GET['berm11x'],request.GET['berm11y'],request.GET['berm12x'],request.GET['berm12y'],request.GET['berm13x'],request.GET['berm13y'],request.GET['1.name'],request.GET['1.type'],request.GET['1.gamma'],request.GET['1.qu'],request.GET['1.ka'],request.GET['1.kp'],request.GET['1.phi'],request.GET['2.name'],request.GET['2.type'],request.GET['2.gamma'],request.GET['2.qu'],request.GET['2.ka'],request.GET['2.kp'],request.GET['2.phi'],request.GET['3.name'],request.GET['3.type'],request.GET['3.gamma'],request.GET['3.qu'],request.GET['3.ka'],request.GET['3.kp'],request.GET['3.phi'],request.GET['4.name'],request.GET['4.type'],request.GET['4.gamma'],request.GET['4.qu'],request.GET['4.ka'],request.GET['4.kp'],request.GET['4.phi'],request.GET['5.name'],request.GET['5.type'],request.GET['5.gamma'],request.GET['5.qu'],request.GET['5.ka'],request.GET['5.kp'],request.GET['5.phi'],request.GET['6.name'],request.GET['6.type'],request.GET['6.gamma'],request.GET['6.qu'],request.GET['6.ka'],request.GET['6.kp'],request.GET['6.phi'],request.GET['7.name'],request.GET['7.type'],request.GET['7.gamma'],request.GET['7.qu'],request.GET['7.ka'],request.GET['7.kp'],request.GET['7.phi'],request.GET['8.name'],request.GET['8.type'],request.GET['8.gamma'],request.GET['8.qu'],request.GET['8.ka'],request.GET['8.kp'],request.GET['8.phi'],request.GET['9.name'],request.GET['9.type'],request.GET['9.gamma'],request.GET['9.qu'],request.GET['9.ka'],request.GET['9.kp'],request.GET['9.phi'],request.GET['10.name'],request.GET['10.type'],request.GET['10.gamma'],request.GET['10.qu'],request.GET['10.ka'],request.GET['10.kp'],request.GET['10.phi'],request.GET['11.name'],request.GET['11.type'],request.GET['11.gamma'],request.GET['11.qu'],request.GET['11.ka'],request.GET['11.kp'],request.GET['11.phi'],request.GET['12.name'],request.GET['12.type'],request.GET['12.gamma'],request.GET['12.qu'],request.GET['12.ka'],request.GET['12.kp'],request.GET['12.phi'],request.GET['13.name'],request.GET['13.type'],request.GET['13.gamma'],request.GET['13.qu'],request.GET['13.ka'],request.GET['13.kp'],request.GET['13.phi'],request.GET['14.name'],request.GET['14.type'],request.GET['14.gamma'],request.GET['14.qu'],request.GET['14.ka'],request.GET['14.kp'],request.GET['14.phi'],request.GET['wp1'],request.GET['wp1_layer'],request.GET['wp1_layer_front'],request.GET['wp2'],request.GET['wp2_layer'],request.GET['wp2_layer_front'],request.GET['wp3'],request.GET['wp3_layer'],request.GET['wp3_layer_front'],request.GET['wp4'],request.GET['wp4_layer'],request.GET['wp4_layer_front'],request.GET['wp5'],request.GET['wp5_layer'],request.GET['wp5_layer_front'],request.GET['wp6'],request.GET['wp6_layer'],request.GET['wp6_layer_front'],request.GET['wp7'],request.GET['wp7_layer'],request.GET['wp7_layer_front'],request.GET['wp8'],request.GET['wp8_layer'],request.GET['wp8_layer_front'],request.GET['wp9'],request.GET['wp9_layer'],request.GET['wp9_layer_front'],request.GET['wp10'],request.GET['wp10_layer'],request.GET['wp10_layer_front'],request.GET['wp11'],request.GET['wp11_layer'],request.GET['wp11_layer_front'],request.GET['wp12'],request.GET['wp12_layer'],request.GET['wp12_layer_front'],request.GET['wp13'],request.GET['wp13_layer'],request.GET['wp13_layer_front'],request.GET['wp14'],request.GET['wp14_layer'],request.GET['wp14_layer_front'],request.GET['wp15'],request.GET['wp15_layer'],request.GET['wp15_layer_front'],request.GET['wp16'],request.GET['wp16_layer'],request.GET['wp16_layer_front'],request.GET['wp17'],request.GET['wp17_layer'],request.GET['wp17_layer_front'],request.GET['wp18'],request.GET['wp18_layer'],request.GET['wp18_layer_front'],request.GET['wp19'],request.GET['wp19_layer'],request.GET['wp19_layer_front'],request.GET['wp20'],request.GET['wp20_layer'],request.GET['wp20_layer_front'],request.GET['wp21'],request.GET['wp21_layer'],request.GET['wp21_layer_front'],request.GET['wp22'],request.GET['wp22_layer'],request.GET['wp22_layer_front'],request.GET['wp23'],request.GET['wp23_layer'],request.GET['wp23_layer_front'],request.GET['wp24'],request.GET['wp24_layer'],request.GET['wp24_layer_front'],request.GET['wp25'],request.GET['wp25_layer'],request.GET['wp25_layer_front'],request.GET['wp26'],request.GET['wp26_layer'],request.GET['wp26_layer_front'],request.GET['wp27'],request.GET['wp27_layer'],request.GET['wp27_layer_front'],request.GET['wp28'],request.GET['wp28_layer'],request.GET['wp28_layer_front'],request.GET['wp29'],request.GET['wp29_layer'],request.GET['wp29_layer_front'],request.GET['wp30'],request.GET['wp30_layer'],request.GET['wp30_layer_front'],request.GET['surcharge_unit_weight'],request.GET['min_surcharge_height'],request.GET['angle'],request.GET['angle_change_elev'],request.GET['water_elev'],request.GET['cut_elev'],request.GET['total_weights'],request.GET['scale_factor'],request.GET['sheet_type'],request.GET['beam_type'],request.GET['water_cut_elev'],request.GET['top_sheet'],request.GET['beam_spacing'],request.GET['beam_size_override'],request.GET['beam_override'],request.GET['beam_modulus_override'],request.GET['beam_inertia_override'],request.GET['ers_type'],request.GET['soldier_beam_method'],request.GET['supplied_length'],request.GET['wat_check'],request.GET['angle_change_type'],request.GET['surface_elev']),
                               type="Cantilever")
        saved_calc.save()



    return render(request, "cant_output.html", {"surcharge": surcharge_output,
                                                "layers": layers,
                                                "active_pressures": active_pressure,
                                                "passive_pressures": passive_pressure,
                                                "water_pressures": water_pressure,
                                                "active_pressure_front": active_pressure_front,
                                                "passive_pressure_back": passive_pressure_back,
                                                "min_length": min_length,
                                                "min_length_elev": min_length_elev,
                                                "footing_output": footing_output,
                                                "total_footing_surcharge": total_footing_surcharge,
                                                "sheet_type": sheet_type[1],
                                                "train_output": train_output,
                                                "design_text": design_text,
                                                "moment": moment,
                                                "multiplier": multi[0],
                                                "deflection": deflection[1],
                                                "deflection_elev": deflection[2],
                                                "bending_stress": bending_stress,
                                                "surface": surface,
                                                "beam_output": beam_output,
                                                "wat_output": wat_output,
                                                "berm_output": berm_output,
                                                "berm_reduction_output": berm_reduction_output,
                                                "soldier_beam_method": soldier_beam_method,
                                                "net_output": net_output,
                                                "cant_output": cant_output,
                                                "max_moment_elevation": max_moment_elevation,
                                                "min_length_work_forces": data[7],
                                                "min_length_work_moments": data[8],
                                                "multiplier_supplied_length": multi[4],
                                                "multiplier_value": round(multi[3], 2),
                                                "I": sheet_type[3],
                                                "Sx": sheet_type[2]
                                                })


def multi_output(request):
    # TAKE INPUT DATA FROM USER
    footings = []
    trains = []
    # footing_surcharge(type, width, distance, elevation, load, spacing_1, spacing_2)
    if request.GET['footing_1_type'] != '':
        footing_1 = footing_surcharge(float(request.GET['footing_1_type']),
                                      float(request.GET['footing_1_width']),
                                      float(request.GET['footing_1_distance']),
                                      float(request.GET['footing_1_elevation']),
                                      float(request.GET['footing_1_load']),
                                      float(request.GET['footing_1_spacing_1']),
                                      float(request.GET['footing_1_spacing_2']))
        footings.append(footing_1)
    if request.GET['footing_2_type'] != '':
        footing_2 = footing_surcharge(float(request.GET['footing_2_type']),
                                      float(request.GET['footing_2_width']),
                                      float(request.GET['footing_2_distance']),
                                      float(request.GET['footing_2_elevation']),
                                      float(request.GET['footing_2_load']),
                                      float(request.GET['footing_2_spacing_1']),
                                      float(request.GET['footing_2_spacing_2']))
        footings.append(footing_2)
    if request.GET['footing_3_type'] != '':
        footing_3 = footing_surcharge(float(request.GET['footing_3_type']),
                                      float(request.GET['footing_3_width']),
                                      float(request.GET['footing_3_distance']),
                                      float(request.GET['footing_3_elevation']),
                                      float(request.GET['footing_3_load']),
                                      float(request.GET['footing_3_spacing_1']),
                                      float(request.GET['footing_3_spacing_2']))
        footings.append(footing_3)
    if request.GET['footing_4_type'] != '':
        footing_4 = footing_surcharge(float(request.GET['footing_4_type']),
                                      float(request.GET['footing_4_width']),
                                      float(request.GET['footing_4_distance']),
                                      float(request.GET['footing_4_elevation']),
                                      float(request.GET['footing_4_load']),
                                      float(request.GET['footing_4_spacing_1']),
                                      float(request.GET['footing_4_spacing_2']))
        footings.append(footing_4)

    if request.GET['train_1_distance'] != '':
        train_1 = train_loading(float(request.GET['train_1_distance']),
                                float(request.GET['train_1_load']),
                                float(request.GET['train_1_tie_size']),
                                float(request.GET['train_1_elevation'])
                                )
        trains.append(train_1)
    if request.GET['train_2_distance'] != '':
        train_2 = train_loading(float(request.GET['train_2_distance']),
                                float(request.GET['train_2_load']),
                                float(request.GET['train_2_tie_size']),
                                float(request.GET['train_2_elevation'])
                                )
        trains.append(train_2)
    if request.GET['train_3_distance'] != '':
        train_3 = train_loading(float(request.GET['train_3_distance']),
                                float(request.GET['train_3_load']),
                                float(request.GET['train_3_tie_size']),
                                float(request.GET['train_3_elevation'])
                                )
        trains.append(train_3)
    if request.GET['train_4_distance'] != '':
        train_4 = train_loading(float(request.GET['train_4_distance']),
                                float(request.GET['train_4_load']),
                                float(request.GET['train_4_tie_size']),
                                float(request.GET['train_4_elevation'])
                                )
        trains.append(train_4)

    surface_side = float(request.GET['surface_side'])

    surface_array = [(request.GET['point0x'], request.GET['point0y']),
                     (request.GET['point1x'], request.GET['point1y']),
                     (request.GET['point2x'], request.GET['point2y']),
                     (request.GET['point3x'], request.GET['point3y']),
                     (request.GET['point4x'], request.GET['point4y']),
                     (request.GET['point5x'], request.GET['point5y']),
                     (request.GET['point6x'], request.GET['point6y']),
                     (request.GET['point7x'], request.GET['point7y']),
                     (request.GET['point8x'], request.GET['point8y']),
                     (request.GET['point9x'], request.GET['point9y']),
                     (request.GET['point10x'], request.GET['point10y']),
                     (request.GET['point11x'], request.GET['point11y']),
                     (request.GET['point12x'], request.GET['point12y']),
                     (request.GET['point13x'], request.GET['point13y'])]
    new_surface_array = []  # Remove all points with no entries

    # Pare down surface array points to just the ones that were entered
    for i in range(len(surface_array)):
        if surface_array[i] != ('', ''):
            new_surface_array.append(surface_array[i])
    surface_array = []
    for i in range(len(new_surface_array)):
        surface_array.append(((float(new_surface_array[i][0])), float(new_surface_array[i][1])))

    berm_array = []
    if request.GET['berm0x'] != '':
        berm_array = [(request.GET['berm0x'], request.GET['berm0y']),
                      (request.GET['berm1x'], request.GET['berm1y']),
                      (request.GET['berm2x'], request.GET['berm2y']),
                      (request.GET['berm3x'], request.GET['berm3y']),
                      (request.GET['berm4x'], request.GET['berm4y']),
                      (request.GET['berm5x'], request.GET['berm5y']),
                      (request.GET['berm6x'], request.GET['berm6y']),
                      (request.GET['berm7x'], request.GET['berm7y']),
                      (request.GET['berm8x'], request.GET['berm8y']),
                      (request.GET['berm9x'], request.GET['berm9y']),
                      (request.GET['berm10x'], request.GET['berm10y']),
                      (request.GET['berm11x'], request.GET['berm11y']),
                      (request.GET['berm12x'], request.GET['berm12y']),
                      (request.GET['berm13x'], request.GET['berm13y'])]
        new_berm_array = []  # Remove all points with no entries

        # Pare down surface array points to just the ones that were entered
        for i in range(len(berm_array)):
            if berm_array[i] != ('', ''):
                new_berm_array.append(berm_array[i])
        berm_array = []
        for i in range(len(new_berm_array)):
            berm_array.append(((float(new_berm_array[i][0])), float(new_berm_array[i][1])))

    if request.GET['1.name'] != '':  # If layer doesn't have a name, assume it does not exist and do not input it.
        layer_1 = Layer(request.GET['1.name'], float(request.GET['1.type']), float(request.GET['1.gamma']),
                        float(request.GET['1.qu']),
                        float(request.GET['1.ka']), float(request.GET['1.kp']),
                        float(request.GET['1.phi']))
    if request.GET['2.name'] != '':
        layer_2 = Layer(request.GET['2.name'], float(request.GET['2.type']), float(request.GET['2.gamma']),
                        float(request.GET['2.qu']),
                        float(request.GET['2.ka']), float(request.GET['2.kp']),
                        float(request.GET['2.phi']))
    if request.GET['3.name'] != '':
        layer_3 = Layer(request.GET['3.name'], float(request.GET['3.type']), float(request.GET['3.gamma']),
                        float(request.GET['3.qu']),
                        float(request.GET['3.ka']), float(request.GET['3.kp']),
                        float(request.GET['3.phi']))
    if request.GET['4.name'] != '':
        layer_4 = Layer(request.GET['4.name'], float(request.GET['4.type']), float(request.GET['4.gamma']),
                        float(request.GET['4.qu']),
                        float(request.GET['4.ka']), float(request.GET['4.kp']),
                        float(request.GET['4.phi']))
    if request.GET['5.name'] != '':
        layer_5 = Layer(request.GET['5.name'], float(request.GET['5.type']), float(request.GET['5.gamma']),
                        float(request.GET['5.qu']),
                        float(request.GET['5.ka']), float(request.GET['5.kp']),
                        float(request.GET['5.phi']))
    if request.GET['6.name'] != '':
        layer_6 = Layer(request.GET['6.name'], float(request.GET['6.type']), float(request.GET['6.gamma']),
                        float(request.GET['6.qu']),
                        float(request.GET['6.ka']), float(request.GET['6.kp']),
                        float(request.GET['6.phi']))
    if request.GET['7.name'] != '':
        layer_7 = Layer(request.GET['7.name'], float(request.GET['7.type']), float(request.GET['7.gamma']),
                        float(request.GET['7.qu']),
                        float(request.GET['7.ka']), float(request.GET['7.kp']),
                        float(request.GET['7.phi']))
    if request.GET['8.name'] != '':
        layer_8 = Layer(request.GET['8.name'], float(request.GET['8.type']), float(request.GET['8.gamma']),
                        float(request.GET['8.qu']),
                        float(request.GET['8.ka']), float(request.GET['8.kp']),
                        float(request.GET['8.phi']))
    if request.GET['9.name'] != '':
        layer_9 = Layer(request.GET['9.name'], float(request.GET['9.type']), float(request.GET['9.gamma']),
                        float(request.GET['9.qu']),
                        float(request.GET['9.ka']), float(request.GET['9.kp']),
                        float(request.GET['9.phi']))
    if request.GET['10.name'] != '':
        layer_10 = Layer(request.GET['10.name'], float(request.GET['10.type']), float(request.GET['10.gamma']),
                        float(request.GET['10.qu']),
                        float(request.GET['10.ka']), float(request.GET['10.kp']),
                        float(request.GET['10.phi']))
    if request.GET['11.name'] != '':
        layer_11 = Layer(request.GET['11.name'], float(request.GET['11.type']), float(request.GET['11.gamma']),
                        float(request.GET['11.qu']),
                        float(request.GET['11.ka']), float(request.GET['11.kp']),
                        float(request.GET['11.phi']))
    if request.GET['12.name'] != '':
        layer_12 = Layer(request.GET['12.name'], float(request.GET['12.type']), float(request.GET['12.gamma']),
                        float(request.GET['12.qu']),
                        float(request.GET['12.ka']), float(request.GET['12.kp']),
                        float(request.GET['12.phi']))
    if request.GET['13.name'] != '':
        layer_13 = Layer(request.GET['13.name'], float(request.GET['13.type']), float(request.GET['13.gamma']),
                        float(request.GET['13.qu']),
                        float(request.GET['13.ka']), float(request.GET['13.kp']),
                        float(request.GET['13.phi']))
    if request.GET['14.name'] != '':
        layer_14 = Layer(request.GET['14.name'], float(request.GET['14.type']), float(request.GET['14.gamma']),
                        float(request.GET['14.qu']),
                        float(request.GET['14.ka']), float(request.GET['14.kp']),
                        float(request.GET['14.phi']))
    if request.GET['15.name'] != '':
        layer_15 = Layer(request.GET['15.name'], float(request.GET['15.type']), float(request.GET['15.gamma']),
                        float(request.GET['15.qu']),
                        float(request.GET['15.ka']), float(request.GET['15.kp']),
                        float(request.GET['15.phi']))
    if request.GET['16.name'] != '':
        layer_16 = Layer(request.GET['16.name'], float(request.GET['16.type']), float(request.GET['16.gamma']),
                        float(request.GET['16.qu']),
                        float(request.GET['16.ka']), float(request.GET['16.kp']),
                        float(request.GET['16.phi']))
    if request.GET['17.name'] != '':
        layer_17 = Layer(request.GET['17.name'], float(request.GET['17.type']), float(request.GET['17.gamma']),
                        float(request.GET['17.qu']),
                        float(request.GET['17.ka']), float(request.GET['17.kp']),
                        float(request.GET['17.phi']))
    if request.GET['18.name'] != '':
        layer_18 = Layer(request.GET['18.name'], float(request.GET['18.type']), float(request.GET['18.gamma']),
                        float(request.GET['18.qu']),
                        float(request.GET['18.ka']), float(request.GET['18.kp']),
                        float(request.GET['18.phi']))
    if request.GET['19.name'] != '':
        layer_19 = Layer(request.GET['19.name'], float(request.GET['19.type']), float(request.GET['19.gamma']),
                        float(request.GET['19.qu']),
                        float(request.GET['19.ka']), float(request.GET['19.kp']),
                        float(request.GET['19.phi']))
    if request.GET['20.name'] != '':
        layer_20 = Layer(request.GET['20.name'], float(request.GET['20.type']), float(request.GET['20.gamma']),
                         float(request.GET['20.qu']),
                         float(request.GET['20.ka']), float(request.GET['20.kp']),
                         float(request.GET['20.phi']))

    # elevation, layer, soil surcharge placeholder, footing placeholder, train placeholder, passive height placeholder
    layers = [[request.GET['wp1'], request.GET['wp1_layer'], 0, 0, 0, 10000, request.GET['wp1_layer_front']],
              [request.GET['wp2'], request.GET['wp2_layer'], 0, 0, 0, 10000, request.GET['wp2_layer_front']],
              [request.GET['wp3'], request.GET['wp3_layer'], 0, 0, 0, 10000, request.GET['wp3_layer_front']],
              [request.GET['wp4'], request.GET['wp4_layer'], 0, 0, 0, 10000, request.GET['wp4_layer_front']],
              [request.GET['wp5'], request.GET['wp5_layer'], 0, 0, 0, 10000, request.GET['wp5_layer_front']],
              [request.GET['wp6'], request.GET['wp6_layer'], 0, 0, 0, 10000, request.GET['wp6_layer_front']],
              [request.GET['wp7'], request.GET['wp7_layer'], 0, 0, 0, 10000, request.GET['wp7_layer_front']],
              [request.GET['wp8'], request.GET['wp8_layer'], 0, 0, 0, 10000, request.GET['wp8_layer_front']],
              [request.GET['wp9'], request.GET['wp9_layer'], 0, 0, 0, 10000, request.GET['wp9_layer_front']],
              [request.GET['wp10'], request.GET['wp10_layer'], 0, 0, 0, 10000, request.GET['wp10_layer_front']],
              [request.GET['wp11'], request.GET['wp11_layer'], 0, 0, 0, 10000, request.GET['wp11_layer_front']],
              [request.GET['wp12'], request.GET['wp12_layer'], 0, 0, 0, 10000, request.GET['wp12_layer_front']],
              [request.GET['wp13'], request.GET['wp13_layer'], 0, 0, 0, 10000, request.GET['wp13_layer_front']],
              [request.GET['wp14'], request.GET['wp14_layer'], 0, 0, 0, 10000, request.GET['wp14_layer_front']],
              [request.GET['wp15'], request.GET['wp15_layer'], 0, 0, 0, 10000, request.GET['wp15_layer_front']],
              [request.GET['wp16'], request.GET['wp16_layer'], 0, 0, 0, 10000, request.GET['wp16_layer_front']],
              [request.GET['wp17'], request.GET['wp17_layer'], 0, 0, 0, 10000, request.GET['wp17_layer_front']],
              [request.GET['wp18'], request.GET['wp18_layer'], 0, 0, 0, 10000, request.GET['wp18_layer_front']],
              [request.GET['wp19'], request.GET['wp19_layer'], 0, 0, 0, 10000, request.GET['wp19_layer_front']],
              [request.GET['wp20'], request.GET['wp20_layer'], 0, 0, 0, 10000, request.GET['wp20_layer_front']],
              [request.GET['wp21'], request.GET['wp21_layer'], 0, 0, 0, 10000, request.GET['wp21_layer_front']],
              [request.GET['wp22'], request.GET['wp22_layer'], 0, 0, 0, 10000, request.GET['wp22_layer_front']],
              [request.GET['wp23'], request.GET['wp23_layer'], 0, 0, 0, 10000, request.GET['wp23_layer_front']],
              [request.GET['wp24'], request.GET['wp24_layer'], 0, 0, 0, 10000, request.GET['wp24_layer_front']],
              [request.GET['wp25'], request.GET['wp25_layer'], 0, 0, 0, 10000, request.GET['wp25_layer_front']],
              [request.GET['wp26'], request.GET['wp26_layer'], 0, 0, 0, 10000, request.GET['wp26_layer_front']],
              [request.GET['wp27'], request.GET['wp27_layer'], 0, 0, 0, 10000, request.GET['wp27_layer_front']],
              [request.GET['wp28'], request.GET['wp28_layer'], 0, 0, 0, 10000, request.GET['wp28_layer_front']],
              [request.GET['wp29'], request.GET['wp29_layer'], 0, 0, 0, 10000, request.GET['wp29_layer_front']],
              [request.GET['wp30'], request.GET['wp30_layer'], 0, 0, 0, 10000, request.GET['wp30_layer_front']],
              [request.GET['wp31'], request.GET['wp31_layer'], 0, 0, 0, 10000, request.GET['wp31_layer_front']],
              [request.GET['wp32'], request.GET['wp32_layer'], 0, 0, 0, 10000, request.GET['wp32_layer_front']],
              [request.GET['wp33'], request.GET['wp33_layer'], 0, 0, 0, 10000, request.GET['wp33_layer_front']],
              [request.GET['wp34'], request.GET['wp34_layer'], 0, 0, 0, 10000, request.GET['wp34_layer_front']],
              [request.GET['wp35'], request.GET['wp35_layer'], 0, 0, 0, 10000, request.GET['wp35_layer_front']],
              [request.GET['wp36'], request.GET['wp36_layer'], 0, 0, 0, 10000, request.GET['wp36_layer_front']],
              [request.GET['wp37'], request.GET['wp37_layer'], 0, 0, 0, 10000, request.GET['wp37_layer_front']],
              [request.GET['wp38'], request.GET['wp38_layer'], 0, 0, 0, 10000, request.GET['wp38_layer_front']],
              [request.GET['wp39'], request.GET['wp39_layer'], 0, 0, 0, 10000, request.GET['wp39_layer_front']],
              [request.GET['wp40'], request.GET['wp40_layer'], 0, 0, 0, 10000, request.GET['wp40_layer_front']]]

    new_layers = []  # Remove all layers with no entries
    for i in range(len(layers)):
        if layers[i] != ['', '', 0, 0, 0, 10000, '']:
            new_layers.append(layers[i])
    layers = []
    for i in range(len(new_layers)):
        layers.append([float(new_layers[i][0]), float(new_layers[i][1]), float(new_layers[i][2]),
                       float(new_layers[i][3]), float(new_layers[i][4]), float(new_layers[i][5]),
                       float(new_layers[i][6])])

    work_points = [[0, request.GET['wp1']],
                   [0, request.GET['wp2']],
                   [0, request.GET['wp3']],
                   [0, request.GET['wp4']],
                   [0, request.GET['wp5']],
                   [0, request.GET['wp6']],
                   [0, request.GET['wp7']],
                   [0, request.GET['wp8']],
                   [0, request.GET['wp9']],
                   [0, request.GET['wp10']],
                   [0, request.GET['wp11']],
                   [0, request.GET['wp12']],
                   [0, request.GET['wp13']],
                   [0, request.GET['wp14']],
                   [0, request.GET['wp15']],
                   [0, request.GET['wp16']],
                   [0, request.GET['wp17']],
                   [0, request.GET['wp18']],
                   [0, request.GET['wp19']],
                   [0, request.GET['wp20']],
                   [0, request.GET['wp21']],
                   [0, request.GET['wp22']],
                   [0, request.GET['wp23']],
                   [0, request.GET['wp24']],
                   [0, request.GET['wp25']],
                   [0, request.GET['wp26']],
                   [0, request.GET['wp27']],
                   [0, request.GET['wp28']],
                   [0, request.GET['wp29']],
                   [0, request.GET['wp30']],
                   [0, request.GET['wp31']],
                   [0, request.GET['wp32']],
                   [0, request.GET['wp33']],
                   [0, request.GET['wp34']],
                   [0, request.GET['wp35']],
                   [0, request.GET['wp36']],
                   [0, request.GET['wp37']],
                   [0, request.GET['wp38']],
                   [0, request.GET['wp39']],
                   [0, request.GET['wp40']]
                   ]

    new_work_points = []  # Remove all points with no entries
    for i in range(len(work_points)):
        if work_points[i] != [0, '']:
            new_work_points.append(work_points[i])
    work_points = []
    for i in range(len(new_work_points)):
        work_points.append([(float(new_work_points[i][0])), float(new_work_points[i][1])])

    surcharge_unit_weight = float(request.GET['surcharge_unit_weight'])
    min_surcharge_height = request.GET['min_surcharge_height']
    if min_surcharge_height:
        min_surcharge_height = float(min_surcharge_height)
    else:
        min_surcharge_height = []
    angle = float(request.GET['angle'])

    angle_change_elev = request.GET['angle_change_elev']
    if angle_change_elev:
        angle_change_elev = float(angle_change_elev)
    else:
        angle_change_elev = []

    angle_change_type = float(request.GET['angle_change_type'])

    water_elev = request.GET['water_elev']
    if water_elev:
        water_elev = float(water_elev)
    else:
        water_elev = float(-10000)

    cut_elev = float(request.GET['cut_elev'])
    total_weights = float(request.GET['total_weights'])
    top_brace_elev = float(request.GET['top_brace_elev'])
    bot_brace_elev = float(request.GET['bot_brace_elev'])
    brace_elevations = [top_brace_elev, bot_brace_elev]
    scale_factor = float(request.GET['scale_factor'])
    sheet_type = float(request.GET['sheet_type'])
    beam_type = float(request.GET['beam_type'])
    beam_spacing = []
    diagram_type = float(request.GET['diagram_type'])

    water_cut_elev = cut_elev
    if water_elev == float(-10000):
        water_cut_elev = float(-10000)
    if request.GET['water_cut_elev'] != '':
        water_cut_elev = float(request.GET['water_cut_elev'])

    top_sheet = [layers[0][0]]
    if request.GET['top_sheet'] != '':
        top_sheet = [float(request.GET['top_sheet'])]

    for i in range(len(sheet_database)):
        if sheet_type == sheet_database[i][0]:
            sheet_type = sheet_database[i]
    for i in range(len(beam_database)):
        if beam_type == beam_database[i][0]:
            beam_type = beam_database[i]

    if request.GET['beam_spacing'] != '':
        beam_spacing = float(request.GET['beam_spacing'])
    if request.GET['beam_size_override'] != '':
        beam_type[4] = float(request.GET['beam_size_override']) / 12
    if request.GET['beam_override'] != '':
        beam_type[1] = request.GET['beam_override']
    if request.GET['beam_modulus_override'] != '':
        beam_type[2] = float(request.GET["beam_modulus_override"])
    if request.GET['beam_inertia_override'] != '':
        beam_type[3] = float(request.GET["beam_inertia_override"])

    ers_type = float(request.GET['ers_type'])
    if ers_type == 1:
        sheet_type = beam_type

    soldier_beam_method = float(request.GET['soldier_beam_method'])

    supplied_length = float(request.GET['supplied_length'])
    supplied_elev = top_sheet[0] - supplied_length

    backside_x = float(request.GET['backside_x'])
    backside_y = float(request.GET['backside_y'])

    save_calculation_name = request.GET['save_calculation_name']


    #  MANIPULATE USER DATA
    for i in range(len(layers)):  # Assign layer properties to work points
        if layers[i][1] == 1.0:
            layers[i][1] = layer_1
        if layers[i][1] == 2.0:
            layers[i][1] = layer_2
        if layers[i][1] == 3.0:
            layers[i][1] = layer_3
        if layers[i][1] == 4.0:
            layers[i][1] = layer_4
        if layers[i][1] == 5.0:
            layers[i][1] = layer_5
        if layers[i][1] == 6.0:
            layers[i][1] = layer_6
        if layers[i][1] == 7.0:
            layers[i][1] = layer_7
        if layers[i][1] == 8.0:
            layers[i][1] = layer_8
        if layers[i][1] == 9.0:
            layers[i][1] = layer_9
        if layers[i][1] == 10.0:
            layers[i][1] = layer_10
        if layers[i][1] == 11.0:
            layers[i][1] = layer_11
        if layers[i][1] == 12.0:
            layers[i][1] = layer_12
        if layers[i][1] == 13.0:
            layers[i][1] = layer_13
        if layers[i][1] == 14.0:
            layers[i][1] = layer_14
        if layers[i][1] == 15.0:
            layers[i][1] = layer_15
        if layers[i][1] == 16.0:
            layers[i][1] = layer_16
        if layers[i][1] == 17.0:
            layers[i][1] = layer_17
        if layers[i][1] == 18.0:
            layers[i][1] = layer_18
        if layers[i][1] == 19.0:
            layers[i][1] = layer_19
        if layers[i][1] == 20.0:
            layers[i][1] = layer_20

    for i in range(len(layers)):  # Assign layer properties to work points
        if layers[i][6] == 1.0:
            layers[i][6] = layer_1
        if layers[i][6] == 2.0:
            layers[i][6] = layer_2
        if layers[i][6] == 3.0:
            layers[i][6] = layer_3
        if layers[i][6] == 4.0:
            layers[i][6] = layer_4
        if layers[i][6] == 5.0:
            layers[i][6] = layer_5
        if layers[i][6] == 6.0:
            layers[i][6] = layer_6
        if layers[i][6] == 7.0:
            layers[i][6] = layer_7
        if layers[i][6] == 8.0:
            layers[i][6] = layer_8
        if layers[i][6] == 9.0:
            layers[i][6] = layer_9
        if layers[i][6] == 10.0:
            layers[i][6] = layer_10
        if layers[i][6] == 11.0:
            layers[i][6] = layer_11
        if layers[i][6] == 12.0:
            layers[i][6] = layer_12
        if layers[i][6] == 13.0:
            layers[i][6] = layer_13
        if layers[i][6] == 14.0:
            layers[i][6] = layer_14
        if layers[i][6] == 15.0:
            layers[i][6] = layer_15
        if layers[i][6] == 16.0:
            layers[i][6] = layer_16
        if layers[i][6] == 17.0:
            layers[i][6] = layer_17
        if layers[i][6] == 18.0:
            layers[i][6] = layer_18
        if layers[i][6] == 19.0:
            layers[i][6] = layer_19
        if layers[i][6] == 20.0:
            layers[i][6] = layer_20

    for i in range(len(layers)-1):
        d = layers[0][0] - cut_elev
        clay_apparent_elev = round(layers[0][0] - 0.25*d, 1)
        stiff_clay_apparent_elev = round(layers[0][0] - 0.75*d, 1)
        if diagram_type == 1 or diagram_type == 2:
            if layers[i][0] > clay_apparent_elev > layers[i+1][0]:
                layers.insert(i+1, [clay_apparent_elev, layers[i][1], 0.0, 0.0, 0.0, 10000, layers[i][6]])
                work_points.insert(i + 1, [0, clay_apparent_elev])
                break
        if diagram_type == 2:
            if layers[i][0] > stiff_clay_apparent_elev > layers[i+1][0]:
                layers.insert(i+1, [stiff_clay_apparent_elev, layers[i][1], 0.0, 0.0, 0.0, 10000, layers[i][6]])
                work_points.insert(i + 1, [0, stiff_clay_apparent_elev])
                break

    for i in range(len(layers) - 1):
        if layers[i][0] >= supplied_elev >= layers[i + 1][0]:
            layers.insert(i + 1, [round(supplied_elev, 2), layers[i][1], 0.0, 0.0, 0.0, 10000, layers[i][6]])
            work_points.insert(i + 1, [0, round(supplied_elev, 2)])
            break

    zero_length = []
    if ers_type == 1.0:
        for i in range(len(layers) - 1):
            if layers[i][0] >= cut_elev >= layers[i + 1][0]:
                if layers[i][1].type == 0:
                    layers.insert(i + 2, [round(cut_elev - beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 2, [0, round(cut_elev - beam_type[4], 2)])
                    layers.insert(i + 3, [round(cut_elev - beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 3, [0, round(cut_elev - beam_type[4], 2)])
                    zero_length = beam_type[4]
                    break
                if layers[i][1].type == 1:
                    layers.insert(i + 2, [round(cut_elev - 1.5 * beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 2, [0, round(cut_elev - 1.5 * beam_type[4], 2)])
                    layers.insert(i + 3, [round(cut_elev - 1.5 * beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 3, [0, round(cut_elev - 1.5 * beam_type[4], 2)])
                    zero_length = 1.5 * beam_type[4]
                    break

    # zero_length = []
    # if ers_type == 1.0:
    #     for i in range(len(layers) - 1):
    #         if layers[i][0] >= cut_elev >= layers[i + 1][0]:
    #             if layers[i][1].type == 0:
    #                 new_elev = round(cut_elev - beam_type[4], 2)
    #                 for j in range(len(layers) - 1):
    #                     if layers[j][0] > new_elev > layers[j + 1][0]:
    #                         layers.insert(j + 1, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j + 1, [0, new_elev])
    #                         layers.insert(j + 2, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j + 2, [0, new_elev])
    #                         zero_length = beam_type[4]
    #                         break
    #                 else:
    #                     continue  # executed if the loop ended normally (no break)
    #                 break  # executed if 'continue' was skipped (break)
    #             if layers[i][1].type == 1:
    #                 new_elev = round(cut_elev - 1.5 * beam_type[4], 2)
    #                 for j in range(len(layers) - 1):
    #                     if layers[j][0] > new_elev > layers[j + 1][0]:
    #                         layers.insert(j + 1, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j + 1, [0, new_elev])
    #                         layers.insert(j + 2, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j + 2, [0, new_elev])
    #                         zero_length = 1.5*beam_type[4]
    #                         break
    #                 else:
    #                     continue  # executed if the loop ended normally (no break)
    #                 break  # executed if 'continue' was skipped (break)

    if berm_array != []:
        layers, work_points = berm_workpoints(layers, work_points, berm_array, cut_elev)

    if request.GET['footing_1_type'] != '':
        combined_footing_load = combine_footings(footings)
        layers, work_points = incorporate_footings(footings, combined_footing_load, layers, work_points, supplied_elev)

    if berm_array != []:
        layers = passive_heights(surface_side, berm_array, layers, cut_elev)

    if request.GET['train_1_distance'] != '':
        train_surcharge = combine_trains(trains)
        for i in range(len(layers)):
            for j in range(len(train_surcharge)):
                if layers[i][0] == train_surcharge[j][0]:
                    layers[i][4] = train_surcharge[j][1]

    wat_check = float(request.GET['wat_check'])
    if wat_check == 0:
        wat_output = []
        for i in range(len(layers)):
            layers[i].append(0)
    else:
        layers, wat_output = water_around_toe(layers, water_elev, cut_elev, supplied_elev)

    layers.sort(key=lambda x: x[0], reverse=True)

    footing_output = []
    for i in range(len(footings)):
        footing_output.append(text_output(footings[i], i + 1))
    footing_output = list(itertools.chain.from_iterable(footing_output))
    total_footing_surcharge = []
    for i in range(len(layers)):
        total_footing_surcharge.append("At elevation " + str(layers[i][0]) + "', total footing surcharge = " +
                                       str(layers[i][3]) + " psf.")
    if footings == []:
        total_footing_surcharge = []
    train_output = ["All rail surcharges calculated using the Cooper E80 method."]
    for i in range(len(layers)):
        train_output.append("At elevation " + str(layers[i][0]) + "', total lateral rail surcharge = " +
                            str(layers[i][4]) + " psf.")
    if trains == []:
        train_output = []

    surcharge = surcharge_heights(surface_side, surface_array, work_points, angle, angle_change_elev, angle_change_type,
                                  min_surcharge_height)
    for i in range(len(surcharge)):
        layers[i][2] = surcharge_unit_weight * (surcharge[i][1] - layers[0][0])
    surcharge_output = []
    for i in range(len(surcharge)):
        surcharge_string = "At elevation " + str(surcharge[i][0]) + "', assume design soil height at elevation " + \
                           str(surcharge[i][1]) + "'."
        surcharge_output.append(surcharge_string)

    berm_output = []
    if berm_array != []:
        for i in range(len(layers)):
            berm_string = "At elevation " + str(layers[i][0]) + "', assume passive soil height at elevation " + \
                          str(layers[i][5]) + "'."
            berm_output.append(berm_string)
    berm_reduction_output = []

    active = active_pressures(layers, water_elev, total_weights)
    passive = passive_pressures(layers, water_cut_elev, cut_elev, total_weights)
    if berm_array != []:
        passive, berm_reduction_output = berm_reduction(layers, berm_array, cut_elev, passive, water_cut_elev,
                                                        total_weights)
    water = water_pressures(layers, water_elev, water_cut_elev, total_weights, supplied_elev)
    active_pressure = active_pressures_output(layers, water_elev, total_weights)
    passive_pressure = passive_pressures_output(layers, water_cut_elev, cut_elev, total_weights)
    water_pressure = water_pressures_output(water)
    apparent = apparent_pressures(active, passive, water, cut_elev, diagram_type, backside_x,
                       backside_y, layers, water_elev, total_weights, ers_type, beam_spacing, zero_length,
                       beam_type, soldier_beam_method)

    if top_sheet[0] != layers[0][0]:
        apparent[0].insert(0, 0)
        apparent[1].insert(0, apparent[1][0])
        apparent[0].insert(0, 0)
        apparent[1].insert(0, top_sheet[0])
        apparent[2].insert(0, 0)
        apparent[3].insert(0, apparent[3][0])
        apparent[2].insert(0, 0)
        apparent[3].insert(0, top_sheet[0])
    beam_output = []
    if ers_type == 1 and soldier_beam_method == 0:
        beam_output = [("Soldier Beam Analysis Effective Widths : " + beam_type[1] + " @ " + str(beam_spacing) +
                        "' spacing"),
                       ("From elevation " + str(apparent[1][0]) + "' to elevation " + str(cut_elev) + "': W = " +
                        str(beam_spacing) + "'"),
                       ("From elevation " + str(cut_elev) + "' to elevation " + str(round(cut_elev - zero_length, 2)) +
                        "': W = 0 (net active W =" + str(beam_type[4]) + "')"),
                       ("At elevation " + str(round(cut_elev - zero_length, 2)) + "' and below: W = 3*" +
                        str(beam_type[4]) + "' = " + str(round(3 * beam_type[4], 2)) + "'")
                       ]
    if ers_type == 1 and soldier_beam_method == 1:
        beam_output = [
            ("Soldier Beam Analysis Effective Widths : " + beam_type[1] + " @ " + str(beam_spacing) + "' spacing"),
            ("From elevation " + str(apparent[1][0]) + "' to elevation " + str(cut_elev) + "': W = " + str(
                beam_spacing) + "'"),
            ("From elevation " + str(cut_elev) + "' to elevation " + str(round(cut_elev - zero_length, 2)) +
             "': W = 0 (net active W =" + str(beam_type[4]) + "')"),
            ("At elevation " + str(round(cut_elev - zero_length, 2)) + "' and below: W = 3*" + str(beam_type[4]) +
             "' = " + str(round(3 * beam_type[4], 2)) + "' for the passive pressures, and W = " + str(beam_type[4]) +
             "' for the active pressures.  Net pressure is limited negatively (passive side) by "
             "(Pa-Pp)*beam spacing")
            ]

    data = two_layer_minimum_length(apparent, brace_elevations)
    min_length = str(round(data[0], 2)) + "'"
    min_length_elev = str(round(data[1], 2)) + "'"
    waler_load = data[2] # currently a list that contains all waler loads
    waler_load_output = data[7]
    design_text = data[3]
    min_length_pressure = data[4]
    multi = two_layer_multiplier(apparent, brace_elevations[1], data, supplied_length)
    moment = two_layer_maximum_moment(apparent, waler_load, brace_elevations)
    max_moment_elevation = round(moment[1], 2)
    moment = math.ceil(moment[0])
    deflection = two_layer_deflection_calc(apparent, brace_elevations[1], data, sheet_type)
    zero_point = data[6]
    pressure_plot = multi_layer_pressure_plot(layers, apparent, brace_elevations, min_length_pressure, data[1], data[0], deflection, scale_factor, multi[1], multi[2], multi[3], zero_point)
    active_passive_plot = ap_plot(layers, active, passive, cut_elev, 0)
    water_pressure_plot = water_plot(layers, water)
    surface = surface_plot(surface_array, work_points)
    strut_diagram = strut_pressure_plot(layers, [apparent[2], apparent[3]], brace_elevations)
    bending_stress = round(moment * 12 / 1000 / sheet_type[2], 2)
    save(pressure_plot, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/pressure_plot.html')
    save(active_passive_plot, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/active_passive_plot.html')
    save(water_pressure_plot, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/water_pressure_plot.html')
    save(surface, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/surface.html')
    save(strut_diagram, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/strut_diagram.html')

    if save_calculation_name != '':
        url_output = str(request.build_absolute_uri)
        saved_calc = SavedCalc(name=save_calculation_name, data=(request.GET['footing_1_type'],request.GET['footing_1_width'],request.GET['footing_1_distance'],request.GET['footing_1_elevation'],request.GET['footing_1_load'],request.GET['footing_1_spacing_1'],request.GET['footing_1_spacing_2'],request.GET['footing_2_type'],request.GET['footing_2_width'],request.GET['footing_2_distance'],request.GET['footing_2_elevation'],request.GET['footing_2_load'],request.GET['footing_2_spacing_1'],request.GET['footing_2_spacing_2'],request.GET['footing_3_type'],request.GET['footing_3_width'],request.GET['footing_3_distance'],request.GET['footing_3_elevation'],request.GET['footing_3_load'],request.GET['footing_3_spacing_1'],request.GET['footing_3_spacing_2'],request.GET['footing_4_type'],request.GET['footing_4_width'],request.GET['footing_4_distance'],request.GET['footing_4_elevation'],request.GET['footing_4_load'],request.GET['footing_4_spacing_1'],request.GET['footing_4_spacing_2'],request.GET['train_1_distance'],request.GET['train_1_load'],request.GET['train_1_tie_size'],request.GET['train_1_elevation'],request.GET['train_2_distance'],request.GET['train_2_load'],request.GET['train_2_tie_size'],request.GET['train_2_elevation'],request.GET['train_3_distance'],request.GET['train_3_load'],request.GET['train_3_tie_size'],request.GET['train_3_elevation'],request.GET['train_4_distance'],request.GET['train_4_load'],request.GET['train_4_tie_size'],request.GET['train_4_elevation'],request.GET['surface_side'],request.GET['point0x'],request.GET['point0y'],request.GET['point1x'],request.GET['point1y'],request.GET['point2x'],request.GET['point2y'],request.GET['point3x'],request.GET['point3y'],request.GET['point4x'],request.GET['point4y'],request.GET['point5x'],request.GET['point5y'],request.GET['point6x'],request.GET['point6y'],request.GET['point7x'],request.GET['point7y'],request.GET['point8x'],request.GET['point8y'],request.GET['point9x'],request.GET['point9y'],request.GET['point10x'],request.GET['point10y'],request.GET['point11x'],request.GET['point11y'],request.GET['point12x'],request.GET['point12y'],request.GET['point13x'],request.GET['point13y'],request.GET['berm0x'],request.GET['berm0y'],request.GET['berm1x'],request.GET['berm1y'],request.GET['berm2x'],request.GET['berm2y'],request.GET['berm3x'],request.GET['berm3y'],request.GET['berm4x'],request.GET['berm4y'],request.GET['berm5x'],request.GET['berm5y'],request.GET['berm6x'],request.GET['berm6y'],request.GET['berm7x'],request.GET['berm7y'],request.GET['berm8x'],request.GET['berm8y'],request.GET['berm9x'],request.GET['berm9y'],request.GET['berm10x'],request.GET['berm10y'],request.GET['berm11x'],request.GET['berm11y'],request.GET['berm12x'],request.GET['berm12y'],request.GET['berm13x'],request.GET['berm13y'],request.GET['1.name'],request.GET['1.type'],request.GET['1.gamma'],request.GET['1.qu'],request.GET['1.ka'],request.GET['1.kp'],request.GET['1.phi'],request.GET['2.name'],request.GET['2.type'],request.GET['2.gamma'],request.GET['2.qu'],request.GET['2.ka'],request.GET['2.kp'],request.GET['2.phi'],request.GET['3.name'],request.GET['3.type'],request.GET['3.gamma'],request.GET['3.qu'],request.GET['3.ka'],request.GET['3.kp'],request.GET['3.phi'],request.GET['4.name'],request.GET['4.type'],request.GET['4.gamma'],request.GET['4.qu'],request.GET['4.ka'],request.GET['4.kp'],request.GET['4.phi'],request.GET['5.name'],request.GET['5.type'],request.GET['5.gamma'],request.GET['5.qu'],request.GET['5.ka'],request.GET['5.kp'],request.GET['5.phi'],request.GET['6.name'],request.GET['6.type'],request.GET['6.gamma'],request.GET['6.qu'],request.GET['6.ka'],request.GET['6.kp'],request.GET['6.phi'],request.GET['7.name'],request.GET['7.type'],request.GET['7.gamma'],request.GET['7.qu'],request.GET['7.ka'],request.GET['7.kp'],request.GET['7.phi'],request.GET['8.name'],request.GET['8.type'],request.GET['8.gamma'],request.GET['8.qu'],request.GET['8.ka'],request.GET['8.kp'],request.GET['8.phi'],request.GET['9.name'],request.GET['9.type'],request.GET['9.gamma'],request.GET['9.qu'],request.GET['9.ka'],request.GET['9.kp'],request.GET['9.phi'],request.GET['10.name'],request.GET['10.type'],request.GET['10.gamma'],request.GET['10.qu'],request.GET['10.ka'],request.GET['10.kp'],request.GET['10.phi'],request.GET['11.name'],request.GET['11.type'],request.GET['11.gamma'],request.GET['11.qu'],request.GET['11.ka'],request.GET['11.kp'],request.GET['11.phi'],request.GET['12.name'],request.GET['12.type'],request.GET['12.gamma'],request.GET['12.qu'],request.GET['12.ka'],request.GET['12.kp'],request.GET['12.phi'],request.GET['13.name'],request.GET['13.type'],request.GET['13.gamma'],request.GET['13.qu'],request.GET['13.ka'],request.GET['13.kp'],request.GET['14.phi'],request.GET['14.name'],request.GET['14.type'],request.GET['14.gamma'],request.GET['14.qu'],request.GET['14.ka'],request.GET['14.kp'],request.GET['15.phi'],request.GET['15.name'],request.GET['15.type'],request.GET['15.gamma'],request.GET['15.qu'],request.GET['15.ka'],request.GET['15.kp'],request.GET['16.phi'],request.GET['16.name'],request.GET['16.type'],request.GET['16.gamma'],request.GET['16.qu'],request.GET['16.ka'],request.GET['16.kp'],request.GET['17.phi'],request.GET['17.name'],request.GET['17.type'],request.GET['17.gamma'],request.GET['17.qu'],request.GET['17.ka'],request.GET['17.kp'],request.GET['18.phi'],request.GET['18.name'],request.GET['18.type'],request.GET['18.gamma'],request.GET['18.qu'],request.GET['18.ka'],request.GET['18.kp'],request.GET['19.phi'],request.GET['19.name'],request.GET['19.type'],request.GET['19.gamma'],request.GET['19.qu'],request.GET['19.ka'],request.GET['19.kp'],request.GET['20.phi'],request.GET['20.name'],request.GET['20.type'],request.GET['20.gamma'],request.GET['20.qu'],request.GET['20.ka'],request.GET['20.kp'],request.GET['wp1'],request.GET['wp1_layer'],request.GET['wp1_layer_front'],request.GET['wp2'],request.GET['wp2_layer'],request.GET['wp2_layer_front'],request.GET['wp3'],request.GET['wp3_layer'],request.GET['wp3_layer_front'],request.GET['wp4'],request.GET['wp4_layer'],request.GET['wp4_layer_front'],request.GET['wp5'],request.GET['wp5_layer'],request.GET['wp5_layer_front'],request.GET['wp6'],request.GET['wp6_layer'],request.GET['wp6_layer_front'],request.GET['wp7'],request.GET['wp7_layer'],request.GET['wp7_layer_front'],request.GET['wp8'],request.GET['wp8_layer'],request.GET['wp8_layer_front'],request.GET['wp9'],request.GET['wp9_layer'],request.GET['wp9_layer_front'],request.GET['wp10'],request.GET['wp10_layer'],request.GET['wp10_layer_front'],request.GET['wp11'],request.GET['wp11_layer'],request.GET['wp11_layer_front'],request.GET['wp12'],request.GET['wp12_layer'],request.GET['wp12_layer_front'],request.GET['wp13'],request.GET['wp13_layer'],request.GET['wp13_layer_front'],request.GET['wp14'],request.GET['wp14_layer'],request.GET['wp14_layer_front'],request.GET['wp15'],request.GET['wp15_layer'],request.GET['wp15_layer_front'],request.GET['wp16'],request.GET['wp16_layer'],request.GET['wp16_layer_front'],request.GET['wp17'],request.GET['wp17_layer'],request.GET['wp17_layer_front'],request.GET['wp18'],request.GET['wp18_layer'],request.GET['wp18_layer_front'],request.GET['wp19'],request.GET['wp19_layer'],request.GET['wp19_layer_front'],request.GET['wp20'],request.GET['wp20_layer'],request.GET['wp20_layer_front'],request.GET['wp21'],request.GET['wp21_layer'],request.GET['wp21_layer_front'],request.GET['wp22'],request.GET['wp22_layer'],request.GET['wp22_layer_front'],request.GET['wp23'],request.GET['wp23_layer'],request.GET['wp23_layer_front'],request.GET['wp24'],request.GET['wp24_layer'],request.GET['wp24_layer_front'],request.GET['wp25'],request.GET['wp25_layer'],request.GET['wp25_layer_front'],request.GET['wp26'],request.GET['wp26_layer'],request.GET['wp26_layer_front'],request.GET['wp27'],request.GET['wp27_layer'],request.GET['wp27_layer_front'],request.GET['wp28'],request.GET['wp28_layer'],request.GET['wp28_layer_front'],request.GET['wp29'],request.GET['wp29_layer'],request.GET['wp29_layer_front'],request.GET['wp30'],request.GET['wp30_layer'],request.GET['wp30_layer_front'],request.GET['wp31'],request.GET['wp31_layer'],request.GET['wp31_layer_front'],request.GET['wp32'],request.GET['wp32_layer'],request.GET['wp32_layer_front'],request.GET['wp33'],request.GET['wp33_layer'],request.GET['wp33_layer_front'],request.GET['wp34'],request.GET['wp34_layer'],request.GET['wp34_layer_front'],request.GET['wp35'],request.GET['wp35_layer'],request.GET['wp35_layer_front'],request.GET['wp36'],request.GET['wp36_layer'],request.GET['wp36_layer_front'],request.GET['wp37'],request.GET['wp37_layer'],request.GET['wp37_layer_front'],request.GET['wp38'],request.GET['wp38_layer'],request.GET['wp38_layer_front'],request.GET['wp39'],request.GET['wp39_layer'],request.GET['wp39_layer_front'],request.GET['wp40'],request.GET['wp40_layer'],request.GET['wp40_layer_front'],request.GET['surcharge_unit_weight'],request.GET['min_surcharge_height'],request.GET['angle'],request.GET['angle_change_elev'],request.GET['water_elev'],request.GET['cut_elev'],request.GET['total_weights'],request.GET['top_brace_elev'],request.GET['bot_brace_elev'],request.GET['diagram_type'],request.GET['backside_x'],request.GET['backside_y'],request.GET['scale_factor'],request.GET['sheet_type'],request.GET['beam_type'],request.GET['water_cut_elev'],request.GET['top_sheet'],request.GET['beam_spacing'],request.GET['beam_size_override'],request.GET['beam_override'],request.GET['beam_modulus_override'],request.GET['beam_inertia_override'],request.GET['ers_type'],request.GET['soldier_beam_method'],request.GET['supplied_length'],request.GET['wat_check'],request.GET['angle_change_type'],request.GET['13.phi']),
        type="Two Layer Braced")
        saved_calc.save()

    return render(request, "multi_output.html", {"surcharge": surcharge_output,
                                           "layers": layers,
                                           "active_pressures": active_pressure,
                                           "passive_pressures": passive_pressure,
                                           "water_pressures": water_pressure,
                                           "min_length": min_length,
                                           "min_length_elev": min_length_elev,
                                           "waler_load": waler_load_output,
                                           "design_text": design_text,
                                           "multiplier": multi[0],
                                           "moment": moment,
                                           "deflection": deflection[1],
                                           "deflection_elev": deflection[2],
                                           "footing_output": footing_output,
                                           "total_footing_surcharge": total_footing_surcharge,
                                           "sheet_type": sheet_type[1],
                                           "bending_stress": bending_stress,
                                           "train_output": train_output,
                                           "beam_output": beam_output,
                                           "wat_output": wat_output,
                                           "berm_output": berm_output,
                                           "berm_reduction_output": berm_reduction_output,
                                           "soldier_beam_method": soldier_beam_method,
                                           "net_output": apparent[4],
                                           "max_moment_elevation": max_moment_elevation,
                                           "min_length_work_moments": data[5],
                                           "multiplier_supplied_length": multi[4],
                                           "multiplier_value": round(multi[3], 2),
                                           "I": sheet_type[3],
                                           "Sx": sheet_type[2]
                                           })


def three_output(request):
    # TAKE INPUT DATA FROM USER
    footings = []
    trains = []
    # footing_surcharge(type, width, distance, elevation, load, spacing_1, spacing_2)
    if request.GET['footing_1_type'] != '':
        footing_1 = footing_surcharge(float(request.GET['footing_1_type']),
                                      float(request.GET['footing_1_width']),
                                      float(request.GET['footing_1_distance']),
                                      float(request.GET['footing_1_elevation']),
                                      float(request.GET['footing_1_load']),
                                      float(request.GET['footing_1_spacing_1']),
                                      float(request.GET['footing_1_spacing_2']))
        footings.append(footing_1)
    if request.GET['footing_2_type'] != '':
        footing_2 = footing_surcharge(float(request.GET['footing_2_type']),
                                      float(request.GET['footing_2_width']),
                                      float(request.GET['footing_2_distance']),
                                      float(request.GET['footing_2_elevation']),
                                      float(request.GET['footing_2_load']),
                                      float(request.GET['footing_2_spacing_1']),
                                      float(request.GET['footing_2_spacing_2']))
        footings.append(footing_2)
    if request.GET['footing_3_type'] != '':
        footing_3 = footing_surcharge(float(request.GET['footing_3_type']),
                                      float(request.GET['footing_3_width']),
                                      float(request.GET['footing_3_distance']),
                                      float(request.GET['footing_3_elevation']),
                                      float(request.GET['footing_3_load']),
                                      float(request.GET['footing_3_spacing_1']),
                                      float(request.GET['footing_3_spacing_2']))
        footings.append(footing_3)
    if request.GET['footing_4_type'] != '':
        footing_4 = footing_surcharge(float(request.GET['footing_4_type']),
                                      float(request.GET['footing_4_width']),
                                      float(request.GET['footing_4_distance']),
                                      float(request.GET['footing_4_elevation']),
                                      float(request.GET['footing_4_load']),
                                      float(request.GET['footing_4_spacing_1']),
                                      float(request.GET['footing_4_spacing_2']))
        footings.append(footing_4)

    if request.GET['train_1_distance'] != '':
        train_1 = train_loading(float(request.GET['train_1_distance']),
                                float(request.GET['train_1_load']),
                                float(request.GET['train_1_tie_size']),
                                float(request.GET['train_1_elevation'])
                                )
        trains.append(train_1)
    if request.GET['train_2_distance'] != '':
        train_2 = train_loading(float(request.GET['train_2_distance']),
                                float(request.GET['train_2_load']),
                                float(request.GET['train_2_tie_size']),
                                float(request.GET['train_2_elevation'])
                                )
        trains.append(train_2)
    if request.GET['train_3_distance'] != '':
        train_3 = train_loading(float(request.GET['train_3_distance']),
                                float(request.GET['train_3_load']),
                                float(request.GET['train_3_tie_size']),
                                float(request.GET['train_3_elevation'])
                                )
        trains.append(train_3)
    if request.GET['train_4_distance'] != '':
        train_4 = train_loading(float(request.GET['train_4_distance']),
                                float(request.GET['train_4_load']),
                                float(request.GET['train_4_tie_size']),
                                float(request.GET['train_4_elevation'])
                                )
        trains.append(train_4)

    surface_side = float(request.GET['surface_side'])

    surface_array = [(request.GET['point0x'], request.GET['point0y']),
                     (request.GET['point1x'], request.GET['point1y']),
                     (request.GET['point2x'], request.GET['point2y']),
                     (request.GET['point3x'], request.GET['point3y']),
                     (request.GET['point4x'], request.GET['point4y']),
                     (request.GET['point5x'], request.GET['point5y']),
                     (request.GET['point6x'], request.GET['point6y']),
                     (request.GET['point7x'], request.GET['point7y']),
                     (request.GET['point8x'], request.GET['point8y']),
                     (request.GET['point9x'], request.GET['point9y']),
                     (request.GET['point10x'], request.GET['point10y']),
                     (request.GET['point11x'], request.GET['point11y']),
                     (request.GET['point12x'], request.GET['point12y']),
                     (request.GET['point13x'], request.GET['point13y'])]
    new_surface_array = []  # Remove all points with no entries

    # Pare down surface array points to just the ones that were entered
    for i in range(len(surface_array)):
        if surface_array[i] != ('', ''):
            new_surface_array.append(surface_array[i])
    surface_array = []
    for i in range(len(new_surface_array)):
        surface_array.append(((float(new_surface_array[i][0])), float(new_surface_array[i][1])))

    berm_array = []
    if request.GET['berm0x'] != '':
        berm_array = [(request.GET['berm0x'], request.GET['berm0y']),
                      (request.GET['berm1x'], request.GET['berm1y']),
                      (request.GET['berm2x'], request.GET['berm2y']),
                      (request.GET['berm3x'], request.GET['berm3y']),
                      (request.GET['berm4x'], request.GET['berm4y']),
                      (request.GET['berm5x'], request.GET['berm5y']),
                      (request.GET['berm6x'], request.GET['berm6y']),
                      (request.GET['berm7x'], request.GET['berm7y']),
                      (request.GET['berm8x'], request.GET['berm8y']),
                      (request.GET['berm9x'], request.GET['berm9y']),
                      (request.GET['berm10x'], request.GET['berm10y']),
                      (request.GET['berm11x'], request.GET['berm11y']),
                      (request.GET['berm12x'], request.GET['berm12y']),
                      (request.GET['berm13x'], request.GET['berm13y'])]
        new_berm_array = []  # Remove all points with no entries

        # Pare down surface array points to just the ones that were entered
        for i in range(len(berm_array)):
            if berm_array[i] != ('', ''):
                new_berm_array.append(berm_array[i])
        berm_array = []
        for i in range(len(new_berm_array)):
            berm_array.append(((float(new_berm_array[i][0])), float(new_berm_array[i][1])))

    if request.GET['1.name'] != '':  # If layer doesn't have a name, assume it does not exist and do not input it.
        layer_1 = Layer(request.GET['1.name'], float(request.GET['1.type']), float(request.GET['1.gamma']),
                        float(request.GET['1.qu']),
                        float(request.GET['1.ka']), float(request.GET['1.kp']),
                        float(request.GET['1.phi']))
    if request.GET['2.name'] != '':
        layer_2 = Layer(request.GET['2.name'], float(request.GET['2.type']), float(request.GET['2.gamma']),
                        float(request.GET['2.qu']),
                        float(request.GET['2.ka']), float(request.GET['2.kp']),
                        float(request.GET['2.phi']))
    if request.GET['3.name'] != '':
        layer_3 = Layer(request.GET['3.name'], float(request.GET['3.type']), float(request.GET['3.gamma']),
                        float(request.GET['3.qu']),
                        float(request.GET['3.ka']), float(request.GET['3.kp']),
                        float(request.GET['3.phi']))
    if request.GET['4.name'] != '':
        layer_4 = Layer(request.GET['4.name'], float(request.GET['4.type']), float(request.GET['4.gamma']),
                        float(request.GET['4.qu']),
                        float(request.GET['4.ka']), float(request.GET['4.kp']),
                        float(request.GET['4.phi']))
    if request.GET['5.name'] != '':
        layer_5 = Layer(request.GET['5.name'], float(request.GET['5.type']), float(request.GET['5.gamma']),
                        float(request.GET['5.qu']),
                        float(request.GET['5.ka']), float(request.GET['5.kp']),
                        float(request.GET['5.phi']))
    if request.GET['6.name'] != '':
        layer_6 = Layer(request.GET['6.name'], float(request.GET['6.type']), float(request.GET['6.gamma']),
                        float(request.GET['6.qu']),
                        float(request.GET['6.ka']), float(request.GET['6.kp']),
                        float(request.GET['6.phi']))
    if request.GET['7.name'] != '':
        layer_7 = Layer(request.GET['7.name'], float(request.GET['7.type']), float(request.GET['7.gamma']),
                        float(request.GET['7.qu']),
                        float(request.GET['7.ka']), float(request.GET['7.kp']),
                        float(request.GET['7.phi']))
    if request.GET['8.name'] != '':
        layer_8 = Layer(request.GET['8.name'], float(request.GET['8.type']), float(request.GET['8.gamma']),
                        float(request.GET['8.qu']),
                        float(request.GET['8.ka']), float(request.GET['8.kp']),
                        float(request.GET['8.phi']))
    if request.GET['9.name'] != '':
        layer_9 = Layer(request.GET['9.name'], float(request.GET['9.type']), float(request.GET['9.gamma']),
                        float(request.GET['9.qu']),
                        float(request.GET['9.ka']), float(request.GET['9.kp']),
                        float(request.GET['9.phi']))
    if request.GET['10.name'] != '':
        layer_10 = Layer(request.GET['10.name'], float(request.GET['10.type']), float(request.GET['10.gamma']),
                         float(request.GET['10.qu']),
                         float(request.GET['10.ka']), float(request.GET['10.kp']),
                         float(request.GET['10.phi']))
    if request.GET['11.name'] != '':
        layer_11 = Layer(request.GET['11.name'], float(request.GET['11.type']), float(request.GET['11.gamma']),
                         float(request.GET['11.qu']),
                         float(request.GET['11.ka']), float(request.GET['11.kp']),
                         float(request.GET['11.phi']))
    if request.GET['12.name'] != '':
        layer_12 = Layer(request.GET['12.name'], float(request.GET['12.type']), float(request.GET['12.gamma']),
                         float(request.GET['12.qu']),
                         float(request.GET['12.ka']), float(request.GET['12.kp']),
                         float(request.GET['12.phi']))
    if request.GET['13.name'] != '':
        layer_13 = Layer(request.GET['13.name'], float(request.GET['13.type']), float(request.GET['13.gamma']),
                         float(request.GET['13.qu']),
                         float(request.GET['13.ka']), float(request.GET['13.kp']),
                         float(request.GET['13.phi']))
    if request.GET['14.name'] != '':
        layer_14 = Layer(request.GET['14.name'], float(request.GET['14.type']), float(request.GET['14.gamma']),
                         float(request.GET['14.qu']),
                         float(request.GET['14.ka']), float(request.GET['14.kp']),
                         float(request.GET['14.phi']))
    if request.GET['15.name'] != '':
        layer_15 = Layer(request.GET['15.name'], float(request.GET['15.type']), float(request.GET['15.gamma']),
                         float(request.GET['15.qu']),
                         float(request.GET['15.ka']), float(request.GET['15.kp']),
                         float(request.GET['15.phi']))
    if request.GET['16.name'] != '':
        layer_16 = Layer(request.GET['16.name'], float(request.GET['16.type']), float(request.GET['16.gamma']),
                         float(request.GET['16.qu']),
                         float(request.GET['16.ka']), float(request.GET['16.kp']),
                         float(request.GET['16.phi']))
    if request.GET['17.name'] != '':
        layer_17 = Layer(request.GET['17.name'], float(request.GET['17.type']), float(request.GET['17.gamma']),
                         float(request.GET['17.qu']),
                         float(request.GET['17.ka']), float(request.GET['17.kp']),
                         float(request.GET['17.phi']))
    if request.GET['18.name'] != '':
        layer_18 = Layer(request.GET['18.name'], float(request.GET['18.type']), float(request.GET['18.gamma']),
                         float(request.GET['18.qu']),
                         float(request.GET['18.ka']), float(request.GET['18.kp']),
                         float(request.GET['18.phi']))
    if request.GET['19.name'] != '':
        layer_19 = Layer(request.GET['19.name'], float(request.GET['19.type']), float(request.GET['19.gamma']),
                         float(request.GET['19.qu']),
                         float(request.GET['19.ka']), float(request.GET['19.kp']),
                         float(request.GET['19.phi']))
    if request.GET['20.name'] != '':
        layer_20 = Layer(request.GET['20.name'], float(request.GET['20.type']), float(request.GET['20.gamma']),
                         float(request.GET['20.qu']),
                         float(request.GET['20.ka']), float(request.GET['20.kp']),
                         float(request.GET['20.phi']))

    # elevation, layer, soil surcharge placeholder, footing placeholder, train placeholder, passive height placeholder
    layers = [[request.GET['wp1'], request.GET['wp1_layer'], 0, 0, 0, 10000, request.GET['wp1_layer_front']],
              [request.GET['wp2'], request.GET['wp2_layer'], 0, 0, 0, 10000, request.GET['wp2_layer_front']],
              [request.GET['wp3'], request.GET['wp3_layer'], 0, 0, 0, 10000, request.GET['wp3_layer_front']],
              [request.GET['wp4'], request.GET['wp4_layer'], 0, 0, 0, 10000, request.GET['wp4_layer_front']],
              [request.GET['wp5'], request.GET['wp5_layer'], 0, 0, 0, 10000, request.GET['wp5_layer_front']],
              [request.GET['wp6'], request.GET['wp6_layer'], 0, 0, 0, 10000, request.GET['wp6_layer_front']],
              [request.GET['wp7'], request.GET['wp7_layer'], 0, 0, 0, 10000, request.GET['wp7_layer_front']],
              [request.GET['wp8'], request.GET['wp8_layer'], 0, 0, 0, 10000, request.GET['wp8_layer_front']],
              [request.GET['wp9'], request.GET['wp9_layer'], 0, 0, 0, 10000, request.GET['wp9_layer_front']],
              [request.GET['wp10'], request.GET['wp10_layer'], 0, 0, 0, 10000, request.GET['wp10_layer_front']],
              [request.GET['wp11'], request.GET['wp11_layer'], 0, 0, 0, 10000, request.GET['wp11_layer_front']],
              [request.GET['wp12'], request.GET['wp12_layer'], 0, 0, 0, 10000, request.GET['wp12_layer_front']],
              [request.GET['wp13'], request.GET['wp13_layer'], 0, 0, 0, 10000, request.GET['wp13_layer_front']],
              [request.GET['wp14'], request.GET['wp14_layer'], 0, 0, 0, 10000, request.GET['wp14_layer_front']],
              [request.GET['wp15'], request.GET['wp15_layer'], 0, 0, 0, 10000, request.GET['wp15_layer_front']],
              [request.GET['wp16'], request.GET['wp16_layer'], 0, 0, 0, 10000, request.GET['wp16_layer_front']],
              [request.GET['wp17'], request.GET['wp17_layer'], 0, 0, 0, 10000, request.GET['wp17_layer_front']],
              [request.GET['wp18'], request.GET['wp18_layer'], 0, 0, 0, 10000, request.GET['wp18_layer_front']],
              [request.GET['wp19'], request.GET['wp19_layer'], 0, 0, 0, 10000, request.GET['wp19_layer_front']],
              [request.GET['wp20'], request.GET['wp20_layer'], 0, 0, 0, 10000, request.GET['wp20_layer_front']],
              [request.GET['wp21'], request.GET['wp21_layer'], 0, 0, 0, 10000, request.GET['wp21_layer_front']],
              [request.GET['wp22'], request.GET['wp22_layer'], 0, 0, 0, 10000, request.GET['wp22_layer_front']],
              [request.GET['wp23'], request.GET['wp23_layer'], 0, 0, 0, 10000, request.GET['wp23_layer_front']],
              [request.GET['wp24'], request.GET['wp24_layer'], 0, 0, 0, 10000, request.GET['wp24_layer_front']],
              [request.GET['wp25'], request.GET['wp25_layer'], 0, 0, 0, 10000, request.GET['wp25_layer_front']],
              [request.GET['wp26'], request.GET['wp26_layer'], 0, 0, 0, 10000, request.GET['wp26_layer_front']],
              [request.GET['wp27'], request.GET['wp27_layer'], 0, 0, 0, 10000, request.GET['wp27_layer_front']],
              [request.GET['wp28'], request.GET['wp28_layer'], 0, 0, 0, 10000, request.GET['wp28_layer_front']],
              [request.GET['wp29'], request.GET['wp29_layer'], 0, 0, 0, 10000, request.GET['wp29_layer_front']],
              [request.GET['wp30'], request.GET['wp30_layer'], 0, 0, 0, 10000, request.GET['wp30_layer_front']],
              [request.GET['wp31'], request.GET['wp31_layer'], 0, 0, 0, 10000, request.GET['wp31_layer_front']],
              [request.GET['wp32'], request.GET['wp32_layer'], 0, 0, 0, 10000, request.GET['wp32_layer_front']],
              [request.GET['wp33'], request.GET['wp33_layer'], 0, 0, 0, 10000, request.GET['wp33_layer_front']],
              [request.GET['wp34'], request.GET['wp34_layer'], 0, 0, 0, 10000, request.GET['wp34_layer_front']],
              [request.GET['wp35'], request.GET['wp35_layer'], 0, 0, 0, 10000, request.GET['wp35_layer_front']],
              [request.GET['wp36'], request.GET['wp36_layer'], 0, 0, 0, 10000, request.GET['wp36_layer_front']],
              [request.GET['wp37'], request.GET['wp37_layer'], 0, 0, 0, 10000, request.GET['wp37_layer_front']],
              [request.GET['wp38'], request.GET['wp38_layer'], 0, 0, 0, 10000, request.GET['wp38_layer_front']],
              [request.GET['wp39'], request.GET['wp39_layer'], 0, 0, 0, 10000, request.GET['wp39_layer_front']],
              [request.GET['wp40'], request.GET['wp40_layer'], 0, 0, 0, 10000, request.GET['wp40_layer_front']]]

    new_layers = []  # Remove all layers with no entries
    for i in range(len(layers)):
        if layers[i] != ['', '', 0, 0, 0, 10000,'']:
            new_layers.append(layers[i])
    layers = []
    for i in range(len(new_layers)):
        layers.append([float(new_layers[i][0]), float(new_layers[i][1]), float(new_layers[i][2]),
                       float(new_layers[i][3]), float(new_layers[i][4]), float(new_layers[i][5]),
                       float(new_layers[i][6])])

    work_points = [[0, request.GET['wp1']],
                   [0, request.GET['wp2']],
                   [0, request.GET['wp3']],
                   [0, request.GET['wp4']],
                   [0, request.GET['wp5']],
                   [0, request.GET['wp6']],
                   [0, request.GET['wp7']],
                   [0, request.GET['wp8']],
                   [0, request.GET['wp9']],
                   [0, request.GET['wp10']],
                   [0, request.GET['wp11']],
                   [0, request.GET['wp12']],
                   [0, request.GET['wp13']],
                   [0, request.GET['wp14']],
                   [0, request.GET['wp15']],
                   [0, request.GET['wp16']],
                   [0, request.GET['wp17']],
                   [0, request.GET['wp18']],
                   [0, request.GET['wp19']],
                   [0, request.GET['wp20']],
                   [0, request.GET['wp21']],
                   [0, request.GET['wp22']],
                   [0, request.GET['wp23']],
                   [0, request.GET['wp24']],
                   [0, request.GET['wp25']],
                   [0, request.GET['wp26']],
                   [0, request.GET['wp27']],
                   [0, request.GET['wp28']],
                   [0, request.GET['wp29']],
                   [0, request.GET['wp30']],
                   [0, request.GET['wp31']],
                   [0, request.GET['wp32']],
                   [0, request.GET['wp33']],
                   [0, request.GET['wp34']],
                   [0, request.GET['wp35']],
                   [0, request.GET['wp36']],
                   [0, request.GET['wp37']],
                   [0, request.GET['wp38']],
                   [0, request.GET['wp39']],
                   [0, request.GET['wp40']]
                   ]

    new_work_points = []  # Remove all points with no entries
    for i in range(len(work_points)):
        if work_points[i] != [0, '']:
            new_work_points.append(work_points[i])
    work_points = []
    for i in range(len(new_work_points)):
        work_points.append([(float(new_work_points[i][0])), float(new_work_points[i][1])])

    surcharge_unit_weight = float(request.GET['surcharge_unit_weight'])
    min_surcharge_height = request.GET['min_surcharge_height']
    if min_surcharge_height:
        min_surcharge_height = float(min_surcharge_height)
    else:
        min_surcharge_height = []
    angle = float(request.GET['angle'])

    angle_change_elev = request.GET['angle_change_elev']
    if angle_change_elev:
        angle_change_elev = float(angle_change_elev)
    else:
        angle_change_elev = []

    angle_change_type = float(request.GET['angle_change_type'])

    water_elev = request.GET['water_elev']
    if water_elev:
        water_elev = float(water_elev)
    else:
        water_elev = float(-10000)

    cut_elev = float(request.GET['cut_elev'])
    total_weights = float(request.GET['total_weights'])
    top_brace_elev = float(request.GET['top_brace_elev'])
    mid_brace_elev = float(request.GET['mid_brace_elev'])
    bot_brace_elev = float(request.GET['bot_brace_elev'])
    brace_elevations = [top_brace_elev, mid_brace_elev, bot_brace_elev]
    scale_factor = float(request.GET['scale_factor'])
    sheet_type = float(request.GET['sheet_type'])
    beam_type = float(request.GET['beam_type'])
    beam_spacing = []
    diagram_type = float(request.GET['diagram_type'])

    water_cut_elev = cut_elev
    if water_elev == float(-10000):
        water_cut_elev = float(-10000)
    if request.GET['water_cut_elev'] != '':
        water_cut_elev = float(request.GET['water_cut_elev'])

    top_sheet = [layers[0][0]]
    if request.GET['top_sheet'] != '':
        top_sheet = [float(request.GET['top_sheet'])]

    for i in range(len(sheet_database)):
        if sheet_type == sheet_database[i][0]:
            sheet_type = sheet_database[i]
    for i in range(len(beam_database)):
        if beam_type == beam_database[i][0]:
            beam_type = beam_database[i]

    if request.GET['beam_spacing'] != '':
        beam_spacing = float(request.GET['beam_spacing'])
    if request.GET['beam_size_override'] != '':
        beam_type[4] = float(request.GET['beam_size_override']) / 12
    if request.GET['beam_override'] != '':
        beam_type[1] = request.GET['beam_override']
    if request.GET['beam_modulus_override'] != '':
        beam_type[2] = float(request.GET["beam_modulus_override"])
    if request.GET['beam_inertia_override'] != '':
        beam_type[3] = float(request.GET["beam_inertia_override"])

    ers_type = float(request.GET['ers_type'])
    if ers_type == 1:
        sheet_type = beam_type

    soldier_beam_method = float(request.GET['soldier_beam_method'])

    supplied_length = float(request.GET['supplied_length'])
    supplied_elev = top_sheet[0] - supplied_length

    backside_x = float(request.GET['backside_x'])
    backside_y = float(request.GET['backside_y'])

    save_calculation_name = request.GET['save_calculation_name']

    #  MANIPULATE USER DATA
    for i in range(len(layers)):  # Assign layer properties to work points
        if layers[i][1] == 1.0:
            layers[i][1] = layer_1
        if layers[i][1] == 2.0:
            layers[i][1] = layer_2
        if layers[i][1] == 3.0:
            layers[i][1] = layer_3
        if layers[i][1] == 4.0:
            layers[i][1] = layer_4
        if layers[i][1] == 5.0:
            layers[i][1] = layer_5
        if layers[i][1] == 6.0:
            layers[i][1] = layer_6
        if layers[i][1] == 7.0:
            layers[i][1] = layer_7
        if layers[i][1] == 8.0:
            layers[i][1] = layer_8
        if layers[i][1] == 9.0:
            layers[i][1] = layer_9
        if layers[i][1] == 10.0:
            layers[i][1] = layer_10
        if layers[i][1] == 11.0:
            layers[i][1] = layer_11
        if layers[i][1] == 12.0:
            layers[i][1] = layer_12
        if layers[i][1] == 13.0:
            layers[i][1] = layer_13
        if layers[i][1] == 14.0:
            layers[i][1] = layer_14
        if layers[i][1] == 15.0:
            layers[i][1] = layer_15
        if layers[i][1] == 16.0:
            layers[i][1] = layer_16
        if layers[i][1] == 17.0:
            layers[i][1] = layer_17
        if layers[i][1] == 18.0:
            layers[i][1] = layer_18
        if layers[i][1] == 19.0:
            layers[i][1] = layer_19
        if layers[i][1] == 20.0:
            layers[i][1] = layer_20
    for i in range(len(layers)):  # Assign layer properties to work points
        if layers[i][6] == 1.0:
            layers[i][6] = layer_1
        if layers[i][6] == 2.0:
            layers[i][6] = layer_2
        if layers[i][6] == 3.0:
            layers[i][6] = layer_3
        if layers[i][6] == 4.0:
            layers[i][6] = layer_4
        if layers[i][6] == 5.0:
            layers[i][6] = layer_5
        if layers[i][6] == 6.0:
            layers[i][6] = layer_6
        if layers[i][6] == 7.0:
            layers[i][6] = layer_7
        if layers[i][6] == 8.0:
            layers[i][6] = layer_8
        if layers[i][6] == 9.0:
            layers[i][6] = layer_9
        if layers[i][6] == 10.0:
            layers[i][6] = layer_10
        if layers[i][6] == 11.0:
            layers[i][6] = layer_11
        if layers[i][6] == 12.0:
            layers[i][6] = layer_12
        if layers[i][6] == 13.0:
            layers[i][6] = layer_13
        if layers[i][6] == 14.0:
            layers[i][6] = layer_14
        if layers[i][6] == 15.0:
            layers[i][6] = layer_15
        if layers[i][6] == 16.0:
            layers[i][6] = layer_16
        if layers[i][6] == 17.0:
            layers[i][6] = layer_17
        if layers[i][6] == 18.0:
            layers[i][6] = layer_18
        if layers[i][6] == 19.0:
            layers[i][6] = layer_19
        if layers[i][6] == 20.0:
            layers[i][6] = layer_20

    for i in range(len(layers) - 1):
        d = layers[0][0] - cut_elev
        clay_apparent_elev = round(layers[0][0] - 0.25 * d, 1)
        stiff_clay_apparent_elev = round(layers[0][0] - 0.75 * d, 1)
        if diagram_type == 1 or diagram_type == 2:
            if layers[i][0] > clay_apparent_elev > layers[i + 1][0]:
                layers.insert(i + 1, [clay_apparent_elev, layers[i][1], 0.0, 0.0, 0.0, 10000, layers[i][6]])
                work_points.insert(i + 1, [0, clay_apparent_elev])
                break
        if diagram_type == 2:
            if layers[i][0] > stiff_clay_apparent_elev > layers[i + 1][0]:
                layers.insert(i + 1, [stiff_clay_apparent_elev, layers[i][1], 0.0, 0.0, 0.0, 10000, layers[i][6]])
                work_points.insert(i + 1, [0, stiff_clay_apparent_elev])
                break

    for i in range(len(layers) - 1):
        if layers[i][0] >= supplied_elev >= layers[i + 1][0]:
            layers.insert(i + 1, [round(supplied_elev, 2), layers[i][1], 0.0, 0.0, 0.0, 10000, layers[i][6]])
            work_points.insert(i + 1, [0, round(supplied_elev, 2)])
            break

    zero_length = []
    if ers_type == 1.0:
        for i in range(len(layers) - 1):
            if layers[i][0] >= cut_elev >= layers[i + 1][0]:
                if layers[i][1].type == 0:
                    layers.insert(i + 2, [round(cut_elev - beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 2, [0, round(cut_elev - beam_type[4], 2)])
                    layers.insert(i + 3, [round(cut_elev - beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 3, [0, round(cut_elev - beam_type[4], 2)])
                    zero_length = beam_type[4]
                    break
                if layers[i][1].type == 1:
                    layers.insert(i + 2, [round(cut_elev - 1.5 * beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 2, [0, round(cut_elev - 1.5 * beam_type[4], 2)])
                    layers.insert(i + 3, [round(cut_elev - 1.5 * beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 3, [0, round(cut_elev - 1.5 * beam_type[4], 2)])
                    zero_length = 1.5 * beam_type[4]
                    break

    # zero_length = []
    # if ers_type == 1.0:
    #     for i in range(len(layers) - 1):
    #         if layers[i][0] >= cut_elev >= layers[i + 1][0]:
    #             if layers[i][1].type == 0:
    #                 new_elev = round(cut_elev - beam_type[4], 2)
    #                 for j in range(len(layers) - 1):
    #                     if layers[j][0] > new_elev > layers[j + 1][0]:
    #                         layers.insert(j + 1, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j + 1, [0, new_elev])
    #                         layers.insert(j + 2, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j + 2, [0, new_elev])
    #                         zero_length = beam_type[4]
    #                         break
    #                 else:
    #                     continue  # executed if the loop ended normally (no break)
    #                 break  # executed if 'continue' was skipped (break)
    #             if layers[i][1].type == 1:
    #                 new_elev = round(cut_elev - 1.5 * beam_type[4], 2)
    #                 for j in range(len(layers) - 1):
    #                     if layers[j][0] > new_elev > layers[j + 1][0]:
    #                         layers.insert(j + 1, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j + 1, [0, new_elev])
    #                         layers.insert(j + 2, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j + 2, [0, new_elev])
    #                         zero_length = 1.5*beam_type[4]
    #                         break
    #                 else:
    #                     continue  # executed if the loop ended normally (no break)
    #                 break  # executed if 'continue' was skipped (break)

    if berm_array != []:
        layers, work_points = berm_workpoints(layers, work_points, berm_array, cut_elev)

    if request.GET['footing_1_type'] != '':
        combined_footing_load = combine_footings(footings)
        layers, work_points = incorporate_footings(footings, combined_footing_load, layers, work_points, supplied_elev)

    if berm_array != []:
        layers = passive_heights(surface_side, berm_array, layers, cut_elev)

    if request.GET['train_1_distance'] != '':
        train_surcharge = combine_trains(trains)
        for i in range(len(layers)):
            for j in range(len(train_surcharge)):
                if layers[i][0] == train_surcharge[j][0]:
                    layers[i][4] = train_surcharge[j][1]

    wat_check = float(request.GET['wat_check'])
    if wat_check == 0:
        wat_output = []
        for i in range(len(layers)):
            layers[i].append(0)
    else:
        layers, wat_output = water_around_toe(layers, water_elev, cut_elev, supplied_elev)

    layers.sort(key=lambda x: x[0], reverse=True)

    footing_output = []
    for i in range(len(footings)):
        footing_output.append(text_output(footings[i], i + 1))
    footing_output = list(itertools.chain.from_iterable(footing_output))
    total_footing_surcharge = []
    for i in range(len(layers)):
        total_footing_surcharge.append("At elevation " + str(layers[i][0]) + "', total footing surcharge = " +
                                       str(layers[i][3]) + " psf.")
    if footings == []:
        total_footing_surcharge = []
    train_output = ["All rail surcharges calculated using the Cooper E80 method."]
    for i in range(len(layers)):
        train_output.append("At elevation " + str(layers[i][0]) + "', total lateral rail surcharge = " +
                            str(layers[i][4]) + " psf.")
    if trains == []:
        train_output = []

    surcharge = surcharge_heights(surface_side, surface_array, work_points, angle, angle_change_elev, angle_change_type,
                                  min_surcharge_height)
    for i in range(len(surcharge)):
        layers[i][2] = surcharge_unit_weight * (surcharge[i][1] - layers[0][0])
    surcharge_output = []
    for i in range(len(surcharge)):
        surcharge_string = "At elevation " + str(surcharge[i][0]) + "', assume design soil height at elevation " + \
                           str(surcharge[i][1]) + "'."
        surcharge_output.append(surcharge_string)

    berm_output = []
    if berm_array != []:
        for i in range(len(layers)):
            berm_string = "At elevation " + str(layers[i][0]) + "', assume passive soil height at elevation " + \
                          str(layers[i][5]) + "'."
            berm_output.append(berm_string)
    berm_reduction_output = []

    active = active_pressures(layers, water_elev, total_weights)
    passive = passive_pressures(layers, water_cut_elev, cut_elev, total_weights)
    if berm_array != []:
        passive, berm_reduction_output = berm_reduction(layers, berm_array, cut_elev, passive, water_cut_elev,
                                                        total_weights)
    water = water_pressures(layers, water_elev, water_cut_elev, total_weights, supplied_elev)
    active_pressure = active_pressures_output(layers, water_elev, total_weights)
    passive_pressure = passive_pressures_output(layers, water_cut_elev, cut_elev, total_weights)
    water_pressure = water_pressures_output(water)
    apparent = apparent_pressures(active, passive, water, cut_elev, diagram_type, backside_x,
                                  backside_y, layers, water_elev, total_weights, ers_type, beam_spacing, zero_length,
                                  beam_type, soldier_beam_method)

    if top_sheet[0] != layers[0][0]:
        apparent[0].insert(0, 0)
        apparent[1].insert(0, apparent[1][0])
        apparent[0].insert(0, 0)
        apparent[1].insert(0, top_sheet[0])
        apparent[2].insert(0, 0)
        apparent[3].insert(0, apparent[3][0])
        apparent[2].insert(0, 0)
        apparent[3].insert(0, top_sheet[0])
    beam_output = []
    if ers_type == 1 and soldier_beam_method == 0:
        beam_output = [("Soldier Beam Analysis Effective Widths : " + beam_type[1] + " @ " + str(beam_spacing) +
                        "' spacing"),
                       ("From elevation " + str(apparent[1][0]) + "' to elevation " + str(cut_elev) + "': W = " +
                        str(beam_spacing) + "'"),
                       ("From elevation " + str(cut_elev) + "' to elevation " + str(round(cut_elev - zero_length, 2)) +
                        "': W = 0 (net active W =" + str(beam_type[4]) + "')"),
                       ("At elevation " + str(round(cut_elev - zero_length, 2)) + "' and below: W = 3*" +
                        str(beam_type[4]) + "' = " + str(round(3 * beam_type[4], 2)) + "'")
                       ]
    if ers_type == 1 and soldier_beam_method == 1:
        beam_output = [
            ("Soldier Beam Analysis Effective Widths : " + beam_type[1] + " @ " + str(beam_spacing) + "' spacing"),
            ("From elevation " + str(apparent[1][0]) + "' to elevation " + str(cut_elev) + "': W = " + str(
                beam_spacing) + "'"),
            ("From elevation " + str(cut_elev) + "' to elevation " + str(round(cut_elev - zero_length, 2)) +
             "': W = 0 (net active W =" + str(beam_type[4]) + "')"),
            ("At elevation " + str(round(cut_elev - zero_length, 2)) + "' and below: W = 3*" + str(beam_type[4]) +
             "' = " + str(round(3 * beam_type[4], 2)) + "' for the passive pressures, and W = " + str(beam_type[4]) +
             "' for the active pressures.  Net pressure is limited negatively (passive side) by "
             "(Pa-Pp)*beam spacing")
        ]

    data = three_layer_minimum_length(apparent, brace_elevations)
    min_length = str(round(data[0], 2)) + "'"
    min_length_elev = str(round(data[1], 2)) + "'"
    waler_load = data[2]  # currently a list that contains all waler loads
    waler_load_output = data[7]
    design_text = data[3]
    min_length_pressure = data[4]
    multi = three_layer_multiplier(apparent, brace_elevations[2], data, supplied_length)
    moment = three_layer_maximum_moment(apparent, data[8], brace_elevations[2])
    max_moment_elevation = round(moment[1], 2)
    moment = math.ceil(moment[0])
    deflection = three_layer_deflection_calc(apparent, brace_elevations[2], data, sheet_type)
    zero_point = data[6]
    pressure_plot = multi_layer_pressure_plot(layers, apparent, brace_elevations, min_length_pressure, data[1], data[0],
                                              deflection, scale_factor, multi[1], multi[2], multi[3], zero_point)
    active_passive_plot = ap_plot(layers, active, passive, cut_elev, 0)
    water_pressure_plot = water_plot(layers, water)
    surface = surface_plot(surface_array, work_points)
    strut_diagram = strut_pressure_plot(layers, [apparent[2], apparent[3]], brace_elevations)
    bending_stress = round(moment * 12 / 1000 / sheet_type[2], 2)
    save(pressure_plot, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/pressure_plot.html')
    save(active_passive_plot, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/active_passive_plot.html')
    save(water_pressure_plot, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/water_pressure_plot.html')
    save(surface, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/surface.html')
    save(strut_diagram, 'C:/Users/tcorcoran/Desktop/thatchercalc/templates/strut_diagram.html')

    if save_calculation_name != '':
        url_output = str(request.build_absolute_uri)
        saved_calc = SavedCalc(name=save_calculation_name, data= (request.GET['footing_1_type'],request.GET['footing_1_width'],request.GET['footing_1_distance'],request.GET['footing_1_elevation'],request.GET['footing_1_load'],request.GET['footing_1_spacing_1'],request.GET['footing_1_spacing_2'],request.GET['footing_2_type'],request.GET['footing_2_width'],request.GET['footing_2_distance'],request.GET['footing_2_elevation'],request.GET['footing_2_load'],request.GET['footing_2_spacing_1'],request.GET['footing_2_spacing_2'],request.GET['footing_3_type'],request.GET['footing_3_width'],request.GET['footing_3_distance'],request.GET['footing_3_elevation'],request.GET['footing_3_load'],request.GET['footing_3_spacing_1'],request.GET['footing_3_spacing_2'],request.GET['footing_4_type'],request.GET['footing_4_width'],request.GET['footing_4_distance'],request.GET['footing_4_elevation'],request.GET['footing_4_load'],request.GET['footing_4_spacing_1'],request.GET['footing_4_spacing_2'],request.GET['train_1_distance'],request.GET['train_1_load'],request.GET['train_1_tie_size'],request.GET['train_1_elevation'],request.GET['train_2_distance'],request.GET['train_2_load'],request.GET['train_2_tie_size'],request.GET['train_2_elevation'],request.GET['train_3_distance'],request.GET['train_3_load'],request.GET['train_3_tie_size'],request.GET['train_3_elevation'],request.GET['train_4_distance'],request.GET['train_4_load'],request.GET['train_4_tie_size'],request.GET['train_4_elevation'],request.GET['surface_side'],request.GET['point0x'],request.GET['point0y'],request.GET['point1x'],request.GET['point1y'],request.GET['point2x'],request.GET['point2y'],request.GET['point3x'],request.GET['point3y'],request.GET['point4x'],request.GET['point4y'],request.GET['point5x'],request.GET['point5y'],request.GET['point6x'],request.GET['point6y'],request.GET['point7x'],request.GET['point7y'],request.GET['point8x'],request.GET['point8y'],request.GET['point9x'],request.GET['point9y'],request.GET['point10x'],request.GET['point10y'],request.GET['point11x'],request.GET['point11y'],request.GET['point12x'],request.GET['point12y'],request.GET['point13x'],request.GET['point13y'],request.GET['berm0x'],request.GET['berm0y'],request.GET['berm1x'],request.GET['berm1y'],request.GET['berm2x'],request.GET['berm2y'],request.GET['berm3x'],request.GET['berm3y'],request.GET['berm4x'],request.GET['berm4y'],request.GET['berm5x'],request.GET['berm5y'],request.GET['berm6x'],request.GET['berm6y'],request.GET['berm7x'],request.GET['berm7y'],request.GET['berm8x'],request.GET['berm8y'],request.GET['berm9x'],request.GET['berm9y'],request.GET['berm10x'],request.GET['berm10y'],request.GET['berm11x'],request.GET['berm11y'],request.GET['berm12x'],request.GET['berm12y'],request.GET['berm13x'],request.GET['berm13y'],request.GET['1.name'],request.GET['1.type'],request.GET['1.gamma'],request.GET['1.qu'],request.GET['1.ka'],request.GET['1.kp'],request.GET['1.phi'],request.GET['2.name'],request.GET['2.type'],request.GET['2.gamma'],request.GET['2.qu'],request.GET['2.ka'],request.GET['2.kp'],request.GET['2.phi'],request.GET['3.name'],request.GET['3.type'],request.GET['3.gamma'],request.GET['3.qu'],request.GET['3.ka'],request.GET['3.kp'],request.GET['3.phi'],request.GET['4.name'],request.GET['4.type'],request.GET['4.gamma'],request.GET['4.qu'],request.GET['4.ka'],request.GET['4.kp'],request.GET['4.phi'],request.GET['5.name'],request.GET['5.type'],request.GET['5.gamma'],request.GET['5.qu'],request.GET['5.ka'],request.GET['5.kp'],request.GET['5.phi'],request.GET['6.name'],request.GET['6.type'],request.GET['6.gamma'],request.GET['6.qu'],request.GET['6.ka'],request.GET['6.kp'],request.GET['6.phi'],request.GET['7.name'],request.GET['7.type'],request.GET['7.gamma'],request.GET['7.qu'],request.GET['7.ka'],request.GET['7.kp'],request.GET['7.phi'],request.GET['8.name'],request.GET['8.type'],request.GET['8.gamma'],request.GET['8.qu'],request.GET['8.ka'],request.GET['8.kp'],request.GET['8.phi'],request.GET['9.name'],request.GET['9.type'],request.GET['9.gamma'],request.GET['9.qu'],request.GET['9.ka'],request.GET['9.kp'],request.GET['9.phi'],request.GET['10.name'],request.GET['10.type'],request.GET['10.gamma'],request.GET['10.qu'],request.GET['10.ka'],request.GET['10.kp'],request.GET['10.phi'],request.GET['11.name'],request.GET['11.type'],request.GET['11.gamma'],request.GET['11.qu'],request.GET['11.ka'],request.GET['11.kp'],request.GET['11.phi'],request.GET['12.name'],request.GET['12.type'],request.GET['12.gamma'],request.GET['12.qu'],request.GET['12.ka'],request.GET['12.kp'],request.GET['12.phi'],request.GET['13.name'],request.GET['13.type'],request.GET['13.gamma'],request.GET['13.qu'],request.GET['13.ka'],request.GET['13.kp'],request.GET['14.phi'],request.GET['14.name'],request.GET['14.type'],request.GET['14.gamma'],request.GET['14.qu'],request.GET['14.ka'],request.GET['14.kp'],request.GET['15.phi'],request.GET['15.name'],request.GET['15.type'],request.GET['15.gamma'],request.GET['15.qu'],request.GET['15.ka'],request.GET['15.kp'],request.GET['16.phi'],request.GET['16.name'],request.GET['16.type'],request.GET['16.gamma'],request.GET['16.qu'],request.GET['16.ka'],request.GET['16.kp'],request.GET['17.phi'],request.GET['17.name'],request.GET['17.type'],request.GET['17.gamma'],request.GET['17.qu'],request.GET['17.ka'],request.GET['17.kp'],request.GET['18.phi'],request.GET['18.name'],request.GET['18.type'],request.GET['18.gamma'],request.GET['18.qu'],request.GET['18.ka'],request.GET['18.kp'],request.GET['19.phi'],request.GET['19.name'],request.GET['19.type'],request.GET['19.gamma'],request.GET['19.qu'],request.GET['19.ka'],request.GET['19.kp'],request.GET['20.phi'],request.GET['20.name'],request.GET['20.type'],request.GET['20.gamma'],request.GET['20.qu'],request.GET['20.ka'],request.GET['20.kp'],request.GET['wp1'],request.GET['wp1_layer'],request.GET['wp1_layer_front'],request.GET['wp2'],request.GET['wp2_layer'],request.GET['wp2_layer_front'],request.GET['wp3'],request.GET['wp3_layer'],request.GET['wp3_layer_front'],request.GET['wp4'],request.GET['wp4_layer'],request.GET['wp4_layer_front'],request.GET['wp5'],request.GET['wp5_layer'],request.GET['wp5_layer_front'],request.GET['wp6'],request.GET['wp6_layer'],request.GET['wp6_layer_front'],request.GET['wp7'],request.GET['wp7_layer'],request.GET['wp7_layer_front'],request.GET['wp8'],request.GET['wp8_layer'],request.GET['wp8_layer_front'],request.GET['wp9'],request.GET['wp9_layer'],request.GET['wp9_layer_front'],request.GET['wp10'],request.GET['wp10_layer'],request.GET['wp10_layer_front'],request.GET['wp11'],request.GET['wp11_layer'],request.GET['wp11_layer_front'],request.GET['wp12'],request.GET['wp12_layer'],request.GET['wp12_layer_front'],request.GET['wp13'],request.GET['wp13_layer'],request.GET['wp13_layer_front'],request.GET['wp14'],request.GET['wp14_layer'],request.GET['wp14_layer_front'],request.GET['wp15'],request.GET['wp15_layer'],request.GET['wp15_layer_front'],request.GET['wp16'],request.GET['wp16_layer'],request.GET['wp16_layer_front'],request.GET['wp17'],request.GET['wp17_layer'],request.GET['wp17_layer_front'],request.GET['wp18'],request.GET['wp18_layer'],request.GET['wp18_layer_front'],request.GET['wp19'],request.GET['wp19_layer'],request.GET['wp19_layer_front'],request.GET['wp20'],request.GET['wp20_layer'],request.GET['wp20_layer_front'],request.GET['wp21'],request.GET['wp21_layer'],request.GET['wp21_layer_front'],request.GET['wp22'],request.GET['wp22_layer'],request.GET['wp22_layer_front'],request.GET['wp23'],request.GET['wp23_layer'],request.GET['wp23_layer_front'],request.GET['wp24'],request.GET['wp24_layer'],request.GET['wp24_layer_front'],request.GET['wp25'],request.GET['wp25_layer'],request.GET['wp25_layer_front'],request.GET['wp26'],request.GET['wp26_layer'],request.GET['wp26_layer_front'],request.GET['wp27'],request.GET['wp27_layer'],request.GET['wp27_layer_front'],request.GET['wp28'],request.GET['wp28_layer'],request.GET['wp28_layer_front'],request.GET['wp29'],request.GET['wp29_layer'],request.GET['wp29_layer_front'],request.GET['wp30'],request.GET['wp30_layer'],request.GET['wp30_layer_front'],request.GET['wp31'],request.GET['wp31_layer'],request.GET['wp31_layer_front'],request.GET['wp32'],request.GET['wp32_layer'],request.GET['wp32_layer_front'],request.GET['wp33'],request.GET['wp33_layer'],request.GET['wp33_layer_front'],request.GET['wp34'],request.GET['wp34_layer'],request.GET['wp34_layer_front'],request.GET['wp35'],request.GET['wp35_layer'],request.GET['wp35_layer_front'],request.GET['wp36'],request.GET['wp36_layer'],request.GET['wp36_layer_front'],request.GET['wp37'],request.GET['wp37_layer'],request.GET['wp37_layer_front'],request.GET['wp38'],request.GET['wp38_layer'],request.GET['wp38_layer_front'],request.GET['wp39'],request.GET['wp39_layer'],request.GET['wp39_layer_front'],request.GET['wp40'],request.GET['wp40_layer'],request.GET['wp40_layer_front'],request.GET['surcharge_unit_weight'],request.GET['min_surcharge_height'],request.GET['angle'],request.GET['angle_change_elev'],request.GET['water_elev'],request.GET['cut_elev'],request.GET['total_weights'],request.GET['top_brace_elev'],request.GET['mid_brace_elev'],request.GET['bot_brace_elev'],request.GET['diagram_type'],request.GET['backside_x'],request.GET['backside_y'],request.GET['scale_factor'],request.GET['sheet_type'],request.GET['beam_type'],request.GET['water_cut_elev'],request.GET['top_sheet'],request.GET['beam_spacing'],request.GET['beam_size_override'],request.GET['beam_override'],request.GET['beam_modulus_override'],request.GET['beam_inertia_override'],request.GET['ers_type'],request.GET['soldier_beam_method'],request.GET['supplied_length'],request.GET['wat_check'],request.GET['angle_change_type'],request.GET['13.phi'])
,type="Three Layer Braced")
        saved_calc.save()

    return render(request, "three_output.html", {"surcharge": surcharge_output,
                                                 "layers": layers,
                                                 "active_pressures": active_pressure,
                                                 "passive_pressures": passive_pressure,
                                                 "water_pressures": water_pressure,
                                                 "min_length": min_length,
                                                 "min_length_elev": min_length_elev,
                                                 "waler_load": waler_load_output,
                                                 "design_text": design_text,
                                                 "multiplier": multi[0],
                                                 "moment": moment,
                                                 "deflection": deflection[1],
                                                 "deflection_elev": deflection[2],
                                                 "footing_output": footing_output,
                                                 "total_footing_surcharge": total_footing_surcharge,
                                                 "sheet_type": sheet_type[1],
                                                 "bending_stress": bending_stress,
                                                 "train_output": train_output,
                                                 "beam_output": beam_output,
                                                 "wat_output": wat_output,
                                                 "berm_output": berm_output,
                                                 "berm_reduction_output": berm_reduction_output,
                                                 "soldier_beam_method": soldier_beam_method,
                                                 "net_output": apparent[4],
                                                 "max_moment_elevation": max_moment_elevation,
                                                 "min_length_work_moments": data[5],
                                                 "multiplier_supplied_length": multi[4],
                                                 "multiplier_value": round(multi[3], 2),
                                                 "I": sheet_type[3],
                                                 "Sx": sheet_type[2]
                                                 })


def micropile_output(request):
    description = request.GET['description']
    L = float(request.GET['L'])
    h = float(request.GET['h'])
    D = float(request.GET['D'])
    alpha = float(request.GET['alpha'])
    ID = float(request.GET['ID'])
    OD = float(request.GET['OD'])
    OD_joint = round(D-2*h, 3)
    D_female = float(request.GET['D_female'])
    Yp = int(request.GET['Yp'])
    Up = int(request.GET['Up'])
    corrosion_reduction = float(request.GET['corrosion_reduction'])
    OD_corrosion = OD + 2*corrosion_reduction

    solution = joint_capacity_function(L, h, D, alpha, ID, OD, D_female, Yp, Up, corrosion_reduction)
    Pi = solution[0]
    Pfr = solution[1]
    limit_load = solution[2]
    limit_load_description = solution[3]
    x_prime = solution[4]
    theta_0 = round(solution[5], 3)
    theta_1 = round(solution[6], 3)
    theta_2 = round(solution[7], 3),
    I_above = solution[8]
    I_below = solution[9]
    I_reduced = solution[10]
    I_full = round(solution[11], 2)
    intact_stiffness_percentage = round(solution[12], 2)
    pin_stress = round(solution[13], 2)
    area_compression = round(solution[14], 3)
    area_tension = round(solution[15], 3)
    Cc = round(solution[16], 3)
    Ct = round(solution[17], 3)
    Pc = round(pin_stress*area_tension, 2)
    Pt = Pc
    Mc = round(solution[18], 2)
    Mt = round(solution[19], 2)
    Mtotal = round(solution[20], 2)
    Mmax = round(solution[21], 2)
    intact_moment_percentage = round(100*solution[22], 2)
    allowable_capacity = round(solution[23], 2)
    I_gross = round(solution[24], 2)
    gross_stiffness_percentage = solution[25]
    Mgross = round(solution[26], 2)
    gross_moment_percentage = round(100*solution[27], 2)
    Ap = round(solution[28], 2)
    Ab = round(solution[29], 2)
    Pi_box = round(solution[30], 2)
    Pfr_box = round(solution[31], 2)
    image_check = solution[32]
    A1_correction = round(solution[33], 2)
    A2_correction = round(solution[34], 2)

    return render(request, "micropile_output.html", {"solution": solution,
                                                     "L": L,
                                                     "h": h,
                                                     "D": D,
                                                     "alpha": alpha,
                                                     "ID": ID,
                                                     "OD": OD,
                                                     "OD_joint": OD_joint,
                                                     "Yp": Yp,
                                                     "Up": Up,
                                                     "Pi": Pi,
                                                     "Pfr": Pfr,
                                                     "limit_load": limit_load,
                                                     "limit_load_description": limit_load_description,
                                                     "x_prime": x_prime,
                                                     "theta_0": theta_0,
                                                     "theta_1": theta_1,
                                                     "theta_2": theta_2,
                                                     "I_above": I_above,
                                                     "I_below": I_below,
                                                     "I_reduced": I_reduced,
                                                     "I_full": I_full,
                                                     "intact_stiffness_percentage": intact_stiffness_percentage,
                                                     "pin_stress": pin_stress,
                                                     "area_tension": area_tension,
                                                     "area_compression": area_compression,
                                                     "Ct": Ct,
                                                     "Cc": Cc,
                                                     "Pc": Pc,
                                                     "Pt": Pt,
                                                     "Mc": Mc,
                                                     "Mt": Mt,
                                                     "Mtotal": Mtotal,
                                                     "Mmax": Mmax,
                                                     "intact_moment_percentage": intact_moment_percentage,
                                                     "allowable_capacity": allowable_capacity,
                                                     "description": description,
                                                     "corrosion_reduction": corrosion_reduction,
                                                     "OD_corrosion": OD_corrosion,
                                                     "I_gross": I_gross,
                                                     "gross_stiffness_percentage": gross_stiffness_percentage,
                                                     "Mgross": Mgross,
                                                     "gross_moment_percentage": gross_moment_percentage,
                                                     "Ap": Ap,
                                                     "Ab": Ab,
                                                     "Pi_box": Pi_box,
                                                     "Pfr_box": Pfr_box,
                                                     "D_female": D_female,
                                                     "image_check": image_check,
                                                     "A1_correction": A1_correction,
                                                     "A2_correction": A2_correction,
                                                     })


def optimizer_output(request):
    # TAKE INPUT DATA FROM USER
    footings = []
    trains = []
    # footing_surcharge(type, width, distance, elevation, load, spacing_1, spacing_2)
    if request.GET['footing_1_type'] != '':
        footing_1 = footing_surcharge(float(request.GET['footing_1_type']),
                                      float(request.GET['footing_1_width']),
                                      float(request.GET['footing_1_distance']),
                                      float(request.GET['footing_1_elevation']),
                                      float(request.GET['footing_1_load']),
                                      float(request.GET['footing_1_spacing_1']),
                                      float(request.GET['footing_1_spacing_2']))
        footings.append(footing_1)
    if request.GET['footing_2_type'] != '':
        footing_2 = footing_surcharge(float(request.GET['footing_2_type']),
                                      float(request.GET['footing_2_width']),
                                      float(request.GET['footing_2_distance']),
                                      float(request.GET['footing_2_elevation']),
                                      float(request.GET['footing_2_load']),
                                      float(request.GET['footing_2_spacing_1']),
                                      float(request.GET['footing_2_spacing_2']))
        footings.append(footing_2)
    if request.GET['footing_3_type'] != '':
        footing_3 = footing_surcharge(float(request.GET['footing_3_type']),
                                      float(request.GET['footing_3_width']),
                                      float(request.GET['footing_3_distance']),
                                      float(request.GET['footing_3_elevation']),
                                      float(request.GET['footing_3_load']),
                                      float(request.GET['footing_3_spacing_1']),
                                      float(request.GET['footing_3_spacing_2']))
        footings.append(footing_3)
    if request.GET['footing_4_type'] != '':
        footing_4 = footing_surcharge(float(request.GET['footing_4_type']),
                                      float(request.GET['footing_4_width']),
                                      float(request.GET['footing_4_distance']),
                                      float(request.GET['footing_4_elevation']),
                                      float(request.GET['footing_4_load']),
                                      float(request.GET['footing_4_spacing_1']),
                                      float(request.GET['footing_4_spacing_2']))
        footings.append(footing_4)

    if request.GET['train_1_distance'] != '':
        train_1 = train_loading(float(request.GET['train_1_distance']),
                                float(request.GET['train_1_load']),
                                float(request.GET['train_1_tie_size']),
                                float(request.GET['train_1_elevation'])
                                )
        trains.append(train_1)
    if request.GET['train_2_distance'] != '':
        train_2 = train_loading(float(request.GET['train_2_distance']),
                                float(request.GET['train_2_load']),
                                float(request.GET['train_2_tie_size']),
                                float(request.GET['train_2_elevation'])
                                )
        trains.append(train_2)
    if request.GET['train_3_distance'] != '':
        train_3 = train_loading(float(request.GET['train_3_distance']),
                                float(request.GET['train_3_load']),
                                float(request.GET['train_3_tie_size']),
                                float(request.GET['train_3_elevation'])
                                )
        trains.append(train_3)
    if request.GET['train_4_distance'] != '':
        train_4 = train_loading(float(request.GET['train_4_distance']),
                                float(request.GET['train_4_load']),
                                float(request.GET['train_4_tie_size']),
                                float(request.GET['train_4_elevation'])
                                )
        trains.append(train_4)

    surface_side = float(request.GET['surface_side'])

    surface_array = [(request.GET['point0x'], request.GET['point0y']),
                     (request.GET['point1x'], request.GET['point1y']),
                     (request.GET['point2x'], request.GET['point2y']),
                     (request.GET['point3x'], request.GET['point3y']),
                     (request.GET['point4x'], request.GET['point4y']),
                     (request.GET['point5x'], request.GET['point5y']),
                     (request.GET['point6x'], request.GET['point6y']),
                     (request.GET['point7x'], request.GET['point7y']),
                     (request.GET['point8x'], request.GET['point8y']),
                     (request.GET['point9x'], request.GET['point9y']),
                     (request.GET['point10x'], request.GET['point10y']),
                     (request.GET['point11x'], request.GET['point11y']),
                     (request.GET['point12x'], request.GET['point12y']),
                     (request.GET['point13x'], request.GET['point13y'])]
    new_surface_array = []  # Remove all points with no entries

    # Pare down surface array points to just the ones that were entered
    for i in range(len(surface_array)):
        if surface_array[i] != ('', ''):
            new_surface_array.append(surface_array[i])
    surface_array = []
    for i in range(len(new_surface_array)):
        surface_array.append(((float(new_surface_array[i][0])), float(new_surface_array[i][1])))

    berm_array = []
    if request.GET['berm0x'] != '':
        berm_array = [(request.GET['berm0x'], request.GET['berm0y']),
                      (request.GET['berm1x'], request.GET['berm1y']),
                      (request.GET['berm2x'], request.GET['berm2y']),
                      (request.GET['berm3x'], request.GET['berm3y']),
                      (request.GET['berm4x'], request.GET['berm4y']),
                      (request.GET['berm5x'], request.GET['berm5y']),
                      (request.GET['berm6x'], request.GET['berm6y']),
                      (request.GET['berm7x'], request.GET['berm7y']),
                      (request.GET['berm8x'], request.GET['berm8y']),
                      (request.GET['berm9x'], request.GET['berm9y']),
                      (request.GET['berm10x'], request.GET['berm10y']),
                      (request.GET['berm11x'], request.GET['berm11y']),
                      (request.GET['berm12x'], request.GET['berm12y']),
                      (request.GET['berm13x'], request.GET['berm13y'])]
        new_berm_array = []  # Remove all points with no entries

        # Pare down surface array points to just the ones that were entered
        for i in range(len(berm_array)):
            if berm_array[i] != ('', ''):
                new_berm_array.append(berm_array[i])
        berm_array = []
        for i in range(len(new_berm_array)):
            berm_array.append(((float(new_berm_array[i][0])), float(new_berm_array[i][1])))

    if request.GET['1.name'] != '':  # If layer doesn't have a name, assume it does not exist and do not input it.
        layer_1 = Layer(request.GET['1.name'], float(request.GET['1.type']), float(request.GET['1.gamma']),
                        float(request.GET['1.qu']),
                        float(request.GET['1.ka']), float(request.GET['1.kp']),
                        float(request.GET['1.phi']))
    if request.GET['2.name'] != '':
        layer_2 = Layer(request.GET['2.name'], float(request.GET['2.type']), float(request.GET['2.gamma']),
                        float(request.GET['2.qu']),
                        float(request.GET['2.ka']), float(request.GET['2.kp']),
                        float(request.GET['2.phi']))
    if request.GET['3.name'] != '':
        layer_3 = Layer(request.GET['3.name'], float(request.GET['3.type']), float(request.GET['3.gamma']),
                        float(request.GET['3.qu']),
                        float(request.GET['3.ka']), float(request.GET['3.kp']),
                        float(request.GET['3.phi']))
    if request.GET['4.name'] != '':
        layer_4 = Layer(request.GET['4.name'], float(request.GET['4.type']), float(request.GET['4.gamma']),
                        float(request.GET['4.qu']),
                        float(request.GET['4.ka']), float(request.GET['4.kp']),
                        float(request.GET['4.phi']))
    if request.GET['5.name'] != '':
        layer_5 = Layer(request.GET['5.name'], float(request.GET['5.type']), float(request.GET['5.gamma']),
                        float(request.GET['5.qu']),
                        float(request.GET['5.ka']), float(request.GET['5.kp']),
                        float(request.GET['5.phi']))
    if request.GET['6.name'] != '':
        layer_6 = Layer(request.GET['6.name'], float(request.GET['6.type']), float(request.GET['6.gamma']),
                        float(request.GET['6.qu']),
                        float(request.GET['6.ka']), float(request.GET['6.kp']),
                        float(request.GET['6.phi']))
    if request.GET['7.name'] != '':
        layer_7 = Layer(request.GET['7.name'], float(request.GET['7.type']), float(request.GET['7.gamma']),
                        float(request.GET['7.qu']),
                        float(request.GET['7.ka']), float(request.GET['7.kp']),
                        float(request.GET['7.phi']))
    if request.GET['8.name'] != '':
        layer_8 = Layer(request.GET['8.name'], float(request.GET['8.type']), float(request.GET['8.gamma']),
                        float(request.GET['8.qu']),
                        float(request.GET['8.ka']), float(request.GET['8.kp']),
                        float(request.GET['8.phi']))
    if request.GET['9.name'] != '':
        layer_9 = Layer(request.GET['9.name'], float(request.GET['9.type']), float(request.GET['9.gamma']),
                        float(request.GET['9.qu']),
                        float(request.GET['9.ka']), float(request.GET['9.kp']),
                        float(request.GET['9.phi']))
    if request.GET['10.name'] != '':
        layer_10 = Layer(request.GET['10.name'], float(request.GET['10.type']), float(request.GET['10.gamma']),
                         float(request.GET['10.qu']),
                         float(request.GET['10.ka']), float(request.GET['10.kp']),
                         float(request.GET['10.phi']))
    if request.GET['11.name'] != '':
        layer_11 = Layer(request.GET['11.name'], float(request.GET['11.type']), float(request.GET['11.gamma']),
                         float(request.GET['11.qu']),
                         float(request.GET['11.ka']), float(request.GET['11.kp']),
                         float(request.GET['11.phi']))
    if request.GET['12.name'] != '':
        layer_12 = Layer(request.GET['12.name'], float(request.GET['12.type']), float(request.GET['12.gamma']),
                         float(request.GET['12.qu']),
                         float(request.GET['12.ka']), float(request.GET['12.kp']),
                         float(request.GET['12.phi']))
    if request.GET['13.name'] != '':
        layer_13 = Layer(request.GET['13.name'], float(request.GET['13.type']), float(request.GET['13.gamma']),
                         float(request.GET['13.qu']),
                         float(request.GET['13.ka']), float(request.GET['13.kp']),
                         float(request.GET['13.phi']))
    if request.GET['14.name'] != '':
        layer_14 = Layer(request.GET['14.name'], float(request.GET['14.type']), float(request.GET['14.gamma']),
                         float(request.GET['14.qu']),
                         float(request.GET['14.ka']), float(request.GET['14.kp']),
                         float(request.GET['14.phi']))

    # elevation, layer, soil surcharge placeholder, footing placeholder, train placeholder, passive height placeholder
    layers = [[request.GET['wp1'], request.GET['wp1_layer'], 0, 0, 0, 10000, request.GET['wp1_layer_front']],
              [request.GET['wp2'], request.GET['wp2_layer'], 0, 0, 0, 10000, request.GET['wp2_layer_front']],
              [request.GET['wp3'], request.GET['wp3_layer'], 0, 0, 0, 10000, request.GET['wp3_layer_front']],
              [request.GET['wp4'], request.GET['wp4_layer'], 0, 0, 0, 10000, request.GET['wp4_layer_front']],
              [request.GET['wp5'], request.GET['wp5_layer'], 0, 0, 0, 10000, request.GET['wp5_layer_front']],
              [request.GET['wp6'], request.GET['wp6_layer'], 0, 0, 0, 10000, request.GET['wp6_layer_front']],
              [request.GET['wp7'], request.GET['wp7_layer'], 0, 0, 0, 10000, request.GET['wp7_layer_front']],
              [request.GET['wp8'], request.GET['wp8_layer'], 0, 0, 0, 10000, request.GET['wp8_layer_front']],
              [request.GET['wp9'], request.GET['wp9_layer'], 0, 0, 0, 10000, request.GET['wp9_layer_front']],
              [request.GET['wp10'], request.GET['wp10_layer'], 0, 0, 0, 10000, request.GET['wp10_layer_front']],
              [request.GET['wp11'], request.GET['wp11_layer'], 0, 0, 0, 10000, request.GET['wp11_layer_front']],
              [request.GET['wp12'], request.GET['wp12_layer'], 0, 0, 0, 10000, request.GET['wp12_layer_front']],
              [request.GET['wp13'], request.GET['wp13_layer'], 0, 0, 0, 10000, request.GET['wp13_layer_front']],
              [request.GET['wp14'], request.GET['wp14_layer'], 0, 0, 0, 10000, request.GET['wp14_layer_front']],
              [request.GET['wp15'], request.GET['wp15_layer'], 0, 0, 0, 10000, request.GET['wp15_layer_front']],
              [request.GET['wp16'], request.GET['wp16_layer'], 0, 0, 0, 10000, request.GET['wp16_layer_front']],
              [request.GET['wp17'], request.GET['wp17_layer'], 0, 0, 0, 10000, request.GET['wp17_layer_front']],
              [request.GET['wp18'], request.GET['wp18_layer'], 0, 0, 0, 10000, request.GET['wp18_layer_front']],
              [request.GET['wp19'], request.GET['wp19_layer'], 0, 0, 0, 10000, request.GET['wp19_layer_front']],
              [request.GET['wp20'], request.GET['wp20_layer'], 0, 0, 0, 10000, request.GET['wp20_layer_front']],
              [request.GET['wp21'], request.GET['wp21_layer'], 0, 0, 0, 10000, request.GET['wp21_layer_front']],
              [request.GET['wp22'], request.GET['wp22_layer'], 0, 0, 0, 10000, request.GET['wp22_layer_front']],
              [request.GET['wp23'], request.GET['wp23_layer'], 0, 0, 0, 10000, request.GET['wp23_layer_front']],
              [request.GET['wp24'], request.GET['wp24_layer'], 0, 0, 0, 10000, request.GET['wp24_layer_front']],
              [request.GET['wp25'], request.GET['wp25_layer'], 0, 0, 0, 10000, request.GET['wp25_layer_front']],
              [request.GET['wp26'], request.GET['wp26_layer'], 0, 0, 0, 10000, request.GET['wp26_layer_front']],
              [request.GET['wp27'], request.GET['wp27_layer'], 0, 0, 0, 10000, request.GET['wp27_layer_front']],
              [request.GET['wp28'], request.GET['wp28_layer'], 0, 0, 0, 10000, request.GET['wp28_layer_front']],
              [request.GET['wp29'], request.GET['wp29_layer'], 0, 0, 0, 10000, request.GET['wp29_layer_front']],
              [request.GET['wp30'], request.GET['wp30_layer'], 0, 0, 0, 10000, request.GET['wp30_layer_front']],
              [request.GET['wp31'], request.GET['wp31_layer'], 0, 0, 0, 10000, request.GET['wp31_layer_front']],
              [request.GET['wp32'], request.GET['wp32_layer'], 0, 0, 0, 10000, request.GET['wp32_layer_front']],
              [request.GET['wp33'], request.GET['wp33_layer'], 0, 0, 0, 10000, request.GET['wp33_layer_front']],
              [request.GET['wp34'], request.GET['wp34_layer'], 0, 0, 0, 10000, request.GET['wp34_layer_front']],
              [request.GET['wp35'], request.GET['wp35_layer'], 0, 0, 0, 10000, request.GET['wp35_layer_front']],
              [request.GET['wp36'], request.GET['wp36_layer'], 0, 0, 0, 10000, request.GET['wp36_layer_front']],
              [request.GET['wp37'], request.GET['wp37_layer'], 0, 0, 0, 10000, request.GET['wp37_layer_front']],
              [request.GET['wp38'], request.GET['wp38_layer'], 0, 0, 0, 10000, request.GET['wp38_layer_front']],
              [request.GET['wp39'], request.GET['wp39_layer'], 0, 0, 0, 10000, request.GET['wp39_layer_front']],
              [request.GET['wp40'], request.GET['wp40_layer'], 0, 0, 0, 10000, request.GET['wp40_layer_front']]]

    new_layers = []  # Remove all layers with no entries
    for i in range(len(layers)):
        if layers[i] != ['', '', 0, 0, 0, 10000, '']:
            new_layers.append(layers[i])
    layers = []
    for i in range(len(new_layers)):
        layers.append([float(new_layers[i][0]), float(new_layers[i][1]), float(new_layers[i][2]),
                       float(new_layers[i][3]), float(new_layers[i][4]), float(new_layers[i][5]),
                       float(new_layers[i][6])])

    work_points = [[0, request.GET['wp1']],
                   [0, request.GET['wp2']],
                   [0, request.GET['wp3']],
                   [0, request.GET['wp4']],
                   [0, request.GET['wp5']],
                   [0, request.GET['wp6']],
                   [0, request.GET['wp7']],
                   [0, request.GET['wp8']],
                   [0, request.GET['wp9']],
                   [0, request.GET['wp10']],
                   [0, request.GET['wp11']],
                   [0, request.GET['wp12']],
                   [0, request.GET['wp13']],
                   [0, request.GET['wp14']],
                   [0, request.GET['wp15']],
                   [0, request.GET['wp16']],
                   [0, request.GET['wp17']],
                   [0, request.GET['wp18']],
                   [0, request.GET['wp19']],
                   [0, request.GET['wp20']],
                   [0, request.GET['wp21']],
                   [0, request.GET['wp22']],
                   [0, request.GET['wp23']],
                   [0, request.GET['wp24']],
                   [0, request.GET['wp25']],
                   [0, request.GET['wp26']],
                   [0, request.GET['wp27']],
                   [0, request.GET['wp28']],
                   [0, request.GET['wp29']],
                   [0, request.GET['wp30']],
                   [0, request.GET['wp31']],
                   [0, request.GET['wp32']],
                   [0, request.GET['wp33']],
                   [0, request.GET['wp34']],
                   [0, request.GET['wp35']],
                   [0, request.GET['wp36']],
                   [0, request.GET['wp37']],
                   [0, request.GET['wp38']],
                   [0, request.GET['wp39']],
                   [0, request.GET['wp40']]
                   ]

    new_work_points = []  # Remove all points with no entries
    for i in range(len(work_points)):
        if work_points[i] != [0, '']:
            new_work_points.append(work_points[i])
    work_points = []
    for i in range(len(new_work_points)):
        work_points.append([(float(new_work_points[i][0])), float(new_work_points[i][1])])

    surcharge_unit_weight = float(request.GET['surcharge_unit_weight'])
    min_surcharge_height = request.GET['min_surcharge_height']
    if min_surcharge_height:
        min_surcharge_height = float(min_surcharge_height)
    else:
        min_surcharge_height = []
    angle = float(request.GET['angle'])

    angle_change_elev = request.GET['angle_change_elev']
    if angle_change_elev:
        angle_change_elev = float(angle_change_elev)
    else:
        angle_change_elev = []

    angle_change_type = float(request.GET['angle_change_type'])

    water_elev = request.GET['water_elev']
    if water_elev:
        water_elev = float(water_elev)
    else:
        water_elev = float(-10000)

    cut_elev = float(request.GET['cut_elev'])
    surface_elev = float(request.GET['surface_elev'])
    total_weights = float(request.GET['total_weights'])
    sheet_type = float(request.GET['sheet_type'])
    beam_type = float(request.GET['beam_type'])
    beam_spacing = []

    water_cut_elev = cut_elev
    if water_elev == float(-10000):
        water_cut_elev = float(-10000)
    if request.GET['water_cut_elev'] != '':
        water_cut_elev = float(request.GET['water_cut_elev'])

    top_sheet = [layers[0][0]]
    if request.GET['top_sheet'] != '':
        top_sheet = [float(request.GET['top_sheet'])]

    for i in range(len(sheet_database)):
        if sheet_type == sheet_database[i][0]:
            sheet_type = sheet_database[i]
    for i in range(len(beam_database)):
        if beam_type == beam_database[i][0]:
            beam_type = beam_database[i]

    if request.GET['beam_spacing'] != '':
        beam_spacing = float(request.GET['beam_spacing'])

    ers_type = float(request.GET['ers_type'])
    if ers_type == 1:
        sheet_type = beam_type

    soldier_beam_method = float(request.GET['soldier_beam_method'])

    #  MANIPULATE USER DATA
    for i in range(len(layers)):  # Assign layer properties to work points
        if layers[i][1] == 1.0:
            layers[i][1] = layer_1
        if layers[i][1] == 2.0:
            layers[i][1] = layer_2
        if layers[i][1] == 3.0:
            layers[i][1] = layer_3
        if layers[i][1] == 4.0:
            layers[i][1] = layer_4
        if layers[i][1] == 5.0:
            layers[i][1] = layer_5
        if layers[i][1] == 6.0:
            layers[i][1] = layer_6
        if layers[i][1] == 7.0:
            layers[i][1] = layer_7
        if layers[i][1] == 8.0:
            layers[i][1] = layer_8
        if layers[i][1] == 9.0:
            layers[i][1] = layer_9
        if layers[i][1] == 10.0:
            layers[i][1] = layer_10
        if layers[i][1] == 11.0:
            layers[i][1] = layer_11
        if layers[i][1] == 12.0:
            layers[i][1] = layer_12
        if layers[i][1] == 13.0:
            layers[i][1] = layer_13
        if layers[i][1] == 14.0:
            layers[i][1] = layer_14
    for i in range(len(layers)):  # Assign layer properties to work points
        if layers[i][6] == 1.0:
            layers[i][6] = layer_1
        if layers[i][6] == 2.0:
            layers[i][6] = layer_2
        if layers[i][6] == 3.0:
            layers[i][6] = layer_3
        if layers[i][6] == 4.0:
            layers[i][6] = layer_4
        if layers[i][6] == 5.0:
            layers[i][6] = layer_5
        if layers[i][6] == 6.0:
            layers[i][6] = layer_6
        if layers[i][6] == 7.0:
            layers[i][6] = layer_7
        if layers[i][6] == 8.0:
            layers[i][6] = layer_8
        if layers[i][6] == 9.0:
            layers[i][6] = layer_9
        if layers[i][6] == 10.0:
            layers[i][6] = layer_10
        if layers[i][6] == 11.0:
            layers[i][6] = layer_11
        if layers[i][6] == 12.0:
            layers[i][6] = layer_12
        if layers[i][6] == 13.0:
            layers[i][6] = layer_13
        if layers[i][6] == 14.0:
            layers[i][6] = layer_14

    zero_length = []
    if ers_type == 1.0:
        for i in range(len(layers) - 1):
            if layers[i][0] >= cut_elev >= layers[i + 1][0]:
                if layers[i][1].type == 0:
                    layers.insert(i + 2,
                                  [round(cut_elev - beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 2, [0, round(cut_elev - beam_type[4], 2)])
                    layers.insert(i + 3,
                                  [round(cut_elev - beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 3, [0, round(cut_elev - beam_type[4], 2)])
                    zero_length = beam_type[4]
                    break
                if layers[i][1].type == 1:
                    layers.insert(i + 2,
                                  [round(cut_elev - 1.5 * beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 2, [0, round(cut_elev - 1.5 * beam_type[4], 2)])
                    layers.insert(i + 3,
                                  [round(cut_elev - 1.5 * beam_type[4], 2), layers[i][1], 0, 0, 0, 10000, layers[i][6]])
                    work_points.insert(i + 3, [0, round(cut_elev - 1.5 * beam_type[4], 2)])
                    zero_length = 1.5 * beam_type[4]
                    break

    # zero_length = []
    # if ers_type == 1.0:
    #     for i in range(len(layers) - 1):
    #         if layers[i][0] >= cut_elev >= layers[i + 1][0]:
    #             if layers[i][1].type == 0:
    #                 new_elev = round(cut_elev-beam_type[4], 2)
    #                 for j in range(len(layers) - 1):
    #                     if layers[j][0] > new_elev > layers[j + 1][0]:
    #                         layers.insert(j+1, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j+1, [0, new_elev])
    #                         layers.insert(j+2, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j+2, [0, new_elev])
    #                         zero_length = beam_type[4]
    #                         break
    #                 else:
    #                     continue  # executed if the loop ended normally (no break)
    #                 break  # executed if 'continue' was skipped (break)
    #             if layers[i][1].type == 1:
    #                 new_elev = round(cut_elev - 1.5*beam_type[4], 2)
    #                 for j in range(len(layers) - 1):
    #                     if layers[j][0] > new_elev > layers[j + 1][0]:
    #                         layers.insert(j+1, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j+1, [0, new_elev])
    #                         layers.insert(j+2, [new_elev, layers[j][1], 0, 0, 0, 10000])
    #                         work_points.insert(j+2, [0, new_elev])
    #                         zero_length = 1.5*beam_type[4]
    #                         break
    #                 else:
    #                     continue  # executed if the loop ended normally (no break)
    #                 break  # executed if 'continue' was skipped (break)

    if berm_array != []:
        layers, work_points = berm_workpoints(layers, work_points, berm_array, cut_elev)

    if request.GET['footing_1_type'] != '':
        combined_footing_load = combine_footings(footings)
        layers, work_points = incorporate_footings(footings, combined_footing_load, layers, work_points, 1000)

    if berm_array != []:
        layers = passive_heights(surface_side, berm_array, layers, cut_elev)

    if request.GET['train_1_distance'] != '':
        train_surcharge = combine_trains(trains)
        for i in range(len(layers)):
            for j in range(len(train_surcharge)):
                if layers[i][0] == train_surcharge[j][0]:
                    layers[i][4] = train_surcharge[j][1]

    wat_check = float(request.GET['wat_check'])
    if wat_check == 0:
        wat_output = []
        for i in range(len(layers)):
            layers[i].append(0)
    else:
        layers, wat_output = water_around_toe(layers, water_elev, cut_elev, 1000)

    layers.sort(key=lambda x: x[0], reverse=True)

    surcharge = surcharge_heights(surface_side, surface_array, work_points, angle, angle_change_elev, angle_change_type,
                                  min_surcharge_height)
    for i in range(len(surcharge)):
        layers[i][2] = surcharge_unit_weight * (surcharge[i][1] - layers[0][0])


    ######## BEGIN OPTIMIZATION ITERATIONS HERE ############
    start_iterations = int(request.GET['start_iterations'])
    end_iterations = int(request.GET['end_iterations'])
    def_sheet_database = sorted(sheet_database, key = lambda x: int(x[3]))
    def_beam_database = sorted(beam_database, key = lambda x: int(x[3]))
    bending_sheet_database = sorted(sheet_database, key = lambda x: int(x[2]))
    bending_beam_database = sorted(beam_database, key = lambda x: int(x[2]))

    # iterate brace elevation to determine minimum length, minimum moment, minimum deflection
    total_iterations = math.floor(start_iterations - end_iterations)
    iterations = []
    for i in range(start_iterations, end_iterations, -1):
        iterations.append([i])

    for iteration in iterations:
        for i in range(1, len(layers)):
            if layers[i-1][0] > iteration[0]-2 > layers[i][0] and iteration[0]-2 != layers[i][0]:
                layers.insert(i, [iteration[0]-2, layers[i][1], 0.0, 0.0, 0.0, 10000, layers[i][6],0])
                work_points.insert(i, [0, iteration[0]-2])
                break

    surcharge = surcharge_heights(surface_side, surface_array, work_points, angle, angle_change_elev, angle_change_type,
                                  min_surcharge_height)
    for i in range(len(surcharge)):
        layers[i][2] = surcharge_unit_weight * (surcharge[i][1] - layers[0][0])
    for iteration in iterations:
        start = timer()
        brace_elev = iteration[0]
        cantilever_cut_elev = brace_elev - 2
        cant_water_cut_elev = -999999
        if water_elev >= cantilever_cut_elev:
            cant_water_cut_elev = cantilever_cut_elev
        else:
            cant_water_cut_elev = water_elev

        active = active_pressures(layers, water_elev, total_weights)
        cant_passive = passive_pressures(layers, cant_water_cut_elev, cantilever_cut_elev, total_weights)
        braced_passive = passive_pressures(layers, water_cut_elev, cut_elev, total_weights)
        if berm_array != []:
            cant_passive, berm_reduction_output = berm_reduction(layers, berm_array, cut_elev, cant_passive, cant_water_cut_elev, total_weights)
            braced_passive, berm_reduction_output = berm_reduction(layers, berm_array, cut_elev, braced_passive, water_cut_elev, total_weights)
        active_cant = active_pressures_front(layers, water_cut_elev, cantilever_cut_elev, total_weights)
        passive_cant = passive_pressures_back(layers, water_elev, cantilever_cut_elev, surface_elev, total_weights)
        cant_water = water_pressures(layers, water_elev, cant_water_cut_elev, total_weights,
                             1000)  # length of sheet doesn't matter
        braced_water = water_pressures(layers, water_elev, water_cut_elev, total_weights,
                               1000)  # length of sheet doesn't matter

        cant_net = net_pressures(active, cant_passive, cant_water, cantilever_cut_elev, ers_type, beam_spacing, zero_length, beam_type,
                    soldier_beam_method)

        cant = cant_pressures(active_cant, passive_cant, cant_water, cantilever_cut_elev, ers_type, beam_spacing, zero_length, beam_type,
                      soldier_beam_method)
        braced_net = net_pressures(active, braced_passive, braced_water, cut_elev, ers_type, beam_spacing, zero_length, beam_type,
                            soldier_beam_method)
        if top_sheet[0] != layers[0][0]:
            cant_net[0].insert(0, 0)
            cant_net[1].insert(0, cant_net[1][0])
            cant_net[0].insert(0, 0)
            cant_net[1].insert(0, top_sheet[0])
            braced_net[0].insert(0, 0)
            braced_net[1].insert(0, braced_net[1][0])
            braced_net[0].insert(0, 0)
            braced_net[1].insert(0, top_sheet[0])
        cant_data = minimum_length_cantilever(cant_net, cant, cantilever_cut_elev)
        cant_moment = maximum_moment_cantilever(cant_net)
        braced_moment = [0]
        braced_data = minimum_length(braced_net, brace_elev)
        if braced_data[0] == ():
            print(str(iteration[0]) + " does not work because brace doesnt solve")
            iteration = "does not work"
            continue
        braced_moment = maximum_moment(braced_net, braced_data[2], brace_elev)
        cant_moment = maximum_moment_cantilever(cant_net)
        max_moment = max(cant_moment[0], braced_moment[0])
        iteration.append(max_moment)

        cant_multi = multiplier_cantilever_optimizer(cant_net, cant, cant_data, cantilever_cut_elev)
        if cant_multi == ([],[]):
            print(str(iteration[0]) + " does not work because not enough length to cantilever")
            iteration = "does not work"
            break
        braced_multi = multiplier_optimizer(braced_net, brace_elev, braced_data)
        if braced_multi == ([],[]):
            print(str(iteration[0]) + " does not work because not enough length for braced")
            iteration = "does not work"
            continue

        if iteration != "does not work":
            optimized_length = max(cant_multi[1], braced_multi[1], layers[0][0]-cut_elev+5)
            iteration.append(optimized_length)

            # need to compute deflection for both, combine, report the max
            cant_deflection = deflection_calc_cantilever(cant_net, cant_data, [0, 0, 0, 1])[0]
            braced_deflection = deflection_calc(braced_net, brace_elev, braced_data, [0, 0, 0, 1])[0]
            total_deflection = []
            for i in range(len(layers)):
                total_deflection.append([0, layers[i][0]])
            for i in range(len(total_deflection)):
                for j in range(len(cant_deflection)):
                    if total_deflection[i][1] == cant_deflection[j][1]:
                        total_deflection[i][0] += cant_deflection[j][0]
                        break
            for i in range(len(total_deflection)):
                for j in range(len(braced_deflection)):
                    if total_deflection[i][1] == braced_deflection[j][1]:
                        total_deflection[i][0] += braced_deflection[j][0]
                        break

            # for i in range(len(braced_deflection)):
            #     for j in range(len(total_deflection)):
            #         if braced_deflection[i][1] == total_deflection[j][1]:
            #             total_deflection[j][0] += braced_deflection[i][0]
            #             break
            max_def_list = sorted(total_deflection, key=lambda x: x[0], reverse=True)
            max_deflection = round(max_def_list[0][0], 3)
            max_deflection_elev = round(max_def_list[0][1], 2)
            iteration.append(max_deflection)
            iteration.append(max_deflection_elev)
            if ers_type == 0:
                old_deflection = []
                for i in range(len(def_sheet_database)):
                    deflection = max_deflection/def_sheet_database[i][3]
                    bending_stress = max_moment *0.012/def_sheet_database[i][2]
                    if old_deflection == [] and deflection < 2 and bending_stress < 32:
                        iteration.append(def_sheet_database[i])
                        iteration.append(deflection)
                        iteration.append(round(bending_stress, 2))
                        break
                    if old_deflection != [] and old_deflection>= 2 and deflection < 2 and bending_stress < 32:
                        iteration.append(def_sheet_database[i])
                        iteration.append(deflection)
                        iteration.append(round(bending_stress, 2))
                        break
                old_deflection = []
                for i in range(len(def_sheet_database)):
                    bending_stress = max_moment * 0.012 / def_sheet_database[i][2]
                    deflection = max_deflection / def_sheet_database[i][3]
                    if old_deflection == [] and deflection < 1 and bending_stress < 32:
                        iteration.append(def_sheet_database[i])
                        iteration.append(deflection)
                        iteration.append(round(bending_stress, 2))
                        break
                    if old_deflection != [] and old_deflection >= 1 and deflection < 1 and bending_stress < 32:
                        iteration.append(def_sheet_database[i])
                        iteration.append(deflection)
                        iteration.append(round(bending_stress, 2))
                        break
                old_deflection = []
                for i in range(len(def_sheet_database)):
                    bending_stress = max_moment * 0.012 / def_sheet_database[i][2]
                    deflection = max_deflection / def_sheet_database[i][3]
                    if old_deflection == [] and deflection < 0.25 and bending_stress < 32:
                        iteration.append(def_sheet_database[i])
                        iteration.append(deflection)
                        iteration.append(round(bending_stress, 2))
                        break
                    if old_deflection != [] and old_deflection >= 0.25 and deflection < 0.25 and bending_stress < 32:
                        iteration.append(def_sheet_database[i])
                        iteration.append(deflection)
                        iteration.append(round(bending_stress, 2))
                        break
            if ers_type == 1:
                old_deflection = []
                for i in range(len(def_beam_database)):
                    deflection = max_deflection/def_beam_database[i][3]
                    bending_stress = max_moment * 0.012 / def_beam_database[i][2]
                    if old_deflection == [] and deflection < 2 and bending_stress < 32:
                        iteration.append(def_beam_database[i])
                        iteration.append(deflection)
                        iteration.append(round(bending_stress, 2))
                        break
                    if old_deflection != [] and old_deflection>= 2 and deflection < 2 and bending_stress < 32:
                        iteration.append(def_beam_database[i])
                        iteration.append(deflection)
                        iteration.append(round(bending_stress, 2))
                        break
                old_deflection = []
                for i in range(len(def_sheet_database)):
                    deflection = max_deflection / def_beam_database[i][3]
                    bending_stress = max_moment * 0.012 / def_beam_database[i][2]
                    if old_deflection == [] and deflection < 1 and bending_stress < 32:
                        iteration.append(def_beam_database[i])
                        iteration.append(deflection)
                        iteration.append(round(bending_stress, 2))
                        break
                    if old_deflection != [] and old_deflection >= 1 and deflection < 1 and bending_stress < 32:
                        iteration.append(def_beam_database[i])
                        iteration.append(deflection)
                        iteration.append(round(bending_stress, 2))
                        break
                old_deflection = []
                for i in range(len(def_sheet_database)):
                    deflection = max_deflection / def_beam_database[i][3]
                    bending_stress = max_moment * 0.012 / def_beam_database[i][2]
                    if old_deflection == [] and deflection < 0.25 and bending_stress < 32:
                        iteration.append(def_beam_database[i])
                        iteration.append(deflection)
                        iteration.append(round(bending_stress, 2))
                        break
                    if old_deflection != [] and old_deflection >= 0.25 and deflection < 0.25 and bending_stress < 32:
                        iteration.append(def_beam_database[i])
                        iteration.append(deflection)
                        iteration.append(round(bending_stress, 2))
                        break

        end = timer()
        print("iteration complete", iteration, str(round(end-start,1))+" seconds")

    new_iterations = []
    for iteration in iterations:
        if len(iteration) == 14:
            new_iterations.append(iteration)
    iterations = new_iterations
    # for iteration in iterations:
    #     if len(iteration) != 11:
    #         iterations.remove(iteration)
    deflection_list = []
    for i in range(len(iterations)):
        deflection_list.append(iterations[i][3])
    min_deflection = min(deflection_list)
    for iteration in iterations:
        iteration.append(round(iteration[3]/min_deflection, 2))
    min_moment = sorted(iterations, key=lambda x: x[1])
    min_moment_output = "Minimum moment of " + str(round(min_moment[0][1],2)) + "#'/' occurs at installing the brace at elevation " + str(min_moment[0][0]) + "'"
    min_length = sorted(iterations, key=lambda x: x[2])
    min_length_output = "Minimum length of " + str(
        min_moment[0][2]) + "' occurs at installing the brace at elevation " + str(min_length[0][0]) + "'"
    min_deflection = sorted(iterations, key=lambda x: x[3])
    min_deflection_output = "Minimum deflection of " + str(
        min_moment[0][3]) + "/I occurs at installing the brace at elevation " + str(min_deflection[0][0]) + "'"

    output = []
    for iteration in iterations:
        output.append("")
        output_string = "Installing the brace at elevation " + str(iteration[0]) + "': "
        output.append(output_string)
        output_string = "Mmax =  " + str(int(round(iteration[1], 0))) + "#'/'"
        output.append(output_string)
        output_string = "Length =  " + str(iteration[2]) + "'"
        output.append(output_string)
        output_string = "Deflection/Min Deflection =  " + str(iteration[14])
        output.append(output_string)
        output_string = 'To achieve a deflection under 2", use ' + str(
            iteration[5][1]) + " or greater which results in deflection of " + str(
            round(iteration[6], 2)) + '" at elevation ' + str(iteration[4]) + "' and a bending stress of " + str(iteration[7]) + " ksi"
        output.append(output_string)
        output_string = 'To achieve a deflection under 1", use ' + str(
            iteration[8][1]) + " or greater which results in deflection of " + str(
            round(iteration[9], 2)) + '" at elevation ' + str(iteration[4]) + "' and a bending stress of " + str(iteration[10]) + " ksi"
        output.append(output_string)
        output_string = 'To achieve a deflection under 0.25", use ' + str(
            iteration[11][1]) + " or greater which results in deflection of " + str(
            round(iteration[12], 2)) + '" at elevation ' + str(iteration[4]) + "' and a bending stress of " + str(iteration[13]) + " ksi"
        output.append(output_string)
        output.append("")

    end = timer()
    print(iterations)
    print(request.build_absolute_uri)
    return render(request, 'optimizer_output.html', {"iterations": iterations,
                                                     "output": output,
                                                     "min_moment": min_moment_output,
                                                     "min_length": min_length_output,
                                                     "min_deflection": min_deflection_output


                                                     })


def loader(request):
    return render(request, 'loader.html')

