from discord.ext import commands
import os
import sys
import csv
import random
import game.character as gc

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')


class BattleSim(object):
    def __init__(self, testing):
        self.mapWidth = 2
        self.mapHeight = 3
        self.primeList = [2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37, 41,
                          43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

        self.testing = testing
        self.p_ch = []
        self.map = [[-1 for x in range(self.mapWidth)]
                    for y in range(self.mapHeight)]
        self.rel_matrix = []

    def makeBattle(self):
        with open(os.path.join(DATA_DIR, 'p_characters.csv')) as csvFile:
            csvRead = csv.reader(csvFile)
            del self.p_ch[:]
            for idx, row in enumerate(csvRead):
                name = row[0]
                energy = 10
                warmth = 10
                sanity = 10
                health = 10
                tempchar = gc.Character(name, energy, warmth, sanity, health)
                self.p_ch.append(tempchar)
                randX = random.randint(0, self.mapHeight-1)
                randY = random.randint(0, self.mapWidth-1)
                self.p_ch[idx].set_position(randX, randY)
                self.p_ch[idx].id = idx

                if self.map[randX][randY] == -1:
                    self.map[randX][randY] = self.primeList[idx]
                else:
                    self.map[randX][randY] *= self.primeList[idx]

                print("added", row[0], "into", randX+1, randY+1)
        # print('\n'.join([''.join(['{:4}'.format(item) for item in row])
        #      for row in self.p_pos]))

        for people in self.p_ch:
            self.rel_matrix.append([0 for x in range(len(self.p_ch))])

    def getCharFromMap(self, row, col):
        outList = []
        inVal = self.map[row][col]
        charIdx = 0
        while inVal > 1 and charIdx < len(self.p_ch):
            if inVal % self.primeList[charIdx] == 0:
                # print('okay', inVal, self.primeList[charIdx])
                inVal /= self.primeList[charIdx]
                outList.append(self.p_ch[charIdx])
                charIdx += 1
            else:
                charIdx += 1
        print(', '.join(outList))
        return outList

    def interact(self, personList):
        participants = len(personList)
        if participants == 2:
            rel_score = self.rel_matrix[personList[0]][personList[1]]
            if rel_score > 10:
                # friendly encounter
                

    def nextTurn(self, time):
        p_move = 0.6

        # to move or not to move, energy loss, dead?
        for idx, person in enumerate(self.p_ch):
            if person.alive:
                # print("initial", self.p_pos[idx])
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

                # print("row, col", rowPos, colPos)

                person.position[0] = rowPos
                person.position[1] = colPos
                # print("moved?", self.p_pos[idx])
                # print()

                if self.map[rowPos][colPos] == -1:
                    self.map[rowPos][colPos] = self.primeList[idx]
                else:
                    self.map[rowPos][colPos] *= self.primeList[idx]

                person.active = True

        # discovery, person or event
        # first see if there's another person on the space
        for idx, person in enumerate(self.p_ch):
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
                    self.interact(charlist)

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
    b.nextTurn(1)
    b.printMap()
