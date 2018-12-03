#!/usr/bin/env python3

import argparse
from enum import Enum

class Direction(Enum):
    """Direction the enum for the hexagons"""
    N = 0
    NE = 1
    SE = 2
    S = 3
    SW = 4
    NW = 5


def cal_steps(directions):
    """cal_steps calculate the smallest steps need to reach the destionation"""
    direction_count = {
        Direction.N: 0,
        Direction.NE: 0,
        Direction.SE: 0,
        Direction.S: 0,
        Direction.SW: 0,
        Direction.NW: 0,
    }

    for direction in directions:
        direct = Direction[direction.upper()]

        opp_direct = Direction((direct.value + 3) % 6)
        complment_direct_1 = Direction((direct.value + 2) % 6)
        complment_direct_2 = Direction((direct.value + 4) % 6)

        if direction_count[opp_direct] > 0:
            direction_count[opp_direct] -= 1
        elif direction_count[complment_direct_1] > 0:
            direction_count[complment_direct_1] -= 1
            ajd_direction = Direction((direct.value + 1) % 6)
            direction_count[ajd_direction] += 1
        elif direction_count[complment_direct_2] > 0:
            direction_count[complment_direct_2] -= 1
            ajd_direction = Direction((direct.value + 5) % 6)
            direction_count[ajd_direction] += 1
        else:
            direction_count[direct] += 1

    steps = 0
    for _, count in direction_count.items():
        steps += count

    return steps

def main():
    """Hex Ed
    """
    parser = argparse.ArgumentParser(description='Hex Ed')
    parser.add_argument('-i', dest='file_path', help='path to input data file',
                        required=True)

    args = parser.parse_args()
    with open(args.file_path, 'r') as file:
        input_data = [d for line in file.readlines() for d in line.split(',')]

    print(cal_steps(input_data))

if __name__ == '__main__':
    main()
