import Live

from _Framework.SceneComponent import SceneComponent
from _Framework.SubjectSlot import subject_slot

from SpecialClipSlotComponent import SpecialClipSlotComponent

class SpecialSceneComponent(SceneComponent):
    __module__ = __name__

    def __init__(self, _oSession, num_slots, tracks_to_use_callback, *a, **k):
        super(SpecialSceneComponent, self).__init__(num_slots, tracks_to_use_callback, *a, **k)
        self.m_oSession   = _oSession
        self.m_oSelButton = None
        self.m_oVolButton = None
        self.m_nVolValue  = 0.0

    def disconnect(self):
        SceneComponent.disconnect(self)
        self.m_oSelButton = None
        self.m_oVolButton = None

    def _create_clip_slot(self):
        return SpecialClipSlotComponent()

    # ******************************************************

    def set_select_control(self, _oControl):
        if _oControl != self.m_oSelButton:
            self.m_oSelButton = _oControl
            self._on_select_value.subject = _oControl
            self.update()

    @subject_slot(u'value')
    def _on_select_value(self, value):
        if self.is_enabled():
            self._do_select_scene(self._scene)

    # ******************************************************

    def set_vol_control(self, _oControl, _nVolValue):
        if _oControl != self.m_oVolButton:
            if (_oControl == None and self.m_oVolButton != None):
                self.m_oVolButton.turn_off()
            self.m_oVolButton = _oControl
            self.m_nVolValue  = _nVolValue
            self._on_volume_value.subject = _oControl
            if (_oControl != None):
                _oControl.turn_on()

    @subject_slot(u'value')
    def _on_volume_value(self, value):
        if self.is_enabled() and self.m_oVolButton != None:
            for nTrackIdx in range(self.m_oSession.width()):
                oStrip = self.m_oSession._mixer.channel_strip(nTrackIdx)
                if (oStrip._track != None):
                    oStrip._track.mixer_device.volume.value = self.m_nVolValue

    # ******************************************************

    def update(self):
        super(SpecialSceneComponent, self).update()
        if self._allow_updates and self.m_oSelButton != None:
            if self._scene != None and self.is_enabled():
                if self.song().view.selected_scene == self._scene:
                    self.m_oSelButton.turn_on()
                else:
                    self.m_oSelButton.turn_off()
            else:
                self.m_oSelButton.turn_off()

