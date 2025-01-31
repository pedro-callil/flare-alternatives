#! /usr/bin/env python3

from aspen_values import info, prices

from_mmscfd = 1e-6*24*365
from_mmscfd_to_mtd = 1e-6*365
from_mmscfd_to_mwh = 1e-9*365*24
from_mmscfd_to_kghr = 1e-6*365*24
to_annual = 0.365

class Stream:
    """!
        Implements stream characteristics such as composition and volume
    """
    def __init__(self, methane=0, ethane=0, propane=0, butane=0, pentane=0,
                 nitrogen=0, carbon_dioxide=0, hydrogen_sulphide=0):
        self.methane = methane
        self.ethane = ethane
        self.propane = propane
        self.butane = butane
        self.pentane = pentane
        self.nitrogen = nitrogen
        self.carbon_dioxide = carbon_dioxide
        self.hydrogen_sulphide = hydrogen_sulphide

        # Products
        self.steam = 0
        self.value = 0
        self.lng = 0
        self.cng = 0
        self.methanol = 0
        self.electricity = 0
        self.carbon = 0

        # pretreatment
        self.ptreat = 0

    def duplicate(self):
        other = Stream(methane = self.methane,
                       ethane = self.ethane,
                       propane = self.propane,
                       butane = self.butane,
                       pentane = self.pentane,
                       nitrogen = self.nitrogen,
                       carbon_dioxide = self.carbon_dioxide,
                       hydrogen_sulphide = self.hydrogen_sulphide)

        other.value = self.value

        return other

    def get_flowrate(self):
        return (self.methane +
                self.ethane +
                self.propane +
                self.butane +
                self.pentane +
                self.nitrogen +
                self.carbon_dioxide +
                self.hydrogen_sulphide)

    def get_value(self, choice=""):
        if self.steam >= 1e-12:
            self.value += prices["Steam"]*self.steam
        if self.carbon >= 1e-12:
            self.value += prices["Carbon"]*self.carbon
        if self.electricity >= 1e-12:
            return self.value + prices["GTW"]*self.electricity
        elif self.lng >= 1e-12:
            return self.value + prices["LNG"]*self.lng
        elif self.cng >= 1e-12:
            return self.value + prices["CNG"]*self.cng
        elif self.methanol >= 1e-12:
            return self.value + prices["Methanol"]*self.methanol
        elif choice == "ethane":
            if (self.hydrogen_sulphide/(1e-12+self.get_flowrate()) < 2e-3 and
                self.carbon_dioxide/(1e-12+self.get_flowrate()) < 4e-3):
                return prices["ethane"]*self.ethane*1.1953*0.0307/1000
            else:
                return 0
        elif choice == "lpg":
            if (self.hydrogen_sulphide/(1e-12+self.get_flowrate()) < 2e-3 and
                self.carbon_dioxide/(1e-12+self.get_flowrate()) < 4e-3):
                return prices["lpg"]*(self.propane*0.0441+
                                      self.butane*0.0581)*1.1953/1000
            else:
                return 0
        elif choice == "condensates":
            if (self.hydrogen_sulphide/(1e-12+self.get_flowrate()) < 2e-3 and
                self.carbon_dioxide/(1e-12+self.get_flowrate()) < 4e-3):
                return prices["condensates"]*self.pentane*0.0721*1.1953/1000
            else:
                return 0


