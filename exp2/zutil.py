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
import pickle
import pandas as pd
OBJS = ['I', 'W', 'RI', 'RW']
PKLDIR = '../eplots/pkl'
CSVDIR = '../eplots/csv'
HEAD_schemes =   ['did', 'lamb', 'obj', 'method', 'budget', 'scheme', 'setM', 'I', 'W', 'RI', 'RW'] # 确实是有冗余的
HEAD_optscheme = ['did', 'lamb', 'obj', 'method', 'budget', 'opt_scheme', 'opt_setM_star', 'opt_obj_star']

def mymain():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, allow_abbrev=False)
    add_args_general(parser)
    add_args_zutil(parser)
    args, name2value = parse_args_all(parser)
    # print(args)
    # print(name2value)

    if args.func == 'merge2csv_var':
        merge2csv_var(args.did_list, args.lamb_list, args.obj_list, args.method_list)
    if args.func == 'merge2csv_select':
        merge2csv_select(name2value['-files'])

    if args.func == 'csvopt':
        aggregate_optscheme_optresult(args.did_list, args.lamb_list, args.obj_list, args.method_list, args.budget_list)
    if args.func == 'csvfull':
        aggregate_scheme_result(args.did_list, args.lamb_list, args.obj_list, args.method_list, args.budget_list)
    if args.func == 'csvbr1':
        brute_raw_csv1(args.did_list, args.lamb_list, args.budget_list)
    # if args.func == 'csvbr4':
    #     brute_unifom_csv4(args.did_list, args.lamb_list, args.obj_list, args.budget_list)



    if args.func == 'show2csvs_select':
        show2csvs_select(name2value['-files'])
    if args.func == 'combine2csv_select':
        combine2csv_select(name2value['-files'])

    if args.func == 'clean_old_pkl':
        clean_old_pkl(args.did_list, args.lamb_list, args.obj_list, args.method_list)

    if args.func == 'add_prefix_pkl':
        add_prefix_pkl(args.did_list, args.lamb_list, args.obj_list, args.method_list)

    if args.func == 'detectHeadLines':
        detectHeadLines(name2value['-file'])


def brute_raw_csv1(dl, ll, bl):

    # 哇竟然只需要吧 setM_star 改成 comb, 不对还要去掉obj
    for did in dl:
        for lamb in ll:
            fullrow_list = [HEAD_schemes] ##################
            prefix = f"{did}_{str(int(lamb))}_A_brute"
            pklsrc = get_latest_path(PKLDIR, prefix, '.pkl')
            print(pklsrc)
            if pklsrc != None:
                budget2scheme2comb2result = pickle.load(open(pklsrc, 'rb'))
                print(budget2scheme2comb2result.keys())
                if bl ==None:
                    bl = budget2scheme2comb2result.keys()
                for budget in bl:
                    scheme2comb2result = budget2scheme2comb2result[budget]
                    for scheme, comb2result in scheme2comb2result.items():
                        for comb, result in comb2result.items():
                            fullrow_list.append([did, lamb, 'A', 'brute', budget, scheme, comb, *result])

            data = pd.DataFrame(fullrow_list)
            prefix_out = f"br1_{did}_{str(int(lamb))}_A_brute"
            data.to_csv(f"{CSVDIR}/{prefix_out}.csv", index=False, header=False, sep='\t')


