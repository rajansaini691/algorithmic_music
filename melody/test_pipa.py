
from melody_types import *
from note_constraints import add_note_constraints
from note_filler import fill_notes
from direction_filler import fill_directions
from note_generator import song_to_string, song_to_allolib
from harmony import add_harmony
from grace_note import add_grace_notes
import dataclasses
import copy

import sys

pentatonic_scale = Scale('A', ([0, 3, 5, 7, 10]))

# Main melody
pipa_phrase = Phrase(
    phrase_elements=[
        LandingNote(duration=3, pitch='A4'),
        LandingNote(duration=1, pitch='G4'),
        LandingNote(duration=4, pitch='A4'),
        Rest(3),
        Segment(5),
        LandingNote(duration=3, pitch='E4'),
        LandingNote(duration=1, pitch='D4'),
        LandingNote(duration=4, pitch='E4'),
        Rest(3),
        Segment(5),
        LandingNote(duration=3, pitch='D4'),
        LandingNote(duration=1, pitch='C4'),
        LandingNote(duration=4, pitch='D4'),
        Rest(3),
        Segment(5),
        LandingNote(duration=4, pitch='A3'),
        Rest(4),
        Segment(4),
        Segment(4),
        ],
    scale=pentatonic_scale, time_signature=[4,4], atomic_unit=1/8, tempo=90,
    chords=[('i', 16), ('v', 16), ('iv', 16), ('i', 8), ('VI', 4), ('VII', 4)],
    mood=Mood.MINOR)

# Resolution
resolution = Phrase(
    phrase_elements=[LandingNote(duration=4, pitch='A4')],
    scale=pentatonic_scale, time_signature=[4,4], atomic_unit=1/8, tempo=90,
    harmonic_level=0
)

first = copy.deepcopy(pipa_phrase)
first.harmonic_level = 0

second = copy.deepcopy(first)
second.harmonic_level = 1

third = copy.deepcopy(second)
third.harmonic_level = 2

phrases = [first, second, third, resolution]

song = Song(phrases = phrases)

fill_directions(song)
add_note_constraints(song)
fill_notes(song)
add_harmony(song)
add_grace_notes(song)

#print(song_to_string(song), file=sys.stderr)
print(song_to_allolib(song))
