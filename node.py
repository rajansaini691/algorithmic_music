
from abc import ABC, abstractmethod
from note import SimpleNote
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
    def __init__(self):
        """
        Please call me when inheriting
        """
        self._edges = []

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
        next_nodes = [next_node for weight, next_node in self._edges]
        weights = [weight for weight, next_node in self._edges]
        return choices(next_nodes, weights=weights)[0]

    @abstractmethod
    def emit(self):
        """
        Should return a list of Note objects. These are played
        simultaneously whenever the current node is played.
        For example, [SimpleNote("C"), SimpleNote("E"), SimpleNote("G")]
        """
        pass

class Tonic(GraphNode):
    """
    Let's just assume we're in the key of C for now
    """
    def emit(self):
        chord = ["C3", "E3", "G3"]
        return [SimpleNote(note) for note in chord]


if __name__ == "__main__":
    # A very casual testing of our tonic
    t = Tonic()
    notes = t.emit()
    print([note.emit(0) for note in notes])

    # Test hooking up graphs
    a, b, c = Tonic(), Tonic(), Tonic()
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
