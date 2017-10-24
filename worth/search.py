#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import base64
from make_dict import read_index
from compress import varbyte_uncompress
from compress import from_gaps
import mmh3
from collections import defaultdict
import time


def parse_command_line():
    parser = argparse.ArgumentParser(description='compressed documents reader')
    parser.add_argument('arguments', nargs='+', help='arguments for searcher')
    return parser.parse_args()


name_index = 'optimised_index'

if __name__ == "__main__":
    while True:
        try:
            line = raw_input()
            words = line.strip().split(u'&')
            words = [word.strip().lower() for word in words]

            index, url_list = read_index(name_index)

            result_urls = defaultdict(list)

            for word in words:
                hash = abs(mmh3.hash(word))
                list_decode = index[hash]
                #print(list_decode)
                # list_decode = base64.b64decode(index[hash])
                # list_decode = varbyte_uncompress(list_decode)
                # list_decode = from_gaps(list_decode)
                result_urls[word].extend(list_decode)

            print(line)
            res_ = set(result_urls[words[0]])
            for word in words[1:]:
                res_ = sorted(res_ & set(result_urls[word]))
            list_res = [url_list[i] for i in res_]
            print(len(list_res))
            for item in list_res:

                print(item)
        except:
            break
