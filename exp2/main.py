#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/9/2 20:36
@Desc    :
'''

from network import Network
from noperator_brute import BruteOperator
from noperator_greedy import GreedyOperator
from noperator_h1 import H1Operator
from noperator_h2 import H2Operator
from ploter import Ploter
from zutil import *
import sys
import pandas as pd

def algo(parser_algo):
    args, unk = parser_algo.parse_known_args()
    # logname = f"{args.did}_{args.method}_{args.obj}"

    logname = f"{'+'.join(args.did_list)}_{'+'.join([str(int(x)) for x in args.lamb_list])}_{'+'.join(args.obj_list)}_{'+'.join(args.method_list)}"
    logger = get_log(logname)
    logger.info('python '+' '.join(sys.argv))

    for did in args.did_list:
        for lamb in args.lamb_list:
            logger.info(f"{'=' * 20}_{lamb}")
            network = Network(logger, did, args.seed, lamb)
            for grain in args.grain_list:
                if 'brute' in args.method_list:
                    obj = 'A'
                    operator = BruteOperator(logger, network, obj, args.budget_list, grain)
                    operator.opt_price_objs()
                for obj in args.obj_list:
                    if 'h1' in args.method_list:
                        operator = H1Operator(logger, network, obj, args.budget_list, grain)
                        operator.opt_price()
                    if 'h2' in args.method_list:
                        operator = H2Operator(logger, network, obj, args.budget_list, grain)
                        operator.opt_price()
                    if 'greedy' in args.method_list:
                        operator = GreedyOperator(logger, network, obj, args.budget_list, grain)
                        operator.run()


def plot(parser_plot):
    object_methods = [method_name for method_name in dir(Ploter)
                      if callable(getattr(Ploter, method_name)) and '__' not in method_name]
    print(object_methods)

    args, unk = parser_plot.parse_known_args()
    logname = f"{args.did}_plot"
    logger = get_log(logname)
    logger.info('run plot')
    ploter = Ploter(logger)
    # analyst.generate_csv_from_pkl(args.did, args.method_list, args.obj, args.budget_list, args.grain_p, args.grain_alpha )
    # analyst.extract_axisvalue_from_csv(args.did, args.obj, args.grain_p, args.grain_alpha, args.budget_list, args.method_list)

    logger.info(f"excute function Analyst.{args.func}")

    if args.func == 'plot_curve':
        for lamb in args.gamma_list:
            network = Network(logger, args.did, args.seed,  lamb)
            ploter.plot_curve(network, args.curvename_list)
    if args.func == 'plot_curve_single':
        network = Network(logger, args.did, args.seed, args.lamb)
        ploter.plot_curve_single(network, args.curvename_list, args.gamma_list)
    if args.func == 'plot_dist': # distribution is for population U rather than R and S
        for lamb in args.gamma_list:
            network = Network(logger, args.did, args.seed, lamb)
            ploter.plot_dist(network, args.curvename_list, args.bin)




    if args.func == 'plot_from_pkl_3d':
        for budget in args.budget_list:
            ploter.plot_from_pkl_3d(args.did, args.obj, budget, args.grain, args.method, args.lamb)
    if args.func == 'plot_from_axisvalue_budget':
        for budget in args.budget_list:
            ploter.plot_from_axisvalue_budget(args.did, budget, args.obj, args.method_list, args.grain_list, args.lamb)

    if args.func == 'plot_from_axisvalue_epsilon':
        for grain in args.grain_list:
            ploter.plot_from_axisvalue_epsilon(args.did, args.budget_list, args.obj, args.method_list, grain, args.lamb)


def add_args_general(subparser):
    subparser.add_argument('-s', "--seed", metavar='',
                           default='32', help="Seed for all random, usually fixed.")

    subparser.add_argument('-d', "--did", metavar='',
                           choices=['d1', 'd2', 'd3', 'd4', 'd5', 'd6'], help="Data to experiment.")
    subparser.add_argument('-dl', "--did_list", metavar='',
                           nargs='+', choices=['d1', 'd2', 'd3', 'd4', 'd5', 'd6'], help="Data list to experiment.")

    subparser.add_argument('-l', "--lamb", metavar='',
                           type=float, help="Para lambda of p() and q().")
    subparser.add_argument('-ll', "--lamb_list", metavar='',
                           nargs='+', type=float, help="Diff paras of p() and q().")

    subparser.add_argument('-o', "--obj", metavar='',
                           choices=['I', 'W', 'RI', 'RW'], help="Objective.")
    subparser.add_argument('-ol', "--obj_list", metavar='',
                           nargs='+', choices=['I', 'W', 'RI', 'RW'], help="Objective.")

    subparser.add_argument('-m', "--method", metavar='',
                           choices=['brute', 'greedy', 'h1', 'h2'], help="Method for subprob1.")
    subparser.add_argument('-ml', "--method_list", metavar='',
                           nargs='+', choices=['brute', 'greedy', 'h1', 'h2'], help="Method list for subprob1.")

    subparser.add_argument('-g', "--grain", metavar='',  # algo 不用list , 跑最小的就行, plot 用list
                           type=int, help="Reciprocal of epsilon p and q.")
    subparser.add_argument('-gl', "--grain_list", metavar='',
                           nargs='+', type=int, help="Grain list.")

    subparser.add_argument('-bl', "--budget_list", metavar='',
                           nargs='+', type=int, help="Budget of suppliers.")


def add_args_algo(subparser):
    add_args_general(subparser)


def add_args_analyze(subparser):
    add_args_general(subparser)
    # ------------- Below: for individual function of Ploter ------------- #
    subparser.add_argument('-f', "--func", metavar='',
                             help="Function to call in Ploter.")

    subparser.add_argument('-c', "--curvename", metavar='', # 既然已经有了cl这个c应该是用不着了吧
                             choices=['p', 'q', 'vis', 'deg', 'p_deg', 'q_deg'], help="(plot_curve) Curve to plot.")
    subparser.add_argument('-cl', "--curvename_list", metavar='',
                             nargs='+', choices=['p', 'q', 'vis', 'deg', 'p_deg', 'q_deg'], help="(plot_curve) Curves to plot.")

    subparser.add_argument('-bin', "--bin", metavar='',
                             type=int, default=10, help="Plot dist: # of bins")


if __name__ == "__main__":
    nowTime = datetime.datetime.now().strftime("%m%d-%H%M%S")
    cmd = f"\n\n{nowTime}\npython {' '.join(sys.argv)}"
    with open("RESULT.log", "a") as myfile:
        myfile.write(cmd)

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=False)
    subparsers = parser.add_subparsers(help='sub-commands', dest='cmd')
    parser_algo = subparsers.add_parser('algo', help='algo module', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_plot = subparsers.add_parser('plot', help='plot module', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args, unk = parser.parse_known_args()



    if args.cmd == "algo":
        add_args_algo(parser_algo)
        s = parser_algo.format_help().replace('\n\n', '\n')
        print(f"{'*' * 50}\n{s}")
        algo(parser_algo)
    if args.cmd == "plot":
        add_args_analyze(parser_plot)
        s = parser_plot.format_help().replace('\n\n', '\n')
        print(f"{'*' * 50}\n{s}")
        plot(parser_plot)



