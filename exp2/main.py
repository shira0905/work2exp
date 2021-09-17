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

    budget_list = [int(x) for x in args.budget_list.split(',')]

    network = Network(logger, args.did, args.seed, args.percent_R, args.percent_S, int(args.a))
    netoperator = Netoperator(logger, network, args.version, args.method, int(args.grain_p), int(args.grain_alpha))


    if args.method == 'greedy':
        do_greedy(budget_list, netoperator.pq_list, netoperator, logger)
    if args.method == 'brute':
        do_brute(budget_list, netoperator.pq_list, netoperator, logger)




def do_greedy(budget_list, pq_list, netoperator, logger):
    budget_max = max(budget_list)
    for budget in range(1, budget_max + 1):
        if budget not in netoperator.budget2scheme2result.keys():
            netoperator.budget2scheme2result[budget] = {}

    cnt_invalid, cnt_valid = 0, 0
    for p, q in pq_list:
        tilderR, tilderS = netoperator.get_tilderR_tilderU(p, q)
        if len(tilderR) == 0 or len(tilderS) == 0:
            logger.info(f"{'='*20} {(p, q)} is invalid scheme since with empty set: {'tilderS' if len(tilderR) == 0 else ''} {'tilderR' if len(tilderS) == 0 else ''}")
            cnt_invalid += 1

        else:
            logger.info(f"{'='*20} {(p, q)} complete computation")
            cnt_valid += 1

            max_history_result = None
            max_history_budget = 0
            for b in range(budget_max, 0, -1):
                search_result = netoperator.search_budget2scheme2result(b, tilderR, tilderS)
                if search_result :
                    max_history_result = search_result
                    max_history_budget = b
                    # logger.info(f" max history budget={b}")
                    break
            logger.info(f"max_history_budget={max_history_budget}, max_history_result={None if not max_history_result else max_history_result[:3]}")
            (M_last, Incr_last, requester2IncrMlast, rev_last) = max_history_result if max_history_result else (set(), 0, dict(), 0)
            for budget in range(1, max_history_budget):
                M, incr, requester2Incr, rev = netoperator.search_budget2scheme2result(budget, tilderR, tilderS)
                revenue = (p - q) * incr
                netoperator.budget2scheme2result[budget][(p, q)] = (M, incr, requester2Incr, revenue)
                logger.info(
                    f"load: budget={budget}; scheme=({p},{q}); tilderR=({len(tilderR)}) tilderS=({len(tilderS)}); result={M, incr}; rev={(p - q) * incr}")

            for budget_last in range(max_history_budget, budget_max):
                # 哪些不用 copy() 的
                logger.info(netoperator.get_marginal_greedy(tilderR, tilderS, M_last, Incr_last, requester2IncrMlast, budget_last))
                M, incr, requester2IncrMlast = netoperator.get_marginal_greedy(tilderR, tilderS, M_last, Incr_last, requester2IncrMlast, budget_last)
                revenue = (p-q)*incr
                netoperator.budget2scheme2result[budget_last + 1][(p, q)] = (M, incr, requester2IncrMlast, revenue)
                # logger.info(f"compute: budget={budget_last + 1}; scheme={(p,q)}; result=({M}, {incr}) ")
                logger.info(
                    f"compute: budget={budget_last + 1}; scheme=({p},{q}); tilderR=({len(tilderR)}) tilderS=({len(tilderS)}); result={M, incr}; rev={(p - q) * incr}")
                M_last = M.copy()
    netoperator.dump_budget2scheme2result()
    logger.info(f"cnt_invalid={cnt_invalid}, cnt_valid={cnt_valid}")



# def do_brute(budget_list, pq_list, netoperator, logger):
#     for budget in budget_list:
#         if budget not in netoperator.budget2scheme2result.keys():
#             netoperator.budget2scheme2result[budget] = {}
#         for p, q in pq_list:
#             tilderR, tilderS = netoperator.get_tilderR_tilderU(p, q)
#             result = netoperator.search_budget2scheme2result(budget, tilderR, tilderS)
#             # 可能需要修改一下，现在是从当前对象的结果中搜索，完全可以从历史所有结果中搜索
#             if result:
#                 M, incr = result[0], result[1]
#                 logger.info(
#                     f"load: budget={budget}; scheme=({p},{q}); tilderR=({len(tilderR)}) tilderS=({len(tilderS)}); result={M, incr}; rev={(p-q)*incr}")
#             else:
#                 M, incr = netoperator.get_M_brute(budget, tilderR, tilderS)
#                 logger.info(
#                     f"compute: budget={budget}; scheme=({p},{q}); tilderR=({len(tilderR)}) tilderS=({len(tilderS)}); result={M, incr}; rev={(p-q)*incr}")
#             revenue = (p - q) * incr
#             netoperator.budget2scheme2result[budget][(p, q)] = (M, incr, revenue)
#     netoperator.dump_budget2scheme2result()


def do_brute(budget_list, pq_list, netoperator, logger):
    for budget in budget_list:
        if budget not in netoperator.budget2scheme2result.keys():
            netoperator.budget2scheme2result[budget] = {}
        for p, q in pq_list:
            tilderR, tilderS = netoperator.get_tilderR_tilderU(p, q)
            result = netoperator.search_budget2scheme2result(budget, tilderR, tilderS)
            # 可能需要修改一下，现在是从当前对象的结果中搜索，完全可以从历史所有结果中搜索
            if result:
                M, incr = result[0], result[1]
                logger.info(
                    f"load: budget={budget}; scheme=({p},{q}); tilderR=({len(tilderR)}) tilderS=({len(tilderS)}); result={M, incr}; rev={(p - q) * incr}")
            else:
                M, incr = netoperator.get_M_brute(budget, tilderR, tilderS)
                logger.info(
                    f"compute: budget={budget}; scheme=({p},{q}); tilderR=({len(tilderR)}) tilderS=({len(tilderS)}); result={M, incr}; rev={(p - q) * incr}")
            revenue = (p - q) * incr
            netoperator.budget2scheme2result[budget][(p, q)] = (M, incr, revenue)
    netoperator.dump_budget2scheme2result()





if __name__ == "__main__":
    main()

    # grain_prices = {}
    # judge whether a scheme form a sides that computed in history

    # grain_list_p 设置成睡得参数比较合适呢， operator还是main呢， operator吧，
    # 那么就是 每一个