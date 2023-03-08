import Live
from _Framework.TransportComponent import TransportComponent

class SpecialTransportComponent(TransportComponent):
  __doc__ = 'TransportComponent'

  def __init__(self, _hCfg):
    TransportComponent.__init__(self)
    self.m_hCfg      = _hCfg
    self.m_oCtrlInst = _hCfg['oCtrlInst']
    return None

  def disconnect(self):
    TransportComponent.disconnect(self)

