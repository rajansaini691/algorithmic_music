# Architecture
## Main idea
Create data structures at different musical levels of abstraction; these will
be heavily driven by theory. For example, `Song` -> `Phrase` -> `Segment` -> `Notes` -> `Note` -> `Pitch`.

Separate data from algorithm. Data structures will be relatively pure,
algorithms create and modify them. The algorithms themselves will only depend
on a set of loose preconditions and postconditions, enabling them to be swapped
out. For example, there are many ways to add notes to phrases; it is important
for the programmer to be able to test out different techniques without breaking
the program.

## Frontend
Goal: 
  Allow the user to type a scale, rhythmic structure, and series of notes,
  and translate that into a series of allolib instructions.

### Original Text
Scale: C D E F G A B C    # C major
  E D C D | E E E _ | * * D ...

### Tokenized
[Scale([C, D, E, F ...]), Comment(" C major"), Note(E), Note(D), Note(C) ... ]

@Synth 0.1 we9jf 0290923 093939 
@Synth 0.1 we9jf 0290923 093939 
@Synth 0.1 we9jf 0290923 093939 
@Synth 0.1 we9jf 0290923 093939 
