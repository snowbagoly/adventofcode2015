from aocd import get_data
import re

number_regex = re.compile("-?\\d+")

s = get_data(day=13,year=2015)

#first part
def sit(sitting_so_far,first,last,happiness_so_far): #from day 9
    people_left = people-sitting_so_far
    if people_left:
        return max(sit(sitting_so_far | {p}, first, p, happiness_so_far+changes[(last,p)]+changes[(p,last)]) for p in people_left)
    else:
        return happiness_so_far+changes[(last,first)]+changes[(first,last)]

people = set()
changes = {}
for line in s.replace("gain ","").replace("lose ","-").split("\n"):
    splitted = line.split(" ")
    person1,change,person2 = splitted[0],int(splitted[2]),splitted[-1][:-1]
    changes[(person1,person2)] = change
    people.add(person1)
    people.add(person2)
one_person = next(iter(people))
print(sit({one_person},one_person,one_person,0))

#second part
people.add("me")
for p in people:
    changes[(p,"me")] = 0
    changes[("me",p)] = 0
print(sit({one_person},one_person,one_person,0))