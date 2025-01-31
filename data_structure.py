#! /usr/bin/env python3

from field_gas_profiles import components
from flare_intensity import get_flare_intensity
from alternatives import alternatives
from alternatives import ccs_alternatives
from calculate import get_npv

from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("WxAgg")
import numpy as np

from random import random

name_of_parts = {"ff": "fractionation",
                 "ngl": "NGL removal",
                 "chemical": "chemical AGR",
                 "membrane": "membrane AGR",
                 "psa": "PSA AGR",
                 "noagr": "no AGR"}

def beautify(string):
    parts = string.split("_")
    return name_of_parts[parts[0]] + "\n" + name_of_parts[parts[1]]

class DataStructure:

    def __init__(self):
        self.components = [0.0]*len(components)
        self.volume = 0.0
        self.available_gas = 0.0
        self.emissions = 0.0
        self.carbon_capture = 0
        self.carbon_tax = 0.0
        self.location = ""
        self.extra_penalty_water = False
        self.extra_penalty_electricity = False
        self.extra_penalty_carbon = False
        self.extra_penalty_size = False
        self.alternatives = [False]*len(alternatives)

        self.npvlabels = []
        self.npvvalues = []

        self.capex = []
        self.opex = []
        self.carbon = []
        self.energy = []

    def __repr__(self):
        string = ""
        for i, elem in enumerate(self.components):
            string += components[i] + ": " + str(elem) + "\n"
        string += 'Volume: ' + str(self.volume)
        string += '\nCCS: ' + str(ccs_alternatives[self.carbon_capture])
        string += '\nCarbon Tax: ' + str(self.carbon_tax)
        string += '\nEx. Pnlty. Water: ' + str(self.extra_penalty_water)
        string += '\nEx. Pnlty. Electricity: ' + str(self.extra_penalty_electricity)
        string += '\nEx. Pnlty. Carbon: ' + str(self.extra_penalty_carbon)
        string += '\nEx. Pnlty. Size: ' + str(self.extra_penalty_size)
        string += '\nAlternatives: '

        for i, elem in enumerate(self.alternatives):
            if elem:
                string += alternatives[i] + ' '

        string += '\n'

        return string

    def flare_intensity(self):

        self.emissions = get_flare_intensity(self.volume, self.components)
        return self.emissions

    def net_present_values(self):


        self.npvlabels = []
        self.npvvalues = []

        for i, value in enumerate(self.alternatives):
            if value:
                npv_dict, costs_dict = get_npv(self, alternatives[i])
                if (not npv_dict == {}):
                    self.npvlabels.append(alternatives[i])
                    maximum = -1e12
                    maxkey = ""
                    for key in npv_dict.keys():
                        if (npv_dict[key] > maximum):
                            maximum = npv_dict[key]/1e6
                            maxkey = key
                    self.npvvalues.append(maximum)
                    self.npvlabels[-1] += ("\n" + beautify(maxkey))
                    self.capex.append(costs_dict[key][0]/1e6)
                    self.opex.append(costs_dict[key][1]/1e6)
                    self.carbon.append(costs_dict[key][2]/1e6)
                    self.energy.append(costs_dict[key][3]/1e6)

        self.npvvalues, self.capex, self.opex, \
            self.carbon, self.energy, self.npvlabels = (list(t) for t in
                                          zip(*sorted(zip(self.npvvalues,
                                                          self.capex,
                                                          self.opex,
                                                          self.carbon,
                                                          self.energy,
                                                          self.npvlabels))))

    def cwee_cost(self):

        if (len(self.npvvalues) == 0 or
                len(self.npvvalues) != len([i for i in
                                            self.alternatives if i])):
            self.net_present_values()

        #self.capex, self.opex, self.carbon, \
        #        self.energy, self.npvlabels = \
        #            (list(t) for t in
        #             zip(*sorted(zip(self.capex, self.opex,
        #                             self.carbon, self.energy,
        #                             self.npvlabels),
        #                         reverse=True)))

