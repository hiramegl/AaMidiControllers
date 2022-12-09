import Live

from _Framework.CompoundComponent import CompoundComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.TransportComponent import TransportComponent

from SpecialSessionComponent import SpecialSessionComponent
from SpecialMixerComponent import SpecialMixerComponent

from .ModeSession import ModeSession
from .ModeSeqZoom import ModeSeqZoom
from .ModeSeqCmd  import ModeSeqCmd
from .ModeTools   import ModeTools

from .ColorsMK2   import CLIP_COLOR_TABLE, RGB_COLOR_TABLE

MODE_NONE     = -1
MODE_SESSION  = 0
MODE_SEQ_ZOOM = 1
MODE_SEQ_CMD  = 2
MODE_TOOLS    = 3

BUT_UP        = 0
BUT_DOWN      = 1
BUT_LEFT      = 2
BUT_RIGHT     = 3
BUT_SESSION   = 4
BUT_SEQ_ZOOM  = 5
BUT_SEQ_CMD   = 6
BUT_TOOLS     = 7

SEQ_TIME_ZOOM_BAR    = 0 #  4 beat = 1 bar             (in 2 surfaces)
SEQ_TIME_ZOOM_PHRASE = 1 # 16 beat = 4 bars = 1 phrase (in 2 surfaces)

SEQ_SECTION_MODE_1_2 = 0
SEQ_SECTION_MODE_1   = 1
SEQ_SECTION_MODE_2   = 2
SEQ_SECTION_MODE_4   = 3
SEQ_SECTION_MODE_8   = 4

