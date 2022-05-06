import time
import Live
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.TransportComponent import TransportComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.SubjectSlot import subject_slot #added

class SpecialTransportComponent(TransportComponent):
    __doc__ = ' TransportComponent that only uses certain buttons if a shift button is pressed'

    def __init__(self, _hCfg):
        TransportComponent.__init__(self)
        self.m_hCfg      = _hCfg
        self.m_oCtrlInst = _hCfg['oCtrlInst']
        self.m_oSong     = self.m_oCtrlInst.song()
        self.m_bAutoOn   = False # auto not started
        self.m_bBusy     = False # not currently busy
        self.m_nLastVal  = 0     # last value of tempo encoder (MIDI value) (used for re-sync)
        self.m_nStart    = 0.0   # start time reference for auto-tempo
        self.m_nDelta    = 0.0   # auto-tempo delta

        self.m_hEls       = {}
        self.m_hListeners = {}

        # controls
        self.register_el('enc', 'Tempo', self._on_tempo)

        # target tempo for auto decrease or auto increase
        self.m_nTempoBottom = 60.0 # lowest tempo target
        self.m_nTempoTarget = self.m_nTempoBottom
        self.register_el('but', 'TempoTarget', self._on_tempo_target)

        # default tempo vel is 1 bpm / 1 bar
        self.m_nTempoVel = 1.0
        self.register_el('but', 'TempoVel'  , self._on_tempo_vel)
        self.register_el('but', 'TempoAuto' , self._on_tempo_auto)
        self.register_el('but', 'TempoReset', self._on_tempo_reset)

        # tempo window buttons
        self.m_nTempoMax  = self.m_hCfg['TempoMax']
        self.m_nTempoMin  = self.m_hCfg['TempoMin']
        self.m_nTempoSpan = int(self.m_nTempoMax - self.m_nTempoMin)
        self.register_el('but', 'TempoWinDec', self._on_tempo_win_dec)
        self.register_el('but', 'TempoWinInc', self._on_tempo_win_inc)
        return None


    def disconnect(self):
        TransportComponent.disconnect(self)
        for sName in self.m_hListeners:
            self.get_el(sName).remove_value_listener(self.m_hListeners[sName])
        return None

    # ================================================================

    # executes every 100 ms
    def update_sync_tasks(self):
        if (self.m_bAutoOn == False or self.m_bBusy == True):
            return # nothing else to do here

        # update tempo according to the delta
        nOldTempo = self.m_oSong.tempo
        nNewTempo = nOldTempo + self.m_nDelta
        if (self.m_nDelta < 0.0):
            #Live.Base.log('Decreasing: %f -> %f' % (nOldTempo, nNewTempo))
            if (nNewTempo > self.m_nTempoTarget):
                self.m_oSong.tempo = nNewTempo
            else:
                self.m_bAutoOn     = False # we are done!
                self.m_oSong.tempo = self.m_nTempoTarget
                nTimespan          = time.time() - self.m_nStart
                self.alert('> DONE TEMPO DECR in %f [sec]' % (nTimespan))
        else:
            #Live.Base.log('Increasing: %f -> %f' % (nOldTempo, nNewTempo))
            if (nNewTempo < self.m_nTempoTarget):
                self.m_oSong.tempo = nNewTempo
            else:
                self.m_bAutoOn     = False # we are done!
                self.m_oSong.tempo = self.m_nTempoTarget
                nTimespan          = time.time() - self.m_nStart
                self.alert('> DONE TEMPO INCR in %f [sec]' % (nTimespan))

        # recompute nTempoMax and nTempoMin so that m_nLastVal is equivalent to the current tempo
        nRatio = self.m_nTempoSpan / 128.0

        self.m_nTempoMin = int(nNewTempo - (nRatio * self.m_nLastVal))
        if (self.m_nTempoMin < 0):
            self.m_nTempoMin = 10 # minimum possible tempo
        self.m_nTempoMax = self.m_nTempoMin + self.m_nTempoSpan

    # ================================================================

    @subject_slot(u'value')
    def _on_tempo(self, _nValue):
        self.m_nLastVal = _nValue

        if (self.m_bAutoOn):
            self.m_bAutoOn = False # stop auto-tempo!
            return # nothing else to do here!

        # manually updating the tempo!
        if self.is_enabled():
            nRatio = self.m_nTempoSpan / 128.0
            self.song().tempo = nRatio * _nValue + self.m_nTempoMin


    @subject_slot(u'value')
    def _on_tempo_target(self, _nValue):
        if self.is_enabled():
            self.m_nTempoTarget = self.m_nTempoBottom + _nValue
            self.alert('> TARGET: %f [BPM]' % (self.m_nTempoTarget))
            self.compute_tempo_delta()


    @subject_slot(u'value')
    def _on_tempo_vel(self, _nValue):
        if self.is_enabled():
            nBars = _nValue / 5 # an integer between 0 and 25
            if (nBars == 0):
                self.m_nTempoVel = 0.5 # tempo velocity in bars
            else:
                self.m_nTempoVel = nBars * 1.0 # tempo velocity in bars
            nBarDuration = (60.0 / self.m_oSong.tempo) * 4.0 # in seconds
            nTimeSpan    = self.m_nTempoVel * nBarDuration   # in seconds
            self.alert('> Tempo velocity: %f [Bars] = %f [sec]' % (self.m_nTempoVel, nTimeSpan))
            self.compute_tempo_delta()


    @subject_slot(u'value')
    def _on_tempo_auto(self, _nValue):
        if _nValue < 64:
           return # do not process "toggle off"

        if self.is_enabled() == False:
           return # only when enabled

        # check if is already running, in that case only stop
        if self.m_bAutoOn:
            self.m_bAutoOn = False
            self.m_nStart  = 0.0
            self.m_nDelta  = 0.0
            self.alert('> STOP AUTO TEMPO <')
            return

        # start auto tempo
        self.m_nStart  = time.time() # time as float (seconds), decimals are milliseconds
        self.m_bAutoOn = True
        self.compute_tempo_delta()


    @subject_slot(u'value')
    def _on_tempo_reset(self, _nValue):
        if _nValue < 64:
           return # do not process "toggle off"

        self.m_nTempoMax = self.m_hCfg['TempoMax']
        self.m_nTempoMin = self.m_hCfg['TempoMin']
        self.alert('> [RESET] Tempo window: %d - %d [BPM]' % (self.m_nTempoMin, self.m_nTempoMax))


    @subject_slot(u'value')
    def _on_tempo_win_dec(self, _nValue):
        if _nValue < 64:
           return # do not process "toggle off"

        if self.is_enabled():
            self.m_nTempoMax = self.m_nTempoMax - 5
            self.m_nTempoMin = self.m_nTempoMin - 5
            self.alert('> [DECR] Tempo window: %d - %d  [BPM]' % (self.m_nTempoMin, self.m_nTempoMax))


    @subject_slot(u'value')
    def _on_tempo_win_inc(self, _nValue):
        if _nValue < 64:
           return # do not process "toggle off"

        if self.is_enabled():
            self.m_nTempoMax = self.m_nTempoMax + 5
            self.m_nTempoMin = self.m_nTempoMin + 5
            self.alert('> [INCR] Tempo window: %d - %d [BPM]' % (self.m_nTempoMin, self.m_nTempoMax))

    # ================================================================

    def compute_tempo_delta(self):
        if self.m_bAutoOn == False:
            return # nothing else to do here!

        self.m_bBusy = True

        # we have start time, tempo velocity, current tempo, target tempo (min/max)
        nCurrTempo    = self.m_oSong.tempo               # in BPM
        nBarDuration  = (60.0 / nCurrTempo) * 4.0        # in seconds
        nTimeSpan     = self.m_nTempoVel * nBarDuration  # in seconds
        nEndTime      = self.m_nStart + nTimeSpan        # in seconds
        nTempoDelta   = self.m_nTempoTarget - nCurrTempo # in BPM
        self.m_nDelta = (nTempoDelta / nTimeSpan) / 10.0 # in BPM (divide with 10.0 since sync tasks executes every 100 ms)
        if (nTempoDelta < 0.0):
            self.alert('> TEMPO DECR (%f -> %f) in %f [s] => %f [bars]' % (nCurrTempo, self.m_nTempoTarget, nTimeSpan, self.m_nTempoVel))
            #Live.Base.log('> TEMPO DECR (%f -> %f) in %f [s] => %f [bars]' % (nCurrTempo, self.m_nTempoTarget, nTimeSpan, self.m_nTempoVel))
        else:
            self.alert('> TEMPO INCR (%f -> %f) in %f [s] => %f [bars]' % (nCurrTempo, self.m_nTempoTarget, nTimeSpan, self.m_nTempoVel))
            #Live.Base.log('> TEMPO INCR (%f -> %f) in %f [s] => %f [bars]' % (nCurrTempo, self.m_nTempoTarget, nTimeSpan, self.m_nTempoVel))

        self.m_bBusy = False

    # ================================================================

    def register_el(self, _sType, _sName, _fListener):
        if (_sType == 'but'):
            _fListener.subject = self.create_button(_sName)
        elif (_sType == 'enc'):
            _fListener.subject = self.create_encoder(_sName)
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


    def create_encoder(self, _sName, _nIndex = None):
        return self.create_button(_sName, _nIndex)


    def get_el(self, _sName, _nIndex = None):
        sName, sKey, nOffset = self.get_el_ids(_sName, _nIndex)
        return self.m_hEls[sName]

    # ****************************************************************

    def alert(self, _sMessage):
        self.m_oCtrlInst.show_message(_sMessage)


