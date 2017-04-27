import os
import errno
import sqlite3
from discord.ext import commands


class Learner(object):
    ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
    DATA_DIR = os.path.join(ROOT_DIR, 'data')

    def __init__(self, bot):
        self.bot = bot
        self.brain = 'test'

        self.dictionary = sqlite3.connect(os.path.join(Learner.DATA_DIR, self.brain + '_dict.db'))
        self.synonyms = sqlite3.connect(os.path.join(Learner.DATA_DIR, 'snym.db'))
        self.antonyms = sqlite3.connect(os.path.join(Learner.DATA_DIR, 'anym.db'))
        self.relations = sqlite3.connect(os.path.join(Learner.DATA_DIR, 'relations.db'))
        self.physvec = sqlite3.connect(os.path.join(Learner.DATA_DIR, 'physvec.db'))
        self.abstvec = sqlite3.connect(os.path.join(Learner.DATA_DIR, 'abstvec.db'))

        self.dt_curs = self.dictionary.cursor()
        self.sn_curs = self.dictionary.cursor()
        self.an_curs = self.dictionary.cursor()
        self.re_curs = self.dictionary.cursor()
        self.pv_curs = self.dictionary.cursor()
        self.av_curs = self.dictionary.cursor()

        # dictionary initialized externally, but to keep things modular, create if non-existent
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
        self.sn_curs.execute('''
                             CREATE TABLE IF NOT EXISTS synonyms(
                                word INTEGER,
                                sywd INTEGER,
                                bond INTEGER,
                                FOREIGN KEY(word) REFERENCES dictionary(wID),
                                FOREIGN KEY(sywd) REFERENCES dictionary(wID)
                             )
                             ''')
        self.an_curs.execute('''
                             CREATE TABLE IF NOT EXISTS antonyms(
                                word INTEGER,
                                anwd INTEGER,
                                bond INTEGER,
                                FOREIGN KEY(word) REFERENCES dictionary(wID),
                                FOREIGN KEY(anwd) REFERENCES dictionary(wID)
                             )
                             ''')
        self.re_curs.execute('''
                             CREATE TABLE IF NOT EXISTS relations(
                                word INTEGER,
                                parent INTEGER,
                                child INTEGER,
                                branch INTEGER,
                                FOREIGN KEY(word) REFERENCES dictionary(wID)
                             )
                             ''')
        self.pv_curs.execute('''
                             CREATE TABLE IF NOT EXISTS physvector(
                                word INTEGER,
                                touch INTEGER,
                                sight INTEGER,
                                smell INTEGER,
                                sound INTEGER,
                                texture INTEGER,
                                FOREIGN KEY(word) REFERENCES dictionary(wID)
                             )
                             ''')
        self.av_curs.execute('''
                             CREATE TABLE IF NOT EXISTS abstvector(
                                word INTEGER,
                                sentience INTEGER,
                                sentiment INTEGER,
                                FOREIGN KEY(word) REFERENCES dictionary(wID)
                             )
                              ''')

    def search_dict(self, word):
        query = self.dt_curs.execute('SELECT * FROM dictionary WHERE word=?',
                                     (word,))
        d_list = query.fetchall()
        if d_list:
            d_id = []
            for row in d_list:
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
        #print("adding to dictionary", word)
        self.dt_curs.execute('INSERT INTO dictionary(word) VALUES (?)',
                             (word,))
        self.print_dict()
        self.dictionary.commit()

    def remove_from_dict(self, wid):
        self.dt_curs.execute('DELETE * FROM dictionary WHERE wID=?',
                             (wid,))

    def print_dict(self):
        self.dt_curs.execute('SELECT * FROM dictionary LIMIT 1')
        if self.dt_curs.fetchone() == None:
            print("Dictionary is empty")
        for row in self.dt_curs.execute('SELECT * FROM dictionary ORDER BY wID'):
            print(row)

if __name__ == '__main__':
    l = Learner("test")
