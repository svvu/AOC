#!/usr/bin/env python3

import argparse

def calculate_checksum_by_min_max(data):
    """Calculate checksum for input data by summing (max value - min value) of each line"""
    checksum = 0
    for line_data in data:
        min_value = min(line_data)
        max_value = max(line_data)
        checksum += max_value - min_value
    return checksum

def calculate_checksum_by_divisible(data):
    """Calculate checksum for data by summing 2 numbers are divisble to each other in each line"""
    check_sum = 0
    # Method 1
    # for line_data in data:
    #     value_set = set()
    #     sorted_data = sorted(line_data, reverse=True)
    #     max_value = sorted_data[0]

    #     for value in sorted_data:
    #         for i in range(2, int(max_value / value)+1):
    #             if value * i in value_set:
    #                 check_sum += i
    #         value_set.add(value)

    # Method 2
    for line_data in data:
        check_values = []
        for value in line_data:
            for t_value in check_values:
                if value > t_value and value % t_value == 0:
                    check_sum += int(value / t_value)
                elif t_value % value == 0:
                    check_sum += int(t_value / value)
            check_values.append(value)

    return check_sum

def main():
    """Corruption Checksum.

    Calculate the checksum for spreadsheet consists of rows of random numbers.
    Mode:
    - min_max: For each row, determine the difference between the largest value and the
               smallest value; the checksum is the sum of all of these differences.
    - divisible: Find the only two numbers in each row where one evenly divides the other,
                 the checksum is the sum of the divided value.
    """
    parser = argparse.ArgumentParser(description='Calculate the checksum for spreadsheet '
                                                 'consists of rows of random numbers')
    parser.add_argument('-i', dest='file_path', help='path to input data file',
                        required=True)
    parser.add_argument('-t', dest='type', help='algorithm type to calculate checksum',
                        choices=['min_max', 'divisible'], default='min_max')

    args = parser.parse_args()

    with open(args.file_path, 'r') as file:
        lines = file.readlines()
        input_data = [[int(value) for value in line.split(' ')] for line in lines]

    if args.type == 'min_max':
        print(calculate_checksum_by_min_max(input_data))
    else:
        print(calculate_checksum_by_divisible(input_data))

if __name__ == '__main__':
    main()
