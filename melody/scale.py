"""
Scale objects allow you to encode any scale. They are intentionally stateless, so that they can
be shared between many melodies.
"""
from dataclasses import dataclass
from collections import namedtuple
from helpers import midi_to_note_name
import copy


def note_name_to_scale_degree(note_name):
    """
    note_name   Name of the note; for ex "C", "Db", "F#"
    """
    lut = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    if len(note_name) == 1:
        return lut[note_name]
    if len(note_name) == 2:
        assert(note_name[1] == 'b' or note_name[1] == '#')
        accidental = -1 if note_name[1] == 'b' else 1
        return lut[note_name] + accidental

# TODO Transfer documentation onto SimplerScale
class Scale:
    def __init__(self, key, scale_degrees, name="[insert name]",
                 same_up_down=True, octave_duplication=True):
        """
        Initialize scale with notes and rules.
        Example:
            C major is key='C', scale_degrees=[0, 2, 4, 5, 7, 9, 11]
            D natural-minor is key='D', scale_degrees=[0, 2, 3, 5, 7, 8, 10]

        Parameters:
            key                     What note is the tonic? Pass in a string.
                                    For example, 'Db', 'B', 'A#'. 

            scale_degrees           A scale is defined by its scale degrees.
                                    For example, the major scale is
                                    [0, 2, 4, 5, 7, 9, 11].

            same_up_down            The scale is the same when going up and down.
                                    If this is set to False, please pass a tuple
                                    of (ascending_scale, descending_scale) to
                                    scale_degrees instead.
                                    This feature was intended to support Indian
                                    Ragas, many of which have separate ascending and
                                    descending scales (see aroh, avaroh).
                                    
            octave_duplication      The scale is the same at all octaves. This
                                    is True for all Western scales, but some
                                    Middle Eastern maqams require this to be
                                    set to False.
        """
        # Add a bunch of invariants to make sure implementation works
        assert(octave_duplication == True), """
            So sorry, we don't support scales that don't repeat at the 
            octave yet! Please post an issue if this feature is
            important to you.
        """
        assert(len(scale_degrees) > 0), "A scale needs at least one note"
        assert(not same_up_down or scale_degrees[0] == 0), "Make sure your scale's first note is the tonic (0)"
        
        if same_up_down:
            assert(all(x < y for x, y in zip(scale_degrees[0:], scale_degrees[1:]))), """
                Make sure your scale is strictly increasing
            """
        if not same_up_down:
            up, down = scale_degrees
            assert(all(x < y for x, y in zip(up[0:], up[1:]))), """
                Make sure ascending scale is strictly increasing
            """
            assert(all(x > y for x, y in zip(down[0:], down[1:]))), """
                Make sure descending scale is strictly decreasing 
            """
        assert(not octave_duplication or not same_up_down or scale_degrees[-1] < 12), """
            If you're duplicating at the octave, your scale needs to
            fit within one octave.
        """

        # TODO (Nice-have): Support non-octave-duplicating scales
        # TODO Harder but would be awesome: Support characteristic phrases

        # Use a poor man's double-linked-list.
        # Each node stores [pitch, note_above, note_below]
        @dataclass
        class ScaleDegreeNode:
            pitch: int
            note_above = None
            note_below = None

        # TODO Get scales with different up-and-down rules working
        assert(same_up_down), "Sadly not implemented yet :("

        # Get one octave working
        scale_degree_nodes = []
        for i in range(len(scale_degrees)):
            curr_pitch = scale_degrees[i]
            curr_node = ScaleDegreeNode(curr_pitch)
            prev_node = scale_degree_nodes[i-1] if i > 0 else None
            if prev_node is not None:
                prev_node.note_above = curr_node
                curr_node.note_below = prev_node
            scale_degree_nodes += [curr_node]

        # Now copy the list multiple times and stitch together
        scale_notes = []
        for oct_num in range(10):
            curr_oct = copy.deepcopy(scale_degree_nodes)
            for note in curr_oct:
                note.pitch += oct_num * 12

            # Stitch together
            if len(scale_notes) > 0:
                assert(curr_oct[0].note_below == None)
                curr_oct[0].note_below = scale_notes[-1]
                scale_notes[-1].note_above = curr_oct[0]

            scale_notes += curr_oct

        # Add the offset from the key
        tonic_offset = note_name_to_scale_degree(key)   # Number between 0 and 12
        for note in scale_notes:
            note.pitch += tonic_offset

        # Save a copy of the scale notes
        self._scale_notes = scale_notes


    # TODO Check neighboring notes too
    def step_up(self, current_note):
        """
        Gets the note in the scale one step above the current note

        Currently returns None if there is no note below the current one.
        """
        return self.skip_up(current_note, 1)


    # TODO Check neighboring notes too
    def step_down(self, current_note):
        """
        Gets the note in the scale one step below the current note

        Currently returns None if there is no note below the current one.
        """
        return self.skip_down(current_note, 1)

    def skip_up(self, current_note, n):
        """
        Gets a note in the scale n notes above the current note
        """
        node = None
        for note in self._scale_notes:
            if current_note == note.pitch:
                node = note

        for _ in range(n):
            if node is not None:
                node = node.note_above

        return node.pitch
        
    def skip_down(self, current_note, n):
        """
        Gets the note in the scale n notes below the current note
        """
        node = None
        for note in self._scale_notes:
            if current_note == note.pitch:
                node = note

        for _ in range(n):
            if node is not None:
                node = node.note_below

        return node.pitch


