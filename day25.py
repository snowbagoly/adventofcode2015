from aocd import get_data
import re

MUL_CONST = 252533
MOD_CONST = 33554393
FIRST_VALUE_CONST = 20151125

def parse_expected_pos(raw_data):
    number_regex = re.compile(r"\D*(\d+)\D*(\d+)")
    return tuple(map(lambda x: int(x)-1, number_regex.match(raw_data).group(1,2)))

def calculate_expected_index(x,y):
    n = x + y # the number of "complete diagonals" before this index
    return n * (n + 1) // 2 + y # the number of fields in the former diagonals, plus the remaining in the current diagonal

def calculate_multiplier(multiplier_map, i):
    multiplier_map[i] = multiplier_map[i//2]**2%MOD_CONST

raw_data = get_data(day=25,year=2015)
expected_pos = parse_expected_pos(raw_data)
expected_index = calculate_expected_index(*expected_pos)

multiplier_map = { 1: MUL_CONST }

i = 1
while i < expected_index:
    i *= 2
    calculate_multiplier(multiplier_map, i)

i = 1
current_value = FIRST_VALUE_CONST
for b in bin(expected_index)[2::][::-1]:
    if b == "1":
        current_value *= multiplier_map[i]
        current_value %= MOD_CONST
    i *= 2

print(current_value)