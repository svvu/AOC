#!/usr/bin/env python3

import argparse
import operator as op

REGISTERS = {}

def register_value(register):
    """Get the register value by name

    If register not found, 0 value will be returned
    """
    if register in REGISTERS:
        return REGISTERS[register]
    else:
        return 0

class Condition:
    """Condition is condition checking for an instruction."""
    lookup = {'<': op.lt, '<=': op.le, '==': op.eq, '>=': op.ge, '>': op.gt, '!=': op.ne}

    def __init__(self, clause, register, operator, value):
        self.clause = clause
        self.register = register
        self.operator = operator
        self.value = int(value)

    def satisfy(self):
        """Check whether or not the condition pass or not"""
        rvalue = register_value(self.register)
        return Condition.lookup[self.operator](rvalue, self.value)

class Instruction:
    """Instruction is an operation to the register."""
    def __init__(self, register, action, value, condition):
        self.register = register
        self.action = action
        self.value = int(value)
        self.condition = condition

    def execute(self):
        """Execute the operation on the register if condition meet."""
        rvalue = register_value(self.register)
        if self.condition.satisfy():
            if self.action == 'inc':
                rvalue += self.value
            else:
                rvalue -= self.value

        return rvalue

def parse_and_exec_instructions(instructions):
    """Parse the instruction string and exec the instructions."""
    max_helded = 0
    for instruction_str in instructions:
        components = instruction_str.split(' ')

        condition = Condition(*components[3:7])
        instruction = Instruction(*components[0:3], condition)

        value = instruction.execute()
        max_helded = value if value > max_helded else max_helded
        REGISTERS[instruction.register] = value

    return max_helded

def main():
    """Registers

    Each instruction consists of several parts: the register to modify, whether
    to increase or decrease that register's value, the amount by which to
    increase or decrease it, and a condition. If the condition fails, skip the
    instruction without modifying the register. The registers all start at 0.
    """
    parser = argparse.ArgumentParser(description="Registers")
    parser.add_argument('-i', dest='file_path', help='path to input data file',
                        required=True)

    args = parser.parse_args()
    with open(args.file_path, 'r') as file:
        input_data = file.readlines()

    max_helded = parse_and_exec_instructions(input_data)
    print("Max register value: %s" % max(REGISTERS.values()))
    print("Max value: %s" % max_helded)

if __name__ == '__main__':
    main()
