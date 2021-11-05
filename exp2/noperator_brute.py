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
        self.objs2budget2scheme2optsolution = self.load_objs2budget2scheme2optsolution()


    def opt_price_objs(self):
        for budget in self.budget_list:
            self.logger.info(f"{'=' * 30} {self.network.did}_{int(self.network.lamb)}_A_{self.method}  b={budget}")
            for (p, q) in self.pq_list:  # 里面的循环是algorithm 1了
                if budget not in self.budgets2schemes2combs2result.keys():
                    self.budgets2schemes2combs2result[budget] = {}
                if (p, q) in self.budgets2schemes2combs2result[budget].keys():  # 应该等价于 self.budget2scheme2optsolution
                    self.logger.info(f'skip {(p, q)} ')
                else:
                    self.logger.info(f'compute {(p, q)}')
                    tilderR, tilderS = self.get_tilderR_tilderS(p, q)
                    comb_list = list(itertools.combinations(tilderS, budget))
                    combs2result = {}
                    for i, comb in enumerate(comb_list):
                        combs2result[comb] = self.compute_obj4(comb, tilderR, p, q)
                    self.budgets2schemes2combs2result[budget][(p, q)] = combs2result
            self.dump_budgets2schemes2combs2result()

            schemes2combs2result = self.budgets2schemes2combs2result[budget]
            for obj in self.OBJS:
                schemes2optsolution = {}
                for scheme, combs2result in schemes2combs2result.items():
                    if len(combs2result.keys()) > 0:
                        sorted_combs2result = sorted(combs2result.items(),
                                                     key=lambda kv: kv[1][self.OBJS.index(obj)], reverse=True)
                        schemes2optsolution[scheme] = (sorted_combs2result[0][0], *sorted_combs2result[0][1])
                self.objs2budget2scheme2optsolution[obj][budget] = schemes2optsolution

                prefix = f"{self.network.did}_{int(self.network.lamb)}_{obj}_{self.method}"
                nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
                result_pkl_path = f"{self.PKL_DIR}/{prefix}_{nowTime}.pkl"
                pickle.dump(self.objs2budget2scheme2optsolution[obj], open(result_pkl_path, 'wb'))


    def load_objs2budget2scheme2optsolution(self):
        objs2budget2scheme2optsolution = {}
        for obj in self.OBJS:
            prefix = f"{self.network.did}_{int(self.network.lamb)}_{obj}_{self.method}"
            pklsrc = get_latest_path(self.PKL_DIR, prefix, 'pkl')
            if pklsrc != None:
                objs2budget2scheme2optsolution[obj] = pickle.load(open(pklsrc, 'rb'))
            else:
                objs2budget2scheme2optsolution[obj] = {}
        return objs2budget2scheme2optsolution



    def load_budgets2schemes2combs2result(self):
        budgets2schemes2combs2result = {}
        # self.PKL_PREFIX = f"{self.network.did}_{int(self.network.lamb)}_{self.obj}_{self.method}"
        prefix =  f"{self.network.did}_{int(self.network.lamb)}_A_{self.method}"
        pklsrc = get_latest_path(self.PKL_DIR, prefix, 'pkl')
        if pklsrc != None:
            budgets2schemes2combs2result = pickle.load(open(pklsrc, 'rb'))
        return budgets2schemes2combs2result


    def dump_budgets2schemes2combs2result(self):
        """Dump the result pkl with cur_time.
        """
        nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
        pklpath = f"{self.PKL_DIR}/{self.network.did}_{int(self.network.lamb)}_A_{self.method}_{nowTime}.pkl"
        pickle.dump(self.budgets2schemes2combs2result, open(pklpath, 'wb'))



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
