# -*- coding: utf-8 -*-

import os

from app.similarity import SIMILARITY_MODE
from app.similarity import TextSimilarity

if __name__ == '__main__':
    mode = input("please input a compare mode ({}): ".format(list(SIMILARITY_MODE.keys())))
    while mode not in SIMILARITY_MODE.keys():
        print("please input a compare mode ({}): ".format(mode))
        mode = input("please input a compare mode: ({})".format(SIMILARITY_MODE.keys()))

    file_a = input("please input file_a path (like: ./data/a.txt):")
    while not os.path.isfile(file_a):
        print("{} is not a file".format(file_a))
        file_a = input("please input file_a path (like: ./data/a.txt):")

    file_b = input("please input file_b path (like: ./data/b.txt): ")
    while not os.path.isfile(file_b):
        print("{} is not a file".format(file_b))
        file_b = input("please input file_b path (like: ./data/a.txt): ")

    similarity = TextSimilarity(file_a, file_b).similarity(mode)
    print("similarity: {}%".format(round(similarity * 100, 2)))
