from aocd import get_data

s = get_data(day=7,year=2015)

#first part
def bitwise_not(n):
	return 65535 - n

from_wires = {}
for line in s.split("\n"):
	data = line.split(" -> ")
	from_wires[data[1]] = data[0]

def calculate_values():
	demands = ["a"]
	while demands:
		p = demands[-1]
		descr = from_wires[p]
		if descr.isdigit():
			value[p] = int(descr)
			demands.pop()
		elif " " not in descr:
			if descr not in value:
				demands.append(descr);continue
			value[p] = value[descr]
			demands.pop()
		elif "NOT" in descr:
			a = descr.split()[1]
			if not a.isdigit() and a not in value:
				demands.append(a);continue
			else:
				a = int(a) if a.isdigit() else value[a]
			
			value[p] = bitwise_not(a)
			demands.pop()
		else:
			a,op,b = descr.split()
			if not a.isdigit() and a not in value:
				demands.append(a);continue
			else:
				a = int(a) if a.isdigit() else value[a]
			if not b.isdigit() and b not in value:
				demands.append(b);continue
			else:
				b = int(b) if b.isdigit() else value[b]
			
			if op == "AND":
				value[p] = a & b
			elif op == "OR":
				value[p] = a | b
			elif op == "LSHIFT":
				value[p] = a << b
			elif op == "RSHIFT":
				value[p] = a >> b
			demands.pop()
value = {}
calculate_values()
print(value["a"])

#second part
value = {"b": value["a"]}
calculate_values()
print(value["a"])