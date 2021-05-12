"""
Generate a blues phrase
"""
from melody_types import *
from note_constraints import add_note_constraints
from note_filler import fill_notes
from direction_filler import fill_directions
from note_generator import song_to_string, song_to_allolib

blues_scale = Scale('F', [0, 3, 5, 7, 10])

# Main melody
blues_structure = Phrase(
    phrase_elements=[
        Segment(6), LandingNote(duration=2, pitch='F4'), Rest(4), Rest(6), Rest(6),
        Segment(6), LandingNote(duration=2, pitch='F4'), Rest(4), Rest(6), Rest(6),
        Segment(6), LandingNote(duration=2, pitch='Bb4'), Rest(4), Rest(6), Rest(6),
        Segment(6), LandingNote(duration=2, pitch='F4'), Rest(4), Rest(6), Rest(6),
        Segment(6), LandingNote(duration=2, pitch='C5'), Rest(4),
        Segment(6), LandingNote(duration=2, pitch='Bb4'), Rest(4),
        Segment(6), LandingNote(duration=2, pitch='F4'), Rest(4)
        ],
    scale=blues_scale)
phrases = [blues_structure]
song = Song(phrases = phrases)

fill_directions(song)
add_note_constraints(song)
fill_notes(song)

print(song_to_allolib(song))

accompaniment = Phrase(
    phrase_elements=[
        Rest(6), LandingNote(duration=6*3, pitch='F3'),
        Rest(6), LandingNote(duration=6*3, pitch='F3'),
        Rest(6), LandingNote(duration=6*3, pitch='Bb3'),
        Rest(6), LandingNote(duration=6*3, pitch='F3'),
        Rest(6), LandingNote(duration=6, pitch='C4'),
        Rest(6), LandingNote(duration=6, pitch='Bb3'),
        Rest(6), LandingNote(duration=6*3, pitch='F3'),
    ],
    scale=blues_scale)

phrases = [accompaniment]

song = Song(phrases = phrases)

fill_directions(song)
add_note_constraints(song)
fill_notes(song)

print(song_to_allolib(song))
