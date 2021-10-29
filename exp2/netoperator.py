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
    """The class of an operator aim to maximize revenue"""

    def __init__(self, logger, network, method, obj, budget_list, grain):
        self.logger = logger
        self.network = network
        self.method = method
        self.obj = obj
        self.budget_list = budget_list

        self.budget2scheme2result = self.load_budget2scheme2result()
        self.p_list_all = np.linspace(0, 1, num=grain + 1, endpoint=True)  # todo: extend to epsilon=0
        self.alpha_list_all = np.linspace(0, 1, num=grain + 1, endpoint=True)  # todo: extend to epsilon=0

    def algo(self):
        if self.method == 'greedy':
            self.do_greedy()
        if self.method == 'brute':
            self.do_brute()
        if self.method == 'shapley':
            self.do_shapley()





    def do_shapley(self):
        coalition = [1,2,3]
        combs = []
        for i in range(0, len(coalition) + 1):
            listing = [list(x) for x in itertools.combinations(coalition, i)]
            combs.extend(listing)
        for comb in [[1,2,3]]:
            print('===========', comb)
            print('-------compute_shapley_traditional')
            self.compute_shapley_traditional(comb)
            print('-------compute_shapley_efficient')
            self.compute_shapley_efficient(comb)

    def compute_shapley_efficient(self, coalition):
        node2sv = {}
        for v in coalition:
            print('compute shapley value of', v)
            sv = 1 / (1 + self.network.graph.out_degree[v])
            for u in self.network.graph[v]:
                # sv += 1 / (1 + len(self.network.graph[u]))
                sv += 1 / (1 + self.network.graph.out_degree[u])
                print(
                    f"{v}'s neighbor {u}, degr(u)={self.network.graph.out_degree[u]}, delta_sv={ 1/(1 + self.network.graph.out_degree[u])} ")
            node2sv[v] = sv
        for node, sv in node2sv.items():
            print(node, sv)

    def compute_shapley_traditional(self, coalition):
        pers = list(itertools.permutations(coalition))
        node2sv = {}
        for i, pi in enumerate(pers):
            for j, node in enumerate(pi):
                marginal = self.nu1(pi[:j+1]) - self.nu1(pi[:j])
                if node not in node2sv.keys():
                    node2sv[node] = 0
                node2sv[node] = (node2sv[node]*i + marginal)/ (i+1)
        for node, sv in node2sv.items():
            print(node, sv)


    def nu1(self, coalition):
        nuset = set()
        for member in coalition:
            nuset.add(member)
            nuset = nuset.union(self.network.graph[member])
        return len(nuset)



    def do_greedy(self):
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
                self.logger.info(f"load | {budget} | {(p, alpha)} | {len(tilderR)} | {len(tilderS)} | {M} | {increase}| {rev} | {sw} ")

            for budget_last in range(max_history_budget, budget_max):
                if self.obj == 'rev':
                    M_last, increase = self.get_marginal_greedy(tilderR, tilderS, M_last, budget_last) # M_last alredy +1
                    rev = (p - q) * increase
                    sw = self.compute_sw(M_last, tilderR)
                if self.obj == 'sw':
                    M_last, sw = self.get_marginal_greedy(tilderR, tilderS, M_last, budget_last)
                    increase = self.compute_sw(M_last, tilderR)
                    rev = (p - q) * increase
                self.budget2scheme2result[budget_last + 1][(p, alpha)] = (M_last.copy(), increase, rev, sw)
                self.logger.info(f"compute | {budget} | {(p, alpha)} | {len(tilderR)} | {len(tilderS)} | {M_last} | {increase}| {rev} | {sw} ")
        self.dump_budget2scheme2result()

    def do_brute(self):
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

    def get_tilderR_tilderS(self, p, q):
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

    def load_budget2scheme2result(self):
        """Load the latest result pkl under

        :return: budget2scheme2result
        :rtype: dict
        """
        budget2scheme2result = {}
        result_pkl_path_list = [d for d in os.listdir(f"../eplots/pkl{str(self.network.gamma).replace('.','')}/") if f"{self.network.did}_{self.method}_{self.obj}" in d and '.pkl' in d]
        result_pkl_path_list.sort()
        if len(result_pkl_path_list) > 0:
            budget2scheme2result = pickle.load(open(f"../eplots/pkl{str(self.network.gamma).replace('.','')}/{result_pkl_path_list[-1]}", 'rb'))
        return budget2scheme2result

    def search_budget2scheme2result(self, budget, tilderR, tilderS):
        """Search if given tilderR, tilderS has been computed in history.

        :param budget:
        :type budget:
        :param tilderR:
        :type tilderR:
        :param tilderS:
        :type tilderS:
        :return: result=(suppliers M, increase I, revenue R) in dictionary budget2scheme2result with legal key
        :rtype: (set(), int, float)
        """
        if budget not in self.budget2scheme2result.keys():
            return None
        scheme2result = self.budget2scheme2result[budget]
        for scheme, result in scheme2result.items():
            # p, q = scheme
            p, alpha = scheme
            tilderR_history, tilderS_history = self.get_tilderR_tilderS(p, p*alpha)
            if tilderR_history == tilderR and tilderS_history == tilderS:
                return result
        return None

    def dump_budget2scheme2result(self):
        """Dump the result pkl with cur_time  .

        :return: None
        :rtype: None
        """
        nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
        result_pkl_path = f"../eplots/pkl{str(self.network.gamma).replace('.','')}/{self.network.did}_{self.method}_{self.obj}_{nowTime}.pkl"
        pickle.dump(self.budget2scheme2result, open(result_pkl_path, 'wb'))

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

    def compute_incr(self, M, tilderR):
        """The visibility increase of tilderR when adding selected suppliers

        Given fix tau=2 default_new_dist=1,
        - reduced_dist=1 only when spl[r][l_e]=0 --> I_r_S union network.get_visible(l_s, 1)= {one hop neighbors of l_s}
        - reduced_dist=0 only when spl[r][l_e]=0 --> I_r_S union network.get_visible(l_s, 0)={l_s}
        - otherwise<=0 otherwise --> I_r_S union empty

        :param M:
        :type M:
        :param tilderR:
        :type tilderR:
        :return:
        :rtype:
        """

        incr_R = 0
        for r in tilderR:
            I_r_S = set()
            for s in M:
                reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[r][r]
                I_r_S = I_r_S.union(self.network.get_visible(s, reduced_dist))

            ori_tau_vis = self.network.get_visible(r, self.network.tau)
            I_r = I_r_S.difference(ori_tau_vis)
            incr_R += len(I_r)
        return incr_R

    def compute_sw(self, M, tilderR):
        """The social welfare of tilderR when adding selected suppliers

        :return: sw
        :rtype: float
        """
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