def aggregate_scheme_result(dl, ll, ol,  ml, bl):
    """
    budgets2optscheme2optresult
    :return:
    :rtype:
    """
    for did in dl:
        for lamb in ll:
            for obj in ol:
                csvnote = f"full_{did}_{str(int(lamb))}_{obj}_{'+'.join(ml)}_{'+'.join([str(b) for b in bl])}"
                row_list = [HEAD_schemes]
                for method in ml:
                    pklnote = f"{did}_{str(int(lamb))}_{obj}_{method}"
                    pklsrc = get_latest_path(PKLDIR, pklnote, 'pkl')
                    if pklsrc == None:
                        row_list.append(row_list.append([did, lamb, obj, method, None, None, None, None, None, None, None]))
                        continue
                    budget2scheme2optsolution = pickle.load(open(pklsrc, 'rb'))
                    # for budget, scheme2optsolution in budget2scheme2optsolution:
                    for budget in bl:
                        if budget not in budget2scheme2optsolution.keys():
                            # for scheme
                            row_list.append([did, lamb, obj, method, budget, None, None, None, None, None, None])
                            continue
                        scheme2optsolution = budget2scheme2optsolution[budget]
                        for scheme, optsolution in scheme2optsolution.items():
                            # print(scheme, optsolution)
                            row_list.append([did, lamb, obj, method, budget, scheme, optsolution[0], optsolution[1],
                                             round(optsolution[2], 2), round(optsolution[3], 2), round(optsolution[4], 2)])

                df = pd.DataFrame(row_list)
                csv = f'{CSVDIR}/{csvnote}.csv'
                print(csv)
                df.to_csv(csv, index=False, header=False, sep='\t')

def aggregate_optscheme_optresult(dl, ll, ol,  ml, bl):
    """
    budgets2optscheme2optresult
    :return:
    :rtype:
    """
    for did in dl:
        for lamb in ll:
            for obj in ol:
                csvnote = f"opt_{did}_{str(int(lamb))}_{obj}_{'+'.join(ml)}_{'+'.join([str(b) for b in bl])}"
                row_list = [HEAD_schemes]
                for method in ml:
                    pklnote = f"{did}_{str(int(lamb))}_{obj}_{method}"
                    pklsrc = get_latest_path(PKLDIR, pklnote, 'pkl')
                    if pklsrc == None:
                        for budget in bl:
                            row_list.append([did, lamb, obj, method, budget, None, None, None])
                        continue
                    budget2scheme2optsolusion = pickle.load(open(pklsrc, 'rb'))
                    # for budget, scheme2optsolution in budget2scheme2optsolution:
                    for budget in bl:
                        if budget not in budget2scheme2optsolusion.keys():
                            row_list.append([did, lamb, obj, method, budget, None, None, None])
                            continue
                        scheme2optsolusion = budget2scheme2optsolusion[budget]
                        sorted_scheme2optsolusion = sorted(scheme2optsolusion.items(), key=lambda kv: kv[1][OBJS.index(obj) + 1], reverse=True)
                        opt_scheme = sorted_scheme2optsolusion[0][0]
                        optsolusion = sorted_scheme2optsolusion[0][1]
                        # opt_setM_star, objI, objW, objRI, objRW = sorted_scheme2optsolusion[0][1]
                        # opt_obj_star = round(sorted_scheme2optsolusion[0][1][OBJS.index(obj) + 1], 2)
                        row_list.append([did, lamb, obj, method, budget, opt_scheme, *optsolusion])
                df = pd.DataFrame(row_list)
                csv = f'{CSVDIR}/{csvnote}.csv'
                print(csv)
                df.to_csv(csv,  index=False, header=False, sep='\t')


def show2csvs_select(files):
    """

    :param files:
    :type files:
    :return:
    :rtype:
    """
    head = ['did', 'lamb', 'obj', 'method', 'budget', 'scheme', 'setM_star', 'I', 'W', 'RI', 'RW']
    filename_list = files.split('\n')
    if '' in filename_list:
        filename_list.remove('')
    print(filename_list)
    for file in filename_list:
        row_list = [head]
        src = f"{PKLDIR}/{file}"
        print(file.split('_'))
        did, lamb, obj, method = file.split('_')[1:5] if file.split('_')[0] == '' else file.split('_')[0:4]
        budget2scheme2optsolution = pickle.load(open(src, 'rb'))
        for budget, scheme2optsolution in budget2scheme2optsolution.items():
            print(budget)
            for scheme, result in scheme2optsolution.items():
                print(scheme, result)
                # setM_star, I, W, RI, RW = result
                row = [did, lamb, obj, method, budget, scheme, *result]
                row_list.append(row)
        data = pd.DataFrame(row_list)
        nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
        csvname = f"{CSVDIR}/{file.replace('.pkl', '.csv')}"
        data.to_csv(csvname, index=False, header=False, sep='\t')



