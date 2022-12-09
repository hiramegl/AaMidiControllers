from _Framework.CompoundComponent import CompoundComponent

BUTTON_OFF = 0
BUTTON_ON  = 127

class ModeBase(CompoundComponent):
  def __init__(self, _oCtrlInst, _hCfg, _oMatrix, _lSide, _lNav):
    super(ModeBase, self).__init__()
    self.m_oCtrlInst = _oCtrlInst
    self.m_hCfg      = _hCfg
    self.m_oMatrix   = _oMatrix
    self.m_lSide     = _lSide
    self.m_lNav      = _lNav
    self.m_nNav      = len(_lNav)
    self.m_nTracks   = _hCfg['NumTracks']
    self.m_nScenes   = _hCfg['NumScenes']
    self.m_nHeight   = _oMatrix.height()
    self.m_nWidth    = _oMatrix.width()
    self.m_rHeight   = range(self.m_nHeight)
    self.m_rWidth    = range(self.m_nWidth)
    self.m_oSession  = _hCfg['oSession']
    self.m_oZooming  = _hCfg['oZooming']
    self.m_oMixer    = _hCfg['oMixer']
    self.m_oTransp   = _hCfg['oTransp']
    self.m_oSelector = _hCfg['oSelector']

  # **************************************************************************

  def setup_nav_buttons(self, _bActive, _sSkin = ""):
    if _bActive:
      for nIdx in range(self.m_nNav):
         oNav = self.m_lNav[nIdx]
         oNav.set_on_off_values(_sSkin)
         oNav.turn_on()
      self.m_oSession.set_select_buttons(self.m_lNav[1], self.m_lNav[0])
      self.m_oMixer.set_select_buttons(self.m_lNav[3], self.m_lNav[2])
    else:
      self.m_oSession.set_select_buttons(None, None)
      self.m_oMixer.set_select_buttons(None, None)

  def change_prev_mode(self):
    return

  # **************************************************************************

  def sel_scene_idx_abs(self):
    aAllScenes = self.scenes()
    oSelScene  = self.sel_scene()
    return list(aAllScenes).index(oSelScene)

  def scenes(self):
    return self.song().scenes

  def sel_scene(self):
    return self.song().view.selected_scene

  def sel_track(self):
    return self.song().view.selected_track

  def sel_clip_slot(self):
    return self.song().view.highlighted_clip_slot

  def get_clip_or_none(self):
    oClipSlot = self.sel_clip_slot()
    if (oClipSlot == None): return None
    return oClipSlot.clip

  # ----------------

  def get_midi_track_or_none(self):
    oTrack = self.sel_track()
    if (oTrack.has_midi_input):
      return oTrack
    return None

  def get_midi_slot_or_none(self):
    oClipSlot = self.sel_clip_slot()
    if (oClipSlot == None): return None
    oTrack = self.sel_track()
    if (oTrack.has_midi_input):
      return oClipSlot
    return None

  def get_midi_clip_or_none(self):
    oClipSlot = self.sel_clip_slot()
    if (oClipSlot == None): return None
    oClip = oClipSlot.clip
    if (oClip == None): return None
    if (not oClip.is_midi_clip): return None
    return oClip

  # ----------------

  def get_audio_track_or_none(self):
    oTrack = self.sel_track()
    if (oTrack.has_audio_input):
      return oTrack
    return None

  def get_audio_slot_or_none(self):
    oClipSlot = self.sel_clip_slot()
    if (oClipSlot == None): return None
    oTrack = self.sel_track()
    if oTrack.has_audio_input:
      return oClipSlot
    return None

  def get_audio_clip_or_none(self):
    oClipSlot = self.sel_clip_slot()
    if (oClipSlot == None): return None
    oClip = oClipSlot.clip
    if (oClip == None): return None
    if oClip.is_midi_clip: return None
    return oClip

  # ****************************************************************************

  def _on_sel_scene_changed(self):
    self.update_stateful_controls()

  def _on_sel_track_changed(self):
    self.update_stateful_controls()

  def update_stateful_controls(self):
    return

  # ****************************************************************************

  def log(self, _sMsg):
    self.m_oCtrlInst.xlog(_sMsg)

  def alert(self, _sMsg):
    self.m_oCtrlInst.alert(_sMsg)
