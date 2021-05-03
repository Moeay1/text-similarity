# -*- coding: utf-8 -*-

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

    def __init__(self, file_a: str, file_b: str):
        """
        构造函数
        :param file_a: 对比文档 a 路径
        :param file_b: 对比文档 b 路径
        """
        self.file_a = file_a
        self.file_b = file_b

    def similarity(self, mode: str) -> float:
        """
        计算文本相似度
        :param mode: 对比模式
        :return: 文本相似度 0 <= result <= 1
        """

        if mode not in SIMILARITY_MODE.keys():
            raise ValueError("not support this mode: {}".format(mode))

        return SIMILARITY_MODE[mode](self.file_a, self.file_b).similarity()
