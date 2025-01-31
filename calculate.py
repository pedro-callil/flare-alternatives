#! /usr/bin/env python3

from calculate_classes import *

from field_gas_profiles import country_multiplier

def get_npv(data_structure, alternative):

    volume = data_structure.volume
    components = data_structure.components
    mltpl = country_multiplier[data_structure.location][0]
    irate = country_multiplier[data_structure.location][1]

    Gas = Stream(methane=volume*components[0]/100,
                 ethane=volume*components[1]/100,
                 propane=volume*components[2]/100,
                 butane=volume*components[3]/100,
                 pentane=volume*components[4]/100,
                 nitrogen=volume*components[5]/100,
                 carbon_dioxide=volume*components[6]/100,
                 hydrogen_sulphide=volume*components[7]/100)

    # acid gas removal

    chemical = ChemicalAGR()
    after_chemical_stream = chemical.apply(Gas)[0]

    membrane = MembraneAGR()
    after_membrane_stream = membrane.apply(Gas)[0]

    psa = PSAAGR()
    after_psa_stream = psa.apply(Gas)[0]

    after_noagr_stream = Gas.duplicate()

    ff_chemical = FullFractionationNGL()
    after_ff_chemical = ff_chemical.apply(after_chemical_stream)
    after_ff_chemical_stream = after_ff_chemical[0]
    after_ff_chemical_stream.value += after_ff_chemical[1].get_value(choice="ethane")
    after_ff_chemical_stream.value += after_ff_chemical[2].get_value(choice="lpg")
    after_ff_chemical_stream.value += after_ff_chemical[3].get_value(
                                        choice="condensates")

    ff_membrane = FullFractionationNGL()
    after_ff_membrane = ff_membrane.apply(after_membrane_stream)
    after_ff_membrane_stream = after_ff_membrane[0]
    after_ff_membrane_stream.value += after_ff_membrane[1].get_value(choice="ethane")
    after_ff_membrane_stream.value += after_ff_membrane[2].get_value(choice="lpg")
    after_ff_membrane_stream.value += after_ff_membrane[3].get_value(
                                        choice="condensates")

    ff_psa = FullFractionationNGL()
    after_ff_psa = ff_psa.apply(after_psa_stream)
    after_ff_psa_stream = after_ff_psa[0]
    after_ff_psa_stream.value += after_ff_psa[1].get_value(choice="ethane")
    after_ff_psa_stream.value += after_ff_psa[2].get_value(choice="lpg")
    after_ff_psa_stream.value += after_ff_psa[3].get_value(choice="condensates")

    ff_noagr = FullFractionationNGL()
    after_ff_noagr = ff_noagr.apply(after_noagr_stream)
    after_ff_noagr_stream = after_ff_noagr[0]
    after_ff_noagr_stream.value += after_ff_noagr[1].get_value(choice="ethane")
    after_ff_noagr_stream.value += after_ff_noagr[2].get_value(choice="lpg")
    after_ff_noagr_stream.value += after_ff_noagr[3].get_value(choice="condensates")

    ngl_chemical = RemovalNGL()
    after_ngl_chemical = ngl_chemical.apply(after_chemical_stream)
    after_ngl_chemical_stream = after_ngl_chemical[0]
    after_ngl_chemical_stream.value += after_ngl_chemical[1].get_value(
                                    choice="condensates")

    ngl_membrane = RemovalNGL()
    after_ngl_membrane = ngl_membrane.apply(after_membrane_stream)
    after_ngl_membrane_stream = after_ngl_membrane[0]
    after_ngl_membrane_stream.value += after_ngl_membrane[1].get_value(
                                    choice="condensates")

    ngl_psa = RemovalNGL()
    after_ngl_psa = ngl_psa.apply(after_psa_stream)
    after_ngl_psa_stream = after_ngl_psa[0]
    after_ngl_psa_stream.value += after_ngl_psa[1].get_value(choice="condensates")

    ngl_noagr = RemovalNGL()
    after_ngl_noagr = ngl_noagr.apply(after_noagr_stream)
    after_ngl_noagr_stream = after_ngl_noagr[0]
    after_ff_noagr_stream.value += after_ngl_noagr[1].get_value(choice="condensates")

    # Utilization technologies

    costs = dict()

    alternative_class = classes_dict[alternative]

    util_ff_chemical = alternative_class()
    costs["ff_chemical"] = (util_ff_chemical.apply(after_ff_chemical_stream),
                            [chemical, ff_chemical, util_ff_chemical])

    util_ff_membrane = alternative_class()
    costs["ff_membrane"] = (util_ff_membrane.apply(after_ff_membrane_stream),
                            [membrane, ff_membrane, util_ff_membrane])

    util_ff_psa = alternative_class()
    costs["ff_psa"] = (util_ff_psa.apply(after_ff_psa_stream),
                       [psa, ff_psa, util_ff_psa])

    util_ff_noagr = alternative_class()
    costs["ff_noagr"] = (util_ff_noagr.apply(after_ff_noagr_stream),
                         [ff_noagr, util_ff_noagr])

    util_ngl_chemical = alternative_class()
    costs["ngl_chemical"] = (util_ngl_chemical.apply(after_ngl_chemical_stream),
                             [chemical, ngl_chemical, util_ngl_chemical])

    util_ngl_membrane = alternative_class()
    costs["ngl_membrane"] = (util_ngl_membrane.apply(after_ngl_membrane_stream),
                             [membrane, ngl_membrane, util_ngl_membrane])

    util_ngl_psa = alternative_class()
    costs["ngl_psa"] = (util_ngl_psa.apply(after_ngl_psa_stream),
                        [psa, ngl_psa, util_ngl_psa])

    util_ngl_noagr = alternative_class()
    costs["ngl_noagr"] = (util_ngl_noagr.apply(after_ngl_noagr_stream),
                          [ngl_noagr, util_ngl_noagr])

    feasible = dict()
    for pretreatment in costs.keys():
        if (costs[pretreatment][0][0] != False):
            feasible[pretreatment] = costs[pretreatment][0][0].get_value()
            for elem in costs[pretreatment][1]:
                feasible[pretreatment] -= elem.get_cost([mltpl, irate],
                                carbon_tax=data_structure.carbon_tax)[0]
            feasible[pretreatment] *= sum([(1+irate)**(-i) for i in range(10)])

    split_costs = dict()
    for pretreatment in costs.keys():
        split_costs[pretreatment] = [0,0,0,0]
        if (costs[pretreatment][0][0] != False):
            for elem in costs[pretreatment][1]:
                for i in range(4):
                    split_costs[pretreatment][i] += list(elem.get_cost([mltpl, irate],
                            carbon_tax=data_structure.carbon_tax))[1:][i]
            for i in range(len(split_costs[pretreatment])):
                split_costs[pretreatment][i] *= sum([(1+irate)**(-i)
                                                     for i in range(10)])

    return feasible, split_costs

