from aocd import get_data

s = get_data(day=11,year=2015)

#first part
def increment(current):
    i = len(current)-1
    while i>=0 and current[i] == "z": i -= 1
    next_word = current[:i]
    if i>=0:
        next_word += chr(ord(current[i])+1)
    next_word += "a"*(len(current)-i-1)
    return next_word

def is_right(current):
    has_no_forbidden = not any(c in current for c in "iol")
    if not has_no_forbidden:
        return False
    has_increasing_three = any("".join(map(chr,range(o,o+3))) in current for o in range(ord("a"),ord("z")-1))
    has_two_double_letters = sum(current.count(chr(o)*2) for o in range(ord("a"),ord("z")+1)) >= 2
    return has_increasing_three and has_no_forbidden and has_two_double_letters

current = s
while not is_right(current):
    current = increment(current)
print(current)

#second part
current = increment(current)
while not is_right(current):
    current = increment(current)
print(current)