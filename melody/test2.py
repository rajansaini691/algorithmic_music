"""
Generate a phrase
"""
from melody_types import *
from note_constraints import add_note_constraints
from note_filler import fill_notes
from direction_filler import fill_directions
from note_generator import song_to_string, song_to_allolib

# yaman = Scale('C', ([0, 2, 4, 6, 9, 11], [12, 11, 9, 7, 6, 4, 2, 0]), same_up_down=False)
lydian_scale = Scale('C', ([0, 2, 4, 6, 7, 9, 11]))
melodic_minor_scale = Scale('C', ([0, 2, 3, 5, 7, 9, 11]))
bhairavi = Scale('C', [0, 1, 3, 5, 7, 8, 10])

# Main melody
lydian_phrase = Phrase(
    phrase_elements=[
        LandingNote(duration=2, pitch='E4'), Rest(2),
        Segment(4), Segment(4),
        LandingNote(duration=2, pitch='C4'), Rest(2),
        Segment(8),
        LandingNote(duration=2, pitch='B3'), Rest(2),
        Segment(8),
        LandingNote(duration=2, pitch='C4'), Rest(6),
        ],
    scale=lydian_scale)


melodic_minor_phrase = Phrase(
    phrase_elements=[
        LandingNote(duration=2, pitch='Eb4'), Rest(2),
        Segment(4), Segment(4),
        LandingNote(duration=2, pitch='C4'), Rest(2),
        Segment(8),
        LandingNote(duration=2, pitch='B3'), Rest(2),
        Segment(6),
        LandingNote(duration=2, pitch='C4'), Rest(2),
        ],
    scale=melodic_minor_scale)

bhairavi_phrase = Phrase(
    phrase_elements=[
        Segment(10), LandingNote(duration=2, pitch='G4'),
        Segment(8),
        Segment(8),
        Segment(8),
        Segment(8),
        Segment(8),
        LandingNote(duration=2, pitch='C4')
    ],
    scale=bhairavi)


phrases = [lydian_phrase, melodic_minor_phrase]
#phrases = [bhairavi_phrase]

song = Song(phrases = phrases)

fill_directions(song)
add_note_constraints(song)
fill_notes(song)

print(song_to_allolib(song))