class Selector(CompoundComponent):
  def __init__(self, _oCtrlInst, _hCfg, _oMatrix, _lTop, _lSide):
    self.m_oCtrlInst = _oCtrlInst
    super(Selector, self).__init__()
    self.m_hCfg      = _hCfg
    self.m_oMatrix   = _oMatrix
    self.m_lTop      = _lTop
    self.m_lSide     = _lSide
    self.m_nCurMode  = MODE_NONE
    self.m_nTracks   = _hCfg['NumTracks']
    self.m_nScenes   = _hCfg['NumScenes']
    lNav             = _lTop[:4]
    self.m_lMode     = _lTop[4:]
    self.m_bCtrlInit = False

    self.m_nTimeZoomMode = SEQ_TIME_ZOOM_BAR
    self.m_nSectionMode  = SEQ_SECTION_MODE_1 # CHANGE HERE SECTION MODE!

    self.m_hCfg['oSelector'] = self

    self.m_oSession = SpecialSessionComponent(self.m_nTracks, self.m_nScenes)
    self.m_hCfg['oSession'] = self.m_oSession

    self.m_oMixer = SpecialMixerComponent(
      num_tracks  = self.m_nTracks,
      name        = 'Mixer')
    self.m_hCfg['oMixer'] = self.m_oMixer
    for nTrackIdx in range(self.m_nTracks):
      oStrip = self.m_oMixer.channel_strip(nTrackIdx)
      oStrip.name = 'Channel_Strip_' + str(nTrackIdx)
    self.m_oSession.set_mixer(self.m_oMixer)
    self.m_oSession.set_rgb_mode(CLIP_COLOR_TABLE, RGB_COLOR_TABLE)

    self.m_oZooming = SessionZoomingComponent(
      session         = self.m_oSession,
      enable_skinning = True,
      name            = 'Session_Overview')
    self.m_hCfg['oZooming'] = self.m_oZooming

    self.m_oTransp = TransportComponent(name = 'Transport')
    self.m_hCfg['oTransp'] = self.m_oTransp

    self.m_oModeSession = ModeSession(_oCtrlInst, self.m_hCfg, _oMatrix, _lSide, lNav)
    self.m_oModeSeqZoom = ModeSeqZoom(_oCtrlInst, self.m_hCfg, _oMatrix, _lSide, lNav)
    self.m_oModeSeqCmd  = ModeSeqCmd (_oCtrlInst, self.m_hCfg, _oMatrix, _lSide, lNav)
    self.m_oModeTools   = ModeTools  (_oCtrlInst, self.m_hCfg, _oMatrix, _lSide, lNav)

  def disconnect(self):
    self.m_oSession     = None
    self.m_oZooming     = None
    self.m_oMixer       = None
    self.m_oModeSession = None
    self.m_oModeSeqZoom = None
    self.m_oModeSeqCmd  = None
    self.m_oModeTools   = None

  def session_component(self):
    return self.m_oSession

  def update(self):
    self.m_oSession.set_allow_update(False)
    self.m_oZooming.set_allow_update(False)
    self.m_oMixer.set_allow_update(False)

    for nSceneIdx in range(self.m_nScenes):
      for nTrackIdx in range(self.m_nTracks):
        oButton = self.m_oMatrix.get_button(nTrackIdx, nSceneIdx)
        oButton.set_enabled(True)
    for nSceneIdx in range(self.m_nScenes):
      self.m_lSide[nSceneIdx].set_enabled(True)
    for nTrackIdx in range(self.m_nTracks):
      self.m_lTop[nTrackIdx].set_enabled(True)

    self.select_mode(MODE_SESSION, 127)
    self.m_lMode[MODE_SEQ_ZOOM].set_light('Mode.SeqZoom.Off')
    self.m_lMode[MODE_SEQ_CMD ].set_light('Mode.SeqCmd.Off')
    self.m_lMode[MODE_TOOLS   ].set_light('Mode.Tools.Off')

    self.m_oSession.set_allow_update(True)
    self.m_oZooming.set_allow_update(True)
    self.m_oMixer.set_allow_update(True)

    self.setup_controller_refs()

  def route(self, _oButton, _hAttr, _nValue):
    sType = _hAttr['sType']
    if sType == 'top':
      # navigation button or mode button
      nIdx = _hAttr['nIdx']
      if nIdx >= BUT_UP and nIdx <= BUT_RIGHT:
        # navigation button
        if self.m_nCurMode == MODE_SESSION:
          return # event handled by the session/zoom components
        elif self.m_nCurMode == MODE_SEQ_ZOOM:
          self.m_oModeSeqZoom.nav_cmd(_oButton, nIdx, _nValue)
        elif self.m_nCurMode == MODE_SEQ_CMD:
          self.m_oModeSeqCmd.nav_cmd(_oButton, nIdx, _nValue)
        elif self.m_nCurMode == MODE_TOOLS:
          self.m_oModeTools.nav_cmd(_oButton, nIdx, _nValue)
      else:
        # select-mode button
        self.select_mode(nIdx - BUT_SESSION, _nValue)

    elif sType == 'side':
      # side command button
      nIdx = _hAttr['nIdx']
      if self.m_nCurMode == MODE_SESSION:
        self.m_oModeSession.side_cmd(_oButton, nIdx, _nValue)
      elif self.m_nCurMode == MODE_SEQ_ZOOM:
        self.m_oModeSeqZoom.side_cmd(_oButton, nIdx, _nValue)
      elif self.m_nCurMode == MODE_SEQ_CMD:
        self.m_oModeSeqCmd.side_cmd(_oButton, nIdx, _nValue)
      elif self.m_nCurMode == MODE_TOOLS:
        self.m_oModeTools.side_cmd(_oButton, nIdx, _nValue)

    else: # sType == 'grid':
      nCol = _hAttr['nCol']
      nRow = _hAttr['nRow']
      # side command button
      if self.m_nCurMode == MODE_SESSION:
        return # handled by the session/zoom components
      elif self.m_nCurMode == MODE_SEQ_ZOOM:
        self.m_oModeSeqZoom.grid_cmd(_oButton, nCol, nRow, _nValue)
      elif self.m_nCurMode == MODE_SEQ_CMD:
        self.m_oModeSeqCmd.grid_cmd(_oButton, nCol, nRow, _nValue)
      elif self.m_nCurMode == MODE_TOOLS:
        self.m_oModeTools.grid_cmd(_oButton, nCol, nRow, _nValue)

  def select_mode(self, _nNewMode, _nValue):
    if _nValue == 0: return

    if self.m_nCurMode == _nNewMode:
      if self.m_nCurMode == MODE_SESSION:
        self.m_oModeSession.change_prev_mode()
      return # re-selecting has no effect for other modes (they have few sub-modes)

    # disconnect old mode
    if self.m_nCurMode == MODE_SESSION:
      self.m_lMode[MODE_SESSION].set_light('Mode.Session.Off')
      self.m_oModeSession.set_active(False)
    elif self.m_nCurMode == MODE_SEQ_ZOOM:
      self.m_lMode[MODE_SEQ_ZOOM].set_light('Mode.SeqZoom.Off')
      self.m_oModeSeqZoom.set_active(False)
    elif self.m_nCurMode == MODE_SEQ_CMD:
      self.m_lMode[MODE_SEQ_CMD].set_light('Mode.SeqCmd.Off')
      self.m_oModeSeqCmd.set_active(False)
    elif self.m_nCurMode == MODE_TOOLS:
      self.m_lMode[MODE_TOOLS].set_light('Mode.Tools.Off')
      self.m_oModeTools.set_active(False)

    # connect new mode
    if _nNewMode == MODE_SESSION:
      self.m_lMode[MODE_SESSION].set_light('Mode.Session.On')
      self.m_oModeSession.set_active(True)
    elif _nNewMode == MODE_SEQ_ZOOM:
      self.m_lMode[MODE_SEQ_ZOOM].set_light('Mode.SeqZoom.On')
      self.m_oModeSeqZoom.set_active(True)
    elif _nNewMode == MODE_SEQ_CMD:
      self.m_lMode[MODE_SEQ_CMD].set_light('Mode.SeqCmd.On')
      self.m_oModeSeqCmd.set_active(True)
    elif _nNewMode == MODE_TOOLS:
      self.m_lMode[MODE_TOOLS].set_light('Mode.Tools.On')
      self.m_oModeTools.set_active(True)

    self.m_nCurMode = _nNewMode

  # **************************************************************************

  def _on_sel_scene_changed(self):
    if self.m_nCurMode == MODE_SEQ_ZOOM:
      self.m_oModeSeqZoom._on_sel_scene_changed()
    elif self.m_nCurMode == MODE_SEQ_CMD:
      self.m_oModeSeqCmd._on_sel_scene_changed()
    elif self.m_nCurMode == MODE_TOOLS:
      self.m_oModeTools._on_sel_scene_changed()

  def _on_sel_track_changed(self):
    if self.m_nCurMode == MODE_SEQ_ZOOM:
      self.m_oModeSeqZoom._on_sel_track_changed()
    elif self.m_nCurMode == MODE_SEQ_CMD:
      self.m_oModeSeqCmd._on_sel_track_changed()
    elif self.m_nCurMode == MODE_TOOLS:
      self.m_oModeTools._on_sel_track_changed()

  # ****************************************************************************

  def setup_controller_refs(self):
    if self.m_bCtrlInit: return # grids already found! nothing else to do here!

    self.m_sMyName = self.m_oCtrlInst.__class__.__name__
    self.m_nMyId   = self.m_oCtrlInst.instance_identifier()
    self.log('> Current instance: %s / %d' % (self.m_sMyName, self.m_nMyId))

    lCtrlInsts        = Live.Application.get_application().control_surfaces
    self.m_oFaderCtrl = None
    self.m_lGridInsts = []
    for oCtrlInst in lCtrlInsts:
      if oCtrlInst == None: continue
      sCtrlName = oCtrlInst.__class__.__name__
      nCtrlId   = oCtrlInst.instance_identifier()
      if sCtrlName == 'AaGrid':
        self.log('> Registering control surface: %s / %d' % (sCtrlName, nCtrlId))
        self.m_lGridInsts.append({'name': sCtrlName, 'id': nCtrlId, 'ctrl': oCtrlInst})
      if sCtrlName == 'AaFader':
        self.log('> Registering control surface: %s / %d' % (sCtrlName, nCtrlId))
        self.m_oFaderCtrl = oCtrlInst
    self.m_bCtrlInit = True

  def send_grid_command(self, _sCmd, _hParams = None):
    if self.m_bCtrlInit:
      _hParams = {} if _hParams == None else _hParams
      _hParams['cmd']       = _sCmd
      _hParams['matrix_id'] = self.m_nMyId
      self.m_lGridInsts[0]['ctrl'].receive_matrix_command(_hParams)
      self.m_lGridInsts[1]['ctrl'].receive_matrix_command(_hParams)

  def receive_grid_command(self, _hCmd):
    self.m_oModeSeqZoom.receive_grid_command(_hCmd)
    self.m_oModeSeqCmd.receive_grid_command(_hCmd)

  def send_fader_command(self, _sCmd):
    if self.m_oFaderCtrl == None: return
    nTrackOffset = self.m_oSession.track_offset()
    self.m_oFaderCtrl.move_to_track_offset(nTrackOffset)

  # ****************************************************************

  def set_time_zoom_mode(self, _nTimeZoomMode):
    self.m_nTimeZoomMode = _nTimeZoomMode

  def get_time_zoom_mode(self):
    return self.m_nTimeZoomMode

  def set_section_mode(self, _nSectionMode):
    self.m_nSectionMode = _nSectionMode

  def get_section_mode(self):
    return self.m_nSectionMode

  # ****************************************************************

  def log(self, _sMsg):
    self.m_oCtrlInst.xlog(_sMsg)

  def alert(self, _sMsg):
    self.m_oCtrlInst.alert(_sMsg)
