"""
Contains various visualization methods
"""
from melody_types import *
from note_constraints import add_note_constraints
from note_filler import fill_notes
from direction_filler import fill_directions
from helpers import midi_to_note_name

# TODO Put in helpers.py
def mid2freq(pitch):
    assert(0 <= pitch <= 127)
    return 2**((pitch - 69)/12) * 440

def song_to_allolib(song):
    """
    Generate allolib instructions from the song
    Right now, use with SineEnv module
    @  0.0  2.0 SineEnv 0.3 261.6255653005986   .011 .5 0.0
    """
    out = ""
    time = 0
    for phrase in song.phrases:
        multiplier = phrase.atomic_unit * phrase.time_signature[1] / phrase.tempo * 60
        for token in phrase.phrase_elements:
            if type(token) == Rest:
                out += f"# Rest for {token.duration * multiplier} half-beats\n"
                time += token.duration * multiplier
            if type(token) == Segment:
                for note in token.notes:
                    out += f"# {midi_to_note_name(note.pitch)}\n"
                    out += f"@ {time} {note.duration * multiplier} SineEnv 0.3 {mid2freq(note.pitch)} 0.11 0.5 0.0\n\n"
                    time += note.duration * multiplier
            if type(token) == LandingNote:
                out += f"# {midi_to_note_name(token.pitch)}\n"
                out += f"@ {time} {token.duration * multiplier} SineEnv 0.6 {mid2freq(token.pitch)} 0.11 0.5 0.0\n\n"
                time += token.duration * multiplier
    # FIXME Debugging hack
    return out 
 

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
                notes = ''.join(f"{note.to_string()}\t" for note in token.notes)
                notes = notes if len(token.notes) == token.duration//2 else "*\t" * token.duration
                out += notes

                low, high = token.scale_constraints
                constraints = f"[{midi_to_note_name(low)}, {midi_to_note_name(high)}]"
                out += "\t" + constraints
            if type(token) == LandingNote:
                out += midi_to_note_name(token.pitch) + "\t" + "|\t" * (token.duration - 1)
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

    print(song_to_allolib(song))
