#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/9/2 20:36
@Desc    :
'''

from zutil import get_parser
from network import Network
from netoperator import Netoperator
from zutil import *
import itertools
import pickle
import os


def main():
    args, unk = get_parser().parse_known_args()
    logger, logname = get_log(args.did, args.method, args.version)
    logger.info(args)

    grain_tuple_list = args.grain_list_pq.split(',')
    budget_list = [int(x) for x in args.budget_list.split(',')]

    network = Network(logger, args.did, args.seed, args.percent_R, args.percent_S, args.beta_paras)
    netoperator = Netoperator(logger, network, args.version, args.method, grain_tuple_list)

    # alpha_list = args.grain_list_pq.split(',')
    # for alpha in alpha_list:

    if args.method == 'greedy':
        do_greedy(budget_list, grain_tuple_list, netoperator, logger)
    if args.method == 'brute':
        do_brute(budget_list, grain_tuple_list, netoperator, logger)




def do_greedy(budget_list, grain_tuple_list, netoperator, logger):
    # print('aaaaaa',netoperator.budget2scheme2result[1][:2])
    budget_max = max(budget_list)
    for budget in range(1, budget_max + 1):
        if budget not in netoperator.budget2scheme2result.keys():
            netoperator.budget2scheme2result[budget] = {}
    for grain_tuple_str in grain_tuple_list:
        # e.g., (10, 10)
        grain_tuple = [int(x) for x in grain_tuple_str.split('+')]
        pq_list = netoperator.get_pq_list(*grain_tuple)  # 数据持久化
        logger.info(f"length of pq_list = {len(pq_list)} under grain_tuple = {grain_tuple_str}")
        for p, q in pq_list:
            # e.g., (0.50, 0.70)
            tilderR, tilderS = netoperator.scheme2RS[(p, q)]
            max_history_result = None
            max_history_budget = 0
            # for b in range(budget_max, 0, -1):
            #     logger.info(f'here {b}')
            for b in range(budget_max, 0, -1):
                # logger.info(f'b, tilderR, tilderS:{b, tilderR, tilderS}')
                search_result = netoperator.search_budget2scheme2result(b, tilderR, tilderS)
                # logger.info(f'search_result of {b} is {1 if search_result else None}')
                if search_result:
                    max_history_result = search_result
                    max_history_budget = b
                    logger.info(f" max history budget={b}")
                    break
            for b in range(1, max_history_budget+1):
                search_res = netoperator.search_budget2scheme2result(b, tilderR, tilderS)
                logger.info(
                    f"load: budget={b}; scheme=({p},{q}); result={search_res[:2]} ")

            (M_last, Incr_last, requester2IncrMlast) = max_history_result if max_history_result else (set(), 0, dict())
            # print(M_last, Incr_last)
            for budget_last in range(max_history_budget, budget_max):
                logger.info(f'budget_last = {budget_last}')
                M, card, requester2IncrMlast = netoperator.get_marginal_greedy(tilderR, tilderS, M_last, Incr_last,
                                                                                    requester2IncrMlast, budget_last)
                netoperator.budget2scheme2result[budget_last + 1][(p, q)] = (M, card, requester2IncrMlast)
                # print('here!',netoperator.budget2scheme2result[1][(p, q)][0])
                logger.info(f"compute: budget={budget_last + 1}; scheme=({p},{q}); result=({M}, {card}) ")
                M_last = M.copy()
    netoperator.dump_budget2scheme2result()


def do_brute(budget_list, grain_tuple_list, netoperator, logger):
    for budget in budget_list:
        if budget not in netoperator.budget2scheme2result.keys():
            netoperator.budget2scheme2result[budget] = {}
        for grain_tuple_str in grain_tuple_list:
            # e.g., (10, 10)
            grain_tuple = [int(x) for x in grain_tuple_str.split('+')]
            pq_list = netoperator.get_pq_list(*grain_tuple)  # 数据持久化
            for p, q in pq_list:
                # e.g., (0.50, 0.70)
                tilderR, tilderS = netoperator.scheme2RS[(p, q)]
                result = netoperator.search_budget2scheme2result(budget, tilderR, tilderS)

                if not result:
                    result = netoperator.get_M_brute(budget, tilderR, tilderS)
                    logger.info(
                        f"compute: budget={budget}, scheme=({p},{q}), result={result} "
                        f"\n tilderR({len(tilderR)})={tilderR}, \n tilderS({len(tilderS)})={tilderS})")
                    netoperator.budget2scheme2result[budget][(p, q)] = result
                else:
                    logger.info(
                        f"load: budget={budget}, scheme=({p},{q}), result={result} "
                        f"\n tilderR({len(tilderR)})={tilderR}, \n tilderS({len(tilderS)})={tilderS})")
    netoperator.dump_budget2scheme2result()


if __name__ == "__main__":
    main()

    # grain_prices = {}
    # judge whether a scheme form a sides that computed in history

    # grain_list_p 设置成睡得参数比较合适呢， operator还是main呢， operator吧，
    # 那么就是 每一个