class BasicProcess:
    """!
        Base class implementing a purification/utilization process
    """

    def __init__(self):
        self.name = ""
        self.scale = 0
        self.capex = 0
        self.opex = 0
        self.energy = 0
        self.emissions = 0

    def apply(self, input_stream):
        self.name = "Basic"
        self.scale = input_stream.get_flowrate()
        # Scale is flowrate in SCFD
        self.capex = info[self.name]["CAPEX"]*self.scale
        # CAPEX is informed in USD/SCFD
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        # OPEX is informed in USD/MSCF, hence we multiply by 365
        # and divide by a thousand (number of MSCF in a year)
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        # Energy is informed in MMBTU/hr per MMSCFD. To convert it to
        # MMBTU/yr, one must divide the flowrate by a million (obtaining
        # it in MMSCFD), and then multiply it by 365*24 (obtaining annual
        # consumption in MMBTU)
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd
        # Emissions are informed in tCO2/hr per MMSCFD. To convert it to
        # MMBTU/yr, one must divide the flowrate by a million (obtaining
        # it in MMSCFD), and then multiply it by 365*24 (obtaining annual
        # emissions in tonCO2)

        output_stream = input_stream.duplicate()
        return [output_stream]

    def get_cost(self, location_pair, carbon_tax=0):
        if self.scale < 1e6:
            scale_multiplier = info[self.name]["Scale Multiplier"][0]
        elif self.scale < 3e6:
            scale_multiplier = info[self.name]["Scale Multiplier"][1]
        elif self.scale < 5e6:
            scale_multiplier = info[self.name]["Scale Multiplier"][2]
        elif self.scale < 10e6:
            scale_multiplier = info[self.name]["Scale Multiplier"][3]
        else:
            scale_multiplier = info[self.name]["Scale Multiplier"][4]

        scale_multiplier *= location_pair[0]
        discount_rate = location_pair[1]
        scale_multiplier *= (discount_rate*(1+discount_rate)**10)
        scale_multiplier /= ((1+discount_rate)**10-1)

        capex = scale_multiplier*self.capex
        opex = self.opex
        carbon = carbon_tax*self.emissions
        energy = self.energy*prices["Energy"]
        tacost = capex + opex + carbon + energy

        return tacost, capex, opex, carbon, energy

class ChemicalAGR(BasicProcess):
    """!
        Process of acid gas removal with high efficiency
    """

    def apply(self, input_stream):
        self.name = "Chemical"
        self.scale = input_stream.get_flowrate()
        self.capex = info[self.name]["CAPEX"]*self.scale
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd
        output_stream = input_stream.duplicate()
        output_stream.hydrogen_sulphide *= 0.01
        output_stream.carbon_dioxide *= 0.01
        return [output_stream]

class MembraneAGR(BasicProcess):
    """!
        Process of acid gas removal with average efficiency
    """

    def apply(self, input_stream):
        self.name = "Membrane"
        self.scale = input_stream.get_flowrate()
        self.capex = info[self.name]["CAPEX"]*self.scale
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd
        output_stream = input_stream.duplicate()
        output_stream.hydrogen_sulphide *= 0.05
        output_stream.carbon_dioxide *= 0.05
        return [output_stream]

class PSAAGR(BasicProcess):
    """!
        Process of acid gas removal with low efficiency
    """

    def apply(self, input_stream):
        self.name = "PSA"
        self.scale = input_stream.get_flowrate()
        self.capex = info[self.name]["CAPEX"]*self.scale
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd
        output_stream = input_stream.duplicate()
        output_stream.hydrogen_sulphide *= 0.1
        output_stream.carbon_dioxide *= 0.1
        return [output_stream]

class FullFractionationNGL(BasicProcess):
    """!
        Condensates and LPG removal process with high purity outputs
    """

    def apply(self, input_stream):

        self.ptreat = 2

        dry_gas = Stream()
        dry_gas.methane = 0.99*input_stream.methane
        dry_gas.ethane = 0.32*input_stream.ethane
        dry_gas.propane = 0.05*input_stream.propane
        dry_gas.carbon_dioxide = input_stream.carbon_dioxide
        dry_gas.hydrogen_sulphide = input_stream.hydrogen_sulphide

        ethane = Stream()
        ethane.methane = 0.01*input_stream.methane
        ethane.ethane = 0.65*input_stream.ethane
        ethane.propane = 0.08*input_stream.propane

        lpg = Stream()
        lpg.ethane = 0.03*input_stream.propane
        lpg.propane = 0.85*input_stream.propane
        lpg.butane = 0.95*input_stream.butane
        lpg.pentane = 0.03*input_stream.pentane

        condensates = Stream()
        condensates.propane = 0.02*input_stream.propane
        condensates.butane = 0.05*input_stream.butane
        condensates.pentane = 0.97*input_stream.pentane

        self.name = "Full Fractionation"
        self.scale = input_stream.get_flowrate()
        self.capex = info[self.name]["CAPEX"]*self.scale
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd

        return [dry_gas, ethane, lpg, condensates]

