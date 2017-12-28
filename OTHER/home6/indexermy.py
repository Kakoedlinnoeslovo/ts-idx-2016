# -*- coding: utf-8 -*-
from collections import Counter


class Indexer:
    def __init__(self):
        self.dictionary = dict()
        self.counter_words = Counter()
        self.lev_save = dict(dict())

    def reader(self):
        file_open = open("queries_all.txt", "r")
        for line in file_open:
            line_after  = line.strip().decode('utf-8').lower()
            if line_after.find('\t') > 0:
                left_side, right_side = line_after.split('\t')
                for a,b in zip(left_side, right_side):
                    result = self.levinstein(a,b)
                    self.lev_save[a] = {b:result}
                self.counterWords[word] += 1


            for word in line_after:
                self.counterWords[word] +=1

    def levinstein(self, w1, w2):
        if not w1: return len(w2)
        if not w2: return len(w1)
        return min(self.levinstein(w1[1:], w2[1:]) + (w1[0]!=w2[0]), self.lelinstein(w1[1:], w2)+1, self.levinstein(w1, w2[1:])+1)

if __name__ == "__main__":
    query = Indexer()
    query.reader()