def get_latest_path(dir, prefix, suffix):
    result_filename_list = []
    for filename in os.listdir(dir):
        if prefix in filename and suffix in filename:
            result_filename_list.append(filename)
    result_filename_list.sort()
    print(result_filename_list)
    if len(result_filename_list) > 0:
        return f"{dir}/{result_filename_list[-1]}"
    return None



def clean_old_pkl(did_list, lamb_list, obj_list, method_list):
    for did in did_list:
        for lamb in lamb_list:
            for method in method_list:
                for obj in obj_list: # A 还没有处理
                    prefix = f"{did}_{str(int(lamb))}_{obj}_{method}"
                    pklsrc = get_latest_path(PKLDIR, prefix, 'pkl')
                    for filename in os.listdir(PKLDIR):
                        if filename not in pklsrc:
                            os.remove(f"{PKLDIR}/{filename}")

def get_variable_name(var_org):
    """The var name of variable passed in (only work if unique value)
    """

    for item in sys._getframe(2).f_locals.items():
        if var_org is item[1]:
            return item[0]


def cmd(logger, command, simulation=0):
    """wrap subprocess
    """

    if logger:
        logger.info('Subprocess: \"' + command + '\"')
    else:
        print('Subprocess: \"' + command + '\"')
    if simulation == 0:
        subprocess.run(command, shell=True)


def head_dict(logger, d, head_n):
    """Preview n items of a dict
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
    """

    nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
    logger = logging.getLogger(logname)  # 设定logger的名字
    logger.setLevel(logging.INFO)  # 设定logger得等级
    ch = logging.StreamHandler()  # 输出流的hander，用与设定logger的各种信息
    ch.setLevel(logging.INFO)  # 设定输出hander的level
    logname = f"../elogs/{nowTime}_{logname}.log"
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




def plot_dist_hist(samples, bins, fig_name):
    """plot and save a hist fig under elogs/
    """
    plt.clf()
    plt.hist(samples, bins=bins)
    plt.savefig(f"../elogs/{fig_name}.pdf", dpi=300, bbox_inches="tight", format='pdf')
    plt.clf()


def detectHeadLines(filename):
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



def rename(did='d1', lamb_list=[1,2,3], obj_list=['I', 'W', 'RI', 'RW'], method_list=['h1','greedy','brute']):
    dir = "../eplots/pkl";
    for lamb in lamb_list:
        for obj in obj_list:
            for method in method_list:
                core = f"{did}_{lamb}_{obj}_{method}"
                print(core)


def add_args_zutil(parser):
    parser.add_argument('-f', "--func", metavar='', help="Function to call.")

def parse_args_all(parser):
    knownargs, unk = parser.parse_known_args()
    para_name_list = [x  for x in unk if '-' in x ]

    name2value = {}
    para_name = None
    para_value_list = []
    for elem in unk:
        if elem in para_name_list:
            # 先把上一个参数倒空, 如果没有上一个的话跳过, 那意味着最后一个没有被轮到
            if para_name:
                name2value[para_name] = para_value_list[0] if len(para_value_list)==1 else para_value_list
            para_name = elem
            para_value_list.clear()
        if elem not in para_name_list:
            para_value_list.append(elem)
    name2value[para_name] = para_value_list[0] if len(para_value_list)==1 else para_value_list
    # print(name2value)

    return knownargs, name2value




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

if __name__ == '__main__':
    mymain()





def combine2csv_select(files):
    """
    思考一下这个方法的使用场景
    """
    dir_path = '../eplots/pkl/'
    head = ['did', 'lamb', 'obj', 'method', 'budget', 'scheme', 'setM_star', 'I', 'W', 'RI', 'RW']
    row_list = [head]

    filename_list = files.split('\n')
    if '' in filename_list:
        filename_list.remove('')
    for file in filename_list:
        src = f"{dir_path}{file}"
        did, lamb, obj, method = file.split('_')[1:5] if file.split('_')[0] == '' else file.split('_')[0:4]
        budget2scheme2optsolution = pickle.load(open(src, 'rb'))
        for budget, scheme2optsolution in budget2scheme2optsolution.items():
            print(budget)
            for scheme, result in scheme2optsolution.items():
                print(scheme, result)
                # setM_star, I, W, RI, RW = result
                row = [did, lamb, obj, method, budget, scheme, *result]
                row_list.append(row)
    data = pd.DataFrame(row_list)
    nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
    data.to_csv(f"../eplots/exp/comb_{nowTime}.csv", index=False, header=False, sep='\t')