class RemovalNGL(BasicProcess):
    """!
        Only methane+ethane and NGLs.
    """

    def apply(self, input_stream):

        self.ptreat = 1

        dry_gas = Stream()
        dry_gas.methane = input_stream.methane
        dry_gas.ethane = input_stream.ethane
        dry_gas.carbon_dioxide = input_stream.carbon_dioxide
        dry_gas.hydrogen_sulphide = input_stream.hydrogen_sulphide
        dry_gas.propane = 0.1*input_stream.propane
        dry_gas.butane = 0.1*input_stream.butane

        condensates = Stream()
        condensates.propane = 0.9*input_stream.propane
        condensates.butane = 0.9*input_stream.butane
        condensates.pentane = input_stream.pentane

        self.name = "NGL removal"
        self.scale = input_stream.get_flowrate()
        self.capex = info[self.name]["CAPEX"]*self.scale
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd

        return [dry_gas, condensates]

class LNG(BasicProcess):
    """!
        Liquefied Natural Gas.
    """

    def apply(self, input_stream):

        self.name = "LNG"

        flowrate = input_stream.get_flowrate()
        heavies = input_stream.propane + \
                  input_stream.butane + \
                  input_stream.pentane
        if (input_stream.hydrogen_sulphide/flowrate >
                    info[self.name]["H2S lim"] or
            input_stream.carbon_dioxide/flowrate >
                    info[self.name]["CO2 lim"] or
            heavies/flowrate >
                    info[self.name]["hvy lim"]):
            return [False]

        self.scale = input_stream.get_flowrate()
        self.capex = info[self.name]["CAPEX"]*self.scale
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd

        lng = Stream()
        lng.value = input_stream.value
        lng.lng = (info[self.name]["Product"][input_stream.ptreat]*
                   self.scale*from_mmscfd_to_mtd)

        return [lng]

class CNG(BasicProcess):
    """!
        Compressed Natural Gas.
    """

    def apply(self, input_stream):

        self.name = "CNG"

        flowrate = input_stream.get_flowrate()
        heavies = input_stream.propane + \
                  input_stream.butane + \
                  input_stream.pentane
        if (input_stream.hydrogen_sulphide/flowrate >
                    info[self.name]["H2S lim"] or
            input_stream.carbon_dioxide/flowrate >
                    info[self.name]["CO2 lim"] or
            heavies/flowrate >
                    info[self.name]["hvy lim"]):
            return [False]

        self.scale = input_stream.get_flowrate()
        self.capex = info[self.name]["CAPEX"]*self.scale
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd

        cng = Stream()
        cng.value = input_stream.value
        cng.cng = (info[self.name]["Product"][input_stream.ptreat]*
                   self.scale*from_mmscfd_to_mtd)

        return [cng]

class GrayMethanol(BasicProcess):
    """!
        Gray Methanol production.
    """

    def apply(self, input_stream):

        self.name = "Gray Methanol"

        flowrate = input_stream.get_flowrate()
        heavies = input_stream.propane + \
                  input_stream.butane + \
                  input_stream.pentane
        if (input_stream.hydrogen_sulphide/flowrate >
                    info[self.name]["H2S lim"] or
            input_stream.carbon_dioxide/flowrate >
                    info[self.name]["CO2 lim"] or
            heavies/flowrate >
                    info[self.name]["hvy lim"]):
            return [False]

        self.scale = input_stream.get_flowrate()
        self.capex = info[self.name]["CAPEX"]*self.scale
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd

        gmeth = Stream()
        gmeth.value = input_stream.value
        gmeth.methanol = (info[self.name]["Product"][input_stream.ptreat]*
                          self.scale*from_mmscfd_to_mtd)

        return [gmeth]

