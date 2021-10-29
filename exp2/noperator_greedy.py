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

class GreedyOperator(Noperator):
    """The class of an operator aim to maximize revenue"""

    def __init__(self, logger, network, method, obj, budget_list, grain):
        Noperator.__init__(self, logger, network, method, obj, budget_list, grain)

    def compute(self):
        """For each (p, alpha) under given search mode,
         search the optimal set and compute the corresponding obj value for all budgets using brute.

         :return: Dump budget2scheme2result as pkl
         :rtype: None
         """
        budget_max = max(self.budget_list)
        for budget in range(1, budget_max + 1):
            if budget not in self.budget2scheme2result.keys():
                self.budget2scheme2result[budget] = {}

        palpha_list = list(itertools.product(self.p_list_all, self.alpha_list_all))
        for (p, alpha) in palpha_list:
            q = alpha * p
            self.logger.info(f"{'*' * 10} {(p, alpha, q)}")
            tilderR, tilderS = self.get_tilderR_tilderS(p, q)
            max_history_budget, max_history_result = 0, None
            for b in range(budget_max, 0, -1):
                search_result = self.search_budget2scheme2result(b, tilderR, tilderS)
                if search_result:
                    max_history_result = search_result
                    max_history_budget = b
                    break
            self.logger.info(
                f"max_history_budget={max_history_budget}, max_history_result={None if not max_history_result else max_history_result[:3]}")

            if search_result:
                M_last, increase_last, rev_last, sw_last = max_history_result
            else:
                M_last, increase_last, rev_last, sw_last = set(), 0, 0, 0

            for budget in range(1, max_history_budget + 1):
                M, increase, rev, sw = self.search_budget2scheme2result(budget, tilderR, tilderS)
                rev = (p - q) * increase
                # self.budget2scheme2result[budget][(p, q)] = (M.copy(), increase, rev, sw)
                self.budget2scheme2result[budget][(p, alpha)] = (M.copy(), increase, rev, sw)
                self.logger.info(
                    f"load | {budget} | {(p, alpha)} | {len(tilderR)} | {len(tilderS)} | {M} | {increase}| {rev} | {sw} ")

            for budget_last in range(max_history_budget, budget_max):
                if self.obj == 'rev':
                    M_last, increase = self.get_marginal_greedy(tilderR, tilderS, M_last,
                                                                budget_last)  # M_last alredy +1
                    rev = (p - q) * increase
                    sw = self.compute_sw(M_last, tilderR)
                if self.obj == 'sw':
                    M_last, sw = self.get_marginal_greedy(tilderR, tilderS, M_last, budget_last)
                    increase = self.compute_sw(M_last, tilderR)
                    rev = (p - q) * increase
                self.budget2scheme2result[budget_last + 1][(p, alpha)] = (M_last.copy(), increase, rev, sw)
                self.logger.info(
                    f"compute | {budget} | {(p, alpha)} | {len(tilderR)} | {len(tilderS)} | {M_last} | {increase}| {rev} | {sw} ")
        self.dump_budget2scheme2result()



    def get_marginal_greedy(self, tilderR, tilderS, M_last, budget_last):
        """Get the result (M, Incr)_{b+1} if based on (M_last, Incr_last)_b

        :param tilderR:
        :type tilderR:
        :param tilderS:
        :type tilderS:
        :param M_last:
        :type M_last:
        :param Incr_last:
        :type Incr_last:
        :param budget_last:
        :type budget_last:
        :return: M_last = M_last+{u_star}, card = increase of M_last+{u_star}
        :rtype:
        """

        if len(M_last) < budget_last:  # number of suppliers < budget
            return M_last, self.compute_sw(M_last, tilderR)
        u_star = self.get_best_marginal_supplier(tilderR, tilderS, M_last)
        if u_star:
            M_last.add(u_star)
        if self.obj == 'rev':
            obj = self.compute_incr(M_last, tilderR)
        if self.obj == 'sw':
            obj = self.compute_sw(M_last, tilderR)
        return M_last, obj



    def get_best_marginal_supplier(self, tilderR, tilderS:set, M_last):
        """Get supplier with largest marginal

        If tilderS.difference(M_last) is empty then return None.
        If tilderS are neighbors all ready, then return the first one in tilderS into set, which is meaningless.

        :param tilderR:
        :type tilderR:
        :param tilderS:
        :type tilderS:
        :param M_last:
        :type M_last:
        :return: u_star
        :rtype:
        """

        u_star = None
        max_marginal = 0
        for s in tilderS.difference(M_last):
            if self.obj == 'rev':
                marginal_s = self.compute_marginal_supplier_rev(tilderR, M_last, s)
            if self.obj == 'sw':
                marginal_s = self.compute_marginal_supplier_sw(tilderR, M_last, s)
            if marginal_s >= max_marginal:
                u_star = s
                max_marginal = marginal_s
        return u_star


    def compute_marginal_supplier_rev(self, tilderR, M_last, s_bar):
        """Compute the marginal increase of tilderR by adding supplier candidate s_bar into currentM (for do_greedy)

        # TODO: check if correct
        :math:`\sum_{r \in tilderR} {  I_r(currentM + bar\_s) -  I_r(currentM) }`

        :param tilderR:
        :type tilderR:
        :param M_last: the suppliers have been selected into M
        :type M_last:
        :param s_bar: the candidate supplier to evaluate
        :type s_bar:
        :return: incr_R_marginal if adding s_bar into M_last
        :rtype: int
        """
        incr_R_marginal = 0
        for r in tilderR:
            reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[r][r]  # tau-1-0
            I_r_s_bar = self.network.get_visible(s_bar, reduced_dist)

            I_r_lastM = set()
            # if requester2IncrMlast and r in requester2IncrMlast.keys(): # 已经入选的Mlast对requester 带来的visible set的新增集合
            #     I_r_lastM = requester2IncrMlast[r]
            # else: # 既然现在不准备用 requester2IncrMlast 这个集合了，那么else这里就足够了
            for s in M_last:
                reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[r][r]  # tau-1-0
                I_r_lastM.union(self.network.get_visible(s, reduced_dist))

            origin_tau_visible = self.network.get_visible(r, self.network.tau)

            I_r = I_r_s_bar.difference(I_r_lastM).difference(origin_tau_visible)
            incr_R_marginal += len(I_r) # lower i is int, capital I is set
            # I_r_lastM.union(I_r_s_bar)
        return incr_R_marginal

    def compute_marginal_supplier_sw(self, tilderR, M_last, s_bar):
        """Compute the marginal increase of tilderR by adding supplier candidate s_bar into currentM (for do_greedy)

        # TODO: check if correct
        :math:`\sum_{r \in tilderR} p_r{  V_r(currentM + bar\_s) -  V_r(currentM) }`

        :param tilderR:
        :type tilderR:
        :param M_last: the suppliers have been selected into M
        :type M_last:
        :param s_bar: the candidate supplier to evaluate
        :type s_bar:
        :return: incr_R_marginal if adding s_bar into M_last
        :rtype: float
        """
        SW_marginal = 0
        for r in tilderR:
            reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[r][r]  # tau-1-0
            I_r_s_bar = self.network.get_visible(s_bar, reduced_dist)

            I_r_lastM = set()
            # if requester2IncrMlast and r in requester2IncrMlast.keys(): # 已经入选的Mlast对requester 带来的visible set的新增集合
            #     I_r_lastM = requester2IncrMlast[r]
            # else: # 既然现在不准备用 requester2IncrMlast 这个集合了，那么else这里就足够了
            for s in M_last:
                reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[r][r]  # tau-1-0
                I_r_lastM.union(self.network.get_visible(s, reduced_dist))

            origin_tau_visible = self.network.get_visible(r, self.network.tau)

            I_r = I_r_s_bar.difference(I_r_lastM).difference(origin_tau_visible)
            SW_marginal += len(I_r) * self.network.valuations[r]
        return SW_marginal
