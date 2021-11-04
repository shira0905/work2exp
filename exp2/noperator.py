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
import pandas as pd
import itertools
import datetime
from network import Network
import matplotlib.pyplot as plt
import pickle
from zutil import get_latest_path

import os
# import abc
# from abc import ABC, abstractmethod
#


class Noperator:
    """The class of an operator aim to maximize revenue"""

    def __init__(self, logger, network, obj, budget_list, grain):

        self.logger = logger
        self.network = network
        self.obj = obj

        self.PKL_DIR = "../eplots/pkl"
        self.PKL_PREFIX = f"{self.network.did}_{int(self.network.lamb)}_{self.obj}_{self.method}" # without method since attribute of subclass
        self.OBJS = ['I', 'W', 'RI', 'RW']


        self.budget_list = budget_list
        self.budget2scheme2optsolution = self.load_budget2scheme2optsolution()
        self.p_list_all = [round(x,2) for x in np.linspace(0, 1, num=grain + 1, endpoint=True)]  # todo: extend to epsilon=0
        self.q_list_all = [round(x,2) for x in np.linspace(0, 1, num=grain + 1, endpoint=True)]  # todo: extend to epsilon=0
        self.pq_list = list(itertools.product(self.p_list_all, self.q_list_all))

        # print(self.pq_list )


        # 这里的method是通过子类定义的





    # def opt_setM(self, budget, tilderR, tilderS, p , q):
    #     """subproblem 1, 依存于 get_M_method()
    #
    #     """
    #     optsolution = self.search_budget2scheme2optsolution(budget, tilderR, tilderS)
    #     if optsolution:
    #         setM_, objI_, objW_, objRI_, objRV_ = optsolution # 可以重用的 setM, objI, objW = setM_, objI_, objW_
    #         setM_star = setM_  # 当前所需肯定和所搜索的pkl相同的四个变量, 所以目标相同, 双边阵营相同 --> subproblem1的解相同. 和价格无关的objs也可以重用.
    #     else:
    #         setM_star = self.get_M_star(budget, tilderR, tilderS, p, q)
    #     return setM_star

    # def get_M_star(self, budget, tilderR, tilderS, p, q):
    #     pass


    def get_tilderR_tilderS(self, p, q):
        """Get participating requesters tilderR, potential participating tilderS
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

    def load_budget2scheme2optsolution(self):
        """Load the latest pkl under

        :return: budget2scheme2optsolution
        :rtype: dict
        """
        budget2scheme2optsolution = {}
        pklsrc = get_latest_path(self.PKL_DIR, self.PKL_PREFIX, 'pkl')
        if pklsrc != None:
            budget2scheme2optsolution = pickle.load(open(pklsrc, 'rb'))
        return budget2scheme2optsolution

    def search_budget2scheme2optsolution(self, budget, p, q): # 有错! 如果阵营相同, 目标相同, 价格不同, 那岂不是不能重用了
        """Search if given tilderR, tilderS has been computed in history.
        """
        if budget not in self.budget2scheme2optsolution.keys():
            return None
        scheme2optsolution = self.budget2scheme2optsolution[budget]
        if (p, q) not in scheme2optsolution:
            return None
        optsolution = scheme2optsolution[scheme2optsolution]
        return optsolution

    # def search_budget2scheme2optsolution(self, budget, tilderR, tilderS): # 有错! 如果阵营相同, 目标相同, 价格不同, 那岂不是不能重用了
    #     """Search if given tilderR, tilderS has been computed in history.
    #     """
    #     if budget not in self.budget2scheme2optsolution.keys():
    #         return None
    #     scheme2optsolution = self.budget2scheme2optsolution[budget]
    #     for scheme, optsolution in scheme2optsolution.items():
    #         p, q = scheme
    #         tilderR_history, tilderS_history = self.get_tilderR_tilderS(p, q)
    #         if tilderR_history == tilderR and tilderS_history == tilderS:
    #             return optsolution
    #     return None

    def dump_budget2scheme2optsolution(self):
        """Dump the  pkl with cur_time.

        :return: None
        :rtype: None
        """
        nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
        result_pkl_path = f"{self.PKL_DIR}/{self.PKL_PREFIX}_{nowTime}.pkl"
        # result_pkl_path = f"{self.PKL_DIR}/{self.PKL_PREFIX}.pkl"
        pickle.dump(self.budget2scheme2optsolution, open(result_pkl_path, 'wb'))


    def compute_obj4(self, M, tilderR, p, q):
        objI = 0
        objW = 0
        for requester in tilderR:
            setI_requester = set()
            for supplier in M:
                reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[requester][requester]
                setI_requester = setI_requester.union(self.network.get_visible(supplier, reduced_dist))
            ori_tau_vis = self.network.get_visible(requester, self.network.tau)
            setI_requester = setI_requester.difference(ori_tau_vis)
            objI += len(setI_requester)
            objW += len(setI_requester) * self.network.valuations[requester]
        objRI = p * objI - q * objI
        objRW = p * objI - q * objW
        return (objI, objW, objRI, objRW)

    def compute_objI(self, M, tilderR):
        objI = 0
        for requester in tilderR:
            setI_requester = set()
            for supplier in M:
                reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[requester][requester]
                setI_requester = setI_requester.union(self.network.get_visible(supplier, reduced_dist))
            ori_tau_vis = self.network.get_visible(requester, self.network.tau)
            setI_requester = setI_requester.difference(ori_tau_vis)
            objI += len(setI_requester)
        return objI

    def compute_objW(self, M, tilderR):
        objW = 0
        for requester in tilderR:
            setI_requester = set()
            for supplier in M:
                reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[requester][requester]
                setI_requester = setI_requester.union(self.network.get_visible(supplier, reduced_dist))
            ori_tau_vis = self.network.get_visible(requester, self.network.tau)
            setI_requester = setI_requester.difference(ori_tau_vis)
            objW += len(setI_requester)* self.network.valuations[requester]
        return objW


    def compute_objRI(self, M, tilderR, p, q):
        objI = 0
        for requester in tilderR:
            setI_requester = set()
            for supplier in M:
                reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[requester][requester]
                setI_requester = setI_requester.union(self.network.get_visible(supplier, reduced_dist))
            ori_tau_vis = self.network.get_visible(requester, self.network.tau)
            setI_requester = setI_requester.difference(ori_tau_vis)
            objI += len(setI_requester)
        objRI = (p-q) * objI
        return objRI

    def compute_objRW(self, M, tilderR, p, q):
        objI = 0
        objW = 0
        for requester in tilderR:
            setI_requester = set()
            for supplier in M:
                reduced_dist = self.network.tau - self.network.default_new_dist - self.network.spl[requester][requester]
                setI_requester = setI_requester.union(self.network.get_visible(supplier, reduced_dist))
            ori_tau_vis = self.network.get_visible(requester, self.network.tau)
            setI_requester = setI_requester.difference(ori_tau_vis)
            objI += len(setI_requester)
            objW += len(setI_requester) * self.network.valuations[requester]
        objRW = p * objI - q  * objW
        return objRW

