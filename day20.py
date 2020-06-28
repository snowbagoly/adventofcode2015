from aocd import get_data

raw_data = get_data(day=20,year=2015)

# The task basically is to find the sum of the divisors of a number. But still it can be
# much faster to add up starting by 2 or 3 to every nth number up to a threshold, as
# looking for divisors one by one is usually slower (see sieve of Eratosthenes).

# The number is ten times of the sum of its divisors, so we can start dividing by 10.
# It's obvious that the number has 1 and itself as divisors.

# We still have to make sure that we find the lowest number, so at first approach we iterate
# through all numbers up to max_number, just to make it sure (probably it's a bit too much,
# but we can care about optimization later).

expected_number = int(raw_data)
max_number = expected_number//10-1

def find_lowest_number(max_number, expected_number):
	for i in range(2,max_number+1):
		for j in range(i*2,max_number+1,i):
			divisor_sums[j] += i
			if divisor_sums[j] >= expected_number // 10: # Restricting the scope
				max_number = j

divisor_sums = { i: i+1 for i in range(2,max_number+1)}
find_lowest_number(max_number, expected_number)

for i in range(2,max_number+1):
	if divisor_sums[i] >= expected_number//10:
		print(i)
		break


def find_lowest_number_with_lazy_elves(max_number, expected_number):
	for i in range(2,max_number+1):
		for j in range(i*2,min(i*50,max_number)+1,i):
			divisor_sums[j] += i
			if divisor_sums[j] >= expected_number / 11: # Restricting the scope
				max_number = j
max_number = expected_number//11-1
divisor_sums = { i: i for i in range(2,max_number+1)}
find_lowest_number_with_lazy_elves(max_number, expected_number)
for i in range(2,max_number+1):
	if divisor_sums[i] >= expected_number/11:
		print(i)
		break