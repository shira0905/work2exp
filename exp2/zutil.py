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
import os
import re

def clean_old_files():
    dir_path_list = {'../eplots/pkl10/', '../eplots/pkl20/', '../eplots/pkl30/' }

    did_lit = ['d1', 'd2', 'd4']
    method_list = ['brute', 'greedy', 'h1']
    obj_list = ['rev', 'sw']

    for dir_path in dir_path_list:
        for did in did_lit:
            for method in method_list:
                for obj in obj_list:
                    result_pkl_path_list = [d for d in os.listdir(dir_path) if
                                            f"{did}_{method}_{obj}" in d and '.pkl' in d]
                    result_pkl_path_list.sort()
                    if len(result_pkl_path_list) > 0:
                        for f in result_pkl_path_list[:-1]:
                            os.remove(f"{dir_path}{f}")
                            print(f"os.remove({dir_path}{f})")


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


def get_log(logname):
    """Custom a logger,  return the name of the log file

    :param did:
    :type did:
    :return: logger, logname
    :rtype:
    """

    nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
    logger = logging.getLogger(logname)  # 设定logger的名字
    logger.setLevel(logging.INFO)  # 设定logger得等级
    ch = logging.StreamHandler()  # 输出流的hander，用与设定logger的各种信息
    ch.setLevel(logging.INFO)  # 设定输出hander的level
    logname = f"../elogs/{logname}_{nowTime}.log"
    fh = logging.FileHandler(logname, mode='a')  # 文件流的hander，输出得文件名称，以及mode设置为覆盖模式
    fh.setLevel(logging.INFO)  # 设定文件hander得lever
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)  # 两个hander设置个是，输出得信息包括，时间，信息得等级，以及message
    fh.setFormatter(formatter)
    logger.addHandler(fh)  # 将两个hander添加到我们声明的logger中去
    logger.addHandler(ch)
    var = logger.name
    print(logname)
    return logger


def get_parser(parser):
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
        "--gamma", '-gamma', metavar='\b', default='2', help="the para of valuation function"
    )

    parser.add_argument(
        "--percent_R", '-pr', metavar='\b', default='0.25', help="Fixed currently, the percentage of candidate R"
    )
    parser.add_argument(
        "--percent_S", '-ps', metavar='\b', default='0.25', help="the percentage of candidate S"
    )

    # the parameters to study =================================================
    parser.add_argument(
        "--budget_list", '-bl', metavar='\b', default='0', help="the budget of links to add"
    )
    parser.add_argument(
        "--grain_p", '-gp', metavar='\b', default='10', help="divide p into such invervals"
    )
    parser.add_argument(
        "--grain_alpha", '-ga', metavar='\b', default='10', help="divide alpha into such invervals"
    )
    # methods to use =================================================
    parser.add_argument(
        "--method", '-m', metavar='\b', default='', help="the method to use, {greedy, brute, h1, h2}"
    )
    parser.add_argument(
        "--rev", default=False, action="store_true", help="Whether take revenue as obj, for plot and main."
    )
    parser.add_argument(
        "--sw", default=False, action="store_true", help="Whether take social welfare as obj, for plot and main."
    )
    parser.add_argument(
        "--stat", default=False, action="store_true", help="Whether plot statistics of graph, for plot."
    )
    parser.add_argument(
        "--extract", default=False, action="store_true", help="Whether xxx for plot."
    )

    # return parser


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


def detectHeadLines(filename):
    '''detact headline and return inserted string.

    params:
        f: Markdown file
    '''
    # remove the existing span tags
    f = open(filename, 'r', encoding='utf-8')
    text = ''
    clean = re.compile('<.*?>')
    for line in f.readlines():
        if '#head' not in line:
            if 'span' in line:
                line = re.sub(clean, '', line)
            text += line
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

    # add new tag
    f = open(filename, 'r', encoding='utf-8')
    headline_dic = {'#': 0, '##': 1, '###': 2, '####': 3, '#####': 4, '######': 5}
    suojin = {0: -1, 1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1}

    f.seek(0)

    insert_str = ""
    org_str = ""

    last_status = -1
    c_status = -1

    headline_counter = 0
    iscode = False
    for line in f.readlines():
        if (line[:3] == '```'):
            iscode = not iscode

        # fix code indent bug and fix other indentation bug. 2020/7/3
        if not iscode:
            temp_line = line.strip(' ')
        ls = temp_line.split(' ')
        if len(ls) > 1 and ls[0] in headline_dic.keys() and not iscode:
            headline_counter += 1
            c_status = headline_dic[ls[0]]
            # find first rank headline
            if last_status == -1 or c_status == 0 or suojin[c_status] == 0:
                # init suojin
                for key in suojin.keys():
                    suojin[key] = -1
                suojin[c_status] = 0
            elif c_status > last_status:
                suojin[c_status] = suojin[last_status] + 1

            # update headline text
            headtext = ' '.join(ls[1:-1])
            if ls[-1][-1] == '\n':
                headtext += (' ' + ls[-1][:-1])
            else:
                headtext += (' ' + ls[-1])
            headid = '{}{}'.format('head', headline_counter)
            headline = ls[0] + ' <span id=\"{}\"'.format(headid) + '>' + headtext + '</span>' + '\n'
            org_str += headline

            jump_str = '- [{}](#{}{})'.format(headtext, 'head', headline_counter)
            insert_str += ('\t' * suojin[c_status] + jump_str + '\n')

            last_status = c_status
        else:
            org_str += line

    insert_str = insert_str + org_str
    f.close()

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(insert_str)

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
