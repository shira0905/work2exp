#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/9/2 20:37
@Desc    :
"""

import itertools
import pickle
import datetime
from noperator import Noperator
import pandas as pd
from zutil import get_latest_path

class BruteOperator(Noperator):
    """The class of an operator aim to maximize revenue"""

    def __init__(self, logger, network, obj, budget_list, grain):
        self.method = 'brute'
        Noperator.__init__(self, logger, network, obj, budget_list, grain)
        self.budgets2schemes2combs2result = self.load_budgets2schemes2combs2result()  # 还没有想好怎么基于之前的结果搜索, 不需要把



    def opt_price_objs(self):
        """
        Need: self.budgets2schemes2combs2result
        retuen the opt scheme for all 4 objs (4 rows),
        align API of self.row_list
        """
        self.compute_budgets2schemes2combs2result_pkl()
        # self.transfor_budgets2schemes2combs2result_csv()
        for obj in self.OBJS:
            budget2scheme2optsolution = {}
            for budget, scheme2comb2result in self.budgets2schemes2combs2result.items():
                scheme2optsolution = {}
                for scheme, comb2result in scheme2comb2result.items():
                    sorted_comb2result = sorted(comb2result.items(), key=lambda kv: kv[1][self.OBJS.index(obj)], reverse=True)
                    # print(len(comb2result.keys()), sorted_comb2result[0][0], sorted_comb2result[0][1])
                    # setM_star, obj_star = sorted_comb2result[0][0], sorted_comb2result[0][1][self.OBJS.index(obj)]
                    scheme2optsolution[scheme] = (sorted_comb2result[0][0], *sorted_comb2result[0][1])
                budget2scheme2optsolution[budget] = scheme2optsolution
            prefix = f"{self.network.did}_{int(self.network.lamb)}_{obj}_{self.method}"
            nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
            result_pkl_path = f"{self.PKL_DIR}/{prefix}_{nowTime}.pkl"
            pickle.dump(budget2scheme2optsolution, open(result_pkl_path, 'wb'))


    def compute_budgets2schemes2combs2result_pkl(self):
        """ override parent
        (1) set self.budgets2schemes2combs2result
        (2) dump pkl
        """
        for budget in self.budget_list:
            self.logger.info(f"{'='*30} {self.network.did}_{int(self.network.lamb)}_A_{self.method}  b={budget}")
            if budget in self.budgets2schemes2combs2result.keys():
                self.logger.info('done load')
            else:
                self.budgets2schemes2combs2result[budget] = {}
                # STEP1: compute and record for all (p,q) # 给定 did, lamb, obj, method, 给定 budget, 这个方法只是记录了所有搜索到的scheme,
                for (p, q) in self.pq_list:  # 里面的循环是algorithm 1了
                    tilderR, tilderS = self.get_tilderR_tilderS(p, q)
                    comb_list = list(itertools.combinations(tilderS, budget))
                    combs2result = {}
                    for i, comb in enumerate(comb_list):
                        combs2result[comb] = self.compute_obj4(comb, tilderR, p, q)
                    self.budgets2schemes2combs2result[budget][(p, q)] = combs2result
        self.dump_budgets2schemes2combs2result()





    def load_budgets2schemes2combs2result(self):
        budgets2schemes2combs2result = {}
        # self.PKL_PREFIX = f"{self.network.did}_{int(self.network.lamb)}_{self.obj}_{self.method}"
        prefix =  f"{self.network.did}_{int(self.network.lamb)}_A_{self.method}"
        pklsrc = get_latest_path(self.PKL_DIR, prefix, 'pkl')
        if pklsrc != None:
            budgets2schemes2combs2result = pickle.load(open(pklsrc, 'rb'))
        return budgets2schemes2combs2result


    def search_budgets2schemes2combs2result(self, budget, tilderR, tilderS):
        """Search if given tilderR, tilderS has been computed in history.

        :return: result=(suppliers M, increase I, revenue R) in dictionary budget2scheme2optsolution with legal key
        :rtype: (set(), int, float)
        """
        # if budget not in self.budgets2schemes2combs2result.keys():
        #     return None
        # scheme2comb2result = self.budgets2schemes2combs2result[budget]
        # for scheme, comb2result in scheme2comb2result.items():
        #     p, q = scheme
        #     tilderR_history, tilderS_history = self.get_tilderR_tilderS(p, q)
        #     if tilderR_history == tilderR and tilderS_history == tilderS:
        #         return comb2result
        # return None
        pass

    def dump_budgets2schemes2combs2result(self):
        """Dump the result pkl with cur_time.

        :return: None
        :rtype: None
        """
        nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
        result_pkl_path = f"{self.PKL_DIR}/{self.PKL_PREFIX}_{nowTime}.pkl"
        # result_pkl_path = f"{self.PKL_DIR}/{self.PKL_PREFIX}.pkl"
        pickle.dump(self.budgets2schemes2combs2result, open(result_pkl_path, 'wb'))



    # def dump_budgets2schemes2combs2result(self):
    #     """Dump the result pkl with cur_time.
    #
    #     :return: None
    #     :rtype: None
    #     """
    #     nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
    #     prefix = f"{self.network.did}_{int(self.network.lamb)}_A_{self.method}"
    #     result_pkl_path = f"{self.PKL_DIR}/{prefix}_{nowTime}.pkl"
    #     pickle.dump(self.budgets2schemes2combs2result, open(result_pkl_path, 'wb'))




#####################################################

    def get_M_star(self, budget, tilderR, tilderS, p, q):
        """Get ground truth opt participating suppliers star_M by brute-force method and incr_R R(star_M)

        :return: optimal supplier set star_M, corresponding visibility increase of suppliers incr_R
        :rtype: set(), int
        """
        if len(tilderS) <= budget:
            return tilderS

        comb_list = list(itertools.combinations(tilderS, budget))
        comb2obj = {}
        for i, comb in enumerate(comb_list):
            comb2obj[comb] = self.compute_obj4(comb, tilderR, p, q)[self.OBJS.index(self.obj)]
        sorted_comb2obj = sorted(comb2obj.items(), key=lambda kv: kv[1], reverse=True)

        # if p<q and self.obj =='RI':
            # print("eq:", p, q, sorted_comb2obj[0], sorted_comb2obj[-1], self.compute_obj4(sorted_comb2obj[0][0], tilderR, p, q), self.compute_obj4(comb, tilderR, p, q))
            # return sorted_comb2obj[-1][0]
        # return sorted_comb2obj[0][0]
        # if q<=q:
        #     if self.obj == 'I':
        #     print("ne:", p, q, sorted_comb2obj[0], sorted_comb2obj[-1],
        #           self.compute_obj4(sorted_comb2obj[0][0], tilderR, p, q), self.compute_obj4(comb, tilderR, p, q))

        setM_star = sorted_comb2obj[0][0]
        return setM_star  # 不return 对应的obj值了, 再算一遍咋啦
