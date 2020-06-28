from aocd import get_data
import re
import math

item_pattern = re.compile(r"(?P<item_name>\S+\s?\S+?)\D+(?P<cost>\d+)\D+(?P<damage>\d+)\D+(?P<armor>\d+)")
boss_pattern = re.compile(r"Hit Points: (?P<hit_points>\d+)\nDamage: (?P<damage>\d+)\nArmor: (?P<armor>\d+)")
raw_data = get_data(day=21,year=2015)

class Player:
	def __init__(self, id, hit_points, damage, armor):
		self.id = id
		self.hit_points = hit_points
		self.damage = damage
		self.armor = armor
	def hit(self, damage):
		self.hit_points -= max(1, damage-self.armor)
	def __repr__(self):
		return "<Player '%s' (HP: %d, D: %d, A: %d)>" % (self.id, self.hit_points, self.damage, self.armor)

class Item:
	def __init__(self, line):
		matches = item_pattern.match(line)
		self.item_name = matches.group("item_name")
		self.cost,self.damage,self.armor = [int(matches.group(label)) for label in ["cost", "damage", "armor"]]
	def __repr__(self):
		return "<Item '%s' (Cost: %d, Damage: %d, Armor: %d)>" % (self.item_name, self.cost, self.damage, self.armor)

matches = boss_pattern.match(raw_data)
boss = Player("Boss", *[int(matches.group(label)) for label in ["hit_points", "damage", "armor"]])

shop = """Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3"""

weapons,armors,rings = map(lambda category: [Item(line) for line in category.split("\n")[1:]], shop.split("\n\n"))
player = Player("Me", 100, 0, 0)
players = [player, boss]

def would_i_win(player, boss, items):
	my_damage = sum(item.damage for item in items)
	my_armor = sum(item.armor for item in items)
	boss_damage_to_me = max(1,boss.damage - my_armor)
	turns_to_die_for_me = math.ceil(player.hit_points / boss_damage_to_me)
	my_damage_to_boss = max(1,my_damage - boss.armor)
	turns_to_die_for_boss = math.ceil(boss.hit_points / my_damage_to_boss)
	return turns_to_die_for_boss <= turns_to_die_for_me

def update_edge_value_if_better(player, boss, items, extreme_so_far, value_comparer_func, should_i_lose):
	if should_i_lose ^ would_i_win(player, boss, items):
		item_cost = sum(item.cost for item in items)
		if extreme_so_far is None or value_comparer_func(item_cost,extreme_so_far):
			return item_cost
	return extreme_so_far

# This function tries every combination of items and calculates their costs if they are appropriate.
# Probably there is a better approach (less things should be tried out as some of them are already too
# expensive, and the combinations could have been calculated in a prettier way)
def find_extreme_value(value_comparer_func, should_i_lose):
	extreme_value = None

	for weapon in weapons:
		# Without armor and rings
		extreme_value = update_edge_value_if_better(player, boss, [weapon], extreme_value, value_comparer_func, should_i_lose)

		for armor in armors:
			# With armor, without rings
			extreme_value = update_edge_value_if_better(player, boss, [weapon, armor], extreme_value, value_comparer_func, should_i_lose)

			for ring_i in range(len(rings)):
				# With armor and one ring
				extreme_value = update_edge_value_if_better(player, boss, [weapon, armor, rings[ring_i]], extreme_value, value_comparer_func, should_i_lose)
				for ring_j in range(ring_i+1, len(rings)):
					# With armor and two rings
					extreme_value = update_edge_value_if_better(player, boss, [weapon, armor, rings[ring_i], rings[ring_j]], extreme_value, value_comparer_func, should_i_lose)
		# Without armor, just rings
		for ring_i in range(len(rings)):
			# With one ring
			extreme_value = update_edge_value_if_better(player, boss, [weapon, rings[ring_i]], extreme_value, value_comparer_func, should_i_lose)
			for ring_j in range(ring_i+1, len(rings)):
				# With two rings
				extreme_value = update_edge_value_if_better(player, boss, [weapon, rings[ring_i], rings[ring_j]], extreme_value, value_comparer_func, should_i_lose)
	return extreme_value

print(find_extreme_value(lambda a,b: a < b, False))
print(find_extreme_value(lambda a,b: a > b, True))