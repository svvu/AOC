#!/usr/bin/env python3

import argparse
import math

DIRECTION_VALUE = {
    "down": 0,
    "left": 1,
    "up": 2,
    "right": 3
}

CACHED_STORE_VALUE = {}

def calculate_layer_num(num):
    """Calculate which layer the number is in.

    Layer start at 0, which means the center is layer 0.
    The max value in a layer is: (2l + 1) ** 2
    The min value in a layer is: (2(l - 1) + 1) ** 2 + 1 => (2l - 1) ** 2 + 1
    which is the max value of previous layer + 1

    The method will use the min value formula to calculate the layer.
    If input number is greater than min, but less than the min of next layer,
    the result will be the a decimal number greater than current layer but less than next layer.
    Floot of the result will be the layer the number should be in.
    """
    return math.floor((math.sqrt(num - 1) + 1) / 2)

def max_value_of_layer(layer):
    """Calculate the max value of a layer"""
    return int(math.pow(2 * layer + 1, 2))

def calculate_edge_value_from_center(layer, direct):
    """Calculate the edge value for layer from center (1).

    This is same as the value N (N is layer) steps from center in left/right/up/down direction.
    """
    return max_value_of_layer(layer) - (direct * 2 + 1) * layer

def direction_from_center(layer, num):
    """Find which side of the num is in relative to center"""
    return int((max_value_of_layer(layer) - num) / (2 * layer))

def steps_from_axis(layer, num):
    """Calculate the min steps need to move away from axix to num's position."""

    side = direction_from_center(layer, num)

    return abs(num - calculate_edge_value_from_center(layer, side))

def calculate_steps_from_center(num):
    """Calculate the min step need go from 1 to any number.

    Ex:
    37  36  35  34  33  32  31
    38  17  16  15  14  13  30
    39  18   5   4   3  12  29
    40  19   6   1   2  11  28
    41  20   7   8   9  10  27
    42  21  22  23  24  25  26
    43  44  45  46  47  48  49

    The max value in a layer is: (2l + 1) ** 2
    left edge axis value = max_value - 7l, ex: 2
    top edge axis value = max_value - 5l, ex: 4
    right edge axis value = max_value - 3l, ex: 6
    bottom edge axis value = max_value - 1l, ex: 8

    If a number is in Layer N, then it must take X step from 1 to the edge.
    Then take Y step away from the axis.
    Ex: 18 in layer 2, it takes 2 step to walk from 1 to edge 19, and 1 step
    away from 19.
    """
    if num == 1:
        return 0

    layer = calculate_layer_num(num)
    min_axis_step = steps_from_axis(layer, num)

    return layer + min_axis_step

def get_adjacent_values(layer, num):
    """Get a list of values adjacent to num"""
    if layer == 0:
        return []

    side = direction_from_center(layer, num)
    steps = steps_from_axis(layer, num)
    step_direction = 1 if num - calculate_edge_value_from_center(layer, side) >= 0 else -1

    n_steps = [
        steps * step_direction,
        steps * step_direction + 1,
        steps * step_direction - 1
    ]

    adj_values = set([num - 1])
    p_layer = layer - 1
    for n_step in n_steps:
        # Use bigger value as axis value and smaller value to move away from the axis.
        # Moving left by 3 and up by 4 is same as move up 4 first, then left by 3.
        # But by moving along the axis first will calculate the correct value at the
        # location, because if move along the axis by smaller value and then away from axis
        # will move out of the current square.
        if p_layer > abs(n_step):
            x_value, y_value = p_layer, n_step
            n_side = side
        elif p_layer == abs(n_step) and side != DIRECTION_VALUE['right']:
            # If its the conner case, and its not on the right side, do it normally,
            # Otherwise swap the value because the bottom right value will be cycle back to max.
            # If go right first, it will be at smaller value, and then go down it will not
            # cycle back to max.
            # So it will down first, and then right to increase to max.
            x_value, y_value = p_layer, n_step
            n_side = side
        elif steps == 0 and n_step < 0:
            # If its on the axis, and step backward, should swap and keep the direction.
            # This is a special case.
            x_value, y_value = abs(n_step), p_layer
            n_side = side + step_direction
        else:
            # If step away from axis is lager than the axis value, swap it.
            x_value, y_value = abs(n_step), p_layer * (-step_direction)
            n_side = side - step_direction

        # If side out of range, circle back
        if n_side < 0:
            n_side = 3
        elif n_side > 3:
            n_side = 0

        val = calculate_edge_value_from_center(x_value, n_side) + y_value
        if val < num:
            adj_values.add(val)

    return adj_values

def calculate_value_stored(num):
    """Calculate the value store in num square."""
    if num <= 0:
        return 0

    if num == 1 or num == 2:
        return 1

    if num in CACHED_STORE_VALUE:
        return CACHED_STORE_VALUE[num]

    for n_value in range(3, num+1):
        layer = calculate_layer_num(n_value)

        adj_values = get_adjacent_values(layer, n_value)
        store_value = 0
        for adj_value in adj_values:
            store_value += calculate_value_stored(adj_value)

        CACHED_STORE_VALUE[n_value] = store_value

        if store_value > num:
            return store_value

    return CACHED_STORE_VALUE[num]

def main():
    """Spiral Memory.

    Each square on the grid is allocated in a spiral pattern starting at a
    location marked 1 and then counting up while spiraling outward.
    Ex:
    5   4   3
    6   1   2
    7   8->...
    Requested data must be carried back to square 1 (the location of the only
    access port for this memory system) by programs that can only move up, down,
    left, or right. They always take the shortest path: the Manhattan Distance
    between the location of the data and square 1.

    The grid and then store the value 1 in square 1. Then, in the same allocation
    order as shown above, they store the sum of the values in all adjacent squares,
    including diagonals.
    Ex:
    147  142  133  122   59
    304    5    4    2   57
    330   10    1    1   54
    351   11   23   25   26
    362  747  806--->   ...
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', dest='num', type=int, required=True, help='input number')
    parser.add_argument('-t', dest='type', default='step', choices=['step', 'value'],
                        help='value type to calculate, step from center for input or first '
                             'value store greater than input')

    args = parser.parse_args()

    if args.type == 'step':
        print(calculate_steps_from_center(args.num))
    else:
        print(calculate_value_stored(args.num))

if __name__ == '__main__':
    main()
