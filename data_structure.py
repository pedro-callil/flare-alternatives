#! /usr/bin/env python3

from field_gas_profiles import components
from flare_intensity import get_flare_intensity
from alternatives import alternatives
from alternatives import ccs_alternatives
from capex import get_capex_and_opex

from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("WxAgg")
import numpy as np

from random import random

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

        self.carboncosts = []
        self.watercosts = []
        self.electricity = []
        self.effluents = []

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

        self.emissions, self.available_gas = get_flare_intensity(self.volume,
                                                                self.components)
        return self.emissions, self.available_gas

    def net_present_values(self):


        self.npvlabels = []
        self.npvvalues = []

        for i, value in enumerate(self.alternatives):
            if value:
                self.npvlabels.append(alternatives[i])
                altcapex, altopex = get_capex_and_opex(self, alternatives[i])
                self.npvvalues.append(altcapex + altopex)

        self.npvvalues, self.npvlabels = (list(t) for t in
                                          zip(*sorted(zip(self.npvvalues,
                                                          self.npvlabels))))

    def cwee_cost(self):

        if (len(self.npvvalues) == 0 or
                len(self.npvvalues) != len([i for i in
                                            self.alternatives if i])):
            self.net_present_values()

        self.carboncosts = []
        self.watercosts = []
        self.electricity = []
        self.effluents = []

        for i, value in enumerate(alternatives):
            if value:
                self.carboncosts.append(random()*0.3)
                self.watercosts.append(random()*
                                       self.carboncosts[-1])
                self.electricity.append(random()*0.2*
                                        self.carboncosts[-1])
                self.effluents.append(random()*0.2*
                                      self.carboncosts[-1])

        self.carboncosts, self.npvvalues, self.watercosts, \
                self.electricity, self.effluents, self.npvlabels = \
                    (list(t) for t in
                     zip(*sorted(zip(self.carboncosts, self.npvvalues,
                                     self.watercosts, self.electricity,
                                     self.effluents, self.npvlabels),
                                 reverse=True)))

