from tables import *

from math import log
import dll
import random

ROOK_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
BISHOP_DIRECTIONS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

def bit(x, y):
    i = y * 8 + x
    return 1 << i

def bb_bits(x):
    result = []
    for i in xrange(64):
        if x & (1 << i):
            result.append(i)
    return result

def bb_print(bb):
    bb = bin(bb)[2:]
    bb = ('0' * (64 - len(bb))) + bb
    bb = ''.join(reversed(bb))
    for y in xrange(8):
        i = (7 - y) * 8
        print bb[i:i+8]
    print

def slide(i, truncate, obstacles, directions):
    bb = 0
    px = i % 8
    py = i / 8
    for dx, dy in directions:
        previous = None
        for m in range(1, 9):
            x = px + dx * m
            y = py + dy * m
            if x < 0 or y < 0 or x > 7 or y > 7:
                if previous and truncate:
                    bb &= ~bit(*previous)
                break
            bb |= bit(x, y)
            if bit(x, y) & obstacles:
                break
            previous = (x, y)
    return bb

def rook_slide(i, truncate, obstacles):
    return slide(i, truncate, obstacles, ROOK_DIRECTIONS)

def bishop_slide(i, truncate, obstacles):
    return slide(i, truncate, obstacles, BISHOP_DIRECTIONS)

ROOK6 = [rook_slide(i, True, 0) for i in range(64)]
ROOK8 = [rook_slide(i, False, 0) for i in range(64)]
BISHOP6 = [bishop_slide(i, True, 0) for i in range(64)]
BISHOP8 = [bishop_slide(i, False, 0) for i in range(64)]

def rook_mapping(sq):
    result = {}
    bits = bb_bits(ROOK6[sq])
    n = len(bits)
    for i in xrange(2 ** n):
        bb = 0
        for j in xrange(n):
            if i & (1 << j):
                bb |= 1 << bits[j]
        result[bb] = rook_slide(sq, False, bb)
    return result

def bishop_mapping(sq):
    result = {}
    bits = bb_bits(BISHOP6[sq])
    n = len(bits)
    for i in xrange(2 ** n):
        bb = 0
        for j in xrange(n):
            if i & (1 << j):
                bb |= 1 << bits[j]
        result[bb] = bishop_slide(sq, False, bb)
    return result

ROOK_MAPPING = [rook_mapping(i) for i in range(64)]
BISHOP_MAPPING = [bishop_mapping(i) for i in range(64)]

def dump_map(x):
    print '#define LENGTH %d' % len(x)
    print '#define BITS %d' % (log(len(x)) / log(2))
    print
    keys = ', '.join('0x%016x' % k for k in sorted(x))
    print 'bb KEYS[] = {%s};' % keys
    values = ', '.join('0x%016x' % x[k] for k in sorted(x))
    print 'bb VALUES[] = {%s};' % values

def generate_lookup_tables():
    mask = 0xffffffffffffffff
    table = []
    offsets = []
    for i in range(64):
        sub = {}
        for k, v in BISHOP_MAPPING[i].items():
            x = ((k * MAGIC_BISHOP[i]) & mask) >> SHIFT_BISHOP[i]
            sub[x] = v
        sub = [sub.get(j, 0) for j in range(max(sub) + 1)]
        offsets.append(len(table))
        table.extend(sub)
    # for x in table:
    #     print '0x%016x,' % x
    table = []
    offsets = []
    for i in range(64):
        sub = {}
        for k, v in ROOK_MAPPING[i].items():
            x = ((k * MAGIC_ROOK[i]) & mask) >> SHIFT_ROOK[i]
            sub[x] = v
        sub = [sub.get(j, 0) for j in range(max(sub) + 1)]
        offsets.append(len(table))
        table.extend(sub)
    # for x in table:
    #     print '0x%016x,' % x

def random_rook(sq):
    bb = 0
    for i in range(20):
        bb |= 1 << random.randint(0, 63)
    bb_print(bb)
    bb &= ROOK6[sq]
    bb *= MAGIC_ROOK[sq]
    bb &= 0xffffffffffffffff
    bb >>= SHIFT_ROOK[sq]
    bb = ATTACK_ROOK[bb + OFFSET_ROOK[sq]]
    bb_print(bb)

def random_bishop(sq):
    bb = 0
    for i in range(20):
        bb |= 1 << random.randint(0, 63)
    bb_print(bb)
    bb &= BISHOP6[sq]
    bb *= MAGIC_BISHOP[sq]
    bb &= 0xffffffffffffffff
    bb >>= SHIFT_BISHOP[sq]
    bb = ATTACK_BISHOP[bb + OFFSET_BISHOP[sq]]
    bb_print(bb)

def main():
    # generate_lookup_tables()
    random_bishop(0)
    return
    for i in range(64):
        magic = dll.magic_search_random(BISHOP_MAPPING[i])
        print '%2d, 0x%016x' % (i, magic)
    for i in range(64):
        magic = dll.magic_search_random(ROOK_MAPPING[i])
        print '%2d, 0x%016x' % (i, magic)

if __name__ == '__main__':
    main()
