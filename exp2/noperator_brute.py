#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/9/2 20:37
@Desc    :
"""
import random
import math
import numpy as np
from zutil import get_log, plot_dist_hist
import itertools
import datetime
from network import Network
import matplotlib.pyplot as plt
import pickle
import os

import abc
from abc import ABC, abstractmethod

from noperator import Noperator


class BruteOperator(Noperator):
    """The class of an operator aim to maximize revenue"""

    def __init__(self, logger, network, method, obj, budget_list, grain):
        Noperator.__init__(self, logger, network, method, obj, budget_list, grain)




    def compute(self):
        """For each (p, alpha) under given search mode,
         search the optimal set and compute the corresponding obj value for all budgets using brute.

         :return: Dump budget2scheme2result as pkl
         :rtype: None
         """

        for budget in self.budget_list:
            if budget not in self.budget2scheme2result.keys():
                self.budget2scheme2result[budget] = {}
            palpha_list = list(itertools.product(self.p_list_all, self.alpha_list_all))
            for (p, alpha) in palpha_list:
                q = alpha * p
                tilderR, tilderS = self.get_tilderR_tilderS(p, q)
                result = self.search_budget2scheme2result(budget, tilderR, tilderS)
                # 可能需要修改一下，现在是从当前对象的结果中搜索，完全可以从历史所有结果中搜索
                if result:
                    M, increase, sw = result[0], result[1], result[3]  # obj= increase if rev , sw if sw
                    rev = (p - q) * increase
                    self.logger.info(f"load | {budget} | {(p, alpha)} | {len(tilderR)} | {len(tilderS)} | {M} | {increase}| {rev} | {sw} ")
                else:
                    if self.obj == 'rev':
                        M, increase = self.get_M_brute(budget, tilderR, tilderS)
                        rev = (p - q) * increase
                        sw = self.compute_sw(M, tilderR)
                    if self.obj == 'sw':
                        M, sw = self.get_M_brute(budget, tilderR, tilderS)
                        increase = self.compute_incr(M, tilderR)
                        rev = (p - q) * increase
                    self.logger.info( f"compute | {budget} | {(p, alpha)} | {len(tilderR)} | {len(tilderS)} | {M} | {increase}| {rev} | {sw} ")

                self.budget2scheme2result[budget][(p, alpha)] = (M, increase, rev, sw)
        self.dump_budget2scheme2result()


    def get_M_brute(self, budget, tilderR, tilderS):
        """Get ground truth opt participating suppliers star_M by brute-force method and incr_R R(star_M)

        :param budget:
        :type budget:
        :param tilderR:
        :type tilderR:
        :param tilderS:
        :type tilderS:
        :return: optimal supplier set star_M, corresponding visibility increase of suppliers incr_R
        :rtype: set(), int
        """

        if len(tilderS) <= budget:
            if self.obj == 'rev':
                objvalue = self.compute_incr(tilderS, tilderR)
            if self.obj == 'sw':
                objvalue = self.compute_sw(tilderS, tilderR)
            return tilderS, objvalue

        combs = itertools.combinations(tilderS, budget)
        result = {}
        for i, group in enumerate(combs):
            if self.obj == 'rev':
                pbjvalue = self.compute_incr(group, tilderR)
            if self.obj == 'sw':
                pbjvalue = self.compute_sw(group, tilderR)
            result[group] = pbjvalue
        result_sorted = sorted(result.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        return result_sorted[0][0], result_sorted[0][1]
