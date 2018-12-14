#!/usr/bin/env python3

import argparse

CONNNERS = {
    '/': {
        '^': '>',
        'v': '<',
        '<': 'v',
        '>': '^'
    },
    '\\': {
        '^': '<',
        'v': '>',
        '<': '^',
        '>': 'v'
    }
}
INTERSECTION_TURNS = ['left', 'straight', 'right']
INTERSECTIONS = {
    '>': {
        INTERSECTION_TURNS[0]: '^',
        INTERSECTION_TURNS[1]: '>',
        INTERSECTION_TURNS[2]: 'v'
    },
    '<': {
        INTERSECTION_TURNS[0]: 'v',
        INTERSECTION_TURNS[1]: '<',
        INTERSECTION_TURNS[2]: '^'
    },
    'v': {
        INTERSECTION_TURNS[0]: '>',
        INTERSECTION_TURNS[1]: 'v',
        INTERSECTION_TURNS[2]: '<'
    },
    '^': {
        INTERSECTION_TURNS[0]: '<',
        INTERSECTION_TURNS[1]: '^',
        INTERSECTION_TURNS[2]: '>'
    }
}

class Cart:
    def __init__(self, x, y, direct):
        self.x = x
        self.y = y
        self.direct = direct
        self.inter_num = 0
        self.crash = False

    def next_track(self):
        if self.direct == '<':
            return (self.x - 1, self.y)
        elif self.direct == '>':
            return (self.x + 1, self.y)
        elif self.direct == 'v':
            return (self.x, self.y + 1)
        elif self.direct == '^':
            return (self.x, self.y - 1)

class Track:
    def __init__(self, tracks):
        self.tracks = tracks

    def move_cart(self, cart):
        (x, y) = cart.next_track()
        track = self.tracks[y][x]
        if track in CONNNERS:
            cart.direct = CONNNERS[track][cart.direct]
        elif track == '+':
            cart.direct = INTERSECTIONS[cart.direct][INTERSECTION_TURNS[cart.inter_num % 3]]
            cart.inter_num += 1

        cart.x = x
        cart.y = y

def check_crash_cart(carts, cart):
    crashed_cart = (c for c in carts if not c == cart and not c.crash and cart.x == c.x and cart.y == c.y)
    return next(crashed_cart, None)

def sort_carts(carts):
    return sorted(carts, key=lambda c: (c.y, c.x))

def tick(tracks, carts):
    # printTrack(tracks, carts)
    first_crash = None
    while True:
        safe_carts = []
        for cart in carts:
            if cart.crash:
                continue
            tracks.move_cart(cart)
            cc = check_crash_cart(carts, cart)
            if cc:
                if not first_crash:
                    first_crash = (cc.x, cc.y)
                cc.crash = True
                cart.crash = True
                if cc in safe_carts:
                    safe_carts.remove(cc)
            else:
                safe_carts.append(cart)
        carts = safe_carts
        if len(carts) == 1:
            break
        # printTrack(tracks, carts)
        carts = sort_carts(carts)
    return (first_crash, (carts[0].x, carts[0].y))

def printTrack(track, carts):
    tracks = [[tc[:] for tc in tr] for tr in track.tracks]
    for c in carts:
        if not c.crash:
            tracks[c.y][c.x] = c.direct

    print('\n'.join([''.join(t) for t in tracks]))

def main():
    """
    Tracks consist of straight paths (| and -), curves (/ and \), and
    intersections (+). Curves connect exactly two perpendicular pieces of track;
    for example, this is a closed loop:
        /----\
        |    |
        |    |
        \----/
    Intersections occur when two perpendicular paths cross. At an intersection,
    a cart is capable of turning left, turning right, or continuing straight.
    Here are two loops connected by two intersections:
        /-----\
        |     |
        |  /--+--\
        |  |  |  |
        \--+--/  |
        |     |
        \-----/
    Several carts are also on the tracks. Carts always face either up (^),
    down (v), left (<), or right (>). (On your initial map, the track under
    each cart is a straight path matching the direction the cart is facing.)

    Each time a cart has the option to turn (by arriving at any intersection),
    it turns left the first time,
    goes straight the second time,
    turns right the third time,
    and then repeats those directions starting again with left the fourth time,
    straight the fifth time, and so on. This process is independent of the
    particular intersection at which the cart has arrived - that is,
    the cart has no per-intersection memory.

    Carts all move at the same speed; they take turns moving a single step at a
    time. They do this based on their current location: carts on the top row move
    first (acting from left to right), then carts on the second row move (again
    from left to right), then carts on the third row, and so on. Once each cart
    has moved one step, the process repeats; each of these loops is called a tick.
    """
    parser = argparse.ArgumentParser(description='Mine Cart Madness')
    parser.add_argument('-i', dest='file_path', help='path to input data file',
                        required=True)

    tracks = []
    carts = []
    args = parser.parse_args()
    with open(args.file_path, 'r') as file:
        for row, line in enumerate(file.read().splitlines()):
            row_tracks = []
            for col, t in enumerate(list(line)):
                if t == '<' or t == '>':
                    row_tracks.append('-')
                    carts.append(Cart(col, row, t))
                elif t == 'v' or t == '^':
                    row_tracks.append('|')
                    carts.append(Cart(col, row, t))
                else:
                    row_tracks.append(t)
            tracks.append(row_tracks)

    track = Track(tracks)
    (first_crash, remaining) = tick(track, carts)
    print('First crash at: %s, %s' % first_crash)
    print('Last cart at: %s, %s' % remaining)

if __name__ == '__main__':
    main()
