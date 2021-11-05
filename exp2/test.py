#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/10/15 22:09
@Desc    :
'''

import pickle
import os
import argparse
import sys
from zutil import  *



def load_budget2scheme2result(did, method, obj, gamma):
    """Load the latest result pkl under

    :return: budget2scheme2optsolution
    :rtype: dict
    """
    budget2scheme2result = {}
    result_pkl_path_list = [d for d in os.listdir(f"../eplots/pkl{str(gamma).replace('.', '')}/") if
                            f"{did}_{method}_{obj}" in d and '.pkl' in d]
    result_pkl_path_list.sort()
    if len(result_pkl_path_list) > 0:
        budget2scheme2result = pickle.load(
            open(f"../eplots/pkl{str(gamma).replace('.', '')}/{result_pkl_path_list[-1]}", 'rb'))
    return budget2scheme2result

def example_opt_pricing():
    result_tuple = ('objI', 'objW', 'objRI', 'objRW')
    scheme2result = {(0.3, 0.3): ({0, 0}, 1, 2, 3, 4),
                     (0.6, 0.6): ({0, 0}, 6, 4, 3, 2),
                     (0.9, 0.9): ({0, 0}, 2, 3, 4, 2)}
    a = sorted(scheme2result.items(), key=lambda kv: kv[1][result_tuple.index('objRW')+1] , reverse=True)
    # kv:(首要标准, 次要标准)
    print(a)
    # [((0.3, 0.3), ({0}, 1, 2, 3, 4)), ((0.6, 0.6), ({0}, 6, 4, 3, 2)), ((0.9, 0.9), ({0}, 2, 3, 4, 2))]




if __name__ == '__main__':
    # import pandas as pd
    # df = pd.read_csv("../eplots/exp/result.csv", sep='\t')
    # print(df)
    pklsrc = get_latest_path("../eplots/pkl", "d1_2_I_brute", "pkl")
    d = pickle.load(open('../eplots/pkl/d1_2_A_brute_1105145536.pkl', 'rb'))
    print(d.keys())

    pass
    # did = 'd2'
    # method = 'brute'
    # obj = 'rev'
    # gamma = 2.0
    # # budget2scheme2result_old = load_budget2scheme2result(did, method, obj, str(gamma)+'_old')
    # budget2scheme2optsolution = load_budget2scheme2result(did, method, obj, gamma)
    # budget2scheme2result_old = load_budget2scheme2result(did, 'h1', obj, str(gamma))
    # cnt_ineq = 0
    # for budget, scheme2result in budget2scheme2optsolution.items():
    #     print(budget, '-------------------------')
    #     for scheme, result in scheme2result.items():
    #
    #
    #         result_old = budget2scheme2result_old[budget][scheme]
    #         # print(result_old)
    #         # if result != result_old:
    #         #     print(scheme)
    #         #     print(result_old)
    #         #     print(result)
    #         if result_old> result:
    #             cnt_ineq+=1
    #
    #     # print(d_old[k])
    # print(cnt_ineq)
    # pass
