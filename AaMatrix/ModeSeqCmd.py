from .ModeSeqBase import *

SEQ_CMD_CLIP_STATE_UNDEFINED   = 0
SEQ_CMD_CLIP_STATE_INVALID     = 1
SEQ_CMD_CLIP_STATE_MIDI_EMPTY  = 2
SEQ_CMD_CLIP_STATE_MIDI_READY  = 3
SEQ_CMD_CLIP_STATE_AUDIO_READY = 4

SEQ_SCALE_CHROMATIC = 0

SEQ_ROOT_C = 0

ROW_SCALE_0 = 0
ROW_SCALE_1 = 1
ROW_ROOT_0  = 2
ROW_ROOT_1  = 3
ROW_CMD_ALL = 4
ROW_CMD_SEL = 5
ROW_BIT_CMD = 6
ROW_RHYTHM  = 7

COL_SCALE_MAX   = 5
COL_ROOT_MAX    = 5
COL_TRNSPS      = 6
COL_ZOOM_MODE   = 7
COL_SECTION_1_2 = 6
COL_SECTION_1   = 7
COL_SECTION_2   = 6
COL_SECTION_4   = 7
COL_GRID_SEL_1  = 6
COL_GRID_SEL_2  = 7

COL_PITX_UP = 0
COL_PITX_DW = 1
COL_TIME_LF = 2
COL_TIME_RG = 3
COL_MUL     = 4
COL_DIV     = 5
COL_CH3     = 6
COL_CH2     = 7

BUT_SLIDER_NONE = 3
BUT_SLIDER_VEL  = 0
BUT_SLIDER_LEN  = 1
BUT_SLIDER_SHF  = 2
BUT_SEL_TOG    = 3
BUT_DEL_ALL    = 4
BUT_DEL_SEL    = 5
BUT_MUTE_SEL   = 6
BUT_SOLO_SEL   = 7

BUT_MODE       = 7

MODE_TEMPO     = 0
MODE_SCALE     = 1

