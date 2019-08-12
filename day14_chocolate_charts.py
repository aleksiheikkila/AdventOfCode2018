"""
Advent of code, 2018
Day 14: Chocolate charts
"""
from typing import List

# puzzle input:
INPUT = 554401

class Recipe():
    def __init__(self, score):
        self.score = score


class Recipes():
    def __init__(self, recipes: List[Recipe]):
        self.recipes = recipes  # this is also the scoreboard
        self.current_recipes = [(i, i, recipe.score) for i, recipe in enumerate(self.recipes)]  # elf id, recipe index, score
        print(self.current_recipes)


    def create_recipes(self, max_num_of_recipes: int, return_last_n: int = 10) -> str:
        """Create given amount of recipes, return the scores of the last n recipes as a concatenated string
        
        Arguments:
            max_num_of_recipes {int} -- [loop until this many recipes has been created]
        
        Keyword Arguments:
            return_last_n {int} -- [how many scores to return] (default: {10})
        
        Returns:
            str -- [the return_last_n nbr of recipe scores joined as a string]
        """

        while True:
            rec_sum = sum(score for _, __, score in self.current_recipes)
            num_recipes_to_add = min(max_num_of_recipes - len(self.recipes), len(str(rec_sum)))
            for digit in str(rec_sum)[:num_recipes_to_add]:
                self.recipes.append(Recipe(int(digit)))

            # then update the indexes
            for elf_id, rec_idx, score in self.current_recipes[:num_recipes_to_add+1]:   # slicing creates a new copy
                steps_to_take = 1 + score
                num_recipes = len(self.recipes)
                new_rec_idx = (rec_idx + steps_to_take) % num_recipes
                self.current_recipes[elf_id] = (elf_id, new_rec_idx, self.recipes[new_rec_idx].score)
            
            if len(self.recipes) >= max_num_of_recipes:
                last_n = "".join([str(recipe.score) for recipe in r.recipes[-return_last_n:]])
                return last_n


    def get_num_recipes_before(self, before_recipe_string: str) -> int:
        """Calc how many recipes are generated before given recipe score string is met
        
        Arguments:
            before_recipe_string {str} -- [create new recipes until this string of successive recipe scores is encountered]
        
        Returns:
            int -- [how many recipes there were before the recipe string was encountered for the first time]
        """

        recipe_str_len = len(before_recipe_string)
        
        while True:
            rec_sum = sum(score for _, __, score in self.current_recipes)
            for digit in str(rec_sum):
                self.recipes.append(Recipe(int(digit)))
                if "".join([str(recipe.score) for recipe in self.recipes[-recipe_str_len:]]) == before_recipe_string:
                    return len(self.recipes) - recipe_str_len


            # then update the indexes
            for elf_id, rec_idx, score in self.current_recipes[:]:   # slicing creates a new copy
                steps_to_take = 1 + score
                num_recipes = len(self.recipes)
                new_rec_idx = (rec_idx + steps_to_take) % num_recipes
                self.current_recipes[elf_id] = (elf_id, new_rec_idx, self.recipes[new_rec_idx].score)



# Part A:
# What are the scores of the ten recipes immediately after the number of recipes in your puzzle input?

# Unit tests
r = Recipes(recipes=[Recipe(3), Recipe(7)])
assert r.create_recipes(19) == "5158916779"

r = Recipes(recipes=[Recipe(3), Recipe(7)])
assert r.create_recipes(15) == "0124515891"

r = Recipes(recipes=[Recipe(3), Recipe(7)])
assert r.create_recipes(28) == "9251071085"

r = Recipes(recipes=[Recipe(3), Recipe(7)])
assert r.create_recipes(2028) == "5941429882"

# Then with the prob input:
r = Recipes(recipes=[Recipe(3), Recipe(7)])
print(r.create_recipes(INPUT+10))
# Answer is 3610281143


################
# Part B

# As it turns out, you got the Elves' plan backwards. 
# #They actually want to know how many recipes appear on the scoreboard to the left of the first recipes 
# # whose scores are the digits from your puzzle input.

# unit tests
r = Recipes(recipes=[Recipe(3), Recipe(7)])
assert r.get_num_recipes_before("51589") == 9

r = Recipes(recipes=[Recipe(3), Recipe(7)])
assert r.get_num_recipes_before("01245") == 5

r = Recipes(recipes=[Recipe(3), Recipe(7)])
assert r.get_num_recipes_before("92510") == 18

r = Recipes(recipes=[Recipe(3), Recipe(7)])
assert r.get_num_recipes_before("59414") == 2018

# then with actual input
r = Recipes(recipes=[Recipe(3), Recipe(7)])
print(r.get_num_recipes_before(str(INPUT)))
# Right answer is: 20211326