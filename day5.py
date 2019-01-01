from aocd import get_data

s = get_data(day=5,year=2015)

#first part
def is_nice(line):
    at_least_three_vowels = sum(c in "aeiou" for c in line) >= 3
    twice_in_a_row = any(line[i] == line[i+1] for i in range(len(line)-1))
    no_forbidden = all(f not in line for f in ["ab","cd","pq","xy"])
    return at_least_three_vowels and twice_in_a_row and no_forbidden
print(sum(map(is_nice,s.split("\n"))))

#second part
def is_not_ridiculously_nice(line):
    pair_appears_twice = any(line[i]+line[i+1] in line[i+2:] for i in range(len(line)-2))
    repeating_in_one_dist = any(line[i] == line[i+2] for i in range(len(line)-2))
    return pair_appears_twice and repeating_in_one_dist
print(sum(map(is_not_ridiculously_nice,s.split("\n"))))