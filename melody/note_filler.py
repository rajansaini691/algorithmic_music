"""
Contains various algorithms for filling in a song's notes.
fill_notes is the only exposed method; all others are
swappable implementations.
"""
from scale import Scale
from melody_types import *
from direction_filler import fill_directions
from note_constraints import add_note_constraints
import random


def _generate_possible_notes(num_notes, constraints, scale, direction):
    """
    Return a list of all possible notes in the given scale 
    that satisfy the given constraints and move in the given
    direction.

    Parameters:
        num_notes       How many notes to return
        constraints     [lowest_note, highest_note]
        scale           A Scale object
        direction       A SegmentDirection

    Returns:
        None if no combinations are possible
    """
    num_notes = int(num_notes)
    lowest_note, highest_note = constraints
    result = []

    if direction == SegmentDirection.UP:
        curr = lowest_note
        while curr <= highest_note:
            seq = [scale.skip_up(curr, n) for n in range(0, num_notes)]
            if seq[-1] <= highest_note:
                result += [seq]
            curr = scale.step_up(curr)
        return result

    if direction == SegmentDirection.DOWN:
        curr = highest_note
        while curr >= lowest_note:
            seq = [scale.skip_down(curr, n) for n in range(0, num_notes)]
            if seq[-1] >= lowest_note:
                result += [seq]
            curr = scale.step_down(curr)
        return result

    if direction == SegmentDirection.STRAIGHT:
        curr = lowest_note
        while curr <= highest_note:
            seq = [curr for n in range(0, num_notes)]
            result += [seq]
            curr = scale.step_up(curr)
        return result

    if direction == SegmentDirection.UPDOWN:
        curr = lowest_note
        while curr <= highest_note:
            for n in range(1, num_notes - 1):
                up = [scale.skip_up(curr, i) for i in range(0, n+1)]
                down = [scale.skip_down(up[-1], i) for i in range(1,num_notes-n)]

                assert(len(up) > 0 and len(down) > 0 and len(up+down) == num_notes)
                assert(up[-1] >= up[0] and down[-1] <= down[0])

                if max(up) > highest_note or min(down) < lowest_note:
                    continue

                result += [up+down]
            curr = scale.step_up(curr)
        return result

    if direction == SegmentDirection.DOWNUP:
        curr = highest_note
        while curr >= lowest_note:
            for n in range(1, num_notes - 1):
                down = [scale.skip_down(curr, i) for i in range(0, n+1)]
                up = [scale.skip_up(down[-1], i) for i in range(1,num_notes-n)]

                assert(len(up) > 0 and len(down) > 0 and len(up+down) == num_notes)
                assert(up[-1] >= up[0] and down[-1] <= down[0])

                if max(up) > highest_note or min(down) < lowest_note:
                    continue
                result += [down+up]
            curr = scale.step_down(curr)
        return result



    assert(False), f"{direction} NotImplemented"

def _fill_notes_stepwise(song):
    """
    This algorithm uses the song's scale to randomly fill in
    each segment's notes stepwise, such that scale constraints
    are obeyed. It does not look ahead at any landing points,
    take any characteristic phrases into account, nor favor
    particular sequences. It also assigns one note per beat.
    """
    for phrase in song.phrases:
        for segment in phrase.phrase_elements:
            if type(segment) != Segment:
                continue
            
            num_notes = segment.duration

            potential_sequences = _generate_possible_notes(
                    num_notes, segment.scale_constraints,
                    phrase.scale, segment.direction)
            assert(len(potential_sequences) > 0)

            note_pitches = random.choice(potential_sequences)

            segment.notes = [Note(pitch, new=pitch==segment.new_note, duration=1) for pitch in note_pitches]


# TODO Add a switch, so different algorithms can be chosen by the user
def fill_notes(song):
    """
    Fills in the notes of a song.
    Preconditions:
        The song's has at least one phrase
        Each phrase has at least one segment
        Each segment has a direction and some note constraints
    """
    # TODO Assert preconditions

    return _fill_notes_stepwise(song)

if __name__ == "__main__":
    from helpers import note_name_to_midi

    c_pentatonic = Scale('C', [0, 3, 5, 8, 10])
    first_phrase = Phrase(phrase_elements=[Segment(6), LandingNote(duration=2, pitch='Eb4'), Rest(1), Segment(4)], scale=c_pentatonic)
    second_phrase = Phrase(phrase_elements=[Segment(6), LandingNote(duration=2, pitch='F4'), Rest(1), Segment(2)], scale=c_pentatonic)
    phrases = [first_phrase, second_phrase]
    song = Song(phrases = phrases)

    sequences = _generate_possible_notes(
        6, [note_name_to_midi('C4'), note_name_to_midi('C5')],
        c_pentatonic, SegmentDirection.DOWNUP)

    fill_directions(song)
    add_note_constraints(song)
    fill_notes(song)

