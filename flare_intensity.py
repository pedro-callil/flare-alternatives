#! /usr/bin/env python3

from field_gas_profiles import components
from field_gas_profiles import carbons_in_components
from field_gas_profiles import flared_components

def get_flare_intensity(volume, fractions):

    volume_scf = volume
    flared_vol = 0
    moles_of_carbon = 1.48*1.1956*volume_scf*fractions[0]/sum(fractions)
    for i in range(1,len(components)):
        moles_of_carbon += carbons_in_components[i]*\
                            1.1956*\
                            volume_scf*\
                            fractions[i]/sum(fractions)
    flared_mass = moles_of_carbon*0.044009*0.001*0.365
    return flared_mass
