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
    similarity = Levenshtein("这件事办了很长时间，还没有办成", "锁管机暂时没有中国国家标准")
    similarity.print_similarity()
