import wx

from field_gas_profiles import components
from field_gas_profiles import region_choices
from field_gas_profiles import country_choices
from field_gas_profiles import field_choices
from field_gas_profiles import field_chats

class GasInputTab(wx.Panel):
    def __init__(self, parent, data_structure):
        wx.Panel.__init__(self, parent)

        self.data_structure = data_structure

        title_gas_input = wx.StaticText( self, -1,
                        'Gas field selection, gas profile and volume' )

        title_profile_input = wx.StaticText( self, -1,
                        'Edit gas profile:' )
        title_well_input = wx.StaticText( self, -1,
                        'Select a basin:' )

        title_composition_input = wx.StaticText( self, -1,
                        'Gas profile (mol fraction):' )

        region_input = wx.StaticText( self, -1,
                        'Region:' )

        self.region_choice = wx.Choice(self, size=(200, -1))
        self.region_choice.Clear()
        for region in region_choices:
            self.region_choice.Append(region)

        country_input = wx.StaticText( self, -1,
                        'Country:' )

        self.country_choice = wx.Choice(self, size=(200, -1))

        self.Bind(wx.EVT_CHOICE, self.change_country_menu,
                  self.region_choice)

        field_input = wx.StaticText( self, -1,
                        'Field:' )

        self.field_choice = wx.Choice(self, size=(200, -1))

        self.Bind(wx.EVT_CHOICE, self.change_field_menu,
                  self.country_choice)

        self.Bind(wx.EVT_CHOICE, self.change_gas_profile,
                  self.field_choice)

        self.gas_profiles = []
        for elem in components:
            self.gas_profiles.append([])
            self.gas_profiles[-1].append(wx.StaticText(self, -1, elem))
            self.gas_profiles[-1].append(wx.TextCtrl(self, wx.ID_ANY, '0.0'))

        gas_volume_label = wx.StaticText(self, -1,
                                         'Then, enter flared gas volume (MMSCFD):')
        self.gas_volume = wx.TextCtrl(self, wx.ID_ANY, '0.0')

        self.Bind(wx.EVT_TEXT, self.store_volume, self.gas_volume)

        gasVolumeSizer = wx.BoxSizer(wx.HORIZONTAL)
        gasVolumeSizer.Add((20,0))
        gasVolumeSizer.Add(gas_volume_label,
                            flag=wx.ALIGN_CENTER)
        gasVolumeSizer.Add((5,0))
        gasVolumeSizer.Add(self.gas_volume,
                            flag=wx.ALIGN_CENTER)

        gasProfileSizer = wx.GridSizer(rows=len(components),
                                       cols=2, hgap=0, vgap=5)

        for elem in self.gas_profiles:
            gasProfileSizer.Add(elem[0], flag=wx.ALIGN_LEFT)
            gasProfileSizer.Add(elem[1], flag=wx.ALIGN_RIGHT)
            self.Bind(wx.EVT_TEXT, self.store_gas_profile,
                      elem[1])

        topLevelSizer = wx.BoxSizer(wx.VERTICAL)

        topLevelSizer.Add((0, 10))
        topLevelSizer.Add(title_gas_input,
                          flag=wx.ALIGN_CENTER)
        topLevelSizer.Add((0, 10))

        BottomSizer = wx.BoxSizer(wx.HORIZONTAL)

        LeftSizer = wx.BoxSizer(wx.VERTICAL)
        LeftSizer.Add(title_profile_input,
                      flag=wx.ALIGN_LEFT)
        LeftSizer.Add((0,10))
        LeftSizer.Add(title_composition_input,
                      flag=wx.ALIGN_LEFT)
        LeftSizer.Add((0,10))
        LeftSizer.Add(gasProfileSizer,
                      flag=wx.ALIGN_LEFT)

        RightSizer = wx.BoxSizer(wx.VERTICAL)
        RightSizer.Add(title_well_input,
                       flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,10))
        RightSizer.Add(region_input,
                       flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,10))
        RightSizer.Add(self.region_choice,
                       flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,10))
        RightSizer.Add(country_input,
                       flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,10))
        RightSizer.Add(self.country_choice,
                       flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,10))
        RightSizer.Add(field_input,
                       flag=wx.ALIGN_LEFT)
        RightSizer.Add((0,10))
        RightSizer.Add(self.field_choice,
                       flag=wx.ALIGN_LEFT)

        BottomSizer.Add((20,0))
        BottomSizer.Add(LeftSizer,
                        flag=wx.EXPAND)
        BottomSizer.Add((30,0))
        BottomSizer.Add(RightSizer,
                        flag=wx.EXPAND)
        BottomSizer.Add((20,0))

        topLevelSizer.Add(BottomSizer,
                          flag=wx.EXPAND)

        topLevelSizer.Add((0,30))
        topLevelSizer.Add(gasVolumeSizer,
                      flag=wx.ALIGN_LEFT)
        topLevelSizer.AddStretchSpacer()

        self.SetSizer(topLevelSizer)

    def change_country_menu(self, e):
        self.country_choice.Clear()
        choices=country_choices[self.region_choice.GetString(
                                    self.region_choice.GetSelection())]
        for country in choices:
            self.country_choice.Append(country)
        self.field_choice.Clear()

    def change_field_menu(self, e):
        self.data_structure.location = self.country_choice.GetString(
                                self.country_choice.GetSelection())
        self.field_choice.Clear()
        choices=field_choices[self.data_structure.location]
        for field in choices:
            self.field_choice.Append(field)

    def change_gas_profile(self, e):
        field = field_chats[self.field_choice.GetString(
                self.field_choice.GetSelection())]
        for i, elem in enumerate(self.gas_profiles):
            elem[1].SetValue(str(field[i]))

    def store_gas_profile(self, e):
        for i, elem in enumerate(self.gas_profiles):
            try:
                self.data_structure.components[i] = float(
                        elem[1].GetValue())
            except ValueError:
                self.data_structure.components[i] = 0.0

    def store_volume(self, e):
        try:
            self.data_structure.volume = float(self.gas_volume.GetValue())*1e6
        except ValueError:
            self.data_structure.volume = 0.0
