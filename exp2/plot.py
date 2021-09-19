#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/9/13 15:10
@Desc    :
'''

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from zutil import *
from network import Network
from netoperator import Netoperator
from netoperatorSW import NetoperatorSW
import itertools


def main():
    args, unk = get_parser().parse_known_args()
    logger, logname = get_log(args.did, 'plot', args.version)
    logger.info(args)
    if args.rev:
        plot_rev(args, logger)
    if args.sw:
        plot_sw(args, logger)


def plot_sw(args, logger):
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
        tilderR, tilderS = netoperator_brute.get_tilderR_tilderU(p, q)
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
    data.to_csv(f"../eplots_sw/{args.did}_{args.grain_p}+{args.grain_alpha}.csv", index=False, header=False, sep='\t')

def plot_rev(args, logger):
    budget_list = [int(x) for x in args.budget_list.split(',')]
    network = Network(logger, args.did, args.seed, args.percent_R, args.percent_S, int(args.a))

    netoperator_brute = Netoperator(logger, network, args.version, 'brute', int(args.grain_p), int(args.grain_alpha))
    netoperator_greedy = Netoperator(logger, network, args.version, 'greedy', int(args.grain_p), int(args.grain_alpha))
    res_brute = netoperator_brute.budget2scheme2result
    res_greedy = netoperator_greedy.budget2scheme2result

    row_list = []
    palpha_list = list(itertools.product(netoperator_brute.p_list_all, netoperator_brute.alpha_list_all))
    for (p,alpha) in palpha_list:
        q = alpha * p
        tilderR, tilderS = netoperator_brute.get_tilderR_tilderU(p, q)
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
    data.to_csv(f"../eplots/{args.did}_{args.grain_p}+{args.grain_alpha}.csv", index=False, header=False, sep='\t')


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
    filename = '../elogs/temp12.log'
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
