#!/usr/bin/env python3

import argparse

def reallocation(banks):
    """Reallocate the banks until a patten seen.

    Method return the cycles need to get to a seen patten, and the cycles to the
    previous seen patten.
    """
    reallocation_map = {}
    cycle = 0
    while banks_signature(banks) not in reallocation_map:
        reallocation_map[banks_signature(banks)] = cycle
        banks = redistribution_banks(banks)
        cycle += 1
    return cycle, cycle - reallocation_map[banks_signature(banks)]

def banks_signature(banks):
    """Generate a signature for current banks"""
    return ''.join(str(bank) for bank in banks)

def redistribution_banks(banks):
    """Redistrubute the banks"""
    b_num, b_value = max_bank(banks)
    banks_count = len(banks)

    banks[b_num] = 0
    while b_value > 0:
        b_num = (b_num + 1) % banks_count
        banks[b_num] += 1
        b_value -= 1

    return banks

def max_bank(banks):
    """Find the max banks num and value"""
    bank_val = max(banks)
    bank_num = banks.index(bank_val)
    return bank_num, bank_val

def main():
    """Memory Reallocation

    The reallocation routine operates in cycles.
    In each cycle, it finds the memory bank with the most blocks
    (ties won by the lowest-numbered memory bank) and redistributes those blocks
    among the banks. To do this, it removes all of the blocks from the selected bank,
    then moves to the next (by index) memory bank and inserts one of the blocks.
    It continues doing this until it runs out of blocks; if it reaches the last
    memory bank, it wraps around to the first one.

    It stop when produced a pattern has been seen before.
    """
    parser = argparse.ArgumentParser(description='Memory Reallocation')
    parser.add_argument('-i', dest='file_path', help='path to input data file', required=True)

    args = parser.parse_args()
    with open(args.file_path, 'r') as file:
        input_data = [int(val) for val in file.read().split('\t')]

    cycles, cycles_to_previous = reallocation(input_data)
    print(cycles)
    print(cycles_to_previous)

if __name__ == '__main__':
    main()
