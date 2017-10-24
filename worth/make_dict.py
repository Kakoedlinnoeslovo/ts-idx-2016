#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import pickle
from compress import to_gaps
from compress import varbyte_compress
import mmh3

def read_index(name_index):
    file = open("./{}".format(name_index), "r")
    encoder_method = file.readline()
    # if (encoder_method[:-1]=='varbyte' and i ==0):
    #     encoder = varbyte
    # elif (encoder_method[:-1] == 'simple9' and i==0):
    #     encoder = simple9
    index = pickle.load(file)
    url_list = pickle.load(file)
    return index, url_list


name_index = 'index'

if __name__  == '__main__':
    #SIMPLE REALISATION: JUST SORTED
    #print('Start building dictionary and optimisation')

    index, url_list = read_index(name_index)

    #print([url_list[i] for i in index[abs(mmh3.hash('сша'))]])

    for hash in index.keys():
        #gaps = to_gaps(index[hash])
        index[hash] = sorted(index[hash], reverse=False)
        #varbyte_gaps = varbyte_compress(sorted_gaps)
        #index[hash] = base64.b64encode(varbyte_gaps)

    encoder_method = "varbyte"

    file = open("./optimised_index", "w")
    file.write(encoder_method + '\n')
    pickle.dump(index, file)
    pickle.dump(url_list, file)
    file.close()
