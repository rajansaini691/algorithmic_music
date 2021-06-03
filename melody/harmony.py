from helpers import midi_to_note_name, chord_name_to_notes
from melody_types import *

"""
Adds harmony to the melody
"""

def add_bass(phrase):
    # The tonic is super low by design, so we add 2 octaves
    bass_pitch = phrase.scale.tonic() + 2*12

    bass_line = HarmonyLine(harmony_elements=[])
    phrase.harmony = [bass_line]
    
    for chord, duration in phrase.chords:
        notes = chord_name_to_notes(chord, tonic=bass_pitch, major=(phrase.mood == Mood.MAJOR), minor=(phrase.mood == Mood.MINOR))
        phrase.harmony[0].harmony_elements += [HarmonyNote(pitch=notes[0], duration=duration, dynamic_change=DynamicChange.CRESCENDO)]

def add_repeated_bass(phrase):
    # The tonic is super low by design, so we add 2 octaves
    bass_pitch = phrase.scale.tonic() + 2*12

    if phrase.harmony is None:
        phrase.harmony = [HarmonyLine(harmony_elements=[]), HarmonyLine(harmony_elements=[])]
    elif len(phrase.harmony) < 2:
        phrase.harmony += [HarmonyLine(harmony_elements=[])]
    phrase.harmony[1].instrument = 'Saw'

    for chord, duration in phrase.chords:
        notes = chord_name_to_notes(chord, tonic=bass_pitch, major=(phrase.mood == Mood.MAJOR), minor=(phrase.mood == Mood.MINOR))
        print(notes)
        for i in range(duration):
            phrase.harmony[1].harmony_elements += [HarmonyNote(pitch=notes[0], duration=1)]

def add_harmony(song):
    """
    Adds harmony in successive stages
    """
    for phrase in song.phrases:
        if phrase.harmonic_level > 0:
            add_bass(phrase)
        if phrase.harmonic_level > 0:
            add_repeated_bass(phrase)
