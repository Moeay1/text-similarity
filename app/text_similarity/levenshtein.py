# -*- coding: utf-8 -*-

"""
莱温斯坦距离 计算文本相似度
"""

from app.text_similarity.base import SimilarityBase
from app.utils.levenshtein import distance


class Levenshtein(SimilarityBase):

    def similarity(self) -> float:
        """
        获取文本相似度
        :return: 文本相似度 0 <= result <= 1
        """

        max_length = max(len(self.text_a), len(self.text_b))
        return (max_length - float(distance(self.text_a, self.text_b))) / max_length


if __name__ == '__main__':
    similarity = Levenshtein("data/a.txt", "data/b.txt")
    similarity.print_similarity()
