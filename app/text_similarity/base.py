# -*- coding: utf-8 -*-


class LengthException(Exception):
    """
    长度异常
    """


class SimilarityBase:

    def __init__(self, text_a: str, text_b: str):
        """
        初始化文本相似度
        :param text_a: 对比文本 a
        :param text_b: 对比文本 b
        """
        # if len(text_a) < 10 or len(text_a) > 150:
        #     raise LengthException("len of text must between 10 and 150")
        # if len(text_b) < 10 or len(text_b) > 150:
        #     raise LengthException("len of text must between 10 and 150")
        self.text_a = text_a
        self.text_b = text_b

    def similarity(self) -> float:
        """
        获取文本相似度
        :return: 文本相似度 0 <= result <= 1
        """
        raise NotImplementedError("must implement similarity method")

    def print_similarity(self):
        """
        打印文本相似度
        :return:
        """
        print(f"text_a: {self.text_a}")
        print(f"text_b: {self.text_b}")
        print(f"similarity result: {self.similarity()}")
