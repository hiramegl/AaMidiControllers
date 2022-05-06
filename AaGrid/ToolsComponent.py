import Live

from _Framework.CompoundComponent import CompoundComponent
from _Framework.TransportComponent import TransportComponent

class ToolsComponent(CompoundComponent):

    def __init__(self, _oCtrlInst, _oMatrix, _lSceneButtons, _lNavButtons, _lTrackSliders):
        self.m_oCtrlInst = _oCtrlInst
        super(ToolsComponent, self).__init__()

        self.m_oTransp = TransportComponent()
        self.m_oTransp.name = 'Transport'

        self.m_oMatrix       = _oMatrix
        self.m_lSceneButtons = _lSceneButtons
        self.m_lNavButtons   = _lNavButtons
        self.m_lTrackSliders = _lTrackSliders

        self.m_nRollStart    = 0.0 # roll start for 1 bar (1/8 of 1 bar  = 1/2 beat)
        self.m_nRollSpan     = 4.0
        self.m_aSizes        = [0.125, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0] # in beats
        self.m_nSizeIdx      = 3 # default size = 1 beat
        self.m_aToolsSkin    = [
            ['Loop.Size' , 'Loop.Size' , 'Loop.Size' , 'Loop.Size' , 'Loop.Size'  , 'Loop.Size'  , 'Loop.Size', 'Loop.Size'],
            ['Loop.Shift', 'Loop.Shift', 'Loop.Start', 'Loop.Start', 'Loop.Middle', 'Loop.Middle', 'Loop.End' , 'Loop.End' ],
            ['Loop.Begin', 'Loop.Begin', 'Loop.Bars' , 'Loop.Bars' , 'Loop.Enable', 'Loop.Dupl'  , 'Loop.Show', 'Loop.Show'],
            ['Loop.Roll' , 'Loop.Roll' , 'Loop.Roll' , 'Loop.Roll' , 'Loop.Roll'  , 'Loop.Roll'  , 'Loop.Roll', 'Loop.Roll'],
            ['Loop.Roll' , 'Loop.Roll' , 'Loop.Roll' , 'Loop.Roll' , 'Loop.Roll'  , 'Loop.Roll'  , 'Loop.Roll', 'Loop.Roll'],
            ['Clip.Reset', 'Clip.Reset', 'Clip.Reset', 'Clip.Cmd'  , 'Clip.Cmd'   , 'Clip.Warp'  , 'Sess.Metr', 'Sess.Folw'],
            ['Clip.Play' , 'Clip.Stop' , 'Clip.Dupl' , 'Clip.Rew'  , 'Clip.Forw'  , 'Sess.Play'  , 'Sess.Stop', 'Sess.Rec' ],
        ]
        self.m_oButSize_1_8 = None
        self.m_oButSize_1_4 = None
        self.m_oButSize_1_2 = None
        self.m_oButSize_1   = None
        self.m_oButSize_2   = None
        self.m_oButSize_4   = None
        self.m_oButSize_8   = None
        self.m_oButSize_16  = None

        self.m_oButShiftDec = None
        self.m_oButShiftInc = None
        self.m_oButLpStaDiv = None
        self.m_oButLpStaMul = None
        self.m_oButLpMidDiv = None
        self.m_oButLpMidMul = None
        self.m_oButLpEndDiv = None
        self.m_oButLpEndMul = None

        self.m_oButBeginDec = None
        self.m_oButBeginInc = None
        self.m_oButBars_1   = None
        self.m_oButBars_2   = None
        self.m_oButLoopEnab = None
        self.m_oButLoopDupl = None
        self.m_oButEnvlShow = None
        self.m_oButLoopShow = None

        self.m_oButRoll_1_1 = None
        self.m_oButRoll_1_2 = None
        self.m_oButRoll_1_3 = None
        self.m_oButRoll_1_4 = None
        self.m_oButRoll_1_5 = None
        self.m_oButRoll_1_6 = None
        self.m_oButRoll_1_7 = None
        self.m_oButRoll_1_8 = None

        self.m_oButRoll_2_1 = None
        self.m_oButRoll_2_2 = None
        self.m_oButRoll_2_3 = None
        self.m_oButRoll_2_4 = None
        self.m_oButRoll_2_5 = None
        self.m_oButRoll_2_6 = None
        self.m_oButRoll_2_7 = None
        self.m_oButRoll_2_8 = None

        self.m_oButPitchRes = None
        self.m_oButDetunRes = None
        self.m_oButGainRes  = None
        self.m_oButClipCrop = None
        self.m_oButClipQuan = None
        self.m_oButClipWarp = None
        self.m_oButSessMetr = None
        self.m_oButSessFolw = None

        self.m_oButClipPlay = None
        self.m_oButClipStop = None
        self.m_oButClipDupl = None
        self.m_oButSessStop = None

    def disconnect(self):
        self.m_oMatrix       = None
        self.m_lSceneButtons = None
        self.m_lNavButtons   = None

        # remove track/scene/session parameters listeners here! (if any)

        # remove buttons listeners
        self._connect_ctl(self.m_oButSize_1_8, None, self._on_size_1_8_value)
        self._connect_ctl(self.m_oButSize_1_4, None, self._on_size_1_4_value)
        self._connect_ctl(self.m_oButSize_1_2, None, self._on_size_1_2_value)
        self._connect_ctl(self.m_oButSize_1  , None, self._on_size_1_value)
        self._connect_ctl(self.m_oButSize_2  , None, self._on_size_2_value)
        self._connect_ctl(self.m_oButSize_4  , None, self._on_size_4_value)
        self._connect_ctl(self.m_oButSize_8  , None, self._on_size_8_value)
        self._connect_ctl(self.m_oButSize_16 , None, self._on_size_16_value)

        self._connect_ctl(self.m_oButShiftDec, None, self._on_shift_dec_value)
        self._connect_ctl(self.m_oButShiftInc, None, self._on_shift_inc_value)
        self._connect_ctl(self.m_oButLpStaDiv, None, self._on_loop_sta_div_value)
        self._connect_ctl(self.m_oButLpStaMul, None, self._on_loop_sta_mul_value)
        self._connect_ctl(self.m_oButLpMidDiv, None, self._on_loop_mid_div_value)
        self._connect_ctl(self.m_oButLpMidMul, None, self._on_loop_mid_mul_value)
        self._connect_ctl(self.m_oButLpEndDiv, None, self._on_loop_end_div_value)
        self._connect_ctl(self.m_oButLpEndMul, None, self._on_loop_end_mul_value)

        self._connect_ctl(self.m_oButBeginDec, None, self._on_begin_dec_value)
        self._connect_ctl(self.m_oButBeginInc, None, self._on_begin_inc_value)
        self._connect_ctl(self.m_oButBars_1  , None, self._on_bars_1_value)
        self._connect_ctl(self.m_oButBars_2  , None, self._on_bars_2_value)
        self._connect_ctl(self.m_oButLoopEnab, None, self._on_loop_enab_value)
        self._connect_ctl(self.m_oButLoopDupl, None, self._on_loop_dupl_value)
        self._connect_ctl(self.m_oButEnvlShow, None, self._on_envl_show_value)
        self._connect_ctl(self.m_oButLoopShow, None, self._on_loop_show_value)

        self._connect_ctl(self.m_oButRoll_1_1, None, self._on_roll_1_1_value)
        self._connect_ctl(self.m_oButRoll_1_2, None, self._on_roll_1_2_value)
        self._connect_ctl(self.m_oButRoll_1_3, None, self._on_roll_1_3_value)
        self._connect_ctl(self.m_oButRoll_1_4, None, self._on_roll_1_4_value)
        self._connect_ctl(self.m_oButRoll_1_5, None, self._on_roll_1_5_value)
        self._connect_ctl(self.m_oButRoll_1_6, None, self._on_roll_1_6_value)
        self._connect_ctl(self.m_oButRoll_1_7, None, self._on_roll_1_7_value)
        self._connect_ctl(self.m_oButRoll_1_8, None, self._on_roll_1_8_value)

        self._connect_ctl(self.m_oButRoll_2_1, None, self._on_roll_2_1_value)
        self._connect_ctl(self.m_oButRoll_2_2, None, self._on_roll_2_2_value)
        self._connect_ctl(self.m_oButRoll_2_3, None, self._on_roll_2_3_value)
        self._connect_ctl(self.m_oButRoll_2_4, None, self._on_roll_2_4_value)
        self._connect_ctl(self.m_oButRoll_2_5, None, self._on_roll_2_5_value)
        self._connect_ctl(self.m_oButRoll_2_6, None, self._on_roll_2_6_value)
        self._connect_ctl(self.m_oButRoll_2_7, None, self._on_roll_2_7_value)
        self._connect_ctl(self.m_oButRoll_2_8, None, self._on_roll_2_8_value)

        self._connect_ctl(self.m_oButPitchRes, None, self._on_pitch_res_value)
        self._connect_ctl(self.m_oButDetunRes, None, self._on_detun_res_value)
        self._connect_ctl(self.m_oButGainRes , None, self._on_gain_res_value )
        self._connect_ctl(self.m_oButClipCrop, None, self._on_clip_crop_value)
        self._connect_ctl(self.m_oButClipQuan, None, self._on_clip_quan_value)
        self._connect_ctl(self.m_oButClipWarp, None, self._on_clip_warp_value)
        self._connect_ctl(self.m_oButSessMetr, None, self._on_sess_metr_value)
        self._connect_ctl(self.m_oButSessFolw, None, self._on_sess_folw_value)

        self._connect_ctl(self.m_oButClipPlay, None, self._on_clip_play_value)
        self._connect_ctl(self.m_oButClipStop, None, self._on_clip_stop_value)
        self._connect_ctl(self.m_oButClipDupl, None, self._on_clip_dupl_value)
        self._connect_ctl(self.m_oButSessStop, None, self._on_sess_stop_value)
        self.m_oTransp.set_seek_buttons (None, None)
        self.m_oTransp.set_play_button  (None)
        self.m_oTransp.set_record_button(None)

    def connect_controls(self, _nSubMode):
        # set skin and load the map of buttons
        aButMap = []
        if _nSubMode == 0:
            for nSceneIdx in range(self.m_oMatrix.height() - 1): # the last row is track select button
                aSceneButMap = []
                for nTrackIdx in range(self.m_oMatrix.width()):
                    oButton = self.m_oMatrix.get_button(nTrackIdx, nSceneIdx)
                    aSceneButMap.append(oButton)
                    if nSceneIdx < 7:
                        oButton.set_on_off_values("Tools.%s" % (self.m_aToolsSkin[nSceneIdx][nTrackIdx]))
                    else:
                        oButton.set_on_off_values("Tools.NotAvail")
                        oButton.turn_off()
                aButMap.append(aSceneButMap)

        #elif _nSubMode == 1:

        # connect controls
        self.setup_functions(aButMap, _nSubMode)

    def release_controls(self, _nSubMode):
        # load a map of empty buttons
        aButMap = []
        for nSceneIdx in range(self.m_oMatrix.height()):
            aSceneButMap = []
            for nTrackIdx in range(self.m_oMatrix.width()):
                aSceneButMap.append(None)
            aButMap.append(aSceneButMap)

        self.setup_functions(aButMap, _nSubMode)

    def setup_functions(self, _aButMap, _nSubMode):
        if (_nSubMode == 0): # Loop tools
            self.m_oButSize_1_8 = self._connect_ctl(self.m_oButSize_1_8, _aButMap[0][0], self._on_size_1_8_value, self.m_nSizeIdx == 0)
            self.m_oButSize_1_4 = self._connect_ctl(self.m_oButSize_1_4, _aButMap[0][1], self._on_size_1_4_value, self.m_nSizeIdx == 1)
            self.m_oButSize_1_2 = self._connect_ctl(self.m_oButSize_1_2, _aButMap[0][2], self._on_size_1_2_value, self.m_nSizeIdx == 2)
            self.m_oButSize_1   = self._connect_ctl(self.m_oButSize_1  , _aButMap[0][3], self._on_size_1_value  , self.m_nSizeIdx == 3)
            self.m_oButSize_2   = self._connect_ctl(self.m_oButSize_2  , _aButMap[0][4], self._on_size_2_value  , self.m_nSizeIdx == 4)
            self.m_oButSize_4   = self._connect_ctl(self.m_oButSize_4  , _aButMap[0][5], self._on_size_4_value  , self.m_nSizeIdx == 5)
            self.m_oButSize_8   = self._connect_ctl(self.m_oButSize_8  , _aButMap[0][6], self._on_size_8_value  , self.m_nSizeIdx == 6)
            self.m_oButSize_16  = self._connect_ctl(self.m_oButSize_16 , _aButMap[0][7], self._on_size_16_value , self.m_nSizeIdx == 7)

            self.m_oButShiftDec = self._connect_ctl(self.m_oButShiftDec, _aButMap[1][0], self._on_shift_dec_value,    True)
            self.m_oButShiftInc = self._connect_ctl(self.m_oButShiftInc, _aButMap[1][1], self._on_shift_inc_value,    True)
            self.m_oButLpStaDiv = self._connect_ctl(self.m_oButLpStaDiv, _aButMap[1][2], self._on_loop_sta_div_value, True)
            self.m_oButLpStaMul = self._connect_ctl(self.m_oButLpStaMul, _aButMap[1][3], self._on_loop_sta_mul_value, True)
            self.m_oButLpMidDiv = self._connect_ctl(self.m_oButLpMidDiv, _aButMap[1][4], self._on_loop_mid_div_value, True)
            self.m_oButLpMidMul = self._connect_ctl(self.m_oButLpMidMul, _aButMap[1][5], self._on_loop_mid_mul_value, True)
            self.m_oButLpEndDiv = self._connect_ctl(self.m_oButLpEndDiv, _aButMap[1][6], self._on_loop_end_div_value, True)
            self.m_oButLpEndMul = self._connect_ctl(self.m_oButLpEndMul, _aButMap[1][7], self._on_loop_end_mul_value, True)

            self.m_oButBeginDec = self._connect_ctl(self.m_oButBeginDec, _aButMap[2][0], self._on_begin_dec_value, True)
            self.m_oButBeginInc = self._connect_ctl(self.m_oButBeginInc, _aButMap[2][1], self._on_begin_inc_value, True)
            self.m_oButBars_1   = self._connect_ctl(self.m_oButBars_1  , _aButMap[2][2], self._on_bars_1_value   , True)
            self.m_oButBars_2   = self._connect_ctl(self.m_oButBars_2  , _aButMap[2][3], self._on_bars_2_value   , True)
            self.m_oButLoopEnab = self._connect_ctl(self.m_oButLoopEnab, _aButMap[2][4], self._on_loop_enab_value, True)
            self.m_oButLoopDupl = self._connect_ctl(self.m_oButLoopDupl, _aButMap[2][5], self._on_loop_dupl_value, True)
            self.m_oButEnvlShow = self._connect_ctl(self.m_oButEnvlShow, _aButMap[2][6], self._on_envl_show_value, True)
            self.m_oButLoopShow = self._connect_ctl(self.m_oButLoopShow, _aButMap[2][7], self._on_loop_show_value, True)

            self.m_oButRoll_1_1 = self._connect_ctl(self.m_oButRoll_1_1, _aButMap[3][0], self._on_roll_1_1_value, False)
            self.m_oButRoll_1_2 = self._connect_ctl(self.m_oButRoll_1_2, _aButMap[3][1], self._on_roll_1_2_value, False)
            self.m_oButRoll_1_3 = self._connect_ctl(self.m_oButRoll_1_3, _aButMap[3][2], self._on_roll_1_3_value, False)
            self.m_oButRoll_1_4 = self._connect_ctl(self.m_oButRoll_1_4, _aButMap[3][3], self._on_roll_1_4_value, False)
            self.m_oButRoll_1_5 = self._connect_ctl(self.m_oButRoll_1_5, _aButMap[3][4], self._on_roll_1_5_value, False)
            self.m_oButRoll_1_6 = self._connect_ctl(self.m_oButRoll_1_6, _aButMap[3][5], self._on_roll_1_6_value, False)
            self.m_oButRoll_1_7 = self._connect_ctl(self.m_oButRoll_1_7, _aButMap[3][6], self._on_roll_1_7_value, False)
            self.m_oButRoll_1_8 = self._connect_ctl(self.m_oButRoll_1_8, _aButMap[3][7], self._on_roll_1_8_value, False)

            self.m_oButRoll_2_1 = self._connect_ctl(self.m_oButRoll_2_1, _aButMap[4][0], self._on_roll_2_1_value, False)
            self.m_oButRoll_2_2 = self._connect_ctl(self.m_oButRoll_2_2, _aButMap[4][1], self._on_roll_2_2_value, False)
            self.m_oButRoll_2_3 = self._connect_ctl(self.m_oButRoll_2_3, _aButMap[4][2], self._on_roll_2_3_value, False)
            self.m_oButRoll_2_4 = self._connect_ctl(self.m_oButRoll_2_4, _aButMap[4][3], self._on_roll_2_4_value, False)
            self.m_oButRoll_2_5 = self._connect_ctl(self.m_oButRoll_2_5, _aButMap[4][4], self._on_roll_2_5_value, False)
            self.m_oButRoll_2_6 = self._connect_ctl(self.m_oButRoll_2_6, _aButMap[4][5], self._on_roll_2_6_value, False)
            self.m_oButRoll_2_7 = self._connect_ctl(self.m_oButRoll_2_7, _aButMap[4][6], self._on_roll_2_7_value, False)
            self.m_oButRoll_2_8 = self._connect_ctl(self.m_oButRoll_2_8, _aButMap[4][7], self._on_roll_2_8_value, False)

            self.m_oButPitchRes = self._connect_ctl(self.m_oButPitchRes, _aButMap[5][0], self._on_pitch_res_value, True)
            self.m_oButDetunRes = self._connect_ctl(self.m_oButDetunRes, _aButMap[5][1], self._on_detun_res_value, True)
            self.m_oButGainRes  = self._connect_ctl(self.m_oButGainRes , _aButMap[5][2], self._on_gain_res_value , True)
            self.m_oButClipCrop = self._connect_ctl(self.m_oButClipCrop, _aButMap[5][3], self._on_clip_crop_value, True)
            self.m_oButClipQuan = self._connect_ctl(self.m_oButClipQuan, _aButMap[5][4], self._on_clip_quan_value, True)
            self.m_oButClipWarp = self._connect_ctl(self.m_oButClipWarp, _aButMap[5][5], self._on_clip_warp_value, False)
            self.m_oButSessMetr = self._connect_ctl(self.m_oButSessMetr, _aButMap[5][6], self._on_sess_metr_value, False)
            self.m_oButSessFolw = self._connect_ctl(self.m_oButSessFolw, _aButMap[5][7], self._on_sess_folw_value, False)

            self.m_oButClipPlay = self._connect_ctl(self.m_oButClipPlay, _aButMap[6][0], self._on_clip_play_value, True)
            self.m_oButClipStop = self._connect_ctl(self.m_oButClipStop, _aButMap[6][1], self._on_clip_stop_value, True)
            self.m_oButClipDupl = self._connect_ctl(self.m_oButClipDupl, _aButMap[6][2], self._on_clip_dupl_value, True)
            self.m_oButSessStop = self._connect_ctl(self.m_oButSessStop, _aButMap[6][6], self._on_sess_stop_value, True)
            self.m_oTransp.set_seek_buttons (_aButMap[6][4], _aButMap[6][3])
            self.m_oTransp.set_play_button  (_aButMap[6][5])
            self.m_oTransp.set_record_button(_aButMap[6][7])

            if (self.m_oButSize_1_8 != None):
                self.update_size_index(127, self.m_nSizeIdx)
                self.update_stateful_controls()
                self.update_rolling_buttons(-1)
                _aButMap[6][3].turn_on()
                _aButMap[6][4].turn_on()
                _aButMap[6][5].turn_on()
                _aButMap[6][7].turn_on()

            self.m_nRollStart = 0.0
            self.m_nRollSpan  = 4.0

    # **************************************************************************

    def _connect_ctl(self, _oCurBut, _oNewBut, _fListener, _bOn = None):
        if (_oCurBut != _oNewBut):
            if (_oCurBut != None):
                _oCurBut.remove_value_listener(_fListener)
                _oCurBut.turn_off()
            if (_oNewBut != None):
                _oNewBut.add_value_listener(_fListener)
                if _bOn != None:
                    if _bOn == True:
                        _oNewBut.turn_on()
                    else:
                        _oNewBut.turn_off()
        return _oNewBut

    # **************************************************************************

    def _on_size_1_8_value(self, _nValue):
        assert (self.m_oButSize_1_8 != None)
        self.update_size_index(_nValue, 0)

    def _on_size_1_4_value(self, _nValue):
        assert (self.m_oButSize_1_4 != None)
        self.update_size_index(_nValue, 1)

    def _on_size_1_2_value(self, _nValue):
        assert (self.m_oButSize_1_2 != None)
        self.update_size_index(_nValue, 2)

    def _on_size_1_value(self, _nValue):
        assert (self.m_oButSize_1 != None)
        self.update_size_index(_nValue, 3)

    def _on_size_2_value(self, _nValue):
        assert (self.m_oButSize_2 != None)
        self.update_size_index(_nValue, 4)

    def _on_size_4_value(self, _nValue):
        assert (self.m_oButSize_4 != None)
        self.update_size_index(_nValue, 5)

    def _on_size_8_value(self, _nValue):
        assert (self.m_oButSize_8 != None)
        self.update_size_index(_nValue, 6)

    def _on_size_16_value(self, _nValue):
        assert (self.m_oButSize_16 != None)
        self.update_size_index(_nValue, 7)

    def update_size_index(self, _nValue, _nIdx):
        assert (_nValue in range(128))
        if (_nValue != 127): return

        self.m_nSizeIdx = _nIdx
        if _nIdx == 0: self.m_oButSize_1_8.turn_on()
        else:          self.m_oButSize_1_8.turn_off()
        if _nIdx == 1: self.m_oButSize_1_4.turn_on()
        else:          self.m_oButSize_1_4.turn_off()
        if _nIdx == 2: self.m_oButSize_1_2.turn_on()
        else:          self.m_oButSize_1_2.turn_off()
        if _nIdx == 3: self.m_oButSize_1.turn_on()
        else:          self.m_oButSize_1.turn_off()
        if _nIdx == 4: self.m_oButSize_2.turn_on()
        else:          self.m_oButSize_2.turn_off()
        if _nIdx == 5: self.m_oButSize_4.turn_on()
        else:          self.m_oButSize_4.turn_off()
        if _nIdx == 6: self.m_oButSize_8.turn_on()
        else:          self.m_oButSize_8.turn_off()
        if _nIdx == 7: self.m_oButSize_16.turn_on()
        else:          self.m_oButSize_16.turn_off()
        aSize = ["1/8 [beat]", "1/4 [beat]", "1/2 [beat]", "1 [beat]", "2 [beat]", "1 [bar]", "2 [bar]", "4 [bar]"]
        self.alert("> Size: %s" % (aSize[_nIdx]))

    # **************************************************************************

    def fetch_loop_vars(self, _oButton, _nValue):
        assert (_oButton != None)
        oClip = self.get_clip_or_none(_nValue)
        if (oClip == None): return (None, None, None, None, None)
        nLoopStart = oClip.loop_start
        nLoopEnd   = oClip.loop_end
        nLoopSpan  = nLoopEnd - nLoopStart
        nSize      = self.m_aSizes[self.m_nSizeIdx]
        return (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize)

    # **************************************************************************

    def _on_shift_dec_value(self, _nValue):
        (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars(self.m_oButShiftDec, _nValue)
        if (oClip == None): return
        oClip.loop_start = nLoopStart - nSize
        oClip.loop_end   = nLoopEnd   - nSize
        self.update_rolling_buttons(-1)

    def _on_shift_inc_value(self, _nValue):
        (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars(self.m_oButShiftInc, _nValue)
        if (oClip == None): return
        oClip.loop_end   = nLoopEnd   + nSize
        oClip.loop_start = nLoopStart + nSize
        self.update_rolling_buttons(-1)

    def _on_loop_sta_div_value(self, _nValue):
        (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars(self.m_oButLpStaDiv, _nValue)
        if (oClip == None): return
        oClip.loop_start = nLoopStart + (nLoopSpan / 2)
        self.update_rolling_buttons(-1)

    def _on_loop_sta_mul_value(self, _nValue):
        (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars(self.m_oButLpStaMul, _nValue)
        if (oClip == None): return
        oClip.loop_start = nLoopStart - nLoopSpan
        self.update_rolling_buttons(-1)

    def _on_loop_mid_div_value(self, _nValue):
        (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars(self.m_oButLpMidDiv, _nValue)
        if (oClip == None): return
        oClip.loop_start = nLoopStart + (nLoopSpan / 4)
        oClip.loop_end   = nLoopEnd   - (nLoopSpan / 4)
        self.update_rolling_buttons(-1)

    def _on_loop_mid_mul_value(self, _nValue):
        (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars(self.m_oButLpMidMul, _nValue)
        if (oClip == None): return
        oClip.loop_start = nLoopStart - (nLoopSpan / 2)
        oClip.loop_end   = nLoopEnd   + (nLoopSpan / 2)
        self.update_rolling_buttons(-1)

    def _on_loop_end_div_value(self, _nValue):
        (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars(self.m_oButLpEndDiv, _nValue)
        if (oClip == None): return
        oClip.loop_end = nLoopStart + (nLoopSpan / 2)
        self.update_rolling_buttons(-1)

    def _on_loop_end_mul_value(self, _nValue):
        (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars(self.m_oButLpEndMul, _nValue)
        if (oClip == None): return
        oClip.loop_end = nLoopStart + (nLoopSpan * 2)
        self.update_rolling_buttons(-1)

    # **************************************************************************

    def _on_begin_dec_value(self, _nValue):
        (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars(self.m_oButBeginDec, _nValue)
        if (oClip == None): return
        nStart = oClip.start_marker
        oClip.start_marker = nStart - nSize

    def _on_begin_inc_value(self, _nValue):
        (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars(self.m_oButBeginInc, _nValue)
        if (oClip == None): return
        nStart = oClip.start_marker
        if (nStart + nSize < nLoopEnd) and (nStart + nSize < oClip.end_marker):
            oClip.start_marker = nStart + nSize

    def _on_bars_1_value(self, _nValue):
        (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars(self.m_oButBars_1, _nValue)
        if (oClip == None): return
        oClip.loop_end    = nLoopStart + 4.0
        self.m_nRollStart = nLoopStart
        self.m_nRollSpan  = 4.0
        self.update_rolling_buttons(-1)

    def _on_bars_2_value(self, _nValue):
        (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars(self.m_oButBars_2, _nValue)
        if (oClip == None): return
        oClip.loop_end    = nLoopStart + 8.0
        self.m_nRollStart = nLoopStart
        self.m_nRollSpan  = 8.0
        self.update_rolling_buttons(-1)

    def _on_loop_enab_value(self, _nValue):
        assert (self.m_oButLoopEnab != None)
        oClip = self.get_clip_or_none(_nValue)
        if (oClip == None): return
        bLooping      = oClip.looping
        oClip.looping = not bLooping
        self.update_stateful_controls()

    def _on_loop_dupl_value(self, _nValue):
        assert (self.m_oButLoopDupl != None)
        oClip = self.get_clip_or_none(_nValue)
        if (oClip == None): return
        if (oClip.is_midi_clip):
            oClip.duplicate_loop()
        else:
            self.alert("> LOOP DUPLICATE NOT AVAILABLE in audio tracks!")
        self.update_rolling_buttons(-1)

    def _on_envl_show_value(self, _nValue):
        assert (self.m_oButEnvlShow != None)
        oClip = self.get_clip_or_none(_nValue)
        if (oClip == None): return
        oView = self.application().view
        oView.show_view('Detail')
        oView.focus_view('Detail')
        oView.show_view('Detail/Clip')
        oView.focus_view('Detail/Clip')
        oClip.view.show_envelope()

    def _on_loop_show_value(self, _nValue):
        assert (self.m_oButLoopShow != None)
        oClip = self.get_clip_or_none(_nValue)
        if (oClip == None): return
        oView = self.application().view
        oView.show_view('Detail')
        oView.focus_view('Detail')
        oView.show_view('Detail/Clip')
        oView.focus_view('Detail/Clip')
        oClip.view.hide_envelope()
        oClip.view.show_loop()

    # **************************************************************************

    def _on_roll_1_1_value(self, _nValue):
        assert (self.m_oButRoll_1_1 != None)
        self.handle_roll_value(_nValue, 0.0, 1.0, 0)

    def _on_roll_1_2_value(self, _nValue):
        assert (self.m_oButRoll_1_2 != None)
        self.handle_roll_value(_nValue, 1.0, 1.0, 1)

    def _on_roll_1_3_value(self, _nValue):
        assert (self.m_oButRoll_1_3 != None)
        self.handle_roll_value(_nValue, 2.0, 1.0, 2)

    def _on_roll_1_4_value(self, _nValue):
        assert (self.m_oButRoll_1_4 != None)
        self.handle_roll_value(_nValue, 3.0, 1.0, 3)

    def _on_roll_1_5_value(self, _nValue):
        assert (self.m_oButRoll_1_5 != None)
        self.handle_roll_value(_nValue, 4.0, 1.0, 4)

    def _on_roll_1_6_value(self, _nValue):
        assert (self.m_oButRoll_1_6 != None)
        self.handle_roll_value(_nValue, 5.0, 1.0, 5)

    def _on_roll_1_7_value(self, _nValue):
        assert (self.m_oButRoll_1_7 != None)
        self.handle_roll_value(_nValue, 6.0, 1.0, 6)

    def _on_roll_1_8_value(self, _nValue):
        assert (self.m_oButRoll_1_8 != None)
        self.handle_roll_value(_nValue, 7.0, 1.0, 7)

    def _on_roll_2_1_value(self, _nValue):
        assert (self.m_oButRoll_2_1 != None)
        self.handle_roll_value(_nValue, 0.0, 0.5, 8)

    def _on_roll_2_2_value(self, _nValue):
        assert (self.m_oButRoll_2_2 != None)
        self.handle_roll_value(_nValue, 0.5, 0.5, 9)

    def _on_roll_2_3_value(self, _nValue):
        assert (self.m_oButRoll_2_3 != None)
        self.handle_roll_value(_nValue, 1.0, 0.5, 10)

    def _on_roll_2_4_value(self, _nValue):
        assert (self.m_oButRoll_2_4 != None)
        self.handle_roll_value(_nValue, 1.5, 0.5, 11)

    def _on_roll_2_5_value(self, _nValue):
        assert (self.m_oButRoll_2_5 != None)
        self.handle_roll_value(_nValue, 2.0, 0.5, 12)

    def _on_roll_2_6_value(self, _nValue):
        assert (self.m_oButRoll_2_6 != None)
        self.handle_roll_value(_nValue, 2.5, 0.5, 13)

    def _on_roll_2_7_value(self, _nValue):
        assert (self.m_oButRoll_2_7 != None)
        self.handle_roll_value(_nValue, 3.0, 0.5, 14)

    def _on_roll_2_8_value(self, _nValue):
        assert (self.m_oButRoll_2_8 != None)
        self.handle_roll_value(_nValue, 3.5, 0.5, 15)

    def handle_roll_value(self, _nValue, _nOffset, _nSize, _nIdx):
        if (_nValue != 127): return
        oClip = self.get_clip_or_none(127)
        if (oClip == None): return
        if (self.m_nCurrRollIdx != _nIdx):
            nClipEnd = oClip.end_marker
            nLoopEnd = self.m_nRollStart + _nOffset + _nSize
            if nLoopEnd > nClipEnd: return
            oClip.loop_start = 0.0
            oClip.loop_end   = nLoopEnd
            oClip.loop_start = self.m_nRollStart + _nOffset
        else:
            # selecting the same roll button! return to normal loop
            oClip.loop_start = oClip.start_marker
            oClip.loop_end   = oClip.end_marker
            oClip.loop_start = self.m_nRollStart
            oClip.loop_end   = self.m_nRollStart + self.m_nRollSpan
            _nIdx = -1
        self.update_rolling_buttons(_nIdx)

    def update_rolling_buttons(self, _nIdx):
        self.m_nCurrRollIdx = _nIdx
        if _nIdx == 0:  self.m_oButRoll_1_1.turn_on()
        else:           self.m_oButRoll_1_1.turn_off()
        if _nIdx == 1:  self.m_oButRoll_1_2.turn_on()
        else:           self.m_oButRoll_1_2.turn_off()
        if _nIdx == 2:  self.m_oButRoll_1_3.turn_on()
        else:           self.m_oButRoll_1_3.turn_off()
        if _nIdx == 3:  self.m_oButRoll_1_4.turn_on()
        else:           self.m_oButRoll_1_4.turn_off()
        if _nIdx == 4:  self.m_oButRoll_1_5.turn_on()
        else:           self.m_oButRoll_1_5.turn_off()
        if _nIdx == 5:  self.m_oButRoll_1_6.turn_on()
        else:           self.m_oButRoll_1_6.turn_off()
        if _nIdx == 6:  self.m_oButRoll_1_7.turn_on()
        else:           self.m_oButRoll_1_7.turn_off()
        if _nIdx == 7:  self.m_oButRoll_1_8.turn_on()
        else:           self.m_oButRoll_1_8.turn_off()
        if _nIdx == 8:  self.m_oButRoll_2_1.turn_on()
        else:           self.m_oButRoll_2_1.turn_off()
        if _nIdx == 9:  self.m_oButRoll_2_2.turn_on()
        else:           self.m_oButRoll_2_2.turn_off()
        if _nIdx == 10: self.m_oButRoll_2_3.turn_on()
        else:           self.m_oButRoll_2_3.turn_off()
        if _nIdx == 11: self.m_oButRoll_2_4.turn_on()
        else:           self.m_oButRoll_2_4.turn_off()
        if _nIdx == 12: self.m_oButRoll_2_5.turn_on()
        else:           self.m_oButRoll_2_5.turn_off()
        if _nIdx == 13: self.m_oButRoll_2_6.turn_on()
        else:           self.m_oButRoll_2_6.turn_off()
        if _nIdx == 14: self.m_oButRoll_2_7.turn_on()
        else:           self.m_oButRoll_2_7.turn_off()
        if _nIdx == 15: self.m_oButRoll_2_8.turn_on()
        else:           self.m_oButRoll_2_8.turn_off()

        if (_nIdx < 0): return

        aSize = ["1 / 1", "2 / 1", "3 / 1", "4 / 1", "1 / 2", "2 / 2", "3 / 2", "4 / 2", "1.1 / 1", "1.2 / 1", "2.1 / 1", "2.2 / 1", "3.1 / 1", "3.2 / 1", "4.1 / 1", "4.2 / 1"]
        self.alert("> Roll: %s" % (aSize[_nIdx]))

    # **************************************************************************

    def _on_pitch_res_value(self, _nValue):
        oClip = self.get_clip_or_none(_nValue)
        if oClip == None: return
        if not oClip.is_midi_clip:
            oClip.pitch_coarse = 0
        else:
            self.alert('> No PITCH in midi files')

    def _on_detun_res_value(self, _nValue):
        oClip = self.get_clip_or_none(_nValue)
        if oClip == None: return
        if not oClip.is_midi_clip:
            oClip.pitch_fine = 0
        else:
            self.alert('> No DETUNE in midi files')

    def _on_gain_res_value (self, _nValue):
        oClip = self.get_clip_or_none(_nValue)
        if oClip == None: return
        if not oClip.is_midi_clip:
            oClip.gain = 0.40 #float(_nValue) / 127.0
        else:
            self.alert('> No GAIN in midi files')

    def _on_clip_crop_value(self, _nValue):
        oClip = self.get_clip_or_none(_nValue)
        if oClip == None: return
        if oClip.is_midi_clip:
            oClip.crop()
        else:
            self.alert('> No CROP in audio files')

    def _on_clip_quan_value(self, _nValue):
        oClip = self.get_clip_or_none(_nValue)
        if oClip == None: return
        oClip.quantize(1, 0)

    def _on_clip_warp_value(self, _nValue):
        oClip = self.get_clip_or_none(_nValue)
        if oClip == None: return
        if oClip.is_midi_clip:
            self.alert('> No WARP in midi files')
            return
        bWarping      = oClip.warping
        oClip.warping = not bWarping
        self.update_stateful_controls()

    def _on_sess_metr_value(self, _nValue):
        if (_nValue != 127): return
        bMetronome = self.song().metronome
        self.song().metronome = not bMetronome
        self.update_stateful_controls()

    def _on_sess_folw_value(self, _nValue):
        if (_nValue != 127): return
        bFollowing = self.song().view.follow_song
        self.song().view.follow_song = not bFollowing
        self.update_stateful_controls()

    def _on_clip_stop_value(self, _nValue):
        oClipSlot = self.get_clip_slot_or_none(_nValue)
        if (oClipSlot == None): return
        oClipSlot.stop()

    def _on_clip_play_value(self, _nValue):
        oClipSlot = self.get_clip_slot_or_none(_nValue)
        if (oClipSlot == None): return
        oClipSlot.fire()

    def _on_clip_dupl_value(self, _nValue):
        oClipSlot = self.get_clip_slot_or_none(_nValue)
        if (oClipSlot == None):
            return
        nSelSceneIdxAbs = self.sel_scene_idx_abs()
        oSelTrack = self.sel_track()
        oSelTrack.duplicate_clip_slot(nSelSceneIdxAbs)
        self.alert('> DUPLICATED CLIP at track "%s", scene: %d' % (oSelTrack.name, nSelSceneIdxAbs))

    def _on_sess_stop_value(self, _nValue):
        if (_nValue != 127): return
        self.song().stop_all_clips()
        self.song().stop_playing()

    # **************************************************************************

    def _on_sel_scene_changed(self):
        self.update_stateful_controls()

    def _on_sel_track_changed(self):
        self.update_stateful_controls()

    def update_stateful_controls(self):
        if (self.is_enabled() == False): return
        if (self.m_oButLoopEnab == None): return

        bLooping = False
        bWarping = False

        oClip = self.get_clip_or_none(127)
        if (oClip != None):
            bLooping = oClip.looping
            if (oClip.is_audio_clip):
                bWarping = oClip.warping

        bMetronome = self.song().metronome
        bFollowing = self.song().view.follow_song

        if bLooping:   self.m_oButLoopEnab.turn_on()
        else:          self.m_oButLoopEnab.turn_off()
        if bWarping:   self.m_oButClipWarp.turn_on()
        else:          self.m_oButClipWarp.turn_off()
        if bMetronome: self.m_oButSessMetr.turn_on()
        else:          self.m_oButSessMetr.turn_off()
        if bFollowing: self.m_oButSessFolw.turn_on()
        else:          self.m_oButSessFolw.turn_off()

    # ****************************************************************

    def sel_scene_idx_abs(self):
        aAllScenes = self.scenes()
        oSelScene  = self.sel_scene()
        return list(aAllScenes).index(oSelScene)

    def scenes(self):
        return self.song().scenes

    def sel_scene(self):
        return self.song().view.selected_scene

    def sel_track(self):
        return self.song().view.selected_track

    def get_clip_slot_or_none(self, _nValue):
        assert (_nValue in range(128))
        if (_nValue != 127): return None
        oClipSlot = self.sel_clip_slot()
        return oClipSlot

    def get_clip_or_none(self, _nValue):
        assert (_nValue in range(128))
        if (_nValue != 127): return None
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot == None): return None
        oClip = oClipSlot.clip
        return oClip

    def sel_clip_slot(self):
        return self.song().view.highlighted_clip_slot

    def alert(self, _sMessage):
        self.m_oCtrlInst.show_message(_sMessage)

