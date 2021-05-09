"""
Contains various visualization methods
"""
from melody_types import *
from note_constraints import add_note_constraints
from note_filler import fill_notes
from direction_filler import fill_directions
from helpers import midi_to_note_name

def song_to_allolib(song):
    """
    Generate allolib instructions from the song
    """
    # TODO Implement
    pass

def song_to_string(song):
    """
    Return a string giving information about the song
    """
    out = ""
    for phrase in song.phrases:
        for token in phrase.phrase_elements:
            if type(token) == Rest:
                out += "_\t" * token.duration
            if type(token) == Segment:
                notes = ''.join(f"{midi_to_note_name(note.pitch)}\t" for note in token.notes)
                print(f"len: {len(token.notes)}, duration: {token.duration//2}")
                notes = notes if len(token.notes) == token.duration//2 else "*\t" * token.duration
                out += notes
            if type(token) == LandingNote:
                out += "|\t" * token.duration
        out += '\n'

    return out

if __name__ == "__main__":
    c_pentatonic = Scale('C', [0, 3, 5, 8, 10])
    first_phrase = Phrase(phrase_elements=[Segment(6), LandingNote(duration=2, pitch='Eb4'), Rest(1), Segment(4)], scale=c_pentatonic)
    second_phrase = Phrase(phrase_elements=[Segment(6), LandingNote(duration=2, pitch='F4'), Rest(1), Segment(2)], scale=c_pentatonic)
    phrases = [first_phrase, second_phrase]
    song = Song(phrases = phrases)

    fill_directions(song)
    add_note_constraints(song)
    fill_notes(song)

    print(song_to_string(song))
