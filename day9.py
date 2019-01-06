from aocd import get_data

s = get_data(day=9,year=2015)

#first part
def travel(traveled_so_far,last_city,dist_so_far,selector):
    cities_left = cities-traveled_so_far
    if cities_left:
        return selector(travel(traveled_so_far | {c}, c, dist_so_far+weights[(last_city,c)],selector) for c in cities_left)
    else:
        return dist_so_far
cities = set()
weights = {}
for line in s.split("\n"):
    from_city, _, to_city, _, dist = line.split()
    weights[(from_city,to_city)] = weights[(to_city,from_city)] = int(dist)
    cities.add(from_city)
    cities.add(to_city)

print(min(travel({fst_city},fst_city,0,min) for fst_city in cities))

#second part
print(max(travel({fst_city},fst_city,0,max) for fst_city in cities))