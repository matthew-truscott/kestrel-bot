import game.br_vec as vec
import game.br_json as js
import random

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

    def add_item(self, item, item_dict):
        # if an item of carry is introduced, often will want an intelligent way of cleaning up the inventory so the
        # least valuable thing is thrown, value per carry. If conflicts, go by count, else randomize
        trash = item
        vpcref = item["value"] / item["carry"]
        n = 1
        res = 0
        while trash["carry"] + self.carry > self.carrylimit():
            for k, count in self.inventory.items():
                if k < 1:
                    # houston we have a problem
                    self.inventory.pop(k, None)
                else:
                    # compare vpc
                    iitem = item_dict["%i" % (k)]
                    vpc = iitem["value"] / iitem["carry"]
                    if vpc < vpcref:
                        trash = iitem
                        vpcref = vpc
                        n = count
                    elif vpc == vpcref:
                        if count == 0:
                            # key should have been cleared
                            self.inventory.pop(k, None)
                        elif count < n:
                            trash = iitem
                            vpcref = vpc
                            n = count
                        elif count == n:
                            if random.random() < 0.5:
                                trash = iitem
                                vpcref = vpc
            # now we have trash to throw
            if item["id"] == trash["id"]:
                # do nothing, since there is no space and item is not valuable enough to keep
                res = 1
            else:
                if self.inventory[trash["id"]] == 1:
                    self.inventory.pop(trash["id"], None)
                else:
                    self.inventory[trash["id"]] -= 1
        return res

    def show_inventory(self, item_dict):
        for k, count in self.inventory.items():
            item = item_dict["%i" % (k)]
            print(item.name, ": ", count)







    def loot(self, corpse, item_dict):
        loot = 0
        if "protection" in corpse:
            id = js.get_random_element(corpse, "protection")
            item = item_dict["%i" % (id)]
            if item["category"] == "x":
                # no chest armour loot
                pass
            elif item["category"] == "armour":
                # equip and replace if better than current protection, otherwise, leave
                if self.protection <= item["protection"]:
                    self.armour = item
                    self.protection = item["protection"]
                    loot += 1
                    print("picked up", item["name"])
        if "weapon" in corpse:
            id = js.get_random_element(corpse, "weapon")
            item = item_dict["%i" % (id)]
            if item["category"] == "x":
                pass
            elif item["category"] == "weapon":
                # equip if better range, keep old weapon if it has more damage
                # else loot if better damage
                # loot if current weapon(s) are non-perma
                # if overlimit, run inventory handling first
                if not self.weapon:
                    self.weapon = item
                    loot += 1
                    print("picked up", item["name"])
                elif self.weapon["range"] <= item["range"]:
                    if self.weapon["damage"] > item["damage"]:
                        self.add_item(self.weapon, item_dict)
                    self.weapon = item
                    loot += 1
                    print("picked up", item["name"])
                elif self.weapon["damage"] < item["damage"]:
                    self.add_item(item, item_dict)
                    loot += 1
                    print("stored", item["name"])
                elif self.weapon["ammo"] > 0:
                    self.add_item(item, item_dict)
                    loot += 1
                    print("stored", item["name"])
        if "junk" in corpse:
            id = js.get_random_element(corpse, "junk")
            item = item_dict["%i" % (id)]
            if item["category"] == "x":
                pass
            elif item["category"] == "junk":
                # loot if valuable enough
                self.add_item(item, item_dict)
                loot += 1
                print("stored", item["name"])
        print("loot", loot)
        return loot
