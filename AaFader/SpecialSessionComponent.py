import Live

from _Framework.SessionComponent import SessionComponent
from _Framework.ButtonElement import ButtonElement

def release_control(control):
  if control != None:
    control.release_parameter()

class SpecialSessionComponent(SessionComponent):
  "Special Session Component"
  __module__ = __name__

  def __init__(self, _nNumTracks, _nNumScenes):
    SessionComponent.__init__(self, _nNumTracks, _nNumScenes)
    self._slot_launch_button = None

    self.m_nTempo1 = 0
    self.m_nTempo2 = 0
    self.m_oTempo1Control      = None
    self.m_oTempo1RstControl   = None
    self.m_oTempo2Control      = None
    self.m_oTempo2RstControl   = None
    self.m_oTrackSelControl    = None
    self.m_oTrackSelRstControl = None
    self.m_oSceneSelControl    = None
    self.m_oSceneSelRstControl = None
    self.m_oTrackPanControl    = None
    self.m_oTrackPanRstControl = None
    self.m_oClipGainControl    = None
    self.m_oClipGainRstControl = None
    self.m_oClipPitControl     = None
    self.m_oClipPitRstControl  = None
    self.m_oClipDetControl     = None
    self.m_oClipDetRstControl  = None

    def make_control_slot(name):
      return self.register_slot(None, getattr(self, u'_%s_value' % name), u'value')

    self._tempo_1_control_slot       = make_control_slot(u'tempo_1')
    self._tempo_1_rst_control_slot   = make_control_slot(u'tempo_1_rst')
    self._tempo_2_control_slot       = make_control_slot(u'tempo_2')
    self._tempo_2_rst_control_slot   = make_control_slot(u'tempo_2_rst')
    self._track_sel_control_slot     = make_control_slot(u'track_sel')
    self._track_sel_rst_control_slot = make_control_slot(u'track_sel_rst')
    self._scene_sel_control_slot     = make_control_slot(u'scene_sel')
    self._scene_sel_rst_control_slot = make_control_slot(u'scene_sel_rst')
    self._track_pan_control_slot     = make_control_slot(u'track_pan')
    self._track_pan_rst_control_slot = make_control_slot(u'track_pan_rst')
    self._clip_gain_control_slot     = make_control_slot(u'clip_gain')
    self._clip_gain_rst_control_slot = make_control_slot(u'clip_gain_rst')
    self._clip_pit_control_slot      = make_control_slot(u'clip_pit')
    self._clip_pit_rst_control_slot  = make_control_slot(u'clip_pit_rst')
    self._clip_det_control_slot      = make_control_slot(u'clip_det')
    self._clip_det_rst_control_slot  = make_control_slot(u'clip_det_rst')

  def disconnect(self):
    SessionComponent.disconnect(self)
    if (self._slot_launch_button != None):
      self._slot_launch_button.remove_value_listener(self._slot_launch_value)
      self._slot_launch_button = None

    self.m_oTempo1Control      = None
    self.m_oTempo1RstControl   = None
    self.m_oTempo2Control      = None
    self.m_oTempo2RstControl   = None
    self.m_oTrackSelControl    = None
    self.m_oTrackSelRstControl = None
    self.m_oSceneSelControl    = None
    self.m_oSceneSelRstControl = None
    self.m_oTrackPanControl    = None
    self.m_oTrackPanRstControl = None
    self.m_oClipGainControl    = None
    self.m_oClipGainRstControl = None
    self.m_oClipPitControl     = None
    self.m_oClipPitRstControl  = None
    self.m_oClipDetControl     = None
    self.m_oClipDetRstControl  = None

  def link_with_track_offset(self, track_offset, scene_offset):
    assert (track_offset >= 0)
    assert (scene_offset >= 0)
    if self._is_linked():
      self._unlink()
    self.set_offsets(track_offset, scene_offset)
    self._link()

  def unlink(self):
    if self._is_linked():
      self._unlink()

  def set_slot_launch_button(self, button):
    assert ((button == None) or isinstance(button, ButtonElement))
    if (self._slot_launch_button != button):
      if (self._slot_launch_button != None):
        self._slot_launch_button.remove_value_listener(self._slot_launch_value)
      self._slot_launch_button = button
      if (self._slot_launch_button != None):
        self._slot_launch_button.add_value_listener(self._slot_launch_value)
      self.update()

  def _slot_launch_value(self, value):
    assert (value in range(128))
    assert (self._slot_launch_button != None)
    if self.is_enabled():
      if ((value != 0) or (not self._slot_launch_button.is_momentary())):
        if (self.song().view.highlighted_clip_slot != None):
          self.song().view.highlighted_clip_slot.fire()

  def _scroll_page_left(self):
    SessionComponent._scroll_page_left(self)
    self._update_paging_controls()

  def _scroll_page_right(self):
    SessionComponent._scroll_page_right(self)
    self._update_paging_controls()

  def _update_paging_controls(self):
    nLeftValue  = 127 if self._can_scroll_page_left()  else 0
    nRightValue = 127 if self._can_scroll_page_right() else 0
    self._page_left_button.send_value(nLeftValue, True)
    self._page_right_button.send_value(nRightValue, True)

  def send_bank_values(self, _nIdx):
    if _nIdx > 3: return
    self._on_tempo_1_change()
    self._on_tempo_2_change()
    self._on_track_sel_change()
    self._on_scene_sel_change()
    self._on_track_pan_change()
    self._on_clip_gain_change()
    self._on_clip_pit_change()
    self._on_clip_det_change()

  def on_sel_track_change(self):
    self._on_track_pan_change()
    self._on_clip_gain_change()
    self._on_clip_pit_change()
    self._on_clip_det_change()

  def on_sel_scene_change(self):
    self._on_track_pan_change()
    self._on_clip_gain_change()
    self._on_clip_pit_change()
    self._on_clip_det_change()

  # TEMPO 1 ******************************************************************

  def set_tempo_1(self, _oControl):
    if _oControl != self.m_oTempo1Control:
      release_control(self.m_oTempo1Control)
      self.m_oTempo1Control = _oControl
      self._tempo_1_control_slot.subject = _oControl
      self._on_tempo_1_change()

  def _tempo_1_value(self, _nValue):
    assert self.m_oTempo1Control != None
    assert isinstance(_nValue, int)
    self.m_nTempo1 = _nValue
    self.song().tempo = 20 + self.m_nTempo2 + _nValue

  def _on_tempo_1_change(self):
    # compute the value for tempo 1 (main tempo)
    nTempo = self.song().tempo
    self.m_nTempo1 = nTempo - 20
    if self.m_nTempo1 > 127:
      self.m_nTempo1 = 127
    self.m_oTempo1Control.send_value(self.m_nTempo1, True)

  # TEMPO 1 RESET ************************************************************

  def set_tempo_1_rst(self, _oControl):
    if _oControl != self.m_oTempo1RstControl:
      release_control(self.m_oTempo1RstControl)
      self.m_oTempo1RstControl = _oControl
      self._tempo_1_rst_control_slot.subject = _oControl
      self.update()

  def _tempo_1_rst_value(self, _nValue):
    assert self.m_oTempo1RstControl != None
    assert isinstance(_nValue, int)
    self.m_nTempo1Rst = 108
    self.song().tempo = 20 + self.m_nTempo2 + 108
    self.m_oTempo1Control.send_value(108, True)

  # TEMPO 2 ******************************************************************

  def set_tempo_2(self, _oControl):
    if _oControl != self.m_oTempo2Control:
      release_control(self.m_oTempo2Control)
      self.m_oTempo2Control = _oControl
      self._tempo_2_control_slot.subject = _oControl
      self._on_tempo_2_change()

  def _tempo_2_value(self, _nValue):
    assert self.m_oTempo2Control != None
    assert isinstance(_nValue, int)
    self.m_nTempo2 = _nValue
    self.song().tempo = 20 + self.m_nTempo1 + _nValue

  def _on_tempo_2_change(self):
    # compute the value for tempo 2 (extra tempo)
    nTempo = self.song().tempo
    self.m_nTempo2 = nTempo - 20 - 127
    if self.m_nTempo2 < 0:
      self.m_nTempo2 = 0
    self.m_oTempo2Control.send_value(self.m_nTempo2, True)

  # TEMPO 2 RESET ************************************************************

  def set_tempo_2_rst(self, _oControl):
    if _oControl != self.m_oTempo2RstControl:
      release_control(self.m_oTempo2RstControl)
      self.m_oTempo2RstControl = _oControl
      self._tempo_2_rst_control_slot.subject = _oControl
      self.update()

  def _tempo_2_rst_value(self, _nValue):
    assert self.m_oTempo2RstControl != None
    assert isinstance(_nValue, int)
    self.m_nTempo2Rst = 0
    self.song().tempo = 20 + self.m_nTempo1 + 0
    self.m_oTempo2Control.send_value(0, True)

  # TRACK SEL ****************************************************************

  def set_track_sel(self, _oControl):
    if _oControl != self.m_oTrackSelControl:
      release_control(self.m_oTrackSelControl)
      self.m_oTrackSelControl = _oControl
      self._track_sel_control_slot.subject = _oControl
      self._on_track_sel_change()

  def _track_sel_value(self, _nValue):
    assert self.m_oTrackSelControl != None
    assert isinstance(_nValue, int)
    oTrack = self.get_track(_nValue)
    if oTrack != None:
      self.sel_track(oTrack)

  def _on_track_sel_change(self):
    # find the index of the selected track
    nSelTrackIdx = self.sel_track_idx_abs()
    self.m_oTrackSelControl.send_value(nSelTrackIdx, True)

  # TRACK SEL RESET **********************************************************

  def set_track_sel_rst(self, _oControl):
    if _oControl != self.m_oTrackSelRstControl:
      release_control(self.m_oTrackSelRstControl)
      self.m_oTrackSelRstControl = _oControl
      self._track_sel_rst_control_slot.subject = _oControl
      self.update()

  def _track_sel_rst_value(self, _nValue):
    assert self.m_oTrackSelRstControl != None
    assert isinstance(_nValue, int)
    oTrack = self.get_track(0)
    if oTrack != None:
      self.sel_track(oTrack)
      self.m_oTrackSelControl.send_value(0, True)

  # SCENE SEL ****************************************************************

  def set_scene_sel(self, _oControl):
    if _oControl != self.m_oSceneSelControl:
      release_control(self.m_oSceneSelControl)
      self.m_oSceneSelControl = _oControl
      self._scene_sel_control_slot.subject = _oControl
      self._on_scene_sel_change()

  def _scene_sel_value(self, _nValue):
    assert self.m_oSceneSelControl != None
    assert isinstance(_nValue, int)
    oScene = self.get_scene(_nValue)
    if oScene != None:
      self.sel_scene(oScene)

  def _on_scene_sel_change(self):
    # find the index of the selected Scene
    nSelSceneIdx = self.sel_scene_idx_abs()
    self.m_oSceneSelControl.send_value(nSelSceneIdx, True)

  # SCENE SEL RESET **********************************************************

  def set_scene_sel_rst(self, _oControl):
    if _oControl != self.m_oSceneSelRstControl:
      release_control(self.m_oSceneSelRstControl)
      self.m_oSceneSelRstControl = _oControl
      self._scene_sel_rst_control_slot.subject = _oControl
      self.update()

  def _scene_sel_rst_value(self, _nValue):
    assert self.m_oSceneSelRstControl != None
    assert isinstance(_nValue, int)
    oScene = self.get_scene(0)
    if oScene != None:
      self.sel_scene(oScene)
      self.m_oSceneSelControl.send_value(0, True)

  # TRACK PAN ****************************************************************

  def set_track_pan(self, _oControl):
    if _oControl != self.m_oTrackPanControl:
      release_control(self.m_oTrackPanControl)
      self.m_oTrackPanControl = _oControl
      self._track_pan_control_slot.subject = _oControl

      oPanning = self.song().view.selected_track.mixer_device.panning
      self.m_oTrackPanControl.connect_to(oPanning)
      self.update()

  def _track_pan_value(self, _nValue):
    assert isinstance(_nValue, int)
    # should not do anything

  def _on_track_pan_change(self):
    if self.m_oTrackPanControl != None:
      self.m_oTrackPanControl.release_parameter()
      oPanning = self.song().view.selected_track.mixer_device.panning
      self.m_oTrackPanControl.connect_to(oPanning)

  # TRACK PAN RESET **********************************************************

  def set_track_pan_rst(self, _oControl):
    if _oControl != self.m_oTrackPanRstControl:
      release_control(self.m_oTrackPanRstControl)
      self.m_oTrackPanRstControl = _oControl
      self._track_pan_rst_control_slot.subject = _oControl
      self.update()

  def _track_pan_rst_value(self, _nValue):
    assert self.m_oTrackPanRstControl != None
    assert isinstance(_nValue, int)
    self.song().view.selected_track.mixer_device.panning.value = 0

  # CLIP GAIN ****************************************************************

  def set_clip_gain(self, _oControl):
    if _oControl != self.m_oClipGainControl:
      release_control(self.m_oClipGainControl)
      self.m_oClipGainControl = _oControl
      self._clip_gain_control_slot.subject = _oControl
      self._on_clip_gain_change()
      self.update()

  def _clip_gain_value(self, _nValue):
    assert self.m_oClipGainControl != None
    assert isinstance(_nValue, int)
    oClipSlot = self.sel_clip_slot_or_none()
    if (oClipSlot == None):
      self.m_oClipGainControl.send_value(0, True)
      return
    oClip = oClipSlot.clip
    if (oClip == None):
      self.m_oClipGainControl.send_value(0, True)
      return
    oClip.gain = float(_nValue) / 127.0

  def _on_clip_gain_change(self):
    assert self.m_oClipGainControl != None
    oClipSlot = self.sel_clip_slot_or_none()
    if oClipSlot == None:
      self.m_oClipGainControl.send_value(0, True)
      return
    oClip = oClipSlot.clip
    if oClip == None:
      self.m_oClipGainControl.send_value(0, True)
      return
    if oClip.is_audio_clip == False:
      self.m_oClipGainControl.send_value(0, True)
      return
    nValue = int(oClip.gain * 127.0)
    self.m_oClipGainControl.send_value(nValue, True)

  # CLIP GAIN RESET **********************************************************

  def set_clip_gain_rst(self, _oControl):
    if _oControl != self.m_oClipGainRstControl:
      release_control(self.m_oClipGainRstControl)
      self.m_oClipGainRstControl = _oControl
      self._clip_gain_rst_control_slot.subject = _oControl
      self.update()

  def _clip_gain_rst_value(self, _nValue):
    assert self.m_oClipGainRstControl != None
    assert isinstance(_nValue, int)
    oClipSlot = self.sel_clip_slot_or_none()
    if oClipSlot == None: return
    oClip = oClipSlot.clip
    if oClip == None: return
    if oClip.is_audio_clip == False: return
    oClip.gain = 0.85

  # CLIP PITCH ***************************************************************

  def set_clip_pit(self, _oControl):
    if _oControl != self.m_oClipPitControl:
      release_control(self.m_oClipPitControl)
      self.m_oClipPitControl = _oControl
      self._clip_pit_control_slot.subject = _oControl
      self._on_clip_pit_change()
      self.update()

  def _clip_pit_value(self, _nValue):
    assert self.m_oClipPitControl != None
    assert isinstance(_nValue, int)
    oClip = self.get_clip_or_none()
    if (oClip == None):
      return
    if (oClip.is_audio_clip):
      fValue = float(_nValue) - 64.0
      fPitch = fValue / 1.3 # coarse pitch, 128 / 97 ~= 1.3
      nPitch = int(fPitch)
      nPitch = -48 if nPitch < -48 else nPitch
      oClip.pitch_coarse = nPitch
    else:
      oTrack = self.get_track_or_none()
      if oTrack == None:
        return
      aDevices = oTrack.devices
      for nDevIdx in range(len(aDevices)):
        oDevice = aDevices[nDevIdx]
        sClass  = oDevice.class_name
        if (sClass != 'MidiPitcher'):
          continue
        aParams = oDevice.parameters
        for nPrmIdx  in range(len(aParams)):
          oParam = aParams[nPrmIdx]
          if (oParam.name != 'Pitch'):
            continue
          nPitch = _nValue - 64
          nPitch = -64 if nPitch < -64 else nPitch
          nPitch = 63  if nPitch > 63  else nPitch
          oParam.value = nPitch

  def _on_clip_pit_change(self):
    assert self.m_oClipPitControl != None
    oClip = self.get_clip_or_none(self.m_oClipPitControl, 64)
    if (oClip == None or self.m_oClipPitControl == None):
      return
    nValue = 64
    if (oClip.is_audio_clip):
      nPitch = oClip.pitch_coarse
      fValue = float(nPitch) * 1.3 + 64.0
      nValue = int(fValue)
    else:
      oTrack = self.get_track_or_none()
      if oTrack == None:
        return
      aDevices = oTrack.devices
      for nDevIdx in range(len(aDevices)):
        oDevice = aDevices[nDevIdx]
        sClass  = oDevice.class_name
        if (sClass != 'MidiPitcher'):
          continue
        aParams = oDevice.parameters
        for nPrmIdx  in range(len(aParams)):
          oParam = aParams[nPrmIdx]
          if (oParam.name != 'Pitch'):
            continue
          nValue = oParam.value + 64

    nValue = 0   if nValue < 0   else nValue
    nValue = 127 if nValue > 127 else nValue
    self.m_oClipPitControl.send_value(nValue, True)

  # CLIP PITCH RESET *********************************************************

  def set_clip_pit_rst(self, _oControl):
    if _oControl != self.m_oClipPitRstControl:
      release_control(self.m_oClipPitRstControl)
      self.m_oClipPitRstControl = _oControl
      self._clip_pit_rst_control_slot.subject = _oControl
      self.update()

  def _clip_pit_rst_value(self, _nValue):
    assert self.m_oClipPitRstControl != None
    assert isinstance(_nValue, int)
    oClip = self.get_clip_or_none()
    if (oClip == None):
      return
    if (oClip.is_audio_clip):
      oClip.pitch_coarse = 0
    else:
      oTrack = self.get_track_or_none()
      if oTrack == None:
        return
      aDevices = oTrack.devices
      for nDevIdx in range(len(aDevices)):
        oDevice = aDevices[nDevIdx]
        sClass  = oDevice.class_name
        if (sClass != 'MidiPitcher'):
          continue
        aParams = oDevice.parameters
        for nPrmIdx  in range(len(aParams)):
          oParam = aParams[nPrmIdx]
          if (oParam.name == 'Pitch'):
            oParam.value = 0

    # update rotary controller value
    self.m_oClipPitControl.send_value(64, True)

  # CLIP DETUNE **************************************************************

  def set_clip_det(self, _oControl):
    if _oControl != self.m_oClipDetControl:
      release_control(self.m_oClipDetControl)
      self.m_oClipDetControl = _oControl
      self._clip_det_control_slot.subject = _oControl
      self._on_clip_det_change()
      self.update()

  def _clip_det_value(self, _nValue):
    assert self.m_oClipDetControl != None
    assert isinstance(_nValue, int)
    oClip = self.get_clip_or_none()
    if (oClip == None):
      return
    if (oClip.is_audio_clip):
      fValue  = float(_nValue) - 64.0
      fDetune = fValue / 1.28 # fine pitch, 128 / 100
      nDetune = int(fDetune)
      nDetune = -49 if nDetune < -49 else nDetune
      nDetune =  49 if nDetune >  49 else nDetune
      oClip.pitch_fine = nDetune

  def _on_clip_det_change(self):
    assert self.m_oClipDetControl != None
    oClip = self.get_clip_or_none(self.m_oClipDetControl, 64)
    if (oClip == None or self.m_oClipDetControl == None):
      return
    nValue = 64
    if (oClip.is_audio_clip):
      nDetune = oClip.pitch_fine # -49 ... 49
      fValue  = float(nDetune) * 1.28 + 64.0
      nValue  = int(fValue)

    nValue = 1   if nValue < 1   else nValue
    nValue = 127 if nValue > 127 else nValue
    self.m_oClipDetControl.send_value(nValue, True)

  # CLIP DETUNE RESET ********************************************************

  def set_clip_det_rst(self, _oControl):
    if _oControl != self.m_oClipDetRstControl:
      release_control(self.m_oClipDetRstControl)
      self.m_oClipDetRstControl = _oControl
      self._clip_det_rst_control_slot.subject = _oControl
      self.update()

  def _clip_det_rst_value(self, _nValue):
    assert self.m_oClipDetRstControl != None
    assert isinstance(_nValue, int)
    oClip = self.get_clip_or_none()
    if (oClip == None):
      return
    if (oClip.is_audio_clip):
      oClip.pitch_fine = 0

    # update rotary controller value
    self.m_oClipDetControl.send_value(64, True)

  # ****************************************************************

  def sel_clip_slot_or_none(self):
      return self.song().view.highlighted_clip_slot

  def scenes(self):
    return self.song().scenes

  def get_scene(self, _nSceneIdxAbs):
    aScenes = self.scenes()
    if _nSceneIdxAbs < len(aScenes):
      return aScenes[_nSceneIdxAbs]
    return None

  def sel_scene(self, _oScene = None):
    if (_oScene != None):
      self.song().view.selected_scene = _oScene
    return self.song().view.selected_scene

  def sel_scene_idx_abs(self):
    aAllScenes = self.scenes()
    oSelScene  = self.sel_scene()
    return list(aAllScenes).index(oSelScene)

  def tracks(self):
    return self.song().tracks # visible_tracks

  def returns(self):
    return self.song().return_tracks

  def tracks_and_returns(self):
    return tuple(self.tracks()) + tuple(self.returns())

  def get_track(self, _nTrackIdxAbs):
    aTracks = self.tracks()
    if _nTrackIdxAbs < len(aTracks):
      return aTracks[_nTrackIdxAbs]
    return None

  def sel_track(self, _oTrack = None):
    if (_oTrack != None):
      self.song().view.selected_track = _oTrack
    return self.song().view.selected_track

  def sel_track_idx_abs(self):
    aAllTracks = self.tracks_and_returns()
    oSelTrack  = self.sel_track()
    return list(aAllTracks).index(oSelTrack)

  def send_reset_value(self, _oControl, _nResetValue):
    if (_oControl != None):
      _oControl.send_value(_nResetValue, True)
    return None

  def get_track_or_none(self, _oControl = None, _nResetValue = None):
    if (not self.is_enabled()):
      # disabled! nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    oSelTrack = self.sel_track()

    if (oSelTrack == None):
      # no track! nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    if (oSelTrack == self.song().master_track):
      # is master track, nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    if (not oSelTrack in self.tracks()):
      # is a return track, nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    return oSelTrack

  def get_clip_or_none(self, _oControl = None, _nResetValue = None):
    oTrack = self.get_track_or_none(_oControl, _nResetValue)
    if (oTrack == None):
      return None

    nSelSceneIdxAbs = self.sel_scene_idx_abs()
    oClipSlot       = oTrack.clip_slots[nSelSceneIdxAbs]
    if (not oClipSlot.has_clip):
      # empty clip, nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    return oClipSlot.clip

