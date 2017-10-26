#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import base64
from compress import varbyte_uncompress
from compress import simple9_uncompress
from compress import from_gaps
import simple9
import varbyte
import mmh3
import pickle
from collections import defaultdict
import time


def parse_command_line():
    parser = argparse.ArgumentParser(description='compressed documents reader')
    parser.add_argument('arguments', nargs='+', help='arguments for searcher')
    return parser.parse_args()

def read_index(name_index):
    file = open("./{}".format(name_index), "r")
    encoder_method = file.readline().strip()
    index = pickle.load(file)
    url_list = pickle.load(file)
    if (encoder_method =='varbyte'):
        decoder = varbyte
        return index, url_list, decoder
    else:
        decoder = simple9
        return index, url_list, decoder


name_index = 'optimised_index'

if __name__ == "__main__":
    index, url_list, decoder_method = read_index(name_index)
    while True:
        try:
            line = raw_input()
            words = line.strip().split(u'&')
            words = [word.strip().lower() for word in words]

            result_urls = defaultdict(list)

            for word in words:
                hash = abs(mmh3.hash(word))
                #list_decode = index[hash]
                #print(list_decode)
                list_decode = decoder_method.decompress(index[hash])
                #list_decode = from_gaps(list_decode)
                result_urls[word].extend(list_decode)

            print(line)
            res_ = set(result_urls[words[0]])

            for word in words[1:]:
                res_ = res_ & set(result_urls[word])
            res_ = sorted(list(res_))

            list_res = [url_list[i] for i in res_]
            print(len(list_res))
            for item in list_res:
                print(item)
        except:
            break
