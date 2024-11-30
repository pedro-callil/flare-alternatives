#! /usr/bin/env python3

from field_gas_profiles import components
from alternatives import alternatives
from alternatives import ccs_alternatives

from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("WxAgg")
import numpy as np

from random import random

class DataStructure:

    def __init__(self):
        self.components = [0.0]*len(components)
        self.volume = 0.0
        self.carbon_capture = 0
        self.carbon_tax = 0.0
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

        return 20.0

    def net_present_values(self):


        self.npvlabels = []
        self.npvvalues = []

        for i, value in enumerate(alternatives):
            if value:
                self.npvlabels.append(alternatives[i])
                self.npvvalues.append(random())

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
                self.watercosts.append(random()*0.3)
                self.electricity.append(random()*0.2)
                self.effluents.append(random()*0.2)

        self.carboncosts, self.npvvalues, self.watercosts, \
                self.electricity, self.effluents, self.npvlabels = \
                    (list(t) for t in
                     zip(*sorted(zip(self.carboncosts, self.npvvalues,
                                     self.watercosts, self.electricity,
                                     self.effluents, self.npvlabels))))