class SimplerScale(Scale):
    """
    A newer, better implementation of Scale

    To do C major, you must pass the equivalent of:
        C D E F G A B C (the final C is required to show that B can go to C)
    """
    def __init__(self, key, scale_name, scale=None, ascending_scale=None, descending_scale=None):
        assert((ascending_scale is not None) == (descending_scale is not None)), (
                "If you're passing an ascending scale, you need a "
                 "descending scale too, and vice-versa")
        assert((descending_scale is not None) != (scale is not None)), (
                "If your scale is the same going up and down, use scale "
                "and leave ascending/descending as None")

        self._scale_name = scale_name

        self._ascending_scale = ascending_scale if not scale else scale
        self._descending_scale = descending_scale if not scale else list(reversed(scale))

    def _step_helper(self, current_note, scale):
        octave = current_note // 12
        notes = set()

        # We subtract 1, since the last note in the scale shouldn't go to anything
        for i in range(len(scale) - 1):
            # sd stands for scale degree
            sd = scale[i]
            note = octave * 12 + sd

            if note % 12 == current_note % 12:
                num_steps = scale[i+1] - scale[i]
                next_note = current_note + num_steps
                notes.add(next_note)

        assert(len(notes) > 0), f"In {self._scale_name}, you can't move up from {midi_to_note_name(current_note)}"
        return notes

    def step_up(self, current_note):
        """
        Returns a set of notes that can be played one-step above the current;
        user may pick which one to use.
        """
        return self._step_helper(current_note, self._ascending_scale)

    def step_down(self, current_note):
        """
        Returns a set of notes that can be played one-step below the current;
        user may pick which one to use.
        """
        return self._step_helper(current_note, self._descending_scale)

    def skip_up(self, current_note, n):
        return self._ascending_scale.skip_up(current_note, n)

    def skip_down(self, current_note, n):
        return self.descending_scale.skip_down(current_note, n)

if __name__ == "__main__":
    s = Scale('C', [0, 2, 4, 5, 7, 9, 11])
    assert(s.step_down(60) == 59)
    assert(s.step_up(60) == 62) # C -> D
    assert(s.step_up(62) == 64) # D -> E
    assert(s.step_up(64) == 65) # E -> F

    # Test ascending-descending scale
    yaman_arohana = [-1, 2, 4, 6, 7, 6, 9, 11, 12]
    yaman_avarohana = [12, 11, 9, 7, 6, 4, 2, 0]
    yaman = SimplerScale('C', scale_name="yaman", ascending_scale=yaman_arohana, descending_scale=yaman_avarohana)

    # Test ascending
    assert(yaman.step_up(59) == {60, 62})
    assert(yaman.step_up(62) == {64})
    assert(yaman.step_up(64) == {66})
    assert(yaman.step_up(66) == {67, 69})
    assert(yaman.step_up(67) == {66})
    assert(yaman.step_up(69) == {71})
    assert(yaman.step_up(71) == {72, 74})

    # Test descending
    assert(yaman.step_down(72) == {71}) # S -> N
    assert(yaman.step_down(71) == {69}) # N -> Dh
    assert(yaman.step_down(69) == {67}) # Dh -> P
    assert(yaman.step_down(67) == {66}) # P -> M
    assert(yaman.step_down(66) == {64}) # M -> G
    assert(yaman.step_down(64) == {62}) # G -> R
    assert(yaman.step_down(62) == {60}) # R -> S

    # Test normal scale
    C = SimplerScale('C', scale_name='C major', scale=[0, 2, 4, 5, 7, 9, 11, 12])

    assert(C.step_up(60) == {62})   # C -> D
    assert(C.step_down(62) == {60}) # D -> C
    assert(C.step_up(62) == {64}) # D -> E
    assert(C.step_down(64) == {62}) # E -> D
    assert(C.step_up(64) == {65}) # E -> F
    assert(C.step_down(65) == {64}) # F -> E
    assert(C.step_up(65) == {67}) # F -> G
    assert(C.step_down(67) == {65}) # G -> F
    assert(C.step_up(64) == {65})   # B -> C
    assert(C.step_down(65) == {64}) # C -> B
