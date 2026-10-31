"""Generate and validate text combinations under assumed 6/33 + 1/16 rules."""
from math import comb
from random import SystemRandom
import sys


def validate(rows):
    keys = []
    for red, blue in rows:
        if len(red) != 6 or len(set(red)) != 6:
            raise ValueError('red balls must be six distinct integers')
        if any(type(x) is not int or not 1 <= x <= 33 for x in red):
            raise ValueError('red ball outside 1..33')
        if type(blue) is not int or not 1 <= blue <= 16:
            raise ValueError('blue ball outside 1..16')
        keys.append((tuple(sorted(red)), blue))
    if len(set(keys)) != len(keys):
        raise ValueError('duplicate complete combination')
    return True


def generate(count=1, red_pool=range(1, 34), blue_pool=range(1, 17), required=()):
    red = sorted(set(red_pool))
    blue = sorted(set(blue_pool))
    fixed = sorted(set(required))
    if type(count) is not int or count < 1:
        raise ValueError('count must be a positive integer')
    if any(type(x) is not int or not 1 <= x <= 33 for x in red + fixed):
        raise ValueError('invalid red pool or required ball')
    if any(type(x) is not int or not 1 <= x <= 16 for x in blue):
        raise ValueError('invalid blue pool')
    if len(fixed) > 6 or not set(fixed) <= set(red):
        raise ValueError('required balls conflict with allowed pool')
    remaining = [x for x in red if x not in fixed]
    slots = 6 - len(fixed)
    if len(remaining) < slots or not blue:
        raise ValueError('insufficient candidate balls')
    red_count = comb(len(remaining), slots)
    capacity = red_count * len(blue)
    if count > capacity:
        raise ValueError('requested count exceeds candidate capacity')
    rng = SystemRandom()
    # Sample ranks without replacement, then unrank lexicographic combinations.
    # This also terminates when the caller requests the entire candidate space.
    result = []
    for ticket in rng.sample(range(capacity), count):
        rank, blue_index = divmod(ticket, len(blue))
        chosen = []
        start = 0
        for left in range(slots, 0, -1):
            for index in range(start, len(remaining) - left + 1):
                block = comb(len(remaining) - index - 1, left - 1)
                if rank < block:
                    chosen.append(remaining[index])
                    start = index + 1
                    break
                rank -= block
        result.append((sorted(fixed + chosen), blue[blue_index]))
    validate(result)
    return result


if __name__ == '__main__':
    try:
        count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
        for red, blue in generate(count):
            print(' '.join(f'{x:02d}' for x in red) + f' | {blue:02d}')
        print('Assumed standard rules; current official rules not checked by this script.')
    except ValueError as error:
        raise SystemExit(str(error))
