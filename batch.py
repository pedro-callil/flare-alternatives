#! /usr/bin/env python3

from data_structure import DataStructure
from alternatives import alternatives

import pandas as pd

#                        C1     C2     C3     C4     C5     N      CO2    H2S
locations = {
    "United States":    [58.70, 11.90, 10.30,  8.80,  7.80,  0.00,  0.90,  0.50],
    "Nigeria":          [90.12,  6.94,  2.09,  0.77,  0.08,  0.00,  0.00,  0.00],
    "Saudi Arabia":     [55.50, 18.00,  9.80,  4.50,  1.60,  0.20,  8.90,  1.50],
    "Australia":        [87.50,  3.87,  1.34,  0.58,  2.24,  2.79,  1.68,  0.00],
    "Brazil":           [81.57,  9.17,  5.13,  2.39,  0.83,  0.52,  0.39,  0.00],
    "United Kingdom":   [69.40, 14.50,  9.00,  0.90,  0.00,  2.20,  4.00,  0.00]}

location = "United Kingdom"
scale = 10.80

table = {
        "Ctax": [],
        "LNG": [],
        "GTW (NGE)": [],
        "GTW (CCGT+CCS)": [],
        "GTW (NGT+CHP+CCS)": [],
        "GTW (NGT)": [],
        "GTW (CCGT)": [],
        "GTW (NGT+CHP)": [],
        "CNG": [],
        "Gray Methanol": [],
        "Turquoise Methanol": []
}

for i in range(500):
    carbon_tax = i/25

    data = DataStructure()
    data.components = locations[location]
    data.carbon_tax = carbon_tax
    data.alternatives = [True]*len(alternatives)
    data.location = location
    data.volume = scale*1e6

    data.net_present_values()

    table["Ctax"].append(carbon_tax)

    for i, elem in enumerate(data.npvlabels):
        table[elem.split('\n')[0]].append(data.npvvalues[i])

df = pd.DataFrame(table)
df.to_csv('file.csv')

