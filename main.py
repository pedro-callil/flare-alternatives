#! /usr/bin/env python3

import wx

from field_gas_profiles import components
from field_gas_profiles import region_choices
from field_gas_profiles import country_choices
from field_gas_profiles import field_choices
from field_gas_profiles import field_chats

from gas_input_tab import GasInputTab
from alternative_picker_tab import AlternativePickerTab
from results_tab import ResultsTab
from data_structure import DataStructure

class MainAppFrame(wx.Frame):
    def __init__(self):

        data = DataStructure()

        sizex, sizey = wx.DisplaySize()
        sizex = int(sizex*1/2+0.5)
        sizey = int(sizey*4/5+0.5)
        wx.Frame.__init__(self, None,
                          title="Natural Gas Destination Tool",
                          size=(sizex, sizey),
                          style=wx.DEFAULT_FRAME_STYLE | wx.CENTER)

        self.Bind(wx.EVT_SIZE, self.renew_size)
        self.window = wx.ScrolledWindow(self)
        notebook = wx.Notebook(self.window)

        gas_input_tab = GasInputTab(notebook, data)

        alternative_picker_tab = AlternativePickerTab(notebook, data)

        results_tab = ResultsTab(notebook, data)

        notebook.AddPage(gas_input_tab, "Gas Profile")
        notebook.AddPage(alternative_picker_tab, "Flare alternatives")
        notebook.AddPage(results_tab, "Results")

        self.window.SetScrollRate(10, 10)
        self.window.EnableScrolling(True, True)
        sizer = wx.BoxSizer()
        sizer.Add(notebook, 1, wx.EXPAND)
        self.window.SetSizer(sizer)

    def renew_size(self, e):
        self.window.SetSize(self.GetClientSize())


if __name__=="__main__":
    app = wx.App()
    MainAppFrame().Show()
    app.MainLoop()
