from aocd import get_data

s = get_data(day=2,year=2015)

#first part
def line_to_sq_feet(line):
    a,b,c = map(int,line.split("x"))
    sides = [a*b,b*c,a*c]
    return sum(sides)*2 + min(sides)
print(sum(map(line_to_sq_feet,s.split("\n"))))

#second part
def line_to_ribbon(line):
    a,b,c = sorted(map(int,line.split("x")))
    sides = [a*b,b*c,a*c]
    return 2*a + 2*b + a*b*c
print(sum(map(line_to_ribbon,s.split("\n"))))