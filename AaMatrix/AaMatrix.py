from __future__ import with_statement

import os
import time
import Live

from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement

from .ConfigurableButtonElement import ConfigurableButtonElement
from .Selector import Selector

try:
  xrange
except NameError:
  xrange = range

LP_MINI_MK3_ID                 = 13
LP_X_ID                        = 12
SYSEX_START                    = 240
SYSEX_NON_REALTIME             = 126
SYSEX_GENERAL_INFO             = 6
SYSEX_IDENTITY_REQUEST_ID      = 1
SYSEX_END                      = 247
SYSEX_IDENTITY_REQUEST_MESSAGE = (SYSEX_START, SYSEX_NON_REALTIME, 127, SYSEX_GENERAL_INFO, SYSEX_IDENTITY_REQUEST_ID, SYSEX_END)
NOVATION_MANUFACTURER_ID       = (0, 32, 41)
FIRMWARE_MODE_COMMAND          = 16
STANDALONE_MODE                = 0
STD_MSG_HEADER                 = (SYSEX_START,) + NOVATION_MANUFACTURER_ID + (2,)

class AaMatrix(ControlSurface):
  __doc__ = "AaMatrix controller"
  _active_instances = []

  def __init__(self, _oCtrlInstance):
    ControlSurface.__init__(self, _oCtrlInstance)
    self.m_oCtrlInstance = _oCtrlInstance
    self.m_sProductName  = 'AaMatrix'
    self.m_oSelector     = None #needed because update hardware is called.
    self._lpx            = False
    self._mk2_rgb        = False
    self._mk3_rgb        = False

    with self.component_guard():
      self.load_config()
      self._suppress_send_midi         = True
      self._suppress_session_highlight = True
      self._suggested_input_port       = ("Launchpad", "Launchpad Mini", "Launchpad S", "Launchpad MK2", "Launchpad X", "Launchpad Mini MK3")
      self._suggested_output_port      = ("Launchpad", "Launchpad Mini", "Launchpad S", "Launchpad MK2", "Launchpad X", "Launchpad Mini MK3")
      self._control_is_with_automap    = False
      self._user_byte_write_button     = None
      self._config_button              = None
      self._wrote_user_byte            = False
      self._challenge                  = Live.Application.get_random_int(0, 400000000) & 2139062143
      self._init_done                  = False
      self.__add_listeners()
      self.xlog('init started')

  def load_config(self):
    # default configuration ************************************************
    self.m_hCfg   = {
      'oCtrlInst'   : self.m_oCtrlInstance,
      'sProductName': self.m_sProductName,
      'sProductDir' : 'AaConfig/%s' % (self.m_sProductName),
      'NumTracks'   : 8,
      'NumScenes'   : 8,
      'Channel'     : 0,
    }

    sHome     = os.getenv('HOME')
    sFilePath = '%s/%s/config.txt' % (sHome, self.m_hCfg['sProductDir'])
    bFileExists = os.path.isfile(sFilePath)
    if (bFileExists == False):
      self.log('> config file "%s" not found!' % (sFilePath))
      return # config file does not exist, nothing else to do here!

    # parse config file, line by line
    self.xlog('reading: "%s"' % (sFilePath))
    oFile = open(sFilePath, 'r')
    for sLine in oFile:
      sLine = sLine.strip()
      if (len(sLine) == 0): continue
      if (sLine[0] == '#'): continue
      # the first token in the line is the name of the config feature
      aConfig = sLine.split('#')
      aTokens = aConfig[0].split('|')
      # do not parse lines with less than 2 tokens
      if (len(aTokens) < 2): continue
      sName  = aTokens[0].strip()
      sValue = aTokens[1].strip()
      # parse the value of the config feature
      sKey = ''.join(sToken.capitalize() for sToken in sName.split('_'))
      self.xlog('   parsed: %16s => %16s | %s' % (sName, sKey, sValue))
      self.m_hCfg[sKey] = int(sValue)
    self.xlog('config loaded succesfully!')

  # HANDSHAKE PROTOCOL *******************************************************

  def refresh_state(self):
    ControlSurface.refresh_state(self)
    self.schedule_message(5, self._update_hardware)

  def _update_hardware(self):
    self._suppress_send_midi = False
    if self._user_byte_write_button != None:
      self._user_byte_write_button.send_value(1)
      self._wrote_user_byte = True
    self._suppress_send_midi = True
    self.set_enabled(False)
    self._suppress_send_midi = False
    self._send_challenge()

  def _send_challenge(self):
    # send challenge for all models to allow to detect which one is actually plugged
    self._send_midi(SYSEX_IDENTITY_REQUEST_MESSAGE)                                        # for mk3 and LPX
    challenge_bytes = tuple([ self._challenge >> 8 * index & 127 for index in xrange(4) ]) # for mk2
    self._send_midi((240, 0, 32, 41, 2, 24, 64) + challenge_bytes + (247,))
    for index in range(4):                                                                 # for mk1's
      challenge_byte = self._challenge >> 8 * index & 127
      self._send_midi((176, 17 + index, challenge_byte))

  def handle_sysex(self, midi_bytes):
    if len(midi_bytes) >= 10 and midi_bytes[:8] == (240, 126, 0, 6, 2, 0, 32, 41): #0,32,41=novation
      # MK3
      if len(midi_bytes) >= 12 and midi_bytes[8:10] == (19,1):
        self._mk3_rgb = True
        #programmer mode
        self._send_midi(STD_MSG_HEADER + (LP_MINI_MK3_ID, 14, 1, SYSEX_END))
        #led feedback: internal off, external on
        self._send_midi(STD_MSG_HEADER + (LP_MINI_MK3_ID, 10, 0, 1, SYSEX_END))
        #disable sleep mode
        self._send_midi(STD_MSG_HEADER + (LP_MINI_MK3_ID, 9, 1, SYSEX_END))
        self._suppress_send_midi = False
        self.set_enabled(True)
        self.init()
      elif len(midi_bytes) >= 12 and midi_bytes[8:10] == (3,1):
        self._lpx = True
        #programmer mode
        self._send_midi(STD_MSG_HEADER + (LP_X_ID, 14, 1, SYSEX_END))
        #led feedback: internal off, external on
        self._send_midi(STD_MSG_HEADER + (LP_X_ID, 10, 0, 1, SYSEX_END))
        #disable sleep mode
        self._send_midi(STD_MSG_HEADER + (LP_X_ID, 9, 1, SYSEX_END))
        self._suppress_send_midi = False
        self.set_enabled(True)
        self.init()
      else:
        ControlSurface.handle_sysex(self, midi_bytes)
    elif len(midi_bytes) == 9 and midi_bytes[:9] == (240, 0, 32, 41, 2, 13, 14, 1, 247):
      self.xlog("Challenge Response ok (mk3)")
    elif len(midi_bytes) == 10 and midi_bytes[:7] == (240, 0, 32, 41, 2, 24, 64):
      # MK2
      response = long(midi_bytes[7])
      response += long(midi_bytes[8]) << 8
      if response == Live.Application.encrypt_challenge2(self._challenge):
        self.xlog("Challenge Response ok (mk2)")
        self._mk2_rgb = True
        self._suppress_send_midi = False
        self.set_enabled(True)
        self.init()
    elif len(midi_bytes) == 8 and midi_bytes[1:5] == (0, 32, 41, 6):
      # MK1
      response = long(midi_bytes[5])
      response += long(midi_bytes[6]) << 8
      if response == Live.Application.encrypt_challenge2(self._challenge):
        self.xlog("Challenge Response ok (mk1)")
        self._mk2_rgb = False
        self.init()
        self._suppress_send_midi = False
        self.set_enabled(True)
    else:
      ControlSurface.handle_sysex(self, midi_bytes)

  def init(self):
    if self._init_done: return
    self._init_done = True

    # second part of the __init__ after model has been identified using its challenge response
    if self._mk3_rgb or self._lpx:
      from .SkinMK2 import make_skin
      self._skin = make_skin()
      self._side_notes = (89, 79, 69, 59, 49, 39, 29, 19)
      self._drum_notes = (20, 30, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126)
    elif self._mk2_rgb:
      from .SkinMK2 import make_skin
      self._skin = make_skin()
      self._side_notes = (89, 79, 69, 59, 49, 39, 29, 19)
      self._drum_notes = (20, 30, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126)
    else:
      from .SkinMK1 import make_skin # @Reimport
      self._skin = make_skin()
      self._side_notes = (8, 24, 40, 56, 72, 88, 104, 120)
      self._drum_notes = (41, 42, 43, 44, 45, 46, 47, 57, 58, 59, 60, 61, 62, 63, 73, 74, 75, 76, 77, 78, 79, 89, 90, 91, 92, 93, 94, 95, 105, 106, 107)

    with self.component_guard():
      is_momentary = True
      self._config_button = ButtonElement(is_momentary, MIDI_CC_TYPE, 0, 0, optimized_send_midi=False)
      self._config_button.add_value_listener(self._config_value)
      self._user_byte_write_button = ButtonElement(is_momentary, MIDI_CC_TYPE, 0, 16)
      self._user_byte_write_button.name = 'User_Byte_Button'
      self._user_byte_write_button.send_value(1)
      self._user_byte_write_button.add_value_listener(self._user_byte_value)

      matrix = ButtonMatrixElement()
      matrix.name = 'Button_Matrix'
      for row in range(8):
        button_row = []
        for column in range(8):
          if self._mk2_rgb or self._mk3_rgb or self._lpx:
            # for mk2 buttons are assigned "top to bottom"
            midi_note = (81 - (10 * row)) + column
          else:
            midi_note = row * 16 + column
          button = ConfigurableButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, midi_note, skin = self._skin, control_surface = self)
          button.name = 'Grid_' + str(column) + '_' + str(row)
          button.m_hAttr = {'sType': 'grid', 'nRow': row, 'nCol': column}
          button_row.append(button)
        matrix.add_row(tuple(button_row))

      if self._mk3_rgb or self._lpx :
        top_buttons  = [ConfigurableButtonElement(is_momentary, MIDI_CC_TYPE, 0, 91 + index, skin = self._skin) for index in range(8)]
        side_buttons = [ConfigurableButtonElement(is_momentary, MIDI_CC_TYPE, 0, self._side_notes[index], skin = self._skin) for index in range(8)]
      else:
        top_buttons  = [ConfigurableButtonElement(is_momentary, MIDI_CC_TYPE, 0, 104 + index, skin = self._skin) for index in range(8)]
        side_buttons = [ConfigurableButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, self._side_notes[index], skin = self._skin) for index in range(8)]
      for i in range(8):
         top_buttons[i].name    = 'Top_' + str(i)
         top_buttons[i].m_hAttr = {'sType': 'top', 'nIdx': i}
      for i in range(8):
         side_buttons[i].name    = 'Side_' + str(i)
         side_buttons[i].m_hAttr = {'sType': 'side', 'nIdx': i}

      self.m_oSelector = Selector(self, self.m_hCfg, matrix, top_buttons, side_buttons)
      self.m_oSelector.name = 'Selector'
      for control in self.controls:
        if isinstance(control, ConfigurableButtonElement):
          control.add_value_listener(self._button_value, identify_sender = True)

      self._suppress_session_highlight = False
      self.set_highlighting_session_component(self.m_oSelector.session_component())
      self.request_rebuild_midi_map() # due to our 2 stage init, we need to rebuild midi map
      self.m_oSelector.update()       # and request update
      if self._lpx:
        self.xlog("AaMatrix (LPX) Loaded !")
      elif self._mk3_rgb:
        self.xlog("AaMatrix (mk3) Loaded !")
      elif self._mk2_rgb:
        self.xlog("AaMatrix (mk2) Loaded !")
      else:
        self.xlog("AaMatrix (classic) Loaded !")

  def _user_byte_value(self, value):
    assert (value in range(128))
    if not self._wrote_user_byte:
      enabled = (value == 1)
      self._control_is_with_automap = not enabled
      self._suppress_send_midi = self._control_is_with_automap
      if not self._control_is_with_automap:
        for control in self.controls:
          if isinstance(control, ConfigurableButtonElement):
            control.force_next_send()
      self.set_enabled(enabled)
      self._suppress_send_midi = False
    else:
      self._wrote_user_byte = False

  def disconnect(self):
    self._suppress_send_midi = True
    for control in self.controls:
      if isinstance(control, ConfigurableButtonElement):
        control.remove_value_listener(self._button_value)
    if self.m_oSelector != None:
      self._user_byte_write_button.remove_value_listener(self._user_byte_value)
      self._config_button.remove_value_listener(self._config_value)

    ControlSurface.disconnect(self)
    self._suppress_send_midi = False
    if self._lpx:
      # lpx needs disconnect string sent
      self._send_midi(STD_MSG_HEADER + (LP_X_ID, 14, 0, SYSEX_END))
      self._send_midi(STD_MSG_HEADER + (LP_X_ID, FIRMWARE_MODE_COMMAND, STANDALONE_MODE, SYSEX_END))
    elif self._mk3_rgb:
      # launchpad mk2 needs disconnect string sent
      self._send_midi(STD_MSG_HEADER + (LP_MINI_MK3_ID, 14, 0, SYSEX_END))
      self._send_midi(STD_MSG_HEADER + (LP_MINI_MK3_ID, FIRMWARE_MODE_COMMAND, STANDALONE_MODE, SYSEX_END))
    elif self._mk2_rgb:
      # launchpad mk2 needs disconnect string sent
      self._send_midi((240, 0, 32, 41, 2, 24, 64, 247))

    if self._config_button != None:
      self._config_button.send_value(32) #Send enable flashing led config message to LP
      self._config_button.send_value(0)
      self._config_button = None

    if self._user_byte_write_button != None:
      self._user_byte_write_button.send_value(0)
      self._user_byte_write_button = None
    self.xlog('disconnected!')

  # ****************************************************************

  def _send_midi(self, midi_bytes, optimized=None):
    sent_successfully = False
    if not self._suppress_send_midi:
      sent_successfully = ControlSurface._send_midi(self, midi_bytes, optimized=optimized)
    return sent_successfully

  def _set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks):
    if not self._suppress_session_highlight:
      ControlSurface._set_session_highlight(self, track_offset, scene_offset, width, height, include_return_tracks)

  def _button_value(self, value, _oSender):
    assert value in range(128)
    self.m_oSelector.route(_oSender, _oSender.m_hAttr, value)

  def _config_value(self, value):
    assert value in range(128)

  # ****************************************************************

  def __add_listeners(self):
    self.__remove_listeners()
    if not self.song().scenes_has_listener(self.__on_scenes_changed):
      self.song().add_scenes_listener(self.__on_scenes_changed)
    if not self.song().view.selected_scene_has_listener(self.__on_sel_scene_changed):
      self.song().view.add_selected_scene_listener(self.__on_sel_scene_changed)
    if not self.song().tracks_has_listener(self.__on_tracks_changed):
      self.song().add_tracks_listener(self.__on_tracks_changed)
    if not self.song().view.selected_track_has_listener(self.__on_sel_track_changed):
      self.song().view.add_selected_track_listener(self.__on_sel_track_changed)

  def __remove_listeners(self):
    if self.song().scenes_has_listener(self.__on_scenes_changed):
      self.song().remove_scenes_listener(self.__on_scenes_changed)
    if self.song().view.selected_scene_has_listener(self.__on_sel_scene_changed):
      self.song().view.remove_selected_scene_listener(self.__on_sel_scene_changed)
    if self.song().tracks_has_listener(self.__on_tracks_changed):
      self.song().remove_tracks_listener(self.__on_tracks_changed)
    if self.song().view.selected_track_has_listener(self.__on_sel_track_changed):
      self.song().view.remove_selected_track_listener(self.__on_sel_track_changed)

  def __on_scenes_changed(self):
    self.__add_listeners()
    self.__update_scenes()

  def __on_sel_scene_changed(self):
    self.__update_scenes()

  def __update_scenes(self):
    if self.m_oSelector == None: return
    self.m_oSelector._on_sel_scene_changed()

  def __on_tracks_changed(self):
    self.__add_listeners()
    self.__update_tracks()

  def __on_sel_track_changed(self):
    self.__update_tracks()

  def __update_tracks(self):
    if self.m_oSelector == None: return
    self.m_oSelector._on_sel_track_changed()

  # ****************************************************************

  def receive_grid_command(self, _hCmd):
    self.m_oSelector.receive_grid_command(_hCmd)

  # ****************************************************************

  def log(self, _sMessage):
      Live.Base.log(_sMessage)

  def xlog(self, _sMessage):
      self.log('> %s: %s' % (self.m_sProductName, _sMessage))

  def alert(self, sMessage):
      self.m_oCtrlInstance.show_message(sMessage)
