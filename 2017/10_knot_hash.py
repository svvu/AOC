#!/usr/bin/env python3

import argparse
from functools import reduce

def cal_hash(data, hash_fun, times=1):
    """Calculate the hash value for the input"""
    hash_list = list(range(256))
    index = 0
    skip = 0

    for _ in range(times):
        for length in data:
            hash_list = reverse(hash_list, index, length)
            index = (index + length + skip) % len(hash_list)
            skip += 1

    return hash_fun(hash_list)


def reverse(hlist, index, length):
    """Reverse the elements between index and index + length"""
    list_len = len(hlist)
    for lth in range(int(length / 2)):
        c_index = (index + lth) % list_len
        t_index = (index + length - lth - 1) % list_len
        hlist[c_index], hlist[t_index] = hlist[t_index], hlist[c_index]

    return hlist

def multiplication_hash_fun(hash_list):
    """Generate the hash value by multiply the first two numbers in the list"""
    return hash_list[0] * hash_list[1]

def hex_hash_fun(hash_list):
    """"Generrate the hash value by convert the list to hex

    - Reduce the list by XOR each consecutive block of 16 numbers
    - Convert the number to hex representation
    """
    hex_values = list()
    for i in range(0, 256, 16):
        sub_list = hash_list[i:i+16]
        hex_value = reduce(lambda x, y: x ^ y, sub_list)
        hex_values.append('{:02x}'.format(hex_value))

    return ''.join(hex_values)

def main():
    """Knot Hash

    Hash Type
    multi
    - Reverse the order of that length of elements in the list, starting with the
      element at the current position.
    - Move the current position forward by that length plus the skip size.
    - Increase the skip size by one.
    - Multiplying the first two numbers in the list.

    hex
    - Convert characters to bytes using their ASCII codes
    - Add the following lengths to the end of the sequence: 17, 31, 73, 47, 23
    - Run a total of 64 rounds, using the same length sequence in each round,
      start with the previous round's current position and skip size
    - Use numeric bitwise XOR to combine each consecutive block of 16 numbers
    - Cover to number to 2 digit hex representation.
    """
    parser = argparse.ArgumentParser(description='Knot Hash')
    parser.add_argument('-i', dest='file_path', help='path to input data file',
                        required=True)
    parser.add_argument('-t', dest='type', choices=['multi', 'hex'],
                        default='multi', help='hash type')

    args = parser.parse_args()
    with open(args.file_path, 'r') as file:
        input_data = file.readlines()

    if args.type == 'multi':
        data = [int(i) for j in input_data for i in j.split(",")]
        value = cal_hash(data, multiplication_hash_fun)
    else:
        data = [ord(character) for line in input_data for character in line] + [17, 31, 73, 47, 23]
        value = cal_hash(data, hex_hash_fun, 64)

    print('Hash value is: %s' % value)

if __name__ == '__main__':
    main()
