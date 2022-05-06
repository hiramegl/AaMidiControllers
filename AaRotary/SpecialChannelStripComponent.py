import os
import time
import math
import datetime
import Live

from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.ChannelStripComponent import ChannelStripComponent

BUTTON_OFF = 0
BUTTON_ON  = 127

TRACK_FOLD_DELAY = 5

class SpecialChannelStripComponent(ChannelStripComponent):
    ' Subclass of channel strip component using select button for (un)folding tracks '
    __module__ = __name__

    def __init__(self, _hCfg):
        ChannelStripComponent.__init__(self)
        self.m_hCfg      = _hCfg
        self.m_nBanks    = _hCfg['NumBanks']
        self.m_nStrips   = 8 # 8 strips in a BCR-2000
        self.m_oCtrlInst = _hCfg['oCtrlInst']
        self.m_oSong     = _hCfg['oCtrlInst'].song()
        self.m_bBusy     = False
        self.m_hDevCfgs  = { # devices with explicit configuration
            # Audio effects
            'Vocoder'         : { 'strips': 3 },
            'Overdrive'       : { 'strips': 1 },
            'BeatRepeat'      : { 'strips': 2, 'extra_functions': ['Pitch Reset','PDecay Reset','Volume Reset', 'Decay Reset'] },
            'Compressor2'     : { 'strips': 2 },

            'Resonator'       : { 'strips': 6 },
            'AutoPan'         : { 'strips': 2 },

            'Echo'            : { 'strips': 6 },
            'Delay'           : { 'strips': 2 },

            'FilterDelay'     : { 'strips': 4 },
            'GrainDelay'      : { 'strips': 2 },
            'Chorus'          : { 'strips': 2 },

            'Flanger'         : { 'strips': 3 },
            'Phaser'          : { 'strips': 3 },
            'FrequencyShifter': { 'strips': 2 },

            'Reverb'          : { 'strips': 3 },
            'Eq8'             : { 'strips': 2, 'extra_functions': ['Center Freq', 'Q', '1 Auto Inc', '1 Auto Dec', '2 Auto Dec', '2 Auto Inc', 'Auto Time', 'Auto Q Dec', 'Auto Q Inc'] },
            'FilterEQ3'       : { 'strips': 1 },
            'Redux'           : { 'strips': 1 },

            'AudioEffectGroupDevice': { 'strips': 2, 'extra_functions': ['Fade Out'] },
            'InstrumentGroupDevice' : { 'strips': 4, 'use_orig': True },
            'DrumGroupDevice'       : { 'strips': 2, 'drum_map': True },

            # instruments
            'UltraAnalog'     : { 'banks': 3, 'strips': 8 },
            'Collision'       : { 'banks': 3, 'strips': 8 },
            'LoungeLizard'    : { 'banks': 1, 'strips': 8 },
            'Operator'        : { 'banks': 4, 'strips': 8 },
            'MultiSampler'    : { 'banks': 3, 'strips': 8 },
            'OriginalSimpler' : {
                'banks' : 3,
                'strips': 8,
                'extra_functions': [
                    'Playback Mode',
                    'Retrigger',
                    'Voices',
                    'Reverse',
                    'Crop',
                    'Warp As',
                    'Warp Double',
                    'Warp Half',
                    'Slicing Playback Mode',
                    'Gain',
                    'Warp',
                    'Warp Mode',
                    'Start Marker Pos',
                    'Start Marker Res',
                    'End Marker Pos',
                    'End Marker Res',
                    'Beats Gran Res',
                    'Beats Trans Loop Mode',
                    'Beats Trans Envelope',
                    'Tones Grain Size',
                    'Texture Grain Size',
                    'Texture Flux',
                    'Complex Pro Formants',
                    'Complex Pro Envelope',
                    'Slicing Style',
                    'Slicing Sensitivity',
                    'Slicing Beat Division',
                    'Slicing Region Count',
                    'Clear Slices',
                ] },
            'StringStudio'    : { 'banks': 3, 'strips': 8 },
            'InstrumentVector': { 'banks': 3, 'strips': 8 },
        }
        self.m_nNumUsedBanks = 0
        self.m_nLogNotMapped = _hCfg['LogNotMapped']
        self.m_nLogLoadedDev = _hCfg['LogLoadedDev']
        self._toggle_fold_ticks_delay = -1
        self._register_timer_callback(self._on_timer)
        self.init_midi_ctls()

    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        self.disconnect_ctls(True)
        ChannelStripComponent.disconnect(self)

    def _select_value(self, value):
        ChannelStripComponent._select_value(self, value)
        if (self.is_enabled() and (self._track != None)):
            if (self._track.is_foldable and (self._select_button.is_momentary() and (value != 0))):
                self._toggle_fold_ticks_delay = TRACK_FOLD_DELAY
            else:
                self._toggle_fold_ticks_delay = -1

    def _on_timer(self):
        if (self.is_enabled() and (self._track != None)):
            if (self._toggle_fold_ticks_delay > -1):
                assert self._track.is_foldable
                if (self._toggle_fold_ticks_delay == 0):
                    self._track.fold_state = (not self._track.fold_state)
                self._toggle_fold_ticks_delay -= 1

    def init_midi_ctls(self):
        self.m_hMidiCtls = {}
        self.m_hDevReg   = {}

        # common configuration parameters
        bIsMomentary = True
        nMidiType    = MIDI_CC_TYPE

        # create midi controls map
        for nBankIdx in range(self.m_nBanks):
            hBank    = {}
            nChannel = self.m_hCfg['Bank%dChannel' % (nBankIdx + 1)]
            self.m_hMidiCtls[nBankIdx] = hBank
            for nStripIdx in range(self.m_nStrips):
                hStrip = {}
                hBank[nStripIdx] = hStrip
                for sPanel in ('Main', 'Group'):
                    hPanel = {}
                    hStrip[sPanel] = hPanel
                    for sType in ('Button', 'Rotary'):
                        hType = {}
                        hPanel[sType] = hType
                        aOffsets = self.m_hCfg[sPanel][sType]
                        for nCtlIdx in range(len(aOffsets)):
                            nOffset  = aOffsets[nCtlIdx]
                            nControl = nOffset + nStripIdx
                            sName    = 'ctl_%d_%d_%s_%s_%d_%d' % (nBankIdx, nStripIdx, sPanel, sType, nCtlIdx, nControl)
                            hType[nCtlIdx] = {
                                'control': ButtonElement(bIsMomentary, nMidiType, nChannel, nControl, name = sName)
                            }

    def disconnect_ctls(self, _bClear):
        nBanks = self.m_nBanks if _bClear else self.m_nNumUsedBanks
        for nBankIdx in range(nBanks):
            hBank = self.m_hMidiCtls[nBankIdx]
            for nStripIdx in range (self.m_nStrips):
                hStrip = hBank[nStripIdx]
                for sPanel in ('Main', 'Group'):
                    hPanel = hStrip[sPanel]
                    for sType in ('Button', 'Rotary'):
                        hType = hPanel[sType]
                        for nCtlIdx in hType.keys(): # nCtlIdx => 0, 1, 2, 3
                            hMidiCtl = hType[nCtlIdx]
                            if (_bClear):
                                hMidiCtl['control'].send_value(0, True)
                            hMidiCtl['control'].release_parameter()
                            if ('slot' in hMidiCtl):
                                hMidiCtl['slot'].disconnect()
                            #self.log('>> disconnected, bank %d, strip %d, panel %s, type %s, idx %d' % (nBankIdx, nStripIdx, sPanel, sType, nCtlIdx))

        if (_bClear): # remove references to the device parameters and controls, we are shutting down Ableton Live!
            for nTrackAbsIdx in self.m_hDevReg:
                hDevices = self.m_hDevReg[nTrackAbsIdx]
                for sDevice in hDevices:
                    hDevice = hDevices[sDevice]
                    for sParam in hDevice['dev_params']:
                        hDevice['dev_params'][sParam]['param']   = None
                        hDevice['dev_params'][sParam]['control'] = None
                    for sParam in hDevice['panel_params']:
                        hDevice['panel_params'][sParam]['param']   = None
                        hDevice['panel_params'][sParam]['control'] = None
                    if ('extra_params' in hDevice):
                        for sParam in hDevice['extra_params']:
                            hDevice['extra_params'][sParam]['param']   = None
                            hDevice['extra_params'][sParam]['control'] = None
                    if ('auto_params' in hDevice):
                        for sParam in hDevice['auto_params']['param_refs']:
                            hDevice['auto_params']['param_refs'][sParam]['param']   = None
                            hDevice['auto_params']['param_refs'][sParam]['control'] = None

    # ****************************************************************

    def _connect_parameters(self):
        ChannelStripComponent._connect_parameters(self)
        if not self._allow_updates: return
        if not self.is_enabled(): return
        # here we know for sure that the track is valid!

        oTrack = self.get_track_or_return_or_none()
        if (oTrack == None): return
        sTrack = self.to_ascii(oTrack.name)
        if self.m_nLogLoadedDev == 1:
            self.log('>****************************************************************************************************')
            self.log('> track: %s' % (sTrack))

        # disconnect already connected midi controls
        self.disconnect_ctls(False)

        # prepare device registry
        self.m_nCurrBank  = 0 # BCR2000 preset index
        self.m_nCurrStrip = 0 # BCR2000 strip  index
        nCurrTrackIdxAbs  = self.curr_track_idx_abs()
        if (not nCurrTrackIdxAbs in self.m_hDevReg):
            self.m_hDevReg[nCurrTrackIdxAbs] = {}

        # connect the midi controls to the new device parameters
        aDevices = oTrack.devices
        for nDeviceIdx in range(len(aDevices)):
            oDevice = aDevices[nDeviceIdx]
            sClass  = self.to_ascii(oDevice.class_name)
            if (not sClass in self.m_hDevCfgs):
                self.dump_device(oDevice)
                continue

            # register device in device registry
            if (not sClass in self.m_hDevReg[nCurrTrackIdxAbs]):
                self.m_hDevReg[nCurrTrackIdxAbs][sClass] = {
                    'device'      : oDevice,
                    'track'       : sTrack,
                    'preset_index': 0,
                    'preset_saved': False,
                    'dev_params'  : {},
                    'panel_params': {},
                }
            hDevReg = self.m_hDevReg[nCurrTrackIdxAbs][sClass]

            sDevice  = self.to_ascii(oDevice.name)
            sDisplay = self.to_ascii(oDevice.class_display_name)
            if self.m_nLogLoadedDev == 1:
                self.log('> -----------------------------------------------------------------------------------')
                self.log('> LOADING => Class: "%s", Device: "%s", Display: "%s"' % (sClass, sDevice, sDisplay))

            # check if there are enough strips for this device,
            # otherwise start in the next bank!
            nStrips = self.m_hDevCfgs[sClass]['strips']
            if (self.m_nCurrStrip > (8 - nStrips)):
                self.m_nCurrStrip = 0
                self.m_nCurrBank += 1
                if (self.m_nCurrBank == self.m_nBanks):
                    self.log('> DONE Reconnecting midi controls to parameters, used banks: %d (MAX REACHED!)' % (self.m_nNumUsedBanks))
                    return # Maximum number of banks reached! we cannot map more controls!

            # connect midi controls to device parameters
            if 'drum_map' in self.m_hDevCfgs[sClass]:
                for oDrumPad in oDevice.drum_pads:
                    if len(oDrumPad.chains) == 0: continue
                    nNote  = oDrumPad.note
                    oChain = oDrumPad.chains[0] # check the first chain only
                    for oChainDev in oChain.devices:
                        if oChainDev.class_name != 'OriginalSimpler': continue
                        for oParam in oChainDev.parameters:
                            if oParam.name != 'Volume': continue
                            sParam = 'Volume_%d' % nNote
                            nBank  = nNote / 24
                            nStrip = nNote % 4 + ((nNote / 12) % 2) * 4
                            nRow   = 2 - ((nNote % 12) / 4)
                            #self.log('>>> %d %d %d - %s' % (nBank, nStrip, nRow, oChainDev.name))
                            oCtrl  = self.m_hMidiCtls[nBank][nStrip]['Main']['Rotary'][nRow]['control']
                            oCtrl.connect_to(oParam)
                            hDevReg['dev_params'][sParam] = {
                                'param'  : sParam,
                                'control': oCtrl,
                            }
                            self.m_nCurrBank = nBank
            else:
                bUseOrig = 'use_orig' in self.m_hDevCfgs[sClass]
                aParams  = oDevice.parameters
                for nParamIdx in range(len(aParams)):
                    oParam = aParams[nParamIdx]
                    if bUseOrig:
                        sParam = self.to_ascii(oParam.original_name)
                    else:
                        sParam = self.to_ascii(oParam.name)
                    oCtrl = self.get_control(sClass, sParam)
                    if (oCtrl == None): continue
                    oCtrl.connect_to(oParam)
                    hDevReg['dev_params'][sParam] = {
                        'param'  : oParam,
                        'control': oCtrl,
                    }

            # add main panel functions: preset save, preset prev, preset next
            self.add_panel_functions(sClass, hDevReg)
            # add extra device functions
            self.add_extra_functions(sClass, hDevReg)

            if self.m_nLogLoadedDev == 1:
                self.log('> Loaded "%s", bank: %d, first strip: %d' % (sClass, self.m_nCurrBank, self.m_nCurrStrip))

            # finished adding device, update offsets for the next device
            if 'banks' in self.m_hDevCfgs[sClass]:
                nBanks = self.m_hDevCfgs[sClass]['banks']
                self.m_nCurrBank     = self.m_nCurrBank + nBanks
                self.m_nNumUsedBanks = self.m_nCurrBank
                self.m_nCurrStrip    = 0
            else:
                self.m_nNumUsedBanks = self.m_nCurrBank + 1
                self.m_nCurrStrip += nStrips
                if (self.m_nCurrStrip >= 8):
                    self.m_nCurrBank += 1
                    self.m_nCurrStrip = 0

        self.log('> DONE Reconnecting midi controls to parameters, used banks: %d' % (self.m_nNumUsedBanks))

    def add_panel_functions(self, _sClass, _hDevReg):
        self.add_panel_function(_sClass, 'Preset Save', BUTTON_ON, _hDevReg)
        if (self.m_hDevCfgs[_sClass]['strips'] == 1): return # not possible to add the rest of the panel functions
        self.add_panel_function(_sClass, 'Preset Prev' , BUTTON_ON, _hDevReg)
        self.add_panel_function(_sClass, 'Preset Next'     , BUTTON_ON, _hDevReg)

    def add_panel_function(self, _sClass, _sParam, _nMsg, _hDevReg):
        oCtrl = self.get_control(_sClass, _sParam)
        if (oCtrl == None): return # unavailable control, nothing else to do
        oSlot = self.get_slot(_sClass, _sParam)
        oSlot.subject = oCtrl
        oCtrl.send_value(_nMsg, True) # update midi control
        _hDevReg['panel_params'][_sParam] = {
            'param'  : _nMsg, # used when syncing bank
            'control': oCtrl,
        }

    def add_extra_functions(self, _sClass, _hDevReg):
        if (not 'extra_functions' in self.m_hDevCfgs[_sClass]): return
        if (not 'extra_params' in _hDevReg):
            _hDevReg['extra_params'] = {}
        for sParam in self.m_hDevCfgs[_sClass]['extra_functions']:
            oCtrl = self.get_control(_sClass, sParam)
            if (oCtrl == None): continue
            oSlot = self.get_slot(_sClass, sParam)
            oSlot.subject = oCtrl
            _hDevReg['extra_params'][sParam] = {
                'param'  : 0.0, # default value
                'control': oCtrl,
            }
            #self.log('>> connected extra param "%s / %s"' % (_sClass, sParam))
            # Extra functions are normally reset functions which
            # reset some parameter of the device.
            # But there are other extra functions that actually
            # have a state, independent from the real device
            # parameter values, for example: Eq8's Center Freq & Q
            self.extra_control_config(oCtrl, _sClass, sParam, _hDevReg)

    def extra_control_config(self, _oCtrl, _sClass, _sParam, _hDevReg):
        hExtraParams = _hDevReg['extra_params']

        if (_sClass == 'Eq8' and _sParam == 'Q'):
            # intialize auto and extra parameters if necessary
            if (not 'auto_params' in _hDevReg):
                _hDevReg['auto_params'] = {
                    'on'   : False, 'type': None, 'delta': 0.0,
                    'start': 0.0  , 'vel' : 64,
                }
                hExtraParams['Center Freq']['param'] = 0.5 # used for bank sync
                hExtraParams['Q'          ]['param'] = 0.3 # used for bank sync

            # refresh the parameter and control references
            _hDevReg['auto_params']['param_refs'] = {
                'lo_param': {
                    'param'  : _hDevReg['dev_params']['1 Frequency A']['param'],
                    'control': _hDevReg['dev_params']['1 Frequency A']['control'],
                },
                'hi_param': {
                    'param'  : _hDevReg['dev_params']['2 Frequency A']['param'],
                    'control': _hDevReg['dev_params']['2 Frequency A']['control'],
                },
            }

            # update midi control values
            self.compute_eq8_frequencies()
            nFreq = hExtraParams['Center Freq']['param'] # 0.0 .. 1.0 # used for bank sync
            nQ    = hExtraParams['Q'          ]['param'] # 0.0 .. 1.0 # used for bank sync
            hExtraParams['Center Freq']['control'].send_value(int(nFreq * 127), True)
            hExtraParams['Q'          ]['control'].send_value(int(nQ    * 127), True)

        elif _sClass == 'OriginalSimpler':
            self.init_simpler_control(_sParam, hExtraParams, _oCtrl)

        else:
            _oCtrl.send_value(0, True)

    # returns an ALREADY CREATED control always
    # can only be used while connecting controls!
    # it useas m_nCurrBank and m_nCurrStrip!
    def get_control(self, _sClass, _sParam):
        hMidiCtl = self.get_control_hash(_sClass, _sParam)
        if hMidiCtl == None: return None
        return hMidiCtl['control']

    # returns a BRAND NEW slot always
    # can only be used while connecting controls!
    # it useas m_nCurrBank and m_nCurrStrip!
    def get_slot(self, _sClass, _sParam):
        hMidiCtl = self.get_control_hash(_sClass, _sParam)
        if hMidiCtl == None: return None
        sParam = _sParam.replace(' ', '_')
        oSlot  = self.register_slot(None, getattr(self, u'_%s_%s_value' % (_sClass, sParam)), u'value')
        hMidiCtl['slot'] = oSlot
        return oSlot

    def get_control_hash(self, _sClass, _sParam):
        hParamCfgs = self.m_hCfg['devices'][_sClass]['param_cfgs']
        if (not _sParam in hParamCfgs):
            if self.m_nLogNotMapped == 1:
                self.log('>>> "%s / %s" without mapping!' % (_sClass, _sParam))
            return None # parameter without mapped midi control
        sPanel, sType, nRowIdx, nStripIdx, nBankOff = hParamCfgs[_sParam]
        return self.m_hMidiCtls[self.m_nCurrBank + nBankOff][self.m_nCurrStrip + nStripIdx][sPanel][sType][nRowIdx]

    # Warp mode values:
    # 0 = Beats Mode
    # 1 = Tones Mode
    # 2 = Texture Mode
    # 3 = Re-Pitch Mode
    # 4 = Complex Mode
    # 6 = Complex Pro Mode

    # Beats Granulation Resolution
    # 0 = 1 Bar
    # 1 = 1/2
    # 2 = 1/4
    # 3 = 1/8
    # 4 = 1/16
    # 5 = 1/32
    # 6 = Transients

    # Beats Transient Loop Mode
    # 0 = off
    # 1 = forward
    # 2 = alternate
    def init_simpler_control(self, _sParam, _hExtraParams, _oCtrl):
        oDevice = self.get_device('OriginalSimpler')
        oSample = oDevice.sample

        aDevicePrm = ['Playback Mode', 'Retrigger', 'Voices']
        bUseDevice = (_sParam in aDevicePrm)

        nMidi = 0
        if oSample != None or bUseDevice:
            if _sParam == 'Playback Mode':
                nModeIdx = oDevice.playback_mode
                nMidi    = nModeIdx * 43
            elif _sParam == 'Retrigger':
                nMidi = oDevice.retrigger * 127
            elif _sParam == 'Voices':
                aVoices = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 24, 32]
                nMidi   = aVoices.index(oDevice.voices) * 9
            elif _sParam == 'Reverse':
                nMidi = BUTTON_ON
            elif _sParam == 'Crop':
                nMidi = BUTTON_ON
            elif _sParam == 'Warp As':
                nMidi = BUTTON_ON if oDevice.can_warp_as else BUTTON_OFF
            elif _sParam == 'Warp Double':
                nMidi = BUTTON_ON if oDevice.can_warp_double else BUTTON_OFF
            elif _sParam == 'Warp Half':
                nMidi = BUTTON_ON if oDevice.can_warp_half else BUTTON_OFF
            elif _sParam == 'Slicing Playback Mode':
                nMidi = oDevice.slicing_playback_mode * 43
            elif _sParam == 'Gain':
                nMidi = int(oSample.gain * 127.0)
            elif _sParam == 'Warp':
                nMidi = oSample.warping * BUTTON_ON
            elif _sParam == 'Warp Mode':
                nValue = oSample.warp_mode
                if nValue == 6: nValue = 5
                nMidi = nValue * 22
            elif _sParam == 'Start Marker Pos':
                nDiv  = float(oSample.length) / 127.0           # in samples
                nMidi = int(float(oSample.start_marker) / nDiv) # MIDI  value [0.0, ..., 127.0] int
            elif _sParam == 'Start Marker Res':
                nMidi  = 0 # use coarse resolution by default
            elif _sParam == 'End Marker Pos':
                nDiv  = float(oSample.length) / 127.0         # in samples
                nMidi = int(float(oSample.end_marker) / nDiv) # MIDI  value [0.0, ..., 127.0] int
            elif _sParam == 'End Marker Res':
                nMidi  = 0 # use coarse resolution by default
            elif _sParam == 'Beats Gran Res':
                nMidi = oSample.beats_granulation_resolution * 19
            elif _sParam == 'Beats Trans Loop Mode':
                nMidi = oSample.beats_transient_loop_mode * 43
            elif _sParam == 'Beats Trans Envelope':
                nMidi = int(float(oSample.beats_transient_envelope) / 100.0 * 127.0)
            elif _sParam == 'Tones Grain Size':
                nMidi = int((oSample.tones_grain_size - 12.0) / 88.0 * 127.0)
            elif _sParam == 'Texture Grain Size':
                nMidi = int((oSample.texture_grain_size - 2.0) / 261.0 * 127.0)
            elif _sParam == 'Texture Flux':
                nMidi = int(float(oSample.texture_flux) / 100.0 * 127.0)
            elif _sParam == 'Complex Pro Formants':
                nMidi = int(float(oSample.complex_pro_formants) / 100.0 * 127.0)
            elif _sParam == 'Complex Pro Envelope':
                nMidi = int((oSample.complex_pro_envelope - 8.0) / 248.0 * 127.0)
            elif _sParam == 'Slicing Style':
                nMidi = oSample.slicing_style * 32
            elif _sParam == 'Slicing Sensitivity':
                nMidi = int(oSample.slicing_sensitivity * 127.0)
            elif _sParam == 'Slicing Beat Division':
                nMidi = oSample.slicing_beat_division * 12
            elif _sParam == 'Slicing Region Count':
                nMidi = int((oSample.slicing_region_count - 2.0) / 62.0 * 127.0)
            elif _sParam == 'Clear Slices':
                nMidi = BUTTON_ON

        _oCtrl.send_value(nMidi, True)
        _hExtraParams[_sParam]['param'] = float(nMidi) / 127.0 # used for bank sync

    # ****************************************************************

    def dump_device(self, _oDevice):
        sClass   = self.to_ascii(_oDevice.class_name)
        sDevice  = self.to_ascii(_oDevice.name)
        sDisplay = self.to_ascii(_oDevice.class_display_name)
        self.log('------------------------------------------------------------------------')
        self.log('> Class: %s, Device: %s, Display: %s' % (sClass, sDevice, sDisplay))

        aParams  = _oDevice.parameters
        for nParamIdx in range(len(aParams)):
            oParam    = aParams[nParamIdx]
            sParam    = self.to_ascii(oParam.name)
            sOriginal = self.to_ascii(oParam.original_name)
            if (oParam.is_quantized):
                aValues = []
                for oValue in oParam.value_items:
                    aValues.append(str(oValue))
                self.log('> Q param: "%s", orig: "%s" => [%s]' % (sParam, sOriginal, ', '.join(aValues)))
            else:
                lLog = (sParam, sOriginal, oParam.value, oParam.min, oParam.max)
                self.log('>   param: "%s", orig: "%s", value: %f, min: %f, max: %f' % lLog)

    # SYNC TASKS ***************************************************************

    def update_sync_tasks(self):
        if (self.m_bBusy == True): return # busy updating delta

        for nTrackIdxAbs in self.m_hDevReg:
            hDevices = self.m_hDevReg[nTrackIdxAbs]
            for sDevice in hDevices:
                hDevReg = hDevices[sDevice]
                if (not 'auto_params' in hDevReg): continue
                if (not hDevReg['auto_params']['on']): continue
                if (sDevice == 'Eq8'):
                    self.update_eq8_sync_tasks(hDevReg)

    def update_eq8_sync_tasks(self, _hDevReg):
        hAutoParams = _hDevReg['auto_params']
        sType  = hAutoParams['type']
        nDelta = hAutoParams['delta']
        oLoPrm = hAutoParams['param_refs']['lo_param']['param']
        oHiPrm = hAutoParams['param_refs']['hi_param']['param']
        nLoFrq = oLoPrm.value
        nHiFrq = oHiPrm.value

        if (sType == 'lo_inc'):
            nNewVal = nLoFrq + nDelta
            if (nNewVal >= nHiFrq):
                hAutoParams['on'] = False
                nNewVal = nHiFrq
                sCmd    = 'LOW INC'
            oLoPrm.value = nNewVal
        elif (sType == 'lo_dec'):
            nNewVal = nLoFrq + nDelta
            if (nNewVal <= 0.0):
                hAutoParams['on'] = False
                nNewVal = 0.0
                sCmd    = 'LOW DEC'
            oLoPrm.value = nNewVal
        elif (sType == 'hi_dec'):
            nNewVal = nHiFrq + nDelta
            if (nNewVal <= nLoFrq):
                hAutoParams['on'] = False
                nNewVal = nLoFrq
                sCmd    = 'HIGH DEC'
            oHiPrm.value = nNewVal
        elif (sType == 'hi_inc'):
            nNewVal = nHiFrq + nDelta
            if (nNewVal >= 1.0):
                hAutoParams['on'] = False
                nNewVal = 1.0
                sCmd    = 'HIGH INC'
            oHiPrm.value = nNewVal
        elif (sType == 'q_dec'):
            nNewVal1 = nLoFrq + nDelta
            nNewVal2 = nHiFrq - nDelta
            if (nNewVal1 >= nNewVal2):
                hAutoParams['on'] = False
                nNewVal1 = nNewVal2
                sCmd     = 'Q DEC'
            oLoPrm.value = nNewVal1
            oHiPrm.value = nNewVal2
        elif (sType == 'q_inc'):
            nNewVal1 = nLoFrq - nDelta
            nNewVal2 = nHiFrq + nDelta
            if (nNewVal1 < 0.0): nNewVal1 = 0.0
            if (nNewVal2 > 1.0): nNewVal2 = 1.0
            if (nNewVal1 == 0.0 and nNewVal2 == 1.0):
                hAutoParams['on'] = False
                sCmd = 'Q INC'
            oLoPrm.value = nNewVal1
            oHiPrm.value = nNewVal2

        if (not hAutoParams['on']):
            nTimeSpan  = time.time() - hAutoParams['start']
            sTrackName = _hDevReg['track']
            self.alert('track "%s", Eq8: Auto %s done in %f [sec]' % (sTrackName, sCmd, nTimeSpan))

    # LISTENERS ****************************************************************

    def send_bank_values(self, _nBankIdx): # index is 0-based
        if (_nBankIdx >= self.m_nNumUsedBanks):
            Live.Base.log('> bank %d not used!' % (_nBankIdx + 1))
            return

        hBank = self.m_hMidiCtls[_nBankIdx]
        for nStripIdx in range (self.m_nStrips):
            hStrip = hBank[nStripIdx]
            for sPanel in ('Main', 'Group'):
                hPanel = hStrip[sPanel]
                for sType in ('Button', 'Rotary'):
                    hType = hPanel[sType]
                    for nCtlIdx in hType.keys():
                        oControl = hType[nCtlIdx]['control']
                        oParam   = oControl.mapped_parameter()
                        if oParam != None:
                            oControl._request_rebuild()
                        else:
                            oControl.send_value(0, True)

        nCurrTrackIdxAbs = self.curr_track_idx_abs()
        for sDevice in self.m_hDevReg[nCurrTrackIdxAbs]:
            hDevReg = self.m_hDevReg[nCurrTrackIdxAbs][sDevice]
            for sParam in hDevReg['panel_params']:
                hPanelParam = hDevReg['panel_params'][sParam]
                hPanelParam['control'].send_value(hPanelParam['param'], True)
            if ('extra_params' in hDevReg):
                for sParam in hDevReg['extra_params']:
                    hExtraParam = hDevReg['extra_params'][sParam]
                    hExtraParam['control'].send_value(int(hExtraParam['param'] * 127), True)
        #Live.Base.log('> sync bank %d!' % (_nBankIdx + 1))

    # ****************************************************************

    def _Vocoder_Preset_Save_value(self, _nValue):
        self.preset_save('Vocoder')

    def _Vocoder_Preset_Prev_value(self, _nValue):
        self.preset_prev('Vocoder')

    def _Vocoder_Preset_Next_value(self, _nValue):
        self.preset_next('Vocoder', _nValue)

    def _Overdrive_Preset_Save_value(self, _nValue):
        self.preset_save('Overdrive')

    def _Overdrive_Preset_Prev_value(self, _nValue):
        self.preset_prev('Overdrive')

    def _Overdrive_Preset_Next_value(self, _nValue):
        self.preset_next('Overdrive', _nValue)

    def _BeatRepeat_Preset_Save_value(self, _nValue):
        self.preset_save('BeatRepeat')

    def _BeatRepeat_Preset_Prev_value(self, _nValue):
        self.preset_prev('BeatRepeat')

    def _BeatRepeat_Preset_Next_value(self, _nValue):
        self.preset_next('BeatRepeat', _nValue)

    def _Compressor2_Preset_Save_value(self, _nValue):
        self.preset_save('Compressor2')

    def _Compressor2_Preset_Prev_value(self, _nValue):
        self.preset_prev('Compressor2')

    def _Compressor2_Preset_Next_value(self, _nValue):
        self.preset_next('Compressor2', _nValue)

    # *****************************************************************

    def _Resonator_Preset_Save_value(self, _nValue):
        self.preset_save('Resonator')

    def _Resonator_Preset_Prev_value(self, _nValue):
        self.preset_prev('Resonator')

    def _Resonator_Preset_Next_value(self, _nValue):
        self.preset_next('Resonator', _nValue)

    def _AutoPan_Preset_Save_value(self, _nValue):
        self.preset_save('AutoPan')

    def _AutoPan_Preset_Prev_value(self, _nValue):
        self.preset_prev('AutoPan')

    def _AutoPan_Preset_Next_value(self, _nValue):
        self.preset_next('AutoPan', _nValue)

    # *****************************************************************

    def _Echo_Preset_Save_value(self, _nValue):
        self.preset_save('Echo')

    def _Echo_Preset_Prev_value(self, _nValue):
        self.preset_prev('Echo')

    def _Echo_Preset_Next_value(self, _nValue):
        self.preset_next('Echo', _nValue)

    def _Delay_Preset_Save_value(self, _nValue):
        self.preset_save('Delay')

    def _Delay_Preset_Prev_value(self, _nValue):
        self.preset_prev('Delay')

    def _Delay_Preset_Next_value(self, _nValue):
        self.preset_next('Delay', _nValue)

    # *****************************************************************

    def _FilterDelay_Preset_Save_value(self, _nValue):
        self.preset_save('FilterDelay')

    def _FilterDelay_Preset_Prev_value(self, _nValue):
        self.preset_prev('FilterDelay')

    def _FilterDelay_Preset_Next_value(self, _nValue):
        self.preset_next('FilterDelay', _nValue)

    def _GrainDelay_Preset_Save_value(self, _nValue):
        self.preset_save('GrainDelay')

    def _GrainDelay_Preset_Prev_value(self, _nValue):
        self.preset_prev('GrainDelay')

    def _GrainDelay_Preset_Next_value(self, _nValue):
        self.preset_next('GrainDelay', _nValue)

    def _Chorus_Preset_Save_value(self, _nValue):
        self.preset_save('Chorus')

    def _Chorus_Preset_Prev_value(self, _nValue):
        self.preset_prev('Chorus')

    def _Chorus_Preset_Next_value(self, _nValue):
        self.preset_next('Chorus', _nValue)

    # *****************************************************************

    def _Flanger_Preset_Save_value(self, _nValue):
        self.preset_save('Flanger')

    def _Flanger_Preset_Prev_value(self, _nValue):
        self.preset_prev('Flanger')

    def _Flanger_Preset_Next_value(self, _nValue):
        self.preset_next('Flanger', _nValue)

    def _Phaser_Preset_Save_value(self, _nValue):
        self.preset_save('Phaser')

    def _Phaser_Preset_Prev_value(self, _nValue):
        self.preset_prev('Phaser')

    def _Phaser_Preset_Next_value(self, _nValue):
        self.preset_next('Phaser', _nValue)

    def _FrequencyShifter_Preset_Save_value(self, _nValue):
        self.preset_save('FrequencyShifter')

    def _FrequencyShifter_Preset_Prev_value(self, _nValue):
        self.preset_prev('FrequencyShifter')

    def _FrequencyShifter_Preset_Next_value(self, _nValue):
        self.preset_next('FrequencyShifter', _nValue)

    # *****************************************************************

    def _Reverb_Preset_Save_value(self, _nValue):
        self.preset_save('Reverb')

    def _Reverb_Preset_Prev_value(self, _nValue):
        self.preset_prev('Reverb')

    def _Reverb_Preset_Next_value(self, _nValue):
        self.preset_next('Reverb', _nValue)

    def _Eq8_Preset_Save_value(self, _nValue):
        self.preset_save('Eq8')

    def _Eq8_Preset_Prev_value(self, _nValue):
        self.preset_prev('Eq8')

    def _Eq8_Preset_Next_value(self, _nValue):
        self.preset_next('Eq8', _nValue)

    def _FilterEQ3_Preset_Save_value(self, _nValue):
        self.preset_save('FilterEQ3')

    def _FilterEQ3_Preset_Prev_value(self, _nValue):
        self.preset_prev('FilterEQ3')

    def _FilterEQ3_Preset_Next_value(self, _nValue):
        self.preset_next('FilterEQ3', _nValue)

    def _Redux_Preset_Save_value(self, _nValue):
        self.preset_save('Redux')

    def _Redux_Preset_Prev_value(self, _nValue):
        self.preset_prev('Redux')

    def _Redux_Preset_Next_value(self, _nValue):
        self.preset_next('Redux', _nValue)

    # *****************************************************************

    def _DrumGroupDevice_Preset_Save_value(self, _nValue):
        self.preset_save('DrumGroupDevice')

    def _DrumGroupDevice_Preset_Prev_value(self, _nValue):
        self.preset_prev('DrumGroupDevice')

    def _DrumGroupDevice_Preset_Next_value(self, _nValue):
        self.preset_next('DrumGroupDevice', _nValue)

    def _InstrumentGroupDevice_Preset_Save_value(self, _nValue):
        self.preset_save('InstrumentGroupDevice')

    def _InstrumentGroupDevice_Preset_Prev_value(self, _nValue):
        self.preset_prev('InstrumentGroupDevice')

    def _InstrumentGroupDevice_Preset_Next_value(self, _nValue):
        self.preset_next('InstrumentGroupDevice', _nValue)

    def _UltraAnalog_Preset_Save_value(self, _nValue):
        self.preset_save('UltraAnalog')

    def _UltraAnalog_Preset_Prev_value(self, _nValue):
        self.preset_prev('UltraAnalog')

    def _UltraAnalog_Preset_Next_value(self, _nValue):
        self.preset_next('UltraAnalog', _nValue)

    def _Collision_Preset_Save_value(self, _nValue):
        self.preset_save('Collision')

    def _Collision_Preset_Prev_value(self, _nValue):
        self.preset_prev('Collision')

    def _Collision_Preset_Next_value(self, _nValue):
        self.preset_next('Collision', _nValue)

    def _LoungeLizard_Preset_Save_value(self, _nValue):
        self.preset_save('LoungeLizard')

    def _LoungeLizard_Preset_Prev_value(self, _nValue):
        self.preset_prev('LoungeLizard')

    def _LoungeLizard_Preset_Next_value(self, _nValue):
        self.preset_next('LoungeLizard', _nValue)

    def _Operator_Preset_Save_value(self, _nValue):
        self.preset_save('Operator')

    def _Operator_Preset_Prev_value(self, _nValue):
        self.preset_prev('Operator')

    def _Operator_Preset_Next_value(self, _nValue):
        self.preset_next('Operator', _nValue)

    def _MultiSampler_Preset_Save_value(self, _nValue):
        self.preset_save('MultiSampler')

    def _MultiSampler_Preset_Prev_value(self, _nValue):
        self.preset_prev('MultiSampler')

    def _MultiSampler_Preset_Next_value(self, _nValue):
        self.preset_next('MultiSampler', _nValue)

    def _OriginalSimpler_Preset_Save_value(self, _nValue):
        self.preset_save('OriginalSimpler')

    def _OriginalSimpler_Preset_Prev_value(self, _nValue):
        self.preset_prev('OriginalSimpler')

    def _OriginalSimpler_Preset_Next_value(self, _nValue):
        self.preset_next('OriginalSimpler', _nValue)

    def _StringStudio_Preset_Save_value(self, _nValue):
        self.preset_save('StringStudio')

    def _StringStudio_Preset_Prev_value(self, _nValue):
        self.preset_prev('StringStudio')

    def _StringStudio_Preset_Next_value(self, _nValue):
        self.preset_next('StringStudio', _nValue)

    def _InstrumentVector_Preset_Save_value(self, _nValue):
        self.preset_save('InstrumentVector')

    def _InstrumentVector_Preset_Prev_value(self, _nValue):
        self.preset_prev('InstrumentVector')

    def _InstrumentVector_Preset_Next_value(self, _nValue):
        self.preset_next('InstrumentVector', _nValue)

    # *****************************************************************

    def _AudioEffectGroupDevice_Preset_Save_value(self, _nValue):
        self.preset_save('AudioEffectGroupDevice')

    def _AudioEffectGroupDevice_Preset_Prev_value(self, _nValue):
        self.preset_prev('AudioEffectGroupDevice')

    def _AudioEffectGroupDevice_Preset_Next_value(self, _nValue):
        self.preset_next('AudioEffectGroupDevice', _nValue)

    # *****************************************************************

    def preset_save(self, _sClass):
        hPanelParams = self.get_panel_params(_sClass)
        oCtrl = hPanelParams['Preset Save']['control']
        oCtrl.send_value(127, True) # turn on button again

        # build the name of the preset
        sTime   = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
        oDevice = self.get_device(_sClass)
        sDevice = self.to_ascii(oDevice.name)
        sName   = '%s_%s' % (sTime, sDevice)
        self.alert('> STORING "%s"' % (sName))

        # open the presets file and load the line-up
        hDevParams  = self.get_dev_params(_sClass)
        sHome       = os.getenv('HOME')
        sFilePath   = '%s/%s/%s/%s_presets.txt' % (sHome, self.m_hCfg['sProductDir'], self.m_hCfg['sDevicesDir'], _sClass)
        bFileExists = os.path.isfile(sFilePath)
        if not bFileExists:
            oFile   = open(sFilePath, 'w')
            aLineup = hDevParams.keys()
            aLineup.remove('Device On')
            aLineup.sort()
            sLineup = '|'.join(aLineup)
            oFile.write('@params:%s\n' % (sLineup))
            self.m_hCfg['devices'][_sClass]['lineup'] = aLineup
        else:
            oFile   = open(sFilePath, 'a')
            aLineup = self.m_hCfg['devices'][_sClass]['lineup']

        # write the values in the presets file
        aActValues = [sName] # actual values, preset name is the first item
        aStrValues = []      # string values
        for sParam in aLineup:
            oValue = hDevParams[sParam]['param'].value
            aActValues.append(oValue)
            aStrValues.append(str(oValue))
        sStrValues = '|'.join(aStrValues)
        oFile.write('%s:%s\n' % (sName, sStrValues))
        oFile.close()

        # add the current values to the list of presets
        aPresets = self.m_hCfg['devices'][_sClass]['preset_cfgs']
        aPresets.append(aActValues)

        # set a flag to indicate that a preset has just been saved
        # and it will recover next time a preset scroll button is presed
        hDevReg  = self.get_dev_reg(_sClass)
        hDevReg['preset_saved'] = True

    def preset_prev(self, _sClass):
        self.load_preset(_sClass, True)

    def preset_next(self, _sClass, _nValue):
        self.load_preset(_sClass, False)

    def load_preset(self, _sClass, _bPrev):
        hPanelParams = self.get_panel_params(_sClass)
        if _bPrev:
            oCtl = hPanelParams['Preset Prev']['control']
        else:
            oCtl = hPanelParams['Preset Next']['control']
        oCtl.send_value(127, True) # toggle on again immediately

        aPresets = self.m_hCfg['devices'][_sClass]['preset_cfgs'] # read from a presets config file
        if (len(aPresets) == 0):
            self.alert('NO PRESETS LOADED!')
            return # no presets available! nothing else to do here!

        # find out the preset index to load
        hDevReg = self.get_dev_reg(_sClass)
        nMaxPresIdx = len(aPresets) - 1
        if hDevReg['preset_saved']:
            #self.log('>> using saved, num presets: %d' % (len(aPresets)))
            nPresetIdx = nMaxPresIdx  # use the latest saved preset
            hDevReg['preset_saved'] = False # reset the flag
        else:
            nPresetIdx = hDevReg['preset_index']
            if (_bPrev):
                nPresetIdx = nPresetIdx - 1 if nPresetIdx > 0 else nMaxPresIdx
            else:
                nPresetIdx = nPresetIdx + 1 if nPresetIdx < nMaxPresIdx else 0
        hDevReg['preset_index'] = nPresetIdx

        #self.log('>> using preset: %d' % (nPresetIdx))
        aLineup = self.m_hCfg['devices'][_sClass]['lineup'] # read from a presets config file
        aPreset = aPresets[nPresetIdx]
        sPreset = aPreset[0] # the name of the preset is the first item

        # apply the preset values to the parameters
        #self.log('>> appling preset %s in class "%s"' % (sPreset, _sClass))
        hDevParams = hDevReg['dev_params']
        for nIdx in range(len(aLineup)):
            sParam = aLineup[nIdx]
            try:
                hDevParams[sParam]['param'].value = aPreset[nIdx + 1]
            except Exception as e:
                self.log(">! Preset '%s' could not update param [%d] '%s' with value %s: %s" % (sPreset, nIdx, sParam, str(aPreset[nIdx]), str(e)))
                self.log(">! min: %s, max: %s" % (str(hDevParams[sParam]['param'].min), str(hDevParams[sParam]['param'].max)))
        self.alert('> LOADED PRESET [%d] "%s"' % (nPresetIdx, sPreset))

    # ****************************************************************

    def _BeatRepeat_Pitch_Reset_value(self, _nValue):
        self.get_dev_params('BeatRepeat')['Pitch']['param'].value = 0.0

    def _BeatRepeat_PDecay_Reset_value(self, _nValue):
        self.get_dev_params('BeatRepeat')['Pitch Decay']['param'].value = 0.0

    def _BeatRepeat_Volume_Reset_value(self, _nValue):
        self.get_dev_params('BeatRepeat')['Volume']['param'].value = 0.85

    def _BeatRepeat_Decay_Reset_value(self, _nValue):
        self.get_dev_params('BeatRepeat')['Decay']['param'].value = 0.0

    def _AudioEffectGroupDevice_Fade_Out_value(self, _nValue):
        self.get_dev_params('AudioEffectGroupDevice')['Effect']['param'].value = 127.0

    def _Eq8_Center_Freq_value(self, _nValue):
        hEq8ExtraParams = self.get_extra_params('Eq8')
        hEq8ExtraParams['Center Freq']['param'] = float(_nValue) / 127.0 # 0.0 .. 1.0
        self.compute_eq8_frequencies()

    def _Eq8_Q_value(self, _nValue):
        hEq8ExtraParams = self.get_extra_params('Eq8')
        hEq8ExtraParams['Q']['param'] = float(_nValue) / 127.0 # 0.0 .. 1.0
        self.compute_eq8_frequencies()

    def compute_eq8_frequencies(self):
        hEq8ExtraParams = self.get_extra_params('Eq8')
        nFreq = hEq8ExtraParams['Center Freq']['param'] # 0.0 .. 1.0
        nQ    = hEq8ExtraParams['Q'          ]['param'] # 0.0 .. 1.0
        nFreqLo = nFreq - nQ
        nFreqHi = nFreq + nQ
        nFreqLo = 0.0 if nFreqLo < 0.0 else nFreqLo
        nFreqHi = 1.0 if nFreqHi > 1.0 else nFreqHi
        hEq8AutoParams = self.get_auto_params('Eq8')
        hEq8AutoParams['param_refs']['lo_param']['param'].value = nFreqLo # update low  freq parameter value
        hEq8AutoParams['param_refs']['hi_param']['param'].value = nFreqHi # update high freq parameter value

    def _Eq8_Auto_Time_value(self, _nValue):
        hEq8AutoParams = self.get_auto_params('Eq8')
        hEq8AutoParams['vel'] = _nValue # 0 .. 127 bars
        self.alert('> EQ8 AUTO-VEL: %d [bars]' % (_nValue))
        self.compute_eq8_auto_delta(hEq8AutoParams);

    def _Eq8_1_Auto_Inc_value(self, _nValue):
        self.handle_Eq8_auto_cmd('lo_inc')

    def _Eq8_1_Auto_Dec_value(self, _nValue):
        self.handle_Eq8_auto_cmd('lo_dec')

    def _Eq8_2_Auto_Dec_value(self, _nValue):
        self.handle_Eq8_auto_cmd('hi_dec')

    def _Eq8_2_Auto_Inc_value(self, _nValue):
        self.handle_Eq8_auto_cmd('hi_inc')

    def _Eq8_Auto_Q_Dec_value(self, _nValue):
        self.handle_Eq8_auto_cmd('q_dec')

    def _Eq8_Auto_Q_Inc_value(self, _nValue):
        self.handle_Eq8_auto_cmd('q_inc')

    def handle_Eq8_auto_cmd(self, _sCmd):
        hDevReg        = self.get_dev_reg('Eq8')
        hEq8AutoParams = self.get_auto_params('Eq8')
        if (hEq8AutoParams['on']):
            hEq8AutoParams['on'] = False
            self.alert('> Track: "%s", STOP AUTO' % (hDevReg['track']))
        else:
            hEq8AutoParams['type']  = _sCmd
            hEq8AutoParams['start'] = time.time()
            hEq8AutoParams['on']    = True
            self.compute_eq8_auto_delta(hEq8AutoParams);

    def compute_eq8_auto_delta(self, _hEq8AutoParams):
        if (not _hEq8AutoParams['on']): return # not auto-updating! nothing else to do here!

        self.m_bBusy = True

        sType  = _hEq8AutoParams['type']
        nStart = _hEq8AutoParams['start']
        nVel   = _hEq8AutoParams['vel']
        nVel   = 0.5 if (nVel == 0) else nVel

        nTempo    = self.m_oSong.tempo    # in BMP
        nBarSpan  = (60.0 / nTempo) * 4.0 # in seconds
        nTimeSpan = nVel * nBarSpan       # in seconds

        if (sType == 'lo_inc'):
            nCur = _hEq8AutoParams['param_refs']['lo_param']['param'].value
            nTgt = _hEq8AutoParams['param_refs']['hi_param']['param'].value
            sCmd = 'LOW FREQ INCR'
        elif (sType == 'lo_dec'):
            nCur = _hEq8AutoParams['param_refs']['lo_param']['param'].value
            nTgt = 0.0
            sCmd = 'LOW FREQ DECR'
        elif (sType == 'hi_dec'):
            nCur = _hEq8AutoParams['param_refs']['hi_param']['param'].value
            nTgt = _hEq8AutoParams['param_refs']['lo_param']['param'].value
            sCmd = 'HIGH FREQ DECR'
        elif (sType == 'hi_inc'):
            nCur = _hEq8AutoParams['param_refs']['hi_param'].value
            nTgt = 1.0
            sCmd = 'HIGH FREQ INCR'
        elif (sType == 'q_dec'):
            nExtraPrm = self.get_extra_params('Eq8')
            nCur = nExtraPrm['Q']['param']
            nTgt = 0.0
            sCmd = 'Q DECR'
        elif (sType == 'q_inc'):
            nExtraPrm = self.get_extra_params('Eq8')
            nCur = nExtraPrm['Q']['param']
            nTgt = 1.0
            sCmd = 'Q INCR'

        nDelta = ((nTgt - nCur) / nTimeSpan) / 10.0 # divide with 10.0 since update executes every 100 ms
        _hEq8AutoParams['delta'] = nDelta
        self.alert('> AUTO %s (%f -> %f) in %f [s] => %f [bars]' % (sCmd, nCur, nTgt, nTimeSpan, nVel))

        self.m_bBusy = False

    def _OriginalSimpler_Playback_Mode_value(self, _nValue):
        self._on_simpler_param_value('Playback Mode', _nValue, True)

    def _OriginalSimpler_Retrigger_value(self, _nValue):
        self._on_simpler_param_value('Retrigger', _nValue, True)

    def _OriginalSimpler_Voices_value(self, _nValue):
        self._on_simpler_param_value('Voices', _nValue, True)

    def _OriginalSimpler_Reverse_value(self, _nValue):
        self._on_simpler_param_value('Reverse', _nValue)

    def _OriginalSimpler_Crop_value(self, _nValue):
        self._on_simpler_param_value('Crop', _nValue)

    def _OriginalSimpler_Warp_As_value(self, _nValue):
        self._on_simpler_param_value('Warp As', _nValue)

    def _OriginalSimpler_Warp_Double_value(self, _nValue):
        self._on_simpler_param_value('Warp Double', _nValue)

    def _OriginalSimpler_Warp_Half_value(self, _nValue):
        self._on_simpler_param_value('Warp Half', _nValue)

    def _OriginalSimpler_Slicing_Playback_Mode_value(self, _nValue):
        self._on_simpler_param_value('Slicing Playback Mode', _nValue)

    def _OriginalSimpler_Gain_value(self, _nValue):
        self._on_simpler_param_value('Gain', _nValue)

    def _OriginalSimpler_Warp_value(self, _nValue):
        self._on_simpler_param_value('Warp', _nValue)

    def _OriginalSimpler_Warp_Mode_value(self, _nValue):
        self._on_simpler_param_value('Warp Mode', _nValue)

    def _OriginalSimpler_Start_Marker_Pos_value(self, _nValue):
        self._on_marker_pos_value('Start Marker', _nValue)

    def _OriginalSimpler_Start_Marker_Res_value(self, _nValue):
        self._on_marker_res_value('Start Marker', _nValue)

    def _OriginalSimpler_End_Marker_Pos_value(self, _nValue):
        self._on_marker_pos_value('End Marker', _nValue)

    def _OriginalSimpler_End_Marker_Res_value(self, _nValue):
        self._on_marker_res_value('End Marker', _nValue)

    def _OriginalSimpler_Beats_Gran_Res_value(self, _nValue):
        self._on_simpler_param_value('Beats Gran Res', _nValue)

    def _OriginalSimpler_Beats_Trans_Loop_Mode_value(self, _nValue):
        self._on_simpler_param_value('Beats Trans Loop Mode', _nValue)

    def _OriginalSimpler_Beats_Trans_Envelope_value(self, _nValue):
        self._on_simpler_param_value('Beats Trans Envelope', _nValue)

    def _OriginalSimpler_Tones_Grain_Size_value(self, _nValue):
        self._on_simpler_param_value('Tones Grain Size', _nValue)

    def _OriginalSimpler_Texture_Grain_Size_value(self, _nValue):
        self._on_simpler_param_value('Texture Grain Size', _nValue)

    def _OriginalSimpler_Texture_Flux_value(self, _nValue):
        self._on_simpler_param_value('Texture Flux', _nValue)

    def _OriginalSimpler_Complex_Pro_Formants_value(self, _nValue):
        self._on_simpler_param_value('Complex Pro Formants', _nValue)

    def _OriginalSimpler_Complex_Pro_Envelope_value(self, _nValue):
        self._on_simpler_param_value('Complex Pro Envelope', _nValue)

    def _OriginalSimpler_Clear_Slices_value(self, _nValue):
        self._on_simpler_param_value('Clear Slices', _nValue)

    def _OriginalSimpler_Slicing_Style_value(self, _nValue):
        self._on_simpler_param_value('Slicing Style', _nValue)

    def _OriginalSimpler_Slicing_Sensitivity_value(self, _nValue):
        self._on_simpler_param_value('Slicing Sensitivity', _nValue)

    def _OriginalSimpler_Slicing_Beat_Division_value(self, _nValue):
        self._on_simpler_param_value('Slicing Beat Division', _nValue)

    def _OriginalSimpler_Slicing_Region_Count_value(self, _nValue):
        self._on_simpler_param_value('Slicing Region Count', _nValue)

    def _on_marker_pos_value(self, _sType, _nValue):
        oDevice = self.get_device('OriginalSimpler')
        oSample = oDevice.sample
        if oSample == None: return

        sPosParam    = '%s Pos' % (_sType)
        sResParam    = '%s Res' % (_sType)
        hExtraParams = self.get_extra_params('OriginalSimpler')
        nSelRes      = int(hExtraParams[sResParam]['param'] * 3.0) # int (0, 1, 2)

        nSpan  = oSample.length
        nDiv0  = float(nSpan) / 127.0   # in samples (float)
        nParam = float(_nValue) / 127.0 # param value [0.0, ..., 1.0) float]

        if nSelRes == 0:
            nPos = int(_nValue * nDiv0) # in samples
            hExtraParams[sPosParam]['pos']   = nPos
            hExtraParams[sPosParam]['param'] = nParam
        elif nSelRes == 1:
            nDiv1 = nDiv0 / 64.0 # in samples (float)
            nOffs = float(_nValue - 64) * nDiv1 # in samples (float) [-X , ..., +X)
            nPos  = int(hExtraParams[sPosParam]['pos'] + nOffs)
        elif nSelRes == 2:
            nDiv1 = (nDiv0 / 64.0) / 64.0 # in samples (float)
            if nDiv1 < 1.0: nDiv1 = 1.0
            nOffs = float(_nValue - 64) * nDiv1 # in samples (float) [-X , ..., +X)
            nPos  = int(hExtraParams[sPosParam]['pos'] + nOffs)

        if _sType == 'Start Marker':
            nEnd = oSample.end_marker
            if (nPos >= 0 and nPos < nEnd):
                oSample.start_marker = nPos
                self.alert('START MARKER: %d' % (nPos))
                return
        else:
            nStart = oSample.start_marker
            if (nPos > nStart and nPos <= nSpan):
                oSample.end_marker = nPos
                self.alert('END MARKER: %d' % (nPos))
                return

        self.alert('%s OUT OF RANGE' % (_sType.upper()))

    def _on_marker_res_value(self, _sType, _nValue):
        oDevice = self.get_device('OriginalSimpler')
        oSample = oDevice.sample
        if oSample == None: return

        nValue       = _nValue / 43 # value between 0 and 3 (int)
        sPosParam    = '%s Pos' % (_sType)
        sResParam    = '%s Res' % (_sType)
        hExtraParams = self.get_extra_params('OriginalSimpler')
        hExtraParams[sResParam]['param'] = float(nValue) / 3.0 # float: [0.0, 0.33, 0.66]

        aResName = ['COARSE', 'MEDIUM', 'FINE']
        self.alert('%s RESOLUTION: %s' % (_sType.upper(), aResName[nValue]))

        nPos = oSample.start_marker if _sType == 'Start Marker' else oSample.end_marker
        if nValue == 0:
            nSpan  = oSample.length
            nDiv   = float(nSpan) / 127.0 # in samples
            nMul   = float(nPos) / nDiv   # MIDI  value [0.0, ..., 127.0] int
            nParam = nMul / 127.0         # param value [0.0, ...,   1.0) float
            nMidi  = int(nParam * 127.0)  # MIDI  value [  0, ...,   127] int
        elif nValue == 1:
            hExtraParams[sPosParam]['pos'] = nPos
            nMidi  = 64
            nParam = 0.5
        elif nValue == 2:
            nMidi  = 64
            nParam = 0.5

        hExtraParams[sPosParam]['control'].send_value(nMidi, True)
        hExtraParams[sPosParam]['param'] = nParam

    def _on_simpler_param_value(self, _sParam, _nValue, _bUseDevice = False):
        oDevice = self.get_device('OriginalSimpler')
        oSample = oDevice.sample

        nParam = float(_nValue) / 127.0
        if oSample != None or _bUseDevice:
            hExtraParams = self.get_extra_params('OriginalSimpler')
            oCtrl        = hExtraParams[_sParam]['control']
            if _sParam == 'Playback Mode':
                oDevice.playback_mode = _nValue / 43
            elif _sParam == 'Retrigger':
                oDevice.retrigger = (_nValue == BUTTON_ON)
            elif _sParam == 'Voices':
                aVoices = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 24, 32]
                oDevice.voices = aVoices[_nValue / 9]
            elif _sParam == 'Reverse':
                oDevice.reverse()
                oCtrl.send_value(BUTTON_ON, True)
            elif _sParam == 'Crop':
                oDevice.crop()
                hExtraParams['Start Marker Pos']['control'].send_value(0, True)
                hExtraParams['Start Marker Pos']['param'] = 0.0
                hExtraParams['End Marker Pos']['control'].send_value(127, True)
                hExtraParams['End Marker Pos']['param'] = 1.0
                oCtrl.send_value(BUTTON_ON, True)
            elif _sParam == 'Warp As':
                if oDevice.can_warp_as: oDevice.warp_as(oDevice.guess_playback_length())
                oCtrl.send_value(BUTTON_ON * oDevice.can_warp_as, True)
                hExtraParams['Warp Half']['control'].send_value(BUTTON_ON * oDevice.can_warp_half, True)
                hExtraParams['Warp Half']['param'] = 1.0 * oDevice.can_warp_half
                hExtraParams['Warp Double']['control'].send_value(BUTTON_ON * oDevice.can_warp_double, True)
                hExtraParams['Warp Double']['param'] = 1.0 * oDevice.can_warp_double
            elif _sParam == 'Warp Double':
                if oDevice.can_warp_double: oDevice.warp_double()
                oCtrl.send_value(BUTTON_ON * oDevice.can_warp_double, True)
                hExtraParams['Warp Half']['control'].send_value(BUTTON_ON * oDevice.can_warp_half, True)
                hExtraParams['Warp Half']['param'] = 1.0 * oDevice.can_warp_half
                hExtraParams['Warp As']['control'].send_value(BUTTON_ON * oDevice.can_warp_as, True)
                hExtraParams['Warp As']['param'] = 1.0 * oDevice.can_warp_as
            elif _sParam == 'Warp Half':
                if oDevice.can_warp_half: oDevice.warp_half()
                oCtrl.send_value(BUTTON_ON * oDevice.can_warp_half, True)
                hExtraParams['Warp Double']['control'].send_value(BUTTON_ON * oDevice.can_warp_double, True)
                hExtraParams['Warp Double']['param'] = 1.0 * oDevice.can_warp_double
                hExtraParams['Warp As']['control'].send_value(BUTTON_ON * oDevice.can_warp_as, True)
                hExtraParams['Warp As']['param'] = 1.0 * oDevice.can_warp_as
            elif _sParam == 'Slicing Playback Mode':
                oDevice.slicing_playback_mode = _nValue / 43
            elif _sParam == 'Gain' and _nValue != 0:
                oSample.gain = nParam
            elif _sParam == 'Warp':
                oSample.warping = (_nValue == BUTTON_ON)
            elif _sParam == 'Warp Mode':
                nWarpMode = _nValue / 22
                if nWarpMode == 5: nWarpMode = 6
                oSample.warp_mode = nWarpMode
            elif _sParam == 'Beats Gran Res':
                oSample.beats_granulation_resolution = _nValue / 19
            elif _sParam == 'Beats Trans Loop Mode':
                oSample.beats_transient_loop_mode = _nValue / 43
            elif _sParam == 'Beats Trans Envelope':
                oSample.beats_transient_envelope = nParam * 100.0
            elif _sParam == 'Tones Grain Size':
                oSample.tones_grain_size = nParam * 88.0 + 12.0
            elif _sParam == 'Texture Grain Size':
                oSample.texture_grain_size = nParam * 261.0 + 2.0
            elif _sParam == 'Texture Flux':
                oSample.texture_flux = nParam * 100.0
            elif _sParam == 'Complex Pro Formants':
                oSample.complex_pro_formants = nParam * 100.0
            elif _sParam == 'Complex Pro Envelope':
                oSample.complex_pro_envelope = nParam * 248.0 + 8.0
            elif _sParam == 'Slicing Style':
                oSample.slicing_style = _nValue / 32
            elif _sParam == 'Slicing Sensitivity':
                oSample.slicing_sensitivity = nParam
            elif _sParam == 'Slicing Beat Division':
                oSample.slicing_beat_division = _nValue / 12
            elif _sParam == 'Slicing Region Count':
                oSample.slicing_region_count = int(nParam * 62.0 + 2.0)
            elif _sParam == 'Clear Slices':
                oSample.clear_slices()
                oCtrl.send_value(BUTTON_ON, True)
        else:
            nParam = 0.0
        hExtraParams[_sParam]['param'] = nParam # used to sync bank

    # ****************************************************************

    def get_dev_reg(self, _sClass):
        nCurrTrackIdxAbs = self.curr_track_idx_abs()
        return self.m_hDevReg[nCurrTrackIdxAbs][_sClass]

    def get_dev_params(self, _sClass):
        return self.get_dev_reg(_sClass)['dev_params']

    def get_panel_params(self, _sClass):
        return self.get_dev_reg(_sClass)['panel_params']

    def get_extra_params(self, _sClass):
        return self.get_dev_reg(_sClass)['extra_params']

    def get_auto_params(self, _sClass):
        return self.get_dev_reg(_sClass)['auto_params']

    def get_device(self, _sClass):
        return self.get_dev_reg(_sClass)['device']

    # ****************************************************************

    def to_ascii(self, _sText, _nTruncate = 0):
        sAscii = ''.join([(ord(cChar) > 127 and '' or cChar.encode('utf-8')) for cChar in _sText])
        if (_nTruncate == 0):
            return sAscii
        else:
            return sAscii[:_nTruncate]

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
        return self.song().tracks # visible_tracks

    def returns(self):
        return self.song().return_tracks

    def tracks_and_returns(self):
        return tuple(self.tracks()) + tuple(self.returns())

    def get_track(self, _nTrackIdxAbs):
        aTracks = self.tracks()
        return aTracks[_nTrackIdxAbs]

    def sel_track(self, _oTrack = None):
        if (_oTrack != None):
            self.song().view.selected_track = _oTrack
        return self.song().view.selected_track

    def sel_track_idx_abs(self):
        aAllTracks = self.tracks_and_returns()
        oSelTrack  = self.sel_track()
        return list(aAllTracks).index(oSelTrack)

    def curr_track_idx_abs(self):
        aAllTracks = self.tracks_and_returns()
        oCurrTrack = self.get_track_or_return_or_none()
        return list(aAllTracks).index(oCurrTrack)

    def get_track_or_return_or_none(self, _oControl = None, _nResetValue = None):
        if (not self.is_enabled()):
            # disabled! nothing else to do!
            return self.send_reset_value(_oControl, _nResetValue)

        if (self._track == None):
            # no track! nothing else to do!
            return self.send_reset_value(_oControl, _nResetValue)

        if (self._track == self.song().master_track):
            # is master track, nothing else to do!
            return self.send_reset_value(_oControl, _nResetValue)

        return self._track

    def get_track_or_none(self, _oControl = None, _nResetValue = None):
        if (not self.is_enabled()):
            # disabled! nothing else to do!
            return self.send_reset_value(_oControl, _nResetValue)

        if (self._track == None):
            # no track! nothing else to do!
            return self.send_reset_value(_oControl, _nResetValue)

        if (self._track == self.song().master_track):
            # is master track, nothing else to do!
            return self.send_reset_value(_oControl, _nResetValue)

        if (not self._track in self.tracks()):
            # is a return track, nothing else to do!
            return self.send_reset_value(_oControl, _nResetValue)

        return self._track

    def get_clip_or_none(self, _oControl = None, _nResetValue = None):
        oTrack = self.get_track_or_none(_oControl, _nResetValue)
        if (oTrack == None):
            return None

        nSelSceneIdxAbs = self.sel_scene_idx_abs()
        oClipSlot       = oTrack.clip_slots[nSelSceneIdxAbs]
        if (not oClipSlot.has_clip):
            # empty clip, nothing else to do!
            return self.send_reset_value(_oControl, _nResetValue)

        return oClipSlot.clip

    def send_reset_value(self, _oControl, _nResetValue):
        if (_oControl != None):
            _oControl.send_value(_nResetValue, True)
        return None

    def log(self, _sMessage):
        Live.Base.log(_sMessage)

    def alert(self, sMessage):
        self.m_oCtrlInst.show_message(sMessage)

