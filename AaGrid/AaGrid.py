from __future__ import with_statement

import os
import time
import Live

from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent

from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.SliderElement import SliderElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.SubjectSlot import subject_slot

from Skin import make_skin
from MainSelectorComponent import MainSelectorComponent
from ConfigurableButtonElement import ConfigurableButtonElement

MANUFACTURER_ID = 71
BUTTON_ON       = 127

class AaGrid(ControlSurface):
    __doc__ = "AaGrid controller"

    def __init__(self, _oCtrlInstance):
        ControlSurface.__init__(self, _oCtrlInstance)
        self.m_oCtrlInstance = _oCtrlInstance
        self.m_sProductName = 'AaGrid'

        with self.component_guard():
            self._suppress_session_highlight = True
            self.load_config()
            self.init()
            self.__add_listeners()
            self.xlog('initialized controller!')

    def disconnect(self):
        self.remove_highlight()
        self.__remove_listeners()
        self.m_oShiftButton.remove_value_listener(self._on_shift_value)
        ControlSurface.disconnect(self)
        self.xlog('disconnected!')

    def load_config(self):
        # default configuration ************************************************
        self.m_hCfg   = {
            'oCtrlInst'   : self.m_oCtrlInstance,
            'sProductName': self.m_sProductName,
            'sProductDir' : 'AaConfig/%s' % (self.m_sProductName),

            'NumTracks'   : 8,  'NumScenes'   : 8,  'NumSliders': 9,
            'Channel'     : 0,  'Mode'        : 98,
            'ClipOffset'  : 0,  'SceneOffset' : 82, 'SliderOffset': 48,
            'SessionUp'   : 64, 'SessionDown' : 65,
            'SessionLeft' : 66, 'SessionRight': 67,
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
            if (len(sLine) == 0):
                continue
            if (sLine[0] == '#'):
                continue
            # the first token in the line is the name of the config feature
            aConfig = sLine.split('#')
            aTokens = aConfig[0].split('|')
            # do not parse lines with less than 2 tokens
            if (len(aTokens) < 2):
                continue
            sName  = aTokens[0].strip()
            sValue = aTokens[1].strip()
            # parse the value of the config feature
            if (sName == 'log'):
                self.m_hCfg['bLog'] = (sValue == 'true')
            else:
                sKey = ''.join(sToken.capitalize() for sToken in sName.split('_'))
                #self.xlog('   parsed: %16s => %16s | %s' % (sName, sKey, sValue))
                self.m_hCfg[sKey] = int(sValue)
        self.xlog('config loaded succesfully!')

    def init(self):
        self.m_oSkin = make_skin()
        bIsMomentary = True
        oMatrix = ButtonMatrixElement()
        oMatrix.name = 'Button_Matrix'

        nClipOffset = self.m_hCfg['ClipOffset']
        nNumScenes  = self.m_hCfg['NumScenes']
        nNumTracks  = self.m_hCfg['NumTracks']
        nNumSliders = self.m_hCfg['NumSliders']
        nChannel    = self.m_hCfg['Channel']
        nMidiType   = MIDI_NOTE_TYPE

        # create the 8x8 matrix of buttons
        for nRowIdx in range(nNumScenes):
            aButtonRow = []
            nRowIdxRel = nNumScenes - 1 - nRowIdx # reversed scene order
            for nColIdx in range(nNumTracks):
                nMidiNote = nClipOffset + nRowIdxRel * nNumTracks + nColIdx
                oButton   = ConfigurableButtonElement(bIsMomentary, nMidiType, nChannel, nMidiNote, skin = self.m_oSkin, control_surface = self)
                oButton.name = 'Clip_Button_%d_%d' % (nRowIdxRel, nColIdx)
                aButtonRow.append(oButton)
            oMatrix.add_row(tuple(aButtonRow))

        # create scene and track buttons
        self.m_lSceneButtonIds = (82, 83, 84, 85, 86, 87, 88, 89)
        self.m_lTrackButtonIds = (64, 65, 66, 67, 68, 69, 70, 71)
        aSceneButtons = [ConfigurableButtonElement(bIsMomentary, nMidiType, nChannel, self.m_lSceneButtonIds[nIdx], skin = self.m_oSkin, name = u'scene_but_%d' % (nIdx)) for nIdx in range(nNumScenes)]
        aTrackButtons = [ConfigurableButtonElement(bIsMomentary, nMidiType, nChannel, self.m_lTrackButtonIds[nIdx], skin = self.m_oSkin, name = u'track_but_%d' % (nIdx)) for nIdx in range(nNumTracks)]

        # create shift button and sliders
        self.m_oShiftButton = ButtonElement(bIsMomentary, nMidiType, nChannel, 98, name = u'shift_but')
        self.m_oShiftButton.add_value_listener(self._on_shift_value)
        aTrackSliders = [SliderElement(MIDI_CC_TYPE, nChannel, self.m_hCfg['SliderOffset'] + nIdx, name = u'track_sli_%d' % (nIdx)) for nIdx in range(nNumSliders)]

        self.m_oSelector = MainSelectorComponent(oMatrix, tuple(aTrackButtons), tuple(aSceneButtons), tuple(aTrackSliders), self, self.m_hCfg)
        self._suppress_session_highlight = False
        self.set_highlighting_session_component(self.m_oSelector.session_component())

        # device config
        self.m_oDevice = DeviceComponent()
        self.m_oDevice.name = 'Device_Component'
        self.set_device_component(self.m_oDevice)

    def _set_session_highlight(self, _nTrackOffset, _nSceneOffset, _nWidth, _nHeight, _nIncludeReturnTracks):
        if not self._suppress_session_highlight:
            ControlSurface._set_session_highlight(self, _nTrackOffset, _nSceneOffset, _nWidth, _nHeight, _nIncludeReturnTracks)

    def _on_shift_value(self, _nValue):
        if _nValue != BUTTON_ON: return
        self.m_oSelector.on_shift_value()

    # ****************************************************************

    def setup_as_primary_instance(self, _oSecPeer):
        self.m_oSelector.setup_as_primary_instance(_oSecPeer)

    def setup_as_secondary_instance(self, _oPrimPeer):
        self.m_oSelector.setup_as_secondary_instance(_oPrimPeer)

    def receive_peer_command(self, _hCmd):
        self.m_oSelector.receive_peer_command(_hCmd)

    def receive_matrix_command(self, _hCmd):
        self.m_oSelector.receive_matrix_command(_hCmd)

    # ****************************************************************

    def __add_listeners(self):
        self.__remove_listeners()
        if (not self.song().scenes_has_listener(self.__on_scenes_changed)):
            self.song().add_scenes_listener(self.__on_scenes_changed)
        if (not self.song().view.selected_scene_has_listener(self.__on_sel_scene_changed)):
            self.song().view.add_selected_scene_listener(self.__on_sel_scene_changed)
        if (not self.song().tracks_has_listener(self.__on_tracks_changed)):
            self.song().add_tracks_listener(self.__on_tracks_changed)
        if (not self.song().view.selected_track_has_listener(self.__on_sel_track_changed)):
            self.song().view.add_selected_track_listener(self.__on_sel_track_changed)

    def __remove_listeners(self):
        if (self.song().scenes_has_listener(self.__on_scenes_changed)):
            self.song().remove_scenes_listener(self.__on_scenes_changed)
        if (self.song().view.selected_scene_has_listener(self.__on_sel_scene_changed)):
            self.song().view.remove_selected_scene_listener(self.__on_sel_scene_changed)
        if (self.song().tracks_has_listener(self.__on_tracks_changed)):
            self.song().remove_tracks_listener(self.__on_tracks_changed)
        if (self.song().view.selected_track_has_listener(self.__on_sel_track_changed)):
            self.song().view.remove_selected_track_listener(self.__on_sel_track_changed)

    def __on_scenes_changed(self):
        self.__add_listeners()
        self.__update_scenes()

    def __on_sel_scene_changed(self):
        self.__update_scenes()

    def __update_scenes(self):
        self.m_oSelector._on_sel_scene_changed()

    def __on_tracks_changed(self):
        self.__add_listeners()
        self.__update_tracks()

    def __on_sel_track_changed(self):
        self.__update_tracks()

    def __update_tracks(self):
        self.m_oSelector._on_sel_track_changed()

    # HANDSHAKE PROTOCOL *******************************************************

    def refresh_state(self):
        super(AaGrid, self).refresh_state()
        self.schedule_message(5, self._update_hardware)

    def _update_hardware(self):
        self._send_midi((240, 126, 127, 6, 1, 247))

    def handle_sysex(self, midi_bytes):
        self._suppress_send_midi = False
        if midi_bytes[3] == 6 and midi_bytes[4] == 2:
             self._on_identity_response(midi_bytes)

    def _on_identity_response(self, midi_bytes):
        if midi_bytes[5] == MANUFACTURER_ID and midi_bytes[6] == self._product_model_id_byte():
            self.log('CONNECTED!')

    def _product_model_id_byte(self):
        return 40

    # ****************************************************************

    def remove_highlight(self):
        _nTrackOffset  = -1
        _nSceneOffset  = -1
        _nNumVisTracks = -1
        _nNumVisScenes = -1
        _bIncludeReturnTracks = False
        self.m_oCtrlInstance.set_session_highlight(_nTrackOffset, _nSceneOffset, _nNumVisTracks, _nNumVisScenes, _bIncludeReturnTracks)

    def log(self, _sMessage):
        Live.Base.log(_sMessage)

    def xlog(self, _sMessage):
        self.log('> %s: %s' % (self.m_sProductName, _sMessage))

    def alert(self, sMessage):
        self.m_oCtrlInstance.show_message(sMessage)

