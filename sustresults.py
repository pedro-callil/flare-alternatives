import wx
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
from matplotlib.pyplot import colormaps

import numpy as np

class SustBarChartTab(wx.Panel):
    def __init__(self, parent, data_structure):
        wx.Panel.__init__(self, parent)

        self.data_structure = data_structure

    def draw(self):

        #if len([i for i in self.data_structure.alternatives if i]) == 0:
        #    return 0

        appearance = wx.SystemSettings.GetAppearance()
        colfac256 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        colfac = (colfac256[0]/256, colfac256[1]/256,
                  colfac256[2]/256, colfac256[3]/256)
        if appearance.IsUsingDarkBackground():
            colstr = 'white'
        else:
            colstr = 'black'

        #width, height = self.GetSize()
        self.figure = Figure(figsize=(6,5),
                             facecolor=colfac)
        self.figure.set_tight_layout(True)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_facecolor(colfac)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        cumsum_wc = []
        cumsum_wce = []
        for i in range(len(self.data_structure.npvlabels)):
            cumsum_wc.append(self.data_structure.capex[i]+
                             self.data_structure.opex[i])
            cumsum_wce.append(cumsum_wc[-1]+
                             self.data_structure.carbon[i])

        colors = colormaps['viridis']([0.3,0.6,0.8,1])

        self.axes.barh(self.data_structure.npvlabels,
                       self.data_structure.capex,
                       label='CAPEX',
                       color=colors[0])
        self.axes.barh(self.data_structure.npvlabels,
                       self.data_structure.opex,
                       left=self.data_structure.capex,
                       label='OPEX',
                       color=colors[1])
        self.axes.barh(self.data_structure.npvlabels,
                       self.data_structure.carbon,
                       left=cumsum_wc,
                       label='CO₂ tax',
                       color=colors[2])
        self.axes.barh(self.data_structure.npvlabels,
                       self.data_structure.energy,
                       left=cumsum_wce,
                       label='Energy',
                       color=colors[3])

        self.axes.legend(ncols=4, loc='lower left',
                         bbox_to_anchor=(0.15, 1), fontsize=8,
                         facecolor=colfac, labelcolor=colstr)

        self.axes.tick_params(which="both",
                              color=colstr,
                              labelcolor=colstr,
                              labelsize=8)
        for spine in ['bottom', 'top', 'left', 'right']:
            self.axes.spines[spine].set_color(colstr)

