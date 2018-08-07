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
        self.bmap = mp.BattleMap(2, 3)
        self.primeList = sp.primerange(0, 100)
        self.p_ch = OrderedDict()
        self.time = 0
        self.rel_matrix = None

    def makeBattle(self):
        # open the character datafile, load in character data
        with open(os.path.join(DATA_DIR, 'p_characters.csv')) as csvFile:
            csvRead = csv.reader(csvFile)
            self.p_ch.clear()
            for idx, row in enumerate(csvRead):
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
                randX = random.randint(0, self.map.h-1)
                randY = random.randint(0, self.map.w-1)
                self.p_ch[id].set_position(vec.vec2(randX, randY))

                if self.bmap.grid[randX, randY] == -1:
                    self.bmap.grid[randX, randY] = self.primeList[idx]
                else:
                    self.bmap.grid[randX, randY] *= self.primeList[idx]

        self.rel_matrix = np.zeros((len(self.p_ch), len(self.p_ch)), dtype=float)

    def getCharFromMap(self, x, y):
        # TODO do this

    def interact(self, personList):
        # TODO code interaction

    def nextTurn(self):
        self.time += 1
        p_move = 0.6

        ## TODO redo everything below

        # to move or not to move, energy loss, dead?
        for idx, person in self.p_ch.items():
            if person.alive:
                print("Map dimensions:", self.mapWidth, self.mapHeight)
                print("moving", person.name)
                print("initial", person.position)
                rowPos = person.position[0]
                colPos = person.position[1]
                choose = random.random()
                # print("dirtest", choose)
                movetest = random.random()
                # print("movetest", movetest)

                if self.map[rowPos][colPos] == self.primeList[idx]:
                    self.map[rowPos][colPos] = -1
                else:
                    self.map[rowPos][colPos] /= self.primeList[idx]

                if movetest < p_move:
                    # print('moving')
                    if rowPos == 0:
                        # top row
                        # print('toprow')
                        if colPos == 0:
                            # top left corner
                            # print('topleft')
                            if self.mapWidth < 2:
                                # 1 column
                                # print('1 column')
                                if self.mapHeight < 2:
                                    # 1 cell, no movement possible
                                    pass
                                else:
                                    # can only move down
                                    rowPos += 1
                            else:
                                if self.mapHeight < 2:
                                    # can only move right
                                    colPos += 1
                                else:
                                    if choose < 0.4:
                                        rowPos += 1
                                    elif choose < 0.8:
                                        colPos += 1
                                    else:
                                        rowPos += 1
                                        colPos += 1
                        elif colPos == self.mapWidth-1:
                            # top right corner
                            if self.mapHeight < 2:
                                # can only move left
                                colPos -= 1
                            else:
                                if choose < 0.4:
                                    rowPos += 1
                                elif choose < 0.8:
                                    colPos -= 1
                                else:
                                    rowPos += 1
                                    colPos -= 1
                        else:
                            # top side
                            if self.mapHeight < 2:
                                # can only move left/right
                                if choose < 0.5:
                                    colPos += 1
                                else:
                                    colPos -= 1
                            else:
                                if choose < 0.25:
                                    colPos -= 1
                                elif choose < 0.5:
                                    colPos += 1
                                elif choose < 0.75:
                                    rowPos += 1
                                elif choose < 0.875:
                                    rowPos += 1
                                    colPos -= 1
                                else:
                                    rowPos += 1
                                    colPos += 1
                    elif rowPos == self.mapHeight-1:
                        # bottom row
                        if colPos == 0:
                            # bottom left
                            if self.mapWidth == 1:
                                # one column
                                rowPos -= 1
                            else:
                                if choose < 0.4:
                                    rowPos -= 1
                                elif choose < 0.8:
                                    colPos += 1
                                else:
                                    rowPos -= 1
                                    colPos += 1
                        elif colPos == self.mapWidth-1:
                            # bottom right
                            if choose < 0.4:
                                rowPos -= 1
                            elif choose < 0.8:
                                colPos -= 1
                            else:
                                rowPos -= 1
                                colPos -= 1
                        else:
                            # bottom row
                            if choose < 0.25:
                                rowPos -= 1
                            elif choose < 0.5:
                                colPos -= 1
                            elif choose < 0.75:
                                colPos += 1
                            elif choose < 0.875:
                                rowPos -= 1
                                colPos -= 1
                            else:
                                rowPos -= 1
                                colPos += 1
                    else:
                        # check if on first or last column
                        if colPos == 0:
                            # left column
                            if choose < 0.25:
                                rowPos -= 1
                            if choose < 0.5:
                                rowPos += 1
                            if choose < 0.75:
                                colPos += 1
                            if choose < 0.875:
                                colPos += 1
                                rowPos -= 1
                            else:
                                colPos += 1
                                rowPos += 1
                        elif colPos == self.mapWidth-1:
                            # right column
                            if choose < 0.25:
                                rowPos -= 1
                            if choose < 0.5:
                                rowPos += 1
                            if choose < 0.75:
                                colPos -= 1
                            if choose < 0.875:
                                colPos -= 1
                                rowPos -= 1
                            else:
                                colPos -= 1
                                rowPos += 1
                        else:
                            # general cases
                            if choose < 0.15:
                                rowPos -= 1
                            elif choose < 0.3:
                                rowPos += 1
                            elif choose < 0.45:
                                colPos -= 1
                            elif choose < 0.6:
                                colPos += 1
                            elif choose < 0.7:
                                rowPos -= 1
                                colPos -= 1
                            elif choose < 0.8:
                                rowPos -= 1
                                colPos += 1
                            elif choose < 0.9:
                                rowPos += 1
                                colPos -= 1
                            else:
                                rowPos += 1
                                colPos += 1

                    person.energy -= 2
                else:
                    person.energy -= 1

                #print("row, col", rowPos, colPos)

                person.position[0] = rowPos
                person.position[1] = colPos
                print("moved?", person.position)
                # print()

                if self.map[rowPos][colPos] == -1:
                    self.map[rowPos][colPos] = self.primeList[idx]
                else:
                    self.map[rowPos][colPos] *= self.primeList[idx]

                person.active = True

        # discovery, person or event
        # first see if there's another person on the space
        for idx, person in self.p_ch.items():
            if person.alive and person.active:
                # get position
                row = person.position[0]
                col = person.position[1]
                charlist = self.getCharFromMap(row, col)
                if len(charlist) > 1:
                    # code if we limit to 1-1 interactions
                    # choosetarget = random.randint(1, len(charlist)-1)
                    # choice = len(charlist) - 1
                    # for target in charlist:
                    #    if (choosetarget == choice and
                    #        target.alive and not person.id == target.id):
                    #        # some kind of interaction is inevitable
                    #        self.interact2(person, target)
                    #    choice -= 1

                    # for multi-interactions
                    #self.interact(charlist)

                    pass

# gather, prepare, eat

    def printMap(self):
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
            for row in self.map]))


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
    b.printMap()
    b.nextTurn()
    b.printMap()
