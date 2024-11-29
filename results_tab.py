import wx

from field_gas_profiles import components
from alternatives import alternatives

class ResultsTab(wx.Panel):
    def __init__(self, parent, data_structure):
        wx.Panel.__init__(self, parent)

        self.data_structure = data_structure

        title_results = wx.StaticText( self, -1,
                        'Economic optimization' )

        start_interface = wx.Button(self, label="Read Data")

        startInterfaceSizer = wx.BoxSizer(wx.HORIZONTAL)
        startInterfaceSizer.Add((20,0))
        startInterfaceSizer.Add(start_interface,
                                flag=wx.ALIGN_LEFT)

        self.Bind(wx.EVT_BUTTON, self.on_start_btn,
                  start_interface)

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

        RightSizer = wx.BoxSizer(wx.VERTICAL)
        RightSizer.Add(startInterfaceSizer,
                       flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,10))
        RightSizer.Add(flareIntensitySizer,
                       flag=wx.ALIGN_LEFT)

        BottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        #BottomSizer.Add((20,0))
        BottomSizer.Add(RightSizer, flag=wx.ALIGN_LEFT)
        #BottomSizer.Add((30,0))
        #BottomSizer.Add(LeftSizer, flag=wx.EXPAND)
        #BottomSizer.Add((20,0))

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

        self.SetSizer(topLevelSizer)

    def on_start_btn(self, e):

        self.flare_intensity_data.SetLabel(
                str(self.data_structure.flare_intensity()))

        self.data_structure.generate_pie_chart()

        print(self.data_structure)
