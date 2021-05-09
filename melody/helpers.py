

def note_name_to_midi(note_name):
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
        if len(note_name) == 2:
            _note, _octave = note_name
            _accidental = 0
            assert("A" <= _note <= "G")
            assert("0" <= _octave <= "8")
        elif len(note_name) == 3:
            _note, _accidental, _octave = note_name
            assert(_accidental == "b" or _accidental == "#")
            _accidental = -1 if _accidental == "b" else 1 if _accidental == "#" else 0

        _octave = int(_octave)

        # Go from note to chromatic scale degree 0-11 (starting from A)
        DEGREES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
        _note = DEGREES[_note]

        # Do some sketchy math to calculate the midi note
        midi_note = _octave * 12 + _accidental + _note + 12

        return midi_note


def midi_to_note_name(midi_note, scale=None):
    """
    Convert a MIDI note number to its human-readable name
    """
    # TODO Use scale to determine which enharmonic to use
    NOTES = 'C C# D Eb E F F# G Ab A Bb B'.split(' ')
    n = midi_note % 12
    note = NOTES[n]
    octave = midi_note // 12 - 1
    return f"{note}{octave}"


if __name__ == "__main__":
    test = 'A0 B0 C4 D5 C#3 Ab8'.split(' ')
    for x in test:
        assert(x == midi_to_note_name(note_name_to_midi(x)))
