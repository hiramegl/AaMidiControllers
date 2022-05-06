from _Framework.MixerComponent import MixerComponent
from SpecialChannelStripComponent import SpecialChannelStripComponent

class SpecialMixerComponent(MixerComponent):

    def __init__(self, _nNumTracks, _hCfg):
        self.m_hCfg = _hCfg
        MixerComponent.__init__(self, _nNumTracks, 0) # nNumReturns = 0

    def disconnect(self):
        MixerComponent.disconnect(self)

    def _create_strip(self):
        return SpecialChannelStripComponent(self.m_hCfg)
