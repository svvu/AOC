#!/usr/bin/env python3

import argparse
import re

class Claim:
    def __init__(self, claim_string):
        (cid, x_index, y_index, width, height) = self._parse_claim(claim_string)

        self.id = int(cid)
        self.x_index = int(x_index)
        self.y_index = int(y_index)
        self.width = int(width)
        self.height = int(height)
        self.overlap = False

    def get_inches(self):
        x_range = range(self.x_index, self.x_index + self.width)
        y_range = range(self.y_index, self.y_index + self.height)
        return [(x, y) for y in y_range for x in x_range]

    # ex claim string: #1 @ 906,735: 28x17
    def _parse_claim(self, claim_string):
        matches = re.match(
            r"^#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)$",
            claim_string
        )
        return (
            matches.group('id'),
            matches.group('x'),
            matches.group('y'),
            matches.group('w'),
            matches.group('h')
        )

def get_overlap_area(claims):
    area_used = [[False for i in range(1000)] for j in range(1000)]
    overlap_area = set()

    for claim in claims:
        claim_obj = Claim(claim)
        for (x_index, y_index) in claim_obj.get_inches():
            if area_used[x_index][y_index]:
                overlap_area.add((x_index, y_index))
            else:
                area_used[x_index][y_index] = True

    return overlap_area

def get_non_overlap(claims):
    area_used = [[[] for i in range(1000)] for j in range(1000)]
    claim_map = {}

    for claim in claims:
        claim_obj = Claim(claim)
        claim_map[claim_obj.id] = claim_obj

        for (x_index, y_index) in claim_obj.get_inches():
            if len(area_used[x_index][y_index]) >= 1:
                claim_obj.overlap = True
                for claim_id in area_used[x_index][y_index]:
                    claim_map[claim_id].overlap = True

            area_used[x_index][y_index].append(claim_obj.id)

    for claim in claim_map.values():
        if not claim.overlap:
            return claim

def main():
    """
    The whole piece of fabric they're working on is a very large square - at least

     1000 inches on each side.

    Each Elf has made a claim about which area of fabric would be ideal for Santa's
    suit. All claims have an ID and consist of a single rectangle with edges
    parallel to the edges of the fabric. Each claim's rectangle is defined as follows:
        The number of inches between the left edge of the fabric and the left edge of the rectangle.
        The number of inches between the top edge of the fabric and the top edge of the rectangle.
        The width of the rectangle in inches.
        The height of the rectangle in inches.

    A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3
    inches from the left edge, 2 inches from the top edge, 5 inches wide, and 4
    inches tall. Visually, it claims the square inches of fabric represented
    by # (and ignores the square inches of fabric represented by .) in the
    diagram below:
        ...........
        ...........
        ...#####...
        ...#####...
        ...#####...
        ...#####...
        ...........
        ...........
        ...........

    The problem is that many of the claims overlap, causing two or more claims
    to cover part of the same areas. For example, consider the following claims:
        #1 @ 1,3: 4x4
        #2 @ 3,1: 4x4
        #3 @ 5,5: 2x2

    Visually, these claim the following areas:
        ........
        ...2222.
        ...2222.
        .11XX22.
        .11XX22.
        .111133.
        .111133.
        ........
    The four square inches marked with X are claimed by both 1 and 2.
    (Claim 3, while adjacent to the others, does not overlap either of them.)
    """
    parser = argparse.ArgumentParser(description='No matter how to slice it')
    parser.add_argument('-i', dest='file_path', help='path to input data file',
                        required=True)

    args = parser.parse_args()
    with open(args.file_path, 'r') as file:
        input_data = file.readlines()

    o_area = get_overlap_area(input_data)
    print('Number of inches overlap: %s' % len(o_area))
    no_overlap = get_non_overlap(input_data)
    print('No overlap claim id: %s' % no_overlap.id)

if __name__ == '__main__':
    main()