class TurquoiseMethanol(BasicProcess):
    """!
        Turquoise Methanol production.
    """

    def apply(self, input_stream):

        self.name = "Turquoise Methanol"

        flowrate = input_stream.get_flowrate()
        heavies = input_stream.propane + \
                  input_stream.butane + \
                  input_stream.pentane
        if (input_stream.hydrogen_sulphide/flowrate >
                    info[self.name]["H2S lim"] or
            input_stream.carbon_dioxide/flowrate >
                    info[self.name]["CO2 lim"] or
            heavies/flowrate >
                    info[self.name]["hvy lim"]):
            return [False]

        self.scale = input_stream.get_flowrate()
        self.capex = info[self.name]["CAPEX"]*self.scale
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd

        tmeth = Stream()
        tmeth.value = input_stream.value
        tmeth.methanol = (info[self.name]["Product"][input_stream.ptreat]*
                          self.scale*from_mmscfd_to_mtd)
        tmeth.carbon = (info[self.name]["Carbon"][input_stream.ptreat]*
                        self.scale*from_mmscfd_to_mtd)

        return [tmeth]

class GTW_CCGT_CCS(BasicProcess):
    """!
        Electricity production through a Combined Cycle Gas Turbine using Carbon
        Capture/Storage.
    """

    def apply(self, input_stream):

        self.name = "GTW (CCGT+CCS)"

        flowrate = input_stream.get_flowrate()
        heavies = input_stream.propane + \
                  input_stream.butane + \
                  input_stream.pentane
        if (input_stream.hydrogen_sulphide/flowrate >
                    info[self.name]["H2S lim"] or
            input_stream.carbon_dioxide/flowrate >
                    info[self.name]["CO2 lim"] or
            heavies/flowrate >
                    info[self.name]["hvy lim"]):
            return [False]

        self.scale = input_stream.get_flowrate()
        self.capex = info[self.name]["CAPEX"]*self.scale
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd

        gtw = Stream()
        gtw.value = input_stream.value
        gtw.electricity = (info[self.name]["Product"][input_stream.ptreat]*
                           self.scale*from_mmscfd_to_mwh)

        return [gtw]

class GTW_CCGT(BasicProcess):
    """!
        Electricity production through a Combined Cycle Gas Turbine using no
        Carbon Capture/Storage.
    """

    def apply(self, input_stream):

        self.name = "GTW (CCGT)"

        flowrate = input_stream.get_flowrate()
        heavies = input_stream.propane + \
                  input_stream.butane + \
                  input_stream.pentane
        if (input_stream.hydrogen_sulphide/flowrate >
                    info[self.name]["H2S lim"] or
            input_stream.carbon_dioxide/flowrate >
                    info[self.name]["CO2 lim"] or
            heavies/flowrate >
                    info[self.name]["hvy lim"]):
            return [False]

        self.scale = input_stream.get_flowrate()
        self.capex = info[self.name]["CAPEX"]*self.scale
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd

        gtw = Stream()
        gtw.value = input_stream.value
        gtw.electricity = (info[self.name]["Product"][input_stream.ptreat]*
                           self.scale*from_mmscfd_to_mwh)

        return [gtw]

class GTW_NGT_CHP_CCS(BasicProcess):
    """!
        Electricity production with a Natural Gas Turbine using Carbon
        Capture/Storage and Combined Heat and Power.
    """

    def apply(self, input_stream):

        self.name = "GTW (NGT+CHP+CCS)"

        flowrate = input_stream.get_flowrate()
        heavies = input_stream.propane + \
                  input_stream.butane + \
                  input_stream.pentane
        if (input_stream.hydrogen_sulphide/flowrate >
                    info[self.name]["H2S lim"] or
            input_stream.carbon_dioxide/flowrate >
                    info[self.name]["CO2 lim"] or
            heavies/flowrate >
                    info[self.name]["hvy lim"]):
            return [False]

        self.scale = input_stream.get_flowrate()
        self.capex = info[self.name]["CAPEX"]*self.scale
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd

        gtw = Stream()
        gtw.value = input_stream.value
        gtw.electricity = (info[self.name]["Product"][input_stream.ptreat]*
                           self.scale*from_mmscfd_to_mwh)
        gtw.steam = (info[self.name]["Steam"][input_stream.ptreat]*
                     self.scale*from_mmscfd_to_kghr)

        return [gtw]

