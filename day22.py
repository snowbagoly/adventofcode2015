from aocd import get_data
import re
import math

class Effect:
    def __init__(self, id, cost, timer, damage, heal, armor, mana):
        self.id = id
        self.cost = cost
        self.timer = timer
        self.damage = damage
        self.heal = heal
        self.armor = armor
        self.mana = mana
    def do_effect(self, player, boss, is_player_turn):
        self.timer -= 1
        boss.hit_points -= self.damage
        player.hit_points += self.heal
        player.armor = self.armor if self.armor > 0 else player.armor
        player.mana += self.mana
    def copy_effect(self):
        return Effect(self.id, self.cost, self.timer, self.damage, self.heal, self.armor, self.mana)
    def __repr__(self):
        return "<Effect %s (Cost: %d, Turns left: %d, Damage: %d, Heal: %d, Armor: %d, Mana: %d)>" % (self.id, self.cost, self.timer, self.damage, self.heal, self.armor, self.mana)

class Wizard:
    def __init__(self, hit_points, mana):
        self.hit_points = hit_points
        self.mana = mana
        self.armor = 0
    def __repr__(self):
        return "<Wizard (HP: %d, M: %d)>" % (self.hit_points, self.mana)

class Boss:
    def __init__(self, hit_points, damage):
        self.id = id
        self.hit_points = hit_points
        self.damage = damage
    def __repr__(self):
        return "<Boss (HP: %d, D: %d)>" % (self.hit_points, self.damage)

# TODO the copies should probably be at the same place (effects are now copied only when the scenario is valid,
# everything else is copied before)
def calculate_next_turn(player, boss, is_player_next, total_mana_cost, active_effects, history, is_hard_mode):
    global best_mana_cost
    if boss.hit_points > 0 and player.hit_points > 0 and (best_mana_cost is None or total_mana_cost < best_mana_cost):
        if is_hard_mode and is_player_next:
            player.hit_points -= 1
        if player.hit_points <= 0:
            return
        active_effects = list(map(lambda e: e.copy_effect(), active_effects))
        player.armor = 0
        for effect in active_effects:
            effect.do_effect(player, boss, is_player_next)
        active_effects = list(filter(lambda effect: effect.timer > 0, active_effects))
        if boss.hit_points <= 0: # killing the boss with a long-lasting effect
            if best_mana_cost is None or total_mana_cost < best_mana_cost:
                best_mana_cost = total_mana_cost
        if is_player_next:
            for instant_effect in instant_effects:
                if player.mana >= instant_effect.cost:
                    new_player = Wizard(player.hit_points, player.mana - instant_effect.cost)
                    new_boss = Boss(boss.hit_points, boss.damage)
                    instant_effect.do_effect(new_player, new_boss, is_player_next)
                    calculate_next_turn(new_player, new_boss, not is_player_next, total_mana_cost + instant_effect.cost, active_effects, history + (instant_effect.id,), is_hard_mode)
            
            active_effect_names = set(effect.id for effect in active_effects)
            for long_lasting_effect in long_lasting_effects:
                if long_lasting_effect.id not in active_effect_names and player.mana >= long_lasting_effect.cost:
                    new_player = Wizard(player.hit_points, player.mana - long_lasting_effect.cost)
                    new_boss = Boss(boss.hit_points, boss.damage)
                    calculate_next_turn(new_player, new_boss, not is_player_next, total_mana_cost + long_lasting_effect.cost, active_effects + [long_lasting_effect], history + (long_lasting_effect.id,), is_hard_mode)
        else:
            new_player = Wizard(player.hit_points - max(1, boss.damage - player.armor), player.mana)
            new_boss = Boss(boss.hit_points, boss.damage)
            calculate_next_turn(new_player, new_boss, not is_player_next, total_mana_cost, active_effects, history, is_hard_mode)
    if boss.hit_points <= 0: # killing the boss with an instant effect
        if best_mana_cost is None or total_mana_cost < best_mana_cost:
            best_mana_cost = total_mana_cost

item_pattern = re.compile(r"(?P<item_name>\S+\s?\S+?)\D+(?P<cost>\d+)\D+(?P<damage>\d+)\D+(?P<armor>\d+)")
boss_pattern = re.compile(r"Hit Points: (?P<hit_points>\d+)\nDamage: (?P<damage>\d+)")
raw_data = get_data(day=22,year=2015)
matches = boss_pattern.match(raw_data)

instant_effects = [Effect("magic_missile", 53, 1, 4, 0, 0, 0), Effect("drain", 73, 1, 2, 2, 0, 0)]
long_lasting_effects = [Effect("shield", 113, 6, 0, 0, 7, 0), Effect("poison", 173, 6, 3, 0, 0, 0),
           Effect("recharge", 229, 5, 0, 0, 0, 101)]


best_mana_cost = None
calculate_next_turn(Wizard(50, 500), Boss(*[int(matches.group(label)) for label in ["hit_points", "damage"]]), True, 0, [], (), False)
print(best_mana_cost)

best_mana_cost = None
calculate_next_turn(Wizard(50, 500), Boss(*[int(matches.group(label)) for label in ["hit_points", "damage"]]), True, 0, [], (), True)
print(best_mana_cost)