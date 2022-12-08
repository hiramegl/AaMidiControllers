from .ModeBase import *

SEQ_CLIP_STATE_UNDEFINED = 0
SEQ_CLIP_STATE_INVALID   = 1
SEQ_CLIP_STATE_EMPTY     = 2
SEQ_CLIP_STATE_READY     = 3

LEN_ONE_BAR    = 4
LEN_ONE_PHRASE = 16
LEN_ONE_OCT    = 12

SEQ_INIT_OCTAVE     = 1
SEQ_SCALE_UNDEF     = -1
SEQ_SCALE_CHROMATIC = 0
SEQ_ROOT_C          = 0

SEQ_TIME_ZOOM_BAR    = 0 #  4 beat = 1 bar             (in 2 surfaces)
SEQ_TIME_ZOOM_PHRASE = 1 # 16 beat = 4 bars = 1 phrase (in 2 surfaces)

SEQ_SECTION_MODE_1_2 = 0
SEQ_SECTION_MODE_1   = 1
SEQ_SECTION_MODE_2   = 2
SEQ_SECTION_MODE_4   = 3
SEQ_SECTION_MODE_8   = 4

class ModeSeqBase(ModeBase):
  def __init__(self, _oCtrlInst, _hCfg, _oMatrix, _lSide, _lNav):
    super(ModeSeqBase, self).__init__(_oCtrlInst, _hCfg, _oMatrix, _lSide, _lNav)
    self.m_aInvalidPattern = [ # for audio clips
      [1, 0, 0, 0, 0, 0, 0, 1],
      [0, 1, 0, 0, 0, 0, 1, 0],
      [0, 0, 1, 0, 0, 1, 0, 0],
      [0, 0, 0, 1, 1, 0, 0, 0],
      [0, 0, 0, 1, 1, 0, 0, 0],
      [0, 0, 1, 0, 0, 1, 0, 0],
      [0, 1, 0, 0, 0, 0, 1, 0],
      [1, 0, 0, 0, 0, 0, 0, 1],
    ]
    self.m_aEmptyPattern = [ # for empty midi clips
      [0, 0, 0, 1, 1, 0, 0, 0],
      [0, 0, 0, 1, 1, 0, 0, 0],
      [0, 0, 0, 1, 1, 0, 0, 0],
      [1, 1, 1, 1, 1, 1, 1, 1],
      [1, 1, 1, 1, 1, 1, 1, 1],
      [0, 0, 0, 1, 1, 0, 0, 0],
      [0, 0, 0, 1, 1, 0, 0, 0],
      [0, 0, 0, 1, 1, 0, 0, 0],
    ]
    self.m_nTimeOffAbs   = 0 # Beat mode: 0, 2, 4, 6, 8, 10, 12, 14 / Bar mode: 0, 8
    self.m_bInit         = False
    self.m_bActive       = False
    self.m_aSectionModes = ['1/2', '1', '2', '4', '8']

  # **************************************************************************

  def set_active(self, _bActive):
    if _bActive:
      self.m_bInit   = True
      self.m_bActive = True
      self.setup_nav_buttons(True, self.m_sNavSkin)
      self.m_nClipState = self.get_clip_state()
      if self.m_nClipState == SEQ_CLIP_STATE_INVALID:
        self.setup_invalid_clip_buttons()
        self.setup_invalid_side_buttons()
      elif self.m_nClipState == SEQ_CLIP_STATE_EMPTY:
        self.setup_empty_clip_buttons()
        self.setup_invalid_side_buttons()
      elif self.m_nClipState == SEQ_CLIP_STATE_READY:
        self.setup_ready_buttons()
    else:
      self.m_bActive = False
      self.setup_nav_buttons(False)
      self.disconnect_clip_listeners()

  def setup_invalid_clip_buttons(self):
    for nPitxIdxRel in self.m_rHeight:
      for nTimeIdxRel in self.m_rWidth:
        oButton = self.get_matrix_button(nPitxIdxRel, nTimeIdxRel)
        oButton.set_on_off_values("SeqBase.Invalid")
        if (self.m_aInvalidPattern[nPitxIdxRel][nTimeIdxRel] == 1):
          oButton.turn_on()
        else:
          oButton.turn_off()

  def setup_invalid_side_buttons(self):
    return

  def setup_empty_clip_buttons(self):
    oTrack = self.get_midi_track_or_none()
    for nPitxIdxRel in self.m_rHeight:
      for nTimeIdxRel in self.m_rWidth:
        oButton = self.get_matrix_button(nPitxIdxRel, nTimeIdxRel)
        oButton.set_on_off_values("SeqBase.Empty")
        if (self.m_aEmptyPattern[nPitxIdxRel][nTimeIdxRel] == 1):
          oButton.turn_on()
        else:
          oButton.turn_off()

  def create_empty_midi_clip(self):
    oTrack = self.sel_track()
    if (not oTrack.has_midi_input): return None
    oClipSlot = self.sel_clip_slot()
    if (oClipSlot == None): return None
    if (oClipSlot.has_clip): return None # it should be an empty clip
    nLength = self.get_section_length()
    oClipSlot.create_clip(nLength)

  # **************************************************************************

  def nav_cmd(self, _oButton, _nIdx, _nValue):
    return # handled by the session and mixer components

  # **************************************************************************

  def get_section_length(self):
    nLength = LEN_ONE_BAR if self.get_time_zoom_mode() == SEQ_TIME_ZOOM_BAR else LEN_ONE_PHRASE
    return nLength

  def get_surface_length(self):
    return self.get_section_length() / 2.0

  def get_bit_length(self):
    return self.get_surface_length() / 8.0

  def set_time_zoom_mode(self, _nTimeZoomMode):
    self.m_oSelector.set_time_zoom_mode(_nTimeZoomMode)

  def get_time_zoom_mode(self):
    return self.m_oSelector.get_time_zoom_mode()

  def set_section_mode(self, _nSectionMode):
    self.m_oSelector.set_section_mode(_nSectionMode)

  def get_section_mode(self):
    return self.m_oSelector.get_section_mode()

  # ****************************************************************************

  def get_clip_state(self):
    self.m_oMidiSlot = self.get_midi_slot_or_none()
    if self.m_oMidiSlot != None and not self.m_oMidiSlot.has_clip_has_listener(self._on_clip_changed):
      self.m_oMidiSlot.add_has_clip_listener(self._on_clip_changed)

    self.m_oClip  = self.get_midi_clip_or_none()
    self.m_oTrack = self.get_midi_track_or_none()

    if self.m_oClip == None:
      if self.m_oTrack == None:
        return SEQ_CLIP_STATE_INVALID # No MIDI track
      else:
        return SEQ_CLIP_STATE_EMPTY # No MIDI Clip but MIDI Track

    if not self.m_oClip.notes_has_listener(self._on_clip_notes_changed):
      self.m_oClip.add_notes_listener(self._on_clip_notes_changed)
    if not self.m_oClip.loop_start_has_listener(self._on_clip_length_changed):
      self.m_oClip.add_loop_start_listener(self._on_clip_length_changed)
    if not self.m_oClip.loop_end_has_listener(self._on_clip_length_changed):
      self.m_oClip.add_loop_end_listener(self._on_clip_length_changed)

    nClipLen = int(self.m_oClip.loop_end - self.m_oClip.loop_start)
    if self.m_nTimeOffAbs >= nClipLen:
      self.m_nTimeOffAbs = 0
    return SEQ_CLIP_STATE_READY # MIDI Clip and MIDI Track

  def disconnect_clip_listeners(self):
    if self.m_oMidiSlot != None and self.m_oMidiSlot.has_clip_has_listener(self._on_clip_changed):
      self.m_oMidiSlot.remove_has_clip_listener(self._on_clip_changed)
    if self.m_oClip != None:
      if self.m_oClip.notes_has_listener(self._on_clip_notes_changed):
        self.m_oClip.remove_notes_listener(self._on_clip_notes_changed)
      if self.m_oClip.loop_start_has_listener(self._on_clip_length_changed):
        self.m_oClip.remove_loop_start_listener(self._on_clip_length_changed)
      if self.m_oClip.loop_end_has_listener(self._on_clip_length_changed):
        self.m_oClip.remove_loop_end_listener(self._on_clip_length_changed)

  def _on_clip_changed(self):
    self.update_stateful_controls()

  def _on_clip_notes_changed(self):
    if self.m_nClipState == SEQ_CLIP_STATE_READY:
      self.on_clip_notes_changed()

  def _on_clip_length_changed(self):
    if self.m_nClipState == SEQ_CLIP_STATE_READY:
      self.on_clip_notes_changed()

  def on_clip_notes_changed(self):
    return

  # **************************************************************************

  def send_grid_command(self, _sCmd, _hParams = None):
    self.m_oSelector.send_grid_command(_sCmd, _hParams)

  # **************************************************************************

  def get_matrix_button(self, _nPitxIdxRel, _nTimeIdxRel):
    nRow = self.m_nHeight - _nPitxIdxRel - 1
    nCol = _nTimeIdxRel
    return self.m_oMatrix.get_button(nCol, nRow)
