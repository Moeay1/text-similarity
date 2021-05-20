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
            actual_similarity = TextSimilarity(
                case["text_a"],
                case["text_b"],
            ).similarity_for_weight(mode_weight={
                "TF-IDF": 99,
                "Levenshtein": 1
            })
            # actual_similarity = TextSimilarity(
            #     case["text_a"],
            #     case["text_b"],
            # ).similarity("Levenshtein")
            # actual_similarity = TextSimilarity(
            #     case["text_a"],
            #     case["text_b"],
            # ).similarity("TF")
            # actual_similarity = TextSimilarity(
            #      case["text_a"],
            #      case["text_b"],
            # ).similarity("TF-IDF")
        except LengthException:
            continue
        lacc = False
        tacc = False
        expected_similarity = case["similarity"]
        if actual_similarity > 1:
            actual_similarity = 1

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
                if expected_similarity > 3:
                    print(case["text_a"])
                    print(case["text_b"])
                    print(actual_similarity)


    acc = succeed_case_num / (succeed_case_num + failed_case_num)
    print("mode: [{}], ACC: {}%".format({
        "TF-IDF": 99,
        "Levenshtein": 1
    }, round(acc * 100, 4)))
    end_time = time()
    run_time = end_time - begin_time
    print(run_time)