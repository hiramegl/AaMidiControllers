from .ModeBase import *

MODE_SELECT = 0
MODE_LAUNCH = 1
MODE_ZOOM   = 2
MODE_SENDS  = 3

BUT_PLAY    = 0
BUT_STOP    = 1
BUT_MUTE    = 2
BUT_SOLO    = 3
BUT_SENDS   = 4
BUT_ZOOM    = 5
BUT_LAUNCH  = 6
BUT_SELECT  = 7

class ModeSession(ModeBase):
  def __init__(self, _oCtrlInst, _hCfg, _oMatrix, _lSide, _lNav):
    super(ModeSession, self).__init__(_oCtrlInst, _hCfg, _oMatrix, _lSide, _lNav)
    self.m_lBank    = _lSide[:BUT_SENDS]
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
      self.m_lSide[BUT_SENDS ].set_on_off_values('Session.ModeMixer')
      self.m_lSide[BUT_ZOOM  ].set_on_off_values('Session.ModeZoom')
      self.m_lSide[BUT_LAUNCH].set_on_off_values('Session.ModeLaunch')
      self.m_lSide[BUT_SELECT].set_on_off_values('Session.ModeSelect')

      if self.m_nCurMode == MODE_SENDS:
        self.setup_clip_track_buttons(_bActive)
        self.m_lSide[BUT_SENDS ].turn_on()
        self.m_lSide[BUT_ZOOM  ].turn_off()
        self.m_lSide[BUT_LAUNCH].turn_off()
        self.m_lSide[BUT_SELECT].turn_off()

      elif self.m_nCurMode == MODE_ZOOM:
        self.m_lSide[BUT_SENDS ].turn_off()
        self.m_lSide[BUT_ZOOM  ].turn_on()
        self.m_lSide[BUT_LAUNCH].turn_off()
        self.m_lSide[BUT_SELECT].turn_off()

      elif self.m_nCurMode == MODE_LAUNCH:
        self.setup_clip_track_buttons(_bActive)
        self.m_lSide[BUT_SENDS ].turn_off()
        self.m_lSide[BUT_ZOOM  ].turn_off()
        self.m_lSide[BUT_LAUNCH].turn_on()
        self.m_lSide[BUT_SELECT].turn_off()

      elif self.m_nCurMode == MODE_SELECT:
        self.setup_clip_track_buttons(_bActive)
        self.m_lSide[BUT_SENDS ].turn_off()
        self.m_lSide[BUT_ZOOM  ].turn_off()
        self.m_lSide[BUT_LAUNCH].turn_off()
        self.m_lSide[BUT_SELECT].turn_on()

  def setup_clip_track_buttons(self, _bActive):
    if _bActive:
      self.m_lSide[BUT_PLAY].set_on_off_values('Session.Play')
      self.m_lSide[BUT_STOP].set_on_off_values('Session.Stop')
      self.m_lSide[BUT_MUTE].set_on_off_values('Session.Mute')
      self.m_lSide[BUT_SOLO].set_on_off_values('Session.Solo')
      for nIdx in range(BUT_PLAY, BUT_SOLO + 1):
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
    if _nIdx < BUT_SENDS:
      return self.handle_clip_track_cmd(_nIdx)
    if   _nIdx == BUT_SENDS:  nCurMode = MODE_SENDS
    elif _nIdx == BUT_ZOOM:   nCurMode = MODE_ZOOM
    elif _nIdx == BUT_LAUNCH: nCurMode = MODE_LAUNCH
    elif _nIdx == BUT_SELECT: nCurMode = MODE_SELECT
    if self.m_nCurMode == nCurMode: return
    self.setup_grid_buttons(False)
    self.m_nCurMode = nCurMode
    self.setup_grid_buttons(True)
    self.setup_side_buttons(True)

  def handle_clip_track_cmd(self, _nIdx):
    if self.m_nCurMode == MODE_ZOOM:
      return False # Zoom mode handle these buttons!

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
    return True # handled
