"""
Simple iii - ii|IV - V - I cadence
"""
from generator.node import Triad
from generator.parser import fmt_instrs, parse_with_rhythm
from generator.note import Kick

"""
Create one node per chord.
"""
# No matter how crazy things get, we always end on the tonic
I = Triad("C4", "E4", "G4", final=True)     
ii = Triad("D4", "F4", "A4")
iii = Triad("E4", "G4", "B4")
IV = Triad("F4", "A4", "C5")
V = Triad("G4", "B4", "D5")
vi = Triad("A4", "C5", "E5")

"""
Add edges between chords (what resolves to what?)
"""
# Have the I chord go to iii
I.add_edge(iii, 1)

# Not sure what to do with the vi, chord; let's go to iii for now
vi.add_edge(iii, 1)

# Give the iii chord an equal chance of going to ii and IV
iii.add_edge(ii, 1/2)     
iii.add_edge(IV, 1/2)

# ii and IV both progress to V
IV.add_edge(V, 1)
ii.add_edge(V, 1)

# Dominant cadence, baby!
V.add_edge(I, 1/2)

# Deceptive cadence?
V.add_edge(vi, 1/2)

print(fmt_instrs(parse_with_rhythm(I, tempo=120)))

"""
Add a kick drum (API will definitely change here to integrate with graph)
"""
k = Kick()
for i in range(6 * 16):
    print(k.emit(i * 60 / 120, 0.01))
