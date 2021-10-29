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

# import abc
# from abc import ABC, abstractmethod
#


class Noperator:
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


    def compute(self):
        pass

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
