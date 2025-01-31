#! /usr/bin/env python3

info = {
        "Chemical":
        {"CAPEX":               0.6,
         "OPEX":                0.9,
         "Energy":              0.0,
         "Emissions":           0.0,
         "Scale Multiplier":    [1.80,1.50,1.20,1.10,1.0]
        },
        "Membrane":
        {"CAPEX":               0.75,
         "OPEX":                0.7,
         "Energy":              0.0,
         "Emissions":           0.0,
         "Scale Multiplier":    [1.80,1.50,1.20,1.10,1.0]
        },
        "PSA":
        {"CAPEX":               0.75,
         "OPEX":                0.65,
         "Energy":              0.0,
         "Emissions":           0.0,
         "Scale Multiplier":    [1.80,1.50,1.20,1.10,1.0]
        },
        "Basic":
        {"CAPEX":               0.35,
         "OPEX":                0.2,
         "Energy":              1.15,
         "Emissions":           0,
         "Scale Multiplier":    [1.00,1.00,1.00,1.00,1.0]
        },
        "NGL removal":
        {"CAPEX":               0.9,
         "OPEX":                0.4,
         "Energy":              2.29,
         "Emissions":           0,
         "Scale Multiplier":    [1.80,1.50,1.20,1.10,1.0]
        },
        "Full Fractionation":
        {"CAPEX":               1.4,
         "OPEX":                0.8,
         "Energy":              3.68,
         "Emissions":           0,
         "Scale Multiplier":    [1.80,1.50,1.20,1.10,1.0]
        },
        "LNG":
        {"CAPEX":               3.0,
         "OPEX":                1.3,
         "Energy":              5.515,
         "Emissions":           0.314,
         "Product":             [21.37,20.16,19.62],
         "Scale Multiplier":    [2.00,1.75,1.40,1.25,1.0],
         "H2S lim":             5e-4,
         "CO2 lim":             3e-3,
         "hvy lim":             5e-2
         },
        "CNG":
        {"CAPEX":               1.0,
         "OPEX":                0.6,
         "Energy":              4.136,
         "Emissions":           0.235,
         "Product":             [21.26,22.25,19.70],
         "Scale Multiplier":    [2.25,1.90,1.60,1.25,1.0],
         "H2S lim":             5e-4,
         "CO2 lim":             1e-2,
         "hvy lim":             5e-2

         },
        "Gray Methanol":
        {"CAPEX":               8.3,
         "OPEX":                0.8,
         "Energy":              26.71,
         "Emissions":           2.524,
         "Product":             [27.31,35.56,38.29],
         "Scale Multiplier":    [1.80,1.50,1.20,1.10,1.0],
         "H2S lim":             1.5e-3,
         "CO2 lim":             4e-3,
         "hvy lim":             5e-2
         },
        "Turquoise Methanol":
        {"CAPEX":               8.5,
         "OPEX":                0.7,
         "Energy":              9.637,
         "Emissions":           0.837,
         "Product":             [70.09,38.32,38.32],
         "Carbon":              [13.31,13.31,13.31],
         "Scale Multiplier":    [2.25,1.90,1.60,1.25,1.0],
         "H2S lim":             1e-3,
         "CO2 lim":             2e-3,
         "hvy lim":             5e-2
         },
        "GTW (CCGT+CCS)":
        {"CAPEX":               4.0,
         "OPEX":                1.1,
         "Energy":              0.0,
         "Emissions":           0.0305,
         "Product":             [7496,6572.52,6364.89],
         "Scale Multiplier":    [1.90,1.60,1.30,1.20,1.0],
         "H2S lim":             4e-2,
         "CO2 lim":             4e-1,
         "hvy lim":             2.5e-1
         },
        "GTW (CCGT)":
        {"CAPEX":               4.0,
         "OPEX":                0.3,
         "Energy":              0.0,
         "Emissions":           2.113,
         "Product":             [7200,6421.87,6233.6],
         "Scale Multiplier":    [1.50,1.20,1.10,1.05,1.0],
         "H2S lim":             4e-2,
         "CO2 lim":             4e-1,
         "hvy lim":             2.5e-1
         },
        "GTW (NGT+CHP+CCS)":
        {"CAPEX":               3.5,
         "OPEX":                1.0,
         "Energy":              0.0,
         "Emissions":           0.0305,
         "Product":             [6289.0,5507.13,5341.45],
         "Steam":               [1159.03,1012.42,971.952],
         "Scale Multiplier":    [1.75,1.50,1.25,1.15,1.0],
         "H2S lim":             4e-2,
         "CO2 lim":             4e-1,
         "hvy lim":             2.5e-1
         },
        "GTW (NGT+CHP)":
        {"CAPEX":               3.5,
         "OPEX":                0.25,
         "Energy":              0.0,
         "Emissions":           2.113,
         "Product":             [6010.0,5363.0,5199.96],
         "Steam":               [1182.36,1023.72,983.424],
         "Scale Multiplier":    [1.50,1.20,1.10,1.05,1.0],
         "H2S lim":             4e-2,
         "CO2 lim":             4e-1,
         "hvy lim":             2.5e-1
         },
        "GTW (NGT)":
        {"CAPEX":               3.0,
         "OPEX":                0.05,
         "Energy":              0.0,
         "Emissions":           2.113,
         "Product":             [6251.0,5583.06,5482.0],
         "Scale Multiplier":    [1.50,1.20,1.10,1.05,1.0],
         "H2S lim":             4e-2,
         "CO2 lim":             4e-1,
         "hvy lim":             2.5e-1
         },
        "GTW (NGE)":
        {"CAPEX":               2.5,
         "OPEX":                0.05,
         "Energy":              0.0,
         "Emissions":           2.113,
         "Product":             [4896.05,4816.05,4716.05],
         "Scale Multiplier":    [1.40,1.15,1.10,1.05,1.0],
         "H2S lim":             1.5e-3,
         "CO2 lim":             2e-1,
         "hvy lim":             1.5e-1
         }
        }

prices = {
        "ethane":       230,
        "lpg":          230,
        "condensates":  285,
        "LNG":          380,
        "CNG":          530,
        "Methanol":     410,
        "GTW":          52.5*24,
        "Steam":        0.0157*2.8,
        "Carbon":       500,
        "Energy":       0.015
        }
