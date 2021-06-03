"""
Contains various visualization methods
"""
from melody_types import *
from note_constraints import add_note_constraints
from note_filler import fill_notes
from direction_filler import fill_directions
from helpers import midi_to_note_name
import sys

# TODO Put in helpers.py
def mid2freq(pitch):
    assert(0 <= pitch <= 127)
    return 2**((pitch - 69)/12) * 440

def sine_env(time, note_duration, amplitude, pitch, attack):
    return f"@ {time} {note_duration} SineEnv {amplitude} {mid2freq(pitch)} {attack} 0.5 0.0\n\n"

def plucked(time, note_duration, amplitude, pitch, attack):
    return f"@ {time} {note_duration} PluckedString {amplitude} {mid2freq(pitch)} 0.1 {attack} 1 -1 1 0.5\n\n"

def vib(time, note_duration, amplitude, pitch, attack):
    # Vib amplitude frequency attackTime releaseTime curve pan table vibRate1 vibRate2 vibRise vibDepth
    return f"@ {time} {note_duration} Vib {amplitude} {mid2freq(pitch-12)} {attack} 0 0 0 0 .05 .00005 0.5 .00  tbSaw\n\n"

def sub(time, note_duration, amplitude, pitch, attack):
    # amplitude frequency attackTime releaseTime sustain curve noise envDur cf1 cf2 cfRise bw1 bw2 bwRise hmnum hmamp pan
    return f"@ {time} {note_duration} Sub 0.8 {mid2freq(pitch)} 0.01 0 0.8 4 0.0 5 100 1000 1 20 20 0.5 10 1 0\n\n"
    
def saw(time, note_duration, amplitude, pitch, attack):
    # amplitude frequency attackTime releaseTime sustain curve noise envDur cf1 cf2 cfRise bw1 bw2 bwRise hmnum hmamp pan
    frequency = mid2freq(pitch)
    attackTime = 0.01
    releaseTime = note_duration
    sustain = 0.2
    curve = 5
    noise = 0
    envDur = 1
    cf1 = 400
    cf2 = 2000
    cfRise = 0.01
    bw1 = 700
    bw2 = 900
    bwRise = 0.5
    hmnum = 12
    hmamp = 1
    pan=0
    return f"@ {time} {note_duration} Sub {amplitude} {frequency} {attackTime} {releaseTime} {sustain} {curve} {noise} {envDur} {cf1} {cf2} {cfRise} {bw1} {bw2} {bwRise} {hmnum} {hmamp} {pan}\n\n"

def generate(time, note_duration, amplitude, pitch, attack, instrument="SineEnv"):
    if instrument == "SineEnv":
        return sine_env(time, note_duration, amplitude, pitch, attack)
    elif instrument == "Plucked":
        return plucked(time, note_duration, amplitude, pitch, attack)
    elif instrument == "Vib":
        return vib(time, note_duration, amplitude, pitch, attack)
    elif instrument == 'Sub':
        return sub(time, note_duration, amplitude, pitch, attack)
    elif instrument == 'Saw':
        return saw(time, note_duration, amplitude, pitch, attack)

def song_to_allolib(song):
    """
    Generate allolib instructions from the song
    Right now, use with SineEnv module
    @  0.0  2.0 SineEnv 0.3 261.6255653005986   .011 .5 0.0
    """
    out = ""

    # TODO Redo the entire time system here
    # Generate melody
    time = 0
    for phrase in song.phrases:
        multiplier = phrase.atomic_unit * phrase.time_signature[1] / phrase.tempo * 60
        phrase_start_time = time
        for token in phrase.phrase_elements:
            if type(token) == Rest:
                out += f"# Rest for {token.duration * multiplier} half-beats\n"
                time += token.duration * multiplier
            if type(token) == Segment:
                for note in token.notes:
                    out += f"# {midi_to_note_name(note.pitch)}\n"
                    out += generate(time, note.duration * multiplier, 0.6, note.pitch, 0.001, instrument='Plucked')
                    time += note.duration * multiplier
            if type(token) == LandingNote:
                out += f"# {midi_to_note_name(token.pitch)}\n"
                out += generate(time, token.duration * multiplier, 0.8, token.pitch, 0.001, instrument='Plucked')
                time += token.duration * multiplier

        # The next phrase will start here whether there's harmony or not
        next_phrase_start_time = time

        # Generate harmony
        multiplier = phrase.atomic_unit * phrase.time_signature[1] / phrase.tempo * 60

        if phrase.harmony == None:
            continue

        for harmonic_line in phrase.harmony:
            time = phrase_start_time
            instrument = harmonic_line.instrument
            for token in harmonic_line.harmony_elements:
                if type(token) == Chord:
                    assert(False), 'Not implemented yet :('
                elif type(token) == HarmonyNote:
                    note_duration = token.duration * multiplier
                    out += f"# {midi_to_note_name(token.pitch)}\n"
                    out += generate(time, note_duration, 0.3, token.pitch, note_duration, instrument=instrument)
                    time += note_duration

        phrase_start_time = next_phrase_start_time

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
                notes = notes if len(token.notes) == token.duration else "*\t" * token.duration
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
