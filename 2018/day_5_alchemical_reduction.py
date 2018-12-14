#!/usr/bin/env python3

import argparse

def reduce(polymer, ignore_unit=''):
    reduced = []

    for c in polymer:
        last = reduced[-1] if reduced else ''
        if c.upper() == ignore_unit.upper():
            continue
        if c != last and c.upper() == last.upper():
            del reduced[-1]
        else:
            reduced.append(c)

    return ''.join(reduced)

def find_shorest_polymer(polymer):
    tried = set()
    shortest = ''
    for c in polymer:
        if c.upper() in tried:
            continue
        else:
            tried.add(c.upper())
            reduced = reduce(polymer, c)
            if not shortest or len(shortest) > len(reduced):
                shortest = reduced
    return shortest


def main():
    """
    The polymer is formed by smaller units which, when triggered,
    react with each other such that two adjacent units of the same type
    and opposite polarity are destroyed. Units' types are represented by l
    etters; units' polarity is represented by capitalization.
    For instance, r and R are units with the same type but opposite
    polarity, whereas r and s are entirely different types and do not react.
    Ex: dabAcCaCBAcCcaDA -> dabCBAcaDA

    1) Find the length polymer after reduce
    2) One of the unit types is causing problems;
    it's preventing the polymer from collapsing as much as it should.
    Figure out which unit type is causing the most problems,
    remove all instances of it (regardless of polarity),
    fully react the remaining polymer, and measure its length.
    Ex: dabAcCaCBAcCcaDA, remove all C/c produce length 4
    """
    parser = argparse.ArgumentParser(description='Alchemical Reduction')
    parser.add_argument('-i', dest='file_path', help='path to input data file',
                        required=True)

    args = parser.parse_args()
    with open(args.file_path, 'r') as file:
        input_data = file.read()

    reduced_polymer = reduce(input_data)
    print('Length of polymer: %s' % len(reduced_polymer))

    shortest = find_shorest_polymer(reduced_polymer)
    print('Length of shortest polymer: %s' % len(shortest))

if __name__ == '__main__':
    main()
