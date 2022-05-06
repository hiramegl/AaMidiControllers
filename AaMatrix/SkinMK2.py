from _Framework.Skin import Skin
from .ColorsMK2 import Rgb

class Colors:
  class DefaultButton:
    On       = Rgb.GREY
    Off      = Rgb.BLACK
    Disabled = Rgb.BLACK

  class Unav:
    On  = Rgb.BLACK
    Off = Rgb.BLACK

  class Mode: #mode buttons colour
    class Session:
      On  = Rgb.GREEN
      Off = Rgb.GREY
    class SeqZoom:
      On  = Rgb.LIGHT_BLUE
      Off = Rgb.GREY
    class SeqCmd:
      On  = Rgb.YELLOW
      Off = Rgb.GREY
    class Tools:
      On  = Rgb.PURPLE
      Off = Rgb.GREY

  class Session:
    #scene
    SceneTriggered      = Rgb.GREEN_BLINK
    Scene               = Rgb.GREEN
    NoScene             = Rgb.BLACK

    #clip states
    ClipStarted         = Rgb.GREEN_PULSE
    ClipStopped         = Rgb.RED_THIRD
    ClipRecording       = Rgb.RED_PULSE
    ClipEmpty           = Rgb.BLACK

    #trigs
    ClipTriggeredPlay   = Rgb.GREEN_BLINK
    ClipTriggeredRecord = Rgb.RED_BLINK
    RecordButton        = Rgb.RED_THIRD

    #stop button
    StopClip            = Rgb.RED
    StopClipTriggered   = Rgb.RED_BLINK

    class Nav:
      On  = Rgb.RED
      Off = Rgb.BLACK

    class ModeMixer:
      On  = Rgb.TURQUOISE
      Off = Rgb.GREY
    class ModeZoom:
      On  = Rgb.PURPLE
      Off = Rgb.GREY
    class ModeLaunch:
      On  = Rgb.GREEN
      Off = Rgb.GREY
    class ModeSelect:
      On  = Rgb.BLUE
      Off = Rgb.GREY

    class Zoom:
      On  = Rgb.PURPLE
      Off = Rgb.PURPLE_THIRD

    class Play:
      On  = Rgb.GREEN
      Off = Rgb.BLACK
    class Stop:
      On  = Rgb.RED
      Off = Rgb.BLACK
    class Mute:
      On  = Rgb.AMBER
      Off = Rgb.BLACK
    class Solo:
      On  = Rgb.BLUE
      Off = Rgb.BLUE_THIRD
    class Send:
      On  = Rgb.RED
      Off = Rgb.YELLOW
    class Monitor:
      In   = Rgb.GREEN_BLINK
      Auto = Rgb.AMBER
      Off  = Rgb.RED
      Unav = Rgb.BLACK
    class Arm:
      On  = Rgb.RED
      Off = Rgb.RED_THIRD

  class Zooming: # session zooming
    Selected = Rgb.AMBER
    Stopped  = Rgb.RED
    Playing  = Rgb.GREEN
    Empty    = Rgb.BLACK

  class SeqBase:
    class Invalid:
      On  = Rgb.RED
      Off = Rgb.BLACK
    class Empty:
      On  = Rgb.GREEN
      Off = Rgb.BLACK

  class SeqZoom:
    class Nav:
      On  = Rgb.LIGHT_BLUE
      Off = Rgb.LIGHT_BLUE
    class Zoom:
      Unav     = Rgb.BLACK
      Selected = Rgb.AMBER
      Active   = Rgb.GREEN
      InSpan   = Rgb.LIGHT_BLUE
      Empty    = Rgb.RED
    class Mode:
      Bar    = Rgb.BLUE
      Phrase = Rgb.LIGHT_BLUE
    class Section:
      On  = Rgb.MINT
      Off = Rgb.GREY
    class LpDup:
      On  = Rgb.AQUA
      Off = Rgb.GREY
    class Start:
      On  = Rgb.GREEN_HALF
      Off = Rgb.BLACK
    class Middle:
      On  = Rgb.AMBER_HALF
      Off = Rgb.BLACK
    class End:
      On  = Rgb.RED_HALF
      Off = Rgb.BLACK
    class ClDup:
      On  = Rgb.TURQUOISE
      Off = Rgb.GREY
    class Toggle:
      Section = Rgb.BLUE
      Tools   = Rgb.LIGHT_BLUE

  class SeqCmd:
    class Nav:
      On  = Rgb.YELLOW
      Off = Rgb.YELLOW
    class Scale:
      On  = Rgb.GREEN
      Off = Rgb.RED
    class Trnsps:
      On  = Rgb.PINK
      Act = Rgb.PINK_BLINK
      Off = Rgb.PINK_THIRD
    class Mode:
      Bar    = Rgb.BLUE
      Phrase = Rgb.LIGHT_BLUE
    class Slider:
      On  = Rgb.LIME
      Off = Rgb.GREY
    class Root:
      On    = Rgb.GREEN
      Black = Rgb.RED
      White = Rgb.AMBER
    class Section:
      On  = Rgb.MINT
      Off = Rgb.GREY
    class GridSel:
      On  = Rgb.GREEN
      Off = Rgb.GREY
    class SelTog:
      On  = Rgb.VIOLET
      Off = Rgb.BLACK
    class PitxAll:
      On  = Rgb.MINT
      Off = Rgb.BLACK
    class PitxSel:
      On  = Rgb.MINT_THIRD
      Off = Rgb.BLACK
    class TimeAll:
      On  = Rgb.LIGHT_BLUE
      Off = Rgb.BLACK
    class TimeSel:
      On  = Rgb.LIGHT_BLUE_THIRD
      Off = Rgb.BLACK
    class LenAll:
      On  = Rgb.PURPLE
      Off = Rgb.BLACK
    class LenBit:
      On  = Rgb.PURPLE_THIRD
      Off = Rgb.GREY
    class ChopAll:
      On  = Rgb.YELLOW
      Off = Rgb.BLACK
    class ChopBit:
      On  = Rgb.YELLOW
      Off = Rgb.GREY
    class DelAll:
      On  = Rgb.RED
      Off = Rgb.BLACK
    class DelSel:
      On  = Rgb.RED_THIRD
      Off = Rgb.BLACK
    class BitCmd:
      On  = Rgb.TURQUOISE
      Off = Rgb.BLACK
    class MuteSel:
      On  = Rgb.AMBER
      Off = Rgb.BLACK
    class SoloSel:
      On  = Rgb.BLUE
      Off = Rgb.BLACK
    class Patt:
      On  = Rgb.BROWN
      Off = Rgb.MINT

  class Tools:
    class Nav:
      On  = Rgb.PURPLE
      Off = Rgb.PURPLE
    class Size: # Time Delta
      On  = Rgb.GREEN
      Off = Rgb.RED
    class ClStart:
      On  = Rgb.MINT_THIRD
      Off = Rgb.BLACK
    class ClEnd:
      On  = Rgb.AMBER_THIRD
      Off = Rgb.BLACK
    class LpStart:
      On  = Rgb.MINT
      Off = Rgb.BLACK
    class LpEnd:
      On  = Rgb.AMBER
      Off = Rgb.BLACK
    class Shift:
      On  = Rgb.LIME
      Off = Rgb.BLACK
    class Start:
      On  = Rgb.GREEN_HALF
      Off = Rgb.BLACK
    class Middle:
      On  = Rgb.AMBER_HALF
      Off = Rgb.BLACK
    class End:
      On  = Rgb.RED_HALF
      Off = Rgb.BLACK
    class Beat14:
      On  = Rgb.BLUE
      Off = Rgb.BLACK
    class Beat58:
      On  = Rgb.LIGHT_BLUE
      Off = Rgb.BLACK
    class Beat18:
      On  = Rgb.MINT
      Off = Rgb.BLACK
    class Reset:
      On  = Rgb.YELLOW
      Off = Rgb.BLACK
    class Crop:
      On  = Rgb.PURPLE
      Off = Rgb.BLACK
    class Quant:
      On  = Rgb.ORANGE
      Off = Rgb.BLACK
    class Warp:
      On  = Rgb.PINK
      Off = Rgb.GREY
    class Metro:
      On  = Rgb.OLIVE
      Off = Rgb.GREY
    class Follow:
      On  = Rgb.LIME
      Off = Rgb.GREY
    class ClPlay:
      On  = Rgb.GREEN
      Off = Rgb.BLACK
    class ClStop:
      On  = Rgb.RED
      Off = Rgb.BLACK
    class ClDup:
      On  = Rgb.TURQUOISE
      Off = Rgb.GREY
    class Rew:
      On  = Rgb.PURPLE
      Off = Rgb.BLACK
    class Ff:
      On  = Rgb.PURPLE
      Off = Rgb.BLACK
    class Play:
      On  = Rgb.GREEN_HALF
      Off = Rgb.BLACK
    class Stop:
      On  = Rgb.RED_HALF
      Off = Rgb.BLACK
    class Rec:
      On  = Rgb.RED_HALF
      Off = Rgb.BLACK
    class Span:
      On  = Rgb.LIME
      Off = Rgb.BLACK
    class LpTogg:
      On  = Rgb.GREEN
      Off = Rgb.GREY
    class LpEnv:
      On  = Rgb.BROWN
      Off = Rgb.BLACK
    class Faders:
      On  = Rgb.TURQUOISE
      Off = Rgb.BLACK

def make_skin():
  return Skin(Colors)
