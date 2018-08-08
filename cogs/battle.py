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
        p_move = 0.6

        ## TODO redo everything below

        # to move or not to move, energy loss, dead?
        for idx, person in self.p_ch.items():
            if person.alive:
                print("Map dimensions:", self.bmap.w, self.bmap.h)
                print("moving", person.name)
                print("initial", person.position)
                px = person.position.x
                py = person.position.y
                movetest = random.random()

                #print('compare', self.bmap.grid[px, py], self.primeList[idx])
                if self.bmap.grid[px, py] == self.primeList[idx]:
                    self.bmap.grid[px, py] = -1
                else:
                    self.bmap.grid[px, py] /= self.primeList[idx]

                if movetest < p_move:
                    mv.random_walk(person.position, self.bmap.w, self.bmap.h, 0.4)
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
        if random.random() < p_event:
            vval = tval["event"]
            vcont = vval["id"]



        # otherwise forage
        else:
            fval = tval["forage"]
            fcont = fval["content"]
            fresult = random.random()
            item = None
            f_iter = 0
            p = fval["p"]
            p_total = sum(fval["p"])
            while fresult > 0.0:
                if fresult < (p[f_iter] / p_total):
                    fresult = -1
                    item = fcont[f_iter]
                else:
                    f_iter += 1
                    fresult -= (p[f_iter] / p_total)
            print(item)



        #







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
