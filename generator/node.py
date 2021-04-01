
from abc import ABC, abstractmethod
from generator.note import SimpleNote
from random import choices

class GraphNode(ABC):
    """
    An element of the composition graph thing.

    Notes:
      - Edges: Outgoing edges are stored as (weight, next_node), where
               weight is proportional to the probability of taking an edge

      - Weight: Suppose this node has 3 outgoing edges, each with weights
                1, 1, 1. Then the probability of going to a given node is 0.33.
                If weights are 1, 2, 1, probabilities become 1/4, 1/2, 1/4
                (we normalize them).

    """
    def __init__(self, final=False):
        """
        Parameters:
            final       Is this node a halting state? (The machine only halts
                        at a halting state)
        """
        # Contains references to the next nodes in the graph
        self._edges = []

        # All of these should implement the emit() method, which ultimately
        # returns a list of instructions. Currently can contain GraphNode
        # and Note objects (as of 3/30/2021)
        self._children = []

        self._final = final

    def add_edge(self, next_node, weight):
        """
        Add an edge leaving this node and entering next_node

        weight    Suppose this node has 3 outgoing edges, each with weights
                  1, 1, 1. Then the probability of going to a given node is 0.33.
                  If weights are 1, 2, 1, probabilities become 1/4, 1/2, 1/4
                  (we normalize them).
        """
        # Make sure we don't accidentally add two edges to the same node
        for curr in self._edges:
            assert(curr != next_node), "Edge already exists"
        
        assert(weight > 0), "Weight shouldn't be non-positive"

        self._edges.append((weight, next_node))

    def next(self):
        """
        Randomly select an edge
        """
        assert(len(self._edges) > 0), "Each node should have at least one outgoing edge"
        next_nodes = [next_node for weight, next_node in self._edges]
        weights = [weight for weight, next_node in self._edges]
        return choices(next_nodes, weights=weights)[0]

    @abstractmethod
    def _get_children(self):
        """
        Should return a list of Note objects. These are played
        simultaneously whenever the current node is played.
        For example, [SimpleNote("C"), SimpleNote("E"), SimpleNote("G")]

        Note: Your list can contain GraphNode objects too, or anything,
              that implements emit() (as long as emit() returns instructions)
        """
        pass

    def emit(self, time, duration):
        """
        Returns a list of instructions

        Parameters:
            time        The time at which this node should be played (seconds)
            duration    For how long should the node be played? (seconds)
        """
        return [x.emit(time, duration) for x in self._get_children()]

    @property
    def final(self):
        return self._final

# TODO Could inherit from Chord for conciseness
class Triad(GraphNode):
    """
    Visiting this node generates a triad
    """
    def __init__(self, root, third, fifth, final=False):
        """
        Play a triad consisting of the three notes
        """
        super().__init__(final=final)
        chord = [root, third, fifth]
        self._children = [SimpleNote(note) for note in chord]
        
    def _get_children(self):
        return self._children


class Chord(GraphNode):
    """
    Visiting this node plays any chord
    """
    def __init__(self, chord, final=False):
        super().__init__()
        self._children = [SimpleNote(note) for note in chord]
        
    def _get_children(self):
        return self._children


if __name__ == "__main__":
    # A very casual testing of our tonic
    t = Triad("C3", "E3", "G3")
    print(t.emit(0, 0))

    # Test hooking up graphs
    a, b, c = Triad("C3", "E3", "G3"), Triad("C3", "E3", "G3"), Triad("C3", "E3", "G3")
    t.add_edge(c, 3)
    t.add_edge(b, 3)
    t.add_edge(a, 3)

    # Make sure distribution is sane
    bins = [0,0,0]
    for _ in range(100):
        n = t.next()
        if n == a:
            bins[0] += 1
        elif n == b:
            bins[1] += 1
        elif n == c:
            bins[2] += 1
    
    print(bins)
