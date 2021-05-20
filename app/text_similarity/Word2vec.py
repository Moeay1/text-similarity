import json

import gensim.models
from gensim.models import Word2Vec
import jieba
import numpy as np
from scipy.linalg import norm
import jieba.analyse

from app.text_similarity.base import SimilarityBase
from app.text_similarity.levenshtein import Levenshtein
from app.text_similarity.tf_idf import TFIDF

from time import *


class Word2vec(SimilarityBase):
    model = Word2Vec.load('./data/wiki.zh.text.model')
    # model = gensim.models.KeyedVectors.load_word2vec_format("./data/sgns.target.word-word.dynwin5.thr10.neg5.dim300.iter5")
    failed = 0

    def eachLineRemoveSymbol(self, str) -> str:
        strline = str.strip() \
            .replace('。', '').strip(':').strip('.').strip(';').replace(' ', '').replace('\t', '').replace('\u3000',
                                                                                                          '').replace(
            '<', '').replace('>', '').replace('(', '') \
            .replace(')', '').replace('?', '').replace('，', '').replace('　　　　　', '') \
            .replace('：', '').replace('　', '').replace('“', '').replace('”', '').replace('.', '').replace('、',
                                                                                                          '').replace(
            '》', '').replace('《', '') \
            .replace('（', '').replace('）', '').replace(']', '').replace('[', '').replace('］', '').replace('［',
                                                                                                          '').replace(
            '；', '')
        return strline

    def vector_similarity(self, s1, s2) -> float:
        def sentence_vector(s):
            s = self.eachLineRemoveSymbol(s)
            words = jieba.lcut(s)
            v = np.zeros(100)
            for word in words:
                try:
                    k = self.model.wv[word]
                except KeyError:
                    k = np.zeros(100)
                v += k

            v /= len(words)
            return v

        v1, v2 = sentence_vector(s1), sentence_vector(s2)
        if v1 == np.zeros(100) | v2 == np.zeros(100):
            return 100
        sim = np.dot(v1, v2) / (norm(v1) * norm(v2))
        if sim > 1:
            return 1
        return sim

    def similarity(self) -> float:
        # return self.vector_similarity(self.text_a, self.text_b)
        # return self.tfidf(self.text_a, self.text_b)
        return self.tfidf(self.text_a, self.text_b)

    def tfidf(self, a, b):
        def sentence_vector(s):
            # s = self.eachLineRemoveSymbol(s)
            tups = jieba.analyse.extract_tags(s, topK=100, withWeight=True, allowPOS=())
            numtups = len(tups)
            i = 0
            word_xweight = 0
            sentence_w2v = 0
            while i < numtups:  # 遍历每一个关键词 i是关键词数
                word = tups[i][0]
                weight = tups[i][1]
                try:
                    tryw2v = self.model.wv[word]
                except KeyError:
                    tryw2v = np.zeros(100)

                word_xweight = word_xweight + (weight * tryw2v)
                i = i + 1
            try:
                sentence_w2v = word_xweight / numtups

            except ZeroDivisionError:
                sentence_w2v = 0
                self.failed = 1
                # print("该文件没有内容")
            if numtups == 0:
                self.failed = 1

            return sentence_w2v

        v1 = sentence_vector(a)
        v2 = sentence_vector(b)
        l = Levenshtein(a, b)
        t = TFIDF(a, b)
        tfidf = l.similarity() * 0.01 + t.similarity() * 0.99
        if self.failed == 1:
            return tfidf
        sim = np.dot(v1, v2) / (norm(v1) * norm(v2))
        if sim > 1:
            return 1
        return 0.96 * sim + 0.04 * tfidf



if __name__ == '__main__':
    s1 = "北京是中国的首都，是一个美丽的城市"
    s2 = "华盛顿是美国的首都，是一个繁华的城市"
    word2vec = Word2vec(s1, s2)
    word2vec.print_similarity()

