# -*- coding: utf-8 -*-

import json
from time import *

from app.similarity import TextSimilarity
from app.text_similarity.base import LengthException

if __name__ == '__main__':
    with open("test_data/text_similarity.json", mode="r")as f:
        test_case_list = json.load(f)

    succeed_case_num = 0
    failed_case_num = 0
    begin_time = time()

    for case in test_case_list:
        try:
            # actual_similarity = TextSimilarity(case["text_a"], case["text_b"]).similarity()
            # actual_similarity = TextSimilarity(
            #     case["text_a"],
            #     case["text_b"],
            # ).similarity("Levenshtein")
            # actual_similarity = TextSimilarity(
            #     case["text_a"],
            #     case["text_b"],
            # ).similarity("TF")
            actual_similarity = TextSimilarity(
                case["text_a"],
                case["text_b"],
            ).similarity("TF-IDF")
            # actual_similarity = TextSimilarity(
            #     case["text_a"],
            #     case["text_b"],
            # ).similarity("word2vec")
            # actual_similarity = TextSimilarity(
            #     case["text_a"],
            #     case["text_b"],
            # ).similarity_for_weight(mode_weight={
            #     "TF-IDF": 99,
            #     "Levenshtein": 1
            # })
        except LengthException:
            continue

        expected_similarity = case["similarity"]
        if actual_similarity > 1:
            actual_similarity = 1

        for i in range(0, 6):
            if int(expected_similarity) == i:
                if i == 0:
                    if 0 <= actual_similarity < 1 / 6:
                        succeed_case_num += 1
                    else:
                        failed_case_num += 1
                if i == 5:
                    if 5 / 6 <= actual_similarity <= 1:
                        succeed_case_num += 1
                    else:
                        failed_case_num += 1
                if 1 <= i <= 4:
                    if (i / 6) <= actual_similarity < ((i + 1) / 6):
                        succeed_case_num += 1
                    else:
                        failed_case_num += 1

    acc = succeed_case_num / (succeed_case_num + failed_case_num)
    print("acc", acc)
    print(succeed_case_num + failed_case_num)
    end_time = time()
    run_time = end_time - begin_time
    print(run_time)
