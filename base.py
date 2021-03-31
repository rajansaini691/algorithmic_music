"""
This is probably completely useless, and the code will probably
be quite poorly-written, but I wanted to see if it could be done.

Main idea:
  Have a composition or accompaniment be partially-encoded
  into a graph with weighted edges, where weights represent
  probabilities of taking a transition.

  We then traverse the graph, keeping track of time
  as a function of tempo (set globally) and tick number (take 1
  transition per tick). 

  Each time we reach a node, emit a set of instructions based
  on the type of node. 
  
  This is an example "instruction"
  @  0   3.5 SineEnv 0.3 260   .011 .2 0.0

  It would be really cool if we could add ties. Unfortunately,
  I'm keeping the code generator stateless for now (though
  this may change in the future).

MVP Architecture:
  Let's say we have the following graph:
     I <-----------|
     |---> IV ---> V
     v     |
     III --
   
   Now, each node will want to have its own
   set of "instructions" to emit. We could
   have each node inherit from a common base
   class and implement some method emit(),
   which returns a list of note structures. 
   The generator could go through the graph for
   a preset number of iterations and fill up
   a large note list while assigning times
   (keep a local variable storing the time).

Note structure:
   A note has several properties, which are synth-specific.
   Custom notes should inherit from this base, and it should
   also have an emit method

Nice-haves:
   Handle swing
   Abstract key from harmonic function (when the given node
   is a chord rather than a note)
   Hold notes between ticks
"""
from abc import ABC, abstractmethod


class GraphNode(ABC):
    """
    An element of the composition graph thing
    """
    @abstractmethod
    def emit():
        """
        Should return a list of Note objects. These are played
        simultaneously whenever the current node is played.
        For example, 
        """
        pass

class Note(ABC):
    """
    Corresponds to a single note instruction, e.g.
    @  0   3.5 SineEnv 0.3 260   .011 .2 0.0
    """
    @abstractmethod
    def emit():
        # TODO Word this better
        """
        Should return a string converting the note's data to its allolib
        format
        """
        pass

class Tonic(GraphNode):
    """
    Let's just assume we're in the key of C for now
    """
    def emit():
        return []
