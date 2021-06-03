"""
Defines all of a song's layers of abstraction. If this file
is unwieldy to go through, please split it up.
"""
from dataclasses import dataclass
import enum
from helpers import note_name_to_midi, midi_to_note_name
from scale import Scale

# The direction the notes in a segment should go
class SegmentDirection(enum.Enum):
    UP = 1
    UPDOWN = 2
    STRAIGHT = 3
    DOWNUP = 4
    DOWN = 5

class DynamicChange(enum.Enum):
    CRESCENDO = 1
    DECRESCENDO = 2

# TODO Add more
class Dynamic(enum.Enum):
    MP = 1
    MF = 2

# TODO Add more
class Articulation(enum.Enum):
    STACCATO = 1
    TENUTO = 2

class Mood(enum.Enum):
    MAJOR = 1
    MINOR = 2

@dataclass
class PhraseElement:
    duration: int = 2

@dataclass
class Rest(PhraseElement):
    pass

@dataclass
class Note:
    # TODO Dynamic stuff
    pitch: int
    articulation: Articulation = None
    grace: bool = False
    duration: int = 2
    importance: int = 0.5   # [0, 1]
    new: bool = False
    
    def get_final_dynamic():
        # TODO Stub
        return 1

    def to_string(self):
        note = midi_to_note_name(self.pitch)
        star = "*" if self.new else ""
        return note + star
        

@dataclass
class LandingNote(PhraseElement):
    pitch: int = 'A7'   # Can be a note name or midi number
    duration: int = 2
    articulation: Articulation = None

    def __post_init__(self):
        if type(self.pitch) == str:
            self.pitch = note_name_to_midi(self.pitch)

@dataclass
class Segment(PhraseElement):
    duration: int
    direction: SegmentDirection = None
    dynamic_change: DynamicChange = None
    dynamic: Dynamic = None
    new_note: int = None        # If the segment contains a new/special note, stores its pitch
    notes: list[Note] = None
    scale_constraints: list[int] = None    # Pair, [low, high]
    scale_width: int = None     # Number of note pitches allowed in segment, based on constraints


# TODO Make HarmonyElement class and inherit from that
@dataclass
class HarmonyNote(PhraseElement):   # A single note played in the harmony.
    pitch: int = 'A7'   # Can be a note name or midi number
    duration: int = 2
    dynamic: Dynamic = None
    articulation: Articulation = None
    dynamic_change: DynamicChange = None

    def __post_init__(self):
        if type(self.pitch) == str:
            self.pitch = note_name_to_midi(self.pitch)

@dataclass
class Chord(PhraseElement):     # Holds a collection of HarmonyNotes; played simultaneously
    notes: list[HarmonyNote] = None
    dynamic_change: DynamicChange = None    # Overrides dynamic change of individual notes

@dataclass
class HarmonyLine:  # Stores multiple harmonic lines to be played simultaneously
    harmony_elements: list[PhraseElement]
    instrument: str = "Vib"

@dataclass
class Phrase:
    # TODO Add option to inherit scale from Song
    scale: Scale
    phrase_elements: list[PhraseElement]
    time_signature: list[int]  # Should be [upper, lower]
    atomic_unit: float      # Fraction of a whole note
    tempo: int = 120
    chords: (str, int) = None   # Contains a list of chords/arpegiatted notes
    harmony: list[HarmonyLine] = None   # Contains a list of chords/arpegiatted notes
    harmonic_level: int = 0
    mood: Mood = None

@dataclass
class Song:
    phrases: list[Phrase]
