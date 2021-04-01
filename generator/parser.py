"""
Probably shouldn't be called parser.py... 

Traverse a graph of GraphNodes and generate stuff
"""
from generator.node import GraphNode, Triad
from generator.note import Note

# Maybe make it a class? IDK
# TODO Would be cool to figure out a way to deal with subdivisions
# TODO Change name from parse() to generate()
def parse(root_node, ticks=50, tempo=120):
    """
    Traverses a graph of nodes and returns a list of instructions

    Parameters:
        root_node   Starting node of graph
        ticks       Each tick, we visit a node and generate an instruction.
                    The tick represents the smallest unit of time.
        tempo       Number of ticks per second
    """
    assert(ticks > 1), "How can we generate anything without any ticks?"
    curr_node = root_node
    instrs = []
    t = 0
    while True:
        instrs += [curr_node.emit(t / tempo, 1 / tempo)]

        if t > ticks and curr_node.final:
            break

        curr_node = curr_node.next()
        t += 1

    return instrs

def fmt_instrs(instrs):
    """
    Pretty-prints a list of instructions
    """
    out = ""
    for note in instrs:
        out += '\n'
        out += '\n'.join(note)
        out += '\n'
    return out

if __name__ == "__main__":
    # Run a simple end-to-end test
    a = Triad("C3", "E3", "G3")
    b = Triad("C3", "E3", "G3")
    c = Triad("C3", "E3", "G3")
    a.add_edge(b, 3)
    a.add_edge(c, 3)
    b.add_edge(a, 3)
    c.add_edge(a, 3)

    print(fmt_instrs(parse(a, ticks=3)))
