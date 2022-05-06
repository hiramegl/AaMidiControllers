from _Framework.MixerComponent import MixerComponent
from SpecialChannelStripComponent import SpecialChannelStripComponent

class SpecialMixerComponent(MixerComponent):

  def _create_strip(self):
    return SpecialChannelStripComponent()