class ModeSeqCmd(ModeSeqBase):
  def __init__(self, _oCtrlInst, _hCfg, _oMatrix, _lSide, _lNav):
    super(ModeSeqCmd, self).__init__(_oCtrlInst, _hCfg, _oMatrix, _lSide, _lNav)
    self.m_sNavSkin   = "SeqCmd.Nav"
    self.m_nCurMode   = MODE_TEMPO
    self.m_nClipState = SEQ_CMD_CLIP_STATE_UNDEFINED
    self.m_lMidiTempoSkin  = [
      ['Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  ],
      ['Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Span'   ],
      ['BitLen' , 'BitLen' , 'BitLen' , 'BitLen' , 'BitLen' , 'BitLen' , 'BitLen' , 'BitLen' , 'Section'],
      ['BitVel' , 'BitVel' , 'BitVel' , 'BitVel' , 'BitVel' , 'BitVel' , 'GridSel', 'GridSel', 'Section'],
      ['PitxAll', 'PitxAll', 'TimeAll', 'TimeAll', 'LenAll' , 'LenAll' , 'ChopAll', 'ChopAll', 'Section'],
      ['PitxSel', 'PitxSel', 'TimeSel', 'TimeSel', 'LenSel' , 'LenSel' , 'ChopSel', 'ChopSel', 'Section'],
      ['MuteAll', 'SoloAll', 'VelRAll', 'DelAll' , 'Patt'   , 'Patt'   , 'Patt'   , 'Patt'   , 'Section'],
      ['MuteSel', 'SoloSel', 'VelRSel', 'DelSel' , 'Patt'   , 'Patt'   , 'Patt'   , 'Patt'   , 'Mode'   ],
    ]
    self.m_lMidiScaleSkin = [
      ['Scale'  , 'Scale'  , 'Scale'  , 'Scale'  , 'Scale'  , 'Scale'  , 'Trnsps' , 'ChrdInv', 'Invalid'],
      ['Scale'  , 'Scale'  , 'Scale'  , 'Scale'  , 'Scale'  , 'Scale'  , 'Chord'  , 'ChrdInv', 'Invalid'],
      ['Root'   , 'Root'   , 'Root'   , 'Root'   , 'Root'   , 'Root'   , 'Chord'  , 'ChrdInv', 'Invalid'],
      ['Root'   , 'Root'   , 'Root'   , 'Root'   , 'Root'   , 'Root'   , 'GridSel', 'GridSel', 'SelTog' ],
      ['BitMul' , 'BitMul' , 'BitMul' , 'BitMul' , 'BitMul' , 'BitMul' , 'BitMul' , 'BitMul' , 'Slider' ],
      ['BitDiv' , 'BitDiv' , 'BitDiv' , 'BitDiv' , 'BitDiv' , 'BitDiv' , 'BitDiv' , 'BitDiv' , 'Slider' ],
      ['BitChp3', 'BitChp3', 'BitChp3', 'BitChp3', 'BitChp3', 'BitChp3', 'BitChp3', 'BitChp3', 'Slider' ],
      ['BitChp2', 'BitChp2', 'BitChp2', 'BitChp2', 'BitChp2', 'BitChp2', 'BitChp2', 'BitChp2', 'Mode'   ],
    ]
    self.m_lAudioTempoSkin = [
      ['Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  ],
      ['Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Tempo'  , 'Invalid'],
      ['Transp' , 'Transp' , 'Transp' , 'Transp' , 'Transp' , 'Transp' , 'Transp' , 'Transp' , 'Transp' ],
      ['Transp' , 'Transp' , 'Transp' , 'Transp' , 'Transp' , 'Transp' , 'Transp' , 'Transp' , 'Transp' ],
      ['Transp' , 'Transp' , 'Transp' , 'Transp' , 'Transp' , 'Transp' , 'Transp' , 'Transp' , 'Transp' ],
      ['Detune' , 'Detune' , 'Detune' , 'Detune' , 'Detune' , 'Detune' , 'Detune' , 'Detune' , 'Detune' ],
      ['Gain'   , 'Gain'   , 'Gain'   , 'Gain'   , 'Gain'   , 'Gain'   , 'Gain'   , 'Gain'   , 'Gain'   ],
      ['Invalid', 'Invalid', 'Invalid', 'Invalid', 'Invalid', 'Invalid', 'Invalid', 'Invalid', 'Invalid'],
    ]
    self.m_lScales = [
      'CHROMATIC',
      'IONIAN NATURAL MAJOR' ,
      'IONIAN NATURAL MINOR' ,
      'IONIAN HARMONIC MAJOR',
      'IONIAN HARMONIC MINOR',
      'IONIAN MELODIC MAJOR' ,
      'IONIAN MELODIC MINOR' ,
      'DORIAN'    ,
      'PHRYGIAN'  ,
      'LYDIAN'    ,
      'MYXOLYDIAN',
      'AEOLIAN'   ,
      'LOCRIAN'   ,
    ]
    self.m_lSliderModes = ['VELOCITY', 'LENGTH', 'FINE SHIFT', 'NONE']
    self.m_lCmdNames    = ['pitx_up', 'pitx_dw', 'time_lf', 'time_rg', 'mul', 'div', 'chop_3', 'chop_2']
    self.m_bTransposing = False

    self.m_nScale  = SEQ_SCALE_CHROMATIC
    self.m_nRoot   = SEQ_ROOT_C
    self.m_nGrid   = 1 # use first controller
    self.m_nSlider = BUT_SLIDER_NONE

  def set_active(self, _bActive):
    if _bActive:
      self.m_bInit   = True
      self.m_bActive = True
      self.setup_nav_buttons(True, self.m_sNavSkin)
      self.m_nClipState = self.get_clip_state()
      if self.m_nClipState == SEQ_CMD_CLIP_STATE_INVALID:
        self.setup_invalid_clip_buttons()
        self.setup_invalid_side_buttons()
      elif self.m_nClipState == SEQ_CMD_CLIP_STATE_MIDI_EMPTY:
        self.setup_empty_clip_buttons()
        self.setup_invalid_side_buttons()
      elif self.m_nClipState == SEQ_CMD_CLIP_STATE_MIDI_READY:
        self.log(">> MIDI READY")
        self.setup_midi_ready_buttons()
      elif self.m_nClipState == SEQ_CMD_CLIP_STATE_AUDIO_READY:
        self.log(">> AUDIO READY")
        self.setup_audio_ready_buttons()
    else:
      self.m_bActive = False
      self.setup_nav_buttons(False)
      self.disconnect_clip_listeners()

  def setup_invalid_side_buttons(self):
    for nIdx in range(8):
      self.m_lSide[nIdx].set_light('SeqZoom.None.Off')

  def setup_midi_ready_buttons(self):
    lSkin = self.m_lMidiTempoSkin
    if self.m_nCurMode == MODE_SCALE:
      lSkin = self.m_lMidiScaleSkin

    lStateful = ['GridSel', 'Span', 'Section', 'Scale', 'Root', 'Trnsps', 'Chord', 'ChrdInv']
    for nRow in self.m_rHeight:
      oSide = self.m_lSide[nRow]
      sSkin = lSkin[nRow][8]
      oSide.set_on_off_values("SeqCmd.%s" % (sSkin))
      oSide.turn_on()
      if not sSkin in lStateful:
        oSide.turn_on() # stateless buttons always on
      for nCol in self.m_rWidth:
        oButton = self.m_oMatrix.get_button(nCol, nRow)
        sSkin   = lSkin[nRow][nCol]
        oButton.set_on_off_values("SeqCmd.%s" % (sSkin))
        oButton.turn_on()
        if not sSkin in lStateful:
          oButton.turn_on() # stateless buttons always on
    self.update_stateful_midi_buttons()

  def setup_audio_ready_buttons(self):
    for nRow in self.m_rHeight:
      oSide = self.m_lSide[nRow]
      sSkin = self.m_lAudioTempoSkin[nRow][8]
      oSide.set_on_off_values("SeqCmd.%s" % (sSkin))
      oSide.turn_on() # stateless buttons always on
      for nCol in self.m_rWidth:
        oButton = self.m_oMatrix.get_button(nCol, nRow)
        sSkin   = self.m_lAudioTempoSkin[nRow][nCol]
        oButton.set_on_off_values("SeqCmd.%s" % (sSkin))
        oButton.turn_on() # stateless buttons always on

  def update_stateful_midi_buttons(self):
    self.update_grid_sel_buttons()
  #  self.update_scale_buttons()
  #  self.update_root_buttons()
  #  self.update_transpose_button()
  #  self.update_zoom_mode_button()
  #  self.update_section_mode_buttons()
  #  self.update_grid_cmd_buttons()
  #  self.update_slider_buttons()

  def update_grid_sel_buttons(self):
    if self.m_nGrid == 1:
      self.m_oMatrix.get_button(COL_GRID_SEL_1, ROW_ROOT_1).turn_on()
      self.m_oMatrix.get_button(COL_GRID_SEL_2, ROW_ROOT_1).turn_off()
    else: # self.m_nGrid == 2
      self.m_oMatrix.get_button(COL_GRID_SEL_1, ROW_ROOT_1).turn_off()
      self.m_oMatrix.get_button(COL_GRID_SEL_2, ROW_ROOT_1).turn_on()

  #def update_scale_buttons(self):
  #  for nIdx in range(12):
  #    nRow   = nIdx / 6
  #    nCol   = nIdx % 6
  #    nScale = nIdx + 1
  #    if self.m_nScale == nScale:
  #      self.m_oMatrix.get_button(nCol, nRow).turn_on()
  #    else:
  #      self.m_oMatrix.get_button(nCol, nRow).turn_off()

  #def update_root_buttons(self):
  #  lWhite = [0, 2, 4, 5, 7, 9, 11]
  #  for nIdx in range(12):
  #    nRow = (nIdx / 6) + 2
  #    nCol = nIdx % 6
  #    if self.m_nRoot == nIdx:
  #      self.m_oMatrix.get_button(nCol, nRow).turn_on()
  #    elif nIdx in lWhite:
  #      self.m_oMatrix.get_button(nCol, nRow).set_light('SeqCmd.Root.White')
  #    else:
  #      self.m_oMatrix.get_button(nCol, nRow).set_light('SeqCmd.Root.Black')

  #def update_transpose_button(self):
  #  oBut = self.m_oMatrix.get_button(COL_TRNSPS, ROW_SCALE_0)
  #  if self.m_nScale == SEQ_SCALE_CHROMATIC:
  #    oBut.turn_off()
  #  elif self.m_bTransposing:
  #    oBut.set_light('SeqCmd.Trnsps.Act')
  #  else:
  #    oBut.turn_on()

  #def update_zoom_mode_button(self):
  #  oBut = self.m_oMatrix.get_button(COL_ZOOM_MODE, ROW_SCALE_0)
  #  if self.get_time_zoom_mode() == SEQ_TIME_ZOOM_BAR:
  #    oBut.set_light('SeqCmd.Mode.Bar')
  #  else:
  #    oBut.set_light('SeqCmd.Mode.Phrase')

  #def update_section_mode_buttons(self):
  #  nSectionMode = self.get_section_mode()
  #  if nSectionMode == SEQ_SECTION_MODE_1_2:
  #    self.m_oMatrix.get_button(COL_SECTION_1_2, ROW_SCALE_1).turn_on()
  #    self.m_oMatrix.get_button(COL_SECTION_1  , ROW_SCALE_1).turn_off()
  #    self.m_oMatrix.get_button(COL_SECTION_2  , ROW_ROOT_0 ).turn_off()
  #    self.m_oMatrix.get_button(COL_SECTION_4  , ROW_ROOT_0 ).turn_off()
  #  elif nSectionMode == SEQ_SECTION_MODE_1:
  #    self.m_oMatrix.get_button(COL_SECTION_1_2, ROW_SCALE_1).turn_off()
  #    self.m_oMatrix.get_button(COL_SECTION_1  , ROW_SCALE_1).turn_on()
  #    self.m_oMatrix.get_button(COL_SECTION_2  , ROW_ROOT_0 ).turn_off()
  #    self.m_oMatrix.get_button(COL_SECTION_4  , ROW_ROOT_0 ).turn_off()
  #  elif nSectionMode == SEQ_SECTION_MODE_2:
  #    self.m_oMatrix.get_button(COL_SECTION_1_2, ROW_SCALE_1).turn_off()
  #    self.m_oMatrix.get_button(COL_SECTION_1  , ROW_SCALE_1).turn_off()
  #    self.m_oMatrix.get_button(COL_SECTION_2  , ROW_ROOT_0 ).turn_on()
  #    self.m_oMatrix.get_button(COL_SECTION_4  , ROW_ROOT_0 ).turn_off()
  #  elif nSectionMode == SEQ_SECTION_MODE_4:
  #    self.m_oMatrix.get_button(COL_SECTION_1_2, ROW_SCALE_1).turn_off()
  #    self.m_oMatrix.get_button(COL_SECTION_1  , ROW_SCALE_1).turn_off()
  #    self.m_oMatrix.get_button(COL_SECTION_2  , ROW_ROOT_0 ).turn_off()
  #    self.m_oMatrix.get_button(COL_SECTION_4  , ROW_ROOT_0 ).turn_on()
  #  elif nSectionMode == SEQ_SECTION_MODE_8:
  #    self.m_oMatrix.get_button(COL_SECTION_1_2, ROW_SCALE_1).turn_off()
  #    self.m_oMatrix.get_button(COL_SECTION_1  , ROW_SCALE_1).turn_off()
  #    self.m_oMatrix.get_button(COL_SECTION_2  , ROW_ROOT_0 ).turn_off()
  #    self.m_oMatrix.get_button(COL_SECTION_4  , ROW_ROOT_0 ).turn_off()

  #def update_slider_buttons(self):
  #  for nIdx in range(BUT_SLIDER_SHF + 1):
  #    if nIdx == self.m_nSlider:
  #      self.m_lSide[nIdx].turn_on()
  #    else:
  #      self.m_lSide[nIdx].turn_off()

  # **************************************************************************

  def side_cmd(self, _oButton, _nIdx, _nValue):
    if _nValue == BUTTON_OFF: return

    if self.m_nClipState == SEQ_CMD_CLIP_STATE_MIDI_READY:
      if _nIdx == BUT_MODE:
        self.set_active(False)
        if self.m_nCurMode == MODE_TEMPO:
          self.m_nCurMode = MODE_SCALE
        else:
          self.m_nCurMode = MODE_TEMPO
        self.set_active(True)
        return

    elif self.m_nClipState == SEQ_CMD_CLIP_STATE_AUDIO_READY:
      return

    #if _nIdx <= BUT_SLIDER_SHF:
    #  if _nIdx == BUT_SLIDER_VEL:
    #    if self.m_nSlider == BUT_SLIDER_VEL:
    #      self.m_nSlider = BUT_SLIDER_NONE
    #    else:
    #      self.m_nSlider = BUT_SLIDER_VEL
    #  elif _nIdx == BUT_SLIDER_LEN:
    #    if self.m_nSlider == BUT_SLIDER_LEN:
    #      self.m_nSlider = BUT_SLIDER_NONE
    #    else:
    #      self.m_nSlider = BUT_SLIDER_LEN
    #  elif _nIdx == BUT_SLIDER_SHF:
    #    if self.m_nSlider == BUT_SLIDER_SHF:
    #      self.m_nSlider = BUT_SLIDER_NONE
    #    else:
    #      self.m_nSlider = BUT_SLIDER_SHF
    #  self.alert('SLIDER MODE: %s' % (self.m_lSliderModes[self.m_nSlider]))
    #  self.update_slider_buttons()
    #  self.send_grid_command('slider_mode', {
    #    'slider_mode_index': self.m_nSlider
    #  })
    #elif _nIdx == BUT_SEL_TOG:
    #  self.send_grid_command('select_toggle')
    #elif _nIdx == BUT_DEL_ALL:
    #  self.send_grid_command('grid_cmd', {
    #    'grid'  : self.m_nGrid,
    #    'subcmd': 'delete',
    #    'mode'  : 'all',
    #  })
    #elif _nIdx == BUT_DEL_SEL:
    #  self.send_grid_command('grid_cmd', {
    #    'grid'  : self.m_nGrid,
    #    'subcmd': 'delete',
    #    'mode'  : 'sel',
    #  })
    #elif _nIdx == BUT_MUTE_SEL:
    #  self.send_grid_command('grid_cmd', {
    #    'grid'  : self.m_nGrid,
    #    'subcmd': 'mute',
    #    'mode'  : 'sel',
    #  })
    #elif _nIdx == BUT_SOLO_SEL:
    #  self.send_grid_command('grid_cmd', {
    #    'grid'  : self.m_nGrid,
    #    'subcmd': 'solo',
    #    'mode'  : 'sel',
    #  })

  def grid_cmd(self, _oButton, _nCol, _nRow, _nValue):
    if _nValue == BUTTON_OFF: return

    #if _nRow == ROW_SCALE_0:
    #  if _nCol <= COL_SCALE_MAX:
    #    self.select_scale(_nCol + 1, True)
    #  elif _nCol == COL_TRNSPS:
    #    if self.m_nScale == SEQ_SCALE_CHROMATIC:
    #      self.alert('TRANSPOSE UNAVAILABLE. SELECT A SCALE FIRST.')
    #      return
    #    elif not self.m_bTransposing: # starting transpose
    #      self.send_grid_command('transpose_scale', {
    #        'subcmd': 'source',
    #      })
    #      self.m_bTransposing = True
    #    else:
    #      self.send_grid_command('transpose_scale', {
    #        'subcmd': 'cancel',
    #      })
    #      self.m_bTransposing = False
    #    self.update_transpose_button()
    #  elif _nCol == COL_ZOOM_MODE:
    #    nZoomMode = SEQ_TIME_ZOOM_PHRASE if self.get_time_zoom_mode() == SEQ_TIME_ZOOM_BAR else SEQ_TIME_ZOOM_BAR
    #    self.toggle_zoom_mode(nZoomMode, True)

    #elif _nRow == ROW_SCALE_1:
    #  if _nCol <= COL_SCALE_MAX:
    #    self.select_scale(_nCol + 7, True)
    #  elif _nCol == COL_SECTION_1_2:
    #    self.select_section_mode(SEQ_SECTION_MODE_1_2, True)
    #  elif _nCol == COL_SECTION_1:
    #    self.select_section_mode(SEQ_SECTION_MODE_1, True)

    #elif _nRow == ROW_ROOT_0:
    #  if _nCol <= COL_ROOT_MAX:
    #    self.select_root(_nCol, True)
    #  elif _nCol == COL_SECTION_2:
    #    self.select_section_mode(SEQ_SECTION_MODE_2, True)
    #  elif _nCol == COL_SECTION_4:
    #    self.select_section_mode(SEQ_SECTION_MODE_4, True)

    if _nRow == ROW_ROOT_1:
      #if _nCol <= COL_ROOT_MAX:
      #  self.select_root(_nCol + 6, True)
      if _nCol == COL_GRID_SEL_1:
        if self.m_nGrid == 1: return
        self.m_nGrid = 1
        self.alert('> GRID: 1')
        self.update_grid_sel_buttons()
      elif _nCol == COL_GRID_SEL_2:
        if self.m_nGrid == 2: return
        self.m_nGrid = 2
        self.alert('> GRID: 2')
        self.update_grid_sel_buttons()

    #elif _nRow == ROW_CMD_ALL:
    #  self.send_grid_command('grid_cmd', {
    #    'grid'  : self.m_nGrid,
    #    'subcmd': self.m_lCmdNames[_nCol],
    #    'mode'  : 'all',
    #  })

    #elif _nRow == ROW_CMD_SEL:
    #  if _nCol <= COL_TIME_RG:
    #    self.send_grid_command('grid_cmd', {
    #      'grid'  : self.m_nGrid,
    #      'subcmd': self.m_lCmdNames[_nCol],
    #      'mode'  : 'sel',
    #    })

    #elif _nRow == ROW_BIT_CMD:
    #  self.send_grid_command('bit_cmd', {
    #    'grid'  : self.m_nGrid,
    #    'subcmd': self.m_lCmdNames[self.m_nCmd],
    #    'index' : _nCol,
    #  })

    #elif _nRow == ROW_RHYTHM:
    #  self.send_grid_command('apply_rhythm', {'pattern_index': _nCol})

  #def select_scale(self, _nScale, _bLocal):
  #  self.m_nScale = SEQ_SCALE_CHROMATIC if _nScale == self.m_nScale else _nScale
  #  self.update_scale_buttons()
  #  if _bLocal:
  #    if not self.m_bTransposing:
  #      self.send_grid_command('sel_scale', {'scale_idx': self.m_nScale})
  #      self.alert('SCALE: "%s"' % (self.m_lScales[self.m_nScale]))
  #    else:
  #      self.send_grid_command('transpose_scale', {
  #        'subcmd': 'target',
  #        'scale' : self.m_nScale,
  #      })
  #      self.m_bTransposing = False
  #  self.update_transpose_button()

  #def select_root(self, _nRoot, _bLocal):
  #  if self.m_nRoot == _nRoot: return
  #  self.m_nRoot = _nRoot
  #  self.update_root_buttons()
  #  if _bLocal:
  #    self.send_grid_command('sel_root', {'root_idx': self.m_nRoot})

  #def toggle_zoom_mode(self, _nZoomMode, _bLocal):
  #  self.set_time_zoom_mode(_nZoomMode)
  #  self.update_zoom_mode_button()
  #  if _bLocal:
  #    self.send_grid_command('zoom_mode', {'new_zoom_mode': _nZoomMode})

  #def select_section_mode(self, _nSectionMode, _bLocal):
  #  self.set_section_mode(_nSectionMode)
  #  self.alert('SECTION MODE: %s' % (self.m_aSectionModes[self.get_section_mode()]))
  #  self.update_section_mode_buttons()
  #  if _bLocal:
  #    self.send_grid_command('section_mode', {'section_mode_index': self.get_section_mode()})

  # **************************************************************************

  def receive_grid_command(self, _hCmd):
    return

  # **************************************************************************

  def update_stateful_controls(self):
    return

  # ****************************************************************************

  def get_clip_state(self):
    self.m_oMidiSlot  = self.get_midi_slot_or_none()
    self.m_oAudioSlot = self.get_audio_slot_or_none()

    if self.m_oMidiSlot != None:
      if not self.m_oMidiSlot.has_clip_has_listener(self._on_clip_changed):
        self.m_oMidiSlot.add_has_clip_listener(self._on_clip_changed)

      self.m_oClip  = self.get_midi_clip_or_none()
      self.m_oTrack = self.get_midi_track_or_none()
      if self.m_oClip == None:
        if self.m_oTrack == None:
          return SEQ_CMD_CLIP_STATE_INVALID # No MIDI track
        else:
          return SEQ_CMD_CLIP_STATE_MIDI_EMPTY # No MIDI Clip but MIDI Track

      if not self.m_oClip.notes_has_listener(self._on_clip_notes_changed):
        self.m_oClip.add_notes_listener(self._on_clip_notes_changed)
      if not self.m_oClip.loop_start_has_listener(self._on_clip_length_changed):
        self.m_oClip.add_loop_start_listener(self._on_clip_length_changed)
      if not self.m_oClip.loop_end_has_listener(self._on_clip_length_changed):
        self.m_oClip.add_loop_end_listener(self._on_clip_length_changed)

      nClipLen = int(self.m_oClip.loop_end - self.m_oClip.loop_start)
      if self.m_nTimeOffAbs >= nClipLen:
        self.m_nTimeOffAbs = 0
      return SEQ_CMD_CLIP_STATE_MIDI_READY # MIDI Clip and MIDI Track

    if self.m_oAudioSlot != None:
      self.m_oClip  = self.get_audio_clip_or_none()
      if self.m_oClip == None:
        return SEQ_CMD_CLIP_STATE_INVALID # No Audio track

      return SEQ_CMD_CLIP_STATE_AUDIO_READY # Audio track

    return SEQ_CMD_CLIP_STATE_INVALID # No Audio track

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
    if self.m_nClipState == SEQ_CMD_CLIP_STATE_MIDI_READY:
      self.on_clip_notes_changed()

  def _on_clip_length_changed(self):
    if self.m_nClipState == SEQ_CMD_CLIP_STATE_MIDI_READY:
      self.on_clip_notes_changed()

  def on_clip_notes_changed(self):
    return
