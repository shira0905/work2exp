#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/9/2 20:37
@Desc    :
"""

import itertools
from noperator import Noperator

class GreedyOperator(Noperator):
    """The class of an operator aim to maximize revenue"""

    def __init__(self, logger, network, obj, budget_list, grain):
        self.method = 'greedy'
        Noperator.__init__(self, logger, network, obj, budget_list, grain)


    def run(self):
        """For each (p, q) under given search mode,
         search the optimal set and compute the corresponding obj value for all budgets using brute.

         :return: Dump budget2scheme2optsolution as pkl
         :rtype: None
         """
        budget_max = max(self.budget_list) # 在算最大budget的时候一定会出小于它的budget时候的结果
        for budget in range(1, budget_max + 1):
            if budget not in self.budget2scheme2optsolution.keys():
                self.budget2scheme2optsolution[budget] = {}

        for (p, q) in self.pq_list:
            tilderR, tilderS = self.get_tilderR_tilderS(p, q)
            budget2setM_star = self.opt_setM(budget_max, tilderR, tilderS, p , q)
            for budget in range(1, budget_max + 1):
                setM_star = budget2setM_star[budget]
                objI, objW, objRI, objRW = self.compute_obj4(setM_star, tilderR, p, q)
                self.budget2scheme2optsolution[budget][(p, q)] = (setM_star, objI, objW, objRI, objRW)

        # 排序统一方法哦util或者plot里面
        # for budget in self.budget_list:
        #     # STEP2: sort and output  opt_setM_star and opt_objX_star  # if obj=='objI', 对应的value就是 opt_objI_star
        #     scheme2optsolution = self.budget2scheme2optsolution[budget]
        #     sorted_scheme2optsolution = sorted(scheme2optsolution.items(), key=lambda kv: kv[1][self.OBJS.index(self.obj)+1], reverse=True)
        #     opt_scheme = sorted_scheme2optsolution[0][0]
        #     opt_setM_star, objI, objW, objRI, objRW = sorted_scheme2optsolution[0][1]
        #     opt_obj_star = round(sorted_scheme2optsolution[0][1][self.OBJS.index(self.obj) + 1], 2)

        self.dump_budget2scheme2optsolution()



    def opt_setM(self, budget_max, tilderR, tilderS, p , q):
        # return a dict of setM_star, for all the b<=budget

        budget2setM_star = {} # 要不要把star 去掉改名

        # STEP1: 搜索历史, 不同的是不需要exactly 搜索给定的budget, 而是可以站在历史的肩膀上增量计算
        max_history_budget, max_history_result = 0, (set(), 0, 0, 0, 0)
        isfirst=0
        for budget in range(budget_max, 0, -1):  # 相同的双边阵营和目标, 搜索有记录的max budget,小于这个肯定已经被计算并且记录了. 左闭右开,
            search_result = self.search_budget2scheme2optsolution(budget, p, q)
            if search_result:
                budget2setM_star[budget] = search_result[0]
                if isfirst == 0:
                    max_history_budget, max_history_result = budget, search_result
                    isfirst = 1
        # self.logger.info(f"max_history_budget={max_history_budget}, max_history_result={None if not max_history_result else max_history_result[:3]}")


        # STEP2: 对于没有计算过的大于 max_history_budget的, 从max_history_budget开始做增量计算
        for budget_last in range(max_history_budget, budget_max):
            setM_last = self.add_best_marginal_supplier(tilderR, tilderS,  p, q, max_history_result[0], budget_last)  # M_last alredy +1
            # 相比返回list, 是不是可以吧opt_set直接接口到get_marginal_greedy
            budget2setM_star[budget_last+1] = setM_last.copy()

        return budget2setM_star



    def add_best_marginal_supplier(self, tilderR, tilderS, p, q, setM_last, budget_last):
        """Get supplier with largest marginal

        If tilderS.difference(M_last) is empty then return None.
        If tilderS are neighbors all ready, then return the first one in tilderS into set, which is meaningless. 不太可能那么多requesters都已经是neighbor了吧

        :return: M_last = M_last+{u_star}, card = increase of M_last+{u_star}
        :rtype:
        """

        if len(setM_last) < budget_last:  # last budget not fully satisfied, not alone current budget
            return setM_last

        # u_star = self.get_best_marginal_supplier(tilderR, tilderS, M_last)
        u_star = None
        max_marginal = 0
        for supplier in tilderS.difference(setM_last):
            marginal_supplier = self.compute_marginal_obj(tilderR, tilderS, p, q, setM_last, supplier)
            if marginal_supplier >= max_marginal:
                u_star = supplier
                max_marginal = marginal_supplier
        if u_star:  # if tilderS.difference(M_last) is empty, then u_star is None
            setM_last.add(u_star)

        return setM_last

    def compute_marginal_obj2(self, tilderR, tilderS, p, q, setM_last, supplier_bar):

        # objI, objW, objRI, objRW = self.compute_obj4(setM_last, tilderR, p, q)
        # objI_, objW_, objRI_, objRW_ = self.compute_obj4(setM_last.add(supplier_bar), tilderR, p, q)

        # 第一种方案, 直接算difference , 可能需要两倍的时间, 不知道准确性怎么样, 并且和论文里面的描述有点不同
        original_obj_list = self.compute_obj4(setM_last, tilderR, p, q)
        new_obj_list = self.compute_obj4(setM_last.add(supplier_bar), tilderR, p, q)
        marginal_obj = new_obj_list[self.OBJS.index(self.obj)] - original_obj_list[self.OBJS.index(self.obj)]
        return marginal_obj


    def compute_marginal_obj(self, tilderR, tilderS, p, q, setM_last, supplier_bar):
        # 第二种方案 直接用推导出来的计算式进行计算, 肯定更快, 严格按照论文里面的描述进行,
        # 但是需要分开写obj比较麻烦

        # for I and W
        objI_marginal = 0
        objW_marginal = 0
        objRI_marginal = 0
        objRW_marginal = 0
        for requester in tilderR:
            # todo 验证最后一个减数是干什么的
            reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[requester][requester]  # tau-1-0
            setI_supplier_bar = self.network.get_visible(supplier_bar, reduced_dist)

            # compute the part to setminus, contribution from selected suppliers setM_last
            setI_setM_last = set()
            for supplier in setM_last:
                reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[requester][requester]  # tau-1-0
                setI_setM_last.union(self.network.get_visible(supplier, reduced_dist))

            # compute the part to setminus, contribution from requester herself
            origin_tau_visible = self.network.get_visible(requester, self.network.tau)

            setI_requester_marginal = setI_supplier_bar.difference(setI_setM_last).difference(origin_tau_visible)
            objI_marginal += len(setI_requester_marginal)  # lower i is int, capital I is set
            objW_marginal += len(setI_requester_marginal) * self.network.valuations[requester]
            objRI_marginal += len(setI_requester_marginal) * (p-q)
            objRW_marginal += len(setI_requester_marginal) * (p-q*self.network.valuations[requester])

        obj2value = {'I':objI_marginal, 'W':objW_marginal, 'RI':objRI_marginal, 'RW':objRW_marginal}
        return obj2value[self.obj]
