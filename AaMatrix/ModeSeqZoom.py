from .ModeSeqBase import *

SEQ_ZOOM_MIDI_CLIP_STATE_UNDEFINED = 0
SEQ_ZOOM_MIDI_CLIP_STATE_INVALID   = 1
SEQ_ZOOM_MIDI_CLIP_STATE_EMPTY     = 2
SEQ_ZOOM_MIDI_CLIP_STATE_READY     = 3

BUT_ZOOM_MODE = 0
BUT_SEC_1_2   = 1
BUT_SEC_1     = 2
BUT_SEC_2     = 3
BUT_SEC_4     = 4
BUT_SEC_8     = 5
BUT_LP_SHOW   = 6

BUT_LP_STA_MUL = 0
BUT_LP_STA_DIV = 1
BUT_LP_MID_MUL = 2
BUT_LP_MID_DIV = 3
BUT_LP_END_MUL = 4
BUT_LP_END_DIV = 5
BUT_LP_DUP     = 6

BUT_TOGGLE   = 7

MODE_SECTION = 0
MODE_TOOLS   = 1

class ModeSeqZoom(ModeSeqBase):
  def __init__(self, _oCtrlInst, _hCfg, _oMatrix, _lSide, _lNav):
    super(ModeSeqZoom, self).__init__(_oCtrlInst, _hCfg, _oMatrix, _lSide, _lNav)
    self.m_sNavSkin      = "SeqZoom.Nav"
    self.m_nCurMode      = MODE_SECTION
    self.m_nClipState    = SEQ_ZOOM_MIDI_CLIP_STATE_UNDEFINED
    self.m_nNumSect      = 0 # number of sections to show
    self.m_nCurSect      = 0 # current section
    self.m_nSpnSect      = 0 # section span (depends on the section mode)
    self.m_nPitxOffAbs   = self.get_pitx_offset_abs_for_octave(SEQ_INIT_OCTAVE) # initial octave
    self.m_nScale        = SEQ_SCALE_CHROMATIC
    self.m_nRootPitx     = SEQ_ROOT_C
    self.m_nNoteLength   = 0.25 # 1 BIT = 1/4 BEAT
    self.m_nNoteShift    = 0.0  # Fine time shift 0/16 .. 15/16 of a BIT (0.0625 increments)
    self.m_bNavSync      = True
    self.m_bLpEnvToggle  = True

  def set_active(self, _bActive):
    if _bActive:
      self.m_bInit   = True
      self.m_bActive = True
      self.setup_nav_buttons(True, self.m_sNavSkin)
      self.m_nClipState = self.get_clip_state()
      if self.m_nClipState == SEQ_ZOOM_MIDI_CLIP_STATE_INVALID:
        self.setup_invalid_clip_buttons()
        self.setup_invalid_side_buttons()
      elif self.m_nClipState == SEQ_ZOOM_MIDI_CLIP_STATE_EMPTY:
        self.setup_empty_clip_buttons()
        self.setup_invalid_side_buttons()
      elif self.m_nClipState == SEQ_ZOOM_MIDI_CLIP_STATE_READY:
        self.setup_ready_buttons()
    else:
      self.m_bActive = False
      self.setup_nav_buttons(False)
      self.disconnect_clip_listeners()

  def setup_invalid_side_buttons(self):
    for nIdx in range(8):
      self.m_lSide[nIdx].set_light('SeqZoom.Invalid.Off')

  def on_clip_notes_changed(self):
    self.update_zoom_buttons()

  def setup_ready_buttons(self):
    self.update_side_buttons()
    self.update_zoom_buttons()

  def update_zoom_buttons(self):
    if not self.m_bActive: return

    self.compute_section_values()
    nTimeDelta = self.get_section_length() # in [beats]
    #  4 beats = 1 bar       (in 2 surfaces)
    # 16 beats = 4 bars = 1 phrase (in 2 surfaces)

    # find out which zoom blocks have notes
    aNotes = self.get_clip_notes()
    hNonEmptyBlocks = {}
    for tNote in aNotes:
      # tNote format: Note, Time, Length, Velocity, Mute
      nPitxIdxAbs = tNote[0] # Note value, between 0 and 127
      nTimeIdxAbs = tNote[1] # Time

      # discard non-visible notes
      if self.m_nScale != SEQ_SCALE_CHROMATIC:
        # in non-chromatic scale we need to discard all notes
        # below the root pitch of the octave -2 (midi 0 .. 12)
        if nPitxIdxAbs < self.m_nRootPitx:
          continue # non-visible note (is lower than the root note)
        if nPitxIdxAbs > (LEN_ONE_OCT * self.m_nHeight + self.m_nRootPitx):
          continue # non-visible note (is higher than the highest visible octave)
      else:
        if nPitxIdxAbs > (LEN_ONE_OCT * self.m_nHeight):
          continue # non-visible note (is higher than the highest visible octave)

      if nTimeIdxAbs < 0:
        continue # non-visible note (is located in negative time)

      if self.m_nScale != SEQ_SCALE_CHROMATIC:
        nZoomRow = nPitxIdxAbs / LEN_ONE_OCT
      else:
        nZoomRow = (nPitxIdxAbs - self.m_nRootPitx) / LEN_ONE_OCT
      nZoomCol = nTimeIdxAbs / nTimeDelta

      sKey = '%d_%d' % (nZoomRow, nZoomCol)
      hNonEmptyBlocks[sKey] = True

    # compute the current block zoom coords
    if self.m_nScale != SEQ_SCALE_CHROMATIC:
      nCurZoomRow = self.m_nPitxOffAbs / LEN_ONE_OCT
    else:
      nCurZoomRow = (self.m_nPitxOffAbs - self.m_nRootPitx) / LEN_ONE_OCT
    nCurZoomCol = self.m_nTimeOffAbs / nTimeDelta
    nMaxSpanCol = (self.m_nTimeOffAbs + (self.m_nSpnSect * nTimeDelta)) / nTimeDelta

    # compute number of visible zoom columns
    nTimeStart   = self.m_oClip.loop_start
    nTimeEnd     = self.m_oClip.loop_end
    nTimeSpan    = int(nTimeEnd - nTimeStart) # in [beats]
    nVisZoomCols = nTimeSpan / nTimeDelta
    if (nTimeSpan % nTimeDelta) != 0:
      nVisZoomCols += 1

    # now actually draw the buttons with the right colors
    for nPitxIdxRel in self.m_rHeight:
      for nTimeIdxRel in self.m_rWidth:
        oButton = self.get_matrix_button(nPitxIdxRel, nTimeIdxRel)
        if nTimeIdxRel >= nVisZoomCols:
          oButton.set_light('SeqZoom.Zoom.Unav')
          continue

        if nTimeIdxRel == nCurZoomCol and nPitxIdxRel == nCurZoomRow:
          oButton.set_light('SeqZoom.Zoom.Selected')
          continue

        sKey = '%d_%d' % (nPitxIdxRel, nTimeIdxRel)
        if sKey in hNonEmptyBlocks:
          oButton.set_light('SeqZoom.Zoom.Active')
        else:
          if nTimeIdxRel >= nCurZoomCol and nTimeIdxRel < nMaxSpanCol:
            oButton.set_light('SeqZoom.Zoom.InSpan')
          else:
            oButton.set_light('SeqZoom.Zoom.Empty')

  def update_side_buttons(self):
    if self.m_nCurMode == MODE_SECTION:
      self.m_lSide[BUT_TOGGLE].set_light('SeqZoom.Toggle.Section')
    else:
      self.m_lSide[BUT_TOGGLE].set_light('SeqZoom.Toggle.Tools')

    if self.m_nCurMode == MODE_SECTION:
      if self.get_time_zoom_mode() == SEQ_TIME_ZOOM_BAR:
        self.m_lSide[BUT_ZOOM_MODE].set_light('SeqZoom.Mode.Bar')
      else:
        self.m_lSide[BUT_ZOOM_MODE].set_light('SeqZoom.Mode.Phrase')
      self.update_section_mode_buttons()
      self.m_lSide[BUT_LP_SHOW].set_light('SeqZoom.LpShow.On')
    else:
      self.m_lSide[BUT_LP_STA_MUL].set_light('SeqZoom.Start.On')
      self.m_lSide[BUT_LP_STA_DIV].set_light('SeqZoom.Start.On')
      self.m_lSide[BUT_LP_MID_MUL].set_light('SeqZoom.Middle.On')
      self.m_lSide[BUT_LP_MID_DIV].set_light('SeqZoom.Middle.On')
      self.m_lSide[BUT_LP_END_MUL].set_light('SeqZoom.End.On')
      self.m_lSide[BUT_LP_END_DIV].set_light('SeqZoom.End.On')
      if self.get_midi_clip_or_none() != None:
        self.m_lSide[BUT_LP_DUP].set_light('SeqZoom.LpDup.On')
      else:
        self.m_lSide[BUT_LP_DUP].set_light('SeqZoom.LpDup.Off')

  def update_section_mode_buttons(self):
    for nIdx in range(SEQ_SECTION_MODE_8 + 1):
      oSide = self.m_lSide[nIdx + 1]
      oSide.set_on_off_values('SeqZoom.Section')
      if nIdx == self.get_section_mode():
        oSide.turn_on()
      else:
        oSide.turn_off()

  # **************************************************************************

  def side_cmd(self, _oButton, _nIdx, _nValue):
    if _nValue == BUTTON_OFF: return
    if self.m_nClipState != SEQ_ZOOM_MIDI_CLIP_STATE_READY:
      return

    if _nIdx == BUT_TOGGLE:
      if self.m_nCurMode == MODE_SECTION:
        self.m_nCurMode = MODE_TOOLS
      else:
        self.m_nCurMode = MODE_SECTION
      self.update_side_buttons()
      return

    if self.m_nCurMode == MODE_SECTION:
      if _nIdx == BUT_ZOOM_MODE:
        nZoomMode = SEQ_TIME_ZOOM_PHRASE if self.get_time_zoom_mode() == SEQ_TIME_ZOOM_BAR else SEQ_TIME_ZOOM_BAR
        self.toggle_zoom_mode(nZoomMode, True)

      elif _nIdx == BUT_LP_SHOW:
        oView = self.application().view
        oView.show_view('Detail')
        oView.focus_view('Detail')
        oView.show_view('Detail/Clip')
        oView.focus_view('Detail/Clip')
        oClip = self.get_clip_or_none()
        if self.m_bLpEnvToggle:
          oClip.view.hide_envelope()
          oClip.view.show_loop()
        else:
          oClip.view.show_envelope()
        self.m_bLpEnvToggle = not self.m_bLpEnvToggle

      else:
        self.set_section_mode(_nIdx - 1)
        self.alert('SECTION MODE: %s' % (self.m_aSectionModes[self.get_section_mode()]))
        self.update_section_mode_buttons()
        self.update_zoom_buttons()
        self.send_grid_command('section_mode', {'section_mode_index': self.get_section_mode()})

    else: # MODE_TOOLS
      if _nIdx == BUT_LP_DUP:
        oClip = self.get_clip_or_none()
        if oClip == None: return
        if self.get_midi_clip_or_none() != None:
          oClip.duplicate_loop()
        return

      oClip = self.get_clip_or_none()
      if oClip == None: return
      nLoopStart = oClip.loop_start
      nLoopEnd   = oClip.loop_end
      nLoopSpan  = nLoopEnd - nLoopStart

      if _nIdx == BUT_LP_STA_MUL:
        oClip.loop_start = nLoopStart - nLoopSpan
      elif _nIdx == BUT_LP_STA_DIV:
        oClip.loop_start = nLoopStart + (nLoopSpan / 2)
      elif _nIdx == BUT_LP_MID_MUL:
        oClip.loop_start = nLoopStart - (nLoopSpan / 2)
        oClip.loop_end   = nLoopEnd   + (nLoopSpan / 2)
      elif _nIdx == BUT_LP_MID_DIV:
        oClip.loop_start = nLoopStart + (nLoopSpan / 4)
        oClip.loop_end   = nLoopEnd   - (nLoopSpan / 4)
      elif _nIdx == BUT_LP_END_MUL:
        oClip.loop_end = nLoopStart + (nLoopSpan * 2)
      elif _nIdx == BUT_LP_END_DIV:
        oClip.loop_end = nLoopStart + (nLoopSpan / 2)

  def toggle_zoom_mode(self, _nZoomMode, _bLocal):
    self.set_time_zoom_mode(_nZoomMode)
    self.m_nNoteLength   = self.get_bit_length()
    self.m_nNoteShift    = 0.0
    if self.get_time_zoom_mode() == SEQ_TIME_ZOOM_BAR:
      self.m_lSide[BUT_ZOOM_MODE].set_light('SeqZoom.Mode.Bar')
    else:
      self.m_lSide[BUT_ZOOM_MODE].set_light('SeqZoom.Mode.Phrase')
    self.update_zoom_buttons()
    if _bLocal:
      self.send_grid_command('zoom_mode', {'new_zoom_mode': _nZoomMode})

  def get_bit_length(self):
    return self.get_surface_length() / 8.0

  def grid_cmd(self, _oButton, _nCol, _nRow, _nValue):
    if _nValue == BUTTON_OFF: return
    if self.m_nClipState == SEQ_ZOOM_MIDI_CLIP_STATE_INVALID:
      self.alert('> SEQ ZOOM AVAILABLE ONLY IN MIDI TRACKS!')
      return # nothing to do here!
    elif self.m_nClipState == SEQ_ZOOM_MIDI_CLIP_STATE_EMPTY:
      self.create_empty_midi_clip()
    elif self.m_nClipState == SEQ_ZOOM_MIDI_CLIP_STATE_READY:
      self.zoom_navigate(7 - _nRow, _nCol, True)

  def zoom_navigate(self, _nOctaveIdx, _nTimeIdx, _bLocal):
    if _nTimeIdx >= self.m_nNumSect: return
    self.m_nPitxOffAbs = _nOctaveIdx * LEN_ONE_OCT
    self.m_nTimeOffAbs = _nTimeIdx   * self.get_time_shift(True)
    self.update_zoom_buttons()
    if _bLocal:
      self.send_grid_command('zoom_nav', {'octave_index': _nOctaveIdx, 'time_index': _nTimeIdx})

  # **************************************************************************

  def compute_section_values(self):
    # compute the number of sections to display depending on
    # the length of the loop
    nClipLen = int(self.m_oClip.loop_end - self.m_oClip.loop_start)
    nSectLen = self.get_section_length()
    nNumSect = nClipLen / nSectLen
    if (nClipLen % nSectLen != 0): nNumSect += 1
    self.m_nNumSect = nNumSect

    # compute the index of the current section
    self.m_nCurSect = self.m_nTimeOffAbs / nSectLen

    # compute the section span
    if self.get_section_mode() == SEQ_SECTION_MODE_2:
      self.m_nSpnSect = 2
    elif self.get_section_mode() == SEQ_SECTION_MODE_4:
      self.m_nSpnSect = 4
    elif self.get_section_mode() == SEQ_SECTION_MODE_8:
      self.m_nSpnSect = 8
    else: # for section modes (1/2, 1) use span = 1
      self.m_nSpnSect = 1

  def get_pitx_offset_abs_for_octave(self, _nOctave):
    return (_nOctave + 2) * LEN_ONE_OCT

  def get_clip_notes(self):
    self.m_oClip.select_all_notes()
    aNotes = self.m_oClip.get_selected_notes()
    self.m_oClip.deselect_all_notes()
    return aNotes

  def get_time_shift(self, _bZoomMode):
    if _bZoomMode:
      # in zoom mode we always navigate in a whole bar / phrase units
      if self.get_time_zoom_mode() == SEQ_TIME_ZOOM_BAR:
        return LEN_ONE_BAR
      return LEN_ONE_PHRASE
    else:
      # in this case the user is navigating with the left, right nav buttons
      if self.m_bNavSync:
        # we have sync navigation so we navigate in a whole bar / phrase units
        if self.get_time_zoom_mode() == SEQ_TIME_ZOOM_BAR:
          return LEN_ONE_BAR
        return LEN_ONE_PHRASE
      else:
        # no sync navigate! we navigate in half bar / phrase units
        if self.get_time_zoom_mode() == SEQ_TIME_ZOOM_BAR:
          return LEN_ONE_BAR / 2
        return LEN_ONE_PHRASE / 2

  # **************************************************************************

  def update_stateful_controls(self):
    self.disconnect_clip_listeners()
    self.set_active(True)

  # **************************************************************************

  def receive_grid_command(self, _hParams):
    sCmd = _hParams['cmd']
    if not self.m_bInit:
      self.m_bInit      = True
      self.m_nClipState = self.get_clip_state()

    if sCmd == 'zoom_nav':
      self.zoom_navigate(_hParams['octave_index'], _hParams['time_index'], False)
    elif sCmd == 'note_nav':
      self.note_navigate(_hParams['pitx_abs'], _hParams['time_abs'])

  def note_navigate(self, _nPitxAbs, _nTimeAbs):
    self.m_nPitxOffAbs = _nPitxAbs
    self.m_nTimeOffAbs = _nTimeAbs
    self.update_zoom_buttons()

  # ****************************************************************************

  def get_clip_state(self):
    self.m_oMidiSlot = self.get_midi_slot_or_none()
    if self.m_oMidiSlot != None and not self.m_oMidiSlot.has_clip_has_listener(self._on_clip_changed):
      self.m_oMidiSlot.add_has_clip_listener(self._on_clip_changed)

    self.m_oClip  = self.get_midi_clip_or_none()
    self.m_oTrack = self.get_midi_track_or_none()

    if self.m_oClip == None:
      if self.m_oTrack == None:
        return SEQ_ZOOM_MIDI_CLIP_STATE_INVALID # No MIDI track
      else:
        return SEQ_ZOOM_MIDI_CLIP_STATE_EMPTY # No MIDI Clip but MIDI Track

    if not self.m_oClip.notes_has_listener(self._on_clip_notes_changed):
      self.m_oClip.add_notes_listener(self._on_clip_notes_changed)
    if not self.m_oClip.loop_start_has_listener(self._on_clip_length_changed):
      self.m_oClip.add_loop_start_listener(self._on_clip_length_changed)
    if not self.m_oClip.loop_end_has_listener(self._on_clip_length_changed):
      self.m_oClip.add_loop_end_listener(self._on_clip_length_changed)

    nClipLen = int(self.m_oClip.loop_end - self.m_oClip.loop_start)
    if self.m_nTimeOffAbs >= nClipLen:
      self.m_nTimeOffAbs = 0
    return SEQ_ZOOM_MIDI_CLIP_STATE_READY # MIDI Clip and MIDI Track

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
    if self.m_nClipState == SEQ_ZOOM_MIDI_CLIP_STATE_READY:
      self.on_clip_notes_changed()

  def _on_clip_length_changed(self):
    if self.m_nClipState == SEQ_ZOOM_MIDI_CLIP_STATE_READY:
      self.on_clip_notes_changed()

  def on_clip_notes_changed(self):
    return
