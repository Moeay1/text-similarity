# -*- coding: utf-8 -*-

import json

from app.similarity import TextSimilarity
from app.text_similarity.base import LengthException

if __name__ == '__main__':
    with open("test_data/text_similarity.json", mode="r")as f:
        test_case_list = json.load(f)

    succeed_case_num = 0
    failed_case_num = 0

    for case in test_case_list:
        try:
            actual_similarity = TextSimilarity(
                case["text_a"],
                case["text_b"],
            ).similarity_for_weight(mode_weight={
                "TF-IDF": 99,
                "Levenshtein": 1
            })
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
    print("mode: [{}], ACC: {}%".format({
        "TF-IDF": 99,
        "Levenshtein": 1
    }, round(acc * 100, 4)))
