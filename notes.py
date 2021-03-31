
class Note(ABC):
    """
    Corresponds to a single note instruction, e.g.
    @  0   3.5 SineEnv 0.3 260   .011 .2 0.0
    """
    def _mid2freq(self, pitch):
        assert(0 <= pitch <= 127)
        return 2**((pitch - 69)/12) * 440

    @abstractmethod
    def emit(self, time):
        # TODO Word this better
        """
        Should return a string converting the note's data to its allolib
        format

        Parameters:
            time            Time (seconds) at which the note should be played
        """
        pass

class SimpleNote(Note):
    """
    A _really_ simple note (sine wave, no attack, no release, no decay).
    Only pitch is controllable.
    """
    def __init__(self, pitch):
        """
        Parameters:
           pitch    The MIDI pitch, should be an integer between 0 and 127 (I think)
        """
        assert(0 <= pitch <= 127)
        self._freq = self._mid2freq(pitch)

    def emit(self, time):
        return f"@  {time}  3.5 SineEnv 0.3 {self._freq}   .011 .2 0.0"
