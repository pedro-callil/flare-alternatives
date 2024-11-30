import wx
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

from field_gas_profiles import components

class PieChartTab(wx.Panel):
    def __init__(self, parent, data_structure):
        wx.Panel.__init__(self, parent)

        self.data_structure = data_structure

    def draw(self):

        if abs(sum(self.data_structure.components)) <= 1e-6:
            return 0

        appearance = wx.SystemSettings.GetAppearance()
        colfac256 = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        colfac = (colfac256[0]/256, colfac256[1]/256,
                  colfac256[2]/256, colfac256[3]/256)
        if appearance.IsUsingDarkBackground():
            colstr = 'white'
        else:
            colstr = 'black'

        self.figure = Figure(figsize=(2.5,3.5),
                             facecolor=colfac)
        self.figure.set_tight_layout(True)
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        wedges, tmp1 = self.axes.pie(self.data_structure.components)
        self.axes.legend(wedges, components,
                         loc="lower center",
                         bbox_to_anchor=(0.5, -0.75),
                         facecolor=colfac,
                         prop={'size': 8},
                         labelcolor=colstr)
        self.axes.set_title('Gas profile',
                            fontdict={'fontsize': 8})
        self.axes.title.set_color(colstr)
        self.figure.subplots_adjust(bottom=3,top=3.5)

