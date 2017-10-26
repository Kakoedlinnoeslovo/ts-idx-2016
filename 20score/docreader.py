#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import argparse
import document_pb2
import gzip
from doc2words import extract_words
from collections import defaultdict
from codecs import open
import pickle
import cPickle
import mmh3

import struct

# Make it work for Python 2+3 and with Unicode
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

class DocumentStreamReader:
    def __init__(self, paths):
        self.paths = paths

    def open_single(self, path):
        return gzip.open(path, 'rb') if path.endswith('.gz') else open(path, 'rb')

    def __iter__(self):
        for path in self.paths:
            with self.open_single(path) as stream:
                while True:
                    sb = stream.read(4)
                    if sb == '':
                        break

                    size = struct.unpack('i', sb)[0]
                    msg = stream.read(size)
                    doc = document_pb2.document()
                    doc.ParseFromString(msg)
                    yield doc


def parse_command_line():
    parser = argparse.ArgumentParser(description='compressed documents reader')
    #parser.add_argument('method', nargs='+', help='compress method')
    parser.add_argument('files', nargs='+', help='Input files (.gz or plain) to process')
    return parser.parse_args()




if __name__ == '__main__':
    index = defaultdict(list)
    url_list = []
    doc_id = 0

    encoder_method = parse_command_line().files[0]
    reader = DocumentStreamReader(parse_command_line().files[1:])
    for doc in reader:
        all_words = extract_words(doc.text)
        uniq_words = list(set(all_words))
        url_list.append(doc.url)
        # if doc.url==u'http://lenta.ru/news/2014/04/23/usarmy/':
        #     print (doc_id)
        for word in uniq_words:
            hash = abs(mmh3.hash(word.encode("utf-8")))
            index[hash].append(doc_id)
        doc_id += 1

    print(len(index))
    #print(index[abs(mmh3.hash('сша'))])
    #print(len([url_list[i] for i in index[abs(mmh3.hash('сша'))]]))
    #print(len(index))

    file = open("./index", "w")
    file.write(encoder_method + '\n')
    pickle.dump(index, file)
    pickle.dump(url_list, file)
    file.close()
    #
    # #print("End building index")
    # #end_time = time.time()
    #print("time %.f " % (end_time - start_time), 'seconds')