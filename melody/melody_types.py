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
    pitch: int = 'A7'
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
    scale_width: int = None    # Number of note pitches allowed in segment, based on constraints
    tempo: int = None
    tempo_change: int = None # TODO Change to an enum

@dataclass
class Phrase:
    # TODO Add option to inherit scale from Song
    scale: Scale
    phrase_elements: list[PhraseElement]

@dataclass
class Song:
    phrases: list[Phrase]
