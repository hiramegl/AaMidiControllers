import Live

from _Framework.MixerComponent import MixerComponent
from SpecialChannelStripComponent import SpecialChannelStripComponent

class SpecialMixerComponent(MixerComponent):
  ' Special mixer class that uses return tracks alongside midi and audio tracks '
  __module__ = __name__

  def __init__(self, _nNumTracks, _hCfg):
    self.m_hCfg = _hCfg # run before 'init', used for master track
    MixerComponent.__init__(self, _nNumTracks)

  def tracks_to_use(self):
    return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

  def _create_strip(self):
    return SpecialChannelStripComponent(self.m_hCfg)

  def _on_sel_scene_changed(self):
    for nIdx in range(len(self._channel_strips)):
      oStrip = self._channel_strips[nIdx]
      oStrip._on_sel_scene_changed()

  def send_bank_values(self, _nBank):
    for nIdx in range(len(self._channel_strips)):
      oStrip = self._channel_strips[nIdx]
      oStrip.send_bank_values(_nBank)

  def update_sync_tasks(self):
    for nIdx in range(len(self._channel_strips)):
      oStrip = self._channel_strips[nIdx]
      oStrip.update_sync_tasks()

