## Main idea
Have a composition or accompaniment be partially-encoded into a graph with weighted edges, where weights represent probabilities of taking a transition.

We traverse the graph, keeping track of time as a function of tempo (set globally) and tick number (take 1 transition per tick). 

Each time we reach a node, emit a set of instructions based on the type of node. 

This is an example "instruction":
  ```
  @  0   3.5 SineEnv 0.3 260   .011 .2 0.0
  ```

It would be really cool if we could add ties. Unfortunately, I'm keeping the code generator stateless for now (though this may change in the future).

## Architecture (MVP)
Let's say we want to model functional harmony using the following graph:
  ```
     I <-----------|
     |---> IV ---> V
     v     ^
     III __|
  ```

Now, each node will want to have its own set of "instructions" to emit. We could have each node inherit from a common base class and implement some method emit(), which returns a list of note structures. The generator could go through the graph for a preset number of iterations and fill up a large note list while assigning times (keep a local variable storing the time).

## Note structure
A note has several properties, which are synth-specific. Custom notes should inherit from this base, and it should also have an emit method

## Nice-haves
  - Handle swing
  - Abstract key from harmonic function (when the given node is a chord rather than a note)
  - Hold notes between ticks
