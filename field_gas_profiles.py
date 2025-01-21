#! /usr/bin/env python3

components = ["Methane", "Ethane", "Propane", "Butane", "Pentane (C₅₊)",
              "N₂","CO₂","H₂S"]

carbons_in_components = [1, 2, 3, 4, 5, 0, 1, 0]

flared_components = [1, 1, 1, 1, 1, 0, 0, 0]

region_choices = ["Africa",
                  "America",
                  "Asia",
                  "Europe",
                  "Oceania"]

country_choices = {"Africa":  ["Algeria", "Nigeria"],
                   "America": ["Venezuela"],
                   "Asia":    ["Iraq", "Kuwait", "Saudi Arabia"],
                   "Europe":  ["France", "Netherlands",
                               "Norway", "Russia", "United Kingdom"],
                   "Oceania": ["Australia", "New Zealand"]}

field_choices = {"France":                   ["Lacq"],
                 "Netherlands":              ["Groningen"],
                 "Norway":                   ["Frigg"],
                 "Russia":                   ["Urengoy"],
                 "United Kingdom":           ["Weald"],
                 "Saudi Arabia":             ["Uthmaniyah"],
                 "Nigeria":                  ["FS-2", "Soku"],
                 "Algeria":                  ["Hassi R’Mel"],
                 "Venezuela":                ["Maracaibo"],
                 "Kuwait":                   ["Burgan"],
                 "Iraq":                     ["Kirkuk"],
                 "New Zealand":              ["Kapumi"],
                 "Australia":                ["Cooper", "Carnarvon"]
                 }

country_multiplier= {"France":                   [1.50, 0.07],
                     "Netherlands":              [1.50, 0.07],
                     "Norway":                   [1.50, 0.07],
                     "Russia":                   [1.50, 0.07],
                     "United Kingdom":           [1.50, 0.07],
                     "Saudi Arabia":             [1.63, 0.12],
                     "Nigeria":                  [1.75, 0.10],
                     "Algeria":                  [1.75, 0.10],
                     "Venezuela":                [1.63, 0.10],
                     "Kuwait":                   [1.63, 0.12],
                     "Iraq":                     [1.63, 0.12],
                     "New Zealand":              [1.50, 0.07],
                     "Australia":                [1.50, 0.07]
                 }

# Weald (Godley Bridge - Port): Paleozoic gas potential
#        in the Weald Basin of southern England, Pullan & Butler
# Cooper & Carnarvon: Impact of Australian natural gas
#        and coal bed methane composition on PEM
#        fuel cell performance, Dicks et al
# Remaining: Modelling emissions from natural gas flaring
#        Umukoro & Ismail

field_chats = {"Lacq":
                  [ 69.0,  3.0,  0.9,   0.5,   0.5,  1.5,  9.3, 15.3],
               "Groningen":
                  [ 81.3,  2.9,  0.4,   0.1,   0.1, 14.3,  0.9,  0.0],
               "Frigg":
                  [ 95.7,  3.6,  0.0,   0.0,   0.0,  0.4,  0.3,  0.0],
               "Urengoy":
                  [ 85.3,  5.8,  5.3,   2.1,   0.2,  0.9,  0.4,  0.0],
               "Weald":
                  [ 85.6,  5.1,  2.8,   1.2,   0.4,  4.2,  0.2,  0.0],
               "Uthmaniyah":
                  [ 55.5, 18.0,  9.8,   4.5,   1.6,  0.2,  8.9,  1.5],
               "FS-2":
                  [90.12, 6.94, 2.09, 0.771, 0.079,  0.0,  0.0,  0.0],
               "Soku":
                  [92.51, 2.78, 1.66,  0.78,  0.30, 0.11, 0.22,  0.0],
               "Hassi R’Mel":
                  [ 83.7,  6.8,  2.1,   0.8,   0.4,  5.8,  0.2,	 0.0],
               "Maracaibo":
                  [ 82.0, 10.0,  3.7,   1.9,   0.7,  1.5,  0.2,  0.0],
               "Burgan":
                  [ 74.3, 14.0,  5.8,   2.0,   0.9,  2.9,  0.0,  0.1],
               "Kirkuk":
                  [ 56.9, 21.2,  6.0,   3.7,   1.6,  0.0,  7.1,  3.5],
               "Kapumi":
                  [ 45.6,  5.8,  2.9,   1.1,   0.8,  0.0, 43.8,  0.0],
               "Cooper":
                  [90.76, 3.77, 0.40,  0.11,  0.08, 1.59, 3.29,  0.0],
               "Carnarvon":
                  [82.48, 8.28, 3.07,  1.66,  0.97, 0.77, 2.78,  0.0]
               }

