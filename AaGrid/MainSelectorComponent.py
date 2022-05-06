import Live

from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.SubjectSlot import subject_slot

from SpecialSessionComponent import SpecialSessionComponent
from SpecialMixerComponent import SpecialMixerComponent
from SequencerComponent import SequencerComponent
from ToolsComponent import ToolsComponent

MAIN_MODE_SESSION   = 0
MAIN_MODE_MIXER     = 1
MAIN_MODE_SEQUENCER = 2
MAIN_MODE_TOOLS     = 3

SESSION_SUBMODE_LAUNCH = 0
SESSION_SUBMODE_ZOOM   = 1
SESSION_SUBMODE_SELECT = 2

MIXER_SUBMODE_TRACK = 0
MIXER_SUBMODE_SENDS = 1
MIXER_SUBMODE_VOL   = 2

class MainSelectorComponent(ModeSelectorComponent):
    """ Class that reassigns the button on the controller to different functions """

    def __init__(self, _oMatrix, _lTrackButtons, _lSceneButtons, _lTrackSliders, _oCtrlSurface, _hCfg):
        ModeSelectorComponent.__init__(self) #super constructor

        self.m_oMatrix       = _oMatrix
        self.m_lNavButtons   = _lTrackButtons[:4]
        self.m_lModeButtons  = _lTrackButtons[4:]
        self.m_lSceneButtons = _lSceneButtons
        self.m_lTrackSliders = _lTrackSliders
        self.m_oMasterSlider = _lTrackSliders[8:][0]
        self.m_oCtrlSurface  = _oCtrlSurface
        self.m_oFaderCtrl    = None
        self.m_hCfg          = _hCfg
        self.m_aSubModeIdx   = [0, 0, 0, 0]           # sub-mode index   (order by main mode)
        self.m_aSubModeNum   = [3, 3, 4, 1]           # num of sub-modes (order by main-mode)
        self.m_nPrevMainMode = MAIN_MODE_SESSION      # previously used main-mode
        self.m_nNewMainMode  = MAIN_MODE_SESSION      # new main-mode
        self.m_nNewSubMode   = SESSION_SUBMODE_LAUNCH # new sub-mode
        self.m_aTitle        = [
            ['SESSION / LAUNCH' , 'SESSION / ZOOM'  , 'SESSION / SELECT'],
            ['MIXER / TRACK'    , 'MIXER / SENDS'   , 'MIXER / VOL'],
            ['SEQUENCER / NOTES', 'SEQUENCER / ZOOM', 'SEQUENCER / TOOLS', 'SEQUENCER / RHYTHMS'],
            ['TOOLS'],
        ]

        self._mode_index = 0 # inherited from ModeSelectorComponent
        self.set_mode_buttons(self.m_lModeButtons)
        self.m_oSession = SpecialSessionComponent(_oMatrix.width(), _oMatrix.height())
        self.m_oSession.name = 'Session_Control'
        self.m_hCfg['oSession'] = self.m_oSession

        self.m_oZooming = SessionZoomingComponent(self.m_oSession, enable_skinning = True)
        self.m_oZooming.name = 'Session_Overview'

        self.m_oMixer = SpecialMixerComponent(_oMatrix.width(), self.m_hCfg)
        self.m_oMixer.name = 'Mixer'
        for nTrackIdx in range(_oMatrix.width()):
            oStrip = self.m_oMixer.channel_strip(nTrackIdx)
            oStrip.name = 'Channel_Strip_' + str(nTrackIdx)
        self.m_oSession.set_mixer(self.m_oMixer)

        self.m_oSequencer = SequencerComponent(_oCtrlSurface, _oMatrix, _lSceneButtons, self.m_lNavButtons, _lTrackSliders)
        self.m_oSequencer.name = 'Sequencer'

        self.m_oTools = ToolsComponent(_oCtrlSurface, _oMatrix, _lSceneButtons, self.m_lNavButtons, _lTrackSliders)
        self.m_oTools.name = 'Tools'

        # non-matrix buttons
        self.m_aAllButtons = []
        for oButton in self.m_lSceneButtons + self.m_lNavButtons:
            self.m_aAllButtons.append(oButton)

        self.m_aAllButtons = tuple(self.m_aAllButtons)

    def disconnect(self):
        for oButton in self._modes_buttons:
            oButton.remove_value_listener(self._mode_value)

        self.m_oSession   = None
        self.m_oZooming   = None
        self.m_oMixer     = None
        self.m_oSequencer = None
        self.m_oTools     = None

        for oButton in self.m_aAllButtons:
            oButton.set_on_off_values("DefaultButton.Disabled", "DefaultButton.Disabled")

        self._on_master_volume_value.subject = None
        self.m_oMatrix       = None
        self.m_lSceneButtons = None
        self.m_lNavButtons   = None
        self.m_lTrackSliders = None
        self.m_oMasterSlider = None

        ModeSelectorComponent.disconnect(self)

    # ****************************************************************

    def setup_as_primary_instance(self, _oSecPeer):
        self.m_oSequencer.setup_as_primary_instance(_oSecPeer)

    def setup_as_secondary_instance(self, _oPrimPeer):
        self.m_oSequencer.setup_as_secondary_instance(_oPrimPeer)

    def receive_peer_command(self, _hCmd):
        self.m_oSequencer.receive_peer_command(_hCmd)

    def receive_matrix_command(self, _hCmd):
        self.m_oSequencer.receive_matrix_command(_hCmd)

    # ****************************************************************

    def session_component(self):
        return self.m_oSession

    def number_of_modes(self):
        return 4 # Session, Mixer, Sequencer, Tools

    def on_enabled_changed(self):
        self.update()

    def channel_for_current_mode(self):
        return self.m_hCfg['Channel'] # 0 => MIDI CHANNEL 1

    def set_mode(self, _nMode):
        self._clean_heap()
        self._modes_heap = [(_nMode, None, None)]
        # in the original implementation of ModeSelectorComponent they prevent
        # from going from a mode index to the same mode index, BUT we need to override
        # that behavior since we want to allow going from a main mode to the same main mode,
        # but switching sub-mode

    def _update_mode(self):
        # get first value of last _modes_heap tuple.
        # _modes_heap tuple structure is (mode, sender, observer)
        self.m_nNewMainMode = self._modes_heap[-1][0]

        if self.m_nPrevMainMode == self.m_nNewMainMode: # remaining in the same mode but switching submode
            # update the submode
            nCurSubMode = self.m_aSubModeIdx[self.m_nNewMainMode]   # current submode index
            nNumSubMode = self.m_aSubModeNum[self.m_nNewMainMode]   # number of submodes of the main mode
            nNewSubMode = (nCurSubMode + 1) % nNumSubMode # use next submode or go back to first submode
            if (nNewSubMode != nCurSubMode):
                self.m_aSubModeIdx[self.m_nNewMainMode] = nNewSubMode # assign the new submode idx
                self.m_nNewSubMode = nNewSubMode
                self.update()
        else:
            self.m_aSubModeIdx[self.m_nNewMainMode] = 0 # changing main mode, start from first submode!
            self.m_nNewSubMode = 0
            self.update() # changing mode, just update right away!

    def update(self):
        assert (self._modes_buttons != None)
        if self.is_enabled():
            self._update_mode_buttons()

            bAsActive   = True
            bPagEnabled = True

            self.m_oSession.set_allow_update(False)
            for nSceneIdx in range(self.m_oMatrix.height()):
                oScene = self.m_oSession.scene(nSceneIdx)
                for nTrackIdx in range(self.m_oMatrix.width()):
                    oScene.clip_slot(nTrackIdx).set_allow_update(False)
            self.m_oZooming.set_allow_update(False)
            self.m_oMixer.set_allow_update(False)

            self.m_oCtrlSurface.show_message("MODE: %s" % (self.m_aTitle[self.m_nNewMainMode][self.m_nNewSubMode]))

            if self.m_nNewMainMode == MAIN_MODE_SESSION:
                self._setup_mixer_controls(not bAsActive)
                self._setup_sequencer_controls(not bAsActive)
                self._setup_tools_controls(not bAsActive)
                self._setup_paging_controls(bPagEnabled)
                self._setup_session_controls(bAsActive)

            elif self.m_nNewMainMode == MAIN_MODE_MIXER:
                self._setup_session_controls(not bAsActive)
                self._setup_sequencer_controls(not bAsActive)
                self._setup_tools_controls(not bAsActive)
                self._setup_paging_controls(bPagEnabled)
                self._setup_mixer_controls(bAsActive)

            elif self.m_nNewMainMode == MAIN_MODE_SEQUENCER:
                self._setup_paging_controls(not bPagEnabled)
                self._setup_session_controls(not bAsActive)
                self._setup_mixer_controls(not bAsActive)
                self._setup_tools_controls(not bAsActive)
                self._setup_sequencer_controls(bAsActive)

            elif self.m_nNewMainMode == MAIN_MODE_TOOLS:
                self._setup_session_controls(not bAsActive)
                self._setup_mixer_controls(not bAsActive)
                self._setup_sequencer_controls(not bAsActive)
                self._setup_paging_controls(bPagEnabled)
                self._setup_tools_controls(bAsActive)

            self._update_control_channels()

            self.m_oSession.set_allow_update(True)
            for nSceneIdx in range(self.m_oMatrix.height()):
                oScene = self.m_oSession.scene(nSceneIdx)
                for nTrackIdx in range(self.m_oMatrix.width()):
                    oScene.clip_slot(nTrackIdx).set_allow_update(True)
            self.m_oZooming.set_allow_update(True)
            self.m_oMixer.set_allow_update(True)

            self.m_nPrevMainMode = self.m_nNewMainMode

    def _update_mode_buttons(self):
        for nModeIdx in range(self.number_of_modes()):
            self._modes_buttons[nModeIdx].set_on_off_values("Mode.On", "Mode.Off")
            if (nModeIdx == self.m_nNewMainMode):
                self._modes_buttons[nModeIdx].turn_on()
            else:
                self._modes_buttons[nModeIdx].turn_off()

    # **************************************************************************

    def _setup_paging_controls(self, _bPagEnabled):
        for oButton in self.m_lNavButtons:
            if _bPagEnabled:
                oButton.set_on_off_values("Nav.On", "Nav.Off")
            else:
                oButton.set_on_off_values("DefaultButton.Disabled", "DefaultButton.Disabled")

        if _bPagEnabled:
            self.m_oSession.set_page_up_button(self.m_lNavButtons[0])
            self.m_oSession.set_page_down_button(self.m_lNavButtons[1])
            self.m_oSession.set_page_left_button(self.m_lNavButtons[2])
            self.m_oSession.set_page_right_button(self.m_lNavButtons[3])
        else:
            self.m_oSession.set_page_up_button(None)
            self.m_oSession.set_page_down_button(None)
            self.m_oSession.set_page_left_button(None)
            self.m_oSession.set_page_right_button(None)

    # **************************************************************************

    def _setup_session_controls(self, _bAsActive):
        if _bAsActive:
            self._toggle_controller_buttons(True)

            if self.m_nNewSubMode == SESSION_SUBMODE_LAUNCH:
                self.release_session_controls(SESSION_SUBMODE_SELECT)
                for nSceneIdx in range(self.m_oSession.height()):
                    oScene = self.m_oSession.scene(nSceneIdx)
                    oScene.set_launch_button(self.m_lSceneButtons[nSceneIdx])
                    for nTrackIdx in range(self.m_oSession.width()):
                        oButton = self.m_oMatrix.get_button(nTrackIdx, nSceneIdx)
                        oButton.set_on_off_values("DefaultButton.Disabled", "DefaultButton.Disabled")
                        oButton.set_enabled(_bAsActive)
                        oScene.clip_slot(nTrackIdx).set_launch_button(oButton)

            elif self.m_nNewSubMode == SESSION_SUBMODE_ZOOM:
                self.release_session_controls(SESSION_SUBMODE_LAUNCH)
                for nSceneIdx in range(self.m_oMatrix.height()):
                    self.m_lSceneButtons[nSceneIdx].set_on_off_values("Scene")
                self.m_oZooming._enable_skinning()
                self.m_oZooming.set_button_matrix(self.m_oMatrix)
                self.m_oZooming.set_scene_bank_buttons(self.m_lSceneButtons)
                self.m_oZooming.update()

            elif self.m_nNewSubMode == SESSION_SUBMODE_SELECT:
                self.release_session_controls(SESSION_SUBMODE_ZOOM)
                for nSceneIdx in range(self.m_oSession.height()):
                    oButton = self.m_lSceneButtons[nSceneIdx]
                    oButton.set_on_off_values("Session.SceneSel")
                    oScene = self.m_oSession.scene(nSceneIdx)
                    oScene.set_select_control(oButton)
                    for nTrackIdx in range(self.m_oSession.width()):
                        oButton = self.m_oMatrix.get_button(nTrackIdx, nSceneIdx)
                        oButton.set_enabled(_bAsActive)
                        oClipSlot = oScene.clip_slot(nTrackIdx)
                        oClipSlot.set_launch_button(oButton)
                        oClipSlot.set_select_button(oButton)
        else:
            self.release_session_controls()

        self.setup_volume_controls(_bAsActive)

    def release_session_controls(self, _nSubMode = None):
        self._toggle_controller_buttons(False)

        # disconnect the buttons from their controls
        if (_nSubMode == SESSION_SUBMODE_LAUNCH or _nSubMode == None):
            for nSceneIdx in range(self.m_oSession.height()):
                oScene = self.m_oSession.scene(nSceneIdx)
                oScene.set_launch_button(None)
                for nTrackIdx in range(self.m_oSession.width()):
                    oScene.clip_slot(nTrackIdx).set_launch_button(None)

        if (_nSubMode == SESSION_SUBMODE_ZOOM or _nSubMode == None):
            self.m_oZooming.set_button_matrix(None)
            self.m_oZooming.set_scene_bank_buttons(None)

        if (_nSubMode == SESSION_SUBMODE_SELECT or _nSubMode == None):
            for nSceneIdx in range(self.m_oSession.height()):
                oScene = self.m_oSession.scene(nSceneIdx)
                oScene.set_select_control(None)
                for nTrackIdx in range(self.m_oSession.width()):
                    oScene.clip_slot(nTrackIdx).set_launch_button(None)
                    oScene.clip_slot(nTrackIdx).set_select_button(None)

    # **************************************************************************

    def _setup_mixer_controls(self, _bAsActive):
        if _bAsActive:
            self._toggle_controller_buttons(True)

            if self.m_nNewSubMode == MIXER_SUBMODE_TRACK:
                self.release_mixer_controls(MIXER_SUBMODE_VOL)
                aNames = ['PanReset', 'VolReset', 'Stop', 'Mute', 'Solo', 'Arm', 'Deck', 'TrackSel']
                aStopButtons = []
                for nTrackIdx in range(self.m_oMatrix.width()):
                    for nSceneIdx in range(self.m_oMatrix.height()):
                        oButton = self.m_oMatrix.get_button(nTrackIdx, nSceneIdx)
                        oButton.set_on_off_values("Mixer.%s" % (aNames[nSceneIdx]))
                        oButton.turn_off()
                    oStrip = self.m_oMixer.channel_strip(nTrackIdx)
                    oStrip.set_track_controls(
                        self.m_oMatrix.get_button(nTrackIdx, 0), # pan reset
                        self.m_oMatrix.get_button(nTrackIdx, 1), # vol reset
                        self.m_oMatrix.get_button(nTrackIdx, 6)) # deck
                    oStrip.set_mute_button  (self.m_oMatrix.get_button(nTrackIdx, 3))
                    oStrip.set_solo_button  (self.m_oMatrix.get_button(nTrackIdx, 4))
                    oStrip.set_arm_button   (self.m_oMatrix.get_button(nTrackIdx, 5))
                    oStrip.set_select_button(self.m_oMatrix.get_button(nTrackIdx, 7))
                    aStopButtons.append     (self.m_oMatrix.get_button(nTrackIdx, 2))
                    oStrip.set_invert_mute_feedback(True)
                self.m_oSession.set_stop_track_clip_buttons(aStopButtons)

                for nSceneIdx in range(self.m_oMatrix.height()):
                    oButton = self.m_lSceneButtons[nSceneIdx]
                    oButton.set_on_off_values("Mixer.SceneSel")
                    oScene = self.m_oSession.scene(nSceneIdx)
                    oScene.set_select_control(oButton)

            elif self.m_nNewSubMode == MIXER_SUBMODE_SENDS:
                self.release_mixer_controls(MIXER_SUBMODE_TRACK)
                aNames = ['Send', 'Send', 'Send', 'Send', 'Send', 'Send', 'Monitor', 'Select']
                for nTrackIdx in range(self.m_oMatrix.width()):
                    for nSceneIdx in range(self.m_oMatrix.height()):
                        self.m_oMatrix.get_button(nTrackIdx, nSceneIdx).set_on_off_values("Mixer.%s" % (aNames[nSceneIdx]))
                    oStrip = self.m_oMixer.channel_strip(nTrackIdx)
                    oStrip.set_send_controls(
                        self.m_oMatrix.get_button(nTrackIdx, 0),
                        self.m_oMatrix.get_button(nTrackIdx, 1),
                        self.m_oMatrix.get_button(nTrackIdx, 2),
                        self.m_oMatrix.get_button(nTrackIdx, 3),
                        self.m_oMatrix.get_button(nTrackIdx, 4),
                        self.m_oMatrix.get_button(nTrackIdx, 5))
                    oStrip.set_monitor_button(self.m_oMatrix.get_button(nTrackIdx, 6))
                    oStrip.set_select_button (self.m_oMatrix.get_button(nTrackIdx, 7))
                    #oStrip.set_view_controls(
                    #    self.m_oMatrix.get_button(nTrackIdx, 6),
                    #    self.m_oMatrix.get_button(nTrackIdx, 7))

                for nSceneIdx in range(self.m_oMatrix.height()):
                    oButton = self.m_lSceneButtons[nSceneIdx]
                    oButton.set_on_off_values("Mixer.SceneSel")
                    oScene = self.m_oSession.scene(nSceneIdx)
                    oScene.set_select_control(oButton)

            elif self.m_nNewSubMode == MIXER_SUBMODE_VOL:
                self.release_mixer_controls(MIXER_SUBMODE_SENDS)
                for nTrackIdx in range(self.m_oMatrix.width()):
                    for nSceneIdx in range(self.m_oMatrix.height()):
                        self.m_oMatrix.get_button(nTrackIdx, nSceneIdx).set_on_off_values("Mixer.Vol")
                    oStrip = self.m_oMixer.channel_strip(nTrackIdx)
                    oStrip.set_vol_controls(
                        self.m_oMatrix.get_button(nTrackIdx, 0),
                        self.m_oMatrix.get_button(nTrackIdx, 1),
                        self.m_oMatrix.get_button(nTrackIdx, 2),
                        self.m_oMatrix.get_button(nTrackIdx, 3),
                        self.m_oMatrix.get_button(nTrackIdx, 4),
                        self.m_oMatrix.get_button(nTrackIdx, 5),
                        self.m_oMatrix.get_button(nTrackIdx, 6),
                        self.m_oMatrix.get_button(nTrackIdx, 7))

                for nSceneIdx in range(self.m_oMatrix.height()):
                    oButton = self.m_lSceneButtons[nSceneIdx]
                    oButton.set_on_off_values("Mixer.SceneSel")
                    oScene = self.m_oSession.scene(nSceneIdx)
                    oScene.set_vol_control(oButton, oStrip.m_aVolMap[nSceneIdx])
        else:
            self.release_mixer_controls()

        self.setup_volume_controls(_bAsActive)

    def release_mixer_controls(self, _nSubMode = None):
        self._toggle_controller_buttons(False)

        # disconnect the buttons from their controls
        if (_nSubMode == MIXER_SUBMODE_TRACK or _nSubMode == None): # track commands
            for nTrackIdx in range(self.m_oMatrix.width()):
                oStrip = self.m_oMixer.channel_strip(nTrackIdx)
                oStrip.set_track_controls(None, None, None)
                oStrip.set_mute_button   (None)
                oStrip.set_solo_button   (None)
                oStrip.set_arm_button    (None)
                oStrip.set_select_button (None)
            self.m_oSession.set_stop_track_clip_buttons(None)
            for nSceneIdx in range(self.m_oMatrix.height()):
                oScene = self.m_oSession.scene(nSceneIdx)
                oScene.set_select_control(None)

        if (_nSubMode == MIXER_SUBMODE_SENDS or _nSubMode == None): # send commands
            for nTrackIdx in range(self.m_oMatrix.width()):
                oStrip = self.m_oMixer.channel_strip(nTrackIdx)
                oStrip.set_send_controls (None, None, None, None, None, None)
                oStrip.set_monitor_button(None)
                oStrip.set_select_button (None)
                #oStrip.set_view_controls(None, None)
            for nSceneIdx in range(self.m_oMatrix.height()):
                oScene = self.m_oSession.scene(nSceneIdx)
                oScene.set_select_control(None)

        if (_nSubMode == MIXER_SUBMODE_VOL or _nSubMode == None):
            for nTrackIdx in range(self.m_oMatrix.width()):
                oStrip = self.m_oMixer.channel_strip(nTrackIdx)
                oStrip.set_vol_controls(None, None, None, None, None, None, None, None)
            for nSceneIdx in range(self.m_oMatrix.height()):
                oScene = self.m_oSession.scene(nSceneIdx)
                oScene.set_vol_control(None, 0.0)

        for nTrackIdx in range(self.m_oSession.width()):
            oStrip = self.m_oMixer.channel_strip(nTrackIdx)
            oStrip.set_volume_control(None)

    # **************************************************************************

    def _setup_sequencer_controls(self, _bAsActive):
        if _bAsActive:
            self._toggle_controller_buttons(True)
            self.m_oSequencer.connect_controls(self.m_nNewSubMode)
        else:
            self.m_oSequencer.release_seq_controls()

    # **************************************************************************

    def _setup_tools_controls(self, _bAsActive):
        if _bAsActive:
            self._toggle_controller_buttons(True)

            if self.m_nNewSubMode == 0: # track commands
                self.release_tools_controls(-1)
                # setup track and scene selection buttons
                for nTrackIdx in range(self.m_oMatrix.width()):
                    self.m_oMatrix.get_button(nTrackIdx, 7).set_on_off_values("Mixer.TrackSel")
                    oStrip = self.m_oMixer.channel_strip(nTrackIdx)
                    oStrip.set_select_button(self.m_oMatrix.get_button(nTrackIdx, 7))
                for nSceneIdx in range(self.m_oMatrix.height()):
                    oButton = self.m_lSceneButtons[nSceneIdx]
                    oButton.set_on_off_values("Mixer.SceneSel")
                    oScene = self.m_oSession.scene(nSceneIdx)
                    oScene.set_select_control(oButton)
                self.m_oTools.connect_controls(0)
        else:
            self.release_tools_controls()

    def release_tools_controls(self, _nSubMode = None):
        self._toggle_controller_buttons(False)

        # disconnect the buttons from their controls
        if (_nSubMode == 0 or _nSubMode == None): # Loop
            for nTrackIdx in range(self.m_oMatrix.width()):
                oStrip = self.m_oMixer.channel_strip(nTrackIdx)
                oStrip.set_select_button(None)
            for nSceneIdx in range(self.m_oMatrix.height()):
                oScene = self.m_oSession.scene(nSceneIdx)
                oScene.set_select_control(None)
            self.m_oTools.release_controls(0)

    # **************************************************************************

    def setup_volume_controls(self, _bActive):
        if _bActive:
            for nTrackIdx in range(self.m_oSession.width()):
                oStrip  = self.m_oMixer.channel_strip(nTrackIdx)
                oSlider = self.m_lTrackSliders[nTrackIdx]
                oStrip.set_volume_control(oSlider)
            self._on_master_volume_value.subject = self.m_oMasterSlider
        else:
            for nTrackIdx in range(self.m_oSession.width()):
                oStrip = self.m_oMixer.channel_strip(nTrackIdx)
                oStrip.set_volume_control(None)
            self._on_master_volume_value.subject = None

    def _toggle_controller_buttons(self, _bActive):
        if _bActive:
            self._activate_navigation_buttons(True)
            self._activate_scene_buttons(True)
            self._activate_matrix(True)
        else:
            # turn off matrix and scene buttons
            for nSceneIdx in range(self.m_oMatrix.height()):
                self.m_lSceneButtons[nSceneIdx].set_on_off_values("DefaultButton.Disabled", "DefaultButton.Disabled")
                for nTrackIdx in range(self.m_oMatrix.width()):
                    self.m_oMatrix.get_button(nTrackIdx, nSceneIdx).set_on_off_values(127, "DefaultButton.Disabled")

    @subject_slot(u'value')
    def _on_master_volume_value(self, _nValue):
        assert (self.m_oMasterSlider != None)
        if self.is_enabled() == False: return
        nVol = float(_nValue) / 127.0
        for nTrackIdx in range(self.m_oSession.width()):
            oStrip = self.m_oMixer.channel_strip(nTrackIdx)
            oTrack = oStrip.track
            if (oTrack != None):
                oTrack.mixer_device.volume.value = nVol

    def on_shift_value(self):
        if self.m_nNewMainMode == MAIN_MODE_SEQUENCER:
            self.m_oSequencer.on_shift_value()
        else:
            if self.m_oFaderCtrl == None:
                self.find_fader_ctrl()
            if self.m_oFaderCtrl == None: return
            nTrackOffset = self.m_oSession.track_offset()
            self.m_oFaderCtrl.move_to_track_offset(nTrackOffset)

    def find_fader_ctrl(self):
        aCtrlInsts = Live.Application.get_application().control_surfaces
        for oCtrlInst in aCtrlInsts:
            sCtrlName = oCtrlInst.__class__.__name__
            if sCtrlName == 'AaFader':
                self.m_oFaderCtrl = oCtrlInst

    # **************************************************************************

    def _activate_navigation_buttons(self, _bActive):
        for oButton in self.m_lNavButtons:
            oButton.set_enabled(_bActive)

    def _activate_scene_buttons(self, _bActive):
        for oButton in self.m_lSceneButtons:
            oButton.set_enabled(_bActive)

    def _activate_matrix(self, _bActive):
        for nSceneIdx in range(self.m_hCfg['NumScenes']):
            for nTrackIdx in range(self.m_hCfg['NumTracks']):
                self.m_oMatrix.get_button(nTrackIdx, nSceneIdx).set_enabled(_bActive)

    # **************************************************************************

    def _on_sel_scene_changed(self):
        if self.m_nNewMainMode == MAIN_MODE_SEQUENCER:
            # force the submode to match with the internal sequencer submode
            self.m_nNewSubMode = self.m_oSequencer._on_sel_scene_changed()
            self.m_aSubModeIdx[MAIN_MODE_SEQUENCER] = self.m_nNewSubMode
        elif self.m_nNewMainMode == MAIN_MODE_TOOLS:
            self.m_oTools._on_sel_scene_changed()

    def _on_sel_track_changed(self):
        if self.m_nNewMainMode == MAIN_MODE_SEQUENCER:
            # force the submode to match with the internal sequencer submode
            self.m_nNewSubMode = self.m_oSequencer._on_sel_track_changed()
            self.m_aSubModeIdx[MAIN_MODE_SEQUENCER] = self.m_nNewSubMode
        elif self.m_nNewMainMode == MAIN_MODE_TOOLS:
            self.m_oTools._on_sel_track_changed()

    # **************************************************************************

    def _update_control_channels(self):
        nChannel = self.channel_for_current_mode()
        for oButton in self.m_aAllButtons:
            oButton.set_channel(nChannel)
            oButton.force_next_send()

    def log(self, _sMessage):
        Live.Base.log(_sMessage)

