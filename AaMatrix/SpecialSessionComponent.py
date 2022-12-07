import Live

from _Framework.SessionComponent import SessionComponent
from _Framework.Util import in_range

from SpecialSceneComponent import SpecialSceneComponent

class SpecialSessionComponent(SessionComponent):
  "Special SessionComponent"
  __module__ = __name__

  def __init__(self, _nNumTracks, _nNumScenes):
    SessionComponent.__init__(self, num_tracks = _nNumTracks, num_scenes = _nNumScenes, enable_skinning = True, name='Session', is_root=True)

  def disconnect(self):
    SessionComponent.disconnect(self)

  def link_with_track_offset(self, track_offset):
    assert (track_offset >= 0)
    if self._is_linked():
      self._unlink()
    self.set_offsets(track_offset, 0)
    self._link()

  def unlink(self):
    if self._is_linked():
      self._unlink()

  def _create_scene(self):
    return SpecialSceneComponent(_oSession = self, num_slots=self._num_tracks, tracks_to_use_callback=self.tracks_to_use)

  def _reassign_scenes(self):
    super(SpecialSessionComponent, self)._reassign_scenes()
    self._update_selected_buttons()

  def on_selected_scene_changed(self):
    super(SpecialSessionComponent, self).on_selected_scene_changed()
    self._update_selected_buttons()

  def _update_selected_buttons(self):
    oSelScene = self.song().view.selected_scene
    for nSceneIdx in range(self.height()):
      oScene = self.scene(nSceneIdx)
      if oScene.m_oSelButton != None:
        if (oScene._scene == oSelScene):
          oScene.m_oSelButton.turn_on()
        else:
          oScene.m_oSelButton.turn_off()

  def _update_stop_clips_led(self, index):
    tracks_to_use = self.tracks_to_use()
    track_index = index + self.track_offset()
    if self.is_enabled() and self._stop_track_clip_buttons != None and index < len(self._stop_track_clip_buttons):
      button = self._stop_track_clip_buttons[index]
      if button != None:
        value_to_send = None
        if track_index < len(tracks_to_use) and tracks_to_use[track_index].clip_slots:
          track = tracks_to_use[track_index]
          if track.fired_slot_index == -2:
            value_to_send = self._stop_clip_triggered_value
          elif track.playing_slot_index >= 0:
            value_to_send = self._stop_clip_value
        else:
          value_to_send = 0
        if value_to_send == None:
          button.turn_off()
        elif in_range(value_to_send, 0, 128):
          button.send_value(value_to_send)
        else:
          button.set_light(value_to_send)


