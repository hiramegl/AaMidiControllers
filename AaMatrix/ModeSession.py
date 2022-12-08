from .ModeBase import *

MODE_SELECT = 0
MODE_LAUNCH = 1
MODE_ZOOM   = 2
MODE_VOLUME = 3
MODE_SENDS  = 4
NUM_MODES   = 5

BUT_PLAY    = 0
BUT_STOP    = 1
BUT_MUTE    = 2
BUT_SOLO    = 3
BUT_PAN_RST = 4
BUT_VOL_RST = 5
BUT_DECK    = 6
BUT_MODE    = 7

MAX_BANKS   = 7

class ModeSession(ModeBase):
  def __init__(self, _oCtrlInst, _hCfg, _oMatrix, _lSide, _lNav):
    super(ModeSession, self).__init__(_oCtrlInst, _hCfg, _oMatrix, _lSide, _lNav)
    self.m_lBank    = _lSide[:MAX_BANKS] # scene bank buttons
    self.m_nCurMode = MODE_SELECT

  def set_active(self, _bActive):
    self.setup_paging_buttons(_bActive)
    self.setup_side_buttons(_bActive)
    self.setup_grid_buttons(_bActive)

  def setup_paging_buttons(self, _bActive):
    if _bActive:
      for oButton in self.m_lNav:
        oButton.set_on_off_values('Session.Nav')
      self.m_oSession.set_page_up_button(self.m_lNav[0])
      self.m_oSession.set_page_down_button(self.m_lNav[1])
      self.m_oSession.set_page_left_button(self.m_lNav[2])
      self.m_oSession.set_page_right_button(self.m_lNav[3])

    else:
      for oButton in self.m_lNav:
        oButton.set_on_off_values('DefaultButton.Disabled', 'DefaultButton.Disabled')
      self.m_oSession.set_page_up_button(None)
      self.m_oSession.set_page_down_button(None)
      self.m_oSession.set_page_left_button(None)
      self.m_oSession.set_page_right_button(None)

  def setup_side_buttons(self, _bActive):
    if _bActive:
      lModeColors = ['Select', 'Launch', 'Zoom', 'Volume', 'Sends']
      sModeColor  = 'Session.Mode%s' % (lModeColors[self.m_nCurMode])
      self.m_lSide[BUT_MODE].set_on_off_values(sModeColor)
      self.m_lSide[BUT_MODE].turn_on()

      if self.m_nCurMode == MODE_VOLUME:
        self.setup_group_volume_buttons(True)
      elif self.m_nCurMode != MODE_ZOOM:
        self.setup_clip_track_buttons(_bActive)

    else:
      if self.m_nCurMode == MODE_VOLUME:
        self.setup_group_volume_buttons(False)

  def setup_group_volume_buttons(self, _bActive):
    if _bActive:
      oStrip = self.m_oMixer.channel_strip(0) # get first strip
      for nIdx in range(7):
        oScene  = self.m_oSession.scene(nIdx)
        oButton = self.m_lSide[nIdx]
        oButton.set_on_off_values('Session.Volume')
        oButton.turn_on()
        oScene.set_vol_control(oButton, oStrip.m_aVolMap[nIdx])

    else:
      for nIdx in range(7):
        oScene = self.m_oSession.scene(nIdx)
        oScene.set_vol_control(None, 0.0)

  def setup_clip_track_buttons(self, _bActive):
    if _bActive:
      lColors = ['Play', 'Stop', 'Mute', 'Solo', 'PanReset', 'VolReset', 'Deck']
      for nIdx in range(BUT_PLAY, BUT_DECK + 1):
        sColor = 'Session.%s' % (lColors[nIdx])
        self.m_lSide[nIdx].set_on_off_values(sColor)
        self.m_lSide[nIdx].turn_on()

  def setup_grid_buttons(self, _bActive):
    if _bActive:
      if self.m_nCurMode == MODE_SENDS:
        aNames = ['Send', 'Send', 'Send', 'Send', 'Send', 'Send', 'Monitor', 'Arm']
        for nTrackIdx in range(self.m_nTracks):
          for nSceneIdx in range(self.m_nScenes):
            self.m_oMatrix.get_button(nTrackIdx, nSceneIdx).set_on_off_values("Session.%s" % (aNames[nSceneIdx]))
          oStrip = self.m_oMixer.channel_strip(nTrackIdx)
          oStrip.set_send_controls(
              self.m_oMatrix.get_button(nTrackIdx, 0),
              self.m_oMatrix.get_button(nTrackIdx, 1),
              self.m_oMatrix.get_button(nTrackIdx, 2),
              self.m_oMatrix.get_button(nTrackIdx, 3),
              self.m_oMatrix.get_button(nTrackIdx, 4),
              self.m_oMatrix.get_button(nTrackIdx, 5))
          oStrip.set_monitor_button(self.m_oMatrix.get_button(nTrackIdx, 6))
          oStrip.set_arm_button    (self.m_oMatrix.get_button(nTrackIdx, 7))

      elif self.m_nCurMode == MODE_VOLUME:
        for nTrackIdx in range(self.m_nTracks):
          for nSceneIdx in range(self.m_nScenes):
            self.m_oMatrix.get_button(nTrackIdx, nSceneIdx).set_on_off_values("Session.Volume")
          oStrip = self.m_oMixer.channel_strip(nTrackIdx)
          oStrip.set_vol_controls(
              self.m_oMatrix.get_button(nTrackIdx, 0),
              self.m_oMatrix.get_button(nTrackIdx, 1),
              self.m_oMatrix.get_button(nTrackIdx, 2),
              self.m_oMatrix.get_button(nTrackIdx, 3),
              self.m_oMatrix.get_button(nTrackIdx, 4),
              self.m_oMatrix.get_button(nTrackIdx, 5),
              self.m_oMatrix.get_button(nTrackIdx, 6),
              self.m_oMatrix.get_button(nTrackIdx, 7))

      elif self.m_nCurMode == MODE_ZOOM:
        for nSceneIdx in range(self.m_nScenes):
          self.m_lSide[nSceneIdx].set_on_off_values('Session.Zoom')
        self.m_oZooming._enable_skinning()
        self.m_oZooming.set_button_matrix(self.m_oMatrix)
        self.m_oZooming.set_scene_bank_buttons(self.m_lBank)
        self.m_oZooming.update()

      elif self.m_nCurMode == MODE_LAUNCH:
        for nSceneIdx in range(self.m_nScenes):
          oScene = self.m_oSession.scene(nSceneIdx)
          for nTrackIdx in range(self.m_oSession.width()):
            oButton = self.m_oMatrix.get_button(nTrackIdx, nSceneIdx)
            oButton.set_on_off_values("Unav")
            oButton.set_enabled(True)
            oScene.clip_slot(nTrackIdx).set_launch_button(oButton)

      elif self.m_nCurMode == MODE_SELECT:
        for nSceneIdx in range(self.m_nScenes):
          oScene = self.m_oSession.scene(nSceneIdx)
          for nTrackIdx in range(self.m_nTracks):
            oButton = self.m_oMatrix.get_button(nTrackIdx, nSceneIdx)
            oButton.set_on_off_values("Unav")
            oButton.set_enabled(True)
            oClipSlot = oScene.clip_slot(nTrackIdx)
            oClipSlot.set_launch_button(oButton)
            oClipSlot.set_select_button(oButton)

    else:
      if self.m_nCurMode == MODE_SENDS:
        for nTrackIdx in range(self.m_nTracks):
          oStrip = self.m_oMixer.channel_strip(nTrackIdx)
          oStrip.set_send_controls (None, None, None, None, None, None)
          oStrip.set_monitor_button(None)
          oStrip.set_arm_button    (None)

      elif self.m_nCurMode == MODE_VOLUME:
        for nTrackIdx in range(self.m_nTracks):
          oStrip = self.m_oMixer.channel_strip(nTrackIdx)
          oStrip.set_vol_controls(None, None, None, None, None, None, None, None)

      elif self.m_nCurMode == MODE_ZOOM:
        self.m_oZooming.set_button_matrix(None)
        self.m_oZooming.set_scene_bank_buttons(None)

      elif self.m_nCurMode == MODE_LAUNCH:
        for nSceneIdx in range(self.m_nScenes):
          oScene = self.m_oSession.scene(nSceneIdx)
          for nTrackIdx in range(self.m_oSession.width()):
            oButton = self.m_oMatrix.get_button(nTrackIdx, nSceneIdx)
            oScene.clip_slot(nTrackIdx).set_launch_button(None)

      if self.m_nCurMode == MODE_SELECT:
        for nSceneIdx in range(self.m_nScenes):
          oScene = self.m_oSession.scene(nSceneIdx)
          for nTrackIdx in range(self.m_nTracks):
            oClipSlot = oScene.clip_slot(nTrackIdx)
            oClipSlot.set_launch_button(None)
            oClipSlot.set_select_button(None)

  def side_cmd(self, _oButton, _nIdx, _nValue):
    if _nValue == BUTTON_OFF: return

    if _nIdx != BUT_MODE:
      return self.handle_clip_track_cmd(_nIdx)

    # we are changing mode! turn off colors!
    self.setup_grid_buttons(False)
    self.setup_side_buttons(False)
    nCurrMode       = self.m_nCurMode
    self.m_nCurMode = (nCurrMode + 1) % NUM_MODES

    # now turn on colors and setup side buttons
    self.setup_grid_buttons(True)
    self.setup_side_buttons(True)

  def handle_clip_track_cmd(self, _nIdx):
    if self.m_nCurMode == MODE_ZOOM or self.m_nCurMode == MODE_VOLUME:
      return False # Zoom and volume mode handle these buttons!

    if _nIdx == BUT_PLAY:
      oClipSlot = self.m_oSession.song().view.highlighted_clip_slot
      if oClipSlot != None: oClipSlot.fire()

    elif _nIdx == BUT_STOP:
      oClipSlot = self.m_oSession.song().view.highlighted_clip_slot
      if oClipSlot != None: oClipSlot.stop()

    elif _nIdx == BUT_MUTE:
      oTrack = self.m_oSession.song().view.selected_track
      oTrack.mute = not oTrack.mute

    elif _nIdx == BUT_SOLO:
      oTrack = self.m_oSession.song().view.selected_track
      oTrack.solo = not oTrack.solo

    elif _nIdx == BUT_PAN_RST:
      oTrack = self.m_oSession.song().view.selected_track
      oTrack.mixer_device.panning.value = 0

    elif _nIdx == BUT_VOL_RST:
      oTrack = self.m_oSession.song().view.selected_track
      oTrack.mixer_device.volume.value = 0.85

    elif _nIdx == BUT_DECK:
      oTrack = self.m_oSession.song().view.selected_track
      nCurr = oTrack.mixer_device.crossfade_assign
      oTrack.mixer_device.crossfade_assign = (nCurr + 1) % 3

    return True # handled
