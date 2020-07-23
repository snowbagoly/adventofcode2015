from aocd import get_data
import re

TIME = 2503
reindeer_regex = re.compile(r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds")

raw_data = get_data(day=14,year=2015)

class Reindeer:
    def __init__(self, name, speed, runtime, resttime):
        self.name = name
        self.speed = int(speed)
        self.runtime = int(runtime)
        self.resttime = int(resttime)
        self.point = 0
    def travel_n_sec(self, n):
        number_of_full_turns = n//(self.runtime+self.resttime)
        remaining_time_in_not_full_turn = n%(self.runtime+self.resttime)
        return self.speed*(number_of_full_turns*self.runtime + min(self.runtime, remaining_time_in_not_full_turn))
    def __repr__(self):
        return "<Reindeer \"%s\" speed: %d, runtime: %d, resttime: %d, point: %d>" \
                   % (self.name, self.speed, self.runtime, self.resttime, self.point)

def parse_reindeer_line(line):
    name, speed, runtime, resttime = reindeer_regex.match(line).group(1,2,3,4)
    return Reindeer(name, speed, runtime, resttime)

reindeers = list(map(parse_reindeer_line, raw_data.split("\n")))
print(max(reindeer.travel_n_sec(TIME) for reindeer in reindeers))

for t in range(1,TIME+1):
    max_dist = max(reindeer.travel_n_sec(t) for reindeer in reindeers)
    for reindeer in reindeers:
        if reindeer.travel_n_sec(t) == max_dist:
            reindeer.point += 1
print(max(reindeer.point for reindeer in reindeers))