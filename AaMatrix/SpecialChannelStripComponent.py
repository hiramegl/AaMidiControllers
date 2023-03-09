import time
import Live

from _Framework.ChannelStripComponent import ChannelStripComponent
from ConfigurableButtonElement import ConfigurableButtonElement

class SpecialChannelStripComponent(ChannelStripComponent):

  def __init__(self):
    ChannelStripComponent.__init__(self)
    self.m_oPanResetButton = None
    self.m_oVolResetButton = None
    self.m_oDeckButton     = None
    self.m_oSend1Button    = None
    self.m_oSend2Button    = None
    self.m_oSend3Button    = None
    self.m_oSend4Button    = None
    self.m_oSend5Button    = None
    self.m_oSend6Button    = None
    self.m_oSend7Button    = None
    self.m_oSend8Button    = None
    self.m_oViewClipButton = None
    self.m_oViewDevButton  = None
    self.m_oVol1Button     = None
    self.m_oVol2Button     = None
    self.m_oVol3Button     = None
    self.m_oVol4Button     = None
    self.m_oVol5Button     = None
    self.m_oVol6Button     = None
    self.m_oVol7Button     = None
    self.m_oVol8Button     = None
    self.m_aVolMap         = [1.0, 0.92, 0.85, 0.7, 0.6, 0.5, 0.4, 0.2]

  def disconnect(self):
    oTrack = self.get_track_or_none()

    # remove track parameters listeners
    if oTrack != None:
      oMixDev = oTrack.mixer_device
      oPan    = oMixDev.panning
      oVol    = oMixDev.volume
      aSends  = oMixDev.sends
      if oPan.value_has_listener(self._on_pan_reset_changed):
        oPan.remove_value_listener(self._on_pan_reset_changed)
      if oVol.value_has_listener(self._on_vol_changed):
        oVol.remove_value_listener(self._on_vol_changed)
      if oMixDev.crossfade_assign_has_listener(self._on_deck_changed):
        oMixDev.remove_crossfade_assign_listener(self._on_deck_changed)
      if len(aSends) > 0 and aSends[0].value_has_listener(self._on_send1_changed):
        aSends[0].remove_value_listener(self._on_send1_changed)
      if len(aSends) > 1 and aSends[1].value_has_listener(self._on_send2_changed):
        aSends[1].remove_value_listener(self._on_send2_changed)
      if len(aSends) > 2 and aSends[2].value_has_listener(self._on_send3_changed):
        aSends[2].remove_value_listener(self._on_send3_changed)
      if len(aSends) > 3 and aSends[3].value_has_listener(self._on_send4_changed):
        aSends[3].remove_value_listener(self._on_send4_changed)
      if len(aSends) > 4 and aSends[4].value_has_listener(self._on_send5_changed):
        aSends[4].remove_value_listener(self._on_send5_changed)
      if len(aSends) > 5 and aSends[5].value_has_listener(self._on_send6_changed):
        aSends[5].remove_value_listener(self._on_send6_changed)
      if len(aSends) > 6 and aSends[6].value_has_listener(self._on_send7_changed):
        aSends[6].remove_value_listener(self._on_send6_changed)
      if len(aSends) > 7 and aSends[7].value_has_listener(self._on_send8_changed):
        aSends[7].remove_value_listener(self._on_send6_changed)

    # remove buttons listeners
    if self.m_oPanResetButton != None:
      self.m_oPanResetButton.remove_value_listener(self._on_pan_reset_value)
      self.m_oPanResetButton = None
    if self.m_oVolResetButton != None:
      self.m_oVolResetButton.remove_value_listener(self._on_vol_reset_value)
      self.m_oVolResetButton = None
    if self.m_oDeckButton != None:
      self.m_oDeckButton.remove_value_listener(self._on_deck_value)
      self.m_oDeckButton = None
    if self.m_oSend1Button != None:
      self.m_oSend1Button.remove_value_listener(self._on_send1_value)
      self.m_oSend1Button = None
    if self.m_oSend2Button != None:
      self.m_oSend2Button.remove_value_listener(self._on_send2_value)
      self.m_oSend2Button = None
    if self.m_oSend3Button != None:
      self.m_oSend3Button.remove_value_listener(self._on_send3_value)
      self.m_oSend3Button = None
    if self.m_oSend4Button != None:
      self.m_oSend4Button.remove_value_listener(self._on_send4_value)
      self.m_oSend4Button = None
    if self.m_oSend5Button != None:
      self.m_oSend5Button.remove_value_listener(self._on_send5_value)
      self.m_oSend5Button = None
    if self.m_oSend6Button != None:
      self.m_oSend6Button.remove_value_listener(self._on_send6_value)
      self.m_oSend6Button = None
    if self.m_oSend7Button != None:
      self.m_oSend7Button.remove_value_listener(self._on_send7_value)
      self.m_oSend7Button = None
    if self.m_oSend8Button != None:
      self.m_oSend8Button.remove_value_listener(self._on_send8_value)
      self.m_oSend8Button = None
    if self.m_oViewClipButton != None:
      self.m_oViewClipButton.remove_value_listener(self._on_view_clip_value)
      self.m_oViewClipButton = None
    if self.m_oViewDevButton != None:
      self.m_oViewDevButton.remove_value_listener(self._on_view_dev_value)
      self.m_oViewDevButton = None
    if self.m_oVol1Button != None:
      self.m_oVol1Button.remove_value_listener(self._on_vol1_value)
      self.m_oVol1Button = None
    if self.m_oVol2Button != None:
      self.m_oVol2Button.remove_value_listener(self._on_vol2_value)
      self.m_oVol2Button = None
    if self.m_oVol3Button != None:
      self.m_oVol3Button.remove_value_listener(self._on_vol3_value)
      self.m_oVol3Button = None
    if self.m_oVol4Button != None:
      self.m_oVol4Button.remove_value_listener(self._on_vol4_value)
      self.m_oVol4Button = None
    if self.m_oVol5Button != None:
      self.m_oVol5Button.remove_value_listener(self._on_vol5_value)
      self.m_oVol5Button = None
    if self.m_oVol6Button != None:
      self.m_oVol6Button.remove_value_listener(self._on_vol6_value)
      self.m_oVol6Button = None
    if self.m_oVol7Button != None:
      self.m_oVol7Button.remove_value_listener(self._on_vol7_value)
      self.m_oVol7Button = None
    if self.m_oVol8Button != None:
      self.m_oVol8Button.remove_value_listener(self._on_vol8_value)
      self.m_oVol8Button = None
    ChannelStripComponent.disconnect(self)

  def set_track(self, _oTrack):
    assert ((_oTrack == None) or isinstance(_oTrack, Live.Track.Track))
    if (_oTrack != self._track):
      oTrack = self.get_track_or_none()
      if oTrack != None: # it has to be a track not a return!
        oMixDev = self._track.mixer_device
        oPan    = oMixDev.panning
        oVol    = oMixDev.volume
        aSends  = oMixDev.sends
        if oPan.value_has_listener(self._on_pan_reset_changed):
          oPan.remove_value_listener(self._on_pan_reset_changed)
        if oVol.value_has_listener(self._on_vol_changed):
          oVol.remove_value_listener(self._on_vol_changed)
        if oMixDev.crossfade_assign_has_listener(self._on_deck_changed):
          oMixDev.remove_crossfade_assign_listener(self._on_deck_changed)
        if len(aSends) > 0 and aSends[0].value_has_listener(self._on_send1_changed):
          aSends[0].remove_value_listener(self._on_send1_changed)
        if len(aSends) > 1 and aSends[1].value_has_listener(self._on_send2_changed):
          aSends[1].remove_value_listener(self._on_send2_changed)
        if len(aSends) > 2 and aSends[2].value_has_listener(self._on_send3_changed):
          aSends[2].remove_value_listener(self._on_send3_changed)
        if len(aSends) > 3 and aSends[3].value_has_listener(self._on_send4_changed):
          aSends[3].remove_value_listener(self._on_send4_changed)
        if len(aSends) > 4 and aSends[4].value_has_listener(self._on_send5_changed):
          aSends[4].remove_value_listener(self._on_send5_changed)
        if len(aSends) > 5 and aSends[5].value_has_listener(self._on_send6_changed):
          aSends[5].remove_value_listener(self._on_send6_changed)
        if len(aSends) > 6 and aSends[6].value_has_listener(self._on_send7_changed):
          aSends[6].remove_value_listener(self._on_send7_changed)
        if len(aSends) > 7 and aSends[7].value_has_listener(self._on_send8_changed):
          aSends[7].remove_value_listener(self._on_send8_changed)
      ChannelStripComponent.set_track(self, _oTrack)
    else:
      self.update()

  def set_track_controls(self, _oPanResetCtl, _oVolResetCtl, _oDeckCtl):
    assert ((_oPanResetCtl == None) or isinstance(_oPanResetCtl, ConfigurableButtonElement))
    assert ((_oVolResetCtl == None) or isinstance(_oVolResetCtl, ConfigurableButtonElement))
    assert ((_oDeckCtl   == None) or isinstance(_oDeckCtl  , ConfigurableButtonElement))
    if _oPanResetCtl != self.m_oPanResetButton:
      if self.m_oPanResetButton != None:
        self.m_oPanResetButton.remove_value_listener(self._on_pan_reset_value)
      self.m_oPanResetButton = _oPanResetCtl
      if self.m_oPanResetButton != None:
        self.m_oPanResetButton.add_value_listener(self._on_pan_reset_value)
    if _oVolResetCtl != self.m_oVolResetButton:
      if self.m_oVolResetButton != None:
        self.m_oVolResetButton.remove_value_listener(self._on_vol_reset_value)
      self.m_oVolResetButton = _oVolResetCtl
      if self.m_oVolResetButton != None:
        self.m_oVolResetButton.add_value_listener(self._on_vol_reset_value)
    if _oDeckCtl != self.m_oDeckButton:
      if self.m_oDeckButton != None:
        self.m_oDeckButton.remove_value_listener(self._on_deck_value)
      self.m_oDeckButton = _oDeckCtl
      if self.m_oDeckButton != None:
        self.m_oDeckButton.add_value_listener(self._on_deck_value)
    self.update()

  def set_send_controls(self, _oSend1Control, _oSend2Control, _oSend3Control, _oSend4Control, _oSend5Control, _oSend6Control, _oSend7Control, _oSend8Control):
    assert ((_oSend1Control == None) or isinstance(_oSend1Control, ConfigurableButtonElement))
    assert ((_oSend2Control == None) or isinstance(_oSend2Control, ConfigurableButtonElement))
    assert ((_oSend3Control == None) or isinstance(_oSend3Control, ConfigurableButtonElement))
    assert ((_oSend4Control == None) or isinstance(_oSend4Control, ConfigurableButtonElement))
    assert ((_oSend5Control == None) or isinstance(_oSend5Control, ConfigurableButtonElement))
    assert ((_oSend6Control == None) or isinstance(_oSend6Control, ConfigurableButtonElement))
    assert ((_oSend7Control == None) or isinstance(_oSend7Control, ConfigurableButtonElement))
    assert ((_oSend8Control == None) or isinstance(_oSend8Control, ConfigurableButtonElement))
    if _oSend1Control != self.m_oSend1Button:
      if self.m_oSend1Button != None:
        self.m_oSend1Button.remove_value_listener(self._on_send1_value)
      self.m_oSend1Button = _oSend1Control
      if self.m_oSend1Button != None:
        self.m_oSend1Button.add_value_listener(self._on_send1_value)
    if _oSend2Control != self.m_oSend2Button:
      if self.m_oSend2Button != None:
        self.m_oSend2Button.remove_value_listener(self._on_send2_value)
      self.m_oSend2Button = _oSend2Control
      if self.m_oSend2Button != None:
        self.m_oSend2Button.add_value_listener(self._on_send2_value)
    if _oSend3Control != self.m_oSend3Button:
      if self.m_oSend3Button != None:
        self.m_oSend3Button.remove_value_listener(self._on_send3_value)
      self.m_oSend3Button = _oSend3Control
      if self.m_oSend3Button != None:
        self.m_oSend3Button.add_value_listener(self._on_send3_value)
    if _oSend4Control != self.m_oSend4Button:
      if self.m_oSend4Button != None:
        self.m_oSend4Button.remove_value_listener(self._on_send4_value)
      self.m_oSend4Button = _oSend4Control
      if self.m_oSend4Button != None:
        self.m_oSend4Button.add_value_listener(self._on_send4_value)
    if _oSend5Control != self.m_oSend5Button:
      if self.m_oSend5Button != None:
        self.m_oSend5Button.remove_value_listener(self._on_send5_value)
      self.m_oSend5Button = _oSend5Control
      if self.m_oSend5Button != None:
        self.m_oSend5Button.add_value_listener(self._on_send5_value)
    if _oSend6Control != self.m_oSend6Button:
      if self.m_oSend6Button != None:
        self.m_oSend6Button.remove_value_listener(self._on_send6_value)
      self.m_oSend6Button = _oSend6Control
      if self.m_oSend6Button != None:
        self.m_oSend6Button.add_value_listener(self._on_send6_value)
    if _oSend7Control != self.m_oSend7Button:
      if self.m_oSend7Button != None:
        self.m_oSend7Button.remove_value_listener(self._on_send7_value)
      self.m_oSend7Button = _oSend7Control
      if self.m_oSend7Button != None:
        self.m_oSend7Button.add_value_listener(self._on_send7_value)
    if _oSend8Control != self.m_oSend8Button:
      if self.m_oSend8Button != None:
        self.m_oSend8Button.remove_value_listener(self._on_send8_value)
      self.m_oSend8Button = _oSend8Control
      if self.m_oSend8Button != None:
        self.m_oSend8Button.add_value_listener(self._on_send8_value)
    self.update()

  def set_view_controls(self, _oViewClipButton, _oViewDevButton):
    assert ((_oViewClipButton == None) or isinstance(_oViewClipButton, ConfigurableButtonElement))
    assert ((_oViewDevButton  == None) or isinstance(_oViewDevButton,  ConfigurableButtonElement))
    if _oViewClipButton != self.m_oViewClipButton:
      if self.m_oViewClipButton != None:
        self.m_oViewClipButton.remove_value_listener(self._on_view_clip_value)
      self.m_oViewClipButton = _oViewClipButton
      if self.m_oViewClipButton != None:
        self.m_oViewClipButton.add_value_listener(self._on_view_clip_value)
    if _oViewDevButton != self.m_oViewDevButton:
      if self.m_oViewDevButton != None:
        self.m_oViewDevButton.remove_value_listener(self._on_view_dev_value)
      self.m_oViewDevButton = _oViewDevButton
      if self.m_oViewDevButton != None:
        self.m_oViewDevButton.add_value_listener(self._on_view_dev_value)
    self.update()

  def set_vol_controls(self, _oVol1Control, _oVol2Control, _oVol3Control, _oVol4Control, _oVol5Control, _oVol6Control, _oVol7Control, _oVol8Control):
    assert ((_oVol1Control == None) or isinstance(_oVol1Control, ConfigurableButtonElement))
    assert ((_oVol2Control == None) or isinstance(_oVol2Control, ConfigurableButtonElement))
    assert ((_oVol3Control == None) or isinstance(_oVol3Control, ConfigurableButtonElement))
    assert ((_oVol4Control == None) or isinstance(_oVol4Control, ConfigurableButtonElement))
    assert ((_oVol5Control == None) or isinstance(_oVol5Control, ConfigurableButtonElement))
    assert ((_oVol6Control == None) or isinstance(_oVol6Control, ConfigurableButtonElement))
    assert ((_oVol7Control == None) or isinstance(_oVol7Control, ConfigurableButtonElement))
    assert ((_oVol8Control == None) or isinstance(_oVol8Control, ConfigurableButtonElement))
    if _oVol1Control != self.m_oVol1Button:
      if self.m_oVol1Button != None:
        self.m_oVol1Button.remove_value_listener(self._on_vol1_value)
      self.m_oVol1Button = _oVol1Control
      if self.m_oVol1Button != None:
        self.m_oVol1Button.add_value_listener(self._on_vol1_value)
    if _oVol2Control != self.m_oVol2Button:
      if self.m_oVol2Button != None:
        self.m_oVol2Button.remove_value_listener(self._on_vol2_value)
      self.m_oVol2Button = _oVol2Control
      if self.m_oVol2Button != None:
        self.m_oVol2Button.add_value_listener(self._on_vol2_value)
    if _oVol3Control != self.m_oVol3Button:
      if self.m_oVol3Button != None:
        self.m_oVol3Button.remove_value_listener(self._on_vol3_value)
      self.m_oVol3Button = _oVol3Control
      if self.m_oVol3Button != None:
        self.m_oVol3Button.add_value_listener(self._on_vol3_value)
    if _oVol4Control != self.m_oVol4Button:
      if self.m_oVol4Button != None:
        self.m_oVol4Button.remove_value_listener(self._on_vol4_value)
      self.m_oVol4Button = _oVol4Control
      if self.m_oVol4Button != None:
        self.m_oVol4Button.add_value_listener(self._on_vol4_value)
    if _oVol5Control != self.m_oVol5Button:
      if self.m_oVol5Button != None:
        self.m_oVol5Button.remove_value_listener(self._on_vol5_value)
      self.m_oVol5Button = _oVol5Control
      if self.m_oVol5Button != None:
        self.m_oVol5Button.add_value_listener(self._on_vol5_value)
    if _oVol6Control != self.m_oVol6Button:
      if self.m_oVol6Button != None:
        self.m_oVol6Button.remove_value_listener(self._on_vol6_value)
      self.m_oVol6Button = _oVol6Control
      if self.m_oVol6Button != None:
        self.m_oVol6Button.add_value_listener(self._on_vol6_value)
    if _oVol7Control != self.m_oVol7Button:
      if self.m_oVol7Button != None:
        self.m_oVol7Button.remove_value_listener(self._on_vol7_value)
      self.m_oVol7Button = _oVol7Control
      if self.m_oVol7Button != None:
        self.m_oVol7Button.add_value_listener(self._on_vol7_value)
    if _oVol8Control != self.m_oVol8Button:
      if self.m_oVol8Button != None:
        self.m_oVol8Button.remove_value_listener(self._on_vol8_value)
      self.m_oVol8Button = _oVol8Control
      if self.m_oVol8Button != None:
        self.m_oVol8Button.add_value_listener(self._on_vol8_value)
    self.update()

  def update(self):
    ChannelStripComponent.update(self)
    if self._allow_updates:
      if self.is_enabled():
        oTrack = self.get_track_or_none()
        if oTrack != None:
          oMixDev = self._track.mixer_device
          oPan    = oMixDev.panning
          oVol    = oMixDev.volume
          aSends  = oMixDev.sends
          if not oPan.value_has_listener(self._on_pan_reset_changed):
            oPan.add_value_listener(self._on_pan_reset_changed)
          if not oVol.value_has_listener(self._on_vol_changed):
            oVol.add_value_listener(self._on_vol_changed)
          if not oMixDev.crossfade_assign_has_listener(self._on_deck_changed):
            oMixDev.add_crossfade_assign_listener(self._on_deck_changed)
          if len(aSends) > 0:
            if not aSends[0].value_has_listener(self._on_send1_changed):
              aSends[0].add_value_listener(self._on_send1_changed)
            self._on_send1_changed()
          elif self.m_oSend1Button != None:
            self.m_oSend1Button.turn_off()
          if len(aSends) > 1:
            if not aSends[1].value_has_listener(self._on_send2_changed):
              aSends[1].add_value_listener(self._on_send2_changed)
            self._on_send2_changed()
          elif self.m_oSend2Button != None:
            self.m_oSend2Button.turn_off()
          if len(aSends) > 2:
            if not aSends[2].value_has_listener(self._on_send3_changed):
              aSends[2].add_value_listener(self._on_send3_changed)
            self._on_send3_changed()
          elif self.m_oSend3Button != None:
            self.m_oSend3Button.turn_off()
          if len(aSends) > 3:
            if not aSends[3].value_has_listener(self._on_send4_changed):
              aSends[3].add_value_listener(self._on_send4_changed)
            self._on_send4_changed()
          elif self.m_oSend4Button != None:
            self.m_oSend4Button.turn_off()
          if len(aSends) > 4:
            if not aSends[4].value_has_listener(self._on_send5_changed):
              aSends[4].add_value_listener(self._on_send5_changed)
            self._on_send5_changed()
          elif self.m_oSend5Button != None:
            self.m_oSend5Button.turn_off()
          if len(aSends) > 5:
            if not aSends[5].value_has_listener(self._on_send6_changed):
              aSends[5].add_value_listener(self._on_send6_changed)
            self._on_send6_changed()
          elif self.m_oSend6Button != None:
            self.m_oSend6Button.turn_off()
          if len(aSends) > 6:
            if not aSends[6].value_has_listener(self._on_send7_changed):
              aSends[6].add_value_listener(self._on_send7_changed)
            self._on_send7_changed()
          elif self.m_oSend7Button != None:
            self.m_oSend7Button.turn_off()
          if len(aSends) > 7:
            if not aSends[7].value_has_listener(self._on_send8_changed):
              aSends[7].add_value_listener(self._on_send8_changed)
            self._on_send8_changed()
          elif self.m_oSend8Button != None:
            self.m_oSend8Button.turn_off()
        else:
          if self.m_oPanResetButton != None:
            self.m_oPanResetButton.reset()
          if self.m_oVolResetButton != None:
            self.m_oVolResetButton.reset()
          if self.m_oDeckButton != None:
            self.m_oDeckButton.reset()
          if self._solo_button != None:
            self._solo_button.reset()
          if self.m_oSend1Button != None:
            self.m_oSend1Button.reset()
          if self.m_oSend2Button != None:
            self.m_oSend2Button.reset()
          if self.m_oSend3Button != None:
            self.m_oSend3Button.reset()
          if self.m_oSend4Button != None:
            self.m_oSend4Button.reset()
          if self.m_oSend5Button != None:
            self.m_oSend5Button.reset()
          if self.m_oSend6Button != None:
            self.m_oSend6Button.reset()
          if self.m_oSend7Button != None:
            self.m_oSend7Button.reset()
          if self.m_oSend8Button != None:
            self.m_oSend8Button.reset()
          if self.m_oViewClipButton != None:
            self.m_oViewClipButton.reset()
          if self.m_oViewDevButton != None:
            self.m_oViewDevButton.reset()
          if self.m_oVol1Button != None:
            self.m_oVol1Button.reset()
          if self.m_oVol2Button != None:
            self.m_oVol2Button.reset()
          if self.m_oVol3Button != None:
            self.m_oVol3Button.reset()
          if self.m_oVol4Button != None:
            self.m_oVol4Button.reset()
          if self.m_oVol5Button != None:
            self.m_oVol5Button.reset()
          if self.m_oVol6Button != None:
            self.m_oVol6Button.reset()
          if self.m_oVol7Button != None:
            self.m_oVol7Button.reset()
          if self.m_oVol8Button != None:
            self.m_oVol8Button.reset()

        self._on_pan_reset_changed()
        self._on_vol_changed()
        self._on_deck_changed()
        self._on_send1_changed()
        self._on_send2_changed()
        self._on_send3_changed()
        self._on_send4_changed()
        self._on_send5_changed()
        self._on_send6_changed()
        self._on_send7_changed()
        self._on_send8_changed()
        self._on_view_clip_changed()
        self._on_view_dev_changed()

  # **************************************************************************

  def _on_pan_reset_value(self, _nValue):
    assert (self.m_oPanResetButton != None)
    assert (_nValue in range(128))
    if (self.is_enabled() and (self._track != None) and (_nValue == 127)):
      self._track.mixer_device.panning.value = 0

  def _on_pan_reset_changed(self):
    if (self.is_enabled() and (self.m_oPanResetButton != None)):
      if self._track != None:
        self.m_oPanResetButton.turn_on()  # pan reset ready to be used!
      else:
        self.m_oPanResetButton.turn_off() # pan reset unavailable!

  # **************************************************************************

  def _on_vol_reset_value(self, _nValue):
    assert (self.m_oVolResetButton != None)
    assert (_nValue in range(128))
    if (self.is_enabled() and (self._track != None) and (_nValue == 127)):
      self._track.mixer_device.volume.value = 0.85

  def _on_vol_changed(self):
    if self.is_enabled():
      if self.m_oVolResetButton != None:
        if self._track != None:
          self.m_oVolResetButton.turn_on()  # vol reset ready to be used!
        else:
          self.m_oVolResetButton.turn_off() # vol reset unavailable!
      if self.m_oVol1Button != None:
        if self._track != None:
          nVol = self._track.mixer_device.volume.value
          if (nVol >= self.m_aVolMap[0] - 0.01):
             self.m_oVol1Button.turn_on()
          else:
             self.m_oVol1Button.turn_off()
          if (nVol >= self.m_aVolMap[1] - 0.01):
             self.m_oVol2Button.turn_on()
          else:
             self.m_oVol2Button.turn_off()
          if (nVol >= self.m_aVolMap[2] - 0.01):
             self.m_oVol3Button.turn_on()
          else:
             self.m_oVol3Button.turn_off()
          if (nVol >= self.m_aVolMap[3] - 0.01):
             self.m_oVol4Button.turn_on()
          else:
             self.m_oVol4Button.turn_off()
          if (nVol >= self.m_aVolMap[4] - 0.01):
             self.m_oVol5Button.turn_on()
          else:
             self.m_oVol5Button.turn_off()
          if (nVol >= self.m_aVolMap[5] - 0.01):
             self.m_oVol6Button.turn_on()
          else:
             self.m_oVol6Button.turn_off()
          if (nVol >= self.m_aVolMap[6] - 0.01):
             self.m_oVol7Button.turn_on()
          else:
             self.m_oVol7Button.turn_off()
          if (nVol >= self.m_aVolMap[7] - 0.01):
             self.m_oVol8Button.turn_on()
          else:
             self.m_oVol8Button.turn_off()
        else:
          self.m_oVol1Button.set_light('Mixer.Vol.Unava')
          self.m_oVol2Button.set_light('Mixer.Vol.Unava')
          self.m_oVol3Button.set_light('Mixer.Vol.Unava')
          self.m_oVol4Button.set_light('Mixer.Vol.Unava')
          self.m_oVol5Button.set_light('Mixer.Vol.Unava')
          self.m_oVol6Button.set_light('Mixer.Vol.Unava')
          self.m_oVol7Button.set_light('Mixer.Vol.Unava')
          self.m_oVol8Button.set_light('Mixer.Vol.Unava')

  def _on_vol1_value(self, _nValue):
    self.handle_vol_value(_nValue, 0)

  def _on_vol2_value(self, _nValue):
    self.handle_vol_value(_nValue, 1)

  def _on_vol3_value(self, _nValue):
    self.handle_vol_value(_nValue, 2)

  def _on_vol4_value(self, _nValue):
    self.handle_vol_value(_nValue, 3)

  def _on_vol5_value(self, _nValue):
    self.handle_vol_value(_nValue, 4)

  def _on_vol6_value(self, _nValue):
    self.handle_vol_value(_nValue, 5)

  def _on_vol7_value(self, _nValue):
    self.handle_vol_value(_nValue, 6)

  def _on_vol8_value(self, _nValue):
    self.handle_vol_value(_nValue, 7)

  def handle_vol_value(self, _nValue, _nIdx):
    assert (_nValue in range(128))
    if (self.is_enabled() and (self._track != None) and (_nValue == 127)):
      self._track.mixer_device.volume.value = self.m_aVolMap[_nIdx]

  # **************************************************************************

  def _on_deck_value(self, _nValue):
    assert (self.m_oDeckButton != None)
    assert (_nValue in range(128))
    if (self.is_enabled() and (self._track != None) and (_nValue == 127)):
      nDeck = self._track.mixer_device.crossfade_assign
      nDeck = (nDeck - 1) % 3 # A -> B -> None
      self._track.mixer_device.crossfade_assign = nDeck

  def _on_deck_changed(self):
    if (self.is_enabled() and (self.m_oPanResetButton != None)):
      if self._track != None:
        nDeck = self._track.mixer_device.crossfade_assign
        if (nDeck == 0):
          self.m_oDeckButton.set_light('Mixer.Deck.A')
        elif (nDeck == 1):
          self.m_oDeckButton.set_light('Mixer.Deck.Unsel')
        else:
          self.m_oDeckButton.set_light('Mixer.Deck.B')
      else:
        self.m_oDeckButton.set_light('Mixer.Deck.Unava')

  # **************************************************************************

  def _on_send1_value(self, _nValue):
    self._handle_send_value(_nValue, 0)

  def _on_send2_value(self, _nValue):
    self._handle_send_value(_nValue, 1)

  def _on_send3_value(self, _nValue):
    self._handle_send_value(_nValue, 2)

  def _on_send4_value(self, _nValue):
    self._handle_send_value(_nValue, 3)

  def _on_send5_value(self, _nValue):
    self._handle_send_value(_nValue, 4)

  def _on_send6_value(self, _nValue):
    self._handle_send_value(_nValue, 5)

  def _on_send7_value(self, _nValue):
    self._handle_send_value(_nValue, 6)

  def _on_send8_value(self, _nValue):
    self._handle_send_value(_nValue, 7)

  def _handle_send_value(self, _nValue, _nIdx):
    assert (_nValue in range(128))
    if (self.is_enabled() and (self._track != None) and (_nValue == 127)):
      oSend = self._track.mixer_device.sends[_nIdx]
      if oSend.is_enabled:
        if oSend.value < 0.5:
          oSend.value = 1.0
        else:
          oSend.value = 0.0

  def _on_send1_changed(self):
    self._handle_send_changed(0, self.m_oSend1Button)

  def _on_send2_changed(self):
    self._handle_send_changed(1, self.m_oSend2Button)

  def _on_send3_changed(self):
    self._handle_send_changed(2, self.m_oSend3Button)

  def _on_send4_changed(self):
    self._handle_send_changed(3, self.m_oSend4Button)

  def _on_send5_changed(self):
    self._handle_send_changed(4, self.m_oSend5Button)

  def _on_send6_changed(self):
    self._handle_send_changed(5, self.m_oSend6Button)

  def _on_send7_changed(self):
    self._handle_send_changed(6, self.m_oSend7Button)

  def _on_send8_changed(self):
    self._handle_send_changed(7, self.m_oSend8Button)

  def _handle_send_changed(self, _nIdx, _oButton):
    if (self._track != None):
      aSends = self._track.mixer_device.sends
      if (self.is_enabled() and (_oButton != None)):
        if (aSends[_nIdx].value > 0.5):
          _oButton.turn_on()
        else:
          _oButton.turn_off()
    else:
      if (self.is_enabled() and _oButton != None):
        _oButton.set_light('Mixer.Send.Unava')

  # **************************************************************************

  def _on_view_clip_value(self, _nValue):
    assert (self.m_oViewClipButton != None)
    assert (_nValue in range(128))
    if (self.is_enabled() and (self._track != None) and (_nValue == 127)):
      self.song().view.selected_track = self._track
      oView = self.application().view
      oView.show_view('Detail')
      oView.focus_view('Detail')
      oView.show_view('Detail/Clip')
      oView.focus_view('Detail/Clip')

  def _on_view_clip_changed(self):
    if (self.is_enabled() and (self.m_oViewClipButton != None)):
      if self._track != None:
        self.m_oViewClipButton.turn_on()  # view clip ready to be used!
      else:
        self.m_oViewClipButton.turn_off() # view clip unavailable!

  def _on_view_dev_value(self, _nValue):
    assert (self.m_oViewDevButton != None)
    assert (_nValue in range(128))
    if (self.is_enabled() and (self._track != None) and (_nValue == 127)):
      self.song().view.selected_track = self._track
      oView = self.application().view
      oView.show_view('Detail')
      oView.focus_view('Detail')
      oView.show_view('Detail/DeviceChain')
      oView.focus_view('Detail/DeviceChain')

  def _on_view_dev_changed(self):
    if (self.is_enabled() and (self.m_oViewDevButton != None)):
      if self._track != None:
        self.m_oViewDevButton.turn_on()  # view dev ready to be used!
      else:
        self.m_oViewDevButton.turn_off() # view dev unavailable!

  # **************************************************************************

  def tracks(self):
    return self.song().tracks # visible_tracks

  def get_track_or_none(self, _oControl = None, _nResetValue = None):
    if (not self.is_enabled()):
      # disabled! nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    if (self._track == None):
      # no track! nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    if (self._track == self.song().master_track):
      # is master track, nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    if (not self._track in self.tracks()):
      # is a return track, nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    return self._track

  def send_reset_value(self, _oControl, _nResetValue):
    if (_oControl != None):
      _oControl.send_value(_nResetValue, True)
    return None

  def log(self, _sMessage):
    Live.Base.log(_sMessage)
