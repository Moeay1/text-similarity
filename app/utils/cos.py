# -*- coding: utf-8 -*-

from typing import List

import numpy as np


def cos(vec_a: List[float], vec_b: List[float]) -> float:
    """
    计算两个向量的夹角的余弦值
    :param vec_a:
    :param vec_b:
    :return:
    """
    if len(vec_a) != len(vec_b):
        raise ValueError("len of vec_a and len of vec_b must equal")

    if not vec_a and not vec_b:
        return 0

    a = np.array(vec_a)
    b = np.array(vec_b)
    if np.sum(a * b) == 0:
        return 0
    return np.sum(a * b) / (np.sqrt(np.sum(a ** 2)) * np.sqrt(np.sum(b ** 2)))
