from discord.ext import commands
import os
import sys
import csv
import random

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

class BattleSim(object):
    def __init__(self, testing):
        self.mapWidth = 10
        self.mapHeight = 10
        self.primeList = [2, 3, 5, 7, 11, 13, 17, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

        self.testing = testing
        self.p_ch = []
        self.p_pos = []
        self.p_energy = []
        self.p_warmth = []
        self.p_sanity = []
        self.p_health = []
        self.map = [[-1 for x in range(self.mapWidth)] for y in range(self.mapHeight)]

    def makeBattle(self):
        with open(os.path.join(DATA_DIR, 'p_characters.csv')) as csvFile:
            csvRead = csv.reader(csvFile)
            del self.p_ch[:]
            for idx, row in enumerate(csvRead):
                self.p_ch.append(row[0])
                randX = random.randint(0, self.mapWidth-1)
                randY = random.randint(0, self.mapHeight-1)
                self.p_pos.append([randX, randY])
                self.p_energy.append(10)
                self.p_warmth.append(10)
                self.p_sanity.append(10)
                self.p_health.append(10)

                if self.map[randX][randY] == -1:
                    self.map[randX][randY] = self.primeList[idx]
                else:
                    self.map[randX][randY] *= self.primeList[idx]

                print("added", row[0], "into", randX+1, randY+1)
        #print('\n'.join([''.join(['{:4}'.format(item) for item in row])
        #      for row in self.p_pos]))

    def getCharFromMap(self, row, col):
        outList = []
        inVal = self.map[row-1][col-1]
        charIdx = 0
        while inVal > 1 and charIdx < len(self.p_ch):
            if inVal % self.primeList[charIdx] == 0:
                #print('okay', inVal, self.primeList[charIdx])
                inVal /= self.primeList[charIdx]
                outList.append(self.p_ch[charIdx])
                charIdx += 1
            else:
                charIdx += 1
        print(', '.join(outList))
        return outList

    def nextTurn(self, time):
        #to move or not to move, energy loss, dead?

        #discovery, person or event
        #gather, prepare, eat


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
    b.getCharFromMap(1, 1)
