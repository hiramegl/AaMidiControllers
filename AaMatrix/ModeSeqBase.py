from .ModeBase import *

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

  def setup_invalid_clip_buttons(self):
    for nPitxIdxRel in self.m_rHeight:
      for nTimeIdxRel in self.m_rWidth:
        oButton = self.get_matrix_button(nPitxIdxRel, nTimeIdxRel)
        oButton.set_on_off_values("SeqBase.Invalid")
        if (self.m_aInvalidPattern[nPitxIdxRel][nTimeIdxRel] == 1):
          oButton.turn_on()
        else:
          oButton.turn_off()

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

  # **************************************************************************

  def send_grid_command(self, _sCmd, _hParams = None):
    self.m_oSelector.send_grid_command(_sCmd, _hParams)

  # **************************************************************************

  def get_matrix_button(self, _nPitxIdxRel, _nTimeIdxRel):
    nRow = self.m_nHeight - _nPitxIdxRel - 1
    nCol = _nTimeIdxRel
    return self.m_oMatrix.get_button(nCol, nRow)