def merge2csv_select(files):
    dir_path = '../eplots/pkl/'
    head = ['did', 'lamb', 'obj', 'method', 'budget', 'opt_scheme', 'opt_setM_star', 'opt_obj_star']
    row_list = [head]
    print(files.split('\n'))
    filename_list = files.split('\n')
    for filename in filename_list:
        did, lamb, obj, method = filename.split('_')[1:5]

        src = f"{dir_path}{filename}"
        budget2scheme2optsolution = pickle.load(open(src, 'rb'))
        for budget, scheme2optsolution in budget2scheme2optsolution.items():
            # 从 noperator 的 optprice 方法重载过来的
            sorted_scheme2optsolution = sorted(scheme2optsolution.items(),
                                          key=lambda kv: kv[1][OBJS.index(obj) + 1],
                                          reverse=True)
            opt_scheme = sorted_scheme2optsolution[0][0]
            opt_setM_star, objI, objW, objRI, objRW = sorted_scheme2optsolution[0][1]
            opt_obj_star = round(sorted_scheme2optsolution[0][1][OBJS.index(obj) + 1], 2)

            row = [did, lamb, obj, method, budget, opt_scheme, opt_setM_star, opt_obj_star]
            row_list.append(row)
    data = pd.DataFrame(row_list)
    nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
    data.to_csv(f"../eplots/exp/merge_{nowTime}.csv", index=False, header=False, sep='\t')



def merge2csv_var(did_list, lamb_list, obj_list, method_list):

    info = f"{'+'.join(did_list)}_{'+'.join([str(int(x)) for x in lamb_list])}_{'+'.join(obj_list)}_{'+'.join(method_list)}"
    head = ['did', 'lamb', 'obj', 'method', 'budget', 'opt_scheme', 'opt_setM_star', 'opt_obj_star']
    row_list = [head]
    for did in did_list:
        for lamb in lamb_list:
            for method in method_list:
                for obj in obj_list:
                    # pklsrc = get_latest_path()
                    result_pkl_path_list = [d for d in os.listdir(dir_path) if
                                            f"{did}_{str(int(lamb))}_{obj}_{method}" in d and '.pkl' in d]
                    result_pkl_path_list.sort()
                    if len(result_pkl_path_list) > 0:
                        src = f"{dir_path}{result_pkl_path_list[0]}"
                        budget2scheme2optsolution = pickle.load(open(src, 'rb'))
                        for budget, scheme2optsolution in budget2scheme2optsolution.items():
                            # 从 noperator 的 optprice 方法重载过来的
                            sorted_scheme2optsolution = sorted(scheme2optsolution.items(),
                                                          key=lambda kv: kv[1][OBJS.index(obj) + 1],
                                                          reverse=True)
                            opt_scheme = sorted_scheme2optsolution[0][0]
                            opt_setM_star, objI, objW, objRI, objRW = sorted_scheme2optsolution[0][1]
                            opt_obj_star = round(sorted_scheme2optsolution[0][1][OBJS.index(obj) + 1], 2)

                            row = [did, lamb, obj, method, budget, opt_scheme, opt_setM_star, opt_obj_star]
                            row_list.append(row)
    data = pd.DataFrame(row_list)
    nowTime = datetime.datetime.now().strftime("%m%d%H%M%S")
    data.to_csv(f"../eplots/exp/merge_{info}.csv", index=False, header=False, sep='\t')






def add_prefix_pkl(did_list, lamb_list, obj_list, method_list):
    """
    The args can be the same as algo, to veryfy the result of the latest run.
    To delete the predix:  clean_old_pkl 应该会在带_开头的文件里面去清楚旧的
    """
    dir_path = '../eplots/pkl/'
    if len(did_list)<1:  # 没有参数的时候就全都改名
        for d in os.listdir(dir_path):
            new_name = '_' + d
            src = f"{dir_path}{d}"
            trg = f"{dir_path}{new_name}"
            print(f"rename from {src} to {trg}")
            os.rename(src, trg)
    for did in did_list:
        for lamb in lamb_list:
            for method in method_list:
                for obj in obj_list:
                    result_pkl_path_list = [d for d in os.listdir(dir_path) if
                                            f"{did}_{str(int(lamb))}_{obj}_{method}" in d and '.pkl' in d]
                    result_pkl_path_list.sort()
                    if len(result_pkl_path_list) > 0:
                        new_name = '_' + result_pkl_path_list[0]
                        src = f"{dir_path}{result_pkl_path_list[0]}"
                        trg = f"{dir_path}{new_name}"
                        print(f"rename from {src} to {trg}")
                        os.rename(src, trg)

def brute_unifom_csv4(dl, ll, ol, bl):
    # 不对, 这个方法是分成4个pkl才算是统一
    # 分成四个csv还是放在algo里面吧

    for did in dl:
        for lamb in ll:
            prefix = f"{did}_{str(int(lamb))}_A_brute"
            pklsrc = get_latest_path(PKLDIR, prefix, '.pkl')
            if pklsrc != None:
                budget2scheme2comb2result = pickle.load(open(pklsrc, 'rb'))
                if bl ==None:
                    bl = budget2scheme2comb2result.keys()
                for obj in ol:
                    row_list = [HEAD_schemes] ##################
                    for budget in bl:
                        scheme2comb2result = budget2scheme2comb2result[budget]
                        # for scheme, comb2result in scheme2comb2result.items():
                        scheme2optresult = {}
                        for scheme, comb2result in scheme2comb2result.items():
                            sorted_comb2obj = sorted(comb2result.items(), key=lambda kv: kv[1][OBJS.index(obj)], reverse=True)
                            scheme2optresult[scheme] = (sorted_comb2obj[0][0], *sorted_comb2obj[0][1])
                            row_list.append([did, lamb, obj, 'brute', budget, scheme, sorted_comb2obj[0][0],
                                             sorted_comb2obj[0][1][0], round(sorted_comb2obj[0][1][1], 2),
                                             round(sorted_comb2obj[0][1][2], 2), round(sorted_comb2obj[0][1][3], 2)])
                    data = pd.DataFrame(row_list)
                    prefix_out = f"br4_{did}_{str(int(lamb))}_{obj}_brute"
                    data.to_csv(f"{CSVDIR}/{prefix_out}.csv", index=False, header=False, sep='\t')



# if method == 'brute':
#     pklnote = f"{did}_{str(int(lamb))}_A_{method}"
#     pklsrc = get_latest_path(PKLDIR, pklnote, 'pkl')
#     if pklsrc == None:
#         for budget in bl:
#             row_list.append([did, lamb, obj, method, budget, None, None, None])
#         continue
#     budget2scheme2comb2result = pickle.load(open(pklsrc, 'rb'))
#     # for budget, scheme2comb2result in budget2scheme2comb2result.items():
#     for budget in bl:
#         if budget not in budget2scheme2comb2result.keys():
#             row_list.append([did, lamb, obj, method, budget, None, None, None])
#             continue
#         scheme2comb2result = budget2scheme2comb2result[budget]
#         scheme2optresult = {}
#         for scheme, comb2result in scheme2comb2result.items():
#             sorted_comb2obj = sorted(comb2result.items(), key=lambda kv: kv[1][OBJS.index(obj)], reverse=True)
#             scheme2optresult[scheme] = (sorted_comb2obj[0][0], *sorted_comb2obj[0][1])
#         sorted_scheme2optresult = sorted(scheme2optresult.items(), key=lambda kv: kv[1][OBJS.index(obj) + 1], reverse=True)
#         opt_scheme = sorted_scheme2optresult[0][0]
#         opt_setM_star= sorted_scheme2optresult[0][1][0]
#         opt_obj_star = round(sorted_scheme2optresult[0][1][OBJS.index(obj) + 1], 2)
#         row_list.append([did, lamb, obj, method, budget, opt_scheme, opt_setM_star, opt_obj_star])
# else:
