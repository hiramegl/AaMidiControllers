import math
from .ModeBase import *

BUT_LP_1    = 0
BUT_LP_2    = 1
BUT_LP_4    = 2
BUT_LP_8    = 3
BUT_LP_16   = 4
BUT_LP_TOGG = 5
BUT_LP_ENV  = 6
BUT_FADERS  = 7

ROW_SIZE        = 0
ROW_START_END   = 1
ROW_SHF_MUL_DIV = 2
ROW_BEAT_14     = 3
ROW_BEAT_58     = 4
ROW_BEAT_18     = 5
ROW_STATEFUL    = 6
ROW_CLIP_SESS   = 7

COL_CL_START_DEC = 0
COL_CL_START_INC = 1
COL_CL_END_DEC   = 2
COL_CL_END_INC   = 3
COL_LP_START_DEC = 4
COL_LP_START_INC = 5
COL_LP_END_DEC   = 6
COL_LP_END_INC   = 7

COL_LP_SHF_DEC = 0
COL_LP_SHF_INC = 1
COL_LP_STA_DIV = 2
COL_LP_STA_MUL = 3
COL_LP_MID_DIV = 4
COL_LP_MID_MUL = 5
COL_LP_END_DIV = 6
COL_LP_END_MUL = 7

COL_RES_TRP  = 0
COL_RES_DET  = 1
COL_RES_GAIN = 2
COL_CROP     = 3
COL_QUANT    = 4
COL_WARP     = 5
COL_METRO    = 6
COL_FOLLOW   = 7

COL_CL_PLAY  = 0
COL_CL_STOP  = 1
COL_CL_DUP   = 2
COL_REW      = 3
COL_FF       = 4
COL_PLAY     = 5
COL_STOP     = 6
COL_REC      = 7

