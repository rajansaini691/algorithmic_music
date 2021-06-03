"""
The direction_filler iterates through a song's phrases and gives each phrase segment
a direction.

Precondition:
    The song has phrases

Postcondition:
    Each phrase segment within the song now has a direction
"""
from melody_types import *
import random


def _fill_directions_random(song):
    """
    Randomly gives directions to each segment; does not accumulate state
    """
    for phrase in song.phrases:
        for pe in phrase.phrase_elements:
            if type(pe) == Segment:
                pe.direction = random.choice(list(SegmentDirection))

# TODO Have user pass weights
def _fill_directions_weighted(song):
    """
    Randomly gives directions, but with a preference for certain motions
    """
    directions = [SegmentDirection.UP, SegmentDirection.DOWN, SegmentDirection.UPDOWN,
            SegmentDirection.DOWNUP, SegmentDirection.STRAIGHT]
    weights = [1, 1, 4, 4, 0.5]
    normalized_weights = [x / sum(weights) for x in weights]
    for phrase in song.phrases:
        for pe in phrase.phrase_elements:
            if type(pe) == Segment:
                pe.direction = random.choices(directions, weights=weights, k=1)[0]
    

def fill_directions(song):
    """
    Precondition:
        The song has phrases

    Postcondition:
        Each phrase segment within the song now has a direction
    """
    # Assert precondition
    assert(len(song.phrases) > 0)

    # TODO Have the user pass in a string or enum that determines
    # the filling technique, then add a switch here
    _fill_directions_weighted(song)

    # Assert postcondition
    for phrase in song.phrases:
        for pe in phrase.phrase_elements:
            if type(pe) == Segment:
                assert(pe.direction is not None)

if __name__ == "__main__":
    # Do a unit test, make sure nothing breaks
    scale = Scale()
    first_phrase = Phrase(phrase_elements=[Segment(6), Rest(1), Segment(3)], scale=scale)
    second_phrase = Phrase(phrase_elements=[Segment(6), Rest(1), Segment(2)], scale=scale)
    phrases = [first_phrase, second_phrase]
    song = Song(phrases = phrases)

    fill_directions(song)
