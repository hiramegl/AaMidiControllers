import Live

from _Framework.CompoundComponent import CompoundComponent
from _Framework.SubjectSlot import subject_slot

BUTTON_ON = 127

LEN_ONE_BAR    = 4
LEN_ONE_PHRASE = 16
LEN_ONE_OCT    = 12

SEQ_PITX_SHIFT_CHROM = 4

SEQ_INST_MODE_UNDEFINED = 0
SEQ_INST_MODE_PRIMARY   = 0
SEQ_INST_MODE_SECONDARY = 1

SEQ_SUBMODE_UNDEFINED = -1
SEQ_SUBMODE_NOTES     = 0
SEQ_SUBMODE_ZOOM      = 1
SEQ_SUBMODE_TOOLS     = 2
SEQ_SUBMODE_RHYTHM    = 3

SEQ_INIT_OCTAVE = 1

SEQ_CLIP_STATE_UNDEFINED = 0
SEQ_CLIP_STATE_INVALID   = 1
SEQ_CLIP_STATE_EMPTY     = 2
SEQ_CLIP_STATE_READY     = 3

SEQ_TIME_ZOOM_BAR    = 0 #  4 beat = 1 bar             (in 2 surfaces)
SEQ_TIME_ZOOM_PHRASE = 1 # 16 beat = 4 bars = 1 phrase (in 2 surfaces)

SEQ_SCALE_UNDEF     = -1
SEQ_SCALE_CHROMATIC = 0

SEQ_ROOT_C = 0

SEQ_LOOP_CMD_STA_DEC = 0
SEQ_LOOP_CMD_STA_INC = 1
SEQ_LOOP_CMD_MID_DEC = 2
SEQ_LOOP_CMD_MID_INC = 3
SEQ_LOOP_CMD_END_DEC = 4
SEQ_LOOP_CMD_END_INC = 5

SEQ_SLIDER_MODE_VELOCITY = 0
SEQ_SLIDER_MODE_LENGTH   = 1
SEQ_SLIDER_MODE_SHIFT    = 2
SEQ_SLIDER_MODE_NONE     = 3

SEQ_SECTION_MODE_1_2 = 0
SEQ_SECTION_MODE_1   = 1
SEQ_SECTION_MODE_2   = 2
SEQ_SECTION_MODE_4   = 3
SEQ_SECTION_MODE_8   = 4

SEQ_BUT_IDX_NOTE_CMDS  = 5
SEQ_BUT_IDX_SLIDR_MODE = 6
SEQ_BUT_IDX_SECT_MODE  = 6
SEQ_BUT_IDX_SECTIONS   = 7

SEQ_NOTE_CMD_TRANS    = 0
SEQ_NOTE_CMD_MUTE     = 1
SEQ_NOTE_CMD_SOLO     = 2
SEQ_NOTE_CMD_SHIFT_DW = 3
SEQ_NOTE_CMD_SHIFT_UP = 4
SEQ_NOTE_CMD_SHIFT_LF = 5
SEQ_NOTE_CMD_SHIFT_RG = 6
SEQ_NOTE_CMD_LP_DUPL  = 7
SEQ_NOTE_CMD_VEL_RST  = 8

SEQ_TRANS_UNAV    = 0
SEQ_TRANS_STANDBY = 1
SEQ_TRANS_AWAIT   = 2

SEQ_BUT_IDX_SHIFT_SIZE = 0
SEQ_BUT_IDX_SHIFT_CMD  = 1
SEQ_BUT_IDX_RHYTHM_CMD = 2
SEQ_BUT_IDX_NOTE_1_CMD = 3
SEQ_BUT_IDX_NOTE_2_CMD = 4
SEQ_BUT_IDX_NOTE_3_CMD = 5
SEQ_BUT_IDX_CMDS       = 6

SEQ_NOTE_CMD_MODE_LEN  = 0
SEQ_NOTE_CMD_MODE_CHOP = 1
SEQ_BUT_IDX_NOTE_1_CMD_ROW_1 = 1
SEQ_BUT_IDX_NOTE_1_CMD_ROW_2 = 2

SEQ_SHF_CMD_SONG_STA_DEC = 0
SEQ_SHF_CMD_SONG_STA_INC = 1
SEQ_SHF_CMD_SONG_END_DEC = 2
SEQ_SHF_CMD_SONG_END_INC = 3
SEQ_SHF_CMD_LOOP_STA_DEC = 4
SEQ_SHF_CMD_LOOP_STA_INC = 5
SEQ_SHF_CMD_LOOP_END_DEC = 6
SEQ_SHF_CMD_LOOP_END_INC = 7

SEQ_RHYTHM_NOTE_MODE    = 0
SEQ_RHYTHM_NOTE_CHOP_2  = 1
SEQ_RHYTHM_NOTE_DIV     = 2
SEQ_RHYTHM_NOTE_MUL     = 3
SEQ_RHYTHM_NOTE_SEL_ALL = 4
SEQ_RHYTHM_NOTE_DEL_SEL = 5
SEQ_RHYTHM_NOTE_CLEAR   = 6
SEQ_RHYTHM_LOOP_SHOW    = 7
SEQ_RHYTHM_NOTE_CHOP_3  = 8

BIT_CHORD_TRIAD = 0
BIT_CHORD_AUGM  = 1
BIT_CHORD_POW_5 = 2
BIT_CHORD_NONE  = 3

BIT_CHORD_INV_0 = 0
BIT_CHORD_INV_1 = 1
BIT_CHORD_INV_2 = 2

