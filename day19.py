from aocd import get_data
import re


test_data = """H => HO
O => OHO
e => HO
e => HH

HOHO""".split("\n")

raw_data = get_data(day=19,year=2015).split("\n")
molecule = raw_data[-1]


class Rule:
	def __init__(self, left, right):
		self.left = left
		self.right = tuple(right)
		self.right_as_string = "".join(right)

	def apply_every_possible_way(self, molecule):
		new_molecules = set()

		for i in range(len(molecule)-len(self.left)+1):
			if molecule[i:i+len(self.left)] == self.left:
				new_molecules.add(molecule[:i] + self.right_as_string + molecule[i+len(self.left):])
		return new_molecules
	def __repr__(self):
		return "<Rule '%s' => '%s'>" % (self.left, self.right_as_string)

def split_by_capital(w):
	return re.findall('[A-Z][^A-Z]*', w)

def parse_rule(line):
	left,right = line.split(" => ")
	right_splitted = split_by_capital(right)
	return Rule(left, right_splitted)

rules = [parse_rule(line) for line in raw_data[:-2]]
all_molecules_after_one_step = set()
for rule in rules:
	all_molecules_after_one_step.update(rule.apply_every_possible_way(molecule))
print(len(all_molecules_after_one_step))


# This is a CF language. We can track back how a word was generated using CYK.
# For CYK we need the normal form (A -> a or A -> BC), but now everything counts
# as a non-terminal, so we can go with the A->BC forms. (Quick check assured that
# we don't have A->B rules, so we don't have to care about unit rules)

# We don't need the actual path resolving, just the number of steps, so we can track the
# minimal number of steps until specific non-terminals (not counting the X-whatever ones)

def convert_to_chomsky_normal_form(rule, additional_non_terminal_index):
	if len(rule.right) > 2:
		first_rule = Rule(rule.left, [rule.right[0],"X%d" % additional_non_terminal_index])
		previous_rules = [Rule("X%d" % (additional_non_terminal_index + i - 1),[rule.right[i],"X%d" % (additional_non_terminal_index + i)]) \
		                        for i in range(1,len(rule.right)-2)]
		last_rule = Rule("X%d" % (additional_non_terminal_index + len(rule.right)-3),rule.right[-2:])
		return [first_rule] + previous_rules + [last_rule]
	else:
		return [rule]

def generate_all_possible_right_sides(pair):
	firsts,seconds = pair
	return [(f,s) for f in firsts for s in seconds]

def find_all_possible_left_sides(possible_combinations):
	""" This function is not so pretty currently :(
	What it does: checks which symbol pairs are actually valid right sides, and 
	finds the left side for those. Additionally it calculates the number of operations
	to achieve that left side as well: the non terminals added at the Chomsky normal form
	conversion are not counted. If we can get to the same non-terminal in less steps, we
	store that number instead. In the end a nasty conversion, because I stored the results
	in (symbol, number_of_operations) style. Probably would help if this was wrapped in a class. """
	global reverse_rule_map
	all_left_sides = {}
	for combination in possible_combinations:
		left_symbol, left_count = combination[0]
		right_symbol, right_count = combination[1]
		right_side = (left_symbol, right_symbol)
		if right_side in reverse_rule_map:
			for left_side in reverse_rule_map[right_side]:
				current_count = left_count+right_count+(left_side[0] != "X")
				if left_side not in all_left_sides or all_left_sides[left_side] > current_count:
					all_left_sides[left_side] = current_count

	return [(key, all_left_sides[key]) for key in all_left_sides]

def create_reverse_rule_map(rules):
	reverse_rule_map = {}
	for rule in rules:
		if rule.right not in reverse_rule_map:
			reverse_rule_map[rule.right] = set()
		reverse_rule_map[rule.right].add(rule.left)
	return reverse_rule_map

def calculate_next_cell_in_row(row,cells):
	if row >= len(cells):
		cells.append([])
	col = len(cells[row])


	# Example zips for calculations
	# cells[0][j] cells[0][j+1]

	# cells[0][j] cells[1][j+1]
	# cells[1][j] cells[0][j+2]

	# cells[0][j] cells[2][j+1]
	# cells[1][j] cells[1][j+2]
	# cells[2][j] cells[0][j+3]

	possible_combinations = zip([cells[k][col] for k in range(row)], [cells[row-(k+1)][col+(k+1)] for k in range(row)])
	possible_right_sides = []
	for pair in possible_combinations:
		possible_right_sides += generate_all_possible_right_sides(pair)
	cells[row].append(find_all_possible_left_sides(possible_right_sides))

rules_in_normal_form = []

additional_non_terminal_index = 0
for rule in rules:
	converted_rules = convert_to_chomsky_normal_form(rule, additional_non_terminal_index)
	if len(converted_rules) > 1:
		additional_non_terminal_index += len(converted_rules)-1
	rules_in_normal_form += converted_rules

reverse_rule_map = create_reverse_rule_map(rules_in_normal_form)

molecule_splitted = [[(c,0)] for c in split_by_capital(molecule)]

cells = [molecule_splitted]
for k in range(1,len(molecule_splitted)):
	for i in range(len(molecule_splitted)-k):
		calculate_next_cell_in_row(k,cells)
print(cells[-1][0])