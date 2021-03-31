
from abc import ABC, abstractmethod
from note import SimpleNote

class GraphNode(ABC):
    """
    An element of the composition graph thing
    """
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
        chord = ["C", "E", "G"]
        return [SimpleNote()]
