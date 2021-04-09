"""
Probably shouldn't be called parser.py... 

Traverse a graph of GraphNodes and generate stuff
"""

# Ugly hack to allow absolute import from the root folder
# whatever its name is. Please forgive the heresy.
if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))
    __package__ = "examples"

from generator.node import GraphNode, Triad
from generator.note import Note
from generator.rhythm import rhythmic_phrase

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

def parse_with_rhythm(root_node, min_num_phrases=3, tempo=60):
    """
    Slightly more complicated implementation of parse() above,
    with rhythmic stuff
    
    Parameters:
        tempo                   Beats per minute (2 measures per chord change, or 8 beats per chord change)
        min_num_phrases         Minimum number of phrases to generate (could be more if we get a deceptive cadence)
    """
    instrs = []
    phrase = rhythmic_phrase()
    curr_node = root_node

    t = 0
    phrases_generated = 0
    secs_per_note = 60 / (2 * tempo)

    while phrases_generated < min_num_phrases or not curr_node.final:
        for measure in phrase:
            for note_len in measure:
                instrs += [curr_node.emit(secs_per_note * t, secs_per_note * note_len / 4)]
                t += note_len

            curr_node = curr_node.next()

        phrases_generated += 1

    # Curr node always ends on the tonic
    instrs += [curr_node.emit(secs_per_note * t, secs_per_note * 4 / 4)]

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
    a = Triad("C3", "E3", "G3", final=True)
    b = Triad("F3", "A3", "C4")
    c = Triad("G3", "B3", "D3")
    a.add_edge(b, 3)
    a.add_edge(c, 3)
    b.add_edge(a, 3)
    c.add_edge(a, 3)

    print(fmt_instrs(parse_with_rhythm(a, ticks=3)))
