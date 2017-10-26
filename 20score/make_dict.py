#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import pickle
from compress import to_gaps
from compress import varbyte_compress
from compress import simple9_compress

import simple9
import varbyte


def read_index(name_index):
    file = open("./{}".format(name_index), "r")
    encoder_method = file.readline().strip()
    index = pickle.load(file)
    url_list = pickle.load(file)
    if (encoder_method=='varbyte'):
         encoder = varbyte
         encoder_str = 'varbyte'
         return index, url_list, encoder, encoder_str
    else:
        encoder = simple9
        encoder_str= 'simple9'
        return index, url_list, encoder, encoder_str

name_index = 'index'

if __name__  == '__main__':
    #SIMPLE REALISATION: JUST SORTED
    #print('Start building dictionary and optimisation')

    index, url_list, encoder_method, encoder_str = read_index(name_index)

    #print(len([url_list[i] for i in index[abs(mmh3.hash('сша'))]]))
    for hash in index.keys():
        #gaps = to_gaps(index[hash])
        sorted_gaps = sorted(index[hash], reverse=False)
        compress_gaps = encoder_method.compress(sorted_gaps)
        index[hash] = compress_gaps


    file = open("./optimised_index", "w")
    file.write(encoder_str + '\n')
    pickle.dump(index, file)
    pickle.dump(url_list, file)
    file.close()
