import os
import sqlite3
from cogs.utils import m_parser as pa
from discord.ext import commands
import random


class MarkovNet(object):
    ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
    DATA_DIR = os.path.join(ROOT_DIR, 'data')

    def __init__(self, bot):
        self.undo_buffer = ''
        self.bot = bot
        self.brain = 'test'

        '''
        There are a lot of databases to be created, one pair for each gram. If we want to
        store words up to a depth of 3, we need 4 databases to store word pairs or triplets
        and one for the dictionary itself. The dictionary pairs word ids to words and the
        other databases relate id pairs/groups to their frequency.
        :param brain:
        '''
        self.dictionary = sqlite3.connect(os.path.join(MarkovNet.DATA_DIR, self.brain + '_dict.db'))
        self.fu_list = sqlite3.connect(os.path.join(MarkovNet.DATA_DIR, self.brain + '_fu.db'))
        self.ru_list = sqlite3.connect(os.path.join(MarkovNet.DATA_DIR, self.brain + '_ru.db'))

        self.dt_curs = self.dictionary.cursor()
        self.fu_curs = self.fu_list.cursor()
        self.ru_curs = self.ru_list.cursor()

        self.dt_curs.execute('''
                             CREATE TABLE IF NOT EXISTS dictionary(
                                wID INTEGER PRIMARY KEY AUTOINCREMENT,
                                word TEXT,
                                class TEXT,
                                plrp TEXT,
                                past TEXT,
                                have TEXT
                             )
                             ''')
        self.fu_curs.execute('''
                             CREATE TABLE IF NOT EXISTS uForwardNet(
                                wordA INTEGER,
                                next INTEGER,
                                count INTEGER,
                                FOREIGN KEY(wordA) REFERENCES dictionary(wID),
                                FOREIGN KEY(next) REFERENCES dictionary(wID)
                             )
                             ''')
        self.ru_curs.execute('''
                             CREATE TABLE IF NOT EXISTS uReverseNet(
                                wordA INTEGER,
                                prev INTEGER,
                                count INTEGER,
                                FOREIGN KEY(wordA) REFERENCES dictionary(wID),
                                FOREIGN KEY(prev) REFERENCES dictionary(wID)
                             )
                             ''')

    def search_dict(self, word):
        query = self.dt_curs.execute('SELECT * FROM dictionary WHERE word=?',
                                     (word,))
        if self.dt_curs:
            d_id = []
            for row in self.dt_curs:
                d_id.append(row[0])
            return d_id
        else:
            return [0]

    def search_id(self, wid):
        query = self.dt_curs.execute('SELECT * FROM dictionary WHERE wid=?',
                                     (wid,))
        if query:
            return wid
        else:
            return 0

    def get_word(self, wid):
        query = self.dt_curs.execute('SELECT * FROM dictionary WHERE wid=?',
                                     (wid,))

        if query:
            ostr = ''
            for row in self.dt_curs:
                ostr = row[1]
            return ostr
        else:
            return None

    def add_to_dict(self, word):
        self.dt_curs.execute('INSERT INTO dictionary(word) VALUES (?)',
                             (word,))

    def remove_from_dict(self, wid):
        self.dt_curs.execute('DELETE * FROM dictionary WHERE wID=?',
                             (wid,))

    def print_dict(self):
        for row in self.dt_curs.execute('SELECT * FROM dictionary ORDER BY wID'):
            print(row)

    def fu_search(self, wordA, next):
        query = self.fu_curs.execute('SELECT * FROM uForwardNet WHERE wordA=? AND next=?',
                                     (wordA, next,))

        if query:
            count = 0
            for row in query:
                count = row[2]
            return count
        else:
            return 0

    def fu_add(self, wordA, next):
        for wi in self.search_dict(wordA):
            for ni in self.search_dict(next):
                if wi == 0:
                    self.add_to_dict(wordA)
                    wi = self.search_dict(wordA)[0]
                if ni == 0:
                    self.add_to_dict(next)
                    ni = self.search_dict(next)[0]

                count = self.fu_search(wi, ni)

                if count == 0:
                    self.fu_curs.execute('INSERT INTO uForwardNet(wordA, next, count) VALUES (?, ?, ?)',
                                         (wi, ni, 1,))
                else:
                    self.fu_curs.execute('UPDATE uForwardNet SET count=? WHERE wordA=? AND next=?',
                                         (count + 1, wi, ni))

    def fu_removeone(self, wordA, next):
        for wi in self.search_dict(wordA):
            for ni in self.search_dict(next):
                if wi == 0:
                    return
                if ni == 0:
                    return

                count = self.fu_search(wi, ni)

                if count == 0:
                    return
                if count == 1:
                    self.fu_curs.execute('DELETE * from uForwardNet WHERE wordA=? AND next=?',
                                         (wi, ni,))
                else:
                    self.fu_curs.execute('UPDATE uForwardNet SET count=? WHERE wordA=? AND next=?',
                                         (count - 1, wi, ni))

                # delete word if necessary
                query = self.fu_curs.execute('SELECT * FROM uForwardNet WHERE wordA=? OR next=?',
                                             (wi, ni,))
                if not query:
                    self.remove_from_dict(wi)

                query = self.fu_curs.execute('SELECT * FROM uForwardNet WHERE wordA=? OR next=?',
                                             (wi, ni,))
                if not query:
                    self.remove_from_dict(ni)

    def fu_removeall(self, wordA, next):
        for wi in self.search_dict(wordA):
            for ni in self.search_dict(next):
                if wi == 0:
                    return
                if ni == 0:
                    return

                self.fu_curs.execute('DELETE * from uForwardNet WHERE wordA=? AND next=?',
                                     (wi, ni,))

    def fu_print(self):
        for row in self.fu_curs.execute('SELECT * FROM uForwardNet'):
            print(row)

    def ru_search(self, wordA, prev):
        query = self.ru_curs.execute('SELECT * FROM uReverseNet WHERE wordA=? AND prev=?',
                                     (wordA, prev,))

        if query:
            count = 0
            for row in query:
                count = row[2]
            return count
        else:
            return 0

    def ru_add(self, wordA, prev):
        for wi in self.search_dict(wordA):
            for pi in self.search_dict(prev):
                if wi == 0:
                    self.add_to_dict(wordA)
                    wi = self.search_dict(wordA)[0]
                if pi == 0:
                    self.add_to_dict(prev)
                    pi = self.search_dict(prev)[0]

                count = self.ru_search(wi, pi)

                if count == 0:
                    self.ru_curs.execute('INSERT INTO uReverseNet(wordA, prev, count) VALUES (?, ?, ?)',
                                         (wi, pi, 1,))
                else:
                    self.ru_curs.execute('UPDATE uReverseNet SET count=? WHERE wordA=? AND prev=?',
                                         (count + 1, wi, pi))

    def ru_removeone(self, wordA, prev):
        for wi in self.search_dict(wordA):
            for pi in self.search_dict(prev):
                if wi == 0:
                    return
                if pi == 0:
                    return

                count = self.ru_search(wi, pi)

                if count == 0:
                    return
                if count == 1:
                    self.ru_curs.execute('DELETE * from uReverseNet WHERE wordA=? AND prev=?',
                                         (wi, pi,))
                else:
                    self.ru_curs.execute('UPDATE uReverseNet SET count=? WHERE wordA=? AND prev=?',
                                         (count - 1, wi, pi))

                # delete word if necessary
                query = self.fu_curs.execute('SELECT * FROM uReverseNet WHERE wordA=? OR prev=?',
                                             (wi, pi,))
                if not query:
                    self.remove_from_dict(wi)

                query = self.fu_curs.execute('SELECT * FROM uReverseNet WHERE wordA=? OR prev=?',
                                             (wi, pi,))
                if not query:
                    self.remove_from_dict(pi)

    def ru_removeall(self, wordA, prev):
        for wi in self.search_dict(wordA):
            for pi in self.search_dict(prev):
                if wi == 0:
                    return
                if pi == 0:
                    return

                self.ru_curs.execute('DELETE * from uReverseNet WHERE wordA=? AND prev=?',
                                     (wi, pi,))

    def ru_print(self):
        for row in self.ru_curs.execute('SELECT * FROM uReverseNet'):
            print(row)

    def add_sentence(self, sentence):
        p_sent = pa.Parser(self.brain)
        fwd = p_sent.parse_sentence(1, sentence)
        rvs = p_sent.reverse_parse_sentence(1, sentence)

        # modify network
        f_chains = fwd.split('\n')
        f_chains = f_chains[:-1]
        for c in f_chains:
            l, m, r = c.partition(p_sent.NEXT_WORD_SYMBOL)
            self.fu_add(l, r)
        r_chains = rvs.split('\n')
        r_chains = r_chains[:-1]
        for c in r_chains:
            l, m, r = c.partition(p_sent.NEXT_WORD_SYMBOL)
            self.ru_add(l, r)

        self.dictionary.commit()
        self.fu_list.commit()
        self.ru_list.commit()

    def delete_sentence(self, sentence):
        p_sent = pa.Parser(self.brain)
        fwd = p_sent.parse_sentence(1, sentence)
        rvs = p_sent.reverse_parse_sentence(1, sentence)

        # modify network
        # modify network
        f_chains = fwd.split('\n')
        f_chains = f_chains[:-1]
        for c in f_chains:
            l, m, r = c.partition(p_sent.NEXT_WORD_SYMBOL)
            self.remove_one(l, r)
        r_chains = rvs.split('\n')
        r_chains = r_chains[:-1]
        for c in r_chains:
            l, m, r = c.partition(p_sent.NEXT_WORD_SYMBOL)
            self.remove_one(l, r)

        self.dictionary.commit()
        self.fu_list.commit()
        self.ru_list.commit()

    def fu_get_next_table(self, idword):
        if not self.search_id(idword):
            raise Exception('id not found!')
        else:
            query = self.fu_curs.execute('SELECT * FROM uForwardNet WHERE wordA=?',
                                         (idword,))
            if not query:
                raise Exception('no table entries found?!')
            return query

    def print_table(self, table):
        for row in table:
            print(row)

    def sum_count(self, table):
        sum = 0
        for row in table:
            sum += row[2]
        return sum

    def u_next_word(self, word):
        idword = self.search_dict(word)[0]
        if idword > 0:
            filtered_table = self.fu_get_next_table(idword).fetchall()
            total_count = self.sum_count(filtered_table)
            rint = random.randint(1, total_count)
            for row in filtered_table:
                if rint <= row[2]:
                    next_word = self.get_word(row[1])
                    if next_word is not None:
                        return next_word
                else:
                    rint -= row[2]
        return None

    def u_random_walk(self):
        out_str = ''
        curr_word = 'initio'
        while not curr_word == 'terminus':
            curr_word = self.u_next_word(curr_word)
            if curr_word is None:
                raise Exception('FATAL ERROR: chain broken somehow')
            elif not curr_word == 'terminus':
                out_str += ' ' + curr_word
        out_str = out_str[1:]
        return out_str

    @commands.command(hidden=True)
    async def train(self, *, message: str):
        self.add_sentence(message)
        self.undo_buffer = message
        await self.bot.say('Sentence learned, to undo type !undo.')

    @commands.command(hidden=True)
    async def show(self, sarg):
        if sarg == 'dictionary':
            self.print_dict()
        if sarg == 'connections':
            self.fu_print()

    @commands.command(hidden=True)
    async def undo(self):
        self.delete_sentence(self.undo_buffer)

    @commands.command(hidden=True)
    async def talk(self):
        await self.bot.say(self.u_random_walk())

    def close_net(self):
        self.dictionary.close()
        self.fu_list.close()
        self.ru_list.close()

def setup(bot):
    bot.add_cog(MarkovNet(bot))

if __name__ == '__main__':
    mn = MarkovNet('test')
    mn.print_dict()
    mn.fu_print()
    print(mn.u_random_walk())
    mn.close_net()
