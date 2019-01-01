from aocd import get_data

s = get_data(day=4,year=2015)

#first part
import md5
def search(zero_num):
    code = ""
    k = 0
    while code[:zero_num] != "0"*zero_num:
        k += 1
        code = md5.new(s + str(k)).hexdigest()
    return k
print(search(5))

#second part
print(search(6))