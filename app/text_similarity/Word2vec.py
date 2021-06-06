import json

import gensim.models
from gensim.models import Word2Vec
import jieba
import numpy as np
from scipy.linalg import norm
import jieba.analyse

from app.text_similarity.base import SimilarityBase, LengthException
from app.text_similarity.levenshtein import Levenshtein
from app.text_similarity.tf_idf import TFIDF

from time import *


class Word2vec(SimilarityBase):
    model = Word2Vec.load('/Users/bytedance/Documents/textSimilarity/text-similarity/data/wiki.zh.text.model')
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
        return self.tfidf(self.text_a, self.text_b)

    def tfidf(self, a, b):
        self.failed = 0
        def sentence_vector(s):
            tups = jieba.analyse.extract_tags(s, topK=100, withWeight=True, allowPOS=())
            numtups = len(tups)
            i = 0
            word_xweight = 0
            while i < numtups:  # 遍历每一个关键词 i是关键词数
                word = tups[i][0]
                weight = tups[i][1]
                try:
                    tryw2v = self.model.wv[word]
                except KeyError:
                    self.failed = 1
                    break
                word_xweight = word_xweight + (weight * tryw2v)
                i = i + 1
            try:
                sentence_w2v = word_xweight / numtups

            except ZeroDivisionError:
                sentence_w2v = 0
                self.failed = 1
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
        if (norm(v1) * norm(v2)) == 0.0:
            return tfidf
        sim = np.dot(v1, v2) / (norm(v1) * norm(v2))

        if sim > 1:
            return 1
        if sim < 0:
            return 0
        return sim * 0.06 + tfidf * 0.94


def testWord2vec() -> float:
    with open("test_data/text_similarity.json", mode="r")as f:
        test_case_list = json.load(f)

    succeed_case_num = 0
    failed_case_num = 0

    for case in test_case_list:
        try:
            actual_similarity = Word2vec(case["text_a"], case["text_b"]).similarity()
        except LengthException:
            continue
        lacc = False
        expected_similarity = case["similarity"]

        for i in range(0, 6):
            if int(expected_similarity) == i:
                if i == 0:
                    if 0 <= actual_similarity < ((i + 1) / 6):
                        succeed_case_num += 1
                        lacc = True
                    else:
                        failed_case_num += 1
                if i == 5:
                    if (i / 6) <= actual_similarity <= 1:
                        succeed_case_num += 1
                        lacc = True
                    else:
                        failed_case_num += 1
                if 1 <= i <= 4:
                    if (i / 6) <= actual_similarity <= ((i + 1) / 6):
                        succeed_case_num += 1
                        lacc = True
                    else:
                        failed_case_num += 1
                if lacc == True:
                    print(case["text_a"])
                    print(case["text_b"])
                    print(actual_similarity)
                lacc = False

    acc = succeed_case_num / (succeed_case_num + failed_case_num)
    print("acc", acc)
    return acc

if __name__ == '__main__':
    # s1 = "他没努力去解决这个问题，这个问题对他来说很容易。"
    # s2 = "他没努力去解决这个问题，这个问题对他本来就很容易。"
    # word2vec = Word2vec(s1, s2)
    # word2vec.print_similarity()
    # w = 0.01
    # bw = 0
    # bestacc = 0.0
    # while w <= 1:
    #     acc = testWord2vec(w)
    #     if acc > bestacc:
    #         bestacc = acc
    #         bw = w
    #     print(w, "     ", acc)
    #     w += 0.01
    testWord2vec()