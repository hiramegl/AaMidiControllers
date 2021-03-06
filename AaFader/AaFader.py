from __future__ import with_statement

import os
import time
import Live

from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent

from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.SliderElement import SliderElement
from _Framework.SubjectSlot import subject_slot

from SpecialMixerComponent import SpecialMixerComponent
from SpecialSessionComponent import SpecialSessionComponent

class AaFader(ControlSurface):
    __doc__ = "AaFader controller"

    def __init__(self, _oCtrlInstance):
        ControlSurface.__init__(self, _oCtrlInstance)
        self.m_oCtrlInstance = _oCtrlInstance
        self.m_sProductName  = 'AaFader'

        with self.component_guard():
            #self.xlog('initializing controller ...')
            self.load_config()
            self.setup_session()
            self.setup_mixer()
            self.m_oSession.set_mixer(self.m_oMixer)
            self.setup_device()
            self.__add_listeners()
            self.set_highlighting_session_component(self.m_oSession)
            self.xlog('initialized controller!')

    def disconnect(self):
        #self.xlog('disconnecting ...')
        self.remove_highlight()
        self.m_oButStopTotal.remove_value_listener(self._on_stop_total)
        self.m_oButBank1Sync.remove_value_listener(self._on_bank_1_sync)
        self.m_oButBank2Sync.remove_value_listener(self._on_bank_2_sync)
        self.m_oButBank3Sync.remove_value_listener(self._on_bank_3_sync)
        self.m_oButBank4Sync.remove_value_listener(self._on_bank_4_sync)
        self.__remove_listeners()
        ControlSurface.disconnect(self)
        self.xlog('disconnected!')

    def load_config(self):
        self.m_nNumTracks = 8

        # default configuration ************************************************
        self.m_hCfg = {
            'oCtrlInst'   : self.m_oCtrlInstance,
            'sProductName': self.m_sProductName,
            'sProductDir' : 'AaConfig/%s' % (self.m_sProductName),

            'NumScenes'   : 1,

            # fixed config
            'Bank0Channel': 0,
            'SessionLeft' : 25, 'SessionRight': 26,
            'StopTotal'   : 27, 'VolOffset'   : 17,

            # bank 1
            'Bank1Sync'   : 28, 'Bank1Channel': 0,  # MIDI-CHANNEL 1
            'Send1Offset' : 33, 'Send2Offset' : 41, # Rotary Bank 1 & 2
            'PitchOffset' : 49, 'PitResOffset': 65, # Rotary Bank 3
            'DetuneOffset': 57, 'DetResOffset': 73, # Rotary Bank 4
            'MuteOffset'  : 1,  'SoloOffset'  : 9,  # Buttons

            # bank 2
            'Bank2Sync'   : 29, 'Bank2Channel': 1,  # MIDI-CHANNEL 2
            'Send3Offset' : 33, 'Send4Offset' : 41, # Rotary Bank 1 & 2
            'PanOffset'   : 49,                     # Rotary Bank 3
            'SelClpOffset': 57,                     # Rotary Bank 4
            'StopOffset'  : 1,  'ArmOffset'   : 9,  # Buttons

            # bank 3
            'Bank3Sync'   : 30, 'Bank3Channel': 2,  # MIDI-CHANNEL 3
            'Send5Offset' : 33, 'Send6Offset' : 41, # Rotary Bank 1 & 2
            'AvVelOffset' : 49, 'VolResOffset': 65, # Rotary Bank 3
            'DeckOffset'  : 57, 'VelTogOffset': 73, # Rotary Bank 4
            'AvIncrOffset': 1,  'AvDecrOffset': 9,  # Buttons

            # bank 4
            'Bank4Sync'   : 31, 'Bank4Channel': 3,  # MIDI-CHANNEL 4
        }

        #self.xlog('loading config ...')
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
            #self.xlog('   parsed: %16s => %16s | %s' % (sName, sKey, sValue))
            self.m_hCfg[sKey] = int(sValue)
        self.xlog('config loaded succesfully!')

    def setup_session(self):
        self.m_oSession = SpecialSessionComponent(self.m_nNumTracks, self.m_hCfg['NumScenes'])
        self.m_oSession.name = 'Session'
        oSession = self.m_oSession
        self.m_hCfg['oSession'] = oSession

        oSession.set_page_left_button (self.create_toggle('SessionLeft' , 0))
        oSession.set_page_right_button(self.create_toggle('SessionRight', 0))
        aButStopTrack = [self.create_button('StopOffset', 2, nTrackIdx) for nTrackIdx in range(self.m_nNumTracks)]
        oSession.set_stop_track_clip_buttons(tuple(aButStopTrack))

        self.m_oButStopTotal = self.create_button('StopTotal', 0)
        self._on_stop_total.subject = self.m_oButStopTotal
        self.m_oButBank1Sync = self.create_button('Bank1Sync', 0)
        self._on_bank_1_sync.subject = self.m_oButBank1Sync
        self.m_oButBank2Sync = self.create_button('Bank2Sync', 0)
        self._on_bank_2_sync.subject = self.m_oButBank2Sync
        self.m_oButBank3Sync = self.create_button('Bank3Sync', 0)
        self._on_bank_3_sync.subject = self.m_oButBank3Sync
        self.m_oButBank4Sync = self.create_button('Bank4Sync', 0)
        self._on_bank_4_sync.subject = self.m_oButBank4Sync

    def setup_mixer(self):
        self.m_oMixer = SpecialMixerComponent(self.m_nNumTracks, self.m_hCfg)
        self.m_oMixer.name = 'Mixer'
        oMixer = self.m_oMixer

        for nTrackIdx in range(self.m_nNumTracks):
            oStrip = oMixer.channel_strip(nTrackIdx)
            oStrip.name = 'Channel_Strip_' + str(nTrackIdx)
            oStrip.set_index(nTrackIdx)
            oStrip.set_send_controls((
                # bank 1
                self.create_encoder('Send1Offset', 1, nTrackIdx),
                self.create_encoder('Send2Offset', 1, nTrackIdx),
                # bank 2
                self.create_encoder('Send3Offset', 2, nTrackIdx),
                self.create_encoder('Send4Offset', 2, nTrackIdx),
                # bank 3
                self.create_encoder('Send5Offset', 3, nTrackIdx),
                self.create_encoder('Send6Offset', 3, nTrackIdx)))

            # bank 1, 2 & 3
            oStrip.set_volume_control(self.create_slider ('VolOffset'   , 0, nTrackIdx))

            # bank 1
            oStrip.set_mute_button   (self.create_toggle ('MuteOffset'  , 1, nTrackIdx))
            oStrip.set_solo_button   (self.create_toggle ('SoloOffset'  , 1, nTrackIdx))
            oStrip.set_pitch_control (self.create_encoder('PitchOffset' , 1, nTrackIdx))
            oStrip.set_pitch_reset   (self.create_toggle ('PitResOffset', 1, nTrackIdx))
            oStrip.set_detune_control(self.create_encoder('DetuneOffset', 1, nTrackIdx))
            oStrip.set_detune_reset  (self.create_toggle ('DetResOffset', 1, nTrackIdx))

            # bank 2
            oStrip.set_arm_button    (self.create_toggle ('ArmOffset'   , 2, nTrackIdx))
            oStrip.set_pan_control   (self.create_encoder('PanOffset'   , 2, nTrackIdx))
            oStrip.set_clip_control  (self.create_button ('SelClpOffset', 2, nTrackIdx))

            # bank 3
            oStrip.set_av_incr_toggle(self.create_toggle ('AvIncrOffset', 3, nTrackIdx))
            oStrip.set_av_decr_toggle(self.create_toggle ('AvDecrOffset', 3, nTrackIdx))
            oStrip.set_av_vel_control(self.create_encoder('AvVelOffset' , 3, nTrackIdx))
            oStrip.set_volume_reset  (self.create_toggle ('VolResOffset', 3, nTrackIdx))
            oStrip.set_deck_control  (self.create_encoder('DeckOffset'  , 3, nTrackIdx))
            oStrip.set_vel_toggle    (self.create_button ('VelTogOffset', 3, nTrackIdx))
            oStrip.set_invert_mute_feedback(True)

    def setup_device(self):
        self.m_oDevice = DeviceComponent()
        self.m_oDevice.name = 'Device_Component'
        self.set_device_component(self.m_oDevice)


    def move_to_track_offset(self, _nTrackOffsetAbs):
        self.m_oSession.set_offsets(_nTrackOffsetAbs, 0)

    # ****************************************************************
    #                nBeatDelta
    #              |<--------->|
    # Beat        Beat        Beat        Beat
    #  |           |           |           |
    #  V           V           V           V
    # -------------------------------------------->
    #  : ^   ^   ^ : ^   ^   ^ : ^   ^   ^ :
    #  : |   |   | : |   |   | : |   |   | :   <=== update_sync_tasks() [~ every 100 ms]
    #
    #   #fTime = time.time() # time as float (seconds), decimals are milliseconds
    #   #nTime = int(fTime)
    #   #sTime = datetime.datetime.fromtimestamp(fTime).strftime('%Y-%m-%d %H:%M:%S.%f')
    #   #Live.Base.log("(%d) %f: %s" % (nTime, fTime, sTime))
    # ****************************************************************

    def update_display(self): # This function is run every 100ms
        self.m_oMixer.update_sync_tasks()

    # ****************************************************************

    @subject_slot(u'value')
    def _on_stop_total(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        self.song().stop_all_clips()
        self.song().stop_playing()

    @subject_slot(u'value')
    def _on_bank_1_sync(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        self._sync_bank(1)

    @subject_slot(u'value')
    def _on_bank_2_sync(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        self._sync_bank(2)

    @subject_slot(u'value')
    def _on_bank_3_sync(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        self._sync_bank(3)

    @subject_slot(u'value')
    def _on_bank_4_sync(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        self._sync_bank(4)

    def _sync_bank(self, _nIdx):
        # update page buttons
        nLeftValue  = 127 if self.m_oSession._can_scroll_page_left()  else 0
        nRightValue = 127 if self.m_oSession._can_scroll_page_right() else 0
        self.m_oSession._page_left_button.send_value(nLeftValue , True)
        self.m_oSession._page_right_button.send_value(nRightValue, True)

        # update track balues
        self.m_oMixer.send_bank_values(_nIdx)
        self.alert('> Synced Bank %d' % (_nIdx))

    # ****************************************************************

    def __add_listeners(self):
        self.__remove_listeners()
        if (not self.song().scenes_has_listener(self.__on_scenes_change)):
            self.song().add_scenes_listener(self.__on_scenes_change)
        if (not self.song().view.selected_scene_has_listener(self.__on_sel_scene_change)):
            self.song().view.add_selected_scene_listener(self.__on_sel_scene_change)

    def __remove_listeners(self):
        if (self.song().scenes_has_listener(self.__on_scenes_change)):
            self.song().remove_scenes_listener(self.__on_scenes_change)
        if (self.song().view.selected_scene_has_listener(self.__on_sel_scene_change)):
            self.song().view.remove_selected_scene_listener(self.__on_sel_scene_change)

    def __on_scenes_change(self):
        self.__add_listeners()
        self.__update_scene_values()

    def __on_sel_scene_change(self):
        self.__update_scene_values()

    def __update_scene_values(self):
        self.m_oMixer._on_sel_scene_changed()

    # ****************************************************************

    def get_el_config(self, _sName, _nBank, _nIndex = None):
        nMidiType    = MIDI_CC_TYPE
        nChannel     = self.m_hCfg['Bank%dChannel' % (_nBank)]
        sKey         = _sName
        nOffset      = 0
        if (_nIndex != None):
            nOffset = _nIndex
            _sName  = '%s_%d' % (_sName, _nIndex)
        return (nMidiType, nChannel, sKey, nOffset, _sName)

    def create_button(self, _sName, _nBank, _nIndex = None):
        bIsMomentary = True
        nMidiType, nChannel, sKey, nOffset, sName = self.get_el_config(_sName, _nBank, _nIndex)
        return ButtonElement(bIsMomentary, nMidiType, nChannel, self.m_hCfg[sKey] + nOffset, name = _sName)


    def create_encoder(self, _sName, _nBank, _nIndex = None):
        return self.create_button(_sName, _nBank, _nIndex)


    def create_toggle(self, _sName, _nBank, _nIndex = None):
        bIsMomentary = False
        nMidiType, nChannel, sKey, nOffset, sName = self.get_el_config(_sName, _nBank, _nIndex)
        return ButtonElement(bIsMomentary, nMidiType, nChannel, self.m_hCfg[sKey] + nOffset, name = _sName)


    def create_slider(self, _sName, _nBank, _nIndex = None):
        nMidiType, nChannel, sKey, nOffset, sName = self.get_el_config(_sName, _nBank, _nIndex)
        return SliderElement(nMidiType, nChannel, self.m_hCfg[sKey] + nOffset, name = _sName)

    # ****************************************************************

    def sel_clip_slot(self):
        return self.song().view.highlighted_clip_slot


    def scenes(self):
        return self.song().scenes

    def sel_scene(self, _oScene = None):
        if (_oScene != None):
            self.song().view.selected_scene = _oScene
        return self.song().view.selected_scene

    def sel_scene_idx_abs(self):
        aAllScenes = self.scenes()
        oSelScene  = self.sel_scene()
        return list(aAllScenes).index(oSelScene)


    def master(self):
        return self.song().master_track

    def tracks(self):
        return self.song().tracks #visible_tracks

    def returns(self):
        return self.song().return_tracks

    def tracks_and_returns(self):
        return tuple(self.tracks()) + tuple(self.returns())

    def sel_track(self, _oTrack = None):
        if (_oTrack != None):
            self.song().view.selected_track = _oTrack
        return self.song().view.selected_track

    def sel_track_idx_abs(self):
        aAllTracks = self.tracks_and_returns()
        oSelTrack  = self.sel_track()
        return list(aAllTracks).index(oSelTrack)


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

