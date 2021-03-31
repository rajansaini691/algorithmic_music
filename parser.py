"""
Probably shouldn't be called parser.py... 

Traverse a graph of GraphNodes and generate stuff
"""
from node import GraphNode, Tonic
from note import Note

# Maybe make it a class? IDK
# TODO Would be cool to figure out a way to deal with subdivisions
def parse(root_node, ticks=50, tempo=120):
    """
    Traverses a graph of nodes and returns a list of instructions

    Parameters:
        root_node   Starting node of graph
        ticks       Each tick, we visit a node and generate an instruction.
                    The tick represents the smallest unit of time.
        tempo       Number of ticks per second
    """
    curr_node = root_node
    instrs = []
    for t in range(ticks):
        instrs += [curr_node.emit(t / tempo)]
        curr_node = curr_node.next()

    return instrs

if __name__ == "__main__":
    a = Tonic()
    b = Tonic()
    c = Tonic()
    a.add_edge(b, 3)
    a.add_edge(c, 3)
    b.add_edge(a, 3)
    c.add_edge(a, 3)

    print(parse(a, ticks=3))