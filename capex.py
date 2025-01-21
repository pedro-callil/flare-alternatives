#! /usr/bin/env python3

from field_gas_profiles import country_multiplier
from alternatives import pp_capex, pp_size_scale, \
                        capex, size_scale, tolerances, ccs_capex

def get_capex_and_opex(data_structure, alternative):

    location_factor = country_multiplier[data_structure.location][0]
    discount_rate = country_multiplier[data_structure.location][1]

    h2s_conc = data_structure.components[-1]/sum(data_structure.components)
    co2_conc = data_structure.components[-2]/sum(data_structure.components)
    c3p_conc = 1-(data_structure.components[0]/sum(data_structure.components)+
                  data_structure.components[1]/sum(data_structure.components))

    h2s_total = data_structure.volume*h2s_conc
    co2_total = data_structure.volume*co2_conc
    c3p_total = data_structure.volume*c3p_conc

    h2s_max = tolerances[alternative][0]*data_structure.volume*(1-h2s_conc)/100.
    co2_max = tolerances[alternative][1]*data_structure.volume*(1-co2_conc)/100.
    c3p_max = tolerances[alternative][2]*data_structure.volume*(1-c3p_conc)/100.

    rel_conc = min(h2s_max/(h2s_total+1e-12),
                   co2_max/(co2_total+1e-12),
                   c3p_max/(c3p_total+1e-12))

    if (rel_conc > 0.1):
        pp = "PSA"
    elif (rel_conc > 0.01):
        pp = "Membrane"
    else:
        pp = "Chemical"

    flowrate = data_structure.available_gas/(365*0.3048**3)

    capex_pp = pp_capex[pp]*flowrate
    capex_treatment = capex[alternative]*flowrate
    capex_ccs = ccs_capex[data_structure.carbon_capture]*data_structure.emissions

    if flowrate < 1:
        scale_factor_pp = pp_size_scale[pp][0]
        scale_factor_treatment = size_scale[alternative][0]
    elif flowrate <3:
        scale_factor_pp = pp_size_scale[pp][1]
        scale_factor_treatment = size_scale[alternative][1]
    elif flowrate <5:
        scale_factor_pp = pp_size_scale[pp][2]
        scale_factor_treatment = size_scale[alternative][2]
    elif flowrate <10:
        scale_factor_pp = pp_size_scale[pp][3]
        scale_factor_treatment = size_scale[alternative][3]
    else:
        scale_factor_pp = pp_size_scale[pp][4]
        scale_factor_treatment = size_scale[alternative][4]

    calccapex = location_factor*(
                scale_factor_treatment*capex_treatment +
                scale_factor_pp*capex_pp +
                capex_ccs
            )

    calcopex = 0

    return calccapex, calcopex
