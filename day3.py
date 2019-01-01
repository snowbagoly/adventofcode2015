from aocd import get_data

s = get_data(day=3,year=2015)

#first part
def go(direction,x,y):
    if direction == "^":
        return x-1,y
    elif direction == "v":
        return x+1,y
    elif direction == ">":
        return x,y+1
    elif direction == "<":
        return x,y-1
def deliver(path):
    visited = set()
    current = (0,0)
    visited.add(current)
    for direction in path:
        current = go(direction,*current)
        visited.add(current)
    return visited

visited = deliver(s)
print(len(visited))

#second part
santa_visited = deliver(s[::2])
robosanta_visited = deliver(s[1::2])
print(len(santa_visited | robosanta_visited))