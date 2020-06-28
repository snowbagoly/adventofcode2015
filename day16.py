from aocd import get_data

import re

sue_pattern = re.compile(r"Sue (?P<id>\d+): (.+): (\d+), (.+): (\d+), (.+): (\d+)")

def is_okay(aunt, expectation):
	for key in aunt:
		if key == "id": continue
		if aunt[key] != expectation[key]:
			return False
	return True

def is_okay_with_updated_retroencabulator(aunt, expectation):
	for key in aunt:
		if key == "id": continue
		if key in ["cats", "trees"]:
			if int(aunt[key]) <= int(expectation[key]):
				return False
		elif key in ["pomeranians", "goldfish"]:
			if int(aunt[key]) >= int(expectation[key]):
				return False
		elif aunt[key] != expectation[key]:
			return False
	return True 

def parse_expected(raw_expected):
	return dict(map(lambda line: line.split(": "), raw_expected.split("\n")))

def parse_aunt(line):
	match = sue_pattern.match(line)
	return dict(zip(("id",)+match.groups()[1::2], match.groups()[::2]))

knowledge = get_data(day=16,year=2015)

raw_expected = """children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1"""

expected = parse_expected(raw_expected)

for raw_aunt in knowledge.split("\n"):
	aunt = parse_aunt(raw_aunt)
	if is_okay(aunt, expected):
		print(aunt["id"])
		break

for raw_aunt in knowledge.split("\n"):
	aunt = parse_aunt(raw_aunt)
	if is_okay_with_updated_retroencabulator(aunt, expected):
		print(aunt["id"])