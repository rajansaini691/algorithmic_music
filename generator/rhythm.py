"""
Generate rhythmic sequences, the downbeat of which we assign a note
"""
import random

def twos_and_threes(total=16):
    """
    Generate sequences of twos and threes that sum to the given total
    """
    assert(total >= 2), "input to twos_and_threes must be >= 2"

    if total == 2 or total == 3:
        return [total]

    if total == 4:
        return [2, 2]

    two_or_three = random.randint(2,3)
    return [two_or_three] + twos_and_threes(total - two_or_three)

def mutate(sequence, keep_begin=0, keep_end=0):
    """
    Generate a similar sequence, keeping stuff similar

    Parameters:
        sequence        A sequence of numbers like [2, 3, 3, 3, 3, 2]
        keep_begin      Number of numbers from beginning to preserve
        keep_end        Number of numbers from end to preserve
    """
    i = keep_begin
    j = len(sequence) - keep_end
    beginning = sequence[0:i]
    middle = sequence[i:j]
    end = sequence[j:]
    new_middle = middle

    while new_middle == middle:
        new_middle = twos_and_threes(sum(middle))

    return beginning + new_middle + end

def rhythmic_phrase():
    """
    Generate a list of 16-note sequences that are related enough
    to each other that they mimic improvisation
    """
    seq = twos_and_threes(16)
    sequences = [seq]

    # TODO Don't hardcode these
    beg_end = [(2, 2), (2, 1), (1, 1)]

    for b, e in beg_end:
        seq = mutate(seq, keep_begin=b, keep_end=e)
        sequences += [seq]

    return sequences

# TODO We can think of the beginning and ending subsequences
# as recurring ideas. We can use this information for automated
# phrasing, which is both cool and important. Accenting these 
# sections should yield good results, in theory.

if __name__ == "__main__":
    print(rhythmic_phrase())
