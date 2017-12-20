#!/usr/bin/env python3

import argparse
import re

DISC_MAP = {}

class Disc:
    """Disc a class represent a disc's properties."""
    def __init__(self, name, weight, discs):
        self.name = name
        self.weight = weight
        self.sub_discs = discs

    def has_children(self):
        """Check whether or not the disc has sub-discs"""
        return True if self.sub_discs else False

    def check_balance(self):
        """Check whether or not the disc is balance or not

        Method return whether or not the disc is balance and the set of discs
        that are not balance if the disc is not balance.
        """
        if not self.has_children():
            return True, {}

        cmap = {}
        for child in self.sub_discs:
            child_disc = DISC_MAP[child]
            balance, c_map = child_disc.check_balance()
            if not balance:
                return balance, c_map
            cmap[child] = sum(c_map.values()) + child_disc.weight

        return len(set(cmap.values())) == 1, cmap

def find_unbalance_disc(disc_weight):
    """Find the disc that is not balance

    The disc that have different total weight than others will be returned.
    """
    weight_count = {}

    for key, value in disc_weight.items():
        if value in weight_count:
            weight_count[value].append(key)
        else:
            weight_count[value] = [key]

    sorted_count = sorted(weight_count.items(), key=lambda item: len(item[1]))
    unbalace_weight, unbalance_disc = sorted_count[0]
    balance_weight, _ = sorted_count[1]

    disc_name = unbalance_disc[0]

    disc = DISC_MAP[disc_name]
    return {
        "name": disc_name,
        "weight": disc.weight,
        "total_weight": unbalace_weight,
        "weight_diff": unbalace_weight - balance_weight
    }

def build_discs(input_data):
    """Build the disc map for the input data.

    Root disc will be returned.
    """
    parent_discs = set()
    child_discs = set()

    for line in input_data:
        # Parse disc representation.
        matches = re.match(r"(?P<name>^\w+) \((?P<weight>\d+)\)(.*(?<=-> )(?P<sub_discs>.*))?", line)
        name = matches.group('name')
        weight = matches.group('weight')
        if matches.group('sub_discs'):
            sub_discs = matches.group('sub_discs').split(', ')
        else:
            sub_discs = None

        disc = Disc(name, int(weight), sub_discs)
        DISC_MAP[disc.name] = disc

        if disc.has_children():
            parent_discs.add(disc.name)
            child_discs |= set(disc.sub_discs)

    root = parent_discs.difference(child_discs).pop()
    return DISC_MAP[root]

def main():
    """Recursive Circus

    One program at the bottom supports the entire tower. It's holding a large disc,
    and on the disc are balanced several more sub-towers. At the bottom of these sub-towers,
    standing on the bottom disc, are other programs, each holding their own disc, and so on.
    At the very tops of these sub-sub-sub-...-towers, many programs stand simply keeping
    the disc below them balanced but with no disc of their own.

    For any program holding a disc, each program standing on that disc forms a sub-tower.
    Each of those sub-towers are supposed to be the same weight, or the disc itself
    isn't balanced. The weight of a tower is the sum of the weights of the programs in that tower.
    """
    parser = argparse.ArgumentParser(description="Recursive Circus")
    parser.add_argument('-i', dest='file_path', help='path to input data file',
                        required=True)

    args = parser.parse_args()
    with open(args.file_path, 'r') as file:
        input_data = file.readlines()

    root = build_discs(input_data)
    print("Root is %s" % root.name)
    balance, weights = root.check_balance()
    if not balance:
        print("Unbalance disc is:")
        print(find_unbalance_disc(weights))

if __name__ == '__main__':
    main()
