import Live

from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.SubjectSlot import subject_slot

class SpecialClipSlotComponent(ClipSlotComponent):
    __module__ = __name__

    def __init__(self, *a, **k):
        super(SpecialClipSlotComponent, self).__init__(*a, **k)
        self.m_oSelectControl = None

    def set_select_control(self, _oControl):
        if (self.m_oSelectControl != _oControl):
            if (self.m_oSelectControl != None):
                self.m_oSelectControl.turn_off()
            self.m_oSelectControl = _oControl
            self._select_control_value.subject = _oControl
            if (self.m_oSelectControl != None):
                self.m_oSelectControl.turn_on()

    @subject_slot(u'value')
    def _select_control_value(self, _nValue):
        if self.is_enabled():
            if (_nValue == 127):
                self._do_select_clip(self._clip_slot)

