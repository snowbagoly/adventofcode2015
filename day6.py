from aocd import get_data

s = get_data(day=6,year=2015)

#first part
def turn_on(x1,y1,x2,y2):
	for i in range(x1,x2+1):
		for j in range(y1,y2+1):
			lights[i][j] = True
def turn_off(x1,y1,x2,y2):
	for i in range(x1,x2+1):
		for j in range(y1,y2+1):
			lights[i][j] = False
def toggle(x1,y1,x2,y2):
	for i in range(x1,x2+1):
		for j in range(y1,y2+1):
			lights[i][j] = not lights[i][j]

lights = [[False for i in range(1000)] for j in range(1000)]
for line in s.split("\n"):
	instr, p1, _, p2 = line.replace("turn ","turn_").split()
	eval("%s(%s,%s)" % (instr,p1,p2))
print(sum(map(sum,lights)))

#second part
lights = [[0 for i in range(1000)] for j in range(1000)]
def turn_on(x1,y1,x2,y2):
	for i in range(x1,x2+1):
		for j in range(y1,y2+1):
			lights[i][j] += 1
def turn_off(x1,y1,x2,y2):
	for i in range(x1,x2+1):
		for j in range(y1,y2+1):
			lights[i][j] = max(lights[i][j]-1,0)
def toggle(x1,y1,x2,y2):
	turn_on(x1,y1,x2,y2)
	turn_on(x1,y1,x2,y2)
for line in s.split("\n"):
	instr, p1, _, p2 = line.replace("turn ","turn_").split()
	eval("%s(%s,%s)" % (instr,p1,p2))
print(sum(map(sum,lights)))