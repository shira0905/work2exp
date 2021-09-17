#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/9/2 20:38
@Desc    :
'''
import argparse
import datetime
import logging
import subprocess
import sys
import matplotlib.pyplot as plt


def get_variable_name(var_org):
    """The var name of variable passed in (only work if unique value)

    :param var_org: the variable to get name from
    :type var_org:
    :return: the var name of parameter
    :rtype:
    """

    for item in sys._getframe(2).f_locals.items():
        if var_org is item[1]:
            return item[0]


def cmd(logger, command, simulation=0):
    """wrap subprocess

    :param logger: if no None then print stdout
    :type logger:
    :param command: the command line to execute
    :type command:
    :param simulation: log but not execute if 1; log and execute default 0
    :type simulation:
    :return:
    :rtype: None
    """

    if logger:
        logger.info('Subprocess: \"' + command + '\"')
    else:
        print('Subprocess: \"' + command + '\"')
    if simulation == 0:
        subprocess.run(command, shell=True)


def head_dict(logger, d, head_n):
    """Preview n items of a dict

    :param logger: if no None then print stdout
    :type logger:
    :param d: the dict to view
    :type d:
    :param head_n: how many key-value pairs to view
    :type head_n:
    :return:
    :rtype: None
    """
    s = ''
    for i, (k, v) in enumerate(d.items()):
        s += '\n' + str(k) + ': ' + str(v)
        if i == head_n - 1:
            break
    if logger:
        logger.info(f"top {head_n} items of {get_variable_name(dict)} : {s}")
    else:
        print(f"top {head_n} items of {get_variable_name(dict)} : {s}")


def get_log(did, method, version):
    """Custom a logger,  return the name of the log file

    :param did:
    :type did:
    :return: logger, logname
    :rtype:
    """

    nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
    logger = logging.getLogger(did)  # 设定logger的名字
    logger.setLevel(logging.INFO)  # 设定logger得等级
    ch = logging.StreamHandler()  # 输出流的hander，用与设定logger的各种信息
    ch.setLevel(logging.INFO)  # 设定输出hander的level
    logname = f"../elogs/{did}_{method}_{nowTime}.log"
    fh = logging.FileHandler(logname, mode='a')  # 文件流的hander，输出得文件名称，以及mode设置为覆盖模式
    fh.setLevel(logging.INFO)  # 设定文件hander得lever
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)  # 两个hander设置个是，输出得信息包括，时间，信息得等级，以及message
    fh.setFormatter(formatter)
    logger.addHandler(fh)  # 将两个hander添加到我们声明的logger中去
    logger.addHandler(ch)
    var = logger.name
    print(var)
    return logger, logname


def get_parser():
    parser = argparse.ArgumentParser()
    # usually fixed =================================================
    parser.add_argument(
        "--version", "-v", metavar='\b', default=f'v{datetime.datetime.now().strftime("%m%d%H%M")}',
        help="The version of experiment, note  folder ../elogsv"
    )
    parser.add_argument(
        "--seed", '-s', metavar='\b', default='32', help="the seed to random valuation and cost"
    )
    parser.add_argument(
        "--did", '-d', metavar='\b', default='d1', help="data_id choose from d1,d2,d3,d4"
    )
    parser.add_argument(
        "--beta_paras", metavar='\b', default='3,6,6,3', help="Beta paras from which draw valuations and costs v1,v2,c1,c2"
    )
    parser.add_argument(
        "--a", '-a', metavar='\b', default='2', help="the para of valuation function"
    )

    parser.add_argument(
        "--percent_R", '-pr', metavar='\b', default='0.25', help="the percentage of candidate R"
    )
    parser.add_argument(
        "--percent_S", '-ps', metavar='\b', default='0.25', help="the percentage of candidate S"
    )

    # the parameters to study =================================================
    parser.add_argument(
        "--budget_list", '-bl', metavar='\b', default='0', help="the budget of links to add"
    )
    # parser.add_argument(
    #     "--grain_list_pq", '-glpq', metavar='\b', default='10,10', help="the budget of links to add"
    # )
    # parser.add_argument(
    #     "--grain_list_p", '-glp', metavar='\b', default='10', help="divide p into such invervals"
    # )
    # parser.add_argument(
    #     "--grain_list_q", '-glq', metavar='\b', default='10', help="divide q into such invervals"
    # )
    parser.add_argument(
        "--grain_p", '-gp', metavar='\b', default='10', help="divide p into such invervals"
    )
    parser.add_argument(
        "--grain_alpha", '-ga', metavar='\b', default='10', help="divide alpha into such invervals"
    )

    # parser.add_argument(
    #     "--rewards_proportion", '-alpha', metavar='\b', default='0.6', help="the proportion share to suppliers"
    # )


    # methods to use =================================================
    parser.add_argument(
        "--method", '-m', metavar='\b', default='', help="the method to use, {greedy, brute, h1, h2}"
    )
    # parser.add_argument(
    #     "--do_brute", default=False, action="store_true", help="Whether to do_brute."
    # )
    # parser.add_argument(
    #     "--do_greedy", default=False, action="store_true", help="Whether to do_greedy."
    # )
    # parser.add_argument(
    #     "--do_h1", default=False, action="store_true", help="Whether to do_h1."
    # )
    # parser.add_argument(
    #     "--do_h2", default=False, action="store_true", help="Whether to do_h2."
    # )
    return parser


def plot_dist_hist(samples, bins, fig_name):
    """plot and save a hist fig under elogs/

    :param samples:
    :type samples:
    :param bins:
    :type bins:
    :param fig_name: elogs/{fig_name}.pdf
    :type fig_name:
    :return: generate a fig under elogs
    :rtype: None
    """
    plt.clf()
    plt.hist(samples, bins=bins)
    plt.savefig(f"../elogs/{fig_name}.pdf", dpi=300, bbox_inches="tight", format='pdf')
    plt.clf()
#
#
# def plot_dist_pdf(v_beta_paras, c_beta_paras, data_name):
#     x = np.linspace(0, 1, 1002)[1:-1]
#     alpha_beta_value_list = [v_beta_paras, c_beta_paras]
#     listname = ["valuations", "costs"]
#     plt.clf()
#     for i, alpha_beta_value in enumerate(alpha_beta_value_list):
#         dist = beta(alpha_beta_value[0], alpha_beta_value[1])
#         dist_y = dist.pdf(x)
#         plt.plot(x, dist_y,
#                  label=r'$\alpha=%.1f,\ \beta=%.1f$ ,%s' % (alpha_beta_value[0], alpha_beta_value[1], listname[i]))
#     plt.xlim(0, 1)
#     plt.ylim(0, 2.5)
#     plt.legend()
#     plt.savefig(f"../elogs/hist_{data_name}_pdf.pdf", dpi=300, bbox_inches="tight", format='pdf')
#     plt.clf()


# if __name__ == '__main__':
