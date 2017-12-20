#!/usr/bin/env python3

import argparse

def find_exit(instructions, rule):
    """Find the steps to exit the maze by the rule"""
    steps = 0
    pos = 0
    while pos < len(instructions):
        steps += 1
        instr = instructions[pos]
        instructions[pos] = rule(instr)
        pos += instr
    return steps

def rule1(val):
    """Increase current instruction by 1"""
    return val + 1

def rule2(val):
    """If current instruction is 3 or more, decrease by 1, otherwise, rule 1."""
    if val >= 3:
        return val -1
    else:
        return rule1(val)


def main():
    """A Maze of Twisty Trampolines, All Alike
    The message includes a list of the offsets for each jump.
    Jumps are relative: -1 moves to the previous instruction, and 2 skips the next one.
    Start at the first instruction in the list. The goal is to follow the jumps
    until one leads outside the list.

    Rule 1: After each jump, the offset of that instruction increases by 1
    Rule 2: After each jump, if the offset was three or more, instead decrease it by 1.
        Otherwise, increase it by 1 as before.
    """
    parser = argparse.ArgumentParser(description="A Maze of Twisty Trampolines, All Alike")
    parser.add_argument('-i', dest='file_path', help='path to input data file',
                        required=True)
    parser.add_argument('-r', dest='rule', choices=[1, 2], default=1, help='rule type')

    args = parser.parse_args()
    with open(args.file_path, 'r') as file:
        input_data = [int(val) for val in file.readlines()]

    if args.rule == 1:
        print(find_exit(input_data, rule1))
    else:
        print(find_exit(input_data, rule2))

if __name__ == '__main__':
    main()
