# -*- coding: utf-8 -*-

"""
TF 计算文本相似度
"""

from typing import Dict
from collections import Counter

import jieba

from app.text_similarity.base import SimilarityBase
from app.utils.cos import cos


class TF(SimilarityBase):

    @staticmethod
    def get_word_to_count(text: str) -> Dict[str, float]:
        """
        获取文本 TF
        :param text: 文本
        :return:
        """
        word_list = jieba.cut(text)
        return Counter(word_list)

    def similarity(self) -> float:
        """
        获取文本相似度
        :return: 文本相似度 0 <= result <= 1
        """

        # 计算文本的词频
        word_to_count_a = self.get_word_to_count(self.text_a)
        word_to_count_b = self.get_word_to_count(self.text_b)

        # 获取次品统计并集
        union_word_set = set(word_to_count_a.keys()) | set(word_to_count_b.keys())

        # 将词频转为向量并得到向量夹角的余弦值
        vec_a = []
        vec_b = []
        for word in union_word_set:
            vec_a.append(word_to_count_a.get(word, 0))
            vec_b.append(word_to_count_b.get(word, 0))
        return cos(vec_a, vec_b)


if __name__ == '__main__':
    similarity = TF("data/a.txt", "data/b.txt")
    similarity.print_similarity()
