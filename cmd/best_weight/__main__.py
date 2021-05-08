# -*- coding: utf-8 -*-

import json

from app.similarity import TextSimilarity
from app.text_similarity.base import LengthException

if __name__ == '__main__':
    with open("test_data/text_similarity.json", mode="r")as f:
        test_case_list = json.load(f)

    best_weight = None
    best_acc = 0

    for i in range(0, 101):
        mode_weight = {
            "TF-IDF": i,
            "Levenshtein": 100 - i
        }

        succeed_case_num = 0
        failed_case_num = 0

        for case in test_case_list:
            try:
                actual_similarity = TextSimilarity(
                    case["text_a"],
                    case["text_b"],
                ).similarity_for_weight(mode_weight)
            except LengthException:
                continue

            expected_similarity = case["similarity"]

            for i in range(0, 6):
                if int(expected_similarity) == i:
                    if (i / 6) < actual_similarity < ((i + 1) / 6):
                        succeed_case_num += 1
                    else:
                        failed_case_num += 1

        acc = succeed_case_num / (succeed_case_num + failed_case_num)
        if acc > best_acc:
            best_acc = acc
            best_weight = mode_weight
        print(f"weight: {mode_weight}, acc: {acc}")

    print(f"best weight: {best_weight}, best acc: {best_acc}")
