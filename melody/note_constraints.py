"""
Adds note constraints to each segment, so that they cannot exceed a
certain threshold.

Precondition:
    Each segment has a direction assigned

Postcondition:
    Each segment has an assigned scale width and set of scale constraints
"""
from melody_types import *
from direction_filler import fill_directions
from scale import Scale
import random
from helpers import midi_to_note_name

def _flip(weight):
    """
    Weighted coin flip, where weight is the probability of True.
    """
    assert(0 <= weight <= 1)
    return True if random.random() < weight else False

# TODO Create an algorithm that takes segment length into account,
# so that constraints can fit longer lengths.

# TODO Tweak constants
def _expanding_method(song):
    """
    Looks at landing note to see where the starting note
    should be. Then alternates between adding new notes
    above and new notes below. Does not take segment length
    into account.
    """
    for phrase in song.phrases:
        # Get the phrase's first landing note
        first_landing_note = None
        for pe in phrase.phrase_elements:
            if type(pe) == LandingNote:
                first_landing_note = pe.pitch
                break

        assert(first_landing_note != None), "There should be at least one landing note per phrase"

        # TODO Don't always start from below 
        # Get initial constraints using first segment length
        first_segment_length = 0
        for pe in phrase.phrase_elements:
            if type(pe) == Segment:
                first_segment_length = pe.duration // 2
                break

        high = first_landing_note
        low = phrase.scale.skip_down(first_landing_note, first_segment_length - 1)
        scale_width = 1

        # How many segments to skip before adding another new note
        # in the same direction
        add_below_cooldown = add_above_cooldown = 1

        # Create constraints
        for pe in phrase.phrase_elements:
            if type(pe) == Segment:
                add_below = add_above = False
                if (pe.direction == SegmentDirection.UP 
                    or pe.direction == SegmentDirection.UPDOWN):
                    add_below |= _flip(0.4)
                if (pe.direction == SegmentDirection.DOWN
                    or pe.direction == SegmentDirection.DOWNUP):
                    add_above |= _flip(0.4)

                # Require cooldown to be zero before adding a new note
                add_below &= add_below_cooldown == 0
                add_above &= add_above_cooldown == 0

                # Update the cooldown
                if add_below_cooldown > 0:
                    add_below_cooldown -= 1
                if add_above_cooldown > 0:
                    add_above_cooldown -= 1

                # Add the constraints
                if add_above:
                    add_above_cooldown = 1
                    high = phrase.scale.step_up(high)
                    pe.new_note = high
                    scale_width += 1

                if add_below:
                    add_below_cooldown = 1
                    low = phrase.scale.step_down(low)
                    pe.new_note = low
                    scale_width += 1
                
                pe.scale_constraints = [low, high]
                pe.scale_width = scale_width

def _get_first_landing_note(song):
    """
    Gets the first landing note in a song
    """
    for phrase in song.phrases:
        for pe in phrase.phrase_elements:
            if type(pe) == LandingNote:
                return pe.pitch

def _lookahead(song):
    """
    Makes sure landing notes are reached smoothly.

    Algorithm:
        For each segment,
            Get the first landing note played upon segment completion
            Make that landing note the bottom/top note of this segment
            if it lies outside the region
    """
    # Initialize landing_note to first note in song
    landing_note = _get_first_landing_note(song)
    assert(landing_note is not None)

    for phrase in reversed(song.phrases):
        for pe in reversed(phrase.phrase_elements):
            # The first note in this phrase element becomes the
            # landing note for the previous phrase element

            if type(pe) == Segment:
                segment = pe
                num_notes = segment.duration

                low = high = next_landing_note = 0
                constraint_range = 1        # max high - low

                if (segment.direction == SegmentDirection.UP or
                    segment.direction == SegmentDirection.DOWN):
                    constraint_range = num_notes

                if (segment.direction == SegmentDirection.UPDOWN or
                    segment.direction == SegmentDirection.DOWNUP):
                    constraint_range = num_notes - 2

                if (segment.direction == SegmentDirection.UP or
                    segment.direction == SegmentDirection.UPDOWN):
                    high = phrase.scale.step_down(landing_note)    # TODO This always arrives from below
                    low = phrase.scale.skip_down(landing_note, constraint_range+1)
                    next_landing_note = low      # For the previous phrase element

                    assert(high is not None)
                    assert(low is not None)

                if (segment.direction == SegmentDirection.DOWN or
                    segment.direction == SegmentDirection.DOWNUP):
                    low = phrase.scale.step_up(landing_note)       # TODO This always arrives from above
                    high = phrase.scale.skip_up(landing_note, constraint_range+1)
                    next_landing_note = high      # For the previous phrase element

                    assert(high is not None)
                    assert(low is not None)

                if segment.direction == SegmentDirection.STRAIGHT:
                    low = phrase.scale.step_up(landing_note) # TODO This always arrives from above
                    high = phrase.scale.step_up(landing_note)
                    next_landing_note = low

                segment.scale_constraints = [low, high]
                landing_note = next_landing_note

            if type(pe) == LandingNote:
                landing_note = pe.pitch


def add_note_constraints(song):
    # TODO Add documentation, assertions for pre/postconditions
    _lookahead(song)


if __name__ == "__main__":
    c_pentatonic = Scale('C', [0, 3, 5, 7, 10])
    first_phrase = Phrase(phrase_elements=[Segment(6), LandingNote(duration=2, pitch='Eb4'), Rest(1), Segment(3)], scale=c_pentatonic,
                            time_signature=[4,4], tempo=120, atomic_unit=1/8)
    second_phrase = Phrase(phrase_elements=[Segment(6), LandingNote(duration=2, pitch='F4'), Rest(1), Segment(2)], scale=c_pentatonic,
                            time_signature=[4,4], tempo=120, atomic_unit=1/8)
    phrases = [first_phrase, second_phrase]
    song = Song(phrases = phrases)

    fill_directions(song)
    add_note_constraints(song)
