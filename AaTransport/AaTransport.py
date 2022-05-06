from __future__ import with_statement

import os
import time
import datetime
import Live

NavDirection = Live.Application.Application.View.NavDirection

from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent

from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.SliderElement import SliderElement
from _Framework.SubjectSlot import subject_slot

from SpecialMixerComponent import SpecialMixerComponent
from SpecialSessionComponent import SpecialSessionComponent
from SpecialTransportComponent import SpecialTransportComponent

class AaTransport(ControlSurface):
    __doc__ = "AaTransport controller"

    def __init__(self, _oCtrlInstance):
        ControlSurface.__init__(self, _oCtrlInstance)
        self.m_oCtrlInstance = _oCtrlInstance
        self.m_sProductName  = 'AaTransport'

        with self.component_guard():
            self.load_config()
            self.setup_session()
            self.setup_mixer()
            self.m_oSession.set_mixer(self.m_oMixer)
            self.setup_device()
            self.setup_transport()
            self.set_highlighting_session_component(self.m_oSession)
            self.xlog('initialized controller!')


    def disconnect(self):
        self.remove_highlight()
        for sName in self.m_hListeners:
            self.get_el(sName).remove_value_listener(self.m_hListeners[sName])
        ControlSurface.disconnect(self)
        self.xlog('disconnected!')


    def load_config(self):
        self.m_nNumTracks = 6

        # default configuration ************************************************
        self.m_hCfg   = {
            'oCtrlInst'   : self.m_oCtrlInstance,
            'sProductName': self.m_sProductName,
            'sProductDir' : 'AaConfig/%s' % (self.m_sProductName),

            'bLog'        : True,
            'NumScenes'   : 1,   'Channel'    : 4,
            'TempoMax'    : 144, 'TempoMin'   : 80,

            # fixed config:
            'SessionLeft' : 67, 'SessionRight': 64, 'Crossfader' : 9,
            'PanOffset'   : 1,  'VolOffset'   : 10,
            'Tempo'       : 8,  'CueVol'      : 17,
            'MasterPan'   : 57, 'MasterVol'   : 58, 'ViewToggle' : 59,

            # bank 1 & 2: session
            'Loop'        : 26, 'Rewind'      : 27, 'Forward'    : 28,
            'StopTotal'   : 29, 'Play'        : 30, 'Record'     : 31,

            # bank 3 & 4: clip
            'ClipLoop'    : 76, 'Warp'        : 77, 'FollowSong' : 78,
            'StopClip'    : 79, 'PlayClip'    : 80, 'DupClip'    : 81,

            # bank 1: select
            'TrackSelAbs' : 7,  'SceneSelAbs' : 16,
            'SceneSelUp'  : 24, 'SceneSelDw'  : 25,
            'SelOffset'   : 18,
            'DeviceLeft'  : 60, 'DeviceRight' : 61,

            # bank 2: tempo
            'TempoTarget' : 62, 'TempoVel'    : 63,
            'TempoAuto'   : 39, 'TempoReset'  : 40,
            'MuteOffset'  : 33,
            'TempoWinDec' : 65, 'TempoWinInc' : 66,

            # bank 3: clip start / sel track
            'ClipGain'    : 68, 'StartSize'   : 69,
            'StartDec'    : 47, 'StartInc'    : 48,
            'SoloOffset'  : 41,
            'TrackSelLf'  : 70, 'TrackSelRg'  : 71,

            # bank 3: loop
            'LoopSize'    : 72, 'ShiftSize'   : 73,
            'ResetOffset' : 49,
            'ShiftDec'    : 55, 'ShiftInc'    : 56,
            'LoopDiv'     : 74, 'LoopMul'     : 75,
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
            #self.xlog('   parsing: %16s | %s' % (sName, sValue))
            # parse the value of the config feature
            if (sName == 'log'):
                self.m_hCfg['bLog'] = (sValue == 'true')
            else:
                sKey = "n%s" % (''.join(sToken.capitalize() for sToken in sName.split('_')))
                self.m_hCfg[sKey] = int(sValue)
        self.xlog('config loaded succesfully!')

    # ****************************************************************

    def setup_session(self):
        self.m_hEls       = {}
        self.m_hListeners = {}
        self.m_oSession   = SpecialSessionComponent(self.m_nNumTracks, self.m_hCfg['NumScenes'])
        self.m_oSession.name = 'Session'
        oSession = self.m_oSession

        oSession.set_page_left_button (self.create_button('SessionLeft'))
        oSession.set_page_right_button(self.create_button('SessionRight'))
        oSession.set_select_buttons   (self.create_button('SceneSelDw'), self.create_button('SceneSelUp'))
        self.register_el('but', 'ViewToggle' , self._on_view_toggle) # 'Detail/Clip' <=> 'Detail/DeviceChain' toggle
        self.register_el('enc', 'SceneSelAbs', self._on_scene_sel_abs)


    def setup_mixer(self):
        self.m_oMixer = SpecialMixerComponent(self.m_nNumTracks)
        self.m_oMixer.name = 'Mixer'
        oMixer = self.m_oMixer

        oMixer.set_crossfader_control    (self.create_encoder('Crossfader'))
        oMixer.set_prehear_volume_control(self.create_encoder('CueVol'))
        oMixer.master_strip().set_pan_control   (self.create_encoder('MasterPan'))
        oMixer.master_strip().set_volume_control(self.create_encoder('MasterVol'))
        oMixer.set_select_buttons(self.create_button('TrackSelRg'), self.create_button('TrackSelLf'))
        self.register_el('enc', 'TrackSelAbs', self._on_track_sel_abs)

        for nTrack in range(self.m_nNumTracks):
            oStrip = oMixer.channel_strip(nTrack)
            oStrip.name = 'Channel_Strip_' + str(nTrack)
            oStrip.set_surface_ctrl  (self)
            oStrip.set_pan_control   (self.create_encoder('PanOffset'  , nTrack))
            oStrip.set_volume_control(self.create_slider ('VolOffset'  , nTrack))
            oStrip.set_select_button (self.create_button ('SelOffset'  , nTrack))
            oStrip.set_mute_button   (self.create_button ('MuteOffset' , nTrack))
            oStrip.set_solo_button   (self.create_button ('SoloOffset' , nTrack))
            oStrip.set_reset_control (self.create_button ('ResetOffset', nTrack))

    def setup_device(self):
        self.m_oDevice = DeviceComponent()
        self.m_oDevice.name = 'Device_Component'
        self.set_device_component(self.m_oDevice)

    def setup_transport(self):
        self.m_oTransport = SpecialTransportComponent(self.m_hCfg)
        self.m_oTransport.name = 'Transport'
        oTransp = self.m_oTransport

        oTransp.set_loop_button  (self.create_button('Loop'))
        oTransp.set_seek_buttons (self.create_toggle('Forward'), self.create_toggle('Rewind'))
        oTransp.set_record_button(self.create_button('Record'))
        #oTransp.set_play_button  (self.create_button('Play'))
        self.register_el('but', 'Play'     , self._on_play)
        self.register_el('but', 'StopTotal', self._on_stop_total)

        self.register_el('but', 'ClipLoop'  , self._on_clip_loop)
        self.register_el('but', 'Warp'      , self._on_warp)
        self.register_el('but', 'FollowSong', self._on_follow_song)
        self.register_el('but', 'StopClip'  , self._on_stop_clip)
        self.register_el('but', 'PlayClip'  , self._on_play_clip)
        self.register_el('but', 'DupClip'   , self._on_dup_clip)

        self.m_nStartSize = 1.0 # 1 beat
        self.register_el('enc', 'ClipGain'   , self._on_clip_gain)
        self.register_el('enc', 'StartSize'  , self._on_start_size)
        self.register_el('but', 'StartDec'   , self._on_start_dec)
        self.register_el('but', 'StartInc'   , self._on_start_inc)
        self.register_el('but', 'DeviceLeft' , self._on_device_left)
        self.register_el('but', 'DeviceRight', self._on_device_right)

        self.m_nShiftSize = 1.0 # 1 beat
        self.register_el('enc', 'LoopSize' , self._on_loop_size)
        self.register_el('enc', 'ShiftSize', self._on_shift_size)
        self.register_el('but', 'ShiftDec', self._on_shift_dec)
        self.register_el('but', 'ShiftInc', self._on_shift_inc)
        self.register_el('but', 'LoopDiv', self._on_loop_div)
        self.register_el('but', 'LoopMul', self._on_loop_mul)

    # ****************************************************************

    @subject_slot(u'value')
    def _on_view_toggle(self, _nValue):
        if (_nValue < 64): # do not process "toggle off"
            return
        # available: Browser, Arranger, Session, Detail, Detail/Clip, Detail/DeviceChain
        oView = self.application().view
        oView.show_view('Detail')
        oView.focus_view('Detail')
        if (oView.is_view_visible('Detail/Clip')):
            oView.show_view('Detail/DeviceChain')
            oView.focus_view('Detail/DeviceChain')
        else:
            oView.show_view('Detail/Clip')
            oView.focus_view('Detail/Clip')


    @subject_slot(u'value')
    def _on_track_sel_abs(self, _nValue):
        aVisTracks = self.song().visible_tracks
        nVisTracks = len(aVisTracks)
        nDenom     = 128 / nVisTracks
        nTrackAbs  = _nValue / nDenom
        if (nTrackAbs >= nVisTracks):
            nTrackAbs = nVisTracks - 1
        self.sel_track(aVisTracks[nTrackAbs])


    @subject_slot(u'value')
    def _on_scene_sel_abs(self, _nValue):
        aScenes = self.scenes()
        nScenes = len(aScenes)
        nDenom  = 128 / nScenes
        if nDenom == 0: return
        nSceneAbs = (127 - _nValue) / nDenom
        if (nSceneAbs >= nScenes):
            nSceneAbs = nScenes - 1
        self.sel_scene(aScenes[nSceneAbs])


    @subject_slot(u'value')
    def _on_stop_total(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot != None):
            oClipSlot.stop()


    @subject_slot(u'value')
    def _on_play(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot != None):
            oClipSlot.fire()


    @subject_slot(u'value')
    def _on_clip_loop(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot == None): return
        oClip = oClipSlot.clip
        if (oClip == None): return
        bLooping      = oClip.looping
        oClip.looping = not bLooping


    @subject_slot(u'value')
    def _on_warp(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot == None): return
        oClip = oClipSlot.clip
        if (oClip == None): return
        bWarping      = oClip.warping
        oClip.warping = not bWarping


    @subject_slot(u'value')
    def _on_follow_song(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        bFollowing = self.song().view.follow_song
        self.song().view.follow_song = not bFollowing


    @subject_slot(u'value')
    def _on_stop_clip(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot != None):
            oClipSlot.stop()


    @subject_slot(u'value')
    def _on_play_clip(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot != None):
            oClipSlot.fire()


    @subject_slot(u'value')
    def _on_dup_clip(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        nSelSceneIdxAbs = self.sel_scene_idx_abs()
        self.sel_track().duplicate_clip_slot(nSelSceneIdxAbs)


    @subject_slot(u'value')
    def _on_clip_gain(self, _nValue):
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot == None): return
        oClip = oClipSlot.clip
        if (oClip == None): return
        oClip.gain = float(_nValue) / 127.0


    @subject_slot(u'value')
    def _on_start_size(self, _nValue):
        nIndex = _nValue / 20

        if (nIndex == 0):
            self.m_nStartSize = 0.125
        elif (nIndex == 1):
            self.m_nStartSize = 0.25
        elif (nIndex == 2):
            self.m_nStartSize = 0.5
        elif (nIndex == 3):
            self.m_nStartSize = 1.0
        elif (nIndex == 4):
            self.m_nStartSize = 2.0
        elif (nIndex == 5):
            self.m_nStartSize = 4.0
        else:
            self.m_nStartSize = 8.0

        self.alert('> Start size: %f' % (self.m_nStartSize))


    @subject_slot(u'value')
    def _on_start_dec(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot == None): return
        oClip = oClipSlot.clip
        if (oClip == None): return
        nStart = oClip.start_marker
        oClip.start_marker = nStart - self.m_nStartSize


    @subject_slot(u'value')
    def _on_start_inc(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot == None): return
        oClip = oClipSlot.clip
        if (oClip == None): return
        nStart = oClip.start_marker
        oClip.start_marker = nStart + self.m_nStartSize


    @subject_slot(u'value')
    def _on_device_left(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        oView = self.application().view
        oView.show_view(u'Detail/DeviceChain')
        oView.focus_view(u'Detail/DeviceChain')
        oView.scroll_view(NavDirection.left, u'Detail/DeviceChain', False)


    @subject_slot(u'value')
    def _on_device_right(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        oView = self.application().view
        oView.show_view(u'Detail/DeviceChain')
        oView.focus_view(u'Detail/DeviceChain')
        oView.scroll_view(NavDirection.right, u'Detail/DeviceChain', False)


    @subject_slot(u'value')
    def _on_loop_size(self, _nValue):
        nIndex = _nValue / 20

        if (nIndex == 0):
            nLoopLen = 0.25
        elif (nIndex == 1):
            nLoopLen = 0.5
        elif (nIndex == 2):
            nLoopLen = 1.0
        elif (nIndex == 3):
            nLoopLen = 2.0
        elif (nIndex == 4):
            nLoopLen = 4.0
        elif (nIndex == 5):
            nLoopLen = 8.0
        else:
            nLoopLen = 16.0

        oClipSlot = self.sel_clip_slot()
        if (oClipSlot == None): return
        oClip = oClipSlot.clip
        if (oClip == None): return
        nLoopStart     = oClip.loop_start
        oClip.loop_end = nLoopStart + nLoopLen


    @subject_slot(u'value')
    def _on_shift_size(self, _nValue):
        nIndex = _nValue / 20

        if (nIndex == 0):
            self.m_nShiftSize = 0.125
        elif (nIndex == 1):
            self.m_nShiftSize = 0.25
        elif (nIndex == 2):
            self.m_nShiftSize = 0.5
        elif (nIndex == 3):
            self.m_nShiftSize = 1.0
        elif (nIndex == 4):
            self.m_nShiftSize = 2.0
        elif (nIndex == 5):
            self.m_nShiftSize = 4.0
        else:
            self.m_nShiftSize = 8.0

        self.alert('> Shift size: %f' % (self.m_nShiftSize))


    @subject_slot(u'value')
    def _on_shift_dec(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot == None): return
        oClip = oClipSlot.clip
        if (oClip == None): return
        nLoopStart = oClip.loop_start
        nLoopEnd   = oClip.loop_end
        oClip.loop_start = nLoopStart - self.m_nShiftSize
        oClip.loop_end   = nLoopEnd   - self.m_nShiftSize


    @subject_slot(u'value')
    def _on_shift_inc(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot == None): return
        oClip = oClipSlot.clip
        if (oClip == None): return
        nLoopStart = oClip.loop_start
        nLoopEnd   = oClip.loop_end
        oClip.loop_end   = nLoopEnd   + self.m_nShiftSize
        oClip.loop_start = nLoopStart + self.m_nShiftSize


    @subject_slot(u'value')
    def _on_loop_div(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot == None): return
        oClip = oClipSlot.clip
        if (oClip == None): return
        nLoopStart = oClip.loop_start
        nLoopEnd   = oClip.loop_end
        nLoopSpan  = (nLoopEnd - nLoopStart) / 2
        oClip.loop_end = nLoopStart + nLoopSpan


    @subject_slot(u'value')
    def _on_loop_mul(self, _nValue):
        if (_nValue < 64): return # do not process "toggle off"
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot == None): return
        oClip = oClipSlot.clip
        if (oClip == None): return
        nLoopStart = oClip.loop_start
        nLoopEnd   = oClip.loop_end
        nLoopSpan  = (nLoopEnd - nLoopStart) * 2
        oClip.loop_end = nLoopStart + nLoopSpan

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
        self.m_oTransport.update_sync_tasks()

    # ****************************************************************

    # F0, 42, 40, 00, 01, 04, 00, 5F, 4F, 0X, F7
    def handle_sysex(self, midi_bytes):
        if len(midi_bytes) == 11:
            if midi_bytes == (240, 66, 64, 0, 1, 4, 0, 95, 79, 0, 247):
                self.alert('AaTransport => SELECT')
            elif midi_bytes == (240, 66, 64, 0, 1, 4, 0, 95, 79, 1, 247):
                self.alert('AaTransport => SOLO / TEMPO')
            elif midi_bytes == (240, 66, 64, 0, 1, 4, 0, 95, 79, 2, 247):
                self.alert('AaTransport => MUTE / TRACK SEL / CLIP: START, GAIN, DUPL')
            elif midi_bytes == (240, 66, 64, 0, 1, 4, 0, 95, 79, 3, 247):
                self.alert('AaTransport => LOOP / LOOP DUPL / CLIP DUPL')
        else:
            ControlSurface.handle_sysex(self,midi_bytes)

    # ****************************************************************

    def register_el(self, _sType, _sName, _fListener):
        if (_sType == 'but'):
            _fListener.subject = self.create_button(_sName)
        elif (_sType == 'enc'):
            _fListener.subject = self.create_encoder(_sName)
        elif (_sType == 'tog'):
            _fListener.subject = self.create_toggle(_sName)
        elif (_sType == 'sli'):
            _fListener.subject = self.create_slider(_sName)
        self.m_hListeners[_sName] = _fListener


    def get_el_ids(self, _sName, _nIndex = None):
        sKey         = _sName
        nOffset      = 0
        if (_nIndex != None):
            nOffset = _nIndex
            _sName  = '%s_%d' % (_sName, _nIndex)
        return (_sName, sKey, nOffset)


    def create_button(self, _sName, _nIndex = None):
        bIsMomentary = True
        nMidiType    = MIDI_CC_TYPE
        nChannel     = self.m_hCfg['Channel']
        sName, sKey, nOffset = self.get_el_ids(_sName, _nIndex)
        oBut = ButtonElement(bIsMomentary, nMidiType, nChannel, self.m_hCfg[sKey] + nOffset, name = sName)
        self.m_hEls[sName] = oBut
        return oBut


    def create_toggle(self, _sName, _nIndex = None):
        bIsMomentary = False
        nMidiType    = MIDI_CC_TYPE
        nChannel     = self.m_hCfg['Channel']
        sName, sKey, nOffset = self.get_el_ids(_sName, _nIndex)
        oBut = ButtonElement(bIsMomentary, nMidiType, nChannel, self.m_hCfg[sKey] + nOffset, name = sName)
        self.m_hEls[sName] = oBut
        return oBut


    def create_encoder(self, _sName, _nIndex = None):
        return self.create_button(_sName, _nIndex)


    def create_slider(self, _sName, _nIndex = None):
        nMidiType    = MIDI_CC_TYPE
        nChannel     = self.m_hCfg['Channel']
        sName, sKey, nOffset = self.get_el_ids(_sName, _nIndex)
        oSlider = SliderElement(nMidiType, nChannel, self.m_hCfg[sKey] + nOffset, name = sName)
        self.m_hEls[sName] = oSlider
        return oSlider


    def get_el(self, _sName, _nIndex = None):
        sName, sKey, nOffset = self.get_el_ids(_sName, _nIndex)
        return self.m_hEls[sName]

    # ****************************************************************

    def sel_clip_slot(self):
        return self.song().view.highlighted_clip_slot

    def sel_scene_idx_abs(self):
        aAllScenes = self.scenes()
        oSelScene  = self.sel_scene()
        return list(aAllScenes).index(oSelScene)

    def scenes(self):
        return self.song().scenes

    def sel_scene(self, _oScene = None):
        if (_oScene != None):
            self.song().view.selected_scene = _oScene
        return self.song().view.selected_scene

    def sel_track(self, _oTrack = None):
        if (_oTrack != None):
            self.song().view.selected_track = _oTrack
        return self.song().view.selected_track

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

