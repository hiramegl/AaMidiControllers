from _Framework.Skin import Skin
from _Framework.ButtonElement import Color

BLACK       = Color(0)
GREEN       = Color(1)
GREEN_BLINK = Color(2)
RED         = Color(3)
RED_BLINK   = Color(4)
AMBER       = Color(5)
AMBER_BLINK = Color(6)

TRACK_OFF = Color(0)
TRACK_ON  = Color(1)

SCENE_OFF = Color(0)
SCENE_ON  = Color(1)

class Colors:
    class DefaultButton:
        On       = GREEN
        Off      = RED
        Disabled = BLACK

    class Nav:
        On  = TRACK_ON
        Off = TRACK_OFF

    class Scene:
        On  = SCENE_ON
        Off = SCENE_OFF

    class Shift:
        On  = SCENE_ON
        Off = SCENE_OFF

    class Mode:
        On  = TRACK_ON
        Off = TRACK_OFF

    class Session:
        # scene
        Scene               = BLACK
        SceneTriggered      = GREEN_BLINK
        NoScene             = BLACK

        # clip states
        ClipStarted         = GREEN
        ClipStopped         = AMBER
        ClipRecording       = RED
        ClipEmpty           = BLACK

        # triggers
        ClipTriggeredPlay   = GREEN_BLINK
        ClipTriggeredRecord = RED_BLINK
        RecordButton        = RED

        # stop
        StopClip            = GREEN_BLINK
        StopClipTriggered   = RED_BLINK

        class SceneSel:
            On  = SCENE_ON
            Off = SCENE_ON

    class Zooming:
        Stopped  = RED
        Selected = AMBER
        Playing  = GREEN
        Empty    = BLACK

    class Mixer:
        class PanReset:
            On  = GREEN
            Off = BLACK
        class VolReset:
            On  = GREEN
            Off = BLACK
        class Stop:
            On  = RED
            Off = RED
        class Mute:
            On  = AMBER
            Off = BLACK
        class Solo:
            On  = GREEN_BLINK
            Off = GREEN
        class Arm:
            On  = RED_BLINK
            Off = RED
        class Deck:
            A     = RED
            B     = GREEN
            Unsel = AMBER
            Unava = BLACK
            Off   = BLACK
        class TrackSel:
            On  = GREEN
            Off = BLACK
        class SceneSel:
            On  = SCENE_ON
            Off = SCENE_OFF

        class Send:
            On    = RED
            Off   = AMBER
            Unava = BLACK
        class Monitor:
            In   = GREEN_BLINK
            Auto = AMBER
            Off  = RED
            Unav = BLACK
        class Select:
            On  = GREEN
            Off = BLACK

        class Vol:
            On    = GREEN
            Off   = AMBER
            Unava = BLACK

    class Sequencer:
        class Nav:
            On  = TRACK_ON
            Off = TRACK_OFF
        class NoteSel:
            On  = SCENE_ON
            Off = SCENE_OFF

        class Invalid:
            On  = RED
            Off = BLACK
        class Empty:
            On  = GREEN
            Off = BLACK

        class Note:
            On   = GREEN
            Off  = BLACK
            Mute = AMBER
            Root = RED
            Play = AMBER

        class Zoom:
            Empty    = AMBER
            Active   = RED
            Selected = GREEN
            Unava    = BLACK

        class Tools:
            class Octv:
                On  = GREEN
                Off = AMBER
            class Scale:
                On  = GREEN
                Off = RED
            class Root:
                On    = GREEN
                Off   = BLACK
                Whole = AMBER
                Half  = RED
            class LpSta:
                On  = AMBER
                Off = AMBER_BLINK
            class LpMid:
                On  = RED
                Off = RED_BLINK
            class LpEnd:
                On  = GREEN
                Off = GREEN_BLINK
            class Trans:
                On   = GREEN       # stand-by
                Off  = GREEN_BLINK # awaiting for new scale
                Unav = BLACK
            class Cmd:
                On  = GREEN
                Off = BLACK
            class Shift: # note oct up, note oct dw, note bit lf, note bit rg
                On  = AMBER
                Off = AMBER_BLINK
            class LpDup:
                On  = RED
                Off = RED_BLINK
            class SlMod:
                On  = GREEN
                Off = AMBER
            class Span:
                On  = GREEN
                Off = RED
            class Sect:
                On    = GREEN
                Off   = AMBER
                Unava = BLACK

        class Rhythm:
            class ShiftSize:
                On  = RED
                Off = AMBER
            class SongStart:
                On  = AMBER
                Off = BLACK
            class SongEnd:
                On  = GREEN
                Off = BLACK
            class LoopStart:
                On  = AMBER
                Off = BLACK
            class LoopEnd:
                On  = GREEN
                Off = BLACK
            class Rhythm:
                On  = GREEN
                Off = BLACK
            class NoteCmd:
                On  = AMBER
                Off = RED
            class CmdMode:
                On  = AMBER
                Off = RED
            class Chop:
                On  = RED
                Off = BLACK
            class Command:
                On  = GREEN
                Off = BLACK
            class SelectAll:
                On  = AMBER
                Off = BLACK
            class DeleteSel:
                On  = RED
                Off = BLACK
            class Clear:
                On  = RED_BLINK
                Off = BLACK
            class LoopShow:
                On  = AMBER
                Off = BLACK
            class PeerNavSy:
                On  = GREEN
                Off = RED
            class PeerPrim:
                On   = GREEN
                Off  = RED
                Unav = AMBER
            class ZoomMode:
                On  = GREEN
                Off = RED
            class Span:
                On  = GREEN
                Off = RED
            class Sect:
                On    = GREEN
                Off   = AMBER
                Unava = BLACK

    class Tools:
        class NotAvail:
                On  = BLACK
                Off = BLACK
        class Loop:
            class Size:
                On  = RED
                Off = AMBER
            class Shift:
                On  = GREEN
                Off = BLACK
            class Start:
                On  = AMBER
                Off = BLACK
            class Middle:
                On  = RED
                Off = BLACK
            class End:
                On  = GREEN
                Off = BLACK
            class Begin:
                On  = RED
                Off = BLACK
            class Bars:
                On  = GREEN
                Off = BLACK
            class Enable:
                On  = GREEN
                Off = AMBER
            class Dupl:
                On  = RED
                Off = BLACK
            class Show:
                On  = AMBER
                Off = BLACK
            class Roll:
                On  = GREEN
                Off = AMBER
        class Clip:
            class Reset: # Transpose, Detune, Gain
                On  = GREEN
                Off = BLACK
            class Cmd: # Crop, Quantize
                On  = RED
                Off = AMBER
            class Warp:
                On  = GREEN
                Off = AMBER
            class Play:
                On  = GREEN
                Off = AMBER
            class Stop:
                On  = RED
                Off = AMBER
            class Dupl:
                On  = RED
                Off = AMBER
            class Rew:
                On  = AMBER
                Off = BLACK
            class Forw:
                On  = AMBER
                Off = BLACK
        class Sess:
            class Metr:
                On  = RED
                Off = AMBER
            class Folw:
                On  = GREEN
                Off = AMBER
            class Play:
                On  = GREEN
                Off = AMBER
            class Stop:
                On  = RED
                Off = AMBER
            class Rec:
                On  = RED_BLINK
                Off = AMBER

def make_skin():
    return Skin(Colors)

