# -*- coding: utf-8 -*-

import os


class SimilarityBase:

    def __init__(self, file_a: str, file_b: str):
        """
        初始化文本相似度
        :param file_a: 文本文件 a 路径
        :param file_b: 文本文件 b 路径
        """
        text_a = ""
        text_b = ""
        if not os.path.isfile(file_a):
            raise ValueError(file_a, "is not file")
        elif not os.path.isfile(file_b):
            raise ValueError(file_a, "is not file")
        else:
            with open(file_a, 'r') as f:
                for line in f.readlines():
                    text_a += line.strip()
            with open(file_b, 'r') as f:
                for line in f.readlines():
                    text_b += line.strip()
        self.text_a = text_a
        self.text_b = text_b

    def similarity(self) -> float:
        """
        获取文本相似度
        :return: 文本相似度 0 <= result <= 1
        """
        raise NotImplementedError("must implement similarity method")

    def print_similarity(self):
        """
        打印文本相似度
        :return:
        """
        print(f"text_a: {self.text_a}")
        print(f"text_b: {self.text_b}")
        print(f"similarity result: {self.similarity()}")
