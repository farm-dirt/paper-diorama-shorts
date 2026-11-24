"""Writes project.json: the scene plan + event times (pictures) + sound cues, all from ONE timeline."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))

SC = []
def scene(**k):
    SC.append(k); return k

# 1 hook: the map at home, the frost bamboo glowing on it
scene(id='map1', start=0.0, end=3.4, set='trip_map', variant='home', dof=0.45, light='warm',
      desc='Frame 0 = the goal: a map with a glowing, steaming bamboo drawing. Mitten taps it (I want THAT).',
      cam={'from': [0, -20, 1.04], 'to': [0, -40, 1.10]}, ev={'tap': 1.45, 'checks': []})
# 2 out the door, through the village
scene(id='village', start=3.4, end=9.2, set='snow_village', variant='dawn',
      tin={'type': 'dive', 'dur': 0.75, 'at': [270, 1330]},
      desc='We dive into HOME on the map and land behind our own front door; mittens push it open; walk out at dawn.',
      cam={'from': [0, 0, 1.0], 'to': [0, -30, 1.22], 'ease': 'in'},
      walk={'s': 5.0, 'e': 9.2, 'rate': 1.9, 'amp': 18}, ev={'door': [4.2, 5.0], 'breath': [5.7, 7.7]})
# 3 the frozen river
scene(id='river', start=9.2, end=15.8, set='ice_river', variant='day',
      tin={'type': 'fog', 'dur': 0.8},
      desc='Breath fog clears on the frozen river. Slow careful steps, the ice creaks, a crack races under us, we hop to the far bank.',
      cam={'from': [0, 80, 1.0], 'to': [0, 40, 1.30]},
      walk=[{'s': 9.7, 'e': 12.0, 'rate': 1.3, 'amp': 12}, {'s': 14.5, 'e': 15.8, 'rate': 1.9, 'amp': 16}],
      camKeys=[{'s': 12.1, 'e': 12.8, 'by': [0, 60, 0.06]}, {'s': 13.5, 'e': 13.9, 'by': [0, -160, 0.10], 'ease': 'out'},
               {'s': 13.9, 'e': 14.15, 'by': [0, 60, 0.12], 'ease': 'in'}, {'s': 14.5, 'e': 15.8, 'by': [0, -40, 0.25]}],
      shake={'t': 14.15, 'dur': 0.35, 'amp': 16},
      ev={'crack': [12.1, 12.8], 'hop': 13.5, 'breath': [13.0]})
# 4 woods: follow the glowing drips; snow dump
scene(id='woods', start=15.8, end=22.0, set='snow_woods', variant='day',
      tin={'type': 'gust', 'dur': 0.7},
      desc='A gust of snow wipes us into the woods. Glowing blue drips mark the path. We look up: a bough dumps snow on our face, mitten wipes it off, the cave appears ahead.',
      cam={'from': [0, 20, 1.0], 'to': [0, -10, 1.25]},
      walk=[{'s': 16.2, 'e': 19.3, 'rate': 1.8, 'amp': 16}, {'s': 21.0, 'e': 22.0, 'rate': 1.8, 'amp': 14}],
      camKeys=[{'s': 19.3, 'e': 19.7, 'by': [0, -150, 0.0]}, {'s': 20.6, 'e': 21.0, 'by': [0, 150, 0.0]}],
      shake={'t': 20.05, 'dur': 0.4, 'amp': 18},
      ev={'fall': 19.65, 'splat': 20.05, 'swipe': 20.6, 'breath': [17.6]})
# 5 map check: river + woods ticked, the cave is next
scene(id='map2', start=22.0, end=23.6, set='trip_map', variant='woods', dof=0.45,
      tin={'type': 'whip', 'dur': 0.45},
      desc='We pull out the map: tick river, tick woods. Only the cave is left.',
      cam={'from': [0, -40, 1.06], 'to': [0, -60, 1.12]},
      ev={'checks': [['river', 22.35], ['woods', 22.85]], 'pencil': [22.35, 23.2]})
# 6 cave mouth: icicle curtain + lantern
scene(id='cave', start=23.6, end=28.6, set='cave_mouth', variant='day',
      tin={'type': 'dive', 'dur': 0.7, 'at': [590, 830]},
      desc='Dive into CAVE on the map: an icicle curtain hangs over the cave. Mitten pushes it aside (chimes), lantern clicks on, we step into the dark.',
      cam={'from': [0, 0, 1.0], 'to': [0, 0, 1.04]},
      camKeys=[{'s': 26.9, 'e': 28.6, 'by': [0, 80, 0.55], 'ease': 'in'}],
      walk={'s': 26.9, 'e': 28.6, 'rate': 1.7, 'amp': 14}, ev={'push': [24.9, 26.1], 'lantern': 26.5})
# 7 inside: rub the frost off the ice wall
scene(id='wall', start=28.6, end=33.2, set='ice_wall', variant='day',
      tin={'type': 'dark', 'dur': 0.9, 'at': [540, 1060]},
      desc='Into the dark, then lantern light on a frosted ice wall. Mitten rubs the frost away: the bamboo is frozen inside, glowing and steaming.',
      cam={'from': [0, 0, 1.0], 'to': [0, -30, 1.12]}, ev={'lantern': 28.0, 'rub': [29.7, 31.5]})
# 8 payoff: crack, snap, scoop, bite
scene(id='payoff', start=33.2, end=41.0, set='bamboo_close', variant='day',
      tin={'type': 'dive', 'dur': 0.6, 'at': [540, 900]},
      desc='Close-up. Spoon taps twice, the ice cracks, third tap shatters it. Snap the bamboo: a wobbly pudding inside. Scoop, it comes to you, bite: warm glow.',
      cam={'from': [0, 40, 1.0], 'to': [0, 40, 1.0]},
      camKeys=[{'s': 36.2, 'e': 37.2, 'by': [0, 0, 0.0]}, {'s': 37.2, 'e': 38.5, 'by': [0, 30, 0.45]}],
      flash={'t': 35.25, 'dur': 0.25, 'color': '#E8FBFF'}, shake={'t': 35.25, 'dur': 0.3, 'amp': 10},
      ev={'taps': [34.1, 34.7], 'shatter': 35.25, 'snap': 36.9, 'scoop': 38.7, 'bite': 40.0})
# 9 loop: tick the cave, dive back into the glowing bamboo -> frame 0
scene(id='map3', start=41.0, end=44.6, set='trip_map', variant='cave', dof=0.45,
      tin={'type': 'fog', 'dur': 0.8, 'color': [1.0, 0.93, 0.80]},
      desc='Warm fog: back to the map. Tick the cave. Push into the glowing bamboo drawing, which loops to frame 0.',
      cam={'from': [0, -40, 1.06], 'to': [0, -40, 1.06]},
      camKeys=[{'s': 42.9, 'e': 44.6, 'by': [85, -215, 0.6], 'ease': 'in'}],
      ev={'checks': [['river', 0], ['woods', 0], ['cave', 41.9]], 'pencil': [41.9, 42.6]})

for s in SC:
    s.pop('walk2', None)

# ---------------------------------------------------------------- sound: brand-new foley for THIS short
FOLEY = {
    'unfold': {'kind': 'paper_unfold', 'n': 5}, 'unfold2': {'kind': 'paper_unfold', 'n': 3, 'd': 0.5},
    'magic': {'kind': 'icicle_chime', 'n': 3}, 'tap': {'kind': 'paper_tap'}, 'ping_soft': {'kind': 'ice_ping', 'n': 1},
    'dive1': {'kind': 'swoosh_dive', 'd': 0.8}, 'dive2': {'kind': 'swoosh_dive', 'd': 0.75}, 'dive3': {'kind': 'swoosh_dive', 'd': 0.65},
    'dive_end': {'kind': 'swoosh_dive', 'd': 1.4},
    'latch': {'kind': 'latch'}, 'door': {'kind': 'door_swing'},
    'step1': {'kind': 'snow_step'}, 'step2': {'kind': 'snow_step'}, 'step3': {'kind': 'snow_step'}, 'step4': {'kind': 'snow_step'},
    'icestep1': {'kind': 'ice_step'}, 'icestep2': {'kind': 'ice_step'},
    'breath1': {'kind': 'breath_out'}, 'breath2': {'kind': 'breath_out'},
    'fog': {'kind': 'fog_hiss', 'd': 0.9}, 'steam': {'kind': 'fog_hiss', 'd': 1.1}, 'hop': {'kind': 'fog_hiss', 'd': 0.4},
    'creak1': {'kind': 'ice_creak'}, 'creak2': {'kind': 'ice_creak'}, 'crack': {'kind': 'ice_crack'}, 'ping': {'kind': 'ice_ping', 'n': 3},
    'land': {'kind': 'thump_snow'}, 'gust': {'kind': 'gust', 'd': 0.9}, 'drip': {'kind': 'drip'}, 'drip2': {'kind': 'drip'},
    'bough': {'kind': 'door_swing'}, 'plop': {'kind': 'snow_plop'}, 'wipe': {'kind': 'mitten_rub', 'd': 0.45, 'rate': 2.2},
    'whip': {'kind': 'whip'}, 'pencil': {'kind': 'pencil_scratch'},
    'chime1': {'kind': 'icicle_chime', 'n': 7}, 'chime2': {'kind': 'icicle_chime', 'n': 5}, 'lantern': {'kind': 'lantern_click'},
    'iris': {'kind': 'iris_whoomp'}, 'rub': {'kind': 'mitten_rub', 'd': 1.8, 'rate': 3.2}, 'reveal': {'kind': 'icicle_chime', 'n': 4},
    'spoon1': {'kind': 'spoon_tap'}, 'spoon2': {'kind': 'spoon_tap'}, 'shatter': {'kind': 'shatter'}, 'snap': {'kind': 'bamboo_snap'},
    'wobble': {'kind': 'wobble', 'd': 1.2}, 'scoop': {'kind': 'scoop'}, 'bite': {'kind': 'bite_soft'}, 'warm': {'kind': 'sparkle_warm', 'n': 8},
    'bed_room': {'kind': 'bed_room', 'd': 4.6}, 'bed_morning': {'kind': 'bed_morning', 'd': 6.6}, 'bed_river': {'kind': 'bed_river', 'd': 7.4},
    'bed_woods': {'kind': 'bed_woods', 'd': 12.0}, 'bed_cave': {'kind': 'bed_cave', 'd': 14.6}, 'bed_glow': {'kind': 'bed_glow', 'd': 13.8},
}
CUES = []
def cue(t, name, gain=1.0, **k):
    CUES.append(dict(t=round(t, 3), name=name, gain=gain, **k))
def steps(s, e, rate, names, gain):
    k, i = 1, 0
    while s + k / rate < e - 0.05:
        cue(s + k / rate - 0.02, names[i % len(names)], gain * (0.85 + 0.15 * (k % 2)))
        k += 1; i += 1
# beds (each place sounds different; they overlap ~0.5 s at every transition)
cue(0.0, 'bed_room', 0.20, dur=4.4, fadeOut=0.6)
cue(3.5, 'bed_morning', 0.26, dur=6.3, fadeIn=0.5, fadeOut=0.7)
cue(9.1, 'bed_river', 0.30, dur=7.2, fadeIn=0.5, fadeOut=0.7)
cue(15.7, 'bed_woods', 0.26, dur=11.9, fadeIn=0.5, fadeOut=1.0)
cue(26.8, 'bed_cave', 0.30, dur=14.6, fadeIn=1.0, fadeOut=0.8)
cue(31.0, 'bed_glow', 0.16, dur=13.6, fadeIn=1.5, fadeOut=0.6)
# 1 map at home
cue(0.0, 'unfold', 0.55); cue(0.15, 'magic', 0.22); cue(1.45, 'tap', 0.45); cue(1.55, 'ping_soft', 0.25); cue(1.9, 'steam', 0.22); cue(2.6, 'unfold2', 0.18)
cue(3.4, 'dive1', 0.45)
# 2 village
cue(4.1, 'latch', 0.5); cue(4.25, 'door', 0.42)
steps(5.0, 9.2, 1.9, ['step1', 'step2', 'step3', 'step4'], 0.55)
cue(5.7, 'breath1', 0.30); cue(7.7, 'breath2', 0.28)
cue(9.2, 'fog', 0.38)
# 3 river
steps(9.7, 12.0, 1.3, ['icestep1', 'icestep2'], 0.40)
cue(10.3, 'creak1', 0.45); cue(11.3, 'creak2', 0.5); cue(12.1, 'crack', 0.85); cue(12.25, 'ping', 0.45)
cue(13.0, 'breath1', 0.22); cue(13.5, 'hop', 0.25); cue(14.13, 'land', 0.8)
steps(14.5, 15.8, 1.9, ['step2', 'step4', 'step1'], 0.55)
cue(15.8, 'gust', 0.5)
# 4 woods
steps(16.2, 19.3, 1.8, ['step3', 'step1', 'step4', 'step2'], 0.52)
for i, tt in enumerate([16.8, 17.55, 18.3, 19.0]):
    cue(tt, 'drip' if i % 2 else 'drip2', 0.30)
cue(17.6, 'breath2', 0.25); cue(19.4, 'bough', 0.30); cue(19.65, 'plop', 0.45); cue(20.05, 'plop', 0.9); cue(20.55, 'wipe', 0.45)
steps(21.0, 22.0, 1.8, ['step1', 'step3'], 0.5)
cue(21.95, 'whip', 0.45)
# 5 map check
cue(22.05, 'unfold2', 0.45); cue(22.35, 'pencil', 0.5); cue(22.85, 'pencil', 0.5)
cue(23.6, 'dive2', 0.45)
# 6 cave mouth
cue(24.95, 'chime1', 0.55); cue(25.35, 'chime2', 0.40); cue(26.5, 'lantern', 0.55)
steps(26.9, 28.6, 1.7, ['step4', 'step2', 'step3'], 0.5)
cue(28.6, 'iris', 0.45)
# 7 ice wall
cue(29.7, 'rub', 0.5); cue(31.3, 'reveal', 0.32)
cue(33.2, 'dive3', 0.40)
# 8 payoff
cue(34.1, 'spoon1', 0.6); cue(34.7, 'spoon2', 0.65); cue(34.75, 'ping_soft', 0.3)
cue(35.25, 'shatter', 0.95); cue(35.35, 'steam', 0.30)
cue(36.9, 'snap', 0.85); cue(37.0, 'steam', 0.25); cue(37.05, 'wobble', 0.5)
cue(38.7, 'scoop', 0.55); cue(40.0, 'bite', 0.6); cue(40.1, 'warm', 0.45)
cue(41.0, 'fog', 0.32)
# 9 map end -> loop
cue(41.15, 'unfold2', 0.35); cue(41.9, 'pencil', 0.5); cue(43.2, 'dive_end', 0.4); cue(43.4, 'magic', 0.2)

proj = {'id': 'frost-bamboo-trip', 'slug': 'frost-bamboo-trip', 'title': 'Frost Bamboo Pudding - the trip', 'fps': 24,
        'voice': None, 'captionY': 420, 'steps': 24,
        'hook': {'text': 'Pudding that grows in *ice*', 's': -0.3, 'e': 3.0, 'y': 300},
        'captions': [], 'scenes': SC, 'foley': FOLEY, 'sfx': CUES}
json.dump(proj, open(os.path.join(HERE, 'project.json'), 'w'), indent=1)
json.dump({'dur': SC[-1]['end'], 'env': [], 'envFps': 30, 'speech': [], 'pauses': [], 'sentences': []},
          open(os.path.join(HERE, 'timing.json'), 'w'))
print('scenes', len(SC), 'dur', SC[-1]['end'])
