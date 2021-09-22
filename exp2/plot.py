#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/9/13 15:10
@Desc    :   For results presentation: (1) format the experiment results, (2) plot as figures
'''

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from zutil import *
from network import Network
from netoperatorREV import NetoperatorREV
from netoperatorSW import NetoperatorSW
import itertools
import math

font = {'family': 'Times New Roman','weight': 'bold','size': 20}
font_legend = {'family': 'Times New Roman','weight': 'bold','size': 18}
hatch_list = ['', "///", "\\\\\\", '---', '...', '*']
def main():
    args, unk = get_parser().parse_known_args()
    logger, logname = get_log(args.did, 'plot', args.version)
    logger.info(args)
    network = Network(logger, args.did, args.seed, args.percent_R, args.percent_S, int(args.gamma))
    if args.rev:
        format_rev(args, logger)
    if args.sw:
        format_sw(args, logger)
    if args.stat:
        plot_distribution_degree(network, args, logger)
        plot_distribution_visibility(network, args, logger)
        plot_distribution_valuation(network, args, logger)
        plot_distribution_cost(network, args, logger)
        plot_function_valuation(network, args, logger)
        plot_function_cost(network, args, logger)
    if args.extract:
        extract_csv_rev(logger)
        extract_csv_sw(logger)
    # plot_rev(network)
    # plot_sw(network)
    extract_3d(args,logger)

def plot_csv(network):
    core_brute = [[435.0214416896235, 790.9553902662993, 1070.601395775941, 1336.3753535353535],
                  [435.0214416896235, 790.9553902662993, 1070.601395775941, 1336.3753535353535],
                  [435.0214416896235, 790.9553902662993, 1070.601395775941, 1336.3753535353535]]

    core_greedy = [[435.0214416896235, 732.4187052341597, 1053.3110835629016, 1303.3817171717171],
                [435.0214416896235, 734.4488797061522, 1053.3110835629016, 1303.3817171717171],
                [435.0214416896235, 752.2152249770431, 1053.3110835629016, 1307.4058953168046]]

    core_brute_trans = np.transpose(core_brute)
    core_greedy_trans = np.transpose(core_greedy)
    print(core_greedy_trans)

    budget_list = [1, 2, 3, 4]
    X = [0.2, 0.1, 0.05]
    for i, budget in enumerate(budget_list):
        Y_brute = core_brute_trans[i]
        Y_greedy = core_greedy_trans[i]
        plt.plot(budget_list, Y_brute, marker='+', label='brute-force' )
        plt.plot(budget_list, Y_greedy, marker='x', label='greedy')
        plt.xlabel("budget")
        plt.ylabel("social welfare")
        plt.legend()
        plt.savefig(f"../eplots/{network.did}_{budget}.pdf", dpi=300, bbox_inches="tight", format='pdf')
        plt.clf()

def plot_rev(network):
    core_brute = [[134.4, 215.52, 242.23999999999995, 292.96], [141.68, 229.4, 292.6, 292.96], [151.20000000000005, 254.61, 321.86, 321.86]]
    core_greedy = [[134.4, 215.52, 241.6, 278.72], [141.68, 229.4, 292.6, 292.6], [151.20000000000005, 254.61, 321.86, 321.86]]
    budget_list = [1, 2, 3, 4]
    X = [0.2, 0.1, 0.05]
    for i,epsilon in enumerate(X):
        Y_brute = core_brute[i]
        Y_greedy = core_greedy[i]
        plt.rc('font', **font)
        plt.plot(budget_list, Y_brute, marker='+', label='brute-force' )
        plt.plot(budget_list, Y_greedy, marker='x', label='greedy')
        plt.xlabel("budget")
        plt.ylabel("revenue")
        plt.legend()
        plt.savefig(f"../eplots/{network.did}_b2OgOb_epsilon{str(epsilon).replace('.','')}_rev.pdf", dpi=300, bbox_inches="tight", format='pdf')
        plt.clf()

def plot_sw(network):
    core_brute = [[435.0214416896235, 790.9553902662993, 1070.601395775941, 1336.3753535353535],
                  [435.0214416896235, 790.9553902662993, 1070.601395775941, 1336.3753535353535],
                  [435.0214416896235, 790.9553902662993, 1070.601395775941, 1336.3753535353535]]

    core_greedy = [[435.0214416896235, 732.4187052341597, 1053.3110835629016, 1303.3817171717171],
                   [435.0214416896235, 734.4488797061522, 1053.3110835629016, 1303.3817171717171],
                   [435.0214416896235, 752.2152249770431, 1053.3110835629016, 1307.4058953168046]]


    budget_list = [1, 2, 3, 4]
    X = [0.2, 0.1, 0.05]
    for i,epsilon in enumerate(X):
        Y_brute = core_brute[i]
        Y_greedy = core_greedy[i]
        plt.rc('font', **font)
        plt.plot(range(len(budget_list)), Y_brute, marker='+' ,label='brute-force' )
        plt.plot(range(len(budget_list)), Y_greedy, marker='o', label='greedy')
        plt.xlabel("budget")
        plt.ylabel("social welfare")
        plt.legend()
        plt.savefig(f"../eplots/{network.did}_b2OgOb_epsilon{str(epsilon).replace('.','')}_sw.pdf", dpi=300, bbox_inches="tight", format='pdf')
        plt.clf()

def extract_3d(args, logger):
    # budget_list = [int(x) for x in args.budget_list.split(',')]
    # network = Network(logger, args.did, args.seed, args.percent_R, args.percent_S, int(args.gamma))
    #
    # netoperator_brute = NetoperatorREV(logger, network, args.version, 'brute', int(args.grain_p), int(args.grain_alpha))
    # netoperator_greedy = NetoperatorREV(logger, network, args.version, 'greedy', int(args.grain_p),
    #                                     int(args.grain_alpha))
    # res_brute = netoperator_brute.budget2scheme2result
    # res_greedy = netoperator_greedy.budget2scheme2result
    #
    # row_list = []
    # palpha_list = list(itertools.product(netoperator_brute.p_list_all, netoperator_brute.alpha_list_all))
    #
    # # index_brute_M = index_brute_M_start + 6 * j
    # index_brute_obj = index_brute_M_start + 6 * j + 2
    # index_greedy_M = index_brute_M_start + 6 * j + 3
    # index_greedy_obj = index_brute_M_start + 6 * j + 5
    #
    # for (p, alpha) in palpha_list:
    #     q = alpha * p
    #     tilderR, tilderS = netoperator_brute.get_tilderR_tilderS(p, q)
    #     row = [p, alpha, q, (p, q), len(tilderR), len(tilderS)]
    #
    #     for b in budget_list:
    #         if len(res_brute[b][(p, q)][0]) == 0:
    #             row.append('{}')
    #         else:
    #             row.append(res_brute[b][(p, q)][0])
    #         row.append(res_brute[b][(p, q)][1])
    #         row.append(res_brute[b][(p, q)][2])
    #
    #         if len(res_greedy[b][(p, q)][0]) == 0:
    #             row.append('{}')
    #         else:
    #             row.append(res_greedy[b][(p, q)][0])
    #         row.append(res_greedy[b][(p, q)][1])
    #         row.append(res_greedy[b][(p, q)][2])
    #     row_list.append(row)
    # # d = {"sid": id2score1.keys(), "log_ppl-": id2score1.values(), "log_ppl+": id2score2.values(),
    # #      "delta_log_ppl": id2deltalogppl.values(), "src": id2src1.values(), "trg": id2trg1.values(),
    # #      "output": id2out1.values()}
    # #
    # # d = {"p": p_list, "alpha": alpha_list, "q": q_list, "scheme": scheme_list)}
    logger.info(f'../eplots/d1_20+20_rev.csv')
    epsilon = 20
    obj = 'rev' # 'revenue'
    df = pd.read_csv(f'../eplots/d1_{epsilon}+{epsilon}_{obj}.csv', header=None, sep='\t')
    print(df)

    fig = plt.figure()
    ax = Axes3D(fig)
    if obj == 'sw':
        index_brute = 25
        index_greedy = 28
    if obj == 'rev':
        index_brute = 26
        index_greedy = 29
    ax.scatter(df[0].tolist(), df[1].tolist(), df[index_brute].tolist(),  marker='+', label='brute')
    ax.scatter(df[0].tolist(), df[1].tolist(), df[index_greedy].tolist(),  marker='x', label='greedy')

    ax.set_xlabel('p', fontdict={'size': 15, 'color': 'red'})
    ax.set_ylabel('alpha', fontdict={'size': 15, 'color': 'red'})
    ax.set_zlabel(obj, fontdict={'size': 15, 'color': 'red'})
    ax.legend()
    # plt.show()
    # df.to_csv(f"../eplots/{args.did}_{args.grain_p}+{args.grain_alpha}_{obj}.csv", index=False, header=False, sep='\t')
    plt.savefig(f"../eplots/{args.did}_{epsilon}+{epsilon}_{obj}.pdf", dpi=300, bbox_inches="tight", format='pdf')

def extract_csv_rev(logger):
    logger.info(f"{'#' * 30} rev")
    epsilon_list = [0.2, 0.1, 0.05]
    grain_list = [5, 10, 20]
    # epsilon_list = [0.2]
    # grain_list = [5]

    brute_core_list = []
    greedy_core_list = []
    for i, epsilon in enumerate(epsilon_list):
        logger.info(f"{'=' * 20} {epsilon} {grain_list[i]}")
        budget_list = [1,2,3,4]
        logger.info(f'../eplots/d1_{grain_list[i]}+{grain_list[i]}_rev.csv')
        df = pd.read_csv(f'../eplots/d1_{grain_list[i]}+{grain_list[i]}_rev.csv', header=None, sep='\t')


        index_brute_M_start = 6

        opt_brute_obj_list = []  # 对应着budget
        opt_brute_M_list = []
        opt_brute_scheme_list = []
        opt_greedy_obj_list = []
        opt_greedy_M_list = []
        opt_greedy_scheme_list = []

        for j,b in enumerate(budget_list):
            # logger.info(f"{'-'*20} {b}")
            index_brute_M = index_brute_M_start + 6*j
            index_brute_obj = index_brute_M_start + 6*j + 2
            index_greedy_M = index_brute_M_start + 6*j + 3
            index_greedy_obj = index_brute_M_start + 6*j + 5

            # df1 = df.sort_values(df.columns[index_brute_obj], ascending=False)
            argmax_brute = df[index_brute_obj].argmax()
            opt_brute_obj_list.append(df.iat[argmax_brute, index_brute_obj])
            opt_brute_M_list.append(df.iat[argmax_brute, index_brute_M])
            opt_brute_scheme_list.append( (df.iat[argmax_brute, 0], df.iat[argmax_brute, 1]))

            argmax_greedy = df[index_greedy_obj].argmax()
            opt_greedy_obj_list.append(df.iat[argmax_greedy, index_greedy_obj])
            opt_greedy_M_list.append(df.iat[argmax_greedy, index_greedy_M])
            opt_greedy_scheme_list.append( (df.iat[argmax_greedy, 0], df.iat[argmax_greedy, 1]))

        # print(opt_brute_obj_list, opt_brute_M_list, opt_brute_scheme_list, opt_greedy_obj_list, opt_greedy_M_list, opt_greedy_scheme_list)
        list_list = [opt_brute_obj_list, opt_brute_M_list, opt_brute_scheme_list, opt_greedy_obj_list, opt_greedy_M_list, opt_greedy_scheme_list]
        listnames = 'opt_brute_obj_list, opt_brute_M_list, opt_brute_scheme_list, opt_greedy_obj_list, opt_greedy_M_list, opt_greedy_scheme_list'
        listname_list = listnames.split(', ')
        for k, reslist in enumerate(list_list):
            logger.info(listname_list[k])
            logger.info(reslist)

        brute_core_list.append(opt_brute_obj_list)
        greedy_core_list.append(opt_greedy_obj_list)
    logger.info(f'brute_core_list: \n {brute_core_list}')
    logger.info(f'greedy_core_list: \n {greedy_core_list}')


def extract_csv_sw(logger):
    logger.info(f"{'#' * 30} sw")
    epsilon_list = [0.2, 0.1, 0.05]
    grain_list = [5, 10, 20]
    # epsilon_list = [0.2]
    # grain_list = [5]
    brute_core_list = []
    greedy_core_list = []

    for i, epsilon in enumerate(epsilon_list):
        logger.info(f"{'=' * 20} {epsilon} {grain_list[i]}")
        budget_list = [1,2,3,4]
        logger.info(f'../eplots/d1_{grain_list[i]}+{grain_list[i]}_sw.csv')
        df = pd.read_csv(f'../eplots/d1_{grain_list[i]}+{grain_list[i]}_sw.csv', header=None, sep='\t')


        index_brute_M_start = 6

        opt_brute_obj_list = []  # 对应着budget
        opt_brute_M_list = []
        opt_brute_scheme_list = []
        opt_greedy_obj_list = []
        opt_greedy_M_list = []
        opt_greedy_scheme_list = []

        for j,b in enumerate(budget_list):
            # logger.info(f"{'-'*20} {b}")
            index_brute_M = index_brute_M_start + 6*j
            index_brute_obj = index_brute_M_start + 6*j + 1
            index_greedy_M = index_brute_M_start + 6*j + 3
            index_greedy_obj = index_brute_M_start + 6*j + 4

            # df1 = df.sort_values(df.columns[index_brute_obj], ascending=False)
            argmax_brute = df[index_brute_obj].argmax()
            opt_brute_obj_list.append(df.iat[argmax_brute, index_brute_obj])
            opt_brute_M_list.append(df.iat[argmax_brute, index_brute_M])
            opt_brute_scheme_list.append( (df.iat[argmax_brute, 0], df.iat[argmax_brute, 1]))

            argmax_greedy = df[index_greedy_obj].argmax()
            opt_greedy_obj_list.append(df.iat[argmax_greedy, index_greedy_obj])
            opt_greedy_M_list.append(df.iat[argmax_greedy, index_greedy_M])
            opt_greedy_scheme_list.append( (df.iat[argmax_greedy, 0], df.iat[argmax_greedy, 1]))

        # print(opt_brute_obj_list, opt_brute_M_list, opt_brute_scheme_list, opt_greedy_obj_list, opt_greedy_M_list, opt_greedy_scheme_list)
        list_list = [opt_brute_obj_list, opt_brute_M_list, opt_brute_scheme_list, opt_greedy_obj_list, opt_greedy_M_list, opt_greedy_scheme_list]
        listnames = 'opt_brute_obj_list, opt_brute_M_list, opt_brute_scheme_list, opt_greedy_obj_list, opt_greedy_M_list, opt_greedy_scheme_list'
        listname_list = listnames.split(', ')
        for k, reslist in enumerate(list_list):
            logger.info(listname_list[k])
            logger.info(reslist)
        brute_core_list.append(opt_brute_obj_list)
        greedy_core_list.append(opt_greedy_obj_list)
    logger.info(f'brute_core_list: \n {brute_core_list}')
    logger.info(f'greedy_core_list: \n {greedy_core_list}')

def extract_csv_sw(logger):
    logger.info(f"{'#' * 30} sw")
    epsilon_list = [0.2, 0.1, 0.05]
    grain_list = [5, 10, 20]
    # epsilon_list = [0.2]
    # grain_list = [5]
    brute_core_list = []
    greedy_core_list = []

    for i, epsilon in enumerate(epsilon_list):
        logger.info(f"{'=' * 20} {epsilon} {grain_list[i]}")
        budget_list = [1,2,3,4]
        logger.info(f'../eplots/d1_{grain_list[i]}+{grain_list[i]}_sw.csv')
        df = pd.read_csv(f'../eplots/d1_{grain_list[i]}+{grain_list[i]}_sw.csv', header=None, sep='\t')


        index_brute_M_start = 6

        opt_brute_obj_list = []  # 对应着budget
        opt_brute_M_list = []
        opt_brute_scheme_list = []
        opt_greedy_obj_list = []
        opt_greedy_M_list = []
        opt_greedy_scheme_list = []

        for j,b in enumerate(budget_list):
            # logger.info(f"{'-'*20} {b}")
            index_brute_M = index_brute_M_start + 6*j
            index_brute_obj = index_brute_M_start + 6*j + 1
            index_greedy_M = index_brute_M_start + 6*j + 3
            index_greedy_obj = index_brute_M_start + 6*j + 4

            # df1 = df.sort_values(df.columns[index_brute_obj], ascending=False)
            argmax_brute = df[index_brute_obj].argmax()
            opt_brute_obj_list.append(df.iat[argmax_brute, index_brute_obj])
            opt_brute_M_list.append(df.iat[argmax_brute, index_brute_M])
            opt_brute_scheme_list.append( (df.iat[argmax_brute, 0], df.iat[argmax_brute, 1]))

            argmax_greedy = df[index_greedy_obj].argmax()
            opt_greedy_obj_list.append(df.iat[argmax_greedy, index_greedy_obj])
            opt_greedy_M_list.append(df.iat[argmax_greedy, index_greedy_M])
            opt_greedy_scheme_list.append( (df.iat[argmax_greedy, 0], df.iat[argmax_greedy, 1]))

        # print(opt_brute_obj_list, opt_brute_M_list, opt_brute_scheme_list, opt_greedy_obj_list, opt_greedy_M_list, opt_greedy_scheme_list)
        list_list = [opt_brute_obj_list, opt_brute_M_list, opt_brute_scheme_list, opt_greedy_obj_list, opt_greedy_M_list, opt_greedy_scheme_list]
        listnames = 'opt_brute_obj_list, opt_brute_M_list, opt_brute_scheme_list, opt_greedy_obj_list, opt_greedy_M_list, opt_greedy_scheme_list'
        listname_list = listnames.split(', ')
        for k, reslist in enumerate(list_list):
            logger.info(listname_list[k])
            logger.info(reslist)
        brute_core_list.append(opt_brute_obj_list)
        greedy_core_list.append(opt_greedy_obj_list)
    logger.info(f'brute_core_list: \n {brute_core_list}')
    logger.info(f'greedy_core_list: \n {greedy_core_list}')

def plot_distribution_degree(network, args, logger):
    node2degree = {}
    for node in network.graph.nodes():
        node2degree[node] = len(network.graph[node])
    plt.hist(node2degree.values(), bins=10)
    plt.savefig(f"../eplots/{network.did}_dist_degree.pdf", dpi=300, bbox_inches="tight", format='pdf')
    plt.clf()

def plot_distribution_visibility(network, args, logger):
    node2visibility = {}
    for node in network.graph.nodes():
        visible_set = network.get_visible(node, network.tau)
        node2visibility[node] = len(visible_set)
    plt.hist(node2visibility.values(), bins=10)
    plt.savefig(f"../eplots/{network.did}_dist_visibility.pdf", dpi=300, bbox_inches="tight", format='pdf')
    plt.clf()


def plot_distribution_valuation(network, args, logger):
    gamma = int(args.gamma)
    node2visibility = {}
    for node in network.graph.nodes():
        visible_set = network.get_visible(node, network.tau)
        node2visibility[node] = len(visible_set)
    vis_max = sorted(node2visibility.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[0][1]

    node2valuation = {}
    for node in range(len(network.graph.nodes())):
        visibility = len(network.get_visible(node, network.tau))
        valuation = math.pow((1 + (visibility / vis_max)), gamma) / math.pow(2, gamma)
        node2valuation[node] = valuation
    plt.hist(node2valuation.values(), bins=10)
    plt.savefig(f"../eplots/{network.did}_dist_valuation.pdf", dpi=300, bbox_inches="tight", format='pdf')
    plt.clf()


def plot_distribution_cost(network, args, logger):
    gamma = int(args.gamma)
    node2visibility = {}
    for node in network.graph.nodes():
        visible_set = network.get_visible(node, network.tau)
        node2visibility[node] = len(visible_set)
    vis_max = sorted(node2visibility.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[0][1]

    node2cost = {}
    for node in range(len(network.graph.nodes())):
        visibility = len(network.get_visible(node, network.tau))
        cost = math.pow((1 + (visibility / vis_max)), gamma) / math.pow(2, gamma)
        node2cost[node] = cost
    plt.hist(node2cost.values(), bins=10)
    plt.savefig(f"../eplots/{network.did}_dist_cost.pdf", dpi=300, bbox_inches="tight", format='pdf')
    plt.clf()


def plot_function_valuation(network, args, logger):
    node2visibility = {}
    for node in network.graph.nodes():
        visible_set = network.get_visible(node, network.tau)
        node2visibility[node] = len(visible_set)
    vis_max = sorted(node2visibility.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[0][1]

    x = np.linspace(0, vis_max, vis_max + 1)
    y = [math.pow((1 + (visibility / vis_max)), int(args.gamma)) / math.pow(2, int(args.gamma)) for visibility in x]
    plt.plot(x, y)
    plt.savefig(f"../eplots/{network.did}_curve_valuation.pdf", dpi=300, bbox_inches="tight", format='pdf')
    plt.clf()


def plot_function_cost(network, args, logger):
    node2visibility = {}
    for node in network.graph.nodes():
        visible_set = network.get_visible(node, network.tau)
        node2visibility[node] = len(visible_set)
    vis_max = sorted(node2visibility.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[0][1]

    x = np.linspace(0, vis_max, vis_max + 1)
    y = [1 - math.pow((1 + (visibility / vis_max)), int(args.gamma)) / math.pow(2, int(args.gamma)) for visibility in x]
    plt.plot(x, y)
    plt.plot(x, y)
    plt.savefig(f"../eplots/{network.did}_curve_cost.pdf", dpi=300, bbox_inches="tight", format='pdf')
    plt.clf()



def format_sw(args, logger):
    """Format the results of social welfare, as as to copy from csv to excel directly

    :param args:
    :type args:
    :param logger:
    :type logger:
    :return:
    :rtype:
    """
    budget_list = [int(x) for x in args.budget_list.split(',')]
    network = Network(logger, args.did, args.seed, args.percent_R, args.percent_S, int(args.a))
    netoperator_brute = NetoperatorSW(logger, network, args.version, 'brute', int(args.grain_p),
                                    int(args.grain_alpha))
    netoperator_greedy = NetoperatorSW(logger, network, args.version, 'greedy', int(args.grain_p),
                                     int(args.grain_alpha))
    res_brute = netoperator_brute.budget2scheme2result
    res_greedy = netoperator_greedy.budget2scheme2result

    row_list = []
    palpha_list = list(itertools.product(netoperator_brute.p_list_all, netoperator_brute.alpha_list_all))
    for (p, alpha) in palpha_list:
        q = alpha * p
        tilderR, tilderS = netoperator_brute.get_tilderR_tilderS(p, q)
        row = [p, alpha, q, (p, q), len(tilderR), len(tilderS)]
        for b in budget_list:
            if len(res_brute[b][(p, q)][0]) == 0:
                row.append('{}')
            else:
                row.append(res_brute[b][(p, q)][0])
            row.append(res_brute[b][(p, q)][1])
            row.append(res_brute[b][(p, q)][2])

            if len(res_greedy[b][(p, q)][0]) == 0:
                row.append('{}')
            else:
                row.append(res_greedy[b][(p, q)][0])
            row.append(res_greedy[b][(p, q)][1])
            row.append(res_greedy[b][(p, q)][2])
        row_list.append(row)
    # d = {"sid": id2score1.keys(), "log_ppl-": id2score1.values(), "log_ppl+": id2score2.values(),
    #      "delta_log_ppl": id2deltalogppl.values(), "src": id2src1.values(), "trg": id2trg1.values(),
    #      "output": id2out1.values()}
    #
    # d = {"p": p_list, "alpha": alpha_list, "q": q_list, "scheme": scheme_list)}
    data = pd.DataFrame(row_list)
    print('data is like:')
    print(data)
    # df = pd.DataFrame(d)pd.DataFrame(row_list)
    # logger.info('df to csv...')
    data.to_csv(f"../eplots_sw/{args.did}_{args.grain_p}+{args.grain_alpha}_sw.csv", index=False, header=False, sep='\t')

def format_rev(args, logger):
    """Format the results of revenue, as as to copy from csv to excel directly

     :param args:
     :type args:
     :param logger:
     :type logger:
     :return:
     :rtype:
     """
    budget_list = [int(x) for x in args.budget_list.split(',')]
    network = Network(logger, args.did, args.seed, args.percent_R, args.percent_S, int(args.gamma))

    netoperator_brute = NetoperatorREV(logger, network, args.version, 'brute', int(args.grain_p), int(args.grain_alpha))
    netoperator_greedy = NetoperatorREV(logger, network, args.version, 'greedy', int(args.grain_p), int(args.grain_alpha))
    res_brute = netoperator_brute.budget2scheme2result
    res_greedy = netoperator_greedy.budget2scheme2result

    row_list = []
    palpha_list = list(itertools.product(netoperator_brute.p_list_all, netoperator_brute.alpha_list_all))
    for (p,alpha) in palpha_list:
        q = alpha * p
        tilderR, tilderS = netoperator_brute.get_tilderR_tilderS(p, q)
        row = [p,alpha,q, (p,q), len(tilderR), len(tilderS)]

        for b in budget_list:
            if len(res_brute[b][(p, q)][0]) == 0:
                row.append('{}')
            else:
                row.append(res_brute[b][(p, q)][0])
            row.append(res_brute[b][(p, q)][1])
            row.append(res_brute[b][(p, q)][2])

            if len(res_greedy[b][(p, q)][0]) == 0:
                row.append('{}')
            else:
                row.append(res_greedy[b][(p, q)][0])
            row.append(res_greedy[b][(p, q)][1])
            row.append(res_greedy[b][(p, q)][2])
        row_list.append(row)
    # d = {"sid": id2score1.keys(), "log_ppl-": id2score1.values(), "log_ppl+": id2score2.values(),
    #      "delta_log_ppl": id2deltalogppl.values(), "src": id2src1.values(), "trg": id2trg1.values(),
    #      "output": id2out1.values()}
    #
    # d = {"p": p_list, "alpha": alpha_list, "q": q_list, "scheme": scheme_list)}
    data = pd.DataFrame(row_list)
    print('data is like:')
    print(data)
    # df = pd.DataFrame(d)pd.DataFrame(row_list)
    # logger.info('df to csv...')
    data.to_csv(f"../eplots/{args.did}_{args.grain_p}+{args.grain_alpha}_rev.csv", index=False, header=False, sep='\t')


def plot_dist_hist(samples, bins, data_name):
    # samples = np.random.beta(alpha_beta_value[0], alpha_beta_value[1],10000)
    # print(alpha_beta_value)
    # print(samples)
    plt.clf()
    plt.hist(samples, bins=bins)
    plt.savefig(f"elogs/hist_{data_name}_freq.pdf", dpi=300, bbox_inches="tight",format='pdf')
    # plt.savefig(f"../elogs/hist_{data_name}_freq.pdf", dpi=300, bbox_inches="tight",format='pdf')
    plt.clf()

def plot_dist_pdf(v_beta_paras,c_beta_paras,data_name):
    x = np.linspace(0, 1, 1002)[1:-1]
    alpha_beta_value_list = [v_beta_paras,c_beta_paras]
    listname = ["valuations","costs"]
    plt.clf()
    for i, alpha_beta_value in enumerate(alpha_beta_value_list):
        dist = beta(alpha_beta_value[0], alpha_beta_value[1])
        dist_y = dist.pdf(x)
        plt.plot(x, dist_y, label=r'$\alpha=%.1f,\ \beta=%.1f$ ,%s' % (alpha_beta_value[0], alpha_beta_value[1], listname[i]))
    plt.xlim(0, 1)
    plt.ylim(0, 2.5)
    plt.legend()
    plt.savefig(f"../elogs/hist_{data_name}_pdf.pdf", dpi=300, bbox_inches="tight",format='pdf')
    plt.clf()

def plot_degree(g):
    for i in g.nodes():
        print(len(g[i]))


def plot_d1():
    filename = '../elogs_rev/temp12.log'
    # f = open(filename, "r")
    df = pd.read_csv(filename, header=None, sep='\t')
    # print(df[1].tolist())

    p_list = df[0].tolist()
    q_list = df[1].tolist()

    rev1b_list = df[5].tolist()
    rev1g_list = df[8].tolist()
    rev2b_list = df[11].tolist()
    rev2g_list = df[14].tolist()
    rev3b_list = df[17].tolist()
    rev3g_list = df[20].tolist()
    rev4b_list = df[23].tolist()
    rev4g_list = df[26].tolist()

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(p_list, q_list,  rev1b_list)

    ax.set_zlabel('revenue', fontdict={'size': 15, 'color': 'red'})
    ax.set_ylabel('q', fontdict={'size': 15, 'color': 'red'})
    ax.set_xlabel('p', fontdict={'size': 15, 'color': 'red'})

    plt.show()

    # # filename可以直接从盘符开始，标明每一级的文件夹直到csv文件，header=None表示头部为空，sep=' '表示数据间使用空格作为分隔符，如果分隔符是逗号，只需换成 ‘，’即可。
    #
    # df.head()
    #
    # df.tail()
    # ax = plt.axes(projection='3d')
    #
    # # Data for a three-dimensional line
    # p = np.linspace(0, 15, 1000)
    # xline = np.sin(zline)
    # yline = np.cos(zline)
    # ax.plot3D(xline, yline, zline, 'gray')
    # plt.show()
    #
    # # Data for three-dimensional scattered points
    # zdata = 15 * np.random.random(100)
    # xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
    # ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
    # ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');
    # plt.show()

if __name__ == '__main__':
    main()