class SequencerComponent(CompoundComponent):

    def __init__(self, _oCtrlInst, _oMatrix, _lSceneButtons, _lNavButtons, _lTrackSliders):
        self.m_oCtrlInst = _oCtrlInst
        super(SequencerComponent, self).__init__()

        self.m_oMatrix       = _oMatrix
        self.m_nHeight       = _oMatrix.height()
        self.m_nWidth        = _oMatrix.width()
        self.m_rHeight       = range(self.m_nHeight)
        self.m_rWidth        = range(self.m_nWidth)
        self.m_aSceneButtons = _lSceneButtons
        self.m_aNavButtons   = _lNavButtons
        self.m_aTrackSliders = _lTrackSliders[:8]
        self.m_oMasterSlider = _lTrackSliders[8:][0]
        self.m_aToolsSkin    = [
            ['Octv' , 'Octv' , 'Scale', 'Scale', 'Scale', 'Scale', 'Scale', 'Scale'],
            ['Octv' , 'Octv' , 'Scale', 'Scale', 'Scale', 'Scale', 'Scale', 'Scale'],
            ['Octv' , 'Octv' , 'Root' , 'Root' , 'Root' , 'Root' , 'Root' , 'Root' ],
            ['Octv' , 'Octv' , 'Root' , 'Root' , 'Root' , 'Root' , 'Root' , 'Root' ],
            ['Octv' , 'Octv' , 'LpSta', 'LpSta', 'LpMid', 'LpMid', 'LpEnd', 'LpEnd'],
            ['Trans', 'Cmd'  , 'Cmd'  , 'Shift', 'Shift', 'Shift', 'Shift', 'LpDup'],
            ['SlMod', 'SlMod', 'SlMod', 'Span' , 'Span' , 'Span' , 'Span' , 'Span' ],
            ['Sect' , 'Sect' , 'Sect' , 'Sect' , 'Sect' , 'Sect' , 'Sect' , 'Sect' ],
        ]
        self.m_aRhythmSkin   = [
            ['ShiftSize', 'ShiftSize', 'ShiftSize', 'ShiftSize', 'ShiftSize', 'ShiftSize', 'ShiftSize', 'ShiftSize'],
            ['SongStart', 'SongStart', 'SongEnd'  , 'SongEnd'  , 'LoopStart', 'LoopStart', 'LoopEnd'  , 'LoopEnd'  ],
            ['Rhythm'   , 'Rhythm'   , 'Rhythm'   , 'Rhythm'   , 'Rhythm'   , 'Rhythm'   , 'Rhythm'   , 'Rhythm'   ],
            ['NoteCmd'  , 'NoteCmd'  , 'NoteCmd'  , 'NoteCmd'  , 'NoteCmd'  , 'NoteCmd'  , 'NoteCmd'  , 'NoteCmd'  ],
            ['NoteCmd'  , 'NoteCmd'  , 'NoteCmd'  , 'NoteCmd'  , 'NoteCmd'  , 'NoteCmd'  , 'NoteCmd'  , 'NoteCmd'  ],
            ['CmdMode'  , 'Chop'     , 'Command'  , 'Command'  , 'SelectAll', 'DeleteSel', 'Clear'    , 'LoopShow' ],
            ['PeerNavSy', 'PeerPrim' , 'ZoomMode' , 'Span'     , 'Span'     , 'Span'     , 'Span'     , 'Span'     ],
            ['Sect'     , 'Sect'     , 'Sect'     , 'Sect'     , 'Sect'     , 'Sect'     , 'Sect'     , 'Sect'     ],
        ]
        self.m_aInvalidPattern = [ # for audio clips
           [1, 0, 0, 0, 0, 0, 0, 1],
           [0, 1, 0, 0, 0, 0, 1, 0],
           [0, 0, 1, 0, 0, 1, 0, 0],
           [0, 0, 0, 1, 1, 0, 0, 0],
           [0, 0, 0, 1, 1, 0, 0, 0],
           [0, 0, 1, 0, 0, 1, 0, 0],
           [0, 1, 0, 0, 0, 0, 1, 0],
           [1, 0, 0, 0, 0, 0, 0, 1],
        ]
        self.m_aEmptyPattern = [ # for empty midi clips
           [0, 0, 0, 1, 1, 0, 0, 0],
           [0, 0, 0, 1, 1, 0, 0, 0],
           [0, 0, 0, 1, 1, 0, 0, 0],
           [1, 1, 1, 1, 1, 1, 1, 1],
           [1, 1, 1, 1, 1, 1, 1, 1],
           [0, 0, 0, 1, 1, 0, 0, 0],
           [0, 0, 0, 1, 1, 0, 0, 0],
           [0, 0, 0, 1, 1, 0, 0, 0],
        ]
        self.m_aRhythmPatterns = [
           ['House'    , 0.25, [0.0, 1.0 , 2.0, 3.0]],
           ['Zouk'     , 0.25, [0.0, 0.75, 1.5, 2.0, 2.75, 3.5]],
           ['Reaggeton', 0.25, [0.0, 0.75, 1.0, 1.5, 2.0, 2.75, 3.0, 3.5]],
           ['Salsa'    , 0.25, [0.0, 0.75, 1.5, 2.5, 3.0]],
           ['Reagge'   , 0.25, [0.5, 1.5 , 2.5, 3.5]],
           ['Triplet'  , 0.33, [0.0, 0.33, 0.66, 1.0, 1.33, 1.66, 2.0, 2.33, 2.66, 3.0, 3.33, 3.66]],
           ['Fill All' , 0.25, [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75]],
           ['FiveFour' , 0.20, [0.0, 0.8, 1.6, 2.4, 3.2]],
        ]
        self.m_bEnabled      = False
        self.m_oPeer         = None
        self.m_oAaMatrix     = None
        self.m_nPeerMode     = SEQ_INST_MODE_UNDEFINED
        self.m_oClip         = None
        self.m_oTrack        = None
        self.m_oMidiSlot     = None
        self.m_aAddClipCtls  = []
        self.m_nSubMode      = SEQ_SUBMODE_UNDEFINED
        self.m_nClipState    = SEQ_CLIP_STATE_UNDEFINED
        self.m_nNoteCmdMode  = SEQ_NOTE_CMD_MODE_LEN
        self.m_nNoteVelocity = 127  # Full velocity
        self.m_nNoteLength   = 0.25 # 1 BIT = 1/4 BEAT
        self.m_nNoteShift    = 0.0  # Fine time shift 0/16 .. 15/16 of a BIT (0.0625 increments)
        self.m_nChordType    = BIT_CHORD_NONE
        self.m_nChordInv     = BIT_CHORD_INV_0
        self.m_nTimeZoomMode = SEQ_TIME_ZOOM_BAR
        self.m_nPitxOffAbs   = self.get_pitx_offset_abs_for_octave(SEQ_INIT_OCTAVE) # initial octave
        self.m_nTimeOffAbs   = 0 # Beat mode: 0, 2, 4, 6, 8, 10, 12, 14 / Bar mode: 0, 8
        self.m_nScale        = SEQ_SCALE_CHROMATIC
        self.m_nRootPitx     = SEQ_ROOT_C
        self.m_nRootBkup     = SEQ_ROOT_C
        self.m_nSliderMode   = SEQ_SLIDER_MODE_NONE
        self.m_aSliderModes  = ['VELOCITY', 'LENGTH', 'FINE SHIFT', 'NONE']
        self.m_nSectionMode  = SEQ_SECTION_MODE_1 # Synchronize this with the Selector's m_nSectionMode of AaMatrix
        self.m_aSectionModes = ['1/2', '1', '2', '4', '8']
        self.m_aSectionFactr = [  0.5,  1 ,  2 ,  4 ,  8 ]
        self.m_hSelectedPitx = {} # selected note pitches chromatic cache (midi value of selected notes, can contain notes outside the scale!)
        self.m_aNoteChrCache = [] # active   note pitches chromatic cache (mirror of ableton midi clip, can contain notes outside the scale!)
        self.m_aScales       = [
            ['CHROMATIC'            , [0]],                        # NEVER USED ACTUALLY
            ['IONIAN NATURAL MAJOR' , [0, 2, 4, 5, 7, 9, 11, 12]],
            ['IONIAN NATURAL MINOR' , [0, 2, 3, 5, 7, 8, 10, 12]],
            ['IONIAN HARMONIC MAJOR', [0, 2, 4, 5, 7, 8, 11, 12]],
            ['IONIAN HARMONIC MINOR', [0, 2, 3, 5, 7, 8, 11, 12]], # (ONLY WHEN GOING UPWARDS)
            ['IONIAN MELODIC MAJOR' , [0, 2, 4, 5, 7, 8, 10, 12]],
            ['IONIAN MELODIC MINOR' , [0, 2, 3, 5, 7, 9, 11, 12]], # (ONLY WHEN GOING UPWARDS)
            ['DORIAN',                [0, 2, 3, 5, 7, 9, 10, 12]],
            ['PHRYGIAN',              [0, 1, 3, 5, 7, 8, 10, 12]],
            ['LYDIAN',                [0, 2, 4, 6, 7, 9, 11, 12]],
            ['MYXOLYDIAN',            [0, 2, 4, 5, 7, 9, 10, 12]],
            ['AEOLIAN',               [0, 2, 3, 5, 7, 8, 10, 12]],
            ['LOCRIAN',               [0, 1, 3, 5, 6, 8, 10, 12]],
        ]
        self.m_hActiveButtons = {} # used to know if the bit buttons are toggled on or off
        self.m_aSizes         = [0.125, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0] # in beats
        self.m_nSizeIdx       = 3 # default size = 1 beat [1/8, 1/4, 1/2, 1, 2, 4, 8, 16]
        self.m_nNumSect       = 0    # number of sections to show
        self.m_nCurSect       = 0    # current section
        self.m_nSpnSect       = 0    # section span (depends on the section mode)
        self.m_oNavSyncBut    = None
        self.m_bNavSync       = True
        self.m_oPeerModeBut   = None
        self.m_oZoomModeBut   = None
        self.m_aLenFactors    = [0.125, 0.25, 0.32, 0.5, 0.65, 0.75, 1.00, 1.15, 1.25, 1.32, 1.50, 1.66, 1.75, 1.80, 1.85, 1.90]
        self.m_aShfFactors    = [0.000, 0.05, 0.10, 0.2, 0.25, 0.30, 0.33, 0.40, 0.50, 0.60, 0.67, 0.70, 0.75, 0.80, 0.90, 0.95]
        self.m_nTransState    = SEQ_TRANS_UNAV
        self.m_nTransScale    = SEQ_SCALE_UNDEF
        self.setup_peer_ref()

    def disconnect(self):
        self.release_seq_controls()
        self.m_oMatrix       = None
        self.m_aSceneButtons = None
        self.m_aNavButtons   = None
        self.m_aTrackSliders = None
        self.m_oMasterSlider = None
        self.m_bEnabled      = False
        self.m_oClip         = None
        self.m_oTrack        = None
        self.m_oMidiSlot     = None
        self.m_oNavSyncBut   = None
        self.m_oPeerModeBut  = None
        self.m_oZoomModeBut  = None
        self.m_nClipState    = SEQ_CLIP_STATE_UNDEFINED

    # **************************************************************************

    def connect_controls(self, _nSubMode):
        self.release_seq_controls()

        # refresh state variables
        self.m_bEnabled   = True
        self.m_nClipState = self.get_clip_state()
        self.m_nSubMode   = _nSubMode

        if self.m_nClipState == SEQ_CLIP_STATE_INVALID:
            self.disconnect_note_selection_buttons()
            self.disconnect_note_navigation_buttons()
            self.setup_invalid_clip_buttons()
        elif self.m_nClipState == SEQ_CLIP_STATE_EMPTY:
            self.disconnect_note_selection_buttons()
            self.disconnect_note_navigation_buttons()
            self.setup_empty_clip_buttons()
        elif self.m_nClipState == SEQ_CLIP_STATE_READY:
            self.compute_section_values()
            #self.focus_clip_view()
            self.setup_note_navigation_buttons()
            self.setup_track_sliders()
            if self.m_nSubMode == SEQ_SUBMODE_NOTES:
                self.setup_notes_buttons()
                self.setup_note_selection_buttons()
            elif self.m_nSubMode == SEQ_SUBMODE_ZOOM:
                self.setup_zoom_buttons()
                self.setup_note_selection_zoom_buttons()
            elif self.m_nSubMode == SEQ_SUBMODE_TOOLS:
                self.setup_tools_buttons()
                self.setup_note_selection_buttons()
            elif self.m_nSubMode == SEQ_SUBMODE_RHYTHM:
                self.setup_rhythm_buttons()
                self.setup_note_selection_buttons()

    def release_seq_controls(self):
        self.disconnect_clip_listeners()

        if self.m_nClipState == SEQ_CLIP_STATE_EMPTY:
            self.disconnect_empty_clip_buttons()
        elif self.m_nClipState == SEQ_CLIP_STATE_READY:
            self.disconnect_note_navigation_buttons()
            self.disconnect_track_sliders()
            if self.m_nSubMode == SEQ_SUBMODE_NOTES:
                self.disconnect_notes_buttons()
                self.disconnect_note_selection_buttons()
            elif self.m_nSubMode == SEQ_SUBMODE_ZOOM:
                self.disconnect_zoom_buttons()
                self.disconnect_note_selection_zoom_buttons()
            elif self.m_nSubMode == SEQ_SUBMODE_TOOLS:
                self.disconnect_tools_buttons()
                self.disconnect_note_selection_buttons()
            elif self.m_nSubMode == SEQ_SUBMODE_RHYTHM:
                self.disconnect_rhythm_buttons()
                self.disconnect_note_selection_buttons()
        self.m_bEnabled = False

    # **************************************************************************

    def setup_peer_ref(self):
        if self.m_oPeer != None: return # peer already found! nothing else to do here!

        self.m_sMyName = self.m_oCtrlInst.__class__.__name__
        self.m_nMyId   = self.m_oCtrlInst.instance_identifier()
        self.log('> Current instance: %s / %d' % (self.m_sMyName, self.m_nMyId))

        aCtrlInsts = Live.Application.get_application().control_surfaces
        aPeerInst  = []
        for oCtrlInst in aCtrlInsts:
            if oCtrlInst == None: continue
            sCtrlName = oCtrlInst.__class__.__name__
            nCtrlId   = oCtrlInst.instance_identifier()
            if sCtrlName == self.m_sMyName and nCtrlId != self.m_nMyId:
                aPeerInst.append({ 'id': nCtrlId, 'ctrl': oCtrlInst })

        if len(aPeerInst) > 0:
            hPeerInst = aPeerInst[0]
            self.log('> Peer found: %s / %d' % (self.m_sMyName, hPeerInst['id']))
            if (self.m_nMyId < hPeerInst['id']):
               self.setup_as_primary_instance(hPeerInst['ctrl'])
               self.m_oPeer.setup_as_secondary_instance(self.m_oCtrlInst)
            else:
               self.setup_as_secondary_instance(hPeerInst['ctrl'])
               self.m_oPeer.setup_as_primary_instance(self.m_oCtrlInst)
        else:
            self.log('> No peer controller found for %s!' % (self.m_sMyName))

    def setup_as_primary_instance(self, _oSecPeer):
        self.setup_instance_mode(SEQ_INST_MODE_PRIMARY, _oSecPeer)

    def setup_as_secondary_instance(self, _oPrimPeer):
        self.setup_instance_mode(SEQ_INST_MODE_SECONDARY, _oPrimPeer)

    def setup_instance_mode(self, _nMode, _oPeer):
        self.m_nPeerMode = _nMode
        self.m_oPeer     = _oPeer
        self.m_sMyName   = self.m_oCtrlInst.__class__.__name__
        self.m_nMyId     = self.m_oCtrlInst.instance_identifier()
        aModeName        = ['Primary', 'Secondary']
        self.log('> %s / %d -> %s surface' % (self.m_sMyName, self.m_nMyId, aModeName[self.m_nPeerMode]))

    def send_peer_command(self, _sCmd, _hParams = None):
        if self.m_oPeer != None:
            _hParams = {} if _hParams == None else _hParams
            _hParams['cmd']     = _sCmd
            _hParams['peer_id'] = self.m_nMyId
            _hParams['peer_md'] = self.m_nPeerMode
            self.m_oPeer.receive_peer_command(_hParams)

    def receive_peer_command(self, _hParams):
        sCmd = _hParams['cmd']

        if sCmd == 'note_nav':
            self.note_navigate(_hParams['dir'], False)
        elif sCmd == 'zoom_nav':
            self.zoom_navigate(_hParams['octave_index'], _hParams['time_index'], False)
        elif sCmd == 'oct_nav':
            self.octave_navigate(_hParams['pitx_off_abs'], False)
        elif sCmd == 'note_sel':
            self.select_note(_hParams['pitch_index_rel'], False)
        elif sCmd == 'note_sel_zoom':
            self.select_note_zoom(_hParams['pitch_zoom_index_rel'], False)
        elif sCmd == 'sel_scale':
            self.select_scale(_hParams['scale_idx'], False)
        elif sCmd == 'sel_root':
            self.select_root(_hParams['root_idx'], False)
        elif sCmd == 'slider_mode':
            self.change_slider_mode(_hParams['slider_mode_index'], False)
        elif sCmd == 'sect_nav':
            self.section_navigate(_hParams['section_index'], False)
        elif sCmd == 'change_note_sel':
            self.change_note_selection(_hParams['select_all'], False)
        elif sCmd == 'change_rhythm_note_cmd_mode':
            self.change_rhythm_note_cmd_mode(_hParams['new_note_cmd_mode'], False)
        elif sCmd == 'nav_sync':
            self.nav_sync_toggle(_hParams['nav_sync_val'], _hParams['pitx_off_abs'], _hParams['time_off_abs'], False)
        elif sCmd == 'peer_mode':
            self.peer_mode_toggle(_hParams['new_peer_mode'], False)
        elif sCmd == 'zoom_mode':
            self.zoom_mode_toggle(_hParams['new_zoom_mode'], False)

    # **************************************************************************

    def setup_matrix_ref(self):
        if self.m_oAaMatrix != None: return

        aCtrlInsts = Live.Application.get_application().control_surfaces
        for oCtrlInst in aCtrlInsts:
            if oCtrlInst == None: continue
            sCtrlName = oCtrlInst.__class__.__name__
            nCtrlId   = oCtrlInst.instance_identifier()
            if sCtrlName == "AaMatrix":
                self.m_oAaMatrix = oCtrlInst
                self.log('> AaMatrix controller found: %s / %d' % (sCtrlName, nCtrlId))

    def send_matrix_command(self, _sCmd, _hParams = None):
        self.setup_matrix_ref()
        _hParams = {} if _hParams == None else _hParams
        _hParams['cmd']     = _sCmd
        _hParams['grid_id'] = self.m_nMyId
        self.m_oAaMatrix.receive_grid_command(_hParams)

    def receive_matrix_command(self, _hParams):
        sCmd = _hParams['cmd']
        if sCmd == 'section_mode':
            self.section_mode(_hParams['section_mode_index'], False)
        elif sCmd == 'zoom_mode':
            self.zoom_mode_toggle(_hParams['new_zoom_mode'], False)
        elif sCmd == 'zoom_nav':
            self.zoom_navigate(_hParams['octave_index'], _hParams['time_index'], False)
        elif sCmd == 'sel_scale':
            self.select_scale(_hParams['scale_idx'], False)
        elif sCmd == 'sel_root':
            self.select_root(_hParams['root_idx'], False)
        elif sCmd == 'slider_mode':
            self.change_slider_mode(_hParams['slider_mode_index'], False)
        elif sCmd == 'select_toggle':
            bDeselectAll = len(self.m_hSelectedPitx) > 0
            self.change_note_selection(not bDeselectAll, False)
        elif sCmd == 'grid_cmd':
            self.handle_grid_cmd(_hParams)
        elif sCmd == 'bit_cmd':
            self.handle_bit_cmd(_hParams)
        elif sCmd == 'bit_cfg':
            self.handle_bit_cfg(_hParams)
        else:
            if self.m_nPeerMode != SEQ_INST_MODE_PRIMARY: return
            if sCmd == 'transpose_scale':
                self.on_transpose_cmd(_hParams)
            elif sCmd == 'apply_rhythm':
                self.apply_rhythm_pattern(_hParams['pattern_index'])

    def handle_grid_cmd(self, _hParams):
        nGridIdx = 1 if self.m_nPeerMode == SEQ_INST_MODE_PRIMARY else 2
        if _hParams['grid'] != nGridIdx: return
        sSubCmd  = _hParams['subcmd']
        bSelMode = (_hParams['mode'] == 'sel') # apply on selected note pitches only
        bAllMode = (_hParams['mode'] == 'all') # apply on all note pitches!
        (nTimeMinAbs, nTimeMaxAbs) = self.get_master_time_vars()
        if sSubCmd == 'mul':
            self.apply_note_cmd(SEQ_RHYTHM_NOTE_MUL, nTimeMinAbs, nTimeMaxAbs, bSelMode)
        elif sSubCmd == 'div':
            self.apply_note_cmd(SEQ_RHYTHM_NOTE_DIV, nTimeMinAbs, nTimeMaxAbs, bSelMode)
        elif sSubCmd == 'chop_3':
            self.apply_note_cmd(SEQ_RHYTHM_NOTE_CHOP_3, nTimeMinAbs, nTimeMaxAbs, bSelMode)
        elif sSubCmd == 'chop_2':
            self.apply_note_cmd(SEQ_RHYTHM_NOTE_CHOP_2, nTimeMinAbs, nTimeMaxAbs, bSelMode)
        elif sSubCmd == 'pitx_up':
            self.operate_notes(SEQ_NOTE_CMD_SHIFT_UP, bAllMode)
        elif sSubCmd == 'pitx_dw':
            self.operate_notes(SEQ_NOTE_CMD_SHIFT_DW, bAllMode)
        elif sSubCmd == 'time_lf':
            self.operate_notes(SEQ_NOTE_CMD_SHIFT_LF, bAllMode)
        elif sSubCmd == 'time_rg':
            self.operate_notes(SEQ_NOTE_CMD_SHIFT_RG, bAllMode)
        elif sSubCmd == 'mute':
            self.operate_notes(SEQ_NOTE_CMD_MUTE, bAllMode)
        elif sSubCmd == 'solo':
            self.operate_notes(SEQ_NOTE_CMD_SOLO, bAllMode)
        elif sSubCmd == 'vel_reset':
            self.operate_notes(SEQ_NOTE_CMD_VEL_RST, bAllMode)
        elif sSubCmd == 'delete':
            if bAllMode: # clear midi clip totally
                oClip = self.get_midi_clip_or_none()
                oClip.remove_notes(0.0, 0, 128.0, 127)
                self.alert('> CLIP CLEARED')
            else:
                self.apply_note_cmd(SEQ_RHYTHM_NOTE_DEL_SEL, nTimeMinAbs, nTimeMaxAbs)

    def handle_bit_cmd(self, _hParams):
        nGridIdx = 1 if self.m_nPeerMode == SEQ_INST_MODE_PRIMARY else 2
        if _hParams['grid'] != nGridIdx: return
        sSubCmd  = _hParams['subcmd']
        nBitIdx  = _hParams['index']
        bSelMode = (_hParams['mode'] == 'sel') # apply on selected note pitches only
        (nTimeMinAbs, nTimeMaxAbs) = self.get_bit_time_vars(nBitIdx)
        if sSubCmd == 'mul':
            self.apply_note_cmd(SEQ_RHYTHM_NOTE_MUL, nTimeMinAbs, nTimeMaxAbs, bSelMode)
        elif sSubCmd == 'div':
            self.apply_note_cmd(SEQ_RHYTHM_NOTE_DIV, nTimeMinAbs, nTimeMaxAbs, bSelMode)
        elif sSubCmd == 'chop_3':
            self.apply_note_cmd(SEQ_RHYTHM_NOTE_CHOP_3, nTimeMinAbs, nTimeMaxAbs, bSelMode)
        elif sSubCmd == 'chop_2':
            self.apply_note_cmd(SEQ_RHYTHM_NOTE_CHOP_2, nTimeMinAbs, nTimeMaxAbs, bSelMode)

    def handle_bit_cfg(self, _hParams):
        sType  = _hParams['type']
        nValue = _hParams['value']

        if sType == 'len':
            self.m_nNoteLength = nValue
            if self.m_nPeerMode == SEQ_INST_MODE_PRIMARY:
                self.alert('BIT CFG LENGTH: %0.3f' % (nValue))
        elif sType == 'vel':
            self.m_nNoteVelocity = nValue
            if self.m_nPeerMode == SEQ_INST_MODE_PRIMARY:
                self.alert('BIT CFG VELOCITY: %d' % (nValue))
        elif sType == 'chord':
            self.m_nChordType = nValue
            if self.m_nPeerMode == SEQ_INST_MODE_PRIMARY:
                lNames = ['TRIAD', 'AUGMENTED', 'POWER 5TH', 'NONE']
                self.alert('BIT CFG CHORD: %s' % (lNames[nValue]))
        elif sType == 'chord_inv':
            self.m_nChordInv = nValue
            if self.m_nPeerMode == SEQ_INST_MODE_PRIMARY:
                lNames = ['NONE', '1 FIRST', '2 SECOND']
                self.alert('BIT CFG CHORD INVERSION: %s' % (lNames[nValue]))

    # **************************************************************************

    def get_clip_state(self):
        self.m_oMidiSlot = self.get_midi_slot_or_none()
        if self.m_oMidiSlot != None and not self.m_oMidiSlot.has_clip_has_listener(self._on_clip_changed):
            self.m_oMidiSlot.add_has_clip_listener(self._on_clip_changed)

        self.m_oClip  = self.get_midi_clip_or_none()
        self.m_oTrack = self.get_midi_track_or_none()

        if self.m_oClip == None:
            if self.m_oTrack == None:
                return SEQ_CLIP_STATE_INVALID
            else:
                return SEQ_CLIP_STATE_EMPTY

        self.m_oClip.add_notes_listener(self._on_clip_notes_changed)
        self.m_oClip.add_loop_start_listener(self._on_clip_length_changed)
        self.m_oClip.add_loop_end_listener(self._on_clip_length_changed)

        nClipLen = int(self.m_oClip.loop_end - self.m_oClip.loop_start)
        if self.m_nTimeOffAbs >= nClipLen:
            self.m_nTimeOffAbs = 0

        return SEQ_CLIP_STATE_READY

    def disconnect_clip_listeners(self):
        if (self.m_oMidiSlot != None and self.m_oMidiSlot.has_clip_has_listener(self._on_clip_changed)):
            self.m_oMidiSlot.remove_has_clip_listener(self._on_clip_changed)
        if (self.m_oClip != None):
            if (self.m_oClip.notes_has_listener(self._on_clip_notes_changed)):
                self.m_oClip.remove_notes_listener(self._on_clip_notes_changed)
            if (self.m_oClip.loop_start_has_listener(self._on_clip_length_changed)):
                self.m_oClip.remove_loop_start_listener(self._on_clip_length_changed)
            if (self.m_oClip.loop_end_has_listener(self._on_clip_length_changed)):
                self.m_oClip.remove_loop_end_listener(self._on_clip_length_changed)

    def _on_clip_changed(self):
        self.connect_controls(SEQ_SUBMODE_NOTES)

    def _on_clip_notes_changed(self):
        if self.m_nClipState == SEQ_CLIP_STATE_READY:
            if self.m_nSubMode == SEQ_SUBMODE_NOTES:
                self.update_beat_grid()
            elif self.m_nSubMode == SEQ_SUBMODE_ZOOM:
                self.update_zoom_buttons()

    def _on_clip_length_changed(self):
        self.compute_section_values()
        if self.m_nClipState == SEQ_CLIP_STATE_READY:
            if self.m_nSubMode == SEQ_SUBMODE_NOTES:
                self.update_beat_grid()
            elif self.m_nSubMode == SEQ_SUBMODE_ZOOM:
                self.update_zoom_buttons()
            elif self.m_nSubMode == SEQ_SUBMODE_TOOLS:
                self.update_section_buttons()
            elif self.m_nSubMode == SEQ_SUBMODE_RHYTHM:
                self.update_section_buttons()

    # **************************************************************************

    def setup_invalid_clip_buttons(self):
        for nPitxIdxRel in self.m_rHeight:
            for nTimeIdxRel in self.m_rWidth:
                oButton = self.get_matrix_button(nPitxIdxRel, nTimeIdxRel)
                oButton.set_on_off_values("Sequencer.Invalid")
                if (self.m_aInvalidPattern[nPitxIdxRel][nTimeIdxRel] == 1):
                    oButton.turn_on()
                else:
                    oButton.turn_off()

    # **************************************************************************

    def setup_empty_clip_buttons(self):
        oTrack = self.get_midi_track_or_none()
        for nPitxIdxRel in self.m_rHeight:
            for nTimeIdxRel in self.m_rWidth:
                oButton = self.get_matrix_button(nPitxIdxRel, nTimeIdxRel)
                oButton.set_on_off_values("Sequencer.Empty")
                if (self.m_aEmptyPattern[nPitxIdxRel][nTimeIdxRel] == 1):
                    oButton.turn_on()
                    oButton.add_value_listener(self._on_add_new_clip_value)
                    self.m_aAddClipCtls.append(oButton)
                else:
                    oButton.turn_off()

    def disconnect_empty_clip_buttons(self):
        for oButton in self.m_aAddClipCtls:
            oButton.remove_value_listener(self._on_add_new_clip_value)
        self.m_aAddClipCtls = []

    def _on_add_new_clip_value(self, _nValue):
        if (_nValue != BUTTON_ON): return
        self.create_empty_midi_clip()

    # **************************************************************************

    def focus_clip_view(self):
        oView = self.application().view
        oView.show_view('Detail')
        oView.focus_view('Detail')
        oView.show_view('Detail/Clip')
        oView.focus_view('Detail/Clip')

    # **************************************************************************

    def setup_note_selection_buttons(self):
        for nPitxIdxRel in self.m_rHeight:
            oButton = self.m_aSceneButtons[nPitxIdxRel]
            oButton.set_on_off_values("Sequencer.NoteSel")
            oButton.m_hSelData = { 'pitch_index_rel': self.m_nHeight - nPitxIdxRel - 1 }
            oButton.add_value_listener(self._on_note_sel_value, identify_sender = True)
        self.update_note_sel_buttons()

    def disconnect_note_selection_buttons(self):
        for oButton in self.m_aSceneButtons:
            oButton.set_on_off_values("DefaultButton.Disabled", "DefaultButton.Disabled")
            oButton.turn_off()
            oButton.remove_value_listener(self._on_note_sel_value)

    def _on_note_sel_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        nPitxIdxRel = _oSender.m_hSelData['pitch_index_rel']
        self.select_note(nPitxIdxRel, True)

    def select_note(self, _nPitxIdxRel, _bLocal):
        nPitxIdxAbs = self.note_pitx_abs(_nPitxIdxRel)
        if self.is_pitx_selected(_nPitxIdxRel):
            del self.m_hSelectedPitx[nPitxIdxAbs]
        else:
            self.m_hSelectedPitx[nPitxIdxAbs] = True
        self.update_note_sel_buttons()
        self.update_note_sel_zoom_buttons()
        if _bLocal and self.m_bNavSync:
            self.send_peer_command('note_sel', { 'pitch_index_rel': _nPitxIdxRel })

    def update_note_sel_buttons(self):
        if (not self.in_valid_submode(SEQ_SUBMODE_NOTES) and
            not self.in_valid_submode(SEQ_SUBMODE_TOOLS) and
            not self.in_valid_submode(SEQ_SUBMODE_RHYTHM)):
            return

        for nPitxIdxRel in self.m_rHeight:
            oButton     = self.m_aSceneButtons[nPitxIdxRel]
            nPitxIdxRel = oButton.m_hSelData['pitch_index_rel']
            if self.is_pitx_selected(nPitxIdxRel):
                oButton.turn_on()
            else:
                oButton.turn_off()

    # **************************************************************************

    def setup_note_navigation_buttons(self):
        aNavDirs = ['up', 'down', 'left', 'right']
        for nNavIdx in range(len(self.m_aNavButtons)):
            oButton = self.m_aNavButtons[nNavIdx]
            oButton.set_on_off_values("Sequencer.Nav")
            oButton.turn_on() # TODO! this should be updated everytime we navigate to a new sequencer section!
            oButton.m_hNavData = { 'dir': aNavDirs[nNavIdx] }
            oButton.add_value_listener(self._on_note_nav_value, identify_sender = True)

    def disconnect_note_navigation_buttons(self):
        for oButton in self.m_aNavButtons:
            oButton.set_on_off_values("DefaultButton.Disabled", "DefaultButton.Disabled")
            oButton.turn_off()
            oButton.remove_value_listener(self._on_note_nav_value)

    def _on_note_nav_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        sDir = _oSender.m_hNavData['dir']
        self.note_navigate(sDir, True)

    def note_navigate(self, _sDir, _bLocal):
        bUpdate = False

        if (_sDir == 'up'):
            nPitxShift  = self.get_pitx_shift()
            nPitxOffAbs = self.m_nPitxOffAbs + nPitxShift
            if nPitxOffAbs <= (LEN_ONE_OCT * 10):
                self.m_nPitxOffAbs = nPitxOffAbs
                bUpdate = True

        elif (_sDir == 'down'):
            nPitxShift  = self.get_pitx_shift()
            nPitxOffAbs = self.m_nPitxOffAbs - nPitxShift
            if nPitxOffAbs >= 0:
                self.m_nPitxOffAbs = nPitxOffAbs
                bUpdate = True

        elif (_sDir == 'left'):
            nTimeShift  = self.get_time_shift(False)
            nTimeOffAbs = self.m_nTimeOffAbs - nTimeShift
            if nTimeOffAbs >= 0:
                self.m_nTimeOffAbs = nTimeOffAbs
                bUpdate = True

        elif (_sDir == 'right'):
            nTimeShift  = self.get_time_shift(False)
            nTimeOffAbs = self.m_nTimeOffAbs + nTimeShift
            oClip = self.m_oClip if self.m_oClip != None else self.get_midi_clip_or_none()

            nClipLength = int(oClip.loop_end - oClip.loop_start)
            if nTimeOffAbs <= nClipLength - nTimeShift:
                self.m_nTimeOffAbs = nTimeOffAbs
                bUpdate = True

        if bUpdate:
            self.update_beat_grid()
            self.update_note_sel_buttons()
            self.update_zoom_buttons()
            self.update_section_buttons()
            if _bLocal and self.m_bNavSync:
                self.send_peer_command('note_nav', { 'dir': _sDir })
                self.send_matrix_command('note_nav', {
                    'pitx_abs': self.m_nPitxOffAbs,
                    'time_abs': self.m_nTimeOffAbs,
                })

        nOctave   = (self.m_nPitxOffAbs / LEN_ONE_OCT) - 2
        nOctShift = self.m_nPitxOffAbs % LEN_ONE_OCT
        lMessage  = '> OCT: %d, SHF: %d, TIME: %d' % (nOctave, nOctShift, self.m_nTimeOffAbs)
        if self.m_bNavSync:
            # if we have nav sync display only the alert of the primary surface
            if (self.m_nPeerMode == SEQ_INST_MODE_PRIMARY):
                self.alert(lMessage)
        else:
            # we are not in sync mode! display the alert always!
            self.alert(lMessage)

    # **************************************************************************

    def setup_track_sliders(self):
        self.m_oMasterSlider.add_value_listener(self._on_master_slider_value)
        for nTimeIdxRel in self.m_rWidth:
            oSlider = self.m_aTrackSliders[nTimeIdxRel]
            oSlider.m_hSliderData = { 'slider_index': nTimeIdxRel }
            oSlider.add_value_listener(self._on_track_slider_value, identify_sender = True)

    def disconnect_track_sliders(self):
        self.m_oMasterSlider.remove_value_listener(self._on_master_slider_value)
        for oSlider in self.m_aTrackSliders:
            oSlider.remove_value_listener(self._on_track_slider_value)

    def _on_master_slider_value(self, _nValue):
        (nTimeMinAbs, nTimeMaxAbs) = self.get_master_time_vars()
        self.apply_slider_cmd(_nValue, nTimeMinAbs, nTimeMaxAbs)

    def _on_track_slider_value(self, _nValue, _oSender):
        nTimeIdxRel = _oSender.m_hSliderData['slider_index']
        (nTimeMinAbs, nTimeMaxAbs) = self.get_bit_time_vars(nTimeIdxRel)
        self.apply_slider_cmd(_nValue, nTimeMinAbs, nTimeMaxAbs)

    def apply_slider_cmd(self, _nValue, _nTimeMinAbs, _nTimeMaxAbs):
        if self.m_nSliderMode == SEQ_SLIDER_MODE_NONE:
            self.alert('SLIDER MODE NOT SELECTED')
            return
        if len(self.m_hSelectedPitx) == 0:
            self.alert('NO SELECTED NOTES')
            return

        bExec   = False
        nValIdx = _nValue / 8
        nBitLen = self.get_bit_length()

        oClip = self.get_midi_clip_or_none()
        # execute command in notes
        aNotes = self.get_clip_notes()
        for tNote in aNotes: # tNote is a tuple
            # tNote format: Note, Time, Length, Velocity, Mute
            nPitxIdxAbs = tNote[0] # Pitch value, between 0 and 127 [int]
            nTimeIdxAbs = tNote[1] # Time [float]

            if not (nPitxIdxAbs in self.m_hSelectedPitx):
                continue # pitch is not selected, nothing else to do here
            if (nTimeIdxAbs < _nTimeMinAbs or nTimeIdxAbs >= _nTimeMaxAbs):
                continue # nothing else to do for this note since is not inside the time range

            nNoteLen  = tNote[2] # note length [float]
            nNoteVel  = tNote[3] # note velocity [int]
            bNoteMute = tNote[4] # mute flag [boolean]
            aNewNotes = list([]) # (pitch [int], time [float], length [float], velocity [int], muted [boolean])

            # remove note
            # (from_time [double], from_pitch [int], time_span [double], pitch_span [int])
            oClip.remove_notes(nTimeIdxAbs, nPitxIdxAbs, nNoteLen, 1)

            if self.m_nSliderMode == SEQ_SLIDER_MODE_VELOCITY:
                self.alert('VEL: %d' % (_nValue))
                aNewNotes.append([nPitxIdxAbs, nTimeIdxAbs, nNoteLen, _nValue, bNoteMute])
                bExec = True
            elif self.m_nSliderMode == SEQ_SLIDER_MODE_LENGTH:
                nNewLen = self.m_aLenFactors[nValIdx] * nBitLen
                self.alert('LENGTH FACTOR: %f' % (self.m_aLenFactors[nValIdx]))
                aNewNotes.append([nPitxIdxAbs, nTimeIdxAbs, nNewLen, nNoteVel, bNoteMute])
                bExec = True
            elif self.m_nSliderMode == SEQ_SLIDER_MODE_SHIFT:
                nNewShift    = self.m_aShfFactors[nValIdx] * nBitLen
                nTimeOrigAbs = float(int(nTimeIdxAbs * 4.0)) / 4.0
                self.alert('SHIFT FACTOR: %f' % (self.m_aShfFactors[nValIdx]))
                aNewNotes.append([nPitxIdxAbs, nTimeOrigAbs + nNewShift, nNoteLen, nNoteVel, bNoteMute])
                bExec = True

            oClip.replace_selected_notes(tuple(aNewNotes))
            oClip.deselect_all_notes() # deselect notes since replacing notes auto-selected them

        if not bExec:
            self.alert('NO NOTES AFFECTED. CHECK SELECTION')

    # **************************************************************************

    def setup_notes_buttons(self):
        for nPitxIdxRel in self.m_rHeight:
            for nTimeIdxRel in self.m_rWidth:
                oButton = self.get_matrix_button(nPitxIdxRel, nTimeIdxRel)
                oButton.set_on_off_values("Sequencer.Note")
                oButton.m_hNoteData = { 'pitx': nPitxIdxRel, 'time': nTimeIdxRel }
                oButton.add_value_listener(self._on_note_bit_value, identify_sender = True)
        self.update_beat_grid()

    def disconnect_notes_buttons(self):
        for nPitxIdxRel in self.m_rHeight:
            for nTimeIdxRel in self.m_rWidth:
                oButton = self.m_oMatrix.get_button(nTimeIdxRel, nPitxIdxRel)
                oButton.turn_off()
                oButton.remove_value_listener(self._on_note_bit_value)

    def update_beat_grid(self):
        if not self.in_valid_submode(SEQ_SUBMODE_NOTES): return
        aNotes = self.get_clip_notes()

        # turn on active bit buttons
        self.m_hActiveButtons = {}
        for tNote in aNotes: # tNote is a tuple
            # tNote format: Note, Time, Length, Velocity, Mute
            nPitxIdxAbs = tNote[0] # Pitch value, between 0 and 127
            nTimeIdxAbs = tNote[1] # Time

            if (self.is_note_visible(nPitxIdxAbs, nTimeIdxAbs) == False):
                continue # nothing else to do for this note since is not visible in remote GUI

            nPitxIdxRel = self.note_pitx_rel(nPitxIdxAbs)
            if nPitxIdxRel < 0:
                continue # note is not visible since there is a scale mask
            nTimeIdxRel = self.note_time_rel(nTimeIdxAbs)
            if self.is_root_note(nPitxIdxAbs):
                self.get_matrix_button(nPitxIdxRel, nTimeIdxRel).set_light('Sequencer.Note.Root')
            else:
                self.get_matrix_button(nPitxIdxRel, nTimeIdxRel).turn_on()
            self.m_hActiveButtons['%d_%d' % (nPitxIdxRel, nTimeIdxRel)] = True

        # turn off inactive bit buttons
        for nPitxIdxRel in self.m_rHeight:
            for nTimeIdxRel in self.m_rWidth:
                sKey = '%d_%d' % (nPitxIdxRel, nTimeIdxRel)
                if (not (sKey in self.m_hActiveButtons)):
                    self.get_matrix_button(nPitxIdxRel, nTimeIdxRel).turn_off()

    def _on_note_bit_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        nPitxIdxRel = _oSender.m_hNoteData['pitx']
        nTimeIdxRel = _oSender.m_hNoteData['time']
        nPitxIdxAbs = self.note_pitx_abs(nPitxIdxRel)
        nTimeIdxAbs = self.note_time_abs(nTimeIdxRel)

        nLen = self.m_nNoteLength
        nVel = self.m_nNoteVelocity
        sKey = '%d_%d' % (nPitxIdxRel, nTimeIdxRel)

        if (sKey in self.m_hActiveButtons):
            # NOTE! in triad or augmented mode the user should remove bit by bit from the chord!
            # bit button is active! remove the key from the hash and remove the note from the clip
            # signature: (from_time [double], from_pitch [int], time_span [double], pitch_span [int])
            self.m_oClip.remove_notes(nTimeIdxAbs, nPitxIdxAbs, nLen, 1)
            del self.m_hActiveButtons[sKey]
        else:
            # NOTE! in triad or augmented mode the user adds only the chord's root note and we add the
            # rest of the notes
            # bit button is inactive! add the key to the hash and add the note to the clip
            # signature: (pitch [int], time [float], length [float], velocity [int], muted [boolean])
            aNotes = list([])
            aNotes.append([nPitxIdxAbs, nTimeIdxAbs, nLen, nVel, False]) # the root note
            if self.m_nScale != SEQ_SCALE_CHROMATIC and self.m_nChordType != BIT_CHORD_NONE: # chord mode on!
                if self.m_nChordType == BIT_CHORD_POW_5:
                    # eighth (1 octave up)
                    nPitxIdxRel8th = nPitxIdxRel + 7
                    nPitxIdxAbs8th = self.note_pitx_abs_chord(nPitxIdxRel8th, False) # never use inversions for power-5th
                    aNotes.append([nPitxIdxAbs8th, nTimeIdxAbs, nLen, nVel, False]) # the root note
                    if self.is_note_visible(nPitxIdxAbs8th, nTimeIdxAbs):
                        nPitxRel = self.note_pitx_rel(nPitxIdxAbs8th)
                        sKey8    = '%d_%d' % (nPitxRel, nTimeIdxRel)
                        self.m_hActiveButtons[sKey8] = True
                else:
                    # third
                    nPitxIdxRel3rd = nPitxIdxRel + 2
                    nPitxIdxAbs3rd = self.note_pitx_abs_chord(nPitxIdxRel3rd, self.m_nChordInv == BIT_CHORD_INV_2)
                    aNotes.append([nPitxIdxAbs3rd, nTimeIdxAbs, nLen, nVel, False]) # the root note
                    if self.is_note_visible(nPitxIdxAbs3rd, nTimeIdxAbs):
                        nPitxRel = self.note_pitx_rel(nPitxIdxAbs3rd)
                        sKey3    = '%d_%d' % (nPitxRel, nTimeIdxRel)
                        self.m_hActiveButtons[sKey3] = True

                # fifth
                nPitxIdxRel5th = nPitxIdxRel + 4
                bUseNeg = self.m_nChordInv != BIT_CHORD_INV_0
                if self.m_nChordType == BIT_CHORD_POW_5:
                    bUseNeg = False # never use inversions for power-5th
                nPitxIdxAbs5th = self.note_pitx_abs_chord(nPitxIdxRel5th, bUseNeg)
                aNotes.append([nPitxIdxAbs5th, nTimeIdxAbs, nLen, nVel, False]) # the root note
                if self.is_note_visible(nPitxIdxAbs5th, nTimeIdxAbs):
                    nPitxRel = self.note_pitx_rel(nPitxIdxAbs5th)
                    sKey5    = '%d_%d' % (nPitxRel, nTimeIdxRel)
                    self.m_hActiveButtons[sKey5] = True

                # seventh
                if self.m_nChordType == BIT_CHORD_AUGM:
                    nPitxIdxRel7th = nPitxIdxRel + 6
                    nPitxIdxAbs7th = self.note_pitx_abs_chord(nPitxIdxRel7th, self.m_nChordInv != BIT_CHORD_INV_0)
                    aNotes.append([nPitxIdxAbs7th, nTimeIdxAbs, nLen, nVel, False]) # the root note
                    if self.is_note_visible(nPitxIdxAbs7th, nTimeIdxAbs):
                        nPitxRel = self.note_pitx_rel(nPitxIdxAbs7th)
                        sKey7    = '%d_%d' % (nPitxRel, nTimeIdxRel)
                        self.m_hActiveButtons[sKey7] = True
            self.m_oClip.replace_selected_notes(tuple(aNotes))
            self.m_hActiveButtons[sKey] = True
        self.m_oClip.deselect_all_notes()

    def note_pitx_abs_chord(self, _nNotePitxRel, _bUseNeg):
        nNotePitxRel = _nNotePitxRel + 7  # use neutral (or positive) scale
        if _bUseNeg: # for notes in first and second inversion
          nNotePitxRel = nNotePitxRel - 7 # use the negative scale
        lScale0  = self.m_aScales[self.m_nScale][1][0:7] # neutral scale (0 based) (use only first 7 offsets!)
        lScaleN  = [p - 12 for p in lScale0]   # negative scale (-12 based)
        lScaleP1 = [p + 12 for p in lScale0]   # positive scale (+12 based)
        lScaleP2 = [p + 24 for p in lScale0]   # positive scale (+24 based) (Power 5th uses this for highest pitch)
        lScale   = lScaleN + lScale0 + lScaleP1 + lScaleP2 # negative, 0 and positive scale offsets
        nPitxAbs = lScale[nNotePitxRel] + self.m_nPitxOffAbs + self.m_nRootPitx
        if nPitxAbs < 0:
            nPitxAbs = nPitxAbs + 12
        if nPitxAbs > 127:
            nPitxAbs = nPitxAbs - 12
        return nPitxAbs

    # **************************************************************************

    def setup_zoom_buttons(self):
        for nPitxIdxRel in self.m_rHeight:
            for nTimeIdxRel in self.m_rWidth:
                oButton = self.get_matrix_button(nPitxIdxRel, nTimeIdxRel)
                oButton.m_hZoomData = {
                    'octave_index': nPitxIdxRel,
                    'time_index'  : nTimeIdxRel
                }
                oButton.add_value_listener(self._on_zoom_value, identify_sender = True)
        self.update_zoom_buttons()

    def disconnect_zoom_buttons(self):
        for nPitxIdxRel in self.m_rHeight:
            for nTimeIdxRel in self.m_rWidth:
                oButton = self.get_matrix_button(nPitxIdxRel, nTimeIdxRel)
                oButton.remove_value_listener(self._on_zoom_value)

    # this should be called anytime when:
    # * the clip is modified (since the length of the clip might have changed)
    # * the navigation buttons has been activated, to move to highlight the correct button
    def update_zoom_buttons(self):
        if not self.in_valid_submode(SEQ_SUBMODE_ZOOM): return

        nTimeDelta = self.get_section_length() # in [beats]
        #  4 beats = 1 bar             (in 2 surfaces)
        # 16 beats = 4 bars = 1 phrase (in 2 surfaces)

        nTimeStart = self.m_oClip.loop_start
        nTimeEnd   = self.m_oClip.loop_end
        nTimeSpan  = int(nTimeEnd - nTimeStart) # in [beats]

        # find out which zoom blocks have notes
        aNotes = self.get_clip_notes()
        hNonEmptyBlocks = {}
        for tNote in aNotes:
            # tNote format: Note, Time, Length, Velocity, Mute
            nPitxIdxAbs = tNote[0] # Note value, between 0 and 127
            nTimeIdxAbs = tNote[1] # Time

            # discard non-visible notes
            if self.m_nScale != SEQ_SCALE_CHROMATIC:
                # in non-chromatic scale we need to discard all notes
                # below the root pitch of the octave -2 (midi 0 .. 12)
                if nPitxIdxAbs < self.m_nRootPitx:
                    continue # non-visible note (is lower than the root note)
                if nPitxIdxAbs > (LEN_ONE_OCT * self.m_nHeight + self.m_nRootPitx):
                    continue # non-visible note (is higher than the highest visible octave)
            else:
                if nPitxIdxAbs > (LEN_ONE_OCT * self.m_nHeight):
                    continue # non-visible note (is higher than the highest visible octave)

            if nTimeIdxAbs < 0:
                continue # non-visible note (is located in negative time)

            if self.m_nScale != SEQ_SCALE_CHROMATIC:
                nZoomRow = nPitxIdxAbs / LEN_ONE_OCT
            else:
                nZoomRow = (nPitxIdxAbs - self.m_nRootPitx) / LEN_ONE_OCT
            nZoomCol = nTimeIdxAbs / nTimeDelta

            sKey = '%d_%d' % (nZoomRow, nZoomCol)
            hNonEmptyBlocks[sKey] = True

        # compute the current block zoom coords
        if self.m_nScale != SEQ_SCALE_CHROMATIC:
            nCurZoomRow = self.m_nPitxOffAbs / LEN_ONE_OCT
        else:
            nCurZoomRow = (self.m_nPitxOffAbs - self.m_nRootPitx) / LEN_ONE_OCT
        nCurZoomCol = self.m_nTimeOffAbs / nTimeDelta

        # compute number of visible zoom columns
        nVisZoomCols = nTimeSpan / nTimeDelta
        if (nTimeSpan % nTimeDelta) != 0:
            nVisZoomCols += 1

        # now actually draw the buttons with the right colors
        for nPitxIdxRel in self.m_rHeight:
            for nTimeIdxRel in self.m_rWidth:
                oButton = self.get_matrix_button(nPitxIdxRel, nTimeIdxRel)
                if nTimeIdxRel >= nVisZoomCols:
                    oButton.set_light('Sequencer.Zoom.Unava')
                    continue

                if nTimeIdxRel == nCurZoomCol and nPitxIdxRel == nCurZoomRow:
                    oButton.set_light('Sequencer.Zoom.Selected')
                    continue

                sKey = '%d_%d' % (nPitxIdxRel, nTimeIdxRel)
                if sKey in hNonEmptyBlocks:
                    oButton.set_light('Sequencer.Zoom.Active')
                else:
                    oButton.set_light('Sequencer.Zoom.Empty')

    def _on_zoom_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        nOctaveIdx = _oSender.m_hZoomData['octave_index']
        nTimeIdx   = _oSender.m_hZoomData['time_index']
        self.zoom_navigate(nOctaveIdx, nTimeIdx, True)

    def zoom_navigate(self, _nOctaveIdx, _nTimeIdx, _bLocal):
        if _nTimeIdx >= self.m_nNumSect: return

        self.m_nPitxOffAbs = _nOctaveIdx * LEN_ONE_OCT
        self.m_nTimeOffAbs = _nTimeIdx   * self.get_time_shift(True)

        self.update_beat_grid()
        self.update_zoom_buttons()
        self.update_section_buttons()
        self.update_note_sel_buttons()

        if _bLocal and self.m_bNavSync:
            self.send_peer_command('zoom_nav', {
                'octave_index': _nOctaveIdx,
                'time_index'  : _nTimeIdx,
            })
            self.send_matrix_command('zoom_nav', {
                'octave_index': _nOctaveIdx,
                'time_index'  : _nTimeIdx,
            })

    def setup_note_selection_zoom_buttons(self):
        for nPitxIdxRel in self.m_rHeight:
            oButton = self.m_aSceneButtons[nPitxIdxRel]
            oButton.set_on_off_values("Sequencer.NoteSel")
            oButton.m_hSelZoomData = { 'pitch_zoom_index_rel': self.m_nHeight - nPitxIdxRel - 1 }
            oButton.add_value_listener(self._on_note_sel_zoom_value, identify_sender = True)
        self.update_note_sel_zoom_buttons()

    def disconnect_note_selection_zoom_buttons(self):
        for oButton in self.m_aSceneButtons:
            oButton.set_on_off_values("DefaultButton.Disabled", "DefaultButton.Disabled")
            oButton.turn_off()
            oButton.remove_value_listener(self._on_note_sel_zoom_value)

    def _on_note_sel_zoom_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        nPitxZoomIdxRel = _oSender.m_hSelZoomData['pitch_zoom_index_rel']
        self.select_note_zoom(nPitxZoomIdxRel, True)

    def select_note_zoom(self, _nPitxZoomIdxRel, _bLocal):
        nPitxZoomIdxAbs = _nPitxZoomIdxRel * LEN_ONE_OCT + self.m_nRootPitx

        # count number of selected notes in this pitch span
        nSelected = 0
        for nPitxIdxRel in range(LEN_ONE_OCT):
            nPitxIdxAbs = nPitxZoomIdxAbs + nPitxIdxRel
            if nPitxIdxAbs in self.m_hSelectedPitx:
                nSelected += 1
        bDeselect = (nSelected == LEN_ONE_OCT) # all notes are selected! Deselecte them!

        # select or deselect notes
        for nPitxIdxRel in range(LEN_ONE_OCT):
            nPitxIdxAbs = nPitxZoomIdxAbs + nPitxIdxRel
            if bDeselect:
                del self.m_hSelectedPitx[nPitxIdxAbs]
            else:
                self.m_hSelectedPitx[nPitxIdxAbs] = True
        self.update_note_sel_zoom_buttons()
        self.update_note_sel_buttons()
        if _bLocal and self.m_bNavSync:
            self.send_peer_command('note_sel_zoom', { 'pitch_zoom_index_rel': _nPitxZoomIdxRel })

    def update_note_sel_zoom_buttons(self):
        if not self.in_valid_submode(SEQ_SUBMODE_ZOOM): return

        for nPitxIdxRel in self.m_rHeight:
            oButton         = self.m_aSceneButtons[nPitxIdxRel]
            nPitxZoomIdxRel = oButton.m_hSelZoomData['pitch_zoom_index_rel']
            nPitxZoomIdxAbs = nPitxZoomIdxRel * LEN_ONE_OCT + self.m_nRootPitx

            # count number of selected notes in this pitch span
            nSelected = 0
            for nPitxIdxRel in range(LEN_ONE_OCT):
                nPitxIdxAbs = nPitxZoomIdxAbs + nPitxIdxRel
                if nPitxIdxAbs in self.m_hSelectedPitx:
                    nSelected += 1
            bSelected = (nSelected == LEN_ONE_OCT) # all notes are selected!
            if bSelected:
                oButton.turn_on()
            else:
                oButton.turn_off()

    # **************************************************************************

    def setup_tools_buttons(self):
        # setup skin
        for nPitxIdxRel in self.m_rHeight:
            for nTimeIdxRel in self.m_rWidth:
                oButton = self.m_oMatrix.get_button(nTimeIdxRel, nPitxIdxRel)
                oButton.set_on_off_values("Sequencer.Tools.%s" % (self.m_aToolsSkin[nPitxIdxRel][nTimeIdxRel]))

        # octave selection buttons
        for nTimeIdxRel in range(2):
            for nPitxIdxRel in range(5):
                oButton = self.m_oMatrix.get_button(nTimeIdxRel, nPitxIdxRel)
                nOctIdx = 4 - nPitxIdxRel
                nPitOff = nTimeIdxRel * 5 + nOctIdx
                oButton.m_hOctaveData = { 'pitx_off_abs': nPitOff * LEN_ONE_OCT }
                oButton.add_value_listener(self._on_octave_nav_value, identify_sender = True)

        # scale, root note and loop buttons
        for nTimeIdxRel in range(6):
            for nPitxIdxRel in range(2):
                oButton   = self.m_oMatrix.get_button(nTimeIdxRel + 2, nPitxIdxRel)
                nScaleIdx = nPitxIdxRel * 6 + nTimeIdxRel + 1
                oButton.m_hScaleData = { 'scale_idx': nScaleIdx }
                oButton.add_value_listener(self._on_scale_value, identify_sender = True)

                oButton  = self.m_oMatrix.get_button(nTimeIdxRel + 2, nPitxIdxRel + 2)
                nRootIdx = nPitxIdxRel * 6 + nTimeIdxRel
                oButton.m_hRootData = { 'root_idx': nRootIdx }
                oButton.add_value_listener(self._on_root_value, identify_sender = True)

            oButton = self.m_oMatrix.get_button(nTimeIdxRel + 2, 4)
            oButton.m_hLoopCmdData = { 'loop_cmd_idx': nTimeIdxRel }
            oButton.add_value_listener(self._on_loop_cmd_value, identify_sender = True)
            oButton.turn_on() # stateless button, these are command buttons!

        # note commands: transpose, mute, solo, note up, note down, shift left, shift right, loop duplicate
        for nTimeIdxRel in self.m_rWidth:
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_NOTE_CMDS)
            oButton.m_hNoteCmdData = { 'note_cmd_index': nTimeIdxRel }
            oButton.add_value_listener(self._on_note_cmd_value, identify_sender = True)
            if nTimeIdxRel > 0:
                oButton.turn_on() # stateless button, these are command buttons!

        # slider mode
        for nTimeIdxRel in range(3):
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_SLIDR_MODE)
            oButton.m_hSliderModeData = { 'slider_mode_index': nTimeIdxRel }
            oButton.add_value_listener(self._on_slider_mode_value, identify_sender = True)

        # section mode
        for nTimeIdxRel in range(5):
            oButton = self.m_oMatrix.get_button(nTimeIdxRel + 3, SEQ_BUT_IDX_SECT_MODE)
            oButton.m_hSectionModeData = { 'section_mode_index': nTimeIdxRel }
            oButton.add_value_listener(self._on_section_mode_value, identify_sender = True)

        # section navigation
        for nTimeIdxRel in self.m_rWidth:
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_SECTIONS)
            oButton.m_hSectionData = { 'section_index': nTimeIdxRel }
            oButton.add_value_listener(self._on_section_value, identify_sender = True)

        self.update_stateful_tools_buttons()

    def disconnect_tools_buttons(self):
        for nTimeIdxRel in range(2):
            for nPitxIdxRel in range(5):
                oButton = self.m_oMatrix.get_button(nTimeIdxRel, nPitxIdxRel)
                oButton.remove_value_listener(self._on_octave_nav_value)

        for nTimeIdxRel in range(6):
            for nPitxIdxRel in range(2):
                oButton = self.m_oMatrix.get_button(nTimeIdxRel + 2, nPitxIdxRel)
                oButton.remove_value_listener(self._on_scale_value)
                oButton = self.m_oMatrix.get_button(nTimeIdxRel + 2, nPitxIdxRel + 2)
                oButton.remove_value_listener(self._on_root_value)
            oButton = self.m_oMatrix.get_button(nTimeIdxRel + 2, 4)
            oButton.remove_value_listener(self._on_loop_cmd_value)

        for nTimeIdxRel in self.m_rWidth:
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_NOTE_CMDS)
            oButton.remove_value_listener(self._on_note_cmd_value)

        for nTimeIdxRel in range(3):
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_SLIDR_MODE)
            oButton.remove_value_listener(self._on_slider_mode_value)

        for nTimeIdxRel in range(5):
            oButton = self.m_oMatrix.get_button(nTimeIdxRel + 3, SEQ_BUT_IDX_SECT_MODE)
            oButton.remove_value_listener(self._on_section_mode_value)

        for nTimeIdxRel in self.m_rWidth:
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_SECTIONS)
            oButton.remove_value_listener(self._on_section_value)

    def update_stateful_tools_buttons(self):
        self.update_tools_octave_buttons()
        self.update_tools_scale_buttons()
        self.update_tools_transpose_button()
        self.update_tools_slider_mode_buttons()
        self.update_section_mode_buttons()
        self.update_section_buttons()

    def update_tools_octave_buttons(self):
        if not self.in_valid_submode(SEQ_SUBMODE_TOOLS): return

        nCurOctIdx = self.m_nPitxOffAbs / LEN_ONE_OCT
        for nTimeIdxRel in range(2):
            for nPitxIdxRel in range(5):
                oButton = self.m_oMatrix.get_button(nTimeIdxRel, nPitxIdxRel)
                nButOctIdx = oButton.m_hOctaveData['pitx_off_abs'] / LEN_ONE_OCT
                if nButOctIdx == nCurOctIdx:
                    oButton.turn_on()
                else:
                    oButton.turn_off()

    def update_tools_scale_buttons(self):
        if not self.in_valid_submode(SEQ_SUBMODE_TOOLS): return

        aIonianOffsets = self.m_aScales[1][1] # Ionian Natural Major: all white semitones
        for nTimeIdxRel in range(6):
            for nPitxIdxRel in range(2):
                oButton = self.m_oMatrix.get_button(nTimeIdxRel + 2, nPitxIdxRel)
                nScale  = oButton.m_hScaleData['scale_idx']
                if nScale == self.m_nScale:
                    oButton.turn_on()
                else:
                    oButton.turn_off()

                oButton = self.m_oMatrix.get_button(nTimeIdxRel + 2, nPitxIdxRel + 2)
                nRoot   = oButton.m_hRootData['root_idx']
                if nRoot == self.m_nRootPitx:
                    oButton.turn_on()
                else:
                    if nRoot in aIonianOffsets:
                        oButton.set_light('Sequencer.Tools.Root.Whole')
                    else:
                        oButton.set_light('Sequencer.Tools.Root.Half')

    def update_tools_transpose_button(self):
        if not self.in_valid_submode(SEQ_SUBMODE_TOOLS): return

        oButton = self.m_oMatrix.get_button(0, SEQ_BUT_IDX_NOTE_CMDS)
        if self.m_nTransState == SEQ_TRANS_UNAV:
            oButton.set_light('Sequencer.Tools.Trans.Unav')
        elif self.m_nTransState == SEQ_TRANS_STANDBY:
            oButton.turn_on()
        else:
            oButton.turn_off()

    def update_tools_slider_mode_buttons(self):
        if not self.in_valid_submode(SEQ_SUBMODE_TOOLS): return

        for nTimeIdxRel in range(3):
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_SLIDR_MODE)
            nSliderModeIdx = oButton.m_hSliderModeData['slider_mode_index']
            if (nSliderModeIdx == self.m_nSliderMode):
                oButton.turn_on()
            else:
                oButton.turn_off()

    def update_section_mode_buttons(self):
        if (not self.in_valid_submode(SEQ_SUBMODE_TOOLS) and
            not self.in_valid_submode(SEQ_SUBMODE_RHYTHM)):
            return

        for nTimeIdxRel in range(5):
            oButton = self.m_oMatrix.get_button(nTimeIdxRel + 3, SEQ_BUT_IDX_SECT_MODE)
            nSectionModeIdx = oButton.m_hSectionModeData['section_mode_index']
            if (nSectionModeIdx == self.m_nSectionMode):
                oButton.turn_on()
            else:
                oButton.turn_off()

    def update_section_buttons(self):
        if (not self.in_valid_submode(SEQ_SUBMODE_TOOLS) and
            not self.in_valid_submode(SEQ_SUBMODE_RHYTHM)):
            return

        self.compute_section_values()
        for nTimeIdxRel in self.m_rWidth:
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_SECTIONS)
            if nTimeIdxRel < self.m_nNumSect:
                if nTimeIdxRel >= self.m_nCurSect and nTimeIdxRel < self.m_nCurSect + self.m_nSpnSect:
                    oButton.turn_on()
                else:
                    oButton.turn_off()
            else:
                oButton.set_light('Sequencer.Rhythm.Sect.Unava')

    def compute_section_values(self):
        # compute the number of sections to display depending on
        # the length of the loop
        nClipLen = int(self.m_oClip.loop_end - self.m_oClip.loop_start)
        nSectLen = self.get_section_length()
        nNumSect = nClipLen / nSectLen
        if (nClipLen % nSectLen != 0): nNumSect += 1
        self.m_nNumSect = nNumSect

        # compute the index of the current section
        nCurSect = self.m_nTimeOffAbs / nSectLen
        self.m_nCurSect = nCurSect

        # compute the section span
        if self.m_nSectionMode == SEQ_SECTION_MODE_2:
            self.m_nSpnSect = 2
        elif self.m_nSectionMode == SEQ_SECTION_MODE_4:
            self.m_nSpnSect = 4
        elif self.m_nSectionMode == SEQ_SECTION_MODE_8:
            self.m_nSpnSect = 8
        else: # for section modes (1/2, 1) use span = 1
            self.m_nSpnSect = 1


    def _on_octave_nav_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        nPitxOffAbs = _oSender.m_hOctaveData['pitx_off_abs']
        self.alert('Octave: %d' % ((nPitxOffAbs / LEN_ONE_OCT) - 2))
        self.octave_navigate(nPitxOffAbs, True)

    def octave_navigate(self, _nPitxOffAbs, _bLocal):
        self.m_nPitxOffAbs = _nPitxOffAbs
        self.update_tools_octave_buttons()
        self.update_beat_grid()
        self.update_zoom_buttons()
        if _bLocal and self.m_bNavSync:
            self.send_peer_command('oct_nav', { 'pitx_off_abs': _nPitxOffAbs })

    def _on_scale_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        nScale = _oSender.m_hScaleData['scale_idx']
        if self.m_nScale == nScale:
            nScale = SEQ_SCALE_CHROMATIC
        self.select_scale(nScale, True)

    def select_scale(self, _nScale, _bLocal):
        self.m_nScale = _nScale
        if self.m_nScale == SEQ_SCALE_CHROMATIC:
            self.m_nRootPitx = SEQ_ROOT_C
        else:
            self.m_nRootPitx = self.m_nRootBkup
        self.m_nPitxOffAbs = (self.m_nPitxOffAbs / LEN_ONE_OCT) * LEN_ONE_OCT
        self.transpose_scale()
        if _bLocal:
            self.send_peer_command('sel_scale', {'scale_idx': _nScale})
            self.alert('SCALE: "%s"' % (self.m_aScales[self.m_nScale][0]))
        self.update_tools_scale_buttons()
        self.update_tools_transpose_button()
        self.update_beat_grid()

    def transpose_scale(self):
        if self.m_nTransState == SEQ_TRANS_UNAV:
            if self.m_nScale == SEQ_SCALE_CHROMATIC:
                self.m_nTransState = SEQ_TRANS_UNAV
            else:
                self.m_nTransState = SEQ_TRANS_STANDBY
        elif self.m_nTransState == SEQ_TRANS_STANDBY:
            if self.m_nScale == SEQ_SCALE_CHROMATIC:
                self.m_nTransState = SEQ_TRANS_UNAV
            else:
                self.m_nTransState = SEQ_TRANS_STANDBY
        elif self.m_nTransState == SEQ_TRANS_AWAIT:
            if self.m_nScale == SEQ_SCALE_CHROMATIC:
                self.m_nTransState = SEQ_TRANS_UNAV
                self.alert('TRANSPOSITION ABORTED, SCALE: "CHROMATIC"')
            else:
                self.execute_transposition()
                self.m_nTransState = SEQ_TRANS_STANDBY

    def execute_transposition(self):
        sSrcScale = self.m_aScales[self.m_nTransScale][0]
        aSrcScale = self.m_aScales[self.m_nTransScale][1]
        sTgtScale = self.m_aScales[self.m_nScale][0]
        aTgtScale = self.m_aScales[self.m_nScale][1]
        self.alert('TRANSPOSING SCALE: "%s" -> "%s"' % (sSrcScale, sTgtScale))

        hTranspose = {}
        for nIdx in range(7):
            if aSrcScale[nIdx] != aTgtScale[nIdx]:
                hTranspose[aSrcScale[nIdx]] = aTgtScale[nIdx]

        # execute command in notes
        oClip  = self.get_midi_clip_or_none()
        aNotes = self.get_clip_notes()
        for tNote in aNotes: # tNote is a tuple
            # tNote format: Note, Time, Length, Velocity, Mute
            nPitxIdxAbs = tNote[0] # Pitch value, between 0 and 127 [int]
            nTimeIdxAbs = tNote[1] # Time [float]
            nNoteLen    = tNote[2] # note length [float]
            nPitxIdxRel = nPitxIdxAbs - self.m_nRootPitx
            nPitxIdxOct = nPitxIdxRel % LEN_ONE_OCT # pitch between 0 and 11
            nNoteOctave = nPitxIdxRel / LEN_ONE_OCT # octave of the note

            if not nPitxIdxOct in hTranspose:
                continue # nothing else to do for this note since is not found in the transpose hash

            # remove note
            # (from_time [double], from_pitch [int], time_span [double], pitch_span [int])
            oClip.remove_notes(nTimeIdxAbs, nPitxIdxAbs, nNoteLen, 1)

            # add the note in the tranposed pitch
            nPitxIdxTrn = hTranspose[nPitxIdxOct] + (nNoteOctave * LEN_ONE_OCT) + self.m_nRootPitx
            nNoteVel    = tNote[3] # note velocity [int]
            bNoteMute   = tNote[4] # mute flag [boolean]
            aNewNotes   = list([]) # (pitch [int], time [float], length [float], velocity [int], muted [boolean])
            aNewNotes.append([nPitxIdxTrn, nTimeIdxAbs, nNoteLen, nNoteVel, bNoteMute])
            oClip.replace_selected_notes(tuple(aNewNotes))
            oClip.deselect_all_notes() # deselect notes since replacing notes auto-selected them

    def _on_root_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        if self.m_nScale == SEQ_SCALE_CHROMATIC:
            return # nothing to do here
        nRoot = _oSender.m_hRootData['root_idx']
        self.select_root(nRoot, True)

    def select_root(self, _nRoot, _bLocal):
        self.m_nRootPitx = _nRoot
        self.m_nRootBkup = _nRoot
        self.update_tools_scale_buttons()
        self.update_beat_grid()
        if _bLocal:
            self.send_peer_command('sel_root', { 'root_idx': _nRoot })

    def _on_loop_cmd_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        nLoopCmdIdx = _oSender.m_hLoopCmdData['loop_cmd_idx']

        (oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize) = self.fetch_loop_vars()
        if nLoopCmdIdx == SEQ_LOOP_CMD_STA_DEC:
            oClip.loop_start = nLoopStart + (nLoopSpan / 2)
        elif nLoopCmdIdx == SEQ_LOOP_CMD_STA_INC:
            oClip.loop_start = nLoopStart - nLoopSpan
        elif nLoopCmdIdx == SEQ_LOOP_CMD_MID_DEC:
            oClip.loop_start = nLoopStart + (nLoopSpan / 4)
            oClip.loop_end   = nLoopEnd   - (nLoopSpan / 4)
        elif nLoopCmdIdx == SEQ_LOOP_CMD_MID_INC:
            oClip.loop_start = nLoopStart - (nLoopSpan / 2)
            oClip.loop_end   = nLoopEnd   + (nLoopSpan / 2)
        elif nLoopCmdIdx == SEQ_LOOP_CMD_END_DEC:
            oClip.loop_end = nLoopStart + (nLoopSpan / 2)
        elif nLoopCmdIdx == SEQ_LOOP_CMD_END_INC:
            oClip.loop_end = nLoopStart + (nLoopSpan * 2)

    def fetch_loop_vars(self):
        nLoopStart = self.m_oClip.loop_start
        nLoopEnd   = self.m_oClip.loop_end
        nLoopSpan  = nLoopEnd - nLoopStart
        nSize      = self.m_aSizes[self.m_nSizeIdx]
        return (self.m_oClip, nLoopStart, nLoopEnd, nLoopSpan, nSize)

    def _on_note_cmd_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        nNoteCmdIdx = _oSender.m_hNoteCmdData['note_cmd_index']

        if nNoteCmdIdx == SEQ_NOTE_CMD_TRANS:
            self.on_transpose_button()
            return

        if nNoteCmdIdx == SEQ_NOTE_CMD_LP_DUPL:
            oClip = self.get_midi_clip_or_none()
            if oClip != None:
                oClip.duplicate_loop()
            return # Nothing else to do here

        self.operate_notes(nNoteCmdIdx)

    def operate_notes(self, _nNoteCmdIdx, _bAllMode = False):
        oClip    = self.get_midi_clip_or_none()
        nSectLen = self.get_section_length()
        nBitLen  = self.get_bit_length()
        bUnsel   = (_nNoteCmdIdx == SEQ_NOTE_CMD_SOLO) # solo command works in unselected notes

        # execute command in notes
        aNotes    = self.get_clip_notes()
        aNewNotes = list([]) # (pitch [int], time [float], length [float], velocity [int], muted [boolean])
        bExec     = False
        for tNote in aNotes: # tNote is a tuple
            # tNote format: Note, Time, Length, Velocity, Mute
            nPitxIdxAbs = tNote[0] # Pitch value, between 0 and 127 [int]
            nTimeIdxAbs = tNote[1] # Time [float]

            if self.is_note_selected(nPitxIdxAbs, nTimeIdxAbs, _bAllMode) == bUnsel:
                continue # nothing else to do for this note

            nNoteLen  = tNote[2] # note length [float]
            nNoteVel  = tNote[3] # note velocity [int]
            bNoteMute = tNote[4] # mute flag [boolean]

            # remove note
            # (from_time [double], from_pitch [int], time_span [double], pitch_span [int])
            oClip.remove_notes(nTimeIdxAbs, nPitxIdxAbs, nNoteLen, 1)

            if _nNoteCmdIdx == SEQ_NOTE_CMD_MUTE:
                aNewNotes.append([nPitxIdxAbs, nTimeIdxAbs, nNoteLen, nNoteVel, not bNoteMute])
                bExec = True
            elif _nNoteCmdIdx == SEQ_NOTE_CMD_SOLO:
                aNewNotes.append([nPitxIdxAbs, nTimeIdxAbs, nNoteLen, nNoteVel, not bNoteMute])
                bExec = True
            elif _nNoteCmdIdx == SEQ_NOTE_CMD_VEL_RST:
                aNewNotes.append([nPitxIdxAbs, nTimeIdxAbs, nNoteLen, 127, bNoteMute])
                bExec = True
            elif _nNoteCmdIdx == SEQ_NOTE_CMD_SHIFT_DW:
                if nPitxIdxAbs - 1 >= 0:
                    aNewNotes.append([nPitxIdxAbs - 1, nTimeIdxAbs, nNoteLen, nNoteVel, bNoteMute])
                bExec = True
            elif _nNoteCmdIdx == SEQ_NOTE_CMD_SHIFT_UP:
                if nPitxIdxAbs + 1 <= 127:
                    aNewNotes.append([nPitxIdxAbs + 1, nTimeIdxAbs, nNoteLen, nNoteVel, bNoteMute])
                bExec = True
            elif _nNoteCmdIdx == SEQ_NOTE_CMD_SHIFT_LF:
                nTimeNew   = nTimeIdxAbs - nBitLen
                nTimeStart = self.m_nTimeOffAbs
                nTimeEnd   = nTimeStart + nSectLen
                if self.is_one_half_mode():
                    if self.m_nPeerMode == SEQ_INST_MODE_SECONDARY: # this is secondary
                        nTimeStart += (nSectLen / 2.0)              # add a time offset of 1/2 section from start time
                    else:
                        nTimeEnd   -= (nSectLen / 2.0)              # remove a time offset of 1/2 section from end time
                if nTimeNew >= nTimeStart:
                    aNewNotes.append([nPitxIdxAbs, nTimeNew, nNoteLen, nNoteVel, bNoteMute])
                    bExec = True
                else:
                    aNewNotes.append([nPitxIdxAbs, nTimeEnd - nBitLen, nNoteLen, nNoteVel, bNoteMute])
                    bExec = True
            elif _nNoteCmdIdx == SEQ_NOTE_CMD_SHIFT_RG:
                nTimeNew   = nTimeIdxAbs + nBitLen
                nTimeStart = self.m_nTimeOffAbs
                nTimeEnd   = nTimeStart + nSectLen
                if self.is_one_half_mode():
                    if self.m_nPeerMode == SEQ_INST_MODE_SECONDARY: # this is secondary
                        nTimeStart += (nSectLen / 2.0)              # add a time offset of 1/2 section from start time
                    else:
                        nTimeEnd   -= (nSectLen / 2.0)              # remove a time offset of 1/2 section from end time
                if nTimeNew < nTimeEnd:
                    aNewNotes.append([nPitxIdxAbs, nTimeNew, nNoteLen, nNoteVel, bNoteMute])
                    bExec = True
                else:
                    aNewNotes.append([nPitxIdxAbs, nTimeNew - nTimeEnd + nTimeStart, nNoteLen, nNoteVel, bNoteMute])
                    bExec = True

        oClip.replace_selected_notes(tuple(aNewNotes))
        oClip.deselect_all_notes() # deselect notes since replacing notes auto-selected them

        if not bExec:
            self.alert('No notes affected. Check selection')

    def on_transpose_button(self):
        if self.m_nTransState == SEQ_TRANS_UNAV:
            self.alert('TRANSPOSE UNAVAILABLE. SELECT A SCALE FIRST.')
        elif self.m_nTransState == SEQ_TRANS_STANDBY:
            self.m_nTransState = SEQ_TRANS_AWAIT
            self.m_nTransScale = self.m_nScale
            sSrcScale = self.m_aScales[self.m_nTransScale][0]
            self.alert('TRANSPOSING, CURRENT SCALE: %s. SELECT A NEW SCALE.' % (sSrcScale))
        elif self.m_nTransState == SEQ_TRANS_AWAIT:
            self.m_nTransState = SEQ_TRANS_STANDBY
            self.m_nTransScale = SEQ_SCALE_UNDEF
        self.update_tools_transpose_button()

    def on_transpose_cmd(self, _hParams):
        sSubCmd = _hParams['subcmd']
        if sSubCmd == 'source':
            self.m_nTransState = SEQ_TRANS_AWAIT
            self.m_nTransScale = self.m_nScale
            sSrcScale = self.m_aScales[self.m_nTransScale][0]
            self.alert('> TRANSPOSING, CURRENT SCALE: %s. SELECT A NEW SCALE.' % (sSrcScale))
            self.update_tools_transpose_button()
        elif sSubCmd == 'cancel':
            self.m_nTransState = SEQ_TRANS_STANDBY
            self.m_nTransScale = SEQ_SCALE_UNDEF
            self.update_tools_transpose_button()
        elif sSubCmd == 'target':
            self.select_scale(_hParams['scale'], True)

    def _on_slider_mode_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        nSliderModeIdx = _oSender.m_hSliderModeData['slider_mode_index']
        self.change_slider_mode(nSliderModeIdx, True)

    def change_slider_mode(self, _nSliderModeIdx, _bLocal):
        if (self.m_nSliderMode == _nSliderModeIdx):
            self.m_nSliderMode = SEQ_SLIDER_MODE_NONE
        else:
            self.m_nSliderMode = _nSliderModeIdx
        self.update_tools_slider_mode_buttons()
        if _bLocal and self.m_bNavSync:
            self.alert('SLIDER MODE: %s' % (self.m_aSliderModes[self.m_nSliderMode]))
            self.send_peer_command('slider_mode', { 'slider_mode_index': self.m_nSliderMode })

    def _on_section_mode_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        nSectionModeIdx = _oSender.m_hSectionModeData['section_mode_index']
        self.section_mode(nSectionModeIdx, True)

    def section_mode(self, _nSectionModeIdx, _bLocal):
        self.m_nSectionMode = _nSectionModeIdx
        if _bLocal:
            self.alert('SECTION MODE: %s' % (self.m_aSectionModes[self.m_nSectionMode]))
        self.update_section_mode_buttons()
        self.update_section_buttons()

    def _on_section_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        nSectionIdx = _oSender.m_hSectionData['section_index']
        self.section_navigate(nSectionIdx, True)

    def section_navigate(self, _nSectionIdx, _bLocal):
        if _nSectionIdx < self.m_nNumSect:
            nLength = self.get_section_length()
            self.m_nTimeOffAbs = _nSectionIdx * nLength
            self.update_beat_grid()
            self.update_zoom_buttons()
            self.update_section_buttons()
            if _bLocal and self.m_bNavSync:
                self.send_peer_command('sect_nav', { 'section_index': _nSectionIdx })
        else:
            self.alert('Section %d out of range!' % (_nSectionIdx))

    # **************************************************************************

    def setup_rhythm_buttons(self):
        for nPitxIdxRel in self.m_rHeight:
            for nTimeIdxRel in self.m_rWidth:
                oButton = self.m_oMatrix.get_button(nTimeIdxRel, nPitxIdxRel)
                oButton.set_on_off_values("Sequencer.Rhythm.%s" % (self.m_aRhythmSkin[nPitxIdxRel][nTimeIdxRel]))

        # connect listeners
        for nTimeIdxRel in self.m_rWidth:
            # shift size
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_SHIFT_SIZE)
            oButton.m_hShiftSizeData = { 'shift_size_index': nTimeIdxRel }
            oButton.add_value_listener(self._on_shift_size_value, identify_sender = True)

            # shift and loop size
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_SHIFT_CMD)
            oButton.m_hShiftCmdData = { 'shift_cmd_index': nTimeIdxRel }
            oButton.add_value_listener(self._on_shift_cmd_value, identify_sender = True)
            oButton.turn_on() # stateless, is a command button!

            # rhythms
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_RHYTHM_CMD)
            oButton.m_hRhythmCmdData = { 'pattern_index': nTimeIdxRel }
            oButton.add_value_listener(self._on_rhythm_cmd_value, identify_sender = True)
            oButton.turn_on() # stateless, is a command button!

            # mul / chop 3
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_NOTE_1_CMD)
            oButton.m_hRhythmNote1CmdData = {
                'rhythm_note_1_cmd_row'  : SEQ_BUT_IDX_NOTE_1_CMD_ROW_1,
                'rhythm_note_1_cmd_index': nTimeIdxRel
            }
            oButton.add_value_listener(self._on_rhythm_note_1_cmd_value, identify_sender = True)

            # div / chop 2
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_NOTE_2_CMD)
            oButton.m_hRhythmNote1CmdData = {
                'rhythm_note_1_cmd_row'  : SEQ_BUT_IDX_NOTE_1_CMD_ROW_2,
                'rhythm_note_1_cmd_index': nTimeIdxRel
            }
            oButton.add_value_listener(self._on_rhythm_note_1_cmd_value, identify_sender = True)

            # commands
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_NOTE_3_CMD)
            oButton.m_hRhythmNote2CmdData = { 'rhythm_note_2_cmd_index': nTimeIdxRel }
            oButton.add_value_listener(self._on_rhythm_note_2_cmd_value, identify_sender = True)
            if nTimeIdxRel > 0:
                oButton.turn_on() # stateless, is a command button!

            # sections
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_SECTIONS)
            oButton.m_hSectionData = { 'section_index': nTimeIdxRel }
            oButton.add_value_listener(self._on_section_value, identify_sender = True)

        # nav, peer, zoom
        self.m_oNavSyncBut = self.m_oMatrix.get_button(0, SEQ_BUT_IDX_CMDS)
        self.m_oNavSyncBut.add_value_listener(self._on_nav_sync_value)
        self.m_oPeerModeBut = self.m_oMatrix.get_button(1, SEQ_BUT_IDX_CMDS)
        self.m_oPeerModeBut.add_value_listener(self._on_peer_mode_value)
        self.m_oZoomModeBut = self.m_oMatrix.get_button(2, SEQ_BUT_IDX_CMDS)
        self.m_oZoomModeBut.add_value_listener(self._on_zoom_mode_value)

        # section mode
        for nTimeIdxRel in range(5):
            oButton = self.m_oMatrix.get_button(nTimeIdxRel + 3, SEQ_BUT_IDX_SECT_MODE)
            oButton.m_hSectionModeData = { 'section_mode_index': nTimeIdxRel }
            oButton.add_value_listener(self._on_section_mode_value, identify_sender = True)

        self.update_stateful_rhythm_buttons()

    def disconnect_rhythm_buttons(self):
        for nTimeIdxRel in self.m_rWidth:
            self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_SHIFT_SIZE).remove_value_listener(self._on_shift_size_value)
            self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_SHIFT_CMD ).remove_value_listener(self._on_shift_cmd_value)
            self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_RHYTHM_CMD).remove_value_listener(self._on_rhythm_cmd_value)
            self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_NOTE_1_CMD).remove_value_listener(self._on_rhythm_note_1_cmd_value)
            self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_NOTE_2_CMD).remove_value_listener(self._on_rhythm_note_1_cmd_value)
            self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_NOTE_3_CMD).remove_value_listener(self._on_rhythm_note_2_cmd_value)
            self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_SECTIONS  ).remove_value_listener(self._on_section_value)
        self.m_oNavSyncBut.remove_value_listener(self._on_nav_sync_value)
        self.m_oPeerModeBut.remove_value_listener(self._on_peer_mode_value)
        self.m_oZoomModeBut.remove_value_listener(self._on_zoom_mode_value)
        for nTimeIdxRel in range(5):
            oButton = self.m_oMatrix.get_button(nTimeIdxRel + 3, SEQ_BUT_IDX_SECT_MODE)
            oButton.remove_value_listener(self._on_section_mode_value)

    def update_stateful_rhythm_buttons(self):
        self.update_shift_size_buttons()
        self.update_rhythm_note_cmd_buttons()
        self.update_nav_sync_button()
        self.update_peer_mode_button()
        self.update_zoom_mode_button()
        self.update_section_mode_buttons()
        self.update_section_buttons()

    def update_rhythm_note_cmd_buttons(self):
        if not self.in_valid_submode(SEQ_SUBMODE_RHYTHM): return
        for nTimeIdxRel in self.m_rWidth:
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_NOTE_1_CMD)
            if self.m_nNoteCmdMode == SEQ_NOTE_CMD_MODE_LEN:
                oButton.turn_on()
            else:
                oButton.turn_off()
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_NOTE_2_CMD)
            if self.m_nNoteCmdMode == SEQ_NOTE_CMD_MODE_LEN:
                oButton.turn_on()
            else:
                oButton.turn_off()
        oButton = self.m_oMatrix.get_button(0, SEQ_BUT_IDX_NOTE_3_CMD)
        if self.m_nNoteCmdMode == SEQ_NOTE_CMD_MODE_LEN:
            oButton.turn_on()
        else:
            oButton.turn_off()

    def update_shift_size_buttons(self):
        for nTimeIdxRel in self.m_rWidth:
            oButton = self.m_oMatrix.get_button(nTimeIdxRel, SEQ_BUT_IDX_SHIFT_SIZE)
            nShiftSizeIdx = oButton.m_hShiftSizeData['shift_size_index']
            if nShiftSizeIdx == self.m_nSizeIdx:
                oButton.turn_on()
            else:
                oButton.turn_off()

    def update_nav_sync_button(self):
        if not self.in_valid_submode(SEQ_SUBMODE_RHYTHM): return
        if self.m_oNavSyncBut != None:
            if self.m_bNavSync:
                self.m_oNavSyncBut.turn_on()
            else:
                self.m_oNavSyncBut.turn_off()

    def update_peer_mode_button(self):
        if not self.in_valid_submode(SEQ_SUBMODE_RHYTHM): return
        if self.m_oPeerModeBut != None:
            if self.m_oPeer == None:
                self.m_oPeerModeBut.set_light('Sequencer.Rhythm.PeerPrim.Unav')
            elif self.m_nPeerMode == SEQ_INST_MODE_PRIMARY:
                self.m_oPeerModeBut.turn_on()
            else:
                self.m_oPeerModeBut.turn_off()

    def update_zoom_mode_button(self):
        if not self.in_valid_submode(SEQ_SUBMODE_RHYTHM): return
        if self.m_nTimeZoomMode == SEQ_TIME_ZOOM_BAR:
            self.m_oZoomModeBut.turn_on()
        else:
            self.m_oZoomModeBut.turn_off()

    def _on_shift_size_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        self.m_nSizeIdx = _oSender.m_hShiftSizeData['shift_size_index']
        self.update_shift_size_buttons()

    def _on_shift_cmd_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        nCmdIdx = _oSender.m_hShiftCmdData['shift_cmd_index']
        oClip = self.get_clip_or_none()
        if oClip == None:
            self.alert('Clip not available!')
            return

        nSize = self.m_aSizes[self.m_nSizeIdx]

        if nCmdIdx == SEQ_SHF_CMD_SONG_STA_DEC:
            oClip.start_marker = oClip.start_marker - nSize
        elif nCmdIdx == SEQ_SHF_CMD_SONG_STA_INC:
            oClip.start_marker = oClip.start_marker + nSize
        elif nCmdIdx == SEQ_SHF_CMD_SONG_END_DEC:
            oClip.end_marker = oClip.end_marker - nSize
        elif nCmdIdx == SEQ_SHF_CMD_SONG_END_INC:
            oClip.end_marker = oClip.end_marker + nSize

        if oClip.looping == False:
            self.alert('Clip not looping!')
            return

        if nCmdIdx == SEQ_SHF_CMD_LOOP_STA_DEC:
            oClip.loop_start = oClip.loop_start - nSize
        elif nCmdIdx == SEQ_SHF_CMD_LOOP_STA_INC:
            if (oClip.loop_start + nSize < oClip.loop_end):
                oClip.loop_start = oClip.loop_start + nSize
        elif nCmdIdx == SEQ_SHF_CMD_LOOP_END_DEC:
            if (oClip.loop_end - nSize > oClip.loop_start):
                oClip.loop_end = oClip.loop_end - nSize
        elif nCmdIdx == SEQ_SHF_CMD_LOOP_END_INC:
            oClip.loop_end = oClip.loop_end + nSize

    def _on_rhythm_cmd_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        if len(self.m_hSelectedPitx) == 0:
            self.alert('No selected notes')
            return
        oClip = self.get_clip_or_none()
        if oClip == None:
            self.alert('Clip not available!')
            return
        nPatternIdx = _oSender.m_hRhythmCmdData['pattern_index']
        self.apply_rhythm_pattern(nPatternIdx)

    def apply_rhythm_pattern(self, _nPatternIdx):
        aRhyPatt  = self.m_aRhythmPatterns[_nPatternIdx]
        nNoteLen  = aRhyPatt[1]
        aPattern  = aRhyPatt[2]
        nNoteVel  = 127
        bNoteMute = False

        aNewNotes = list([]) # (pitch [int], time [float], length [float], velocity [int], muted [boolean])
        for nPitxIdxAbs in self.m_hSelectedPitx:
            for nTimeIdxAbs in aPattern:
                aNewNotes.append([nPitxIdxAbs, self.m_nTimeOffAbs + nTimeIdxAbs, nNoteLen, nNoteVel, bNoteMute])
        oClip = self.get_clip_or_none()
        oClip.replace_selected_notes(tuple(aNewNotes))
        oClip.deselect_all_notes() # deselect notes since replacing notes auto-selected them
        self.alert('Applied rhythm: %s' % (aRhyPatt[0]))

    def _on_rhythm_note_1_cmd_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        nRowIdx = _oSender.m_hRhythmNote1CmdData['rhythm_note_1_cmd_row']
        nCmdIdx = _oSender.m_hRhythmNote1CmdData['rhythm_note_1_cmd_index']
        (nTimeMinAbs, nTimeMaxAbs) = self.get_bit_time_vars(nCmdIdx)

        if self.m_nNoteCmdMode == SEQ_NOTE_CMD_MODE_LEN:
            if nRowIdx == SEQ_BUT_IDX_NOTE_1_CMD_ROW_1: # mul
                self.apply_note_cmd(SEQ_RHYTHM_NOTE_MUL, nTimeMinAbs, nTimeMaxAbs)
            elif nRowIdx == SEQ_BUT_IDX_NOTE_1_CMD_ROW_2: # div
                self.apply_note_cmd(SEQ_RHYTHM_NOTE_DIV, nTimeMinAbs, nTimeMaxAbs)
        else: # self.m_nNoteCmdMode == SEQ_NOTE_CMD_MODE_CHOP
            if nRowIdx == SEQ_BUT_IDX_NOTE_1_CMD_ROW_1: # chop 3
                self.apply_note_cmd(SEQ_RHYTHM_NOTE_CHOP_3, nTimeMinAbs, nTimeMaxAbs)
            elif nRowIdx == SEQ_BUT_IDX_NOTE_1_CMD_ROW_2: # chop 2
                self.apply_note_cmd(SEQ_RHYTHM_NOTE_CHOP_2, nTimeMinAbs, nTimeMaxAbs)

    def _on_rhythm_note_2_cmd_value(self, _nValue, _oSender):
        if (_nValue != BUTTON_ON): return
        nCmdIdx = _oSender.m_hRhythmNote2CmdData['rhythm_note_2_cmd_index']
        (nTimeMinAbs, nTimeMaxAbs) = self.get_master_time_vars()

        if nCmdIdx == SEQ_RHYTHM_NOTE_MODE:
            nNewMode = SEQ_NOTE_CMD_MODE_CHOP if self.m_nNoteCmdMode == SEQ_NOTE_CMD_MODE_LEN else SEQ_NOTE_CMD_MODE_LEN
            self.change_rhythm_note_cmd_mode(nNewMode, True)
        elif nCmdIdx == SEQ_RHYTHM_NOTE_CHOP_2:
            self.apply_note_cmd(SEQ_RHYTHM_NOTE_CHOP_2, nTimeMinAbs, nTimeMaxAbs)
        elif nCmdIdx == SEQ_RHYTHM_NOTE_DIV:
            self.apply_note_cmd(SEQ_RHYTHM_NOTE_DIV, nTimeMinAbs, nTimeMaxAbs)
        elif nCmdIdx == SEQ_RHYTHM_NOTE_MUL:
            self.apply_note_cmd(SEQ_RHYTHM_NOTE_MUL, nTimeMinAbs, nTimeMaxAbs)
        elif nCmdIdx == SEQ_RHYTHM_NOTE_SEL_ALL:
            bDeselectAll = len(self.m_hSelectedPitx) > 0
            self.change_note_selection(not bDeselectAll, True)
        elif nCmdIdx == SEQ_RHYTHM_NOTE_DEL_SEL:
            self.apply_note_cmd(SEQ_RHYTHM_NOTE_DEL_SEL, nTimeMinAbs, nTimeMaxAbs)
        elif nCmdIdx == SEQ_RHYTHM_NOTE_CLEAR:
            oClip = self.get_midi_clip_or_none()
            oClip.remove_notes(0.0, 0, 128.0, 127)
            self.alert('> CLIP CLEARED')
        elif nCmdIdx == SEQ_RHYTHM_LOOP_SHOW:
            oClip = self.get_midi_clip_or_none()
            if (oClip == None): return
            oView = self.application().view
            oView.show_view('Detail')
            oView.focus_view('Detail')
            oView.show_view('Detail/Clip')
            oView.focus_view('Detail/Clip')
            oClip.view.hide_envelope()
            oClip.view.show_loop()
            self.alert('Show loop')

    def apply_note_cmd(self, _nNoteCmd, _nTimeMinAbs, _nTimeMaxAbs, _bSelMode = True):
        if _bSelMode and len(self.m_hSelectedPitx) == 0:
            self.alert('No selected notes')
            return

        bExec   = False
        oClip   = self.get_midi_clip_or_none()
        nBitLen = self.get_bit_length()

        # execute command in notes
        aNotes = self.get_clip_notes()
        for tNote in aNotes: # tNote is a tuple
            # tNote format: Note, Time, Length, Velocity, Mute
            nPitxIdxAbs = tNote[0] # Pitch value, between 0 and 127 [int]
            nTimeIdxAbs = tNote[1] # Time [float]

            if _bSelMode and (not (nPitxIdxAbs in self.m_hSelectedPitx)):
                continue # pitch is not selected, nothing else to do here
            if (nTimeIdxAbs < _nTimeMinAbs or nTimeIdxAbs >= _nTimeMaxAbs):
                continue # nothing else to do for this note since is not inside the time range

            nNoteLen  = tNote[2] # note length [float]
            nNoteVel  = tNote[3] # note velocity [int]
            bNoteMute = tNote[4] # mute flag [boolean]
            aNewNotes = list([]) # (pitch [int], time [float], length [float], velocity [int], muted [boolean])

            # remove note
            # (from_time [double], from_pitch [int], time_span [double], pitch_span [int])
            oClip.remove_notes(nTimeIdxAbs, nPitxIdxAbs, nNoteLen, 1)

            if _nNoteCmd == SEQ_RHYTHM_NOTE_CHOP_2:
                nNoteLenChop = nNoteLen / 2.0
                aNewNotes.append([nPitxIdxAbs, nTimeIdxAbs               , nNoteLenChop, nNoteVel, bNoteMute])
                aNewNotes.append([nPitxIdxAbs, nTimeIdxAbs + nNoteLenChop, nNoteLenChop, nNoteVel, bNoteMute])
                bExec = True
            elif _nNoteCmd == SEQ_RHYTHM_NOTE_CHOP_3:
                nNoteLenChop = nNoteLen / 3.0
                aNewNotes.append([nPitxIdxAbs, nTimeIdxAbs                   , nNoteLenChop, nNoteVel, bNoteMute])
                aNewNotes.append([nPitxIdxAbs, nTimeIdxAbs + nNoteLenChop    , nNoteLenChop, nNoteVel, bNoteMute])
                aNewNotes.append([nPitxIdxAbs, nTimeIdxAbs + nNoteLenChop * 2, nNoteLenChop, nNoteVel, bNoteMute])
                bExec = True
            elif _nNoteCmd == SEQ_RHYTHM_NOTE_DIV:
                nNoteLenDiv = nNoteLen / 2.0
                aNewNotes.append([nPitxIdxAbs, nTimeIdxAbs, nNoteLenDiv, nNoteVel, bNoteMute])
                bExec = True
            elif _nNoteCmd == SEQ_RHYTHM_NOTE_MUL:
                nNoteLenMul = nNoteLen * 2.0
                aNewNotes.append([nPitxIdxAbs, nTimeIdxAbs, nNoteLenMul, nNoteVel, bNoteMute])
                bExec = True
            elif _nNoteCmd == SEQ_RHYTHM_NOTE_DEL_SEL:
                bExec = True
                continue # just remove the notes and continue

            oClip.replace_selected_notes(tuple(aNewNotes))
            oClip.deselect_all_notes() # deselect notes since replacing notes auto-selected them

        if not bExec:
            self.alert('NO NOTES AFFECTED. CHECK SELECTION')

    def change_rhythm_note_cmd_mode(self, _nNewMode, _bLocal):
        self.m_nNoteCmdMode = _nNewMode
        self.update_rhythm_note_cmd_buttons()
        if _bLocal and self.m_bNavSync:
            self.send_peer_command('change_rhythm_note_cmd_mode', {'new_note_cmd_mode': _nNewMode})
            if self.m_nNoteCmdMode == SEQ_NOTE_CMD_MODE_LEN:
                self.alert('NOTE COMMAND MODE: LENGTH')
            else:
                self.alert('NOTE COMMAND MODE: CHOP')

    def change_note_selection(self, _bSelectAll, _bLocal):
        self.m_hSelectedPitx = {}
        if _bSelectAll:
            for nIdx in range(128):
                self.m_hSelectedPitx[nIdx] = True
            self.alert('All notes selected')
        else:
            self.alert('All notes deselected')
        self.update_note_sel_zoom_buttons()
        self.update_note_sel_buttons()
        if _bLocal:
            self.send_peer_command('change_note_sel', {'select_all': _bSelectAll})

    def _on_nav_sync_value(self, _nValue):
        if (_nValue != BUTTON_ON): return
        self.nav_sync_toggle(not self.m_bNavSync, self.m_nPitxOffAbs, self.m_nTimeOffAbs, True)

    def nav_sync_toggle(self, _bNavSync, _nPitxOffAbs, _nTimeOffAbs, _bLocal):
        self.m_bNavSync = _bNavSync
        if _bNavSync:
            # re-sync beat grid offsets if we are toggling on navigation sync
            nTimeLength = self.get_section_length()
            self.m_nPitxOffAbs = (_nPitxOffAbs / LEN_ONE_OCT) * LEN_ONE_OCT # floor(pitch)
            self.m_nTimeOffAbs = (_nTimeOffAbs / nTimeLength) * nTimeLength # floor(time)
            self.update_beat_grid()
        self.update_nav_sync_button()
        if _bLocal:
            self.send_peer_command('nav_sync', {
                'nav_sync_val': _bNavSync,
                'pitx_off_abs': self.m_nPitxOffAbs,
                'time_off_abs': self.m_nTimeOffAbs,
            })

    def _on_peer_mode_value(self, _nValue):
        if (_nValue != BUTTON_ON): return
        nPeerMode = SEQ_INST_MODE_SECONDARY if self.m_nPeerMode == SEQ_INST_MODE_PRIMARY else SEQ_INST_MODE_PRIMARY
        self.peer_mode_toggle(nPeerMode, True)

    def peer_mode_toggle(self, _nPeerMode, _bLocal):
        nCounterPeerMode = self.m_nPeerMode # remote's new peer mode
        self.m_nPeerMode = _nPeerMode       # local's  new peer mode
        self.update_peer_mode_button()
        self.update_beat_grid()
        if _bLocal:
            self.send_peer_command('peer_mode', {
                'new_peer_mode': nCounterPeerMode,
            })

    def _on_zoom_mode_value(self, _nValue):
        if (_nValue != BUTTON_ON): return
        nZoomMode = SEQ_TIME_ZOOM_PHRASE if self.m_nTimeZoomMode == SEQ_TIME_ZOOM_BAR else SEQ_TIME_ZOOM_BAR
        self.zoom_mode_toggle(nZoomMode, True)

    def zoom_mode_toggle(self, _nZoomMode, _bLocal):
        self.m_nTimeZoomMode = _nZoomMode
        self.m_nNoteLength   = self.get_bit_length()
        self.m_nNoteShift    = 0.0
        self.update_zoom_mode_button()
        self.update_beat_grid()
        self.update_zoom_buttons()
        self.update_section_buttons()
        if _bLocal:
            self.send_peer_command('zoom_mode', {'new_zoom_mode': _nZoomMode})

    # **************************************************************************

    def _on_sel_scene_changed(self):
        return self.update_stateful_controls()

    def _on_sel_track_changed(self):
        return self.update_stateful_controls()

    def update_stateful_controls(self):
        if (self.m_bEnabled == False): return SEQ_SUBMODE_UNDEFINED
        self.connect_controls(SEQ_SUBMODE_NOTES)
        return SEQ_SUBMODE_NOTES

    def on_shift_value(self):
        bDeselectAll = len(self.m_hSelectedPitx) > 0
        self.change_note_selection(not bDeselectAll, True)

    # **************************************************************************

    def get_matrix_button(self, _nPitxIdxRel, _nTimeIdxRel):
        nRow = self.m_nHeight - _nPitxIdxRel - 1
        nCol = _nTimeIdxRel
        return self.m_oMatrix.get_button(nCol, nRow)

    def is_note_visible(self, _nPitxIdxAbs, _nTimeIdxAbs):
        nPitxIdxRel = self.note_pitx_rel(_nPitxIdxAbs)
        nTimeIdxRel = self.note_time_rel(_nTimeIdxAbs)
        nPitxMax    = self.note_pitx_rel_max()
        nTimeMax    = self.m_nWidth
        return (nPitxIdxRel >= 0 and nPitxIdxRel < nPitxMax
            and nTimeIdxRel >= 0 and nTimeIdxRel < nTimeMax)

    def is_root_note(self, _nPitxIdxAbs):
        if (self.m_nScale == SEQ_SCALE_CHROMATIC):
            return (_nPitxIdxAbs % LEN_ONE_OCT == 0)
        return (_nPitxIdxAbs % LEN_ONE_OCT == self.m_nRootPitx)

    def get_pitx_shift(self):
        if (self.m_nScale == SEQ_SCALE_CHROMATIC):
            return SEQ_PITX_SHIFT_CHROM
        return LEN_ONE_OCT # up or down a complete octave for the rest of the scales

    def is_note_selected(self, _nPitxIdxAbs, _nTimeIdxAbs, _bAllMode):
        if _bAllMode or (_nPitxIdxAbs in self.m_hSelectedPitx):
            nLen  = self.get_section_length()
            nSpan = self.m_aSectionFactr[self.m_nSectionMode] * nLen
            if self.m_bNavSync == False:
                nSpan = nSpan / 2.0
            nTime = self.m_nTimeOffAbs
            if self.is_one_half_secondary_mode():
                nTime += nLen / 2.0 # add a time offset of 1/2 section
            return _nTimeIdxAbs >= nTime and _nTimeIdxAbs < (nTime + nSpan)
        return False

    def is_pitx_selected(self, _nPitxIdxRel):
        nPitxIdxAbs = self.note_pitx_abs(_nPitxIdxRel)
        return nPitxIdxAbs in self.m_hSelectedPitx

    def note_pitx_rel_max(self):
        if self.m_nScale == SEQ_SCALE_CHROMATIC:
            return self.m_nHeight # only first 8 notes
        else:
            return (LEN_ONE_OCT + 1) # full scale

    def note_pitx_rel(self, _nPitxIdxAbs):
        nPitxRelChr = _nPitxIdxAbs - self.m_nPitxOffAbs
        if self.m_nScale == SEQ_SCALE_CHROMATIC:
            return nPitxRelChr
        else:
            nPitxRelChr   = nPitxRelChr - self.m_nRootPitx
            aScaleOffsets = self.m_aScales[self.m_nScale][1]
            if nPitxRelChr in aScaleOffsets:
                return aScaleOffsets.index(nPitxRelChr)
            return -1 # the pitch is not available in the current scale

    def note_pitx_abs(self, _nNotePitxRel):
        if self.m_nScale == SEQ_SCALE_CHROMATIC:
            return _nNotePitxRel + self.m_nPitxOffAbs
        else:
            aScaleOffsets = self.m_aScales[self.m_nScale][1]
            return aScaleOffsets[_nNotePitxRel] + self.m_nPitxOffAbs + self.m_nRootPitx

    def get_pitx_offset_abs_for_octave(self, _nOctave):
        return (_nOctave + 2) * LEN_ONE_OCT

    def get_time_shift(self, _bZoomMode):
        if _bZoomMode:
            # in zoom mode we always navigate in a whole bar / phrase units
            if self.m_nTimeZoomMode == SEQ_TIME_ZOOM_BAR:
                return LEN_ONE_BAR
            return LEN_ONE_PHRASE
        else:
            # in this case the user is navigating with the left, right nav buttons
            if self.m_bNavSync:
                # we have sync navigation so we navigate in a whole bar / phrase units
                if self.m_nTimeZoomMode == SEQ_TIME_ZOOM_BAR:
                    return LEN_ONE_BAR
                return LEN_ONE_PHRASE
            else:
                # no sync navigate! we navigate in half bar / phrase units
                if self.m_nTimeZoomMode == SEQ_TIME_ZOOM_BAR:
                    return LEN_ONE_BAR / 2
                return LEN_ONE_PHRASE / 2

    def note_time_rel(self, _nTimeIdxAbs):
        nTimeOffset = self.get_time_offset() + self.m_oClip.loop_start
        if self.m_nTimeZoomMode == SEQ_TIME_ZOOM_BAR:
            return int((_nTimeIdxAbs - self.m_nTimeOffAbs - nTimeOffset) * float(LEN_ONE_BAR))
        else:
            return int(_nTimeIdxAbs - self.m_nTimeOffAbs - nTimeOffset)

    def note_time_abs(self, _nNoteTimeIdxRel):
        nTimeOffset = self.get_time_offset() + self.m_oClip.loop_start
        if self.m_nTimeZoomMode == SEQ_TIME_ZOOM_BAR:
            return float(_nNoteTimeIdxRel) / float(LEN_ONE_BAR) + self.m_nTimeOffAbs + nTimeOffset
        else:
            return float(_nNoteTimeIdxRel) + self.m_nTimeOffAbs + nTimeOffset

    def get_time_offset(self):
        if self.m_oPeer != None:
            if self.m_bNavSync and self.m_nPeerMode == SEQ_INST_MODE_SECONDARY:
                 if self.m_nTimeZoomMode == SEQ_TIME_ZOOM_BAR:
                     return LEN_ONE_BAR / 2
                 else:
                     return LEN_ONE_PHRASE / 2
        return 0 # no offset if no-nav-sync or if primary instance (or when there is no peer)

    def create_empty_midi_clip(self):
        oTrack = self.sel_track()
        if (not oTrack.has_midi_input): return None
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot == None): return None
        if (oClipSlot.has_clip): return None # it should be an empty clip
        nLength = self.get_section_length()
        oClipSlot.create_clip(nLength)

    def get_section_length(self):
        nLength = LEN_ONE_BAR if self.m_nTimeZoomMode == SEQ_TIME_ZOOM_BAR else LEN_ONE_PHRASE
        return nLength

    def get_surface_length(self):
        return self.get_section_length() / 2.0

    def get_bit_length(self):
        return self.get_surface_length() / 8.0

    def get_master_time_vars(self):
        nTimeSpan = self.get_surface_length()
        if self.m_nSectionMode == SEQ_SECTION_MODE_1_2:
            nTimeSpan *= 1.0
        elif self.m_nSectionMode == SEQ_SECTION_MODE_1:
            nTimeSpan *= 2.0
        elif self.m_nSectionMode == SEQ_SECTION_MODE_2:
            nTimeSpan *= 4.0
        elif self.m_nSectionMode == SEQ_SECTION_MODE_4:
            nTimeSpan *= 8.0
        elif self.m_nSectionMode == SEQ_SECTION_MODE_8:
            nTimeSpan *= 16.0
        nTimeMinAbs = self.m_nTimeOffAbs
        nTimeMaxAbs = nTimeMinAbs + nTimeSpan
        if self.is_one_half_secondary_mode():
            nTimeMinAbs += self.get_surface_length()
            nTimeMaxAbs += self.get_surface_length()
        return (nTimeMinAbs, nTimeMaxAbs)

    def get_bit_time_vars(self, _nTimeIdxRel):
        nBitLen     = self.get_bit_length()
        nTimeMinAbs = self.m_nTimeOffAbs + (_nTimeIdxRel * nBitLen)
        nTimeMaxAbs = nTimeMinAbs + nBitLen
        if self.is_secondary_mode():
            nTimeMinAbs += self.get_surface_length()
            nTimeMaxAbs += self.get_surface_length()
        return (nTimeMinAbs, nTimeMaxAbs)

    def sel_clip_slot(self):
        return self.song().view.highlighted_clip_slot

    def get_midi_slot_or_none(self):
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot == None): return None
        oTrack = self.sel_track()
        if (oTrack.has_midi_input):
            return oClipSlot
        return None

    def get_clip_or_none(self):
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot == None): return None
        return oClipSlot.clip

    def get_midi_clip_or_none(self):
        oClipSlot = self.sel_clip_slot()
        if (oClipSlot == None): return None
        oClip = oClipSlot.clip
        if (oClip == None): return None
        if (not oClip.is_midi_clip): return None
        return oClip

    def get_midi_track_or_none(self):
        oTrack = self.sel_track()
        if (oTrack.has_midi_input):
            return oTrack
        return None

    def sel_track(self):
        return self.song().view.selected_track

    def get_clip_notes(self):
        self.m_oClip.select_all_notes()
        aNotes = self.m_oClip.get_selected_notes()
        self.m_oClip.deselect_all_notes()
        return aNotes;

    def in_valid_submode(self, _nSubMode):
        if self.m_bEnabled   == False               : return False
        if self.m_nClipState != SEQ_CLIP_STATE_READY: return False
        if self.m_nSubMode   != _nSubMode           : return False
        return True

    def is_one_half_mode(self):
        if (self.m_bNavSync     == True and               # synced surfaces and
            self.m_nSectionMode == SEQ_SECTION_MODE_1_2): # and section mode is 1/2 section
            return True
        return False

    def is_one_half_secondary_mode(self):
        if (self.m_bNavSync     == True and                    # synced surfaces and
            self.m_nPeerMode    == SEQ_INST_MODE_SECONDARY and # this is secondary
            self.m_nSectionMode == SEQ_SECTION_MODE_1_2):      # and section mode is 1/2 section
            return True
        return False

    def is_secondary_mode(self):
        if (self.m_bNavSync  == True and                  # synced surfaces and
            self.m_nPeerMode == SEQ_INST_MODE_SECONDARY): # this is secondary
            return True
        return False

    # ****************************************************************

    def log(self, _sMessage):
        Live.Base.log(_sMessage)

    def alert(self, _sMessage):
        self.m_oCtrlInst.show_message(_sMessage)

