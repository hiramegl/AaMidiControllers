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

class AaRotary(ControlSurface):
    __doc__ = "AaRotary controller"

    def __init__(self, _oCtrlInstance):
        ControlSurface.__init__(self, _oCtrlInstance)
        self.m_oCtrlInstance = _oCtrlInstance
        self.m_sProductName  = 'AaRotary'
        self.m_nNumTracks    = 8

        with self.component_guard():
            self.load_config()
            self.setup_session()
            self.setup_mixer()
            self.m_oSession.set_mixer(self.m_oMixer)
            self.setup_device()
            self.set_highlighting_session_component(self.m_oSession)
            self.xlog('initialized controller!')

    def disconnect(self):
        self.remove_highlight()
        self.m_oButToSelected.remove_value_listener(self._on_to_selected)
        self.m_oButBank1Sync.remove_value_listener(self._on_bank_1_sync)
        self.m_oButBank2Sync.remove_value_listener(self._on_bank_2_sync)
        self.m_oButBank3Sync.remove_value_listener(self._on_bank_3_sync)
        self.m_oButBank4Sync.remove_value_listener(self._on_bank_4_sync)
        self.m_oButBank5Sync.remove_value_listener(self._on_bank_5_sync)
        self.m_oButBank6Sync.remove_value_listener(self._on_bank_6_sync)
        ControlSurface.disconnect(self)
        self.xlog('disconnected!')

    def load_config(self):
        self.m_sDevicesDir = 'devices'

        # default configuration ************************************************
        self.m_hCfg = {
            'oCtrlInst'   : self.m_oCtrlInstance,
            'sProductName': self.m_sProductName,
            'sProductDir' : 'AaConfig/%s' % (self.m_sProductName),
            'sDevicesDir' : self.m_sDevicesDir,

            'NumTracks'   : 1,  'NumScenes'   : 4,
            'NumBanks'    : 6,  'Bank0Channel': 8, # MIDI-CHANNEL 9
            'SessionLeft' : 5,  'SessionRight': 6, # for all BCR2000 presets!
            'ToSelected'  : 7,                     # Move focus to selected track

            'LogNotMapped': 0,                     # Log not mapped parameters
            'LogNotFound' : 0,                     # Log not found preset files
            'LogLoadedDev': 0,                     # Log loaded devices
            'LogParsedPre': 0,                     # Log parsed presets

            'Bank1Sync'   : 8,  'Bank1Channel': 0, # MIDI-CHANNEL 1
            'Bank2Sync'   : 9,  'Bank2Channel': 1, # MIDI-CHANNEL 2
            'Bank3Sync'   : 10, 'Bank3Channel': 2, # MIDI-CHANNEL 3
            'Bank4Sync'   : 11, 'Bank4Channel': 3, # MIDI-CHANNEL 4
            'Bank5Sync'   : 12, 'Bank5Channel': 4, # MIDI-CHANNEL 5
            'Bank6Sync'   : 13, 'Bank6Channel': 5, # MIDI-CHANNEL 6
            'Main': {
                'Button': [65, 73],
                'Rotary': [81, 89, 97],
            },
            'Group': {
                'Button': [33, 41, 1, 57],
                'Rotary': [49, 9, 17, 25],
            },
            'devices': {
                # Audio Effects (6 banks)
                'Vocoder'         : {},
                'Overdrive'       : {},
                'BeatRepeat'      : {},
                'Compressor2'     : {},

                'Resonator'       : {},
                'AutoPan'         : {},

                'Echo'            : {},
                'Delay'           : {},

                'FilterDelay'     : {},
                'GrainDelay'      : {},
                'Chorus'          : {},

                'Flanger'         : {},
                'FrequencyShifter': {},
                'Phaser'          : {},

                'Reverb'          : {},
                'Eq8'             : {},
                'FilterEQ3'       : {},
                'Redux'           : {},

                'AudioEffectGroupDevice': {},
                'InstrumentGroupDevice' : {},
                'DrumGroupDevice' : {},

                # Instruments
                'UltraAnalog'     : {},
                'Collision'       : {},
                'LoungeLizard'    : {},
                'Operator'        : {},
                'MultiSampler'    : {},
                'OriginalSimpler' : {},
                'StringStudio'    : {},
                'InstrumentVector': {},
            },
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
            aParts = list(sToken.capitalize() for sToken in sName.split('_'))
            if (aParts[0] == 'Main' or aParts[0] == 'Group'):
                nIdx = int(aParts[2])
                nVal = int(sValue)
                self.m_hCfg[aParts[0]][aParts[1]][nIdx] = nVal
            else:
                sKey = ''.join(aParts)
                self.m_hCfg[sKey] = int(sValue)

        # parse device's config files
        for sDevice in self.m_hCfg['devices']:
            sFilePath = '%s/%s/%s/%s_config.txt' % (sHome, self.m_hCfg['sProductDir'], self.m_sDevicesDir, sDevice)
            bFileExists = os.path.isfile(sFilePath)
            if (bFileExists == False):
                self.log('> config file "%s" not found!' % (sFilePath))
                continue # device config file does not exist, nothing else to do here!
            self.m_hCfg['devices'][sDevice] = {
                'param_cfgs' : {},
                'lineup'     : [],
                'preset_cfgs': [],
            }
            hDevice = self.m_hCfg['devices'][sDevice]

            # parse config file, line by line
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
                sParam = aTokens[0].strip()
                sParam = sParam.replace('_', ' ')
                sValue = aTokens[1].strip()
                # parse the value of the config feature
                #self.xlog('   parsed: %22s => %s' % (sParam, sValue))
                aValues = sValue.split('_') # sPanel, sType, nRowIdx, nStripIdx, nBankOffset
                if (len(aValues) == 4): aValues.append(0)
                hDevice['param_cfgs'][sParam] = (aValues[0], aValues[1], int(aValues[2]), int(aValues[3]), int(aValues[4]))

            sFilePath = '%s/%s/%s/%s_presets.txt' % (sHome, self.m_hCfg['sProductDir'], self.m_sDevicesDir, sDevice)
            bFileExists = os.path.isfile(sFilePath)
            if (bFileExists == False):
                if self.m_hCfg['LogNotFound'] == 1:
                    self.log('> presets file "%s" not found!' % (sFilePath))
                continue # device config file does not exist, nothing else to do here!

            # parse presets file, line by line
            self.log('reading: "%s"' % (sFilePath))
            oFile = open(sFilePath, 'r')
            for sLine in oFile:
                sLine = sLine.strip()
                if (len(sLine) == 0): continue
                if (sLine[0] == '#'): continue
                if (sLine[0] == '@'):
                    aLine = sLine.split(':')
                    hDevice['lineup'] = aLine[1].split('|')
                    continue # nothing else to do here

                aLine   = sLine.split('#')      # used to separate values from end-of-line comment
                aTokens = aLine[0].split(':')   # used to separate name of the preset from values
                sName   = aTokens[0].strip()    # the first token is the name of the preset
                aValues = aTokens[1].split('|') # used to separate values
                aPreset = [sName]
                for sValue in aValues:
                    aPreset.append(float(sValue.strip()))
                hDevice['preset_cfgs'].append(aPreset)
                if self.m_hCfg['LogParsedPre'] == 1:
                    self.xlog('   parsed: %22s => %s' % (sName, ' / '.join(list(str(oValue) for oValue in aPreset))))

        self.m_nNumTracks = self.m_hCfg['NumTracks']
        self.xlog('config loaded succesfully!')

    def setup_session(self):
        self.m_oSession = SpecialSessionComponent(self.m_nNumTracks, self.m_hCfg['NumScenes'])
        self.m_oSession.name = 'Session'
        oSession = self.m_oSession
        self.m_hCfg['oSession'] = oSession

        oSession.set_page_left_button (self.create_toggle('SessionLeft' , 0))
        oSession.set_page_right_button(self.create_toggle('SessionRight', 0))

        self.m_oButToSelected = self.create_button('ToSelected', 0)
        self._on_to_selected.subject = self.m_oButToSelected

        self.m_oButBank1Sync = self.create_button('Bank1Sync', 0)
        self._on_bank_1_sync.subject = self.m_oButBank1Sync
        self.m_oButBank2Sync = self.create_button('Bank2Sync', 0)
        self._on_bank_2_sync.subject = self.m_oButBank2Sync
        self.m_oButBank3Sync = self.create_button('Bank3Sync', 0)
        self._on_bank_3_sync.subject = self.m_oButBank3Sync
        self.m_oButBank4Sync = self.create_button('Bank4Sync', 0)
        self._on_bank_4_sync.subject = self.m_oButBank4Sync
        self.m_oButBank5Sync = self.create_button('Bank5Sync', 0)
        self._on_bank_5_sync.subject = self.m_oButBank5Sync
        self.m_oButBank6Sync = self.create_button('Bank6Sync', 0)
        self._on_bank_6_sync.subject = self.m_oButBank6Sync

    def setup_mixer(self):
        self.m_oMixer = SpecialMixerComponent(self.m_nNumTracks, self.m_hCfg)
        self.m_oMixer.name = 'Mixer'
        oMixer = self.m_oMixer

        for nTrack in range(self.m_nNumTracks):
            oMixerStrip = oMixer.channel_strip(nTrack)
            oMixerStrip.name = 'Channel_Strip_' + str(nTrack)

    def setup_device(self):
        self.m_oDevice = DeviceComponent()
        self.m_oDevice.name = 'Device_Component'
        self.set_device_component(self.m_oDevice)

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
    def _on_bank_1_sync(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        self._sync_bank(0)

    @subject_slot(u'value')
    def _on_bank_2_sync(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        self._sync_bank(1)

    @subject_slot(u'value')
    def _on_bank_3_sync(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        self._sync_bank(2)

    @subject_slot(u'value')
    def _on_bank_4_sync(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        self._sync_bank(3)

    @subject_slot(u'value')
    def _on_bank_5_sync(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        self._sync_bank(4)

    @subject_slot(u'value')
    def _on_bank_6_sync(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        self._sync_bank(5)

    def _sync_bank(self, _nBankIdx):
        # update page buttons
        nLeftValue  = 127 if self.m_oSession._can_scroll_page_left()  else 0
        nRightValue = 127 if self.m_oSession._can_scroll_page_right() else 0
        self.m_oSession._page_left_button.send_value(nLeftValue, True)
        self.m_oSession._page_right_button.send_value(nRightValue, True)

        # update track values
        self.m_oMixer.send_bank_values(_nBankIdx) # index is 0-based
        self.alert('> Synced Bank %d' % (_nBankIdx + 1))

    @subject_slot(u'value')
    def _on_to_selected(self, _nValue):
        if (_nValue < 64): return # only process toggle on
        nSelTrackIdxAbs = self.sel_track_idx_abs()
        self.log('to selected: %d' % (nSelTrackIdxAbs))
        self.m_oSession.set_offsets(nSelTrackIdxAbs, self.m_oSession.scene_offset())

        # update page buttons
        nLeftValue  = 127 if self.m_oSession._can_scroll_page_left()  else 0
        nRightValue = 127 if self.m_oSession._can_scroll_page_right() else 0
        self.m_oSession._page_left_button.send_value(nLeftValue, True)
        self.m_oSession._page_right_button.send_value(nRightValue, True)

    # ****************************************************************

    def get_el_config(self, _sName, _nBank, _nIndex = None):
        nMidiType = MIDI_CC_TYPE
        nChannel  = self.m_hCfg['Bank%dChannel' % (_nBank)]
        sKey      = _sName
        nOffset   = 0
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
