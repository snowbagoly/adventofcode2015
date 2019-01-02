from aocd import get_data

s = get_data(day=8,year=2015)

#first part
print(sum(len(line)-len(eval(line)) for line in s.split("\n")))

#second part
def extra(line):
	return line.count("\\") + line.count("\"") + 2
print(sum(extra(line) for line in s.split("\n")))