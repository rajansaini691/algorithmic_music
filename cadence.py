"""
Simple ii|IV - V - I cadence
"""
from generator.node import Tonic

a = Tonic()
b = Tonic()
c = Tonic()
a.add_edge(b, 3)
a.add_edge(c, 3)
b.add_edge(a, 3)
c.add_edge(a, 3)

print(fmt_instrs(parse(a, ticks=3)))
