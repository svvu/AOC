#!/usr/bin/env python3

import argparse

def add_pots_if_need(pots, start_pot_num):
    if '#' in pots[0:5]:
        pots = f".....{pots}"
        start_pot_num -= 5
    if '#' in pots[-5:-1]:
        pots = f"{pots}....."
    return (pots, start_pot_num)

def grow(pots, rules, gen_num):
    start_pot_num = 0
    stable_generation = None
    generation_changes = []

    p_change = count_pots_num(pots, start_pot_num)
    for gen in range(1, gen_num+1):
        (pots, start_pot_num) = add_pots_if_need(pots, start_pot_num)

        growed_pots = pots[0:2]

        for i in range(2, len(pots)-2):
            rule = rules.get(pots[i-2:i+3])
            if rule:
                growed_pots += rule
            else:
                growed_pots += '.'

        pots = growed_pots + pots[-2:-1]

        change = count_pots_num(pots, start_pot_num)
        generation_changes.append(change - p_change)
        p_change = change

        if len(generation_changes) > 50:
            generation_changes.pop(0)

        # This means the plans expand consistent on both side with same amount.
        # size 50 is kinda random
        if len(generation_changes) == 50 and len(set(generation_changes)) == 1:
            stable_generation = gen
            break

    gen_left = gen_num - (stable_generation or gen_num)
    return pots, count_pots_num(pots, start_pot_num) + gen_left * generation_changes[-1]

def count_pots_num(pots, start_pot_num):
    return sum(idx + start_pot_num for idx, pot in enumerate(list(pots)) if pot == '#')

def main():
    """
    The pots are numbered, with 0 in front of you. To the left, the pots are
    numbered -1, -2, -3, and so on; to the right, 1, 2, 3.... Your puzzle input
    contains a list of pots from 0 to the right and whether they do (#) or
    do not (.) currently contain a plant, the initial state. (No other pots
    currently contain plants.) For example, an initial state of #..##....
    indicates that pots 0, 3, and 4 currently contain plants.

    Your puzzle input also contains some notes you find on a nearby table:
    someone has been trying to figure out how these plants spread to nearby pots.
    Based on the notes, for each generation of plants, a given pot has or does
    not have a plant based on whether that pot (and the two pots on either side
    of it) had a plant in the last generation. These are written as LLCRR => N,
    where L are pots to the left, C is the current pot being considered, R are
    the pots to the right, and N is whether the current pot will have a plant in the next generation.
    For example:
        A note like ..#.. => . means that a pot that contains a plant but with no
            plants within two pots of it will not have a plant in it during the next generation.
        A note like ##.## => . means that an empty pot with two plants on each
            side of it will remain empty in the next generation.
        A note like .##.# => # means that a pot has a plant in a given generation
            if, in the previous generation, there were plants in that pot,
            the one immediately to the left, and the one two pots to the right,
            but not in the ones immediately to the right and two to the left.
    """
    parser = argparse.ArgumentParser(description='Subterranean Sustainability')
    parser.add_argument('-i', dest='file_path', help='path to input data file',
                        required=True)

    init_state = None
    rules = {}

    args = parser.parse_args()
    with open(args.file_path, 'r') as file:
        lines = file.readlines()

        init_state = lines[0].replace('\n', '').replace('initial state: ', '')

        rule_strings = filter(None, [line.replace('\n', '') for line in lines[1:]])
        for rs in rule_strings:
            rule_data = rs.split(' => ')
            rules[rule_data[0]] = rule_data[1]

    (pots, count) = grow(init_state, rules, 20)

    print("Sum of pot num after %s generation: %s" % (20, count))

    (pots, count) = grow(init_state, rules, 50000000000)

    print("Sum of pot num after %s generation: %s" % (50000000000, count))

if __name__ == '__main__':
    main()
