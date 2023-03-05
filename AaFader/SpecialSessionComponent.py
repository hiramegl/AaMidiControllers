import Live

from _Framework.SessionComponent import SessionComponent
from _Framework.ButtonElement import ButtonElement

def release_control(control):
  if control != None:
    control.release_parameter()

class SpecialSessionComponent(SessionComponent):
  "Special Session Component"
  __module__ = __name__

  def __init__(self, _nNumTracks, _nNumScenes):
    SessionComponent.__init__(self, _nNumTracks, _nNumScenes)
    self._slot_launch_button = None

    self.m_oTempo1Control  = None

    def make_control_slot(name):
      return self.register_slot(None, getattr(self, u'_%s_value' % name), u'value')

    self._tempo_1_control_slot = make_control_slot(u'tempo_1')

  def disconnect(self):
    SessionComponent.disconnect(self)
    if (self._slot_launch_button != None):
      self._slot_launch_button.remove_value_listener(self._slot_launch_value)
      self._slot_launch_button = None

  def link_with_track_offset(self, track_offset, scene_offset):
    assert (track_offset >= 0)
    assert (scene_offset >= 0)
    if self._is_linked():
      self._unlink()
    self.set_offsets(track_offset, scene_offset)
    self._link()

  def unlink(self):
    if self._is_linked():
      self._unlink()

  def set_slot_launch_button(self, button):
    assert ((button == None) or isinstance(button, ButtonElement))
    if (self._slot_launch_button != button):
      if (self._slot_launch_button != None):
        self._slot_launch_button.remove_value_listener(self._slot_launch_value)
      self._slot_launch_button = button
      if (self._slot_launch_button != None):
        self._slot_launch_button.add_value_listener(self._slot_launch_value)
      self.update()

  def _slot_launch_value(self, value):
    assert (value in range(128))
    assert (self._slot_launch_button != None)
    if self.is_enabled():
      if ((value != 0) or (not self._slot_launch_button.is_momentary())):
        if (self.song().view.highlighted_clip_slot != None):
          self.song().view.highlighted_clip_slot.fire()

  def _scroll_page_left(self):
    SessionComponent._scroll_page_left(self)
    self._update_paging_controls()

  def _scroll_page_right(self):
    SessionComponent._scroll_page_right(self)
    self._update_paging_controls()

  def _update_paging_controls(self):
    nLeftValue  = 127 if self._can_scroll_page_left()  else 0
    nRightValue = 127 if self._can_scroll_page_right() else 0
    self._page_left_button.send_value(nLeftValue, True)
    self._page_right_button.send_value(nRightValue, True)

  # TEMPO 1 ******************************************************************

  def set_tempo_1(self, _oControl):
    if _oControl != self.m_oTempo1Control:
      release_control(self.m_oTempo1Control)
      self.m_oTempo1Control = _oControl
      self._tempo_1_control_slot.subject = _oControl
      self.update()

  def _tempo_1_value(self, _nValue):
    assert self.m_oTempo1Control != None
    assert isinstance(_nValue, int)
    self.song().tempo = _nValue + 20