class GTW_NGT_CHP(BasicProcess):
    """!
        Electricity production with a Natural Gas Turbine using no Carbon
        Capture/Storage but with Combined Heat and Power.
    """

    def apply(self, input_stream):

        self.name = "GTW (NGT+CHP)"

        flowrate = input_stream.get_flowrate()
        heavies = input_stream.propane + \
                  input_stream.butane + \
                  input_stream.pentane
        if (input_stream.hydrogen_sulphide/flowrate >
                    info[self.name]["H2S lim"] or
            input_stream.carbon_dioxide/flowrate >
                    info[self.name]["CO2 lim"] or
            heavies/flowrate >
                    info[self.name]["hvy lim"]):
            return [False]

        self.scale = input_stream.get_flowrate()
        self.capex = info[self.name]["CAPEX"]*self.scale
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd

        gtw = Stream()
        gtw.value = input_stream.value
        gtw.electricity = (info[self.name]["Product"][input_stream.ptreat]*
                           self.scale*from_mmscfd_to_mwh)
        gtw.steam = (info[self.name]["Steam"][input_stream.ptreat]*
                     self.scale*from_mmscfd_to_kghr)

        return [gtw]

class GTW_NGT(BasicProcess):
    """!
        Electricity production with a Natural Gas Turbine using no Carbon
        Capture/Storage or Combined Heat and Power.
    """

    def apply(self, input_stream):

        self.name = "GTW (NGT)"

        flowrate = input_stream.get_flowrate()
        heavies = input_stream.propane + \
                  input_stream.butane + \
                  input_stream.pentane
        if (input_stream.hydrogen_sulphide/flowrate >
                    info[self.name]["H2S lim"] or
            input_stream.carbon_dioxide/flowrate >
                    info[self.name]["CO2 lim"] or
            heavies/flowrate >
                    info[self.name]["hvy lim"]):
            return [False]

        self.scale = input_stream.get_flowrate()
        self.capex = info[self.name]["CAPEX"]*self.scale
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd

        gtw = Stream()
        gtw.value = input_stream.value
        gtw.electricity = (info[self.name]["Product"][input_stream.ptreat]*
                           self.scale*from_mmscfd_to_mwh)

        return [gtw]

class GTW_NGE(BasicProcess):
    """!
        Electricity production with a Natural Gas Engine.
    """

    def apply(self, input_stream):

        self.name = "GTW (NGE)"

        flowrate = input_stream.get_flowrate()
        heavies = input_stream.propane + \
                  input_stream.butane + \
                  input_stream.pentane
        if (input_stream.hydrogen_sulphide/flowrate >
                    info[self.name]["H2S lim"] or
            input_stream.carbon_dioxide/flowrate >
                    info[self.name]["CO2 lim"] or
            heavies/flowrate >
                    info[self.name]["hvy lim"]):
            return [False]

        self.scale = input_stream.get_flowrate()
        self.capex = info[self.name]["CAPEX"]*self.scale
        self.opex = info[self.name]["OPEX"]*self.scale*to_annual
        self.energy = info[self.name]["Energy"]*self.scale*from_mmscfd
        self.emissions = info[self.name]["Emissions"]*self.scale*from_mmscfd

        gtw = Stream()
        gtw.value = input_stream.value
        gtw.electricity = (info[self.name]["Product"][input_stream.ptreat]*
                           self.scale*from_mmscfd_to_mwh)

        return [gtw]

classes_dict = {
        "Chemical": ChemicalAGR,
        "Membrane": MembraneAGR,
        "PSA": PSAAGR,
        "Basic": BasicProcess,
        "NGL removal": RemovalNGL,
        "Full Fractionation": FullFractionationNGL,
        "LNG": LNG,
        "CNG": CNG,
        "Gray Methanol": GrayMethanol,
        "Turquoise Methanol": TurquoiseMethanol,
        "GTW (CCGT+CCS)": GTW_CCGT_CCS,
        "GTW (CCGT)": GTW_CCGT,
        "GTW (NGT+CHP+CCS)": GTW_NGT_CHP_CCS,
        "GTW (NGT+CHP)": GTW_NGT_CHP,
        "GTW (NGT)": GTW_NGT,
        "GTW (NGE)": GTW_NGE,
}

