#! /usr/bin/env python3

alternatives = ["LNG",
                "CNG",
                "Gray Methanol",
                "Turquoise Methanol",
                "GTW (CCGT)",
                "GTW (CCGT+CCS)",
                "GTW (NGT)",
                "GTW (NGT+CHP)",
                "GTW (NGT+CHP+CCS)",
                "GTW (NGE)"]

ccs_alternatives = ["CO₂ Adsorption",
                    "No capture"]

pp_alternatives = ["Chemical", "Membrane", "PSA"]

#                                    <1    <3    <5    <10   <15
size_scale = {"LNG":                [2.00, 1.75, 1.40, 1.25, 1.00],
              "CNG":                [2.25, 1.90, 1.60, 1.25, 1.00],
              "GTW (CCGT)":         [1.50, 1.20, 1.10, 1.05, 1.00],
              "GTW (CHP)":          [1.50, 1.20, 1.10, 1.05, 1.00],
              "GTW (NGT)":          [1.50, 1.20, 1.10, 1.05, 1.00],
              "GTW (GEs)":          [1.40, 1.15, 1.10, 1.05, 1.00],
              "Green Methanol":     [1.80, 1.50, 1.20, 1.10, 1.00],
              "Turquoise Methanol": [2.25, 1.90, 1.60, 1.25, 1.00],
              "NGL":                [1.80, 1.50, 1.20, 1.10, 1.00],
              "FNGLs":              [1.80, 1.50, 1.20, 1.10, 1.00]}

#                                    H2S   CO2   C3+
tolerances = {"LNG":                [0.05, 0.30, 5.00],
              "CNG":                [0.05, 1.00, 5.00],
              "GTW (CCGT)":         [4.00, 40.0, 25.0],
              "GTW (CHP)":          [4.05, 40.0, 25.0],
              "GTW (NGT)":          [4.05, 40.0, 25.0],
              "GTW (GEs)":          [0.15, 20.0, 15.0],
              "Green Methanol":     [0.15, 0.40, 5.00],
              "Turquoise Methanol": [0.10, 0.20, 5.00],
              "NGL":                [0.20, 0.40, 100.],
              "FNGLs":              [0.20, 0.40, 100.]}

capex = {"LNG":                 3.0,
         "CNG":                 1.5,
         "GTW (CCGT)":          5.0,
         "GTW (CHP)":           4.8,
         "GTW (NGT)":           4.5,
         "GTW (GEs)":           2.5,
         "Green Methanol":      8.0,
         "Turquoise Methanol":  9.0,
         "NGL":                 0.9,
         "FNGLs":               1.4}

pp_capex = {"Chemical": 0.0,
            "Membrane": 0.0,
            "PSA": 0.0}

ccs_capex = {0: 0.0,
             1: 0.0,
             2: 0.0}

pp_opex = {"Chemical": 0.909,
           "Membrane": 0.520,
           "PSA":      0.716}

pp_size_scale = {"Chemical": [1.80, 1.50, 1.20, 1.10, 1.00],
                 "Membrane": [1.50, 1.20, 1.10, 1.05, 1.00],
                 "PSA":      [1.50, 1.20, 1.10, 1.05, 1.00]}

