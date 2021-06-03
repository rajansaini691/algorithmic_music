

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

def chord_name_to_notes(chord_name, tonic=None, major=False, minor=False):
    """
    Finds the corresponding triad for the provided chord name. If no tonic
    is passed, this function will return a list of offsets from the tonic
    (so [0, 4, 7] for a major chord, for example). Otherwise, if a tonic
    is passed, finds the chord above the tonic (so I for 'C4' is
    ['C4', 'E4', 'G4']).

    major and minor refer to the SCALE, not the chord itself, so that
    the III, VI, and VII chords are returned correctly.
    """
    assert(major != minor)
    major_pattern = [0, 4, 7]
    minor_pattern = [0, 3, 7]
    major_scale = [0, 2, 4, 5, 7, 9, 11]
    minor_scale = [0, 2, 3, 5, 7, 8, 10]
    chord_degrees = None

    # Major
    if 'I' in chord_name or 'V' in chord_name:
        major_chord_to_scale_degree = {
                'I': 1, 'II': 2, 'III': 3, 'IV': 4,
                'V': 5, 'VI': 6, 'VII': 7}
        degree = major_chord_to_scale_degree[chord_name]
        offset = major_scale[degree-1] if major else minor_scale[degree-1]
        chord_degrees = [offset + x for x in major_pattern]


    if 'i' in chord_name or 'v' in chord_name:
        minor_chord_to_scale_degree = {
                'i': 1, 'ii': 2, 'iii': 3, 'iv': 4,
                'v': 5, 'vi': 6, 'vii': 7}
        degree = minor_chord_to_scale_degree[chord_name]
        offset = major_scale[degree-1] if major else minor_scale[degree-1]
        chord_degrees = [offset + x for x in minor_pattern]


    if tonic is not None:
        return [x + tonic for x in chord_degrees]
    else:
        return chord_degrees


if __name__ == "__main__":
    test = 'A0 B0 C4 D5 C#3 Ab8'.split(' ')
    for x in test:
        assert(x == midi_to_note_name(note_name_to_midi(x)))
    test = 'I'
    notes = chord_name_to_notes(test, note_name_to_midi('C4'), minor=True)
    for x in notes:
        print(midi_to_note_name(x))
