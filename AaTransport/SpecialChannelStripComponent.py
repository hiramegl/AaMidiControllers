from _Framework.ChannelStripComponent import ChannelStripComponent

TRACK_FOLD_DELAY = 5

class SpecialChannelStripComponent(ChannelStripComponent):
  'Subclass of channel strip component'
  __module__ = __name__

  def __init__(self):
    ChannelStripComponent.__init__(self)
    self.m_oButReset  = None
    self.m_oSurfaceCtrl = None
    self._toggle_fold_ticks_delay = -1
    self._register_timer_callback(self._on_timer)

  def disconnect(self):
    self._unregister_timer_callback(self._on_timer)
    self._connect_ctl(self.m_oButReset, None, self._on_reset_value)
    self.m_oButReset  = None
    self.m_oSurfaceCtrl = None
    ChannelStripComponent.disconnect(self)

  def set_surface_ctrl(self, _oSurfaceCtrl):
    self.m_oSurfaceCtrl = _oSurfaceCtrl;

  def _select_value(self, value):
    ChannelStripComponent._select_value(self, value)
    if (self.is_enabled() and (self._track != None)):
      if (self._track.is_foldable and (self._select_button.is_momentary() and (value != 0))):
        self._toggle_fold_ticks_delay = TRACK_FOLD_DELAY
      else:
        self._toggle_fold_ticks_delay = -1
    oView = self.m_oSurfaceCtrl.application().view
    oView.show_view('Detail')
    oView.focus_view('Detail')
    oView.show_view('Detail/DeviceChain')
    oView.focus_view('Detail/DeviceChain')

  def _on_timer(self):
    if (self.is_enabled() and (self._track != None)):
      if (self._toggle_fold_ticks_delay > -1):
        assert self._track.is_foldable
        if (self._toggle_fold_ticks_delay == 0):
          self._track.fold_state = (not self._track.fold_state)
        self._toggle_fold_ticks_delay -= 1

  # **************************************************************************

  def set_reset_control(self, _oButReset):
    self.m_oButReset = self._connect_ctl(self.m_oButReset, _oButReset, self._on_reset_value, True)

  # **************************************************************************

  def _connect_ctl(self, _oCurBut, _oNewBut, _fListener, _bOn = None):
    if (_oCurBut != _oNewBut):
      if (_oCurBut != None):
        _oCurBut.remove_value_listener(_fListener)
        _oCurBut.turn_off()
      if (_oNewBut != None):
        _oNewBut.add_value_listener(_fListener)
        if _bOn != None:
          if _bOn == True:
            _oNewBut.turn_on()
          else:
            _oNewBut.turn_off()
    return _oNewBut

  # **************************************************************************

  def _on_reset_value(self, _nValue):
    assert (self.m_oButReset != None)
    oTrack = self.get_track_or_return_or_none()
    if oTrack == None: return
    aDevices = oTrack.devices
    for nDeviceIdx in range(len(aDevices)):
      oDevice = aDevices[nDeviceIdx]
      aParams = oDevice.parameters
      for nParamIdx in range(len(aParams)):
        oParam = aParams[nParamIdx]
        sParam = self.to_ascii(oParam.name)
        if sParam == 'Device On':
          oParam.value = 0 # turn off the device
          break

  # **************************************************************************

  def to_ascii(self, _sText, _nTruncate = 0):
    sAscii = ''.join([(ord(cChar) > 127 and '' or cChar.encode('utf-8')) for cChar in _sText])
    if (_nTruncate == 0):
      return sAscii
    else:
      return sAscii[:_nTruncate]

  def get_track_or_return_or_none(self, _oControl = None, _nResetValue = None):
    if (not self.is_enabled()):
      # disabled! nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    if (self._track == None):
      # no track! nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    if (self._track == self.song().master_track):
      # is master track, nothing else to do!
      return self.send_reset_value(_oControl, _nResetValue)

    return self._track

  def send_reset_value(self, _oControl, _nResetValue):
    if (_oControl != None):
      _oControl.send_value(_nResetValue, True)
    return None

