#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/9/13 15:10
@Desc    :   For results presentation: (1) format the experiment results, (2) plot as figures
'''

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from zutil import *
from network import Network
# from trash.netoperatorREV import NetoperatorREV
from netoperator import Netoperator
import itertools
import math
import os
import pickle
from matplotlib.ticker import LinearLocator
from matplotlib import cm
import matplotlib.pyplot as plt

class Analyst:
    font = {'family': 'Times New Roman', 'weight': 'bold', 'size': 20}
    font_legend = {'family': 'Times New Roman', 'weight': 'bold', 'size': 18}
    hatch_list = ['', "///", "\\\\\\", '---', '...', '*']

    result_item = ['M', 'increase',  'rev', 'sw']
    def __init__(self, logger, ):
        self.logger = logger

    def generate_csv_from_pkl(self, did, method_list, obj, budget_list, grain, gamma):
        """load required result pkls and conbine them into one csv

        """
        grain_p = grain
        grain_alpha = grain
        method2budget2scheme2result = {}
        for method in method_list:
            result_pkl_list =sorted([d for d in os.listdir(f"../eplots/pkl{str(gamma).replace('.','')}") if f"{did}_{method}_{obj}" in d and '.pkl' in d])
            if len(result_pkl_list) > 0:
                budget2scheme2result = pickle.load(open(f"../eplots/pkl{str(gamma).replace('.','')}/{result_pkl_list[-1]}", 'rb'))
                method2budget2scheme2result[method] = budget2scheme2result
            else:
                self.logger.info("No result pkl!")
        # 直接写加载pkl，而不是通过 Netoperator的属性，这样就不用创建对象了 【copy代码保持绝对一致】

        p_list_all = np.linspace(0, 1, num=grain_p + 1, endpoint=True)  # todo: extend to epsilon=0
        alpha_list_all = np.linspace(0, 1, num=grain_alpha + 1, endpoint=True)  # todo: extend to epsilon=0

        row_list = []
        palpha_list = list(itertools.product(p_list_all, alpha_list_all))
        row_head1, row_head2, row_head3 = ['p', 'alpha'], ['p', 'alpha'], ['p', 'alpha']
        for b in budget_list:
            for i, method in enumerate(method_list):
                row_head1.extend([b] * 4)
                row_head2.extend([method]*4)
                row_head3.extend(Analyst.result_item)
        row_list.extend([row_head1, row_head2, row_head3])


        for (p, alpha) in palpha_list:
            # q = alpha * p
            row = [p, alpha]
            for b in budget_list:
                for method in method_list:
                    result = method2budget2scheme2result[method][b][(p, alpha)]
                    row.extend(result)
            row_list.append(row)

        data = pd.DataFrame(row_list)
        print('data is like:')
        print(data)
        data.to_csv(f"../eplots/exp{str(gamma).replace('.','')}/{did}_O{obj}_E{grain}.csv", index=False, header=False, sep='\t')
        # message = f"generate_csv_from_pkl() generate or update ../eplots/exp/{did}_{obj}_{grain_p}-{grain_alpha}.csv"
    #
    #
    # def extract_axisvalue_from_csv(self, did, obj, grain, budget_list, method_list): # 这些参数就可以定位到一个csv了
    #     """ analysis the csv, using operation like sort, max, slice and so on.
    #     (1) load csv as df
    #     (2) operate df as needed
    #     (3) return the list of dictionary needed for plot
    #     """
    #     df = pd.read_csv(f'../eplots/{did}_{obj}_{grain}.csv', header=[0, 1, 2], sep='\t')
    #     X = budget_list
    #     legend2Y = {}
    #     for method in method_list:
    #         legend2Y[method] = []
    #     objseq = Analyst.result_item.index(obj)
    #     print(objseq)
    #     for budget in budget_list:
    #         for i,method in enumerate(method_list):
    #             i_obj = 2 + objseq + len(Analyst.result_item)*i*budget
    #             argmax_obj = df.iloc[:, i_obj].argmax()
    #             opt_scheme = df.iloc[argmax_obj, 0: 2].tolist()
    #             opt_result = df.iloc[argmax_obj, i_obj-objseq : i_obj-objseq+4].tolist()
    #             legend2Y[method].append(opt_result[objseq])
    #             self.logger.info(f"when budget={budget}, method={method}, \n\t opt_scheme={opt_scheme}, \n\t opt_result={opt_result}")
    #
    #     return X, legend2Y

    def plot_from_pkl_3d(self, did, obj, budget, grain, method, gamma):  # grain?, methid_list? if can 2 surfaces

        result_pkl_list = sorted([d for d in os.listdir(f"../eplots/pkl{str(gamma).replace('.','')}") if f"{did}_{method}_{obj}" in d and '.pkl' in d])
        if len(result_pkl_list) > 0:
            budget2scheme2result = pickle.load(open(f"../eplots/pkl{str(gamma).replace('.','')}/{result_pkl_list[-1]}", 'rb'))
        else:
            self.logger.info("No result pkl!")
        xlabel = "p" # 应该就只能是这个了
        ylabel = "alpha"  # or "social welfare"
        zlabel = obj
        X = np.linspace(0, 1, num=grain + 1, endpoint=True)
        Y = np.linspace(0, 1, num=grain + 1, endpoint=True)  # alpha or p?
        X, Y = np.meshgrid(X, Y)
        numx, numy = X.shape
        Z = np.zeros(X.shape)
        max_obj = 0
        max_scheme = (-1, -1)
        for i in range(numx):
            for j in range(numy):
                x, y = X[i][j], Y[i][j]
                result = budget2scheme2result[budget][(x, y)]  # If the scheme key == (p,q)
                # result = scheme2result[(x, y)]  # If the scheme key == (p,alpha)
                Z[i][j] = result[Analyst.result_item.index(obj)]
                if Z[i][j] >= max_obj:
                    max_obj = Z[i][j]
                    max_scheme = (x, y)
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

        ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False, alpha=0.5)
        ax.scatter(max_scheme[0], max_scheme[1], max_obj, s=5)
        s = f"({'%.2f'% max_scheme[0]},{ '%.2f'% max_scheme[1]}), {'%.2f'% max_obj}"
        ax.text(max_scheme[0], max_scheme[1], max_obj, s)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel);
        plt.savefig(f"../eplots/exp{str(gamma).replace('.','')}/{did}_X{xlabel}_Y{ylabel}_Z{zlabel}-B{budget}_E{grain}_M{method}.pdf", dpi=300, bbox_inches="tight", format='pdf')


    # def plot_from_axisvalue_epsilon(self, did, epsilon_list, epsilon2axisvalue, obj):
    #     """ each epsilon plot one figure
    #     """
    #     xlabel = "budget" # 应该就只能是这个了
    #     ylabel = obj  # or "social welfare"
    #     legends = '+'.join(  epsilon2axisvalue.values()[0][1].keys() )  # for naming plot
    #     print(legends)
    #     for epsilon in epsilon_list:
    #         X, legend2Y = epsilon2axisvalue[epsilon]
    #         for legend, Y in legend2Y.items():
    #             plt.rc('font', **Analyst.font)
    #             plt.plot(X, Y, label=legend)
    #             plt.legend()
    #             plt.xlabel(xlabel)
    #             plt.ylabel(ylabel)
    #             plt.savefig(f"../eplots/exp/{did}_X{xlabel}_Y{ylabel}_L{legends}-E{epsilon}_O{obj}.pdf", dpi=300, bbox_inches="tight", format='pdf')
    #             plt.clf()
    #     pass
        # each epsilon plot one figure
    def plot_from_axisvalue_epsilon(self, did, budget_list, obj, method_list, grain, gamma):
        """ each budget plot one figure
        """
        xlabel = "budget"  # 应该就只能是这个了
        ylabel = obj  # or "social welfare"
        legends = '+'.join(method_list)  # for naming plot
        X = budget_list
        legend2Y = {}
        for method in method_list:
            legend2Y[method] = []

        method2budget2scheme2result = {}
        for method in method_list:
            result_pkl_list = sorted([d for d in os.listdir(f"../eplots/pkl{str(gamma).replace('.','')}") if f"{did}_{method}_{obj}" in d and '.pkl' in d])
            if len(result_pkl_list) > 0:
                budget2scheme2result = pickle.load(open(f"../eplots/pkl{str(gamma).replace('.','')}/{result_pkl_list[-1]}", 'rb'))
                method2budget2scheme2result[method] = budget2scheme2result
            else:
                self.logger.info("No result pkl!")

        p_list = np.linspace(0, 1, num=grain + 1, endpoint=True)
        alpha_list = np.linspace(0, 1, num=grain + 1, endpoint=True)
        palpha_list = list(itertools.product(p_list, alpha_list))
        for budget in budget_list:
            for method in method_list:
                max_obj = 0
                max_scheme = (-1, -1)
                for (p, alpha) in palpha_list:
                    obj_value = method2budget2scheme2result[method][budget][(p, alpha)][Analyst.result_item.index(obj)]
                    if obj_value > max_obj:
                        max_obj = obj_value
                        max_scheme = (p, alpha)
                legend2Y[method].append(max_obj)

        plt.rc('font', **Analyst.font)
        width = 0.28

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        X_ = np.arange(1, len(budget_list) + 1)
        plt.xticks(X_ + width / 2, budget_list)  # .set_xticklabels(budget_list)
        for i, legend in enumerate(legend2Y.keys()):  # 每个横坐标点又几根柱子
            plt.bar(X_ + i * width, legend2Y[legend], width, alpha=1, linewidth=1.8,
                    color='white', edgecolor='black', hatch=Analyst.hatch_list[i], label=legend)

            for a, b in zip(X_ + i * width, legend2Y[legend]):
                plt.text(a, b + 0.05, '%.2f' % b, ha='center', va='bottom', fontsize=12)
        plt.legend(loc='lower right')
        plt.savefig(f"../eplots/exp{str(gamma).replace('.','')}/{did}_X{xlabel}_Y{ylabel}_L{legends}-E{grain}.pdf", dpi=300, bbox_inches="tight", format='pdf')
        plt.clf()

    def plot_from_axisvalue_budget(self, did, budget, obj, method_list, grain_list, gamma):
        """ each budget plot one figure
        """
        xlabel = "epsilon"  # 应该就只能是这个了
        ylabel = obj  # or "social welfare"
        legends = '+'.join(method_list)  # for naming plot
        X = grain_list
        legend2Y = {}
        for method in method_list:
            legend2Y[method] = []

        method2budget2scheme2result = {}
        for method in method_list:
            result_pkl_list = sorted([d for d in os.listdir(f"../eplots/pkl{str(gamma).replace('.','')}") if f"{did}_{method}_{obj}" in d and '.pkl' in d])
            if len(result_pkl_list) > 0:
                budget2scheme2result = pickle.load(open(f"../eplots/pkl{str(gamma).replace('.','')}/{result_pkl_list[-1]}", 'rb'))
                method2budget2scheme2result[method] = budget2scheme2result
            else:
                self.logger.info("No result pkl!")

        for grain in grain_list:
            p_list = np.linspace(0, 1, num=grain + 1, endpoint=True)
            alpha_list = np.linspace(0, 1, num=grain + 1, endpoint=True)
            palpha_list = list(itertools.product(p_list, alpha_list))
            for method in method_list:
                max_obj = 0
                max_scheme = (-1, -1)
                for (p, alpha) in palpha_list:
                    obj_value = method2budget2scheme2result[method][budget][(p, alpha)][Analyst.result_item.index(obj)]
                    if obj_value > max_obj:
                        max_obj = obj_value
                        max_scheme = (p, alpha)
                legend2Y[method].append(max_obj)

        plt.rc('font', **Analyst.font)
        width = 0.28

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        X_ = np.arange(1, len(grain_list) + 1)
        plt.xticks(X_ + width / 2, grain_list)  # .set_xticklabels(budget_list)
        for i, legend in enumerate(legend2Y.keys()):  # 每个横坐标点又几根柱子
            plt.bar(X_ + i * width, legend2Y[legend], width, alpha=1, linewidth=1.8,
                   color='white', edgecolor='black', hatch=Analyst.hatch_list[i], label=legend)

            for a, b in zip(X_ + i * width, legend2Y[legend]):
                plt.text(a, b + 0.05, '%.2f' % b, ha='center', va='bottom', fontsize=12)
        plt.legend(loc='lower right')
        plt.savefig(f"../eplots/exp{str(gamma).replace('.','')}/{did}_X{xlabel}_Y{ylabel}_L{legends}-B{budget}.pdf", dpi=300, bbox_inches="tight", format='pdf')
        plt.clf()
    #
    # def plot2(exp_v, data_name, Y_lable_list, budget_list, Y_list):
    #     X = np.arange(1, len(budget_list) + 1)  # 总共有多少个横坐标点
    #     plt.rc('font', **font)
    #     width = 0.28
    #     fig, ax = plt.subplots()
    #     for i, Y in enumerate(Y_list):  # 每个横坐标点又几根柱子
    #         # if i==0:
    #         #     continue
    #         ax.bar(X + i * width, Y, width, alpha=1, linewidth=1.8, color='white', edgecolor='black',
    #                hatch=hatch_list[i], label=Y_lable_list[i])
    #
    #     ax.set_xticks(X + width / 2)  # 将坐标设置在指定位置
    #     ax.set_xticklabels(budget_list)  # 将横坐标替换成
    #     ax.set_xlabel('budget', font)
    #     ax.set_ylabel("revenue", font)
    #     plt.legend(loc="lower right", prop=font_legend)
    #     # plt.legend(loc='best',frameon=False)
    #     command = f"mkdir -p plots{exp_v}"
    #     print('Subprocess: \"' + command + '\"')
    #     subprocess.run(command, shell=True)
    #     plt.savefig(f'plots{exp_v}/{data_name}_f_b_3methods_uppers.pdf', dpi=300, bbox_inches="tight", format='pdf')
    #     plt.clf()

    def plot_dist(self, network, curvename_list, bin):
        """Plot hist to show the distribution of given list. curvename =[]
        """
        node2degree = {}
        for node in network.graph.nodes():
            node2degree[node] = len(network.graph[node])
        deg_max = sorted(node2degree.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[0][1]

        node2visibility = {}
        for node in network.graph.nodes():
            node2visibility[node] = len(network.get_visible(node, network.tau))
        vis_max = sorted(node2visibility.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[0][1]

        for curvename in curvename_list:
            node2curvevalue = {}
            for node in range(len(network.graph.nodes())):
                # visibility = len(network.get_visible(node, network.tau))
                visibility = node2visibility[node]
                degree = node2degree[node]
                if curvename == 'p':
                    curvevalue = math.pow((1 + (visibility / vis_max)), network.gamma) / math.pow(2, network.gamma)
                if curvename == 'q':
                    curvevalue = 1 - math.pow((1 + (visibility / vis_max)), network.gamma) / math.pow(2, network.gamma)
                if curvename == 'p_deg':
                    curvevalue = math.pow((1 + (degree / deg_max)), network.gamma) / math.pow(2, network.gamma)
                if curvename == 'q_deg':
                    curvevalue = 1 - math.pow((1 + (degree / deg_max)), network.gamma) / math.pow(2, network.gamma)
                if curvename == 'vis':
                    curvevalue = visibility
                if curvename == 'deg':
                    curvevalue = node2degree[node]
                node2curvevalue[node] = curvevalue
            plt.hist(node2curvevalue.values(), bins=bin)
            if curvename=='vis' or curvename=='deg':
                figname = f" {network.did}_dist_{curvename}"
            else:
                figname = f" {network.did}_dist_{curvename}_G{network.gamma}"
            plt.savefig(f"../eplots/net/{figname.replace('.','')}.pdf", dpi=300, bbox_inches="tight", format='pdf')
            plt.clf()

    # def plot_curve(self, network, curvename_list):
    #     """Depend on vis_max and gamma
    #     """
    #     node2visibility = {}
    #     for node in network.graph.nodes():
    #         visible_set = network.get_visible(node, network.tau)
    #         node2visibility[node] = len(visible_set)
    #     vis_max = sorted(node2visibility.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[0][1]
    #     x = np.linspace(0, vis_max, vis_max + 1)
    #     if "p" in curvename_list:
    #         y = [math.pow((1 + (visibility / vis_max)), network.gamma) / math.pow(2, network.gamma) for visibility in x]
    #         plt.plot(x, y)
    #         figname = f"{network.did}_curve_p_G{network.gamma}"
    #         plt.savefig(f"../eplots/{figname.replace('.','')}.pdf", dpi=300, bbox_inches="tight", format='pdf')
    #         plt.clf()
    #     if "q" in curvename_list:
    #         y = [1 - math.pow((1 + (visibility / vis_max)), network.gamma) / math.pow(2, network.gamma) for visibility in x]
    #         plt.plot(x, y)
    #         figname = f"{network.did}_curve_q_G{network.gamma}"
    #         plt.savefig(f"../eplots/{figname.replace('.','')}.pdf", dpi=300, bbox_inches="tight", format='pdf')
    #         plt.clf()

    def plot_curve_single(self, network, curvename_list, gamma_list):
        """Depend on vis_max and gamma
        """
        node2visibility = {}
        for node in network.graph.nodes():
            visible_set = network.get_visible(node, network.tau)
            node2visibility[node] = len(visible_set)
        vis_max = sorted(node2visibility.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[0][1]
        x = np.linspace(0, vis_max, vis_max + 1)
        if "p" in curvename_list:
            for gamma in gamma_list:
                y = [math.pow((1 + (visibility / vis_max)), gamma) / math.pow(2, gamma) for visibility in x]
                plt.plot(x, y, label=gamma)
            plt.xlabel('visibility of u')
            plt.ylabel('p of u')
            plt.legend()
            figname = f"{network.did}_curve_p"
            plt.savefig(f"../eplots/net/{figname.replace('.', '')}.pdf", dpi=300, bbox_inches="tight", format='pdf')
            plt.clf()
        if "q" in curvename_list:
            for gamma in gamma_list:
                y = [1 - math.pow((1 + (visibility / vis_max)), gamma) / math.pow(2, gamma) for visibility in x]
                plt.plot(x, y)
            plt.xlabel('visibility of u')
            plt.ylabel('q of u')
            plt.legend()
            figname = f"{network.did}_curve_q"
            plt.savefig(f"../eplots/net/{figname.replace('.', '')}.pdf", dpi=300, bbox_inches="tight", format='pdf')
            plt.clf()

    # def plot_from_pkl_3d_ml(self, did, obj, budget, grain, method_list):  # grain?, methid_list? if can 2 surfaces
    #     """ analysis the csv, using operation like sort, max, slice and so on.
    #     (1) load csv as df
    #     (2) operate df as needed
    #     (3) return the list of dictionary needed for plot
    #     """
    #     # df = pd.read_csv(f'../eplots/{did}_{obj}_{grain}.csv', header=[0, 1, 2], sep='\t')
    #     method2budget2scheme2result = {}
    #     for method in method_list:
    #         result_pkl_list =sorted([d for d in os.listdir(f"../eplots") if f"{did}_{method}_{obj}" in d and '.pkl' in d])
    #         if len(result_pkl_list) > 0:
    #             budget2scheme2result = pickle.load(open(f"../eplots/{result_pkl_list[-1]}", 'rb'))
    #             method2budget2scheme2result[method] = budget2scheme2result
    #         else:
    #             self.logger.info("No result pkl!")
    #
    #     X = np.linspace(0, 1, num=grain + 1, endpoint=True)
    #     Y = np.linspace(0, 1, num=grain + 1, endpoint=True)
    #     X, Y = np.meshgrid(X, Y)
    #
    #     legend2Z = {}
    #     numx, numy = X.shape
    #     for method in method_list:
    #         scheme2result = method2budget2scheme2result[method][budget]
    #         print(scheme2result)
    #         Z = np.zeros(X.shape)
    #         for i in range(numx):
    #             for j in range(numy):
    #                 x, y = X[i][j], Y[i][j]
    #                 result = scheme2result[(x, y)]  # If the scheme key == (p,q)
    #                 # result = scheme2result[(x, y)]  # If the scheme key == (p,alpha)
    #                 Z[i][j] = result[Analyst.result_item.index(obj)]
    #         legend2Z[method] = Z
    #     colors = ['red', 'blue']
    #
    #     # for legend,Z in legend2Z.items():
    #     fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    #     ax.plot_surface(X, Y, legend2Z['brute'], color='red', linewidth=0, antialiased=False, alpha=0.3) #cmap=cm.coolwarm
    #     ax.plot_surface(X, Y, legend2Z['greedy'], color='blue', linewidth=0, antialiased=False, alpha=0.3)  # cmap=cm.coolwarm
    #     plt.show()
