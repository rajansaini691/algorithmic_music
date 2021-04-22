
# Allolib State Machine Thing
This weird compiler-like program will generate a complex set of allolib instructions from a simple graph!

## Motivation
State machines seem to represent many music-theoretical constructs quite naturally. For example, functional harmony relies on the fact that some transitions between some chords are more pleasing than others. We can encode these transitions into a formal, graph-like structure and then generate music by "hopping" between chords. If a node has multiple outgoing edges (i.e., many possible chords can follow from a given one), one will automatically be chosen randomly based on user-supplied weights.

## Usage
1. Write your graph down first. It could be composed of many things, like chords that move between each other or notes that move stepwise. 
   For example:
   ![](./doc/Diatonic-Harmony-Chart-Major.png)
2. Encode your graph using `GraphNode` objects. Because this program is still under active development, the API is constantly changing. Follow `./cadence.py` for a good example.
3. Plug the output into allolib!

## Files
`idea.md` - My initial stream-of-consciousness

`generator/` - Contains the behind-the-scenes stuff (graph aggregation and codegen)

`cadence.py` - A fully-functional example
