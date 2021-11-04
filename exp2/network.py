#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/9/4 12:18
@Desc    :
'''

import networkx as nx
import pickle
# from zutil import *
import random
import math
import numpy as np
import os


class Network:
    """The class of the network"""
    dataset_dict = {
        'd1': ('residence', 217, 2, 'uw', 1, 0.25),
        'd2': ('blog', 1224, 2, 'uw', 1, 0.1),
        'd3': ('dblp', 10000, 2, 'uw', 1, 0.1),
        'd4': ('residence', 217, 3, 'uw', 1, 0.25),
        'd5': ('blog', 1224, 3, 'uw', 1, 0.1),
        'd6': ('dblp', 10000, 3, 'uw', 1, 0.1)
    }
    #         'd3': ('facebook', 5908, 2, 'uw', 1, 0.05),

    def __init__(self, logger, did, seed, lamb):
        self.logger = logger

        self.did = did
        self.seed = seed
        self.lamb = lamb
        self.data_name, self.data_size, self.tau, self.data_weighted, self.default_new_dist, self.percentage = Network.dataset_dict[did]
        self.graph = self.create_graph()
        self.spl = self.compute_spl()

        self.R, self.S = self.random_RS(self.percentage, self.percentage)  # requester set, suppolie set


        # self.beta_paras = [float(x) for x in beta_paras.split(',')]
        # self.valuations, self.costs = self.random_valuations_costs_beta(self.beta_paras[0:2],
        #                                                                 self.beta_paras[2:4])  # 0 if nor S either R

        self.valuations, self.costs = self.generate_valuations_costs_func(lamb)

    def create_graph(self):
        """get nx graph

        :return: nx graph
        :rtype:
        """
        data_path = f"../zdata/{self.data_name}_{self.data_size}.txt"
        graph = nx.read_edgelist(data_path, nodetype=int, data=(('weight', float),), create_using=nx.DiGraph())
        # self.logger.info(len(graph.nodes))
        [graph.add_node(i) for i in range(self.data_size) if i not in graph.nodes]
        # self.logger.info(len(graph.nodes))
        return graph

    def compute_spl(self):
        """get shortest path length for all the pairs

        If spl does not exist, compute and pickle sump; pickle load otherwise

        :return: set self.spl
        :rtype: dict
        """
        filename = f"../zdata/{self.data_name}_{self.data_size}_spl.pkl"
        if os.path.exists(filename):
            spl_pkl_file = open(filename, 'rb')
            spl = pickle.load(spl_pkl_file)
            self.logger.info(f'load:{filename}')
        else:
            spl = dict(nx.all_pairs_shortest_path_length(self.graph))
            spl_pkl_file = open(filename, 'wb')
            pickle.dump(spl, spl_pkl_file)

        # head_dict(None, spl, 2)
        return spl

    def get_visible(self, origin, dist):
        """Get the set who is <= dist far away from original

        :param origin: the center node
        :type origin:
        :param dist: the distance threshold, not necessarily tau
        :type dist:
        :return: dist-visible set
        :rtype: Set
        """
        """
        local information cannot > tau, so we can filter from spl
        """
        visible = set()
        tau_visible_dict = self.spl[origin]
        for i in tau_visible_dict:
            if tau_visible_dict[i] <= dist:
                visible.add(i)
        return visible

    def random_RS(self, percent_R, percent_S):
        """Random requester set R and supplier set S

        Need attributes: self.seed, self.data_size,

        :param percent_R:
        :type percent_R:
        :param percent_S:
        :type percent_S:
        :return: R, S
        :rtype:
        """
        random.seed(self.seed)
        num_total = random.sample(range(0, self.data_size),
                                  math.ceil((percent_R + percent_S) * self.data_size))
        num_R = math.ceil(percent_R * self.data_size)
        num_S = math.ceil(percent_S * self.data_size)
        R = num_total[:num_R]  # R is R in paper, R_ is ~R in paper
        S = num_total[num_S:]
        self.logger.info(f'Finish random requester set R and supplier set S \n \
                            percent_R={percent_R}, num_R={num_R}, len_R={len(R)} \n \
                            percent_S={percent_S}, num_S={num_S}, len_S={len(S)}')
        return R, S

    def random_valuations_costs_beta(self, v_beta_paras, c_beta_paras):
        """Random valuations using v_beta_paras for R and costs using c_beta_paras for S.

        Need attributes: self.seed, self.data_size, self.R, self.S

        :param v_beta_paras:
        :type v_beta_paras:
        :param c_beta_paras:
        :type c_beta_paras:
        :return: valuations, costs
        :rtype:
        """
        valuations, costs = np.zeros(self.data_size), np.zeros(self.data_size)
        np.random.seed(self.seed)
        v = np.random.beta(v_beta_paras[0], v_beta_paras[1], len(self.R))
        for i, r in enumerate(self.R):
            valuations[r] = v[i]
        c = np.random.beta(c_beta_paras[0], c_beta_paras[1], len(self.S))
        for i, s in enumerate(self.S):
            costs[s] = c[i]
        self.logger.info(f"Finish random valuations using v_beta_paras for R and costs using c_beta_paras for S")
        return valuations, costs

    def generate_valuations_costs_func(self, lamb):
        """Generate valuations {p_u} based on function p(visibility)
        and generate costs {q_u} based on f  unction q(visibility).

        TODO: Plot the distributions to see if reasonable function definition.

        :param lamb:
        :type lamb:
        :return: valuations, costs as attributions of objective Network
        :rtype:
        """
        node2degree = {}
        for node in self.graph.nodes():
            node2degree[node] = len(self.graph[node])

        node2visibility = {}
        for node in self.graph.nodes():
            visible_set = self.get_visible(node, self.tau)
            node2visibility[node] = len(visible_set)
        vis_max = sorted(node2visibility.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[0][1]

        # node2valuation = {}
        # node2cost = {}
        valuations = []
        costs = []
        for node in range(len(self.graph.nodes())):
            visibility = len(self.get_visible(node, self.tau))
            valuation = math.pow( (1+(visibility/vis_max)), lamb) / math.pow(2, lamb)
            cost = 1-math.pow( (1+(visibility/vis_max)), lamb) / math.pow(2, lamb)
            valuations.append(valuation)
            costs.append(cost)
        #     node2valuation[node] = valuation
        #     node2cost[node] = cost

        # plt.hist(node2valuation.values(), bins=10)
        # plt.savefig(f"../eplots/{self.did}_dist_valuation.pdf", dpi=300, bbox_inches="tight", format='pdf')
        # plt.clf()
        # plt.hist(node2cost.values(), bins=10)
        # plt.savefig(f"../eplots/{self.did}_dist_cost.pdf", dpi=300, bbox_inches="tight", format='pdf')
        # plt.clf()
        # self.logger.info(f"Finish generate valuations and costs using using lamb={lamb}")

        # x = np.linspace(0, vis_max, vis_max+1)
        # y = [math.pow( (1+(visibility/vis_max)), lamb) / math.pow(2, lamb) for visibility in x]
        # plt.plot(x, y)
        # plt.savefig(f"../eplots/{self.did}_curve_valuation.pdf", dpi=300, bbox_inches="tight", format='pdf')
        # plt.clf()
        #
        # x = np.linspace(0, vis_max, vis_max+1)
        # y = [1-math.pow( (1+(visibility/vis_max)), lamb) / math.pow(2, lamb) for visibility in x]
        # plt.plot(x, y)
        # plt.savefig(f"../eplots/{self.did}_curve_cost.pdf", dpi=300, bbox_inches="tight", format='pdf')
        # plt.clf()

        # s = f"node, degree, visibility, valuation, cost \n"
        # for node in range(len(self.graph.nodes())):
        #     s += f"{node}, {node2degree[node]}, {node2visibility[node]}, {node2valuation[node]}, {node2cost[node]} \n"
        # self.logger.info(f"information of the network: \n {s}")
        return valuations, costs
