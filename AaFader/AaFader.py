from __future__ import with_statement

import os
import time
import Live

from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent

from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.SliderElement import SliderElement
from _Framework.SubjectSlot import subject_slot

from SpecialMixerComponent import SpecialMixerComponent
from SpecialSessionComponent import SpecialSessionComponent

class AaFader(ControlSurface):
  __doc__ = "AaFader controller"

  def __init__(self, _oCtrlInstance):
    ControlSurface.__init__(self, _oCtrlInstance)
    self.m_oCtrlInstance = _oCtrlInstance
    self.m_sProductName  = 'AaFader'

    with self.component_guard():
      #self.xlog('initializing controller ...')
      self.load_config()
      self.setup_session()
      self.setup_mixer()
      self.m_oSession.set_mixer(self.m_oMixer)
      self.setup_device()
      self.__add_listeners()
      self.set_highlighting_session_component(self.m_oSession)
      self.xlog('initialized controller!')

  def disconnect(self):
    #self.xlog('disconnecting ...')
    self.remove_highlight()
    self.m_oButStopTotal.remove_value_listener(self._on_stop_total)
    self.m_oButBank1Sync.remove_value_listener(self._on_bank_1_sync)
    self.m_oButBank2Sync.remove_value_listener(self._on_bank_2_sync)
    self.m_oButBank3Sync.remove_value_listener(self._on_bank_3_sync)
    self.m_oButBank4Sync.remove_value_listener(self._on_bank_4_sync)
    self.__remove_listeners()
    ControlSurface.disconnect(self)
    self.xlog('disconnected!')

  def load_config(self):
    self.m_nNumTracks = 8

    # default configuration ************************************************
    self.m_hCfg = {
      'oCtrlInst'   : self.m_oCtrlInstance,
      'sProductName': self.m_sProductName,
      'sProductDir' : 'AaConfig/%s' % (self.m_sProductName),
      'NumScenes'   : 1,

      # fixed config
      'Bank0Channel': 0,
      'VolOffset'   : 17,
      'SessionLeft' : 25, 'SessionRight': 26,
      'StopTotal'   : 27,

      # bank 1
      'Bank1Channel': 0,  'Bank1Sync'   : 28, # MIDI-CHANNEL 1

      'Tempo1'      : 33, # Rotary Group 1
      'Tempo2'      : 34,
      'TrackSel'    : 35,
      'SceneSel'    : 36,
      'TrackPan'    : 37,
      'ClipGain'    : 38,
      'ClipPit'     : 39,
      'ClipDet'     : 40,

      'Tempo1Rst'   : 41, # Rotary Buttons Group 1
      'Tempo2Rst'   : 42,
      'TrackSelRst' : 43,
      'SceneSelRst' : 44,
      'TrackPanRst' : 45,
      'ClipGainRst' : 46,
      'ClipPitRst'  : 47,
      'ClipDetRst'  : 48,

      'MuteOffset'  : 1,  'SoloOffset'  : 9,  # Buttons

      # bank 2
      'Bank2Channel': 1,  'Bank2Sync'   : 29, # MIDI-CHANNEL 2
      'StopOffset'  : 1,  'SelOffset'   : 9,  # Buttons

      # bank 3
      'Bank3Channel': 2,  'Bank3Sync'   : 30, # MIDI-CHANNEL 3
      'InputOffset' : 1,  'ArmOffset'   : 9,  # Buttons

      # bank 4
      'Bank4Channel': 3,  'Bank4Sync'   : 31, # MIDI-CHANNEL 4
      'AvVelOffset' : 33,                     # Rotary Group 1
      'AvIncrOffset': 1,  'AvDecrOffset': 9,  # Buttons
    }

    #self.xlog('loading config ...')
    sHome   = os.getenv('HOME')
    sFilePath = '%s/%s/config.txt' % (sHome, self.m_hCfg['sProductDir'])
    bFileExists = os.path.isfile(sFilePath)
    if (bFileExists == False):
      self.log('> config file "%s" not found!' % (sFilePath))
      return # config file does not exist, nothing else to do here!

    # parse config file, line by line
    self.xlog('reading: "%s"' % (sFilePath))
    oFile = open(sFilePath, 'r')
    for sLine in oFile:
      sLine = sLine.strip()
      if (len(sLine) == 0): continue
      if (sLine[0] == '#'): continue
      # the first token in the line is the name of the config feature
      aConfig = sLine.split('#')
      aTokens = aConfig[0].split('|')
      # do not parse lines with less than 2 tokens
      if (len(aTokens) < 2): continue
      sName  = aTokens[0].strip()
      sValue = aTokens[1].strip()
      # parse the value of the config feature
      sKey = ''.join(sToken.capitalize() for sToken in sName.split('_'))
      #self.xlog('   parsed: %16s => %16s | %s' % (sName, sKey, sValue))
      self.m_hCfg[sKey] = int(sValue)
    self.xlog('config loaded succesfully!')

  def setup_session(self):
    self.m_oSession = SpecialSessionComponent(self.m_nNumTracks, self.m_hCfg['NumScenes'])
    self.m_oSession.name = 'Session'
    oSession = self.m_oSession
    self.m_hCfg['oSession'] = oSession
    self.m_oSession.set_tempo_1  (self.create_encoder('Tempo1',   0))
    self.m_oSession.set_tempo_2  (self.create_encoder('Tempo2',   0))
    self.m_oSession.set_track_sel(self.create_encoder('TrackSel', 0))
    self.m_oSession.set_scene_sel(self.create_encoder('SceneSel', 0))

    oSession.set_page_left_button (self.create_toggle('SessionLeft' , 0))
    oSession.set_page_right_button(self.create_toggle('SessionRight', 0))

    self.m_oButStopTotal = self.create_button('StopTotal', 0)
    self._on_stop_total.subject = self.m_oButStopTotal
    self.m_oButBank1Sync = self.create_button('Bank1Sync', 0)
    self._on_bank_1_sync.subject = self.m_oButBank1Sync
    self.m_oButBank2Sync = self.create_button('Bank2Sync', 0)
    self._on_bank_2_sync.subject = self.m_oButBank2Sync
    self.m_oButBank3Sync = self.create_button('Bank3Sync', 0)
    self._on_bank_3_sync.subject = self.m_oButBank3Sync
    self.m_oButBank4Sync = self.create_button('Bank4Sync', 0)
    self._on_bank_4_sync.subject = self.m_oButBank4Sync

  def setup_mixer(self):
    self.m_oMixer = SpecialMixerComponent(self.m_nNumTracks, self.m_hCfg)
    self.m_oMixer.name = 'Mixer'
    oMixer = self.m_oMixer

    for nTrackIdx in range(self.m_nNumTracks):
      oStrip = oMixer.channel_strip(nTrackIdx)
      oStrip.name = 'Channel_Strip_' + str(nTrackIdx)
      oStrip.set_index(nTrackIdx)

      # bank 1, 2, 3 & 4
      oStrip.set_volume_control(self.create_slider ('VolOffset'   , 0, nTrackIdx))

      # bank 1
      oStrip.set_mute_button   (self.create_toggle ('MuteOffset'  , 1, nTrackIdx))
      oStrip.set_solo_button   (self.create_toggle ('SoloOffset'  , 1, nTrackIdx))

      # bank 2
      oStrip.set_stop_button   (self.create_toggle ('StopOffset'  , 2, nTrackIdx))
      oStrip.set_sel_button    (self.create_toggle ('SelOffset'   , 2, nTrackIdx))

      # bank 3
      oStrip.set_input_control (self.create_toggle ('InputOffset' , 3, nTrackIdx))
      oStrip.set_arm_control   (self.create_toggle ('ArmOffset'   , 3, nTrackIdx))

      # bank 4
      oStrip.set_av_vel_control(self.create_encoder('AvVelOffset' , 4, nTrackIdx))

      oStrip.set_av_incr_toggle(self.create_toggle ('AvIncrOffset', 4, nTrackIdx))
      oStrip.set_av_decr_toggle(self.create_toggle ('AvDecrOffset', 4, nTrackIdx))

      oStrip.set_invert_mute_feedback(True)

  def setup_device(self):
    self.m_oDevice = DeviceComponent()
    self.m_oDevice.name = 'Device_Component'
    self.set_device_component(self.m_oDevice)

  def move_to_track_offset(self, _nTrackOffsetAbs):
    self.m_oSession.set_offsets(_nTrackOffsetAbs, 0)

  # ****************************************************************
  #        nBeatDelta
  #        |<--------->|
  # Beat    Beat    Beat    Beat
  #  |       |       |       |
  #  V       V       V       V
  # -------------------------------------------->
  #  : ^   ^   ^ : ^   ^   ^ : ^   ^   ^ :
  #  : |   |   | : |   |   | : |   |   | :   <=== update_sync_tasks() [~ every 100 ms]
  #
  #   #fTime = time.time() # time as float (seconds), decimals are milliseconds
  #   #nTime = int(fTime)
  #   #sTime = datetime.datetime.fromtimestamp(fTime).strftime('%Y-%m-%d %H:%M:%S.%f')
  #   #Live.Base.log("(%d) %f: %s" % (nTime, fTime, sTime))
  # ****************************************************************

  def update_display(self): # This function is run every 100ms
    self.m_oMixer.update_sync_tasks()

  # ****************************************************************

  @subject_slot(u'value')
  def _on_stop_total(self, _nValue):
    if (_nValue < 64): return # do not process "toggle off"
    self.song().stop_all_clips()
    self.song().stop_playing()

  @subject_slot(u'value')
  def _on_bank_1_sync(self, _nValue):
    if (_nValue < 64): return # do not process "toggle off"
    self._sync_bank(1)

  @subject_slot(u'value')
  def _on_bank_2_sync(self, _nValue):
    if (_nValue < 64): return # do not process "toggle off"
    self._sync_bank(2)

  @subject_slot(u'value')
  def _on_bank_3_sync(self, _nValue):
    if (_nValue < 64): return # do not process "toggle off"
    self._sync_bank(3)

  @subject_slot(u'value')
  def _on_bank_4_sync(self, _nValue):
    if (_nValue < 64): return # do not process "toggle off"
    self._sync_bank(4)

  def _sync_bank(self, _nIdx):
    # update page buttons
    nLeftValue  = 127 if self.m_oSession._can_scroll_page_left()  else 0
    nRightValue = 127 if self.m_oSession._can_scroll_page_right() else 0
    self.m_oSession._page_left_button.send_value(nLeftValue , True)
    self.m_oSession._page_right_button.send_value(nRightValue, True)

    # update track balues
    self.m_oMixer.send_bank_values(_nIdx)
    self.alert('> Synced Bank %d' % (_nIdx))

  # ****************************************************************

  def __add_listeners(self):
    self.__remove_listeners()
    if (not self.song().tracks_has_listener(self.__on_tracks_change)):
      self.song().add_tracks_listener(self.__on_tracks_change)
    if (not self.song().view.selected_track_has_listener(self.__on_sel_track_change)):
      self.song().view.add_selected_track_listener(self.__on_sel_track_change)
    if (not self.song().scenes_has_listener(self.__on_scenes_change)):
      self.song().add_scenes_listener(self.__on_scenes_change)
    if (not self.song().view.selected_scene_has_listener(self.__on_sel_scene_change)):
      self.song().view.add_selected_scene_listener(self.__on_sel_scene_change)

  def __remove_listeners(self):
    if (self.song().tracks_has_listener(self.__on_tracks_change)):
      self.song().remove_tracks_listener(self.__on_tracks_change)
    if (self.song().view.selected_track_has_listener(self.__on_sel_track_change)):
      self.song().view.remove_selected_track_listener(self.__on_sel_track_change)
    if (self.song().scenes_has_listener(self.__on_scenes_change)):
      self.song().remove_scenes_listener(self.__on_scenes_change)
    if (self.song().view.selected_scene_has_listener(self.__on_sel_scene_change)):
      self.song().view.remove_selected_scene_listener(self.__on_sel_scene_change)

  def __on_tracks_change(self):
    self.__add_listeners()
    self.__update_track_values()

  def __on_sel_track_change(self):
    self.__update_track_values()

  def __update_track_values(self):
    self.m_oSession.on_sel_track_change()
    self.m_oMixer.on_sel_track_change()

  def __on_scenes_change(self):
    self.__add_listeners()
    self.__update_scene_values()

  def __on_sel_scene_change(self):
    self.__update_scene_values()

  def __update_scene_values(self):
    self.m_oMixer.on_sel_scene_change()

  # ****************************************************************

  def get_el_config(self, _sName, _nBank, _nIndex = None):
    nMidiType = MIDI_CC_TYPE
    nChannel  = self.m_hCfg['Bank%dChannel' % (_nBank)]
    sKey      = _sName
    nOffset   = 0
    if (_nIndex != None):
      nOffset = _nIndex
      _sName  = '%s_%d' % (_sName, _nIndex)
    return (nMidiType, nChannel, sKey, nOffset, _sName)

  def create_button(self, _sName, _nBank, _nIndex = None):
    bIsMomentary = True
    nMidiType, nChannel, sKey, nOffset, sName = self.get_el_config(_sName, _nBank, _nIndex)
    return ButtonElement(bIsMomentary, nMidiType, nChannel, self.m_hCfg[sKey] + nOffset, name = _sName)

  def create_encoder(self, _sName, _nBank, _nIndex = None):
    return self.create_button(_sName, _nBank, _nIndex)

  def create_toggle(self, _sName, _nBank, _nIndex = None):
    bIsMomentary = False
    nMidiType, nChannel, sKey, nOffset, sName = self.get_el_config(_sName, _nBank, _nIndex)
    return ButtonElement(bIsMomentary, nMidiType, nChannel, self.m_hCfg[sKey] + nOffset, name = _sName)

  def create_slider(self, _sName, _nBank, _nIndex = None):
    nMidiType, nChannel, sKey, nOffset, sName = self.get_el_config(_sName, _nBank, _nIndex)
    return SliderElement(nMidiType, nChannel, self.m_hCfg[sKey] + nOffset, name = _sName)

  # ****************************************************************

  def sel_clip_slot(self):
    return self.song().view.highlighted_clip_slot

  def scenes(self):
    return self.song().scenes

  def sel_scene(self, _oScene = None):
    if (_oScene != None):
      self.song().view.selected_scene = _oScene
    return self.song().view.selected_scene

  def sel_scene_idx_abs(self):
    aAllScenes = self.scenes()
    oSelScene  = self.sel_scene()
    return list(aAllScenes).index(oSelScene)

  def master(self):
    return self.song().master_track

  def tracks(self):
    return self.song().tracks #visible_tracks

  def returns(self):
    return self.song().return_tracks

  def tracks_and_returns(self):
    return tuple(self.tracks()) + tuple(self.returns())

  def sel_track(self, _oTrack = None):
    if (_oTrack != None):
      self.song().view.selected_track = _oTrack
    return self.song().view.selected_track

  def sel_track_idx_abs(self):
    aAllTracks = self.tracks_and_returns()
    oSelTrack  = self.sel_track()
    return list(aAllTracks).index(oSelTrack)

  def remove_highlight(self):
    _nTrackOffset  = -1
    _nSceneOffset  = -1
    _nNumVisTracks = -1
    _nNumVisScenes = -1
    _bIncludeReturnTracks = False
    self.m_oCtrlInstance.set_session_highlight(_nTrackOffset, _nSceneOffset, _nNumVisTracks, _nNumVisScenes, _bIncludeReturnTracks)

  def log(self, _sMessage):
    Live.Base.log(_sMessage)

  def xlog(self, _sMessage):
    self.log('> %s: %s' % (self.m_sProductName, _sMessage))

  def alert(self, sMessage):
    self.m_oCtrlInstance.show_message(sMessage)

