from aocd import get_data

s = get_data(day=12,year=2015)

#first part
import re

number_regex = re.compile("-?\\d+")

matches = number_regex.findall(s)
print(sum(map(int,matches)))

#second part
def add_to_list_or_summa(value):
    global q, no_red_summa
    if number_regex.match(str(value)):
        no_red_summa += value
    elif isinstance(value,list) or isinstance(value,dict):
            q.append(value)

q = [eval(s)]
no_red_summa = 0
while q:
    p = q.pop(0)
    if isinstance(p,list):
        for val in p:
            add_to_list_or_summa(val)
            
    else:
        has_red_key = any(p[key] == "red" for key in p)
        if not has_red_key:
            for key in p:
                add_to_list_or_summa(p[key])
print(no_red_summa)