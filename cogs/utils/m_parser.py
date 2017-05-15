import re
from enums import e_modify as mo

class Parser:
    WORD_BREAK_SYMBOL = '^'
    NEXT_WORD_SYMBOL = '$'

    def __init__(self, brain,
                 sentence_split_char='\n', word_split_char=' '):
        self.brain = brain
        self.sentence_split_char = sentence_split_char
        self.word_split_char = word_split_char
        self.whitespace_regex = re.compile('\s+')
        self.content = ''

    def parse_word(self, word):
        extremities = True
        exc_count = 0
        que_count = 0
        while extremities:
            if word[-1:] == '!':


    def parse_sentence(self, depth, sentence):
        sent = sentence.split(self.word_split_char)
        line = ''
        if len(sent) > depth:
            for w in range(len(sent) + depth):
                for d in range(depth):
                    if w + d < depth:
                        line += 'initio' + self.WORD_BREAK_SYMBOL
                    elif w + d >= len(sent) + depth:
                        line += 'terminus' + self.WORD_BREAK_SYMBOL
                    else:
                        if sent[w + d - depth].lower() == "i":
                            line += "I" + self.WORD_BREAK_SYMBOL
                        else:
                            line += (parse_word(sent[w + d - depth].lower())
                                + self.WORD_BREAK_SYMBOL)
                line = line[:-1]
                if w >= len(sent):
                    line += self.NEXT_WORD_SYMBOL + 'terminus' + '\n'
                else:
                    if sent[w].lower() == "i":
                        line += self.NEXT_WORD_SYMBOL + "I" + '\n'
                    else:
                        line += (self.NEXT_WORD_SYMBOL +
                                 sent[w].lower() + '\n')
        return {'parsed': line, 'mod': mod}

    def reverse_parse_sentence(self, depth, sentence):
        sent = sentence.split(self.word_split_char)
        sent.reverse()
        line = ''
        if len(sent) > depth:
            for w in range(len(sent) + depth):
                for d in range(depth):
                    if w + d < depth:
                        line += 'terminus' + self.WORD_BREAK_SYMBOL
                    elif w + d >= len(sent) + depth:
                        line += 'initio' + self.WORD_BREAK_SYMBOL
                    else:
                        if sent[w + d - depth].lower() == "i":
                            line += "I" + self.WORD_BREAK_SYMBOL
                        else:
                            line += (sent[w + d - depth].lower() +
                                     self.WORD_BREAK_SYMBOL)
                line = line[:-1]
                if w >= len(sent):
                    line += self.NEXT_WORD_SYMBOL + 'initio' + '\n'
                else:
                    if sent[w].lower() == "i":
                        line += self.NEXT_WORD_SYMBOL + "I" + '\n'
                    else:
                        line += (self.NEXT_WORD_SYMBOL +
                                 sent[w].lower() + '\n')
        return {'parsed': line, 'mod': mod}
