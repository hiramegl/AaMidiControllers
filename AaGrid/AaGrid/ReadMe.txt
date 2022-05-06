APC MINI - MIDI MAPPING
=======================

Channel 1 (MIDI 0)
0 -> 98 (NOTE ON, NOTE OFF)
VALUE = 127

    1    2    3    4    5    6    7    8
  +---------------------------------------+------+
8 | 56   57   58   59   60   61   62   63 |  82  |                             Stop
7 | 48   49   40   51   52   53   54   55 |  83  |                             Solo
6 | 40   41   42   43   44   45   46   47 |  84  |                             Arm
5 | 32   33   34   35   36   37   38   39 |  85  |                             Mute
4 | 24   25   26   27   28   29   30   31 |  86  |                             Select
3 | 16   17   18   19   20   21   22   23 |  87  |                             -
2 | 8    9    10   11   12   13   14   15 |  88  |                             -
1 | 0    1    2    3    4    5    6    7  |  89  |                             Stop all
  +---------------------------------------+------+
  | 64   65   66   67   68   69   70   71 |  98  | ^ v < > Vol Pan Send Device Shift
  +---------------------------------------+------+
  | 48   49   50   51   52   53   54   55 |  56  | <- CONTROL
  +---------------------------------------+------+

===================================================

loading a clip:
---------------
    read notes
    discard non-visible notes
        check if note is inside the visible absolute pitch range,
        * in chromatic mode is ["pitch offset", "pitch offset" + 7]
        * in scale     mode is ["pitch offset" + "root note", "pitch offset" + "root note" + 12]
        if is in visible range then draw it in correct pitch row
           * in chromatic mode is "note pitch" - "pitch offset" = relative pitch
           * in scale     mode is "note pitch" - "pitch offset" - "root note" = relative pitch
             -> find the index of the button by matching with the selected scale and root note,
                add it to the "scale cache" (NOT THE ABSOLUTE PITCH!, but with OCTAVE and RELATIVE PITCH [0 ... 6])
             -> if the pitch is not found then IGNORE the note, it will be present in live's clip but will not be displayed in the surface controller

changing scale or root note:
---------------------------
    the "scale cache" contains objects:
       { 'octave': <oct>, 'rel_pitch': <rel_pitch>, 'abs_time': <abs_time> }
    and is used to allow a user to change scale or root note while keeping track of the activated notes
    when the user changes scale or root note we will go and check the "scale cache" and re-compute the real ABSOLUTE PITCH MIDI values

adding a note to a clip:
-----------------------
    receive note
    compute the absolute pitch value of the note:
        * in chromatic mode is "note pitch" + "pitch offset" = absolute pitch
        * in scale     mode is "note pitch" + "pitch offset" + "root note"
    add it to the "scale cache" (NOT THE ABSOLUTE PITCH!, but with OCTAVE and RELATIVE PITCH [0 ... 6])

