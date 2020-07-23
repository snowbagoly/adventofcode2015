from aocd import get_data
import re

BOWL_SIZE = 100
ingredient_regex = re.compile(r"(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)")

raw_data = get_data(day=15,year=2015)

class Ingredient:
    def __init__(self, name, capacity, durability, flavor, texture, calories):
        self.name = name
        self.capacity = int(capacity)
        self.durability = int(durability)
        self.flavor = int(flavor)
        self.texture = int(texture)
        self.calories = int(calories)

def mul(items):
    result = 1
    for item in items:
        result *= item
    return result

def calculate_score_and_calories(ingredients, separators):
    mix = Ingredient("Mixture", 0, 0, 0, 0, 0)
    separators = (0,) + separators + (100,)
    for i in range(len(separators)-1):
        amount = separators[i+1]-separators[i]
        mix.capacity += ingredients[i].capacity*amount
        mix.durability += ingredients[i].durability*amount
        mix.flavor += ingredients[i].flavor*amount
        mix.texture += ingredients[i].texture*amount
        mix.calories += ingredients[i].calories*amount
    return (mul(map(lambda x: max(0, x), [mix.capacity, mix.durability, mix.flavor, mix.texture])), mix.calories)
    

def parse_ingredient(line):
    return Ingredient(*ingredient_regex.match(line).group(*range(1,7)))
ingredients = list(map(parse_ingredient, raw_data.split("\n")))

# We have to share 100 teaspoons between the ingredients:
# "shifting" the amounts in the list |---|------||-----|
# Have n-1 "separators" to shift: 100c(n-1) variations > nope, we can choose the same, it's something like n+k+1 c n+k
def add_ingredient(pos, prev_combination):
    global all_combinations
    current_combination = tuple(prev_combination[:pos]) + (prev_combination[pos] + 1,) + tuple(prev_combination[pos+1:])
    all_combinations.add(current_combination)
    for i in range(pos):
        add_ingredient(i, current_combination)
    if pos == len(current_combination)-1 and current_combination[pos] < BOWL_SIZE \
        or pos < len(current_combination)-1 and current_combination[pos] < current_combination[pos+1]:
        add_ingredient(pos, current_combination)

starting_separators = (0,)*(len(ingredients)-1)
all_combinations = { starting_separators }
add_ingredient(len(ingredients)-2, starting_separators)

cookies = {calculate_score_and_calories(ingredients, combination) for combination in all_combinations}
print(max(cookies, key=lambda c: c[0])[0])
print(max(filter(lambda c: c[1] == 500, cookies), key=lambda c: c[0])[0])