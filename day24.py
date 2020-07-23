from aocd import get_data

raw_data = get_data(day=24,year=2015)
packages = list(map(int,raw_data.split("\n")))[::-1]

weight_sum = sum(packages)

def mul(items):
	result = 1
	for item in items:
		result *= item
	return result

def find_combinations(expected_weight):
	good_combinations = set()
	best_combination = None
	best_combination_length = len(packages)
	votma = set()
	q = [((),0,-1)]
	while q:
		items,summa,last_index = q.pop(0)
		if summa == expected_weight:
			if best_combination is None or len(items) < best_combination_length or len(items) == best_combination_length and mul(items) < mul(best_combination):
				best_combination_length = len(items)
				best_combination = items
			good_combinations.add(items)
		elif len(items) >= best_combination_length:
			continue
		else:
			for i in range(last_index+1, len(packages)):
				if items + (packages[i],) not in votma and summa+packages[i] <= expected_weight:
					q.append((items + (packages[i],),summa+packages[i],i))
					votma.add(items + (packages[i],))
	print(mul(best_combination))
find_combinations(weight_sum // 3)
find_combinations(weight_sum // 4)