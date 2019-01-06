from aocd import get_data

s = get_data(day=10,year=2015)

#first part
def iterate(current):
    next_word = []
    last = current[0]
    counter = 1
    for c in current[1:]:
        if c == last:
            counter += 1
        else:
            next_word.append(str(counter))
            next_word.append(last)
            counter = 1
        last = c
    next_word.append(str(counter))
    next_word.append(last)
    return "".join(next_word)

for i in range(40):
    s = iterate(s)
print(len(s))

#second part
for i in range(10):
    s = iterate(s)
    print(i,len(s))
print(len(s))