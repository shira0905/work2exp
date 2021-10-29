#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/9/2 20:36
@Desc    :
'''

from network import Network
from netoperator import Netoperator
from noperator_brute import BruteOperator
from noperator_greedy import GreedyOperator
from noperator_h1 import H1Operator
from analyst import Analyst
from zutil import *

def algo(parser_algo):
    args, unk = parser_algo.parse_known_args()
    logname = f"{args.did}_{args.method}_{args.obj}"
    logger = get_log(logname)  # logname = logger.name
    logger.info('run algo')
    network = Network(logger, args.did, args.seed, args.gamma)

    if args.method == 'brute':
        operator = BruteOperator(logger, network, args.method, args.obj, args.budget_list, args.grain)
    if args.method == 'greedy':
        operator = GreedyOperator(logger, network, args.method, args.obj, args.budget_list, args.grain)
    if args.method == 'h1':
        operator = H1Operator(logger, network, args.method, args.obj, args.budget_list, args.grain)

    operator.compute()


def analyze(parser_analyze):
    object_methods = [method_name for method_name in dir(Analyst)
                      if callable(getattr(Analyst, method_name)) and '__' not in method_name]
    print(object_methods)
    args, unk = parser_analyze.parse_known_args()
    logname = f"{args.did}_analyze"
    logger = get_log(logname)
    logger.info('run analyze')
    analyst = Analyst(logger)
    # analyst.generate_csv_from_pkl(args.did, args.method_list, args.obj, args.budget_list, args.grain_p, args.grain_alpha )
    # analyst.extract_axisvalue_from_csv(args.did, args.obj, args.grain_p, args.grain_alpha, args.budget_list, args.method_list)

    logger.info(f"excute function Analyst.{args.func}")

    if args.func == 'plot_curve':
        for gamma in args.gamma_list:
            network = Network(logger, args.did, args.seed,  gamma)
            analyst.plot_curve(network, args.curvename_list)
    if args.func == 'plot_curve_single':
        network = Network(logger, args.did, args.seed, args.gamma)  # here is the default 2 won't used
        analyst.plot_curve_single(network, args.curvename_list, args.gamma_list)
    if args.func == 'plot_dist': # distribution is for population U rather than R and S
        for gamma in args.gamma_list:
            network = Network(logger, args.did, args.seed, gamma)
            analyst.plot_dist(network, args.curvename_list, args.bin)




    if args.func == 'plot_from_pkl_3d':
        for budget in args.budget_list:
            analyst.plot_from_pkl_3d(args.did, args.obj, budget, args.grain, args.method, args.gamma)
    if args.func == 'plot_from_axisvalue_budget':
        for budget in args.budget_list:
            analyst.plot_from_axisvalue_budget(args.did, budget, args.obj, args.method_list, args.grain_list, args.gamma)

    if args.func == 'plot_from_axisvalue_epsilon':
        for grain in args.grain_list:
            analyst.plot_from_axisvalue_epsilon(args.did, args.budget_list, args.obj, args.method_list, grain, args.gamma)

    if args.func == 'generate_csv_from_pkl':
        analyst.generate_csv_from_pkl(args.did, args.method_list, args.obj, args.budget_list, args.grain, args.gamma)


def args_algo(parser_algo):
    parser_algo.add_argument('-d', "--did",  choices=['d1', 'd2', 'd3', 'd4'], help="Data to experiment.", metavar='')
    parser_algo.add_argument('-s', "--seed", default='32', help="Seed for all random process.", metavar='')
    # parser_algo.add_argument('-pr', "--percent_R", default=0.25, type=float, help="Percentage of requesters R/N.", metavar='')
    # parser_algo.add_argument('-ps', "--percent_S", default=0.25, type=float, help="Phe percentage of suppliers S/N.", metavar='')
    parser_algo.add_argument('-gm', "--gamma", default='2', type=float, help="[exp] Parameter of p(v) and q(v).", metavar='')
    parser_algo.add_argument('-bl', "--budget_list", nargs='*', type=int, help="[vary] Budget of suppliers.", metavar='')
    # parser_algo.add_argument('-gp', "--grain_p", type=int, help="[exp] # p = 1/epsilon_p.", metavar='')
    # parser_algo.add_argument('-ga', "--grain_alpha", type=int, help="[exp] # alpha = 1/epsilon_alpha.", metavar='')
    parser_algo.add_argument('-g', "--grain", type=int, help="[exp] # grain=1/eps_p=1/alpha.", metavar='')
    parser_algo.add_argument('-o', "--obj", choices=['rev', 'sw'], help="[exp] Objective to maximize.", metavar='')
    parser_algo.add_argument('-m', "--method", choices=['brute', 'greedy', 'h1', 'h2', 'shapley'], help="[exp] Method for subprob1.", metavar='')


def args_analyze(parser_analyze):
    parser_analyze.add_argument('-d', "--did",  choices=['d1', 'd2', 'd3', 'd4'], help="Data to experiment.", metavar='')
    parser_analyze.add_argument('-s', "--seed", default='32', help="Seed for all random process.", metavar='')
    # parser_analyze.add_argument('-pr', "--percent_R", default=0.25, type=float, help="Percentage of requesters R/N.", metavar='')
    # parser_analyze.add_argument('-ps', "--percent_S", default=0.25, type=float, help="Phe percentage of suppliers S/N.", metavar='')
    parser_analyze.add_argument('-gm', "--gamma", default='2', type=float, help="[exp] Parameter of p(v) and q(v).", metavar='')

    parser_analyze.add_argument('-bl', "--budget_list", nargs='*', type=int, help="[vary] Budget of suppliers.", metavar='')
    # parser_analyze.add_argument('-gp', "--grain_p", type=int, help="[exp] # p = 1/epsilon_p.", metavar='')
    # parser_analyze.add_argument('-ga', "--grain_alpha", type=int, help="[exp] # alpha = 1/epsilon_alpha.", metavar='')
    parser_analyze.add_argument('-g', "--grain", type=int, help="[exp] # grain=1/eps_p=1/alpha.", metavar='')
    parser_analyze.add_argument('-o', "--obj", choices=['rev', 'sw'], help="[exp] Objective to maximize.", metavar='')
    parser_analyze.add_argument('-m', "--method", choices=['brute', 'greedy', 'h1', 'h2'], help="[exp] Method for subprob1.", metavar='')
    parser_analyze.add_argument('-ml', "--method_list", nargs='+', choices=['brute', 'greedy', 'h1', 'h2'], default='', help="[study] The method to use to compute optimum.", metavar='')
    parser_analyze.add_argument('-f', "--func",  help="Function to call in Analyst.", metavar='')
    parser_analyze.add_argument('-c', "--curvename",  choices=['p', 'q', 'vis', 'deg', 'p_deg', 'q_deg'],
                                help="(plot_curve) Curve to plot.", metavar='')
    parser_analyze.add_argument('-cl', "--curvename_list", nargs='+', choices=['p', 'q', 'vis', 'deg', 'p_deg', 'q_deg'],
                                help="(plot_curve) Curves to plot.", metavar='')
    parser_analyze.add_argument('-gml', "--gamma_list", type=float, nargs='+', default=[2], help="[exp] Parameter of p(v) and q(v).",
                                metavar='')
    parser_analyze.add_argument('-gl', "--grain_list", type=int, nargs='+',  help="[exp] Parameter of p(v) and q(v).",
                                                                           metavar='')
    parser_analyze.add_argument('-bin', "--bin", type=int, default=10 , help="Plot dist: # of bins", metavar='')


if __name__ == "__main__":
    nowTime = datetime.datetime.now().strftime("%m%d-%H%M%S")

    cmd = f"\n\n{nowTime}\npython {' '.join(sys.argv)}"
    with open("RESULT.log", "a") as myfile:
        myfile.write(cmd)

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=False)
    subparsers = parser.add_subparsers(help='sub-commands', dest='cmd')
    parser_algo = subparsers.add_parser('algo', help='algo module', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_analyze = subparsers.add_parser('pre', help='analyze module', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args, unk = parser.parse_known_args()

    if args.cmd == "algo":
        args_algo(parser_algo)
        s = parser_algo.format_help().replace('\n\n', '\n')
        print(f"{'*' * 50}\n{s}")
        algo(parser_algo)
    if args.cmd == "pre":
        args_analyze(parser_analyze)
        s = parser_analyze.format_help().replace('\n\n', '\n')
        print(f"{'*' * 50}\n{s}")
        analyze(parser_analyze)



