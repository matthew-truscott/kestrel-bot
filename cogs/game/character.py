import game.br_vec as vec
import game.br_json as js

class Character(object):
    def __init__(self, name,
                 init_energy,
                 init_warmth,
                 init_sanity,
                 init_health):
        self.id = -1 # unset
        self.name = name
        self.energy = init_energy
        self.warmth = init_warmth
        self.sanity = init_sanity
        self.health = init_health
        self.maxenergy = init_energy
        self.maxwarmth = init_warmth
        self.maxsanity = init_sanity
        self.maxhealth = init_health
        self.alignment = 0
        self.position = [0, 0]
        self.active = False
        self.alive = True
        self.position = None
        self.carry = 0
        self.inventory = {}
        self.overheat = 0
        self.shelter = 0
        self.protection = 0
        self.armour = None
        self.weapon = None

    def set_position(self, x, y):
        self.position = vec.vec2(x, y)

    def set_id(self, id):
        self.id = id

    def carrylimit(self):
        cl = (self.energy // 2) + 5
        return cl

    def add_item(self, item):
        if self.carry + item["carry"] < self.carrylimit():
            if item["id"] in self.inventory:
                self.inventory[item["id"]] += 1
            else:
                self.inventory[item["id"]] = 1
            return 0
        else:
            return 1

    def eat_food(self, item):
        if "energy" in item:
            self.energy += item["energy"]
            if self.energy > self.maxenergy:
                self.energy = self.maxenergy
        if "warmth" in item:
            self.warmth += item["warmth"]
            if self.warmth > self.maxwarmth:
                self.warmth = self.maxwarmth
        if "sanity" in item:
            self.sanity += item["sanity"]
            if self.sanity > self.maxsanity:
                self.sanity = self.maxsanity
        if "health" in item:
            self.health += item["health"]
            if self.health > self.maxhealth:
                self.health = self.maxhealth

    def eat_rawfood(self, item):
        if "energy" in item:
            self.energy += item["energy_raw"]
            if self.energy > self.maxenergy:
                self.energy = self.maxenergy
        if "warmth" in item:
            self.warmth += item["warmth_raw"]
            if self.warmth > self.maxwarmth:
                self.warmth = self.maxwarmth
        if "sanity" in item:
            self.sanity += item["sanity_raw"]
            if self.sanity > self.maxsanity:
                self.sanity = self.maxsanity
        if "health" in item:
            self.health += item["health_raw"]
            if self.health > self.maxhealth:
                self.health = self.maxhealth

    def affect(self, event):
        if "energy" in event:
            self.energy += event["energy"]
            if self.energy > self.maxenergy:
                self.energy = self.maxenergy
        if "warmth" in event:
            self.warmth += event["warmth"]
            if self.warmth > self.maxwarmth:
                self.warmth = self.maxwarmth
        if "sanity" in event:
            self.sanity += event["sanity"]
            if self.sanity > self.maxsanity:
                self.sanity = self.maxsanity
        if "health" in event:
            self.health += event["health"]
            if self.health > self.maxhealth:
                self.health = self.maxhealth

    def loot(self, corpse):
        if "protection_chest" in corpse:
            item = js.get_random_element(corpse["protection"])
            if item["category"] == "none":
                # no chest armour loot
                pass
            elif item["category"] == "armour":
                # equip and replace if better than current protection, otherwise, leave
                if self.protection <= item["protection"]:
                    self.armour = item
                    self.protection = item["protection"]
            elif item["category"] == "weapon":
                # equip if better range, keep old weapon if it has more damage
                # else loot if better damage
                # loot if current weapon(s) are non-perma
                
