#!/usr/bin/env python3

import argparse

def make_recipes(num, stopper):
    recipes = '37'
    elf1 = 0
    elf2 = 1
    while True:
        combined_recipes = int(recipes[elf1]) + int(recipes[elf2])
        recipes += str(combined_recipes)
        elf1 = (int(recipes[elf1]) + 1 + elf1) % len(recipes)
        elf2 = (int(recipes[elf2]) + 1 + elf2) % len(recipes)
        sv = stopper(recipes, num)
        if sv:
            return sv

def next_x_recipes_after(recipes, num):
    if len(recipes) > int(num) + 10:
        return recipes[int(num):int(num)+10]

def num_of_recipes_made_for(recipes, num):
    if num in recipes[-len(num)-1:]:
        return recipes.index(num)

def main():
    """
    The Elves are trying to come up with the ultimate hot chocolate recipe;
    they're even maintaining a scoreboard which tracks the quality score (0-9) of each recipe.

    Only two recipes are on the board: the first recipe got a score of 3, the
    second, 7. Each of the two Elves has a current recipe: the first Elf starts
    with the first recipe, and the second Elf starts with the second recipe.

    To create new recipes, the two Elves combine their current recipes. This
    creates new recipes from the digits of the sum of the current recipes' scores.
    With the current recipes' scores of 3 and 7, their sum is 10, and so two new
    recipes would be created: the first with score 1 and the second with score 0.
    If the current recipes' scores were 2 and 3, the sum, 5, would only create one
    recipe (with a score of 5) with its single digit.

    The new recipes are added to the end of the scoreboard in the order they are
    created. So, after the first round, the scoreboard is 3, 7, 1, 0.

    After all new recipes are added to the scoreboard, each Elf picks a new current
    recipe. To do this, the Elf steps forward through the scoreboard a number of
    recipes equal to 1 plus the score of their current recipe. So, after the first
    round, the first Elf moves forward 1 + 3 = 4 times, while the second Elf moves
    forward 1 + 7 = 8 times. If they run out of recipes, they loop back around to
    the beginning. After the first round, both Elves happen to loop around until
    they land on the same recipe that they had in the beginning; in general, they
    will move to different recipes.
    """
    parser = argparse.ArgumentParser(description='Chocolate Charts')
    parser.add_argument('-n', dest='num', help='number of recipes make',
                        required=True)

    args = parser.parse_args()
    scores = make_recipes(args.num, next_x_recipes_after)
    print('After %s recipes, next 10 score is: %s' % (args.num, scores))

    num_recipes = make_recipes(args.num, num_of_recipes_made_for)
    print('After recipes %s appear, number of recipes created: %s' % (args.num, num_recipes))

if __name__ == '__main__':
    main()
