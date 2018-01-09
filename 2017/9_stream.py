#!/usr/bin/env python3

import argparse

OPEN_GROUP_TOEKN = '{'
CLOSE_GROUP_TOEKN = '}'
OPEN_JUNK_TOEKN = '<'
CLOSE_JUNK_TOEKN = '>'
IGNORE_TOEKN = '!'

def calculate_score_and_garbage(data):
    """Calculate the group score and the number of garbage characters for input data
    """
    score = 0
    current_group = 0
    in_junk = False
    ignore = False
    garbage = 0

    for token in data:
        if ignore:
            ignore = False
            continue
        elif in_junk:
            if token == IGNORE_TOEKN:
                ignore = True
            elif token == CLOSE_JUNK_TOEKN:
                in_junk = False
            else:
                garbage += 1
        elif token == OPEN_JUNK_TOEKN:
            in_junk = True
        elif token == OPEN_GROUP_TOEKN:
            current_group += 1
        elif token == CLOSE_GROUP_TOEKN:
            score += current_group
            current_group -= 1

    return score, garbage

def main():
    """Stream Processing

    The characters represent groups - sequences that begin with { and end with }.
    Within a group, there are zero or more other things,
    separated by commas: either another group or garbage.
    Since groups can contain other groups, a } only closes the most-recently-opened
    unclosed group - that is, they are nestable.

    Garbage begins with < and ends with >. Between those angle brackets,
    almost any character can appear, including { and }. Within garbage, < has no special meaning.

    Cancel character !: inside garbage, any character that comes after ! should
    be ignored, including <, >, and even another !.
    Ex: {{<!>},{<!>},{<!>},{<a>}}, 2 groups (since all but the last > are canceled).

    Each group is assigned a score which is one more than the score of the group
    that immediately contains it. (The outermost group gets a score of 1.)
    Ex: {{<a!>},{<a!>},{<a!>},{<ab>}}, score of 1 + 2 = 3.

    Garbage characters num: character within the garbage, the leading and trailing < and >
    don't count, nor do any canceled characters or the ! doing the canceling.
    """
    parser = argparse.ArgumentParser(description='Stream Processing')
    parser.add_argument('-i', dest='file_path', help='path to input data file',
                        required=True)

    args = parser.parse_args()
    with open(args.file_path, 'r') as file:
        input_data = file.readlines()

    score = garbage = 0
    for data in input_data:
        cscore, cgarbage = calculate_score_and_garbage(data)
        score += cscore
        garbage += cgarbage

    print("Score: %s" % score)
    print("Garbage characters: %s" % garbage)

if __name__ == '__main__':
    main()
