from abc import ABC, abstractmethod

class Note(ABC):
    """
    Corresponds to a single note instruction, e.g.
    @  0   3.5 SineEnv 0.3 260   .011 .2 0.0
    """
    def _mid2freq(self, pitch):
        assert(0 <= pitch <= 127)
        return 2**((pitch - 69)/12) * 440


    def _name2mid(self, name):
        """
        Converts note name to MIDI using some dirty math. 
        
        Notes:
           Apologies for the messiness; cleaning this up would be really nice.

        Parameters:
           name         a string following the format "[A-G][b|#]?[0-9]",
                        like C7, A0. This represents the note name.
        """
        # TODO Use python regex to assert that name is properly formatted
        # TODO Need more descriptive error messages
        if len(name) == 2:
            _note, _octave = name
            _accidental = 0
            assert("A" <= _note <= "G")
            assert("0" <= _octave <= "8")
        elif len(name) == 3:
            _note, _accidental, _octave = name
            assert(_accidental == "b" or _accidental == "#")
            _accidental = -1 if _accidental == "b" else 1 if _accidental == "#" else 0

        _octave = int(_octave)

        # Go from note to chromatic scale degree 0-11 (starting from A)
        DEGREES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        _note = DEGREES[_note]

        # Do some sketchy math to calculate the midi note
        midi_note = _octave * 12 + _accidental + _note + 12

        return midi_note


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
           pitch    The MIDI pitch, should either be an integer between 0 and 127 (I think),
                    or the note name (e.g. C7, A2)
        """
        # TODO Might want to inherit this from a more general class
        if type(pitch) == type("A4"):
            pitch = self._name2mid(pitch)

        assert(0 <= pitch <= 127)

        self._freq = self._mid2freq(pitch)

    def emit(self, time):
        return f"@  {time}  3.5 SineEnv 0.3 {self._freq}   .011 .2 0.0"


if __name__ == "__main__":
    """
    Run some sanity checks
    """
    # Test the midi conversion methods
    assert(439 <= SimpleNote("A4")._freq <= 441)
    assert(439 <= SimpleNote(69)._freq <= 441)
