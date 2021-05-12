"""
Some kind of folk music
"""
from generator.node import Triad, Chord
from generator.parser import fmt_instrs, parse_with_rhythm, parse
from generator.note import Kick

"""
Create one node per chord.
"""
# No matter how crazy things get, we always end on the tonic
# FIXME Need a copy() method
i_downbeat = Chord(["F3", "Ab3", "C4"], final=True)     
i = Chord(["F3", "Ab3", "C4"], final=True)     
i_1 = Chord(["F3", "Ab3", "C4"], final=True)     
i_2 = Chord(["F3", "Ab3", "C4"], final=True)     
i_3 = Chord(["F3", "Ab3", "C4"], final=True)     
i_4 = Chord(["F3", "Ab3", "C4"], final=True)     
i_5 = Chord(["F3", "Ab3", "C5"], final=True)     
i_6 = Chord(["F3", "Ab3", "C4"], final=True)     
ii = Triad("G3", "Bb3", "D4", final=True)
III = Triad("Ab3", "C4", "Eb5", final=True)
iv = Triad("Bb3", "F3", "Bb4", final=True)
v = Triad("C4", "Eb4", "G5", final=True)
VI = Triad("Db3", "F4", "Ab5", final=True)

# Twelve bar blues!
m = [None]*13

# I'm intentionally not zero-indexing
m[1] = i_downbeat
m[2] = i
m[3] = i_1
m[4] = i_2
m[5] = iv
m[6] = iv
m[7] = i_3
m[8] = i_4
m[9] = v
m[10] = iv
m[11] = i_5
m[12] = i_6

# Six bar blues!
#m[1] = i_downbeat
#m[2] = i
#m[3] = iv
#m[4] = i_1
#m[5] = v
#m[6] = i_2


"""
Add edges between chords (what resolves to what?)
"""
for i in range(1,12):
    m[i].add_edge(m[i+1], 1)

m[12].add_edge(m[1], 1)


print(fmt_instrs(parse_with_rhythm(m[1], tempo=120*2, delay=3*4)))

"""
Add a kick drum (API will definitely change here to integrate with graph)
"""
#k = Kick()
#for i in range(6 * 16):
#    print(k.emit(i * 60 / 120, 0.01))
