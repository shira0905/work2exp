#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/11/3 20:37
@Desc    :
"""

import itertools
from noperator import Noperator

class H2Operator(Noperator):
    """Opertor uaw method h2 degree (h1 too good...)"""

    def __init__(self, logger, network, obj, budget_list, grain):
        self.method = 'h2'
        Noperator.__init__(self, logger, network, obj, budget_list, grain)

    def opt_price(self):
        """依存于opt_setM()
        """

        for budget in self.budget_list:
            if budget not in self.budget2scheme2optsolution:
                self.budget2scheme2optsolution[budget] = {}

            # STEP1: compute and record for all (p,q) # 给定 did, lamb, obj, method, 给定 budget, 这个方法只是记录了所有搜索到的scheme,
            for (p, q) in self.pq_list:   # 里面的循环是algorithm 1了
                tilderR, tilderS = self.get_tilderR_tilderS(p, q)
                # setM_star = self.opt_setM(budget, tilderR, tilderS, p, q)
                setM_star = self.get_M_star(budget, tilderR, tilderS, p, q)
                objI, objW, objRI, objRW = self.compute_obj4(setM_star, tilderR, p, q)
                self.budget2scheme2optsolution[budget][(p, q)] = (setM_star, objI, objW, objRI, objRW)

        self.dump_budget2scheme2optsolution()

    def get_M_star(self, budget, tilderR, tilderS, p , q): # 用不到的参数为了统一接口
        """
        """
        setM_star = set()
        node2degree = {}
        for node in tilderS:
            setsize = len(self.network.graph[node])
            node2degree[node] = setsize

        sorted_node2degree = sorted(node2degree.items(), key=lambda kv: kv[1], reverse=True)
        cnt = 0
        while cnt < len(sorted_node2degree):
            if len(setM_star) == budget:
                break
            # if node2vis_sorted[cnt][0] not the neigboe of all the reqiesters, ignore ignore
            setM_star.add(sorted_node2degree[cnt][0])
            cnt += 1
        return setM_star


