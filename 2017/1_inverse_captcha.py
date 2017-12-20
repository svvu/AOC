#!/usr/bin/env python3

import argparse

def cal_match_dight_sum(data, step=1):
    """Calculate the sum for dight that match the next digit in the list.

    The list is circular, so the next dight for the last digit is the first one.

    Keyword arguments:
    data -- the data list to calculate
    step -- how many digit ahead to check match (default 1)

    Ex:
    1122 -> 3
    91212129 -> 9
    """

    data_len = len(data)
    if data_len <= 1:
        return 0

    sum_value = 0

    for index, char in enumerate(data):
        next_char = data[get_next_index(data_len, index, step)]

        if char == next_char:
            sum_value += int(char)

    return sum_value

def get_next_index(length, current, step):
    """Get the next index by step.

    If the next index is greater than the length, it loop back to the beginning.
    """
    next_index = current + step
    if next_index >= length:
        return next_index % length
    else:
        return next_index

def main():
    """Inverse Captcha.

    The captcha requires to review a sequence of digits and find the sum of all
    digits that match the next digit / n dight ahead in the list.

    Ex:
    1122 with step 1 -> 3
    1212 with percent step 0.5 -> 6 because all dights match 2 dight ahead
    """
    parser = argparse.ArgumentParser(description='Calculate the sum for digit if it equal \n'
                                                 'to the dight step N ahead in a circular list')
    parser.add_argument('-i', dest='file_path', help='path to input data file',
                        required=True)
    parser.add_argument('-s', dest='step', type=int, default=1,
                        help='step to look ahead to check match')
    parser.add_argument('-p', dest='percent_step', type=float,
                        help='percent of the whole list to look ahead to \n'
                             'check match, ex: 0.5 means look ahead by half \n'
                             'of the length of the data. If this is set, it \n'
                             'will take over -s')

    args = parser.parse_args()

    with open(args.file_path, 'r') as file:
        input_data = file.read()

    data = list(input_data)
    step = int(len(data) * args.percent_step) if args.percent_step else args.step

    sum_value = cal_match_dight_sum(data, step)

    print(sum_value)

if __name__ == '__main__':
    main()
