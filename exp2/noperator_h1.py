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
class H1Operator(Noperator):
    """The class of an operator aim to maximize revenue"""

    def __init__(self, logger, network, method, obj, budget_list, grain):
        Noperator.__init__(self, logger, network, method, obj, budget_list, grain)


    def compute(self):

        for budget in self.budget_list:
            # print(budget)
            # print(self.budget2scheme2result)
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

                    M = self.get_M_topvis(budget, tilderR)
                    sw = self.compute_sw(M, tilderR)
                    increase = self.compute_incr(M, tilderR)
                    rev = (p - q) * increase
                    self.logger.info(
                        f"compute | {budget} | {(p, alpha)} | {len(tilderR)} | {len(tilderS)} | {M} | {increase}| {rev} | {sw} ")
                    self.budget2scheme2result[budget][(p, alpha)] = (M, increase, rev, sw)

                self.budget2scheme2result[budget][(p, alpha)] = (M, increase, rev, sw)
        self.dump_budget2scheme2result()


    def get_M_topvis(self, b, tilderR):
        M = set()
        M.add(1)
        M.remove(1)
        node2vis = {}
        # print(self.network.tau)
        for node in tilderR:
            setsize = len(self.network.get_visible(node, self.network.tau))
            node2vis[node] = setsize

        node2vis_sorted = sorted(node2vis.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        x = 0
        while x < len(node2vis_sorted):
            if len(M) == b:
                break
            M.add(node2vis_sorted[x][0])
            x += 1
        return M
