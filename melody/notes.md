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
