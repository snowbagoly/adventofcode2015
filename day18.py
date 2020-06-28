from aocd import get_data

test_data = """.#.#.#
...##.
#....#
..#...
#.#..#
####.."""

raw_data = get_data(day=18,year=2015)

NUMBER_OF_STEPS = 100
MATRIX_SIZE = 100

def convert_char_to_bool(c):
	return c == "#"

def convert_bool_to_char(b):
	return "#" if b else "."

def is_valid_coordinate(x,y):
	return x>=0 and x<MATRIX_SIZE and y>=0 and y<MATRIX_SIZE

# This function was replaced by the calculate_on_neighours matrix creation
def get_number_of_on_neighbours(lightmatrix, x,y):
	return sum(1 for i in range(x-1,x+2) \
		         for j in range(y-1,y+2) \
		         if is_valid_coordinate(i,j) and (i,j) != (x,y) and lightmatrix[i][j])

def neighbour_coords(x,y):
	return [(i,j) for i in range(x-1,x+2) \
	              for j in range(y-1,y+2) \
	              if is_valid_coordinate(i,j) and (i,j) != (x,y)]

def calculate_on_neighbours(lightmatrix):
	on_neighbours = [[0 for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
	for i in range(MATRIX_SIZE):
		for j in range(MATRIX_SIZE):
			if lightmatrix[i][j]:
				for nx,ny in neighbour_coords(i,j):
					on_neighbours[nx][ny] += 1
	return on_neighbours

def calculate_next_state(lightmatrix, on_neighbours, x,y):
	return (lightmatrix[x][y] and on_neighbours[x][y] in [2,3]) \
	    or (not lightmatrix[x][y] and on_neighbours[x][y] == 3)

def print_lightmatrix(lightmatrix):
	print(*["".join(map(convert_bool_to_char,line)) for line in lightmatrix],sep="\n")

def step(lightmatrix):
	on_neighbours = calculate_on_neighbours(lightmatrix)
	next_lightmatrix = []
	for i in range(len(lightmatrix)):
		next_lightmatrix.append([])
		for j in range(len(lightmatrix[i])):
			next_lightmatrix[-1].append(calculate_next_state(lightmatrix, on_neighbours,i,j))
	return next_lightmatrix

def step_with_stuck(lightmatrix):
	lightmatrix[0][0] = lightmatrix[0][-1] = lightmatrix[-1][0] = lightmatrix[-1][-1] = True
	next_lightmatrix = step(lightmatrix)
	next_lightmatrix[0][0] = next_lightmatrix[0][-1] = next_lightmatrix[-1][0] = next_lightmatrix[-1][-1] = True
	return next_lightmatrix

lightmatrix = [list(map(convert_char_to_bool, line)) for line in raw_data.split("\n")]
for i in range(NUMBER_OF_STEPS):
	lightmatrix = step(lightmatrix)
print(sum(1 for line in lightmatrix for light in line if light))


lightmatrix = [list(map(convert_char_to_bool, line)) for line in raw_data.split("\n")]
for i in range(NUMBER_OF_STEPS):
	lightmatrix = step_with_stuck(lightmatrix)
print(sum(1 for line in lightmatrix for light in line if light))