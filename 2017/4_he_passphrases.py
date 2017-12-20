#!/usr/bin/env python3

import argparse

def count_passphrases(data, validator):
    """Count the number of passphrase that is valid by the validator."""
    count = 0
    for d_values in data:
        if validator(d_values):
            count += 1
    return count

def passphrase_no_duplicate(passphrase):
    """Check a passphrase is valid if there are no duplicate words."""
    words_set = set()
    for word in passphrase.split(' '):
        if word in words_set:
            return False
        words_set.add(word)
    return True

def passphrase_no_anagrams(passphrase):
    """Check a passphrase is valid if there are no words anagrams to each other."""
    words_set = set()
    for word in passphrase.split(' '):
        s_word = ''.join(sorted(word))
        if s_word in words_set:
            return False
        words_set.add(s_word)
    return True

def main():
    """High-Entropy Passphrases

    A valid passphrase
    - must contain no duplicate words
    or
    - contain no two words that are anagrams of each other - that is,
    a passphrase is invalid if any word's letters can be rearranged to form
    any other word in the passphrase.
    """
    parser = argparse.ArgumentParser(description="High-Entropy Passphrases")
    parser.add_argument('-i', dest='file_path', help='path to input data file',
                        required=True)
    parser.add_argument('-t', dest='type', choices=['nd', 'na'], default='nd',
                        help='validation type, nd for no duplication, na for no anagrams')

    args = parser.parse_args()

    with open(args.file_path, 'r') as file:
        input_data = file.read().splitlines()

    if args.type == 'na':
        validator = passphrase_no_anagrams
    else:
        validator = passphrase_no_duplicate

    count = count_passphrases(input_data, validator)
    print(count)

if __name__ == '__main__':
    main()
