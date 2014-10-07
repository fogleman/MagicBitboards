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
        # bb_print(bb)
        # bb_print(result[bb])
    return result

ROOK_MAPPING = [rook_mapping(i) for i in range(64)]
BISHOP_MAPPING = [bishop_mapping(i) for i in range(64)]

def dump_map(x):
    keys = ', '.join('0x%016x' % k for k in sorted(x))
    print 'bb KEYS[] = {%s};' % keys
    values = ', '.join('0x%016x' % x[k] for k in sorted(x))
    print 'bb VALUES[] = {%s};' % values
    print 'int LENGTH = %d;' % len(x)

def generate_tables():
    # rook6
    print '# rook6'
    for i in range(64):
        x = rook_slide(i, True)
        print '0x%016x,' % x
    # rook8
    print '# rook8'
    for i in range(64):
        x = rook_slide(i, False)
        print '0x%016x,' % x
    # bishop6
    print '# bishop6'
    for i in range(64):
        x = bishop_slide(i, True)
        print '0x%016x,' % x
    # bishop8
    print '# bishop8'
    for i in range(64):
        x = bishop_slide(i, False)
        print '0x%016x,' % x
    # bits
    for i in range(64):
        x = rook_slide(i, True)
        x = bishop_slide(i, True)

def main():
    dump_map(ROOK_MAPPING[0])
    return
    for i in range(64):
        print i, len(ROOK_MAPPING[i]), len(set(ROOK_MAPPING[i].values()))
    for i in range(64):
        print i, len(BISHOP_MAPPING[i]), len(set(BISHOP_MAPPING[i].values()))

if __name__ == '__main__':
    main()