class ModeTools(ModeBase):
  def __init__(self, _oCtrlInst, _hCfg, _oMatrix, _lSide, _lNav):
    super(ModeTools, self).__init__(_oCtrlInst, _hCfg, _oMatrix, _lSide, _lNav)
    self.m_aSkin = [
      ['Size'   , 'Size'   , 'Size'   , 'Size'   , 'Size'   , 'Size'   , 'Size'   , 'Size'   , 'Span'  ],
      ['ClStart', 'ClStart', 'ClEnd'  , 'ClEnd'  , 'LpStart', 'LpStart', 'LpEnd'  , 'LpEnd'  , 'Span'  ],
      ['Shift'  , 'Shift'  , 'Start'  , 'Start'  , 'Middle' , 'Middle' , 'End'    , 'End'    , 'Span'  ],
      ['Beat14' , 'Beat14' , 'Beat14' , 'Beat14' , 'Beat14' , 'Beat14' , 'Beat14' , 'Beat14' , 'Span'  ],
      ['Beat58' , 'Beat58' , 'Beat58' , 'Beat58' , 'Beat58' , 'Beat58' , 'Beat58' , 'Beat58' , 'Span'  ],
      ['Beat18' , 'Beat18' , 'Beat18' , 'Beat18' , 'Beat18' , 'Beat18' , 'Beat18' , 'Beat18' , 'LpTogg'],
      ['Reset'  , 'Reset'  , 'Reset'  , 'Crop'   , 'Quant'  , 'Warp'   , 'Metro'  , 'Follow' , 'LpEnv' ],
      ['ClPlay' , 'ClStop' , 'ClDup'  , 'Rew'    , 'Ff'     , 'Play'   , 'Stop'   , 'Rec'    , 'Faders'],
    ]
    self.m_aSizes       = [0.125, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0] # in beats
    self.m_nSizeIdx     = 3 # default size = 1 beat
    self.m_nRollStart   = 0.0 # roll start for 1 bar (1/8 of 1 bar  = 1/2 beat)
    self.m_nRollSpan    = 8.0
    self.m_nCurrRollIdx = -1
    self.m_bLpEnvToggle = True
    self.m_bActive      = False

  def set_active(self, _bActive):
    if _bActive:
      self.setup_buttons()
    else:
      self.m_oTransp.set_seek_buttons(None, None)
      self.m_oTransp.set_play_button(None)
      self.m_oTransp.set_record_button(None)
      self.setup_nav_buttons(False)
    self.m_bActive = _bActive

  def setup_buttons(self):
    self.setup_nav_buttons(True, "Tools.Nav")

    for nRow in self.m_rHeight:
      oSide = self.m_lSide[nRow]
      oSide.set_on_off_values("Tools.%s" % (self.m_aSkin[nRow][8]))
      self.setup_side_button(oSide, nRow)
      for nCol in self.m_rWidth:
        oButton = self.m_oMatrix.get_button(nCol, nRow)
        oButton.set_on_off_values("Tools.%s" % (self.m_aSkin[nRow][nCol]))
        self.setup_grid_button(oButton, nRow, nCol)

  def setup_side_button(self, _oSide, _nRow):
    oClip = self.get_clip_or_none()
    oMidi = self.get_midi_clip_or_none()

    if _nRow == BUT_LP_TOGG: # only for available clips
      if oClip != None and oClip.looping:
        _oSide.turn_on()
      else:
        _oSide.turn_off()

    else: # command buttons always on
      _oSide.turn_on()

  def setup_grid_button(self, _oButton, _nRow, _nCol):
    oAudio = self.get_audio_clip_or_none()
    oSong  = self.song()

    if _nRow == ROW_SIZE: # size button
      if _nCol == self.m_nSizeIdx:
        _oButton.turn_on()
      else:
        _oButton.turn_off()

    elif _nRow == ROW_STATEFUL: # command and stateful buttons
       if _nCol < COL_WARP: # command button: reset, crop, quant
         _oButton.turn_on()
       elif _nCol == COL_WARP and oAudio and oAudio.warping:
         _oButton.turn_on()
       elif _nCol == COL_METRO and oSong.metronome:
         _oButton.turn_on()
       elif _nCol == COL_FOLLOW and oSong.view.follow_song:
         _oButton.turn_on()
       else:
         _oButton.turn_off()

    elif _nRow == ROW_CLIP_SESS:
      if _nCol == COL_REW:
        oFf = self.m_oMatrix.get_button(COL_FF, ROW_CLIP_SESS)
        self.m_oTransp.set_seek_buttons(oFf, _oButton)
        _oButton.turn_on()
        oFf.turn_on()
      elif _nCol == COL_PLAY:
        self.m_oTransp.set_play_button(_oButton)
      elif _nCol == COL_REC:
        self.m_oTransp.set_record_button(_oButton)
      else: # command button
        _oButton.turn_on()

    else: # command button
      _oButton.turn_on()

  def nav_cmd(self, _oButton, _nIdx, _nValue):
    return # handled by the session and mixer components

  def side_cmd(self, _oButton, _nIdx, _nValue):
    if _nValue == BUTTON_OFF: return
    if _nIdx == BUT_FADERS:
      self.alert('> Aligning faders ...')
      self.m_oSelector.send_fader_command('align')
      return

    oClip = self.get_clip_or_none()
    if oClip == None: return
    (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars()

    if _nIdx == BUT_LP_TOGG:
      bLooping = oClip.looping
      oClip.looping = not bLooping
      if bLooping: self.m_lSide[_nIdx].turn_off() # it was looping, now is not looping
      else:        self.m_lSide[_nIdx].turn_on()  # it was not looping, now is looping
    elif _nIdx == BUT_LP_ENV:
      oView = self.application().view
      oView.show_view('Detail')
      oView.focus_view('Detail')
      oView.show_view('Detail/Clip')
      oView.focus_view('Detail/Clip')
      if self.m_bLpEnvToggle:
        oClip.view.hide_envelope()
        oClip.view.show_loop()
      else:
        oClip.view.show_envelope()
      self.m_bLpEnvToggle = not self.m_bLpEnvToggle
    else:
      nSpan = 0.0
      if _nIdx == BUT_LP_1:
        nSpan = 4.0
      elif _nIdx == BUT_LP_2:
        nSpan = 8.0
      elif _nIdx == BUT_LP_4:
        nSpan = 16.0
      elif _nIdx == BUT_LP_8:
        nSpan = 32.0
      elif _nIdx == BUT_LP_16:
        nSpan = 64.0
      if oClip.is_playing:
        nPlayPos   = oClip.playing_position
        nCurrBar   = (math.floor(math.floor(nPlayPos)/ 4.0)) * 4.0
        nLoopStart = nCurrBar
      oClip.loop_end    = nLoopStart + nSpan
      self.m_nRollStart = nLoopStart
      self.m_nCurrRollIdx = -1
      if oClip.is_playing:
        oClip.loop_start = nLoopStart

  def grid_cmd(self, _oButton, _nCol, _nRow, _nValue):
    if _nValue == BUTTON_OFF: return

    oClip = self.get_clip_or_none()

    if _nRow == ROW_SIZE: # size
      if _nCol != self.m_nSizeIdx:
        nOld = self.m_nSizeIdx
        self.m_oMatrix.get_button(nOld,  _nRow).turn_off()
        self.m_oMatrix.get_button(_nCol, _nRow).turn_on()
        self.m_nSizeIdx = _nCol

    elif _nRow == ROW_START_END: # clip start/end, loop start/end
      (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars()
      if (oClip == None): return
      if _nCol == COL_CL_START_DEC:
        oClip.start_marker = oClip.start_marker - nSize
      elif _nCol == COL_CL_START_INC:
        nStart = oClip.start_marker
        if (nStart + nSize < nLoopEnd) and (nStart + nSize < oClip.end_marker):
            oClip.start_marker = nStart + nSize
      elif _nCol == COL_CL_END_DEC:
        oClip.end_marker = oClip.end_marker - nSize
      elif _nCol == COL_CL_END_INC:
        oClip.end_marker = oClip.end_marker + nSize
      if _nCol == COL_LP_START_DEC:
        oClip.loop_start = oClip.loop_start - nSize
      elif _nCol == COL_LP_START_INC:
        if (oClip.loop_start + nSize < oClip.loop_end):
          oClip.loop_start = oClip.loop_start + nSize
      elif _nCol == COL_LP_END_DEC:
        if (oClip.loop_end - nSize > oClip.loop_start):
          oClip.loop_end = oClip.loop_end - nSize
      elif _nCol == COL_LP_END_INC:
        oClip.loop_end = oClip.loop_end + nSize

    elif _nRow == ROW_SHF_MUL_DIV: # shift, mul, div
      (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars()
      if (oClip == None): return
      if _nCol == COL_LP_SHF_DEC:
        oClip.loop_start = nLoopStart - nSize
        oClip.loop_end   = nLoopEnd   - nSize
        self.m_nRollStart = oClip.loop_start
      elif _nCol == COL_LP_SHF_INC:
        oClip.loop_end   = nLoopEnd   + nSize
        oClip.loop_start = nLoopStart + nSize
        self.m_nRollStart = oClip.loop_start
      elif _nCol == COL_LP_STA_DIV:
        oClip.loop_start = nLoopStart + (nLoopSpan / 2)
        self.m_nCurrRollIdx = -1
      elif _nCol == COL_LP_STA_MUL:
        oClip.loop_start = nLoopStart - nLoopSpan
        self.m_nCurrRollIdx = -1
      elif _nCol == COL_LP_MID_DIV:
        oClip.loop_start = nLoopStart + (nLoopSpan / 4)
        oClip.loop_end   = nLoopEnd   - (nLoopSpan / 4)
        self.m_nCurrRollIdx = -1
      elif _nCol == COL_LP_MID_MUL:
        oClip.loop_start = nLoopStart - (nLoopSpan / 2)
        oClip.loop_end   = nLoopEnd   + (nLoopSpan / 2)
        self.m_nCurrRollIdx = -1
      elif _nCol == COL_LP_END_DIV:
        oClip.loop_end = nLoopStart + (nLoopSpan / 2)
        self.m_nCurrRollIdx = -1
      elif _nCol == COL_LP_END_MUL:
        oClip.loop_end = nLoopStart + (nLoopSpan * 2)
        self.m_nCurrRollIdx = -1

    elif _nRow == ROW_BEAT_14:
      nOff = 0.5 * _nCol
      self.handle_roll_value(nOff, 0.5, _nCol)

    elif _nRow == ROW_BEAT_58:
      nOff = 0.5 * _nCol + 4.0
      self.handle_roll_value(nOff, 0.5, _nCol + 8)

    elif _nRow == ROW_BEAT_18:
      self.handle_roll_value(_nCol, 1.0, _nCol + 16)

    elif _nRow == ROW_STATEFUL: # reset, crop, quant, warp, metro, follow
      if _nCol == COL_RES_TRP:
        if oClip == None: return
        if not oClip.is_midi_clip:
          oClip.pitch_coarse = 0
        else:
          self.alert('> No PITCH in midi files')
        return

      elif _nCol == COL_RES_DET:
        if oClip == None: return
        if not oClip.is_midi_clip:
          oClip.pitch_fine = 0
        else:
          self.alert('> No DETUNE in midi files')
        return

      elif _nCol == COL_RES_GAIN:
        if oClip == None: return
        if not oClip.is_midi_clip:
          oClip.gain = 0.4
        else:
          self.alert('> No GAIN in midi files')
        return

      elif _nCol == COL_CROP:
        if oClip == None: return
        if oClip.is_midi_clip:
          oClip.crop()
          self.alert('> Cropping midi clip')
        else:
          self.alert('> No CROP in audio files')
        return

      elif _nCol == COL_QUANT:
        if oClip == None: return
        oClip.quantize(1, 0)
        self.alert('> Quantizing clip')
        return

      elif _nCol == COL_WARP:
        oAudio = self.get_audio_clip_or_none()
        if oAudio:
          bVal = oAudio.warping
          oAudio.warping = not bVal
        else:
          self.alert('> No WARP in midi files')
          return

      elif _nCol == COL_METRO:
        oSong = self.song()
        bVal  = oSong.metronome
        oSong.metronome = not bVal

      elif _nCol == COL_FOLLOW:
        oSong = self.song()
        bVal  = oSong.view.follow_song
        oSong.view.follow_song = not bVal

      if bVal: _oButton.turn_off() # feature was on, now is off
      else:    _oButton.turn_on()  # feature was off, now is on

    elif _nRow == ROW_CLIP_SESS: # clip play/stop/dup, session rew/ff/play/stop/rec
      oClipSlot = self.sel_clip_slot()
      if _nCol == COL_CL_PLAY and oClipSlot:
        oClipSlot.fire()
      elif _nCol == COL_CL_STOP and oClipSlot:
        oClipSlot.stop()
      elif _nCol == COL_CL_DUP and oClipSlot:
        nSelSceneIdxAbs = self.sel_scene_idx_abs()
        oSelTrack = self.sel_track()
        oSelTrack.duplicate_clip_slot(nSelSceneIdxAbs)
        self.alert('> DUPLICATED CLIP at track "%s", scene: %d' % (oSelTrack.name, nSelSceneIdxAbs))
      elif _nCol == COL_STOP:
        oSong = self.song()
        oSong.stop_all_clips()
        oSong.stop_playing()

  def handle_roll_value(self, _nOffset, _nSize, _nIdx):
    oClip = self.get_clip_or_none()
    if (oClip == None): return
    if (self.m_nCurrRollIdx != _nIdx):
      nClipEnd = oClip.end_marker
      nLoopEnd = self.m_nRollStart + _nOffset + _nSize
      if nLoopEnd > nClipEnd: return
      oClip.loop_start = 0.0
      oClip.loop_end   = nLoopEnd
      oClip.loop_start = self.m_nRollStart + _nOffset
      self.m_nCurrRollIdx = _nIdx

    else:
      # selecting the same roll button! return to normal loop
      oClip.loop_start = oClip.start_marker
      oClip.loop_end   = oClip.end_marker
      oClip.loop_start = self.m_nRollStart
      oClip.loop_end   = self.m_nRollStart + self.m_nRollSpan
      self.m_nCurrRollIdx = -1

  # **************************************************************************

  def update_stateful_controls(self):
    if not self.m_bActive: return
    self.setup_side_button(self.m_lSide[BUT_LP_TOGG], BUT_LP_TOGG)
    self.setup_grid_button(self.m_oMatrix.get_button(COL_WARP, ROW_STATEFUL), ROW_STATEFUL, COL_WARP)

  # **************************************************************************

  def fetch_loop_vars(self):
    oClip = self.get_clip_or_none()
    if (oClip == None): return (None, None, None, None, None)
    nLoopStart = oClip.loop_start
    nLoopEnd   = oClip.loop_end
    nLoopSpan  = nLoopEnd - nLoopStart
    nSize      = self.m_aSizes[self.m_nSizeIdx]
    return (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize)
