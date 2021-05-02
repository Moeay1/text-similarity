# -*- coding: utf-8 -*-


def distance(text_a: str, text_b: str) -> int:
    """
    计算 两个文本的莱温斯坦距离
    :param text_a: 文本 a
    :param text_b: 文本 b
    :return: 计算两个文本的莱温斯坦距离
    """
    min_matrix = [[0]]
    for i in range(len(text_a)):
        min_matrix[0].append(i + 1)
    for j in range(len(text_b)):
        min_matrix.append([j + 1])
    for i in range(1, len(text_b) + 1):
        for j in range(1, len(text_a) + 1):
            if text_a[j - 1] == text_b[i - 1]:
                min_step = min_matrix[i - 1][j - 1]
            else:
                min_step = 1 + min(min_matrix[i - 1][j - 1], min_matrix[i][j - 1], min_matrix[i - 1][j])
            min_matrix[i].append(min_step)
    return min_matrix[-1][-1]
