import Live

from _Framework.MixerComponent import MixerComponent
from _Framework.ChannelStripComponent import ChannelStripComponent
from SpecialChannelStripComponent import SpecialChannelStripComponent

class SpecialMixerComponent(MixerComponent):
    ' Special mixer class that uses return tracks alongside midi and audio tracks '
    __module__ = __name__

    def __init__(self, _nNumTracks, _hCfg):
        self.m_hCfg = _hCfg # run before 'init', used for master track
        self.m_nUseSpecialChannelStrip = True
        MixerComponent.__init__(self, _nNumTracks)

    def tracks_to_use(self):
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

    def _create_strip(self):
        if (self.m_nUseSpecialChannelStrip):
            self.m_nUseSpecialChannelStrip = False # use only for the first track
            return SpecialChannelStripComponent(self.m_hCfg)
        return ChannelStripComponent() # use for the rest of the tracks (master, selected)

    def send_bank_values(self, _nBankIdx):
        # since we only attend one ableton live track strip at the time
        # we wil only iterate once, when we operate in the first channel strip
        for nIdx in range(len(self._channel_strips)):
            oStrip = self._channel_strips[nIdx]
            oStrip.send_bank_values(_nBankIdx)

    def update_sync_tasks(self):
        for nIdx in range(len(self._channel_strips)):
            oStrip = self._channel_strips[nIdx]
            oStrip.update_sync_tasks()

