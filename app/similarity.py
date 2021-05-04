# -*- coding: utf-8 -*-

import os
from typing import Dict

from app.text_similarity.tf import TF
from app.text_similarity.tf_idf import TFIDF
from app.text_similarity.levenshtein import Levenshtein

SIMILARITY_MODE = {
    "TF": TF,
    "TF-IDF": TFIDF,
    "Levenshtein": Levenshtein,
}


class TextSimilarity:
    """
    文档相似度
    """

    def __init__(self, text_a: str, text_b: str):
        """
        构造函数
        :param text_a: 对比文档 a
        :param text_b: 对比文档 b
        """
        self.text_a = text_a
        self.text_b = text_b

    def set_text_from_file(self, file_a: str, file_b: str):
        """
        根据文件设置对比文本
        :param file_a: 对比文档 a 路径
        :param file_b: 对比文档 b 路径
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

    def similarity(self, mode: str) -> float:
        """
        计算文本相似度
        :param mode: 对比模式
        :return: 文本相似度 0 <= result <= 1
        """

        if mode not in SIMILARITY_MODE.keys():
            raise ValueError("not support this mode: {}".format(mode))

        return SIMILARITY_MODE[mode](self.text_a, self.text_b).similarity()

    def similarity_for_weight(self, mode_weight: Dict[str, int]) -> float:
        """
        添加权重计算文本相似度
        :param mode_weight: 对比模式及权重 满权重 100
        :return: 文本相似度 0 <= result <= 1
        """

        similarity = 0
        for mode, weight in mode_weight:
            if mode not in SIMILARITY_MODE.keys():
                raise ValueError("not support this mode: {}".format(mode))
            similarity += SIMILARITY_MODE[mode](self.text_a, self.text_b).similarity()
        return similarity
