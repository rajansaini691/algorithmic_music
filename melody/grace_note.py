import sys
from melody_types import *
import dataclasses
"""
Marks notes for grace notes
"""

# Mark grace notes on the peak note of every segment
def _peaks(song):
    for phrase in song.phrases:
        for pe in phrase.phrase_elements:
            if type(pe) == Segment:
                if pe.direction != SegmentDirection.UPDOWN:
                    continue

                # Get peak note
                for i in range(1, len(pe.notes)):
                    if pe.notes[i].pitch < pe.notes[i - 1].pitch:
                        pe.notes[i - 1].grace = True
                        print('sup', file=sys.stderr)
                        break

# Adds a grace note to consonant notes in every segment
def _consonant(song):
    pass

def _insert_grace_notes(song):
    for phrase in song.phrases:
        for pe in phrase.phrase_elements:
            if type(pe) != Segment:
                continue

            segment = pe
            initial_len = len(segment.notes)

            new_notes = []
            flag = False
            for i in range(len(pe.notes)):
                if segment.notes[i].grace and not flag:
                    new_note = Note(pitch=phrase.scale.skip_up(segment.notes[i].pitch, 1), new=True, duration=1/4)
                    new_notes += [new_note]
                    segment.notes[i].duration -= 1/4
                    flag = True
                new_notes += [dataclasses.replace(segment.notes[i])]

            assert(len(new_notes) - initial_len <= 1)
            pe.notes = list(new_notes)

def add_grace_notes(song):
    _peaks(song)
    _insert_grace_notes(song)
