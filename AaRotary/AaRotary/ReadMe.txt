====================================================================================================
Preset 01 - FX 1, M/S
-------------------------

T=Toggle
B=Encoder Bar
P=Encoder Panoramic
D=Encoder Dot
Q=Encoder Quality
S=Encoder Spread
C=Encoder Cut
M=Encoder Damp

Track_X => 13 controls per strip, the offsets are:
--------------+
 Rotary_3     | 49
 Rotary_4     | 9
 Rotary_5     | 17
 Rotary_6     | 25
--------------+
 Button_2     | 33
 Button_3     | 41
 Button_4     | 1
 Button_5     | 57
--------------+
 Button_0     | 65
 Button_1     | 73
--------------+
 Rotary_0     | 81
 Rotary_1     | 89
 Rotary_2     | 97
--------------+

-------------+---------------+
Track_Left   | Track_Right   | 105 | 106
To_Selected  | Sync          | 107 | 108
-------------+---------------+

# SpecialChannelStripComponent documentation
#
# configuration of devices parameters position and presets
# self.m_hCfg = {
#     'devices': {
#          '<device>': {
#               'param_cfgs': {
#                    '<param_name>': (sPanel, sType, nRowIdx, nStripIdx, nBankOffset), ...
#               },
#               'preset_cfgs': [
#                    ['<preset_name>', val1, val2, ...], ...
#               ]
#          }
#     }
# }
#
# configuration of devices by features: strips, extra functions, preset lineup
# self.m_hDevCfgs = {
#     '<device>': {
#         'banks' : <int>,
#         'strips': <int>,
#         'extra_functions': ['Extra Param 1', 'Extra Param 2', ...],
#     }, ...
# }
#
# map of midi controls for all available banks of BCR-2000:
# self.m_hMidiCtls =
# bank / strip / panel / type / index : {
#     'control': <control>,
#     'slot'   : <slot>,
# }
#
# devices registry: ordered by track and device, has references to the
#                   parameters, controls, slots, etc.
# self.m_hDevReg = {
#     <nTrackIdxAbs>: {
#         'Device': {
#             'device': <device_instance>
#             'track' : '<name_of_track>'
#             'preset_index': <int>,
#             'dev_params': {
#                 'Param 1': {
#                      'param'  : <parameter>,
#                      'control': <control>,
#                 }, ...
#             },
#             'panel_params': {
#                 'Param A': {
#                      'param'  : <string>,
#                      'control': <control>,
#                      '<state_var>': <some_state_var>,
#                 }, ...
#             },
#             'extra_params': {
#                 'Param X': {
#                      'param'  : <int|float>,
#                      'control': <control>,
#                 }, ...
#             },
#             'auto_params': {
#                  'on'   : True | False,
#                  'type' : '<auto_program>'
#                  'delta': float,
#                  'start': float,
#                  'vel'  : int, [in bars]
#                  'param_refs': {
#                      'Param 1: {
#                          'param'  : <parameter>,
#                          'control': <control>,
#                      }
#                  }
#             },
#         },
#     }
# }

