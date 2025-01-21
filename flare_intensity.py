#! /usr/bin/env python3

from field_gas_profiles import components
from field_gas_profiles import carbons_in_components
from field_gas_profiles import flared_components

def get_flare_intensity(volume, fractions):

    volume_scf = 1e6*volume/0.3048**3
    moles_of_carbon = 0
    flared_vol = 0
    for i in range(len(components)):
        moles_of_carbon += carbons_in_components[i]*\
                            1.1956*\
                            volume_scf*\
                            fractions[i]/sum(fractions)
        flared_vol += flared_components[i]*\
                            volume*\
                            fractions[i]/sum(fractions)
    flared_mass = moles_of_carbon*0.044009*0.001
    return flared_mass, flared_vol
