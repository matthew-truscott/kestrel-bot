from discord.ext import commands
import os
import sys
import csv
import random
import json
import sympy as sp
import numpy as np
from collections import OrderedDict
import game.character as gc
import game.br_vec as vec
import game.br_move as mv
import game.br_map as mp
import game.br_json as js

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

class BattleSim(object):
    """
    CLASS BattleSim: battle royale simulator, uses a lot of libraries in game folder
    """
    def __init__(self, testing):
        self.bmap = mp.BattleMap(4, 4)
        self.primeList = list(sp.primerange(0, 100))
        self.p_ch = OrderedDict()
        self.time = 0
        self.rel_matrix = {}
        self.message = ""
        self.pull = 0

    def makeBattle(self):
        print(self.primeList)
        # open the character datafile, load in character data
        with open(os.path.join(DATA_DIR, 'p_characters.csv')) as csvFile:
            csvRead = csv.reader(csvFile)
            self.p_ch.clear()
            for row in csvRead:
                name = row[0]
                energy = 10
                warmth = 10
                sanity = 10
                health = 10
                # id needs to be first available
                # TODO might want to find a way to reuse old IDs
                id = 0
                if self.p_ch:
                    id = next(reversed(self.p_ch)) + 1
                else:
                    id = 1

                self.p_ch[id] = gc.Character(name, energy, warmth, sanity, health)
                rx = random.randint(0, self.bmap.h-1)
                ry = random.randint(0, self.bmap.w-1)
                self.p_ch[id].set_position(rx, ry)
                self.p_ch[id].id = id

                if self.bmap.grid[rx, ry] == -1:
                    self.bmap.grid[rx, ry] = int(self.primeList[id])
                else:
                    self.bmap.grid[rx, ry] = int(self.bmap.grid[rx, ry] * self.primeList[id])

        for key, val in self.p_ch.items():
            self.rel_matrix[key] = {}
            for rkey, rval in self.p_ch.items():
                if key == rkey:
                    self.rel_matrix[key][rkey] = val.sanity
                else:
                    self.rel_matrix[key][rkey] = 0

    def getCharFromMap(self, x, y):
        i = 0
        content = self.bmap.grid[x, y]
        outlist = []
        while content > 1 and i < len(self.p_ch):
            # try dividing by prime
            if content % self.primeList[i+1] == 0:
                content /= self.primeList[i+1]
                outlist.append(self.p_ch[i+1])
            i += 1
        return outlist

    def interact(self, personList):
        # TODO code interaction
        pass

    def nextTurn(self):
        self.time += 1
        self.pull += 0.1

        ## TODO redo everything below

        # to move or not to move, energy loss, dead?
        for idx, person in self.p_ch.items():
            if not person.alive:
                continue

            print("Map dimensions:", self.bmap.w, self.bmap.h)
            print("moving", person.name)
            print("initial", person.position)
            px = person.position.x
            py = person.position.y
            movetest = random.random()
            pmove = (self.pull + (person.energy / 10)) / (person.shelter + 1)

            #print('compare', self.bmap.grid[px, py], self.primeList[idx])
            if self.bmap.grid[px, py] == self.primeList[idx]:
                self.bmap.grid[px, py] = -1
            else:
                self.bmap.grid[px, py] /= self.primeList[idx]

            if movetest < pmove and person.energy > 1:
                if self.pull > 1:
                    ppull = 1
                else:
                    ppull = self.pull
                mv.random_walk(person.position, self.bmap.w, self.bmap.h, ppull)
                person.energy -= 2
            else:
                person.energy -= 1

            print("moved?", person.position)

            px = person.position.x
            py = person.position.y

            if self.bmap.grid[px, py] == -1:
                self.bmap.grid[px, py] = self.primeList[idx]
            else:
                self.bmap.grid[px, py] *= self.primeList[idx]

            person.active = True

        # discovery, person or event
        # first see if there's another person on the space
        for idx, person in self.p_ch.items():
            if person.alive and person.active:
                # get position
                px = person.position.x
                py = person.position.y
                charlist = self.getCharFromMap(px, py)
                if len(charlist) == 0:
                    # this should never happen
                    print('event checking found noone where a person should have been')
                    continue
                elif len(charlist) == 1:
                    # solo interactions
                    self.interact_solo(charlist[0])
                elif len(charlist) == 2:
                    # duo interactions
                    pass
                else:
                    # multi interactions
                    pass

        # check if dead
        for idx, person in self.p_ch.items():
            if person.alive:
                if person.health <= 0:
                    print(person.name, "died somehow")
                    person.alive = False
                elif person.energy <= 0:
                    print(person.name, "died of hunger")
                    person.alive = False
                elif person.warmth <= 0:
                    print(person.name, "died of hypothermia")
                    person.alive = False


        # debug, eventually output to bot
        print(self.message)
        self.message = ""

    def interact_solo(self, person):
        print('id', person.id)
        print(self.rel_matrix[person.id][person.id])
        if self.rel_matrix[person.id][person.id] <= -10:
            # suicide
            self.message += "%s killed themselves due to insanity\n" % (person.name)
            person.alive = False
        px = person.position.x
        py = person.position.y

        """
        A typical turn goes as follows:
        - gather (either in the wild or in an urban setting where one can loot) (event chance)
        - prepare (event chance if none already)
        - eat
        - sleep
        """

        # --- GATHER ----------------------------------------------------------
        with open(os.path.join(DATA_DIR, 'terrain.json'), 'r') as f:
            terrain_dict = json.load(f)
        with open(os.path.join(DATA_DIR, 'items.json'), 'r') as f:
            item_dict = json.load(f)
        with open(os.path.join(DATA_DIR, 'events.json'), 'r') as f:
            event_dict = json.load(f)
        # get terrain
        tkey = self.bmap.terrain[px, py]
        #print(terrain_dict["%i" % (tkey)]["name"])
        tval = terrain_dict["%i" % (tkey)]

        # check event
        p_event = tval["p_event"]
        if random.random() < (p_event / 100):
            event = js.get_random_element(tval, "event")
            event_obj = event_dict["%i" % (event)]
            print("event", event_obj["name"])
            # if event is disaster, apply effects on player, unless they are sheltered or protected
            # if sheltered, apply damage to health on shelter
            # if not sheltered but protected, apply damage to health on protection
            if event_obj["category"] == "disaster":
                if "health" in event_obj:
                    h = event_obj["health"]
                    if h < 0:
                        if person.shelter == 0:
                            if person.protection == 0:
                                person.affect(event_obj)
                            else:
                                person.protection += h
                                if person.protection < 0:
                                    person.protection = 0
                        else:
                            person.shelter += h
                            if person.shelter < 0:
                                person.shelter = 0
                print("damage dealt by disaster", person.health, person.protection, person.shelter)


        # otherwise forage
        else:
            item = js.get_random_element(tval, "forage")
            item_obj = item_dict["%i" % (item)]
            print("item", item_obj["name"])
            # if forage is junk, check if space and equip if possible
            if item_obj["category"] == "junk":
                print("junk")
                ia = person.add_item(item_obj)
                if ia > 0:
                    print("inventory full")
                else:
                    print("picked up item")
            # if forage is food, check if space and equip, or eat if not possible
            elif item_obj["category"] == "food":
                print("food")
                ia = person.add_item(item_obj)
                if ia > 0:
                    person.eat_food(item_obj)
                    print("ate food")
                else:
                    print("picked up food")
            # if forage is meat, check if space and equip, or eat if hunger/sanity is critical
            elif item_obj["category"] == "meat":
                print("meat")
                ia = person.add_item(item_obj)
                if ia > 0 and (person.hunger < 3 or person.sanity < 3):
                    person.eat_rawfood(item_obj)
                    print("ate raw meat")
                else:
                    print("picked up meat")
            elif item_obj["category"] == "corpse":
                print("corpse")
                ia = person.loot(item_obj)



        #sleep
        person.energy -= 3
        print("\n")







class BattleCog(object):
    def __init__(self, bot):
        self.bot = bot
        self.p_ch = []

    @commands.command(hidden=True)
    async def battle(self):
        pass

    def setup(bot):
        bot.add_cog(BattleCog(bot))


if __name__ == '__main__':
    b = BattleSim(1)
    b.makeBattle()
    print(b.bmap.grid)
    b.nextTurn()
    print(b.bmap.grid)
    b.nextTurn()
    print(b.bmap.grid)
    b.nextTurn()
    print(b.bmap.grid)
    b.nextTurn()
    print(b.bmap.grid)
