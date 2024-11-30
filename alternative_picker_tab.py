import wx

from alternatives import alternatives
from alternatives import ccs_alternatives

class AlternativePickerTab(wx.Panel):
    def __init__(self, parent, data_structure):
        wx.Panel.__init__(self, parent)

        self.data_structure = data_structure

        title_alternative_input = wx.StaticText( self, -1,
                        'Selection of alternatives to flaring' )

        alternative_static_text = wx.StaticText( self, -1,
                            'Select all possible alternatives to flaring:')

        self.alternative_list_selection = wx.CheckListBox(self,
                            size=(300, -1),
                            choices=alternatives)

        self.Bind(wx.EVT_CHECKLISTBOX, self.get_checked_alternatives,
                  self.alternative_list_selection)

        ccs_text = wx.StaticText( self, -1,
                            'Carbon Capture solution:')

        self.ccs_is_considered = wx.Choice(self,
                                      choices=ccs_alternatives)

        self.Bind(wx.EVT_CHOICE, self.get_ccs_alternative,
                  self.ccs_is_considered)

        carbon_tax_text = wx.StaticText(self, -1,
                                        'Carbon tax (US$/ton):')

        self.carbon_tax_input = wx.TextCtrl(self, wx.ID_ANY, '0.0')

        self.Bind(wx.EVT_TEXT, self.get_carbon_tax,
                  self.carbon_tax_input)

        extra_penalties_text = wx.StaticText(self, -1,
                                        'Extra penalties for:')

        self.water_penalty = wx.CheckBox(self, label="Water usage")
        self.electricity_penalty = wx.CheckBox(self, label="Energy usage")
        self.carbon_penalty = wx.CheckBox(self, label="CO₂ release")
        self.size_penalty = wx.CheckBox(self, label="Size (limited space)")

        self.Bind(wx.EVT_CHECKBOX, self.get_extra_penalty_water,
                  self.water_penalty)
        self.Bind(wx.EVT_CHECKBOX, self.get_extra_penalty_electricity,
                  self.electricity_penalty)
        self.Bind(wx.EVT_CHECKBOX, self.get_extra_penalty_carbon,
                  self.carbon_penalty)
        self.Bind(wx.EVT_CHECKBOX, self.get_extra_penalty_size,
                  self.size_penalty)

        LeftSizer = wx.BoxSizer(wx.VERTICAL)

        LeftSizer.Add(alternative_static_text)
        LeftSizer.Add((0,10))
        LeftSizer.Add(self.alternative_list_selection)

        RightSizer = wx.BoxSizer(wx.VERTICAL)

        RightSizer.Add(ccs_text,
                           flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,10))
        RightSizer.Add(self.ccs_is_considered,
                           flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,10))
        RightSizer.Add(carbon_tax_text,
                           flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,10))
        RightSizer.Add(self.carbon_tax_input,
                           flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,10))
        RightSizer.Add(extra_penalties_text,
                           flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,5))
        RightSizer.Add(self.water_penalty,
                           flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,5))
        RightSizer.Add(self.electricity_penalty,
                           flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,5))
        RightSizer.Add(self.carbon_penalty,
                           flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,5))
        RightSizer.Add(self.size_penalty,
                           flag=wx.ALIGN_LEFT)

        BottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        BottomSizer.Add((20,0))
        BottomSizer.Add(RightSizer, flag=wx.ALIGN_LEFT)
        BottomSizer.Add((30,0))
        BottomSizer.Add(LeftSizer, flag=wx.EXPAND)
        BottomSizer.Add((20,0))

        topLevelSizer = wx.BoxSizer(wx.VERTICAL)

        topLevelSizer.Add((0, 10))
        topLevelSizer.Add(title_alternative_input,
                          flag=wx.ALIGN_CENTER)
        topLevelSizer.Add((0, 10))
        topLevelSizer.Add(BottomSizer,
                          flag=wx.EXPAND)

        self.SetSizer(topLevelSizer)

    def get_checked_alternatives(self, e):

        for i in range(self.alternative_list_selection.GetCount()):
            if self.alternative_list_selection.IsChecked(i):
                self.data_structure.alternatives[i] = True
            else:
                self.data_structure.alternatives[i] = False

    def get_extra_penalty_water(self, e):
        if self.water_penalty.IsChecked():
            self.data_structure.extra_penalty_water = True
        else:
            self.data_structure.extra_penalty_water = False

    def get_extra_penalty_electricity(self, e):
        if self.electricity_penalty.IsChecked():
            self.data_structure.extra_penalty_electricity = True
        else:
            self.data_structure.extra_penalty_electricity = False

    def get_extra_penalty_carbon(self, e):
        if self.carbon_penalty.IsChecked():
            self.data_structure.extra_penalty_carbon = True
        else:
            self.data_structure.extra_penalty_carbon = False

    def get_extra_penalty_size(self, e):
        if self.size_penalty.IsChecked():
            self.data_structure.extra_penalty_size = True
        else:
            self.data_structure.extra_penalty_size = False

    def get_ccs_alternative(self, e):
        self.data_structure.carbon_capture = self.ccs_is_considered.GetSelection()

    def get_carbon_tax(self, e):
        try:
            self.data_structure.carbon_tax = float(self.carbon_tax_input.GetValue())
        except ValueError:
            self.data_structure.carbon_tax = 0.0
