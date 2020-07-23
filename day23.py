from aocd import get_data

raw_data = get_data(day=23,year=2015)
instructions = raw_data.split("\n")

def run_program(instructions, registers):
	p = 0
	while p < len(instructions):
		instruction = instructions[p]
		args = instruction.replace(",","").split(" ")
		if args[0] == "hlf":
			registers[args[1]] //= 2
			p += 1
		elif args[0] == "tpl":
			registers[args[1]] *= 3
			p += 1
		elif args[0] == "inc":
			registers[args[1]] += 1
			p += 1
		elif args[0] == "jmp":
			p += int(args[1])
		elif args[0] == "jie":
			p += int(args[2]) if registers[args[1]] % 2 == 0 else 1
		elif args[0] == "jio":
			p += int(args[2]) if registers[args[1]] == 1 else 1
	return registers
print(run_program(instructions, {"a": 0, "b": 0}))
print(run_program(instructions, {"a": 1, "b": 0}))