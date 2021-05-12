"""
Generate a phrase
"""
from melody_types import *
from note_constraints import add_note_constraints
from note_filler import fill_notes
from direction_filler import fill_directions
from note_generator import song_to_string, song_to_allolib

lydian_scale = Scale('C', ([0, 2, 3, 5, 7, 9, 11]))

# Main melody
lydian_phrase = Phrase(
    phrase_elements=[
        LandingNote(duration=2, pitch='Eb4'), Rest(2),
        Segment(4), Segment(4),
        LandingNote(duration=2, pitch='C4'), Rest(2),
        Segment(8),
        LandingNote(duration=2, pitch='B3'), Rest(2),
        Segment(8),
        LandingNote(duration=2, pitch='C4'), Rest(2),
        ],
    scale=lydian_scale)
phrases = [lydian_phrase]
song = Song(phrases = phrases)

fill_directions(song)
add_note_constraints(song)
fill_notes(song)

print(song_to_allolib(song))


