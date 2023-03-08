import time
import Live

from _Framework.ChannelStripComponent import ChannelStripComponent

TRACK_FOLD_DELAY = 5

def release_control(control):
  if control != None:
    control.release_parameter()

class SpecialChannelStripComponent(ChannelStripComponent):
  ' Subclass of channel strip component using select button for (un)folding tracks '
  __module__ = __name__

  def __init__(self, _hCfg):
    ChannelStripComponent.__init__(self)
    self.m_hCfg      = _hCfg
    self.m_oSession  = _hCfg['oSession']
    self.m_oCtrlInst = _hCfg['oCtrlInst']
    self.m_oSong     = _hCfg['oCtrlInst'].song()
    self.m_bBusy     = False

    self.m_nIndex    = -1
    self.m_hAutoVol  = {}
    self._toggle_fold_ticks_delay = -1
    self._register_timer_callback(self._on_timer)

    self.m_oStopControl   = None
    self.m_oSelControl    = None
    self.m_oInputControl  = None
    self.m_oArmControl    = None

    self.m_oAvVelControl  = None
    self.m_oAvIncrToggle  = None
    self.m_oAvDecrToggle  = None
    self.m_oVolumeReset   = None

    def make_control_slot(name):
      return self.register_slot(None, getattr(self, u'_%s_value' % name), u'value')

    self._stop_button_slot    = make_control_slot(u'stop')
    self._sel_button_slot     = make_control_slot(u'sel')
    self._input_button_slot   = make_control_slot(u'input')
    self._arm_button_slot     = make_control_slot(u'arm')

    self._av_vel_control_slot = make_control_slot(u'av_vel')
    self._av_incr_toggle_slot = make_control_slot(u'av_incr')
    self._av_decr_toggle_slot = make_control_slot(u'av_decr')
    self._volume_reset_slot   = make_control_slot(u'volume_reset')

  def disconnect(self):
    self._unregister_timer_callback(self._on_timer)

    self.m_oStopControl   = None
    self.m_oSelControl    = None
    self.m_oInputControl  = None
    self.m_oArmControl    = None

    self.m_oAvVelControl  = None
    self.m_oAvIncrToggle  = None
    self.m_oAvDecrToggle  = None
    self.m_oVolumeReset   = None

    ChannelStripComponent.disconnect(self)

  def set_index(self, _nIndex):
    self.m_nIndex = _nIndex

  def _select_value(self, value):
    ChannelStripComponent._select_value(self, value)
    if (self.is_enabled() and (self._track != None)):
      if (self._track.is_foldable and (self._select_button.is_momentary() and (value != 0))):
        self._toggle_fold_ticks_delay = TRACK_FOLD_DELAY
      else:
        self._toggle_fold_ticks_delay = -1

  def _on_timer(self):
    if (self.is_enabled() and (self._track != None)):
      if (self._toggle_fold_ticks_delay > -1):
        assert self._track.is_foldable
        if (self._toggle_fold_ticks_delay == 0):
          self._track.fold_state = (not self._track.fold_state)
        self._toggle_fold_ticks_delay -= 1

  def _connect_parameters(self):
    ChannelStripComponent._connect_parameters(self)
    if not self._allow_updates: return
    if not self.is_enabled(): return

    # here we know for sure that the track is valid!
    self._on_av_vel_changed()  # depends on track
    self._on_av_incr_changed() # depends on track
    self._on_av_decr_changed() # depends on track

  # SYNC TASKS ***************************************************************

  def update_sync_tasks(self):
    if (self.m_bBusy == True): return # busy updating delta

    for nTrackIdxAbs in self.m_hAutoVol:
      hAutoVol = self.m_hAutoVol[nTrackIdxAbs]
      if (not hAutoVol['on']): continue # not on, check the next one
      oTrack  = self.get_track(nTrackIdxAbs)
      nCurVol = oTrack.mixer_device.volume.value
      nDelta  = hAutoVol['delta']
      nNewVol = nCurVol + nDelta
      if (nDelta < 0.0):
        if (nNewVol < 0.0):
          hAutoVol['on'] = False
          nNewVol        = 0.0
          nTimeSpan      = time.time() - hAutoVol['start']
          self.m_oAvIncrToggle.send_value(0, True)
          self.m_oAvDecrToggle.send_value(0, True)
          self.alert('%s: reached MIN VOL in %f [sec]!' % (oTrack.name, nTimeSpan))
        oTrack.mixer_device.volume.value = nNewVol
      else:
        if (nNewVol > 1.0):
          hAutoVol['on'] = False
          nNewVol        = 1.0
          nTimeSpan      = time.time() - hAutoVol['start']
          self.m_oAvIncrToggle.send_value(0, True)
          self.m_oAvDecrToggle.send_value(0, True)
          self.alert('%s: reached MAX VOL in %f [sec]!' % (oTrack.name, nTimeSpan))
        oTrack.mixer_device.volume.value = nNewVol

  # AUTO VOLUME **************************************************************

  def get_autovol(self, _nTrackIdxAbs):
    if (not _nTrackIdxAbs in self.m_hAutoVol):
      self.m_hAutoVol[_nTrackIdxAbs] = {
        'vel'  : 20,  # default is 20 bars
        'on'   : False,
        'delta': 0.0,
        'start': 0.0,
      }
    return self.m_hAutoVol[_nTrackIdxAbs]

  def compute_av_delta(self, _oTrack, _nTrackIdxAbs):
    hAutoVol  = self.get_autovol(_nTrackIdxAbs)
    if (not hAutoVol['on']): return # not in use, do not update any parameter

    self.m_bBusy = True

    nVel      = hAutoVol['vel']   # in bars
    nStart    = hAutoVol['start'] # in seconds
    nTgtVol   = hAutoVol['tgt']   # target volume
    nCurrVol  = _oTrack.mixer_device.volume.value
    nVel      = 0.5 if (nVel == 0) else nVel

    nTempo    = self.m_oSong.tempo  # in BPM
    nBarSpan  = (60.0 / nTempo) * 4.0 # in seconds
    nTimeSpan = nVel * nBarSpan     # in seconds
    nVolDelta = nTgtVol - nCurrVol
    nDelta    = (nVolDelta / nTimeSpan) / 10.0 # divide with 10.0 since update executes every 100 ms

    hAutoVol['delta'] = nDelta
    sCmd = 'DECR' if (nDelta < 0.0) else 'INCR'
    self.alert('> VOL %s (%f -> %f) in %f [s] => %f [bars]' % (sCmd, nCurrVol, nTgtVol, nTimeSpan, nVel))

    self.m_bBusy = False

  # LISTENERS ****************************************************************

  def on_sel_track_change(self):
    self._on_stop_changed()  # depends on track
    self._on_sel_changed()   # depends on track
    self._on_input_changed() # depends on track
    self._on_arm_changed()   # depends on track

  def send_bank_values(self, _nBank):
    oTrack = self.get_track_or_none()
    if (_nBank == 1):
      nMute, nSolo, nVol = (0, 0, 0)
      if (oTrack != None):
        nMute  = 0   if oTrack.mute else 127
        nSolo  = 127 if oTrack.solo else 0
        nVol   = int(oTrack.mixer_device.volume.value * 127.0)
      self._mute_button.send_value(nMute, True)
      self._solo_button.send_value(nSolo, True)
      self._volume_control.send_value(nVol, True)
    elif (_nBank == 2):
      nStop, nSel, nVol = (0, 0, 0)
      if (oTrack != None):
        nStop = 127
        nSel  = 127
        nVol  = int(oTrack.mixer_device.volume.value * 127.0)
      self._volume_control.send_value(nVol,  True)
      self.m_oStopControl.send_value (nStop, True)
      self.m_oSelControl.send_value  (nSel,  True)
    elif (_nBank == 3):
      nInput, nArm, nVol = (0, 0, 0)
      if (oTrack != None):
        nInput = 127
        nArm = 127 if oTrack.arm else 0
        nVol = int(oTrack.mixer_device.volume.value * 127.0)
      self._volume_control.send_value(nVol, True)
    elif (_nBank == 4):
      if (oTrack != None):
        nVol = int(oTrack.mixer_device.volume.value * 127.0)
      self._volume_control.send_value(nVol, True)
      self._on_av_vel_changed()
      self._on_av_incr_changed()
      self._on_av_decr_changed()

  # TRACK STOP ***************************************************************

  def set_stop_button(self, _oControl):
    if _oControl != self.m_oStopControl:
      release_control(self.m_oStopControl)
      self.m_oStopControl = _oControl
      self._stop_button_slot.subject = _oControl
      self.update()

  def _stop_value(self, _nValue):
    assert self.m_oStopControl != None
    assert isinstance(_nValue, int)
    oTrack = self.get_track_or_none(self.m_oStopControl, 0)
    if (oTrack == None):
      self.m_oStopControl.send_value(0, True)
      return None
    oTrack.stop_all_clips()
    self.m_oStopControl.send_value(127, True)

  def _on_stop_changed(self):
    if (self.m_oStopControl == None):
      return
    oTrack = self.get_track_or_none(self.m_oStopControl, 0)
    if (oTrack == None or self.m_oSession == None):
      self.m_oStopControl.send_value(0, True)
      return None
    self.m_oStopControl.send_value(127, True)

  # TRACK SELECT *************************************************************

  def set_sel_button(self, _oControl):
    if _oControl != self.m_oSelControl:
      release_control(self.m_oSelControl)
      self.m_oSelControl = _oControl
      self._sel_button_slot.subject = _oControl
      self.update()

  def _sel_value(self, _nValue):
    assert self.m_oSelControl != None
    assert isinstance(_nValue, int)
    oTrack = self.get_track_or_none(self.m_oSelControl, 0)
    if (oTrack == None):
      return None
    self.song().view.selected_track = oTrack
    self.m_oSelControl.send_value(127, True)

  def _on_sel_changed(self):
    if (self.m_oSelControl == None):
      return
    oTrack = self.get_track_or_none(self.m_oSelControl, 0)
    if (oTrack == None or self.m_oSession == None):
      self.m_oSelControl.send_value(0, True)
      return None
    self.m_oSelControl.send_value(127, True)

  # INPUT SELECT *************************************************************

  def set_input_control(self, _oControl):
    if _oControl != self.m_oInputControl:
      release_control(self.m_oInputControl)
      self.m_oInputControl = _oControl
      self._input_button_slot.subject = _oControl
      self.update()

  def _input_value(self, _nValue):
    assert self.m_oInputControl != None
    assert isinstance(_nValue, int)
    oTrack = self.get_track_or_none(self.m_oInputControl, 0)
    if (oTrack == None):
      self.m_oInputControl.send_value(0, True)
      return None
    nMonitor = (oTrack.current_monitoring_state - 1) % 3
    oTrack.current_monitoring_state = nMonitor
    self.m_oInputControl.send_value(127, True)

  def _on_input_changed(self):
    if (self.m_oInputControl == None):
      return
    oTrack = self.get_track_or_none(self.m_oInputControl, 0)
    if (oTrack == None or self.m_oSession == None):
      self.m_oInputControl.send_value(0, True)
      return None
    self.m_oInputControl.send_value(127, True)

  # ARM **********************************************************************

  def set_arm_control(self, _oControl):
    if _oControl != self.m_oArmControl:
      release_control(self.m_oArmControl)
      self.m_oArmControl = _oControl
      self._arm_button_slot.subject = _oControl
      self.update()

  def _arm_value(self, _nValue):
    assert self.m_oArmControl != None
    assert isinstance(_nValue, int)
    oTrack = self.get_track_or_none(self.m_oArmControl, 0)
    if (oTrack == None):
      self.m_oArmControl.send_value(0, True)
      return None
    bArm = oTrack.arm
    oTrack.arm = False if bArm else True
    self.m_hCfg['Mixer'].update_arm_buttons()

  def _on_arm_changed(self):
    if (self.m_oArmControl == None):
      return
    oTrack = self.get_track_or_none(self.m_oArmControl, 0)
    if (oTrack == None or self.m_oSession == None):
      self.m_oArmControl.send_value(0, True)
      return None
    nArm = 127 if oTrack.arm else 0
    self.m_oArmControl.send_value(nArm, True)

  # AUTO-VOLUME VELOCITY *****************************************************

  def set_av_vel_control(self, _oControl):
    if _oControl != self.m_oAvVelControl:
      release_control(self.m_oAvVelControl)
      self.m_oAvVelControl = _oControl
      self._av_vel_control_slot.subject = _oControl
      self.update()

  def _av_vel_value(self, _nValue):
    assert self.m_oAvVelControl != None
    assert isinstance(_nValue, int)
    oTrack = self.get_track_or_none()
    if (oTrack == None):
      return
    # edit the auto-volume velocity for the current track
    nTrackIdxAbs = self.m_oSession.track_offset() + self.m_nIndex
    nAvVel       = _nValue / 2 # 0 ... 63
    hAutoVol     = self.get_autovol(nTrackIdxAbs)

    hAutoVol['vel'] = nAvVel
    self.alert('> Track: "%s", AV-VEL: %f' % (oTrack.name, nAvVel))
    self.compute_av_delta(oTrack, nTrackIdxAbs)

  def _on_av_vel_changed(self):
    oTrack = self.get_track_or_none(self.m_oAvVelControl, 0)
    if (oTrack == None or self.m_oAvVelControl == None):
      return
    nTrackIdxAbs = self.m_oSession.track_offset() + self.m_nIndex
    hAutoVol     = self.get_autovol(nTrackIdxAbs)
    nValue       = hAutoVol['vel'] * 2 # MIDI VALUE

    self.m_oAvVelControl.send_value(nValue, True)

  # VOLUME RESET *************************************************************

  def set_volume_reset(self, _oReset):
    if _oReset != self.m_oVolumeReset:
      release_control(self.m_oVolumeReset)
      self.m_oVolumeReset = _oReset
      self._volume_reset_slot.subject = _oReset
      self.update()

  def _volume_reset_value(self, _nValue):
    # this method process both "on" and "off" values since
    # the volume reset is assigned to a toggle. (Problem with BFC2000)
    assert self.m_oVolumeReset != None
    assert isinstance(_nValue, int)
    oTrack = self.get_track_or_none()
    if (oTrack == None):
      return

    self.m_bBusy = True

    # stop auto-volume update and reset the volume value
    nTrackIdxAbs = self.m_oSession.track_offset() + self.m_nIndex
    hAutoVol   = self.get_autovol(nTrackIdxAbs)

    # update params
    hAutoVol['on']  = False
    hAutoVol['delta'] = 0.0
    hAutoVol['start'] = 0.0

    oTrack.mixer_device.volume.value = 0.85 # 0 dB
    self.m_oAvIncrToggle.send_value(0, True)
    self.m_oAvDecrToggle.send_value(0, True)

    self.m_bBusy = False

  # no need to update the volume reset toggle!

  # AUTO-VOLUME INCREASE *****************************************************

  def set_av_incr_toggle(self, _oToggle):
    if _oToggle != self.m_oAvIncrToggle:
      release_control(self.m_oAvIncrToggle)
      self.m_oAvIncrToggle = _oToggle
      self._av_incr_toggle_slot.subject = _oToggle
      self.update()

  def _av_incr_value(self, _nValue):
    assert self.m_oAvIncrToggle != None
    assert isinstance(_nValue, int)
    oTrack = self.get_track_or_none()
    if (oTrack == None):
      return
    nTrackIdxAbs = self.m_oSession.track_offset() + self.m_nIndex
    hAutoVol     = self.get_autovol(nTrackIdxAbs)

    if (hAutoVol['on']):
      hAutoVol['on'] = False
      self.alert('> Track: "%s", STOP AV' % (oTrack.name))
      self.m_oAvIncrToggle.send_value(0, True)
      self.m_oAvDecrToggle.send_value(0, True)
    else:
      hAutoVol['on']    = True
      hAutoVol['start'] = time.time()
      hAutoVol['tgt']   = 1.0
      self.compute_av_delta(oTrack, nTrackIdxAbs)

  def _on_av_incr_changed(self):
    oTrack = self.get_track_or_none(self.m_oAvIncrToggle, 0)
    if (oTrack == None or self.m_oAvIncrToggle == None):
      return
    nTrackIdxAbs = self.m_oSession.track_offset() + self.m_nIndex
    hAutoVol     = self.get_autovol(nTrackIdxAbs)
    nValue       = 127 if (hAutoVol['on'] and hAutoVol['delta'] > 0.0) else 0
    self.m_oAvIncrToggle.send_value(nValue, True)

  # AUTO-VOLUME DECREASE *****************************************************

  def set_av_decr_toggle(self, _oToggle):
    if _oToggle != self.m_oAvDecrToggle:
      release_control(self.m_oAvDecrToggle)
      self.m_oAvDecrToggle = _oToggle
      self._av_decr_toggle_slot.subject = _oToggle
      self.update()

  def _av_decr_value(self, _nValue):
    assert self.m_oAvDecrToggle != None
    assert isinstance(_nValue, int)
    oTrack = self.get_track_or_none()
    if (oTrack == None):
      return
    nTrackIdxAbs = self.m_oSession.track_offset() + self.m_nIndex
    hAutoVol     = self.get_autovol(nTrackIdxAbs)

    if (hAutoVol['on']):
      hAutoVol['on'] = False
      self.alert('> Track: "%s", STOP AV' % (oTrack.name))
      self.m_oAvIncrToggle.send_value(0, True)
      self.m_oAvDecrToggle.send_value(0, True)
    else:
      hAutoVol['on']    = True
      hAutoVol['start'] = time.time()
      hAutoVol['tgt']   = 0.0
      self.compute_av_delta(oTrack, nTrackIdxAbs)

  def _on_av_decr_changed(self):
    oTrack = self.get_track_or_none(self.m_oAvDecrToggle, 0)
    if (oTrack == None or self.m_oAvDecrToggle == None):
      return
    nTrackIdxAbs = self.m_oSession.track_offset() + self.m_nIndex
    hAutoVol     = self.get_autovol(nTrackIdxAbs)
    nValue       = 127 if (hAutoVol['on'] and hAutoVol['delta'] < 0.0) else 0
    self.m_oAvDecrToggle.send_value(nValue, True)

  # ****************************************************************

  def to_ascii(self, _sText, _nTruncate = 0):
    sAscii = ''.join([(ord(cChar) > 127 and '' or cChar.encode('utf-8')) for cChar in _sText])
    if (_nTruncate == 0):
      return sAscii
    else:
      return sAscii[:_nTruncate]

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
    return self.song().tracks # visible_tracks

  def returns(self):
    return self.song().return_tracks

  def tracks_and_returns(self):
    return tuple(self.tracks()) + tuple(self.returns())

  def get_track(self, _nTrackIdxAbs):
    aTracks = self.tracks()
    return aTracks[_nTrackIdxAbs]

  def sel_track(self, _oTrack = None):
    if (_oTrack != None):
      self.song().view.selected_track = _oTrack
    return self.song().view.selected_track

  def sel_track_idx_abs(self):
    aAllTracks = self.tracks_and_returns()
    oSelTrack  = self.sel_track()
    return list(aAllTracks).index(oSelTrack)

  def get_track_or_none(self, _oControl = None, _nResetValue = None):
    if (not self.is_enabled()):
      # disabled! nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    if (self._track == None):
      # no track! nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    if (self._track == self.song().master_track):
      # is master track, nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    if (not self._track in self.tracks()):
      # is a return track, nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    return self._track

  def get_clip_or_none(self, _oControl = None, _nResetValue = None):
    oTrack = self.get_track_or_none(_oControl, _nResetValue)
    if (oTrack == None):
      return None

    nSelSceneIdxAbs = self.sel_scene_idx_abs()
    oClipSlot       = oTrack.clip_slots[nSelSceneIdxAbs]
    if (not oClipSlot.has_clip):
      # empty clip, nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    return oClipSlot.clip

  def send_reset_value(self, _oControl, _nResetValue):
    if (_oControl != None):
      _oControl.send_value(_nResetValue, True)
    return None

  def alert(self, sMessage):
    self.m_oCtrlInst.show_message(sMessage)
