from gensim.models import Word2Vec
import jieba
import numpy as np
from scipy.linalg import norm

model = Word2Vec.load('./wiki.zh.text.model')


def eachLineRemoveSymbol(str) -> str:
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

def vector_similarity(s1, s2):
    def sentence_vector(s):
        s = eachLineRemoveSymbol(s)
        words = jieba.lcut(s)
        v = np.zeros(100)
        for word in words:
            v += model.wv[word]
            # v += model[word]
        v /= len(words)
        return v

    v1, v2 = sentence_vector(s1), sentence_vector(s2)
    return np.dot(v1, v2) / (norm(v1) * norm(v2))


if __name__ == '__main__':
    print(vector_similarity("我喜欢肯德基的薯条蘸番茄酱吃，非常好吃", "我喜欢肯德基的马铃薯蘸柿子酱吃非常好吃"))
