"""
Adds note constraints to each segment, so that they cannot exceed a
certain threshold.

Precondition:
    Each segment has a direction assigned

Postcondition:
    Each segment has an assigned set of scale constraints
"""
from melody_types import *
from direction_filler import fill_directions
import random

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
        # Get first landing note in each phrase
        first_landing_note = None
        for pe in phrase.phrase_elements:
            if type(pe) == LandingNote:
                first_landing_note = pe.pitch
                break

        assert(first_landing_note != None), "There should be at least one landing note per phrase"

        low = high = first_landing_note

        # How many segments to skip before adding another new note
        # in the same direction
        add_below_cooldown = add_above_cooldown = 0

        # Create constraints
        for pe in phrase.phrase_elements:
            if type(pe) == Segment:
                add_below = add_above = False
                if pe.direction == SegmentDirection.UP:
                    add_below |= _flip(0.4)
                if pe.direction == SegmentDirection.DOWN:
                    add_above |= _flip(0.4)
                if pe.direction == SegmentDirection.DOWNUP:
                    add_above |= _flip(0.4)
                if pe.direction == SegmentDirection.UPDOWN:
                    add_below |= _flip(0.4)

                # Require cooldown to be zero before adding a new note
                add_below &= add_below_cooldown == 0
                add_above &= add_above_cooldown == 0

                # Update the cooldown
                if add_below_cooldown > 0:
                    add_below_cooldown -= 1
                if add_above_cooldown > 0:
                    add_above_cooldown -= 1

                # TODO Update the constraints, note that a new note will be added
                # (above or below), add a field in Segment to reflect the new note,
                # update the cooldown

                if add_above:
                    add_above_cooldown = 1
                    high += 1
                    pe.new_note = high

                if add_below:
                    add_below_cooldown = 1
                    low -= 1
                    pe.new_note = low
                
                pe.scale_constraints = [low, high]
                print([low, high])



def add_note_constraints(song):
    # TODO Add documentation, assertions for pre/postconditions
    _expanding_method(song)


if __name__ == "__main__":
    scale = Scale()
    first_phrase = Phrase(phrase_elements=[Segment(6), LandingNote(duration=2, pitch='A4'), Rest(1), Segment(3)], scale=scale)
    second_phrase = Phrase(phrase_elements=[Segment(6), LandingNote(duration=2, pitch='F4'), Rest(1), Segment(2)], scale=scale)
    phrases = [first_phrase, second_phrase]
    song = Song(phrases = phrases)

    fill_directions(song)
    add_note_constraints(song)
