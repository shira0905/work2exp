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

class Netoperator:
    """The class of an operator"""

    def __init__(self, logger, network: Network, version, method, grain_p, grain_alpha):  # budget, grain_p, grain_q
        self.logger = logger
        self.version = version
        self.network = network
        self.method = method

        self.budget2scheme2result = self.load_budget2scheme2result()
        # self.pq_list = self.get_pq_list2(grain_p, grain_alpha)
        self.p_list_all = np.linspace(0, 1, num=grain_p + 1, endpoint=True)
        self.alpha_list_all = np.linspace(0, 1, num=grain_alpha + 1, endpoint=True)
        # self.scheme2RS = self.get_scheme2RS(self.pq_list)


    # def get_scheme2RS(self, pq_list):
    #     scheme2RS = {}
    #     for p, q in pq_list:
    #         tilderR, tilderS = self.get_tilderR_tilderU(p, q)
    #         scheme2RS[(p, q)] = (tilderR, tilderS)
    #     return scheme2RS

    # def get_scheme2RS(self, grain_tuple_list):
    #     scheme2RS = {}
    #     for grain_tuple_str in grain_tuple_list:
    #         grain_tuple = [int(x) for x in grain_tuple_str.split('+')]
    #         pq_list = self.get_pq_list(*grain_tuple)  # 数据持久化
    #         for p, q in pq_list:
    #             tilderR, tilderS = self.get_tilderR_tilderU(p, q)
    #             scheme2RS[(p, q)] = (tilderR, tilderS)
    #     return scheme2RS

    # def load_budget2scheme2result_(self):
    #     budget2scheme2result = {}
    #     result_pkl_path = f"../elogs/{self.network.did}_{self.method}.pkl"
    #     if os.path.exists(result_pkl_path):  # seed, percent_R, percent_S
    #         budget2scheme2result = pickle.load(open(result_pkl_path, 'rb'))
    #     return budget2scheme2result

    def load_budget2scheme2result(self):
        budget2scheme2result = {}
        result_pkl_path_list = [d for d in os.listdir(f"../eplots") if f"{self.network.did}_{self.method}" in d and 'pkl' in d]
        result_pkl_path_list.sort()
        print(result_pkl_path_list)
        if len(result_pkl_path_list)>0:
            budget2scheme2result = pickle.load(open(f"../eplots/{result_pkl_path_list[-1]}", 'rb'))
        return budget2scheme2result

    # def search_budget2scheme2result_(self, budget, tilderR, tilderS):
    #     scheme_sameRS_list = [k for k, v in self.scheme2RS.items() if v == (tilderR, tilderS)]
    #     # 这里不是很好，scheme2RS  只有当前对象的信息，二不能搜索到历史对象如果已经计算过这组alpha了
    #     # 所以最后存储result的时候是不是应该把 tilderR 和 tilderS 也存进去呢
    #     for scheme_sameRS in scheme_sameRS_list:
    #         try:
    #             self.budget2scheme2result[budget][scheme_sameRS]
    #             return self.budget2scheme2result[budget][scheme_sameRS]
    #         except KeyError as e:
    #             # self.logger.info('KeyError!')
    #             pass
    #         # if self.scheme2result[budget][scheme_sameRS]:
    #         #     return self.scheme2result[budget][scheme_sameRS]
    #     return None

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
        result_pkl_path = f"../eplots/{self.network.did}_{self.method}_{nowTime}.pkl"
        pickle.dump(self.budget2scheme2result, open(result_pkl_path, 'wb'))


    def get_marginal_greedy_(self, tilderR, tilderS, M_last, Incr_last, requester2IncrMlast, budget_last):
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

        u_star, requester2Incr_star = self.get_best_marginal_supplier(tilderR, tilderS, M_last, requester2IncrMlast) # 这个不对，返回了和之前一样的

        print("u_star, requester2Incr_star", u_star, requester2Incr_star)
        if u_star:
            M_last.add(u_star)
        card = self.compute_incr(M_last, tilderR)

        M = M_last.copy()

        # print(currentM , 'add', u_star)
        self.logger.info(M, card, requester2Incr_star)
        return M, card, requester2Incr_star

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
        card = self.compute_incr(M_last, tilderR)

        # print(currentM , 'add', u_star)
        # self.logger.info(M, card)
        return M_last, card


    def get_best_marginal_supplier_(self, tilderR, tilderS:set, M_last, requester2IncrMlast):
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
        requester2Incr_star = set()
        # print(f'tilderS.difference(M_last) = {tilderS.difference(M_last)}')
        for s in tilderS.difference(M_last): # 如果tilderS为空u_star=-1，如果tilderS都已经是好友则返回第一个
            marginal_s, requester2Incr = self.compute_marginal_supplier(tilderR, M_last, requester2IncrMlast, s)
            if marginal_s >= max_marginal:
                u_star = s
                max_marginal = marginal_s
                requester2Incr_star = requester2Incr
        return u_star, requester2Incr_star

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

    def compute_marginal_supplier_(self, tilderR, M_last, requester2IncrMlast, s_bar):
        """Compute the marginal increase of tilderR by adding supplier candidate s_bar into currentM (for do_greedy)

        # TODO 这个不对，返回了和之前一样的
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
        card_R_marginal = 0

        for r in tilderR:
            reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[r][r]  # tau-1-0
            I_r_s_bar = self.network.get_visible(s_bar, reduced_dist)

            I_r_lastM = set()
            if requester2IncrMlast and r in requester2IncrMlast.keys():
                I_r_lastM = requester2IncrMlast[r]
            else:
                for s in M_last:
                    reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[r][r]  # tau-1-0
                    I_r_lastM.union(self.network.get_visible(s, reduced_dist))

            origin_tau_visible = self.network.get_visible(r, self.network.tau)

            I_r = I_r_s_bar.difference(I_r_lastM).difference(origin_tau_visible)
            card_R_marginal += len(I_r)

            I_r_lastM.union(I_r_s_bar)
            # print('I_r_lastM3', I_r_lastM)
            requester2IncrMlast[r] = I_r_lastM  # terrible name Oops
        return card_R_marginal, requester2IncrMlast

    def compute_marginal_supplier(self, tilderR, M_last, s_bar):
        """Compute the marginal increase of tilderR by adding supplier candidate s_bar into currentM (for do_greedy)

        # TODO 这个不对，返回了和之前一样的
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
        card_R_marginal = 0

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
            card_R_marginal += len(I_r)

            I_r_lastM.union(I_r_s_bar)

        return card_R_marginal



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
            card = self.compute_incr(tilderS, tilderR)
            return tilderS, card

        combs = itertools.combinations(tilderS, budget)
        result = {}
        for i, group in enumerate(combs):
            card = self.compute_incr(group, tilderR)
            result[group] = card
        result_sorted = sorted(result.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
        return result_sorted[0][0], result_sorted[0][1]


    def get_M_brute_sw(self, budget, tilderR, tilderS):
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
            card = self.compute_incr(group, tilderR)
            result[group] = card
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

    def compute_revenue(self, p, q, incr):
        return (p-q)*incr

    def compute_incr(self, M, tilderR):
        """The increase (to extend to revenue) of tilderR when adding selected links

        Given fix tau=2 default_new_dist=1,
        - reduced_dist=1 only when spl[r][l_e]=0 --> I_r_S union network.get_visible(l_s, 1)= {one hop neighbors of l_s}
        - reduced_dist=0 only when spl[r][l_e]=0 --> I_r_S union network.get_visible(l_s, 0)={l_s}
        - otherwise<=0 otherwise --> I_r_S union empty

        :param links:
        :type links:
        :param tilderR:
        :type tilderR:
        :return:
        :rtype:
        """
        card = 0
        for r in tilderR:
            I_r_S = set()
            for s in M:
                reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[r][r]
                I_r_S = I_r_S.union(self.network.get_visible(s, reduced_dist))

            ori_tau_vis = self.network.get_visible(r, self.network.tau)
            I_r = I_r_S.difference(ori_tau_vis)
            card += len(I_r)
        return card

    def get_pq_list(self, grain_p, grain_q):
        """Get (p,q) schemes need to study according to the grains and meaningful bound.

        Bound to gaurantee no empty side:
        (1) tilderR={u|p_i(v[i]) >= p, u \in R} if p> max_v then empty tilderR;
        (2) tilderS={u|q_u(c[i]) <= q, u \in S} if q< min S then empty tilderS.

        Grain grain=0 means all possible p/q/schemes affect formation of R and S

        :param grain_p: divede [0,1] into grain_p intervals
        :type grain_p: int
        :param grain_q: divede [0,1] into grain_q intervals
        :type grain_q: int
        :return: pq_list
        :rtype:
        """
        valuations_filtered = [v for i, v in enumerate(self.network.valuations) if i in self.network.R]
        costs_filtered = [c for i, c in enumerate(self.network.costs) if i in self.network.S]
        # "will participant if his per unit valuation does not exceed the per unit price the Operator pays"
        # costs_filtered = [self.costs[i] for i in range(self.N) if i in self.S]
        plot_dist_hist(valuations_filtered, 10, 'd2v')
        plot_dist_hist(costs_filtered, 10, 'd2c')

        p_list_all = np.linspace(0, 1, num=grain_p + 1, endpoint=True) if grain_p != 0 else valuations_filtered
        q_list_all = np.linspace(0, 1, num=grain_q + 1, endpoint=True) if grain_q != 0 else costs_filtered
        max_p = max(valuations_filtered)
        min_q = min(costs_filtered)
        p_list = [p for p in p_list_all if p <= max_p]
        q_list = [q for q in q_list_all if q >= min_q]

        pq_list = list(itertools.product(p_list, q_list))
        return pq_list

    def get_pq_list2(self, grain_p, grain_alpha):
        """Get (p,q) schemes need to study according to the grains and meaningful bound.

        Bound to gaurantee no empty side:
        (1) tilderR={u|p_i(v[i]) >= p, u \in R} if p> max_v then empty tilderR;
        (2) tilderS={u|q_u(c[i]) <= q, u \in S} if q< min S then empty tilderS.

        Grain grain=0 means all possible p/q/schemes affect formation of R and S

        :param grain_p: divede [0,1] into grain_p intervals
        :type grain_p: int
        :param grain_q: divede [0,1] into grain_q intervals
        :type grain_q: int
        :return: pq_list
        :rtype:
        """
        valuations_filtered = [v for i, v in enumerate(self.network.valuations) if i in self.network.R]
        costs_filtered = [c for i, c in enumerate(self.network.costs) if i in self.network.S]
        # "will participant if his per unit valuation does not exceed the per unit price the Operator pays"
        # costs_filtered = [self.costs[i] for i in range(self.N) if i in self.S]
        plot_dist_hist(valuations_filtered, 10, 'd2v')
        plot_dist_hist(costs_filtered, 10, 'd2c')

        p_list_all = np.linspace(0, 1, num=grain_p + 1, endpoint=True) if grain_p != 0 else valuations_filtered
        alpha_list_all = np.linspace(0, 1, num=grain_alpha + 1, endpoint=True) if grain_alpha != 0 else costs_filtered
        # max_p = max(valuations_filtered)
        # min_q = min(costs_filtered)
        # p_list = [p for p in p_list_all if p <= max_p]
        # alpha_list = [alpha for alpha in alpha_list_all if alpha >= min_q]

        palpha_list = list(itertools.product(p_list_all, alpha_list_all))
        pq_list = []
        for palpha in palpha_list:
            p = palpha[0]
            q = palpha[1]*p
            pq_list.append( (p, q))
        return pq_list

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

