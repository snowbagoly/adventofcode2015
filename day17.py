from aocd import get_data

TARGET_SUM = 150

*containers, = map(int,get_data(day=17,year=2015).split("\n"))

def add_container(containers, indexes_used, sum_so_far, index_to_add):
	new_sum_so_far = sum_so_far+containers[index_to_add]
	new_indexes_used = indexes_used+(index_to_add,)
	if new_sum_so_far == TARGET_SUM:
		return [new_indexes_used]
	elif new_sum_so_far > TARGET_SUM:
		return []
	else:
		# If we still have free space, trying to add all following containers (might worth to order the
		# container sizes desc, so we could find with a binary search where to start the adding, but we don't really
		# have that many elements)
		return [solution for i in range(index_to_add+1, len(containers)) \
		        for solution in add_container(containers, new_indexes_used, new_sum_so_far, i)]

solutions = [solution for i in range(len(containers)) \
	         for solution in add_container(containers, (), 0, i)]
print(len(solutions))

min_solution_length = min(map(len, solutions))
solutions_with_min_length = sum(len(solution) == min_solution_length for solution in solutions)
print(solutions_with_min_length)