#!/usr/bin/env python3

import argparse

class Power:
    def __init__(self, x, y, serial_number):
        self.serial_number = serial_number
        self.x = x
        self.y = y
        self.power = calculate_power(self.serial_number, self.x, self.y)
        # For caching
        self.previous_sqrt_power = None
        self.previous_col_power = None
        self.previous_row_power = None

    def get_power(self):
        if not self.power:
            self.power = calculate_power(self.serial_number, self.x, self.y)

        return self.power

    def get_previous_sqrt_power(self, grid, size):
        if not self.previous_sqrt_power:
            self.calculate_square_power(grid, size)

        return self.previous_sqrt_power

    def get_previous_col_power(self, grid, size):
        if not self.previous_col_power:
            self.calculate_col_power(grid, size)

        return self.previous_col_power

    def get_previous_row_power(self, grid, size):
        if not self.previous_row_power:
            self.calculate_row_power(grid, size)

        return self.previous_row_power

    def calculate_square_power(self, grid, size):
        power = 0
        for i in range(size):
            for j in range(size):
                power += grid.get_cell_powers(self.x + j, self.y + i).get_power()
        self.previous_sqrt_power = power

    def calculate_row_power(self, grid, size):
        power = 0
        for i in range(size):
            power += grid.get_cell_powers(self.x + i, self.y).get_power()
        self.previous_row_power = power

    def calculate_col_power(self, grid, size):
        power = 0
        for i in range(size):
            power += grid.get_cell_powers(self.x, self.y + i).get_power()
        self.previous_col_power = power

class PowerGird:
    def __init__(self, w, h, serial_number):
        self.data = [[Power(x+1, y+1, serial_number) for y in range(w)] for x in range(h)]

    def get_cell_powers(self, x, y):
        return self.data[x-1][y-1]

    def set_cell_powers(self, x, y, powers):
        self.data[x-1][y-1] = powers

def find_max_power_square(power_grid, size):
    max_power = 0
    max_power_index = None
    for x in range(1, 302 - size):
        for y in range(1, 302 - size):
            power = calculate_square_power(power_grid, x, y, size)
            if power > max_power:
                max_power = power
                max_power_index = (x, y)

    return (max_power_index, max_power)

def calculate_square_power(power_grid, x, y, size):
    power_cell = power_grid.get_cell_powers(x, y)

    if size == 1:
        power_cell.previous_col_power = power_cell.get_power()
        power_cell.previous_row_power = power_cell.get_power()
        power_cell.previous_sqrt_power = power_cell.get_power()
    else:
        conner_power = power_grid.get_cell_powers(x+size-1, y+size-1).get_power()
        sqrt_power = power_cell.get_previous_sqrt_power(power_grid, size - 1)

        col_cell = power_grid.get_cell_powers(x, y+size-1)
        row_power = col_cell.get_previous_row_power(power_grid, size - 1)

        row_cell = power_grid.get_cell_powers(x+size-1, y)
        col_power = row_cell.get_previous_col_power(power_grid, size - 1)

        power_cell.previous_col_power = int(power_cell.previous_col_power or 0) + col_cell.get_power()
        power_cell.previous_row_power = int(power_cell.previous_row_power or 0) + row_cell.get_power()

        power_cell.previous_sqrt_power = col_power + row_power + sqrt_power + conner_power

    return power_cell.previous_sqrt_power

def calculate_power(serial_number, x, y):
    rack_id = x + 10
    power_level = (rack_id * y + serial_number) * rack_id
    return (power_level // 100) % 10 - 5

def main():
    """
    You watch the Elves and their sleigh fade into the distance as they head toward the North Pole.
    Actually, you're the one fading. The falling sensation returns.

    The low fuel warning light is illuminated on your wrist-mounted device.
    Tapping it once causes it to project a hologram of the situation: a 300x300
    grid of fuel cells and their current power levels, some negative.
    You're not sure what negative power means in the context of time travel, but it can't be good.

    Each fuel cell has a coordinate ranging from 1 to 300 in both the X (horizontal)
    and Y (vertical) direction. In X,Y notation, the top-left cell is 1,1, and
    the top-right cell is 300,1.

    The interface lets you select any 3x3 square of fuel cells.
    To increase your chances of getting to your destination, you decide to
    choose the 3x3 square with the largest total power.

    The power level in a given fuel cell can be found through the following process:
        Find the fuel cell's rack ID, which is its X coordinate plus 10.
        Begin with a power level of the rack ID times the Y coordinate.
        Increase the power level by the value of the grid serial number (your puzzle input).
        Set the power level to itself multiplied by the rack ID.
        Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
        Subtract 5 from the power level.

    For example, to find the power level of the fuel cell at 3,5 in a grid with serial number 8:
        The rack ID is 3 + 10 = 13.
        The power level starts at 13 * 5 = 65.
        Adding the serial number produces 65 + 8 = 73.
        Multiplying by the rack ID produces 73 * 13 = 949.
        The hundreds digit of 949 is 9.
        Subtracting 5 produces 9 - 5 = 4.
        So, the power level of this fuel cell is 4.

    Find the Y x Y square which has the largest total power. The square must be
    entirely within the 300x300 grid. Identify this square using the X,Y c
    oordinate of its top-left fuel cell.
    For example:
        For grid serial number 18, the largest total 3x3 square has a top-left
        corner of 33,45 (with a total power of 29); these fuel cells appear
        in the middle of this 5x5 region:
            -2  -4  4   4   4
            -4  4   4   4  -5
            4   3   3   4  -4
            1   1   2   4  -3
            -1  0   2  -5  -2
    """
    parser = argparse.ArgumentParser(description='Chronal Charge')
    parser.add_argument('-n', dest='serial_number', help='serial number',
                        required=True)
    parser.add_argument('-s', dest='size', help='size',
                        required=False)
    parser.add_argument('-r', dest='range', help='range',
                        required=False)

    args = parser.parse_args()

    serial_number = int(args.serial_number)

    power_grid = PowerGird(300, 300, serial_number)

    if args.size:
        (index, power) = find_max_power_square(power_grid, int(args.size))
        print('Index: %s, Power: %s' % (index, power))

    if args.range:
        mpower = 0
        mindex = None
        mszie = None
        for i in range(1, int(args.range)+1):
            (index, power) = find_max_power_square(power_grid, i)
            if power > mpower:
                mpower = power
                mindex = index
                mszie = i
        print('Index: %s, Size: %s, Power: %s' % (mindex, mszie, mpower))

if __name__ == '__main__':
    main()
