# -*- coding: utf-8 -*-

"""
TF-IDF 计算文本相似度
"""

from typing import Dict

from jieba import analyse

from app.text_similarity.base import SimilarityBase
from app.utils.cos import cos


class TFIDF(SimilarityBase):

    @staticmethod
    def get_word_to_tf_idf(text: str) -> Dict[str, float]:
        """
        获取文本 TF-IDF
        :param text: 文本
        :return:
        """
        tf_idf_func = analyse.extract_tags
        keywords = tf_idf_func(text, topK=None, withWeight=True)
        ans = {}
        for keyword in keywords:
            ans[keyword[0]] = keyword[1]
        return ans

    def similarity(self) -> float:
        """
        获取文本相似度
        :return: 文本相似度 0 <= result <= 1
        """

        # 计算文本的 tf-idf
        word_to_tf_idf_a = self.get_word_to_tf_idf(self.text_a)
        word_to_tf_idf_b = self.get_word_to_tf_idf(self.text_b)

        # 获取次品统计并集
        union_word_set = set(word_to_tf_idf_a.keys()) | set(word_to_tf_idf_b.keys())

        # 将词频转为向量并得到向量夹角的余弦值
        vec_a = []
        vec_b = []
        for word in union_word_set:
            vec_a.append(word_to_tf_idf_a.get(word, 0))
            vec_b.append(word_to_tf_idf_b.get(word, 0))
        sim = cos(vec_a, vec_b)
        if sim > 1:
            sim = 1
        return sim


if __name__ == '__main__':
    # s1 = "这件事办了很长时间，还没有办成"
    # s2 = "锁管机暂时没有中国国家标准"
    # s1 = "北京是中国的首都，是一个美丽的城市"
    # s2 = "华盛顿是美国的首都，是一个繁华的城市"
    # s1 = "我喜欢吃番茄"
    # s2 = "我喜欢吃西红柿"
    s1 = "今天天气很糟糕"
    s2 = "今天天气很晴朗"
    similarity = TFIDF(s1, s2)
    similarity.print_similarity()
