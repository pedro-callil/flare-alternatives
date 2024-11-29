#! /usr/bin/env python3

from field_gas_profiles import components
from alternatives import alternatives
from alternatives import ccs_alternatives

from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("WxAgg")
import numpy as np

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

    def generate_pie_chart(self):

        fig, ax = plt.subplots(figsize=(5,3), subplot_kw=dict(aspect="equal"))
        wedges, texts = ax.pie(self.components,
                               wedgeprops=dict(width=0.5), startangle=199)
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")

        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = f"angle,angleA=0,angleB={ang}"
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(components[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                        horizontalalignment=horizontalalignment, **kw)

        fig.savefig("/tmp/piechart.png", transparent=False)

