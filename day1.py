from aocd import get_data

s = get_data(day=1,year=2015)

#first part
print(s.count("(")-s.count(")"))

#second part
i = 0
floor = 0
for c in s:
    floor += [-1,1][c == "("]
    i += 1
    if floor < 0:
        break
print(i)