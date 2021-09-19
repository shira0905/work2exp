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

class NetoperatorSW:
    """The class of an operator"""

    def __init__(self, logger, network: Network, version, method, grain_p, grain_alpha):  # budget, grain_p, grain_q
        self.logger = logger
        self.version = version
        self.network = network
        self.method = method

        self.budget2scheme2result = self.load_budget2scheme2result()
        self.p_list_all = np.linspace(0, 1, num=grain_p + 1, endpoint=True)  #if grain_p != 0 else valuations_filtered
        self.alpha_list_all = np.linspace(0, 1, num=grain_alpha + 1, endpoint=True) #if grain_alpha != 0 else costs_f

    def load_budget2scheme2result(self):
        budget2scheme2result = {}
        result_pkl_path_list = [d for d in os.listdir(f"../eplots_sw") if f"{self.network.did}_{self.method}" in d and 'pkl' in d]
        result_pkl_path_list.sort()
        print(result_pkl_path_list)
        if len(result_pkl_path_list)>0:
            budget2scheme2result = pickle.load(open(f"../eplots_sw/{result_pkl_path_list[-1]}", 'rb'))
        return budget2scheme2result

    def search_budget2scheme2result(self, budget, tilderR, tilderS):
        if budget not in self.budget2scheme2result.keys():
            return None
        scheme2result = self.budget2scheme2result[budget]
        for scheme, result in scheme2result.items():
            p, q = scheme
            tilderR_history, tilderS_history = self.get_tilderR_tilderU(p, q)
            if tilderR_history == tilderR and tilderS_history == tilderS:
                return result
        return None

    def dump_budget2scheme2result(self):
        nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
        result_pkl_path = f"../eplots_sw/{self.network.did}_{self.method}_{nowTime}.pkl"
        pickle.dump(self.budget2scheme2result, open(result_pkl_path, 'wb'))


    def get_marginal_greedy(self, tilderR, tilderS, M_last, Incr_last, budget_last):
        """Get the result (M, Incr)_{b+1} if based on (currentM, currentIncr)_{b}

        :param tilderR:
        :type tilderR:
        :param tilderS:
        :type tilderS:
        :param currentM:
        :type currentM:
        :param currentIncr:
        :type currentIncr:
        :param current_budget:
        :type current_budget:
        :return:
        :rtype:
        """
        if len(M_last) < budget_last:  # S不够
            return M_last, Incr_last

        u_star = self.get_best_marginal_supplier(tilderR, tilderS, M_last) # 这个不对，返回了和之前一样的
        if u_star:
            M_last.add(u_star)
        card = self.compute_sw(M_last, tilderR)

        # print(currentM , 'add', u_star)
        # self.logger.info(M, card)
        return M_last, card


    def get_best_marginal_supplier(self, tilderR, tilderS:set, M_last):
        """Get supplier with largest marginal

        If tilderS is empty then return -1.
        If tilderS are neighbors all ready, then resutn the first one in tilderS into set, which is meaningless.

        :param tilderR:
        :type tilderR:
        :param tilderS:
        :type tilderS:
        :param currentM:
        :type currentM:
        :return: u_star, supplier with largest marginal
        :rtype:
        """
        u_star = None
        max_marginal = 0
        # print(f'tilderS.difference(M_last) = {tilderS.difference(M_last)}')
        for s in tilderS.difference(M_last): # 如果tilderS为空u_star=-1，如果tilderS都已经是好友则返回第一个
            marginal_s = self.compute_marginal_supplier(tilderR, M_last, s)
            if marginal_s >= max_marginal:
                u_star = s
                max_marginal = marginal_s
        return u_star


    def compute_marginal_supplier(self, tilderR, M_last, s_bar):
        """Compute the marginal increase of tilderR by adding supplier candidate s_bar into currentM (for do_greedy)

        :math:`\sum_{r \in tilderR} {  I_r(currentM + bar\_s) -  I_r(currentM) }`

        :param tilderR:
        :type tilderR:
        :param tilderS:
        :type tilderS:
        :param currentM: the suppliers have been selected into M
        :type currentM:
        :param s_bar: the candidate supplier to evaluate
        :type s_bar:
        :return: f_R_marginal
        :rtype:
        """
        # card_R_marginal = 0
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





    def get_M_brute(self, budget, tilderR, tilderS):
        """Get ground truth opt participating suppliers star_M by brute-force method and revenue R(star_M)

        :param budget:
        :type budget:
        :param tilderR:
        :type tilderR:
        :param tilderS:
        :type tilderS:
        :return: star_M, R(star_M)
        :rtype:
        """

        if len(tilderS) <= budget:
            sw = self.compute_sw(tilderS, tilderR)
            return tilderS, sw

        combs = itertools.combinations(tilderS, budget)
        result = {}
        for i, group in enumerate(combs):
            sw = self.compute_sw(group, tilderR)
            result[group] = sw
        result_sorted = sorted(result.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        return result_sorted[0][0], result_sorted[0][1]

    def compute_sw(self, M, tilderR):
        sw = 0
        for r in tilderR:
            I_r_S = set()
            for s in M:
                reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[r][r]
                I_r_S = I_r_S.union(self.network.get_visible(s, reduced_dist))

            ori_tau_vis = self.network.get_visible(r, self.network.tau)
            I_r = I_r_S.difference(ori_tau_vis)
            sw += len(I_r)*self.network.valuations[r]
        return sw



    def get_tilderR_tilderU(self, p, q):
        """Get participating requesters tilderR, potential participating tilderS

        :param p:
        :type p:
        :param q:
        :type q:
        :return: participating requesters tilderR, potential participating tilderS
        :rtype:
        """
        tilderR, tilderS = set(), set()
        for i in self.network.R:
            if self.network.valuations[i] >= p:
                tilderR.add(i)
        for i in self.network.S:
            if self.network.costs[i] <= q:
                tilderS.add(i)
        # do not set
        return tilderR, tilderS