===================================================

     1            2            3            4            5            6            7            8               Scene
   +--------------------------------------------------------------------------------------------------------+-------------+
 8 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | SEL NOTE  7 |
 7 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | SEL NOTE  6 |
 6 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | SEL NOTE  5 |
 5 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | SEL NOTE  4 |
 4 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | SEL NOTE  3 |
 3 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | SEL NOTE  2 |
 2 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | SEL NOTE  1 |
 1 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] | SEL NOTE  0 |
   +--------------------------------------------------------------------------------------------------------+-------------+
   | OCT UP       OCT DW       SECT LEFT    SECT RGHT    SESSION      MIXER        SEQUENCER    TOOLS       | SEL/DES ALL |
   +--------------------------------------------------------------------------------------------------------+-------------+
   | BIT 1.1      BIT 1.2      BIT 1.3      BIT 1.4      BIT 2.1      BIT 2.2      BIT 2.3      BIT 2.4     |    SLIDER   |
   +--------------------------------------------------------------------------------------------------------+-------------+

     1            2            3            4            5            6            7            8               Scene
   +--------------------------------------------------------------------------------------------------------+-------------+
 8 | [ OCTV  2 ]  [ OCTV  7 ]  [ ION MAJ ]  [ ION MIN ]  [ HAR MAJ ]  [ MEL MAJ ]  [ HAR MIN ]  [ MEL MIN ] | SEL NOTE  7 |
 7 | [ OCTV  1 ]  [ OCTV  6 ]  [ DORIAN  ]  [ PHRYGIN ]  [ LYDIAN  ]  [ MIXOLYD ]  [ AEOLIAN ]  [ LOCRIAN ] | SEL NOTE  6 |
 6 | [ OCTV  0 ]  [ OCTV  5 ]  [    C    ]  [   C #   ]  [    D    ]  [   D #   ]  [    E    ]  [    F    ] | SEL NOTE  5 |
 5 | [ OCTV -1 ]  [ OCTV  4 ]  [   F #   ]  [    G    ]  [   G #   ]  [    A    ]  [   A #   ]  [    B    ] | SEL NOTE  4 |
 4 | [ OCTV -2 ]  [ OCTV  3 ]  [ STA DIV ]  [ STA MUL ]  [ MID DIV ]  [ MID MUL ]  [ END DIV ]  [ END MUL ] | SEL NOTE  3 |
 3 | [ TRANSPS ]  [  MUTE   ]  [  SOLO   ]  [ NOTE UP ]  [ NOTE DW ]  [ SHFT LF ]  [  SHF RG ]  [ LP DUPL ] | SEL NOTE  2 |
 2 | [  VELOC  ]  [ LENGTH  ]  [ SHF FIN ]  [ SEC 1/2 ]  [  SEC 1  ]  [  SEC 2  ]  [  SEC 4  ]  [  SEC 8  ] | SEL NOTE  1 |
 1 | [    1    ]  [    2    ]  [    3    ]  [    4    ]  [    5    ]  [    6    ]  [    7    ]  [    8    ] | SEL NOTE  0 |  <- BAR / PHRASE SELECT
   +--------------------------------------------------------------------------------------------------------+-------------+
   | OCT UP       OCT DW       SECT LEFT    SECT RIGHT   SESSION      MIXER        SEQUENCER    TOOLS       | SEL/DES ALL |
   +--------------------------------------------------------------------------------------------------------+-------------+
   | BIT 1.1      BIT 1.2      BIT 1.3      BIT 1.4      BIT 2.1      BIT 2.2      BIT 2.3      BIT 2.4     |    SLIDER   |
   +--------------------------------------------------------------------------------------------------------+-------------+

CH_MODE -> Change mode of clip (only available when a mode is selected)
MUTE    -> Mute                selected notes
SOLO    -> Solo                selected notes
NOTE UP -> Move note one semitone up
NOTE DW -> Move note one semitone down
SHFT LF -> Move note one bit left
SHFT RG -> Move note one bit right

VELOC   -> Change velocity     of selected notes: SEL NOTE, BIT, VALUE (VELOCITY: 0 .. 127)
LENGTH  -> Change length       of selected notes: SEL NOTE, BIT, VALUE (LENGTH  : 1 .. 64 BITS (16 BEATS = 4 BARS)
SHF FIN -> Fine shift position of selected notes: SEL NOTE, BIT, VALUE (SHIFT   : [0 .. 7] * 1/8 BIT)
SECTION -> Section MODE: 1/2, 1, 2, 4, 8 [bar/phase]

# octave 8 is incomplete! only the first 8 semitones are avaiable!

Octaves
-------
 8 = 120 ... 127          Chrom        Chrom
 7 = 108 ... 119          Top          Bottom
 6 =  96 ... 107          -------      -----
 5 =  84 ...  95          127   8      7   8
 4 =  72 ...  83          126   7      6   7
 3 =  60 ...  71          125   6      5   6
 2 =  48 ...  59          124   5      4   5
 1 =  36 ...  47          123   4      3   4
 0 =  24 ...  35          122   3      2   3
-1 =  12 ...  23          121   2      1   2
-2 =   0 ...  11          120 - 1      0 - 1

     1            2            3            4            5            6            7            8             Scene
   +--------------------------------------------------------------------------------------------------------+-------------+
 8 | [  1 / 8  ]  [  1 / 4  ]  [  1 / 2  ]  [    1    ]  [    2    ]  [    4    ]  [    8    ]  [   1 6   ] | SEL NOTE  7 | <- Shift delta
 7 | [ STA DEC ]  [ STA INC ]  [ END DEC ]  [ END INC ]  [ LPSTDEC ]  [ LPSTINC ]  [ LPENDEC ]  [ LPENINC ] | SEL NOTE  5 | <- Shift: start, end / song, loop
 6 | [  HOUSE  ]  [ HOUSE 2 ]  [  ZOUK   ]  [  RGTTN  ]  [  SALSA  ]  [ REGGAE  ]  [ TRIPLET ]  [ FILLALL ] | SEL NOTE  4 | <- Rhythms
 5 | [ MUL/CH3 ]  [ MUL/CH3 ]  [ MUL/CH3 ]  [ MUL/CH3 ]  [ MUL/CH3 ]  [ MUL/CH3 ]  [ MUL/CH3 ]  [ MUL/CH3 ] | SEL NOTE  3 |
 4 | [ DIV/CH2 ]  [ DIV/CH2 ]  [ DIV/CH2 ]  [ DIV/CH2 ]  [ DIV/CH2 ]  [ DIV/CH2 ]  [ DIV/CH2 ]  [ DIV/CH2 ] | SEL NOTE  3 |
 3 | [ CMD_MOD ]  [ C H O P ]  [   DIV   ]  [   MUL   ]  [ SEL_ALL ]  [ DEL SEL ]  [  CLEAR  ]  [ LP SHOW ] | SEL NOTE  2 |
 2 | [ NAVSYNC ]  [ PRIMARY ]  [ Z O O M ]  [ SEC 1/2 ]  [  SEC 1  ]  [  SEC 2  ]  [  SEC 4  ]  [  SEC 8  ] | SEL NOTE  1 |
 1 | [    1    ]  [    2    ]  [    3    ]  [    4    ]  [    5    ]  [    6    ]  [    7    ]  [    8    ] | SEL NOTE  0 |  <- BAR / PHRASE SELECT
   +--------------------------------------------------------------------------------------------------------+-------------+
   | OCT UP       OCT DW       SECT LEFT    SECT RIGHT   SESSION      MIXER        SEQUENCER    TOOLS       | SEL/DES ALL |
   +--------------------------------------------------------------------------------------------------------+-------------+
   | -            -            -            -            -            -            -            -           |  -          |
   +--------------------------------------------------------------------------------------------------------+-------------+

BEATS & MELODIES

NAVSYNC -> Navigation sync (moving affects both surfaces)
PRIMARY -> Make this the primary surface
ZOOM    -> Sequencer zoom mode: (affects both surfaces always)
           2 beats (for building melody or rhythm)
           2 bars  (for building harmony chords)
ALL_CHR -> Select / deselect all (chromatic mode)
ALL_SCA -> Select / deselect all (scale mode)

CMD_MOD -> Toggle of note command buttons: mul + div / chop3 + chop2
DIV     -> Divide    by 2 len  selected notes
MUL     -> Multipliy by 2 len  selected notes

TOOLS / LOOP, CLIP, SESSION

     1            2            3            4            5            6            7            8             Scene
   +--------------------------------------------------------------------------------------------------------+-------------+
 8 | [  1 / 8  ]  [  1 / 4  ]  [  1 / 2  ]  [    1    ]  [    2    ]  [    4    ]  [    8    ]  [   1 6   ] |  SEL SCENE  |
 7 | [ < SHIFT ]  [ SHIFT > ]  [ / START ]  [ * START ]  [ / MIDDL ]  [ * MIDDL ]  [  / END  ]  [  * END  ] |  SEL SCENE  |
 6 | [ < BEGIN ]  [ BEGIN > ]  [    1    ]  [    2    ]  [ LP TOGG ]  [ LP DUPL ]  [ ENV SHW ]  [ LP SHOW ] |  SEL SCENE  |
 5 | [ BEAT 1a ]  [ BEAT 1b ]  [ BEAT 2a ]  [ BEAT 2b ]  [ BEAT 3a ]  [ BEAT 3b ]  [ BEAT 4a ]  [ BEAT 4b ] |  SEL SCENE  |
 4 | [ BEAT  1 ]  [ BEAT  2 ]  [ BEAT  3 ]  [ BEAT  4 ]  [ BEAT  5 ]  [ BEAT  6 ]  [ BEAT  7 ]  [ BEAT  8 ] |  SEL SCENE  |
 3 | [ TRN RES ]  [ DET RES ]  [ GAI RES ]  [  CROP   ]  [ QUANTIZ ]  [  WARP   ]  [  METRO  ]  [ FOLLOW  ] |  SEL SCENE  |
 2 | [ PLAY CL ]  [ STOP CL ]  [ DUPL CL ]  [ REWIND  ]  [ FORWARD ]  [ SES PLY ]  [ SES STP ]  [ RECORD  ] |  SEL SCENE  |
 1 | [ SEL TRK ]  [ SEL TRK ]  [ SEL TRK ]  [ SEL TRK ]  [ SEL TRK ]  [ SEL TRK ]  [ SEL TRK ]  [ SEL TRK ] |  SEL SCENE  |
   +--------------------------------------------------------------------------------------------------------+-------------+
   | ^            v            <            >            ?            ?            ?            ?           |  ?          |
   +--------------------------------------------------------------------------------------------------------+-------------+
   | TRANSPOSE    DETUNE       GAIN         ?            ?            ?            ?            ?           |  ?          |
   +--------------------------------------------------------------------------------------------------------+-------------+

   crossfade?
   clip warp
   clip gain
   pitch coarse
   pitch fine

   song nudge down
   song nudge up
   song tempo_follow_enabled
   song overdub
   song punch_in
   song punch_out
   song record_mode
   song select_on_launch
   song session_record
   song tempo
   song undo
   song redo
   song stop_all_clips
   song stop_playing

#===================================================================================================

C major = Ionian     mode
D       = Dorian     mode (e.g. "Drunken Sailor")
E       = Phrygian   mode
F       = Lydian     mode (the Simpsons opening theme)
G       = Myxolydian mode ("Royals")
A       = Aeolian    mode "natural minor" (countless songs)
B       = Locrian    mode

1 Ionian      1   2   3   4   5   6   7
2 Dorian      1   2   3b  4   5   6   7b
3 Phrygian    1   2b  3b  4   5   6b  7b
4 Lydian      1   2   3   4#  5   6   7
5 Myxolydian  1   2   3   4   5   6   7b
6 Aeolian     1   2   3b  4   5   6b  7b
7 Locrian     1   2b  3b  4   5b  6b  7b

            1  2  3  4  5  6  7  8
Ion Maj     0  2  4  5  7  9  11 12
Ion Min     0  2  3  5  7  8  10 12
Har Maj     0  2  4  5  7  8  11 12
Har Min     0  2  3  5  7  8  11 12
Mel Maj     0  2  4  5  7  8  10 12
Mel Min     0  2  3  5  7  9  11 12

Har Maj     1  2  3  4  5 b6  7
Har Min     1  2 b3  4  5 b6  7
Mel Maj     1  2  3  4  5 b6 b7
Mel Min     1  2 b3  4  5  6  7

'Diminished',       [0, 1, 3, 4, 6, 7, 9, 10],
'Whole-half',       [0, 2, 3, 5, 6, 8, 9, 11],
'Whole Tone',       [0, 2, 4, 6, 8, 10],
'Minor Blues',      [0, 3, 5, 6, 7, 10],
'Minor Pentatonic', [0, 3, 5, 7, 10],
'Major Pentatonic', [0, 2, 4, 7, 9],
'Harmonic Minor',   [0, 2, 3, 5, 7, 8, 11],
'Melodic Minor',    [0, 2, 3, 5, 7, 9, 11],
'Super Locrian',    [0, 1, 3, 4, 6, 8, 10],
'Bhairav',          [0, 1, 4, 5, 7, 8, 11],
'Hungarian Minor',  [0, 2, 3, 6, 7, 8, 11],
'Minor Gypsy',      [0, 1, 4, 5, 7, 8, 10],
'Hirojoshi',        [0, 2, 3, 7, 8],
'In-Sen',           [0, 1, 5, 7, 10],
'Iwato',            [0, 1, 5, 6, 10],
'Kumoi',            [0, 2, 3, 7, 9],
'Pelog',            [0, 1, 3, 4, 7, 8],
'Spanish',          [0, 1, 3, 4, 5, 6, 8, 10],
'IonEol',           [0, 2, 3, 4, 5, 7, 8, 9, 10, 11]


**************************************************

SCALES:
                      1  2  3  4  5  6  7  8
         MAJOR scale: 0  2  2  1  2  2  2  1 = 12
NATURAL  MINOR scale: 0  2  1  2  2  1  2  2 = 12 (sad, sunburn)
HARMONIC MINOR SCALE: 0  2  1  2  2  1 [3] 1 = 12 (middle east, change 1 note , only used when going upward in the scale, double sharp symbol = x)
MELODIC  MINOR SCALE: 0  2  1  2  2 [2  2] 1 = 12 (melancholy , change 2 notes, only used when going upward in the scale)

**************************************************

DIATONIC INTERVALS

4 qualities of triads
Maj: 0 + 4 + 3 = 7
Min: 0 + 3 + 4 = 7 (sad)
Dim: 0 + 3 + 3 = 6 (serious)
Aug: 0 + 4 + 4 = 8 (bit out of tune)

**************************************************

MAJOR KEY TRIADS

M    m    m    M    M    m    °    M
I    ii   iii  IV   V    vi   vii° I

C    Dm   Em   F    G    Am   B°   C

**************************************************

MINOR KEY TRIADS

m    °    M    m    m    M    M    m
i    ii°  III  iv   v    VI   VII  i

Am   B°   C    Dm   Em   F    G    Am

**************************************************

        MAJOR scales have a LEADING  TONE builtin (7th to 8th is one SEMITONE difference)
NATURAL MINOR scales have a SUBTONIC TONE         (7th to 8th is one TONE     difference)

HARMONIC MINOR scale has 3 chords which differ from NATURAL MINOR:
          M+        Md        m°
i   ii°   III+  iv  V   VI    vii°

III+ (augmented) : has surprise/suspicion/creepier character (not common in pop music)
Vd               : "dominant" chord (Extremely common to use V instead of v in pop songs with minor scale, pulls back to the tone 1)
VII° (diminished): Diminished Leading Tone "Pull" (common in classical music)

MELODIC MINOR scale has 6 chords which differ from NATURAL MINOR:
     m    M+   M    M    m°   m°
i    ii   III+ IV   V    vi°  vii°

     NATURAL MINOR     HARMONIC MINOR      MELODIC MINOR
A                -O-                -O-                -O-
G               O                 #O                 #O       7
F |-----------O------------------O-----------------#O---------6-
E |         O                  O                  O           5
D |-------O------------------O------------------O-------------4-
C |     O                  O                  O               3
B |---O------------------O------------------O-----------------2-
A | O                  O                  O                   1
G |-------------------------------------------------------------
F |
E |-------------------------------------------------------------
                          Raise 7th      Raise 6th and 7th

**************************************************

TRIAD/CHORD INVERSIONS

       1st 2nd
F |-----------
E |        O
D |-----------
C |     O  O
B |-----------
A |
G |--O--O--O--
F |
E |--O--O-----
D
C  --O--

1st inversion: Root         changed position, one octave up
2nd inversion: Root and 3rd changed position, one octave up

**************************************************

POWER CHORD

C5, B5, A5

**************************************************

MYXOLIDIAN SCALE/MODE

Same as MAJOR but 7th is LOWERED

PHRYGIAN SCALE/MODE

Same as MINOR but 2nd is LOWERED

**************************************************

INTERVALS

 - P8: Octave
 - P5: Perfect 5th

* 1: Unisons | -> AUGMENTED : greatest distance between two notes
* 4: 4ths    | -> PERFECT   : right in the middle
* 5: 5ths    | -> DIMINISHED: least distance between two notes
* 8: Octaves |

F |-------------
E |
D |-------------
C |
B |-------------
A |
G |--O--#O--bO--
F |
E |-------------
D
C  --O---O---O--
     P5  A5  d5

* 2: 2nds |  -> AUGMENTED : greatest distance between two notes
* 3: 3rds |  -> MAJOR     : right in the middle
* 6: 6ths |  -> MINOR     : right in the middle
* 7: 7ths |  -> DIMINISHED: least distance between two notes

F |------------------
E |
D |------------------
C |
B |------------------
A |
G |------------------
F |
E |--O--bO--bbO--#O--
D
C  --O---O----O---O--
     M3  m3   d3  A3


**************************************************

DOMINANT / MAJOR-MINOR 7TH CHORD

MAJOR SCALE:
    I    ii   iii  IV   V7   vi   vii°  I
    CM7  Dm7  Em7  FM7  G7   Am7  B§7   CM7

    I, IV       -> CM7, FM7      -> Major         7th chords (Major    triad with a Major 7th on top)
    ii, iii, vi -> Dm7, Em7, Am7 -> Minor         7th chords (Minor    triad with a Minor 7th on top)
    V7          -> G7            -> Major-Minor   7th chord  (Major    triad with a Minor 7th on top)
    B§7         -> B§7           -> Half-Diminish 7th chord  (Diminish triad with a Minor 7th on top)

    B°7         -> C°7           -> Full-Diminish 7th chord  (Diminish triad with a Diminished 7th on top)

MINOR SCALE 7ths:
    i    ii°  III  iv   v    VI   VII7 i

    i7   ii§  III7 iv7  v7   VI7  VII7 i7
    Am7  B§7  C7   Dm7  Em7  F7   G7   Am7

    Major Scale V7 -> Minor Scale VII7

HARMONIC MINOR SCALE 7ths:
               M+          M          m°
    i    ii°   III+  iv    V    VI    vii°
    Am   B°7   C+    d     E    F     G°

    iM7  ii°   III   iv    Vd7  VI    VII#°7 iM7     -> iM7 (minor-major => disonance)
    AmM7 B°7   C7    Dm7   Ed7  F7    G#°7   AmM7

MELODIC MINOR SCALE 7ths:
               M+          M          m°
    i    ii    III+  IV    V    vi°   vii°
    Am   Bm    C+    D     E    F°    G°

    iM7  ii7   III7  IVd7  Vd7  VI#°7 VII#°7 iM7
    AmM7 Bm7   C7    Dd7   Ed7  F#°7  G#°7   AmM7

**************************************************

   CM7   CMm7     Cm7   C§7    C°7
       Dominant

F |----------------------------------------------------------
E |
D |----------------------------------------------------------
C |
B |-O-----bO------bO-----bO----bbO---------------------------
A |
G |-O------O-------O-----bO-----bO---------------------------
F |
E |-O------O------bO-----bO-----bO---------------------------
D
C  -O-    -O-     -O-    -O-    -O-

============================================================================================================================

     1            2            3            4            5            6            7            8             Scene
   +--------------------------------------------------------------------------------------------------------+-------------+
 8 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] |  ->         |
 7 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] |  ->         |
 6 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] |  ->         |
 5 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] |  ->         |
 4 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] |  ->         |
 3 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] |  ->         |
 2 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] |  ->         |
 1 | [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ]  [         ] |  ->         |
   +--------------------------------------------------------------------------------------------------------+-------------+
   | ^            v            <            >            ?            ?            ?            ?           |  ?          |
   +--------------------------------------------------------------------------------------------------------+-------------+
   | ?            ?            ?            ?            ?            ?            ?            ?           |  ?          |
   +--------------------------------------------------------------------------------------------------------+-------------+
