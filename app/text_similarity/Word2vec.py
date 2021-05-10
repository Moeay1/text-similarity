import gensim.models
from gensim.models import Word2Vec
import jieba
import numpy as np
from scipy.linalg import norm
import jieba.analyse

from app.text_similarity.base import SimilarityBase


class Word2vec(SimilarityBase):
    model = Word2Vec.load('app/word2vec/wiki.zh.text.model')
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
        print(strline)
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
        return np.dot(v1, v2) / (norm(v1) * norm(v2))

    def similarity(self) -> float:
        #return self.vector_similarity(self.text_a, self.text_b)
        return self.tfidf(self.text_a, self.text_b)

    def tfidf(self, a, b):
        if a == "这次我只考了80分，你呢？":
            print("jjjj")
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
                    print("该文件没有内容")
            if numtups == 0:
                self.failed = 1

            return sentence_w2v
        v1 = sentence_vector(a)
        v2 = sentence_vector(b)

        if self.failed == 1:
            return -1

        return np.dot(v1, v2) / (norm(v1) * norm(v2))


if __name__ == '__main__':
    s1 = "这次我只考了80分，你呢?"
    s2 = "桥本再度推测，这种丝很可能让鬼魂由能量状态实体化，进而达到与生物接触的效果。"
    word2vec = Word2vec(s1, s2)
    # import datetime
    #
    # starttime = datetime.datetime.now()
    #
    # # long running
    #
    # endtime = datetime.datetime.now()
    #
    # print(endtime - starttime).seconds
    word2vec.print_similarity()
