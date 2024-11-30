import wx
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

from field_gas_profiles import components
from alternatives import alternatives
from econresults import EconBarChartTab
from sustresults import SustBarChartTab
from profresults import PieChartTab

class ResultsTab(wx.Panel):
    def __init__(self, parent, data_structure):
        wx.Panel.__init__(self, parent)

        self.data_structure = data_structure

        title_results = wx.StaticText( self, -1,
                        'Economic optimization' )

        start_interface = wx.Button(self, label="Read data")

        calc_interface = wx.Button(self, label="Calculate costs")

        startInterfaceSizer = wx.BoxSizer(wx.HORIZONTAL)
        startInterfaceSizer.Add((20,0))
        startInterfaceSizer.Add(start_interface,
                                flag=wx.ALIGN_LEFT)

        self.Bind(wx.EVT_BUTTON, self.on_start_btn,
                  start_interface)

        calculate_costs_text = wx.StaticText( self, -1,
                        'Net Present Values (10⁶ US$):')

        startCalcsSizer = wx.BoxSizer(wx.HORIZONTAL)
        startCalcsSizer.Add(calc_interface,
                                flag=wx.ALIGN_LEFT)

        self.Bind(wx.EVT_BUTTON, self.on_calc_btn,
                  calc_interface)

        flare_intensity_text = wx.StaticText( self, -1,
                        'Flare intensity (Mscm³/yr):')

        self.flare_intensity_data = wx.StaticText( self, -1, '')

        flareIntensitySizer = wx.BoxSizer(wx.HORIZONTAL)
        flareIntensitySizer.Add((20,0))
        flareIntensitySizer.Add(flare_intensity_text,
                                flag=wx.ALIGN_CENTER)
        flareIntensitySizer.Add((5,0))
        flareIntensitySizer.Add(self.flare_intensity_data,
                                flag=wx.ALIGN_CENTER)

        self.piechart = PieChartTab(self, data_structure)

        self.econbarchart = EconBarChartTab(self, data_structure)

        self.sustbarchart = SustBarChartTab(self, data_structure)

        RightSizer = wx.BoxSizer(wx.VERTICAL)
        RightSizer.Add(startInterfaceSizer,
                       flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,10))
        RightSizer.Add(flareIntensitySizer,
                       flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,10))
        RightSizer.Add(self.piechart,
                       flag=wx.ALIGN_LEFT)

        LeftSizer = wx.BoxSizer(wx.VERTICAL)
        LeftSizer.Add(startCalcsSizer,
                       flag=wx.ALIGN_LEFT)
        LeftSizer.Add((0,10))
        LeftSizer.Add(calculate_costs_text,
                                flag=wx.ALIGN_LEFT)
        LeftSizer.Add((0,10))
        LeftSizer.Add(self.econbarchart,
                       flag=wx.ALIGN_LEFT)

        BottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        #BottomSizer.Add((20,0))
        BottomSizer.Add(RightSizer, flag=wx.ALIGN_LEFT)
        BottomSizer.Add((30,0))
        BottomSizer.Add(LeftSizer, flag=wx.EXPAND)
        #BottomSizer.Add((20,0))

        env_analysis_btn = wx.Button(self, label="Sustainability analysis")

        sust_str = 'CO₂ release, water and energy usage and'
        sust_str += ' effluent treatment (10⁶ US$/yr):'
        sustainability_text = wx.StaticText(self, -1, sust_str)

        sustBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
        sustBtnSizer.Add((20,0))
        sustBtnSizer.Add(env_analysis_btn,
                          flag=wx.ALIGN_CENTER)
        sustBtnSizer.Add((5,0))

        sustTextSizer = wx.BoxSizer(wx.HORIZONTAL)
        sustTextSizer.Add((20,0))
        sustTextSizer.Add(sustainability_text,
                          flag=wx.ALIGN_CENTER)
        sustTextSizer.Add((5,0))

        self.Bind(wx.EVT_BUTTON, self.on_sust_btn,
                  env_analysis_btn)

        envSizer = wx.BoxSizer(wx.VERTICAL)
        envSizer.Add((0,10))
        envSizer.Add(sustBtnSizer, flag=wx.ALIGN_LEFT)
        envSizer.Add((0,10))
        envSizer.Add(sustTextSizer, flag=wx.ALIGN_LEFT)
        envSizer.Add((0,10))
        envSizer.Add(self.sustbarchart,
                     flag=wx.ALIGN_LEFT)

        title_environ = wx.StaticText( self, -1,
                        'Environmentally friendly options' )

        topLevelSizer = wx.BoxSizer(wx.VERTICAL)

        topLevelSizer.Add((0, 10))
        topLevelSizer.Add(title_results,
                          flag=wx.ALIGN_CENTER)
        topLevelSizer.Add((0, 10))
        topLevelSizer.Add(BottomSizer,
                          flag=wx.EXPAND)
        topLevelSizer.Add((0, 10))
        topLevelSizer.Add(title_environ,
                          flag=wx.ALIGN_CENTER)
        topLevelSizer.Add((0, 10))
        topLevelSizer.Add(envSizer,
                          flag=wx.EXPAND)
        topLevelSizer.Add((0, 800))

        self.SetSizer(topLevelSizer)

    def on_start_btn(self, e):

        self.flare_intensity_data.SetLabel(
                str(self.data_structure.flare_intensity()))

        self.piechart.draw()

        self.Layout()

    def on_calc_btn(self, e):

        self.data_structure.net_present_values()

        self.econbarchart.draw()

        self.Layout()

    def on_sust_btn(self, e):

        self.data_structure.cwee_cost()

        self.sustbarchart.draw()

        self.Layout()

