#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Shiyuan
@Contact :   shira0905@gmail.com
@Time    :   2021/9/12 18:16
@Desc    :
'''

import re
from zutil import *
import os

def main():

    proc_temp12()




def proc_temp13(logname):
    # (1) load pkl as dict , but no info of tilder size
    # (2) process log
    cmd(None, f"grep 'load' {logname}", 0)
    textfile = f"../elogs/{logname}_proc.log"
    f = open(textfile, "r")
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回

    result_pkl_path_list = [d for d in os.listdir(f"../elogs") if
                            f"{self.network.did}_{self.method}" in d and 'pkl' in d]
    result_pkl_path_list.sort()
    print(result_pkl_path_list)
    if len(result_pkl_path_list) > 0:
        budget2scheme2result = pickle.load(open(f"../elogs/{result_pkl_path_list[-1]}", 'rb'))


## functions below temp<=12 is before 0913

def proc_temp12():
    # textfile = '../elogs/temp12.log'
    textfile = '../elogs/temp13.log'
    f = open(textfile, "r")
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回
    rev1b_list = []
    rev1g_list = []
    rev2b_list = []
    rev2g_list = []
    rev3b_list = []
    rev3g_list = []
    rev4b_list = []
    rev4g_list = []


    for line in lines:
        parts = line.split('\t')
        # print(parts)
        p = float(parts[0])
        q = float(parts[1])
        # result = []

        inc1b = int(parts[4])
        inc1g = int(parts[7])
        inc2b = int(parts[10])
        inc2g = int(parts[13])
        inc3b = int(parts[16])
        inc3g = int(parts[19])
        inc4b = int(parts[22])
        inc4g = int(parts[25])
        result = [inc1b, inc1g, inc2b, inc2g, inc3b, inc3g, inc4b, inc4g]
        strline = ''
        for i in result:
            rev = i*(p-q)
            strline+= str(rev)+'\t'

        print(strline)
        # print("\t".join(result))
        # rev1b_list.append(int(parts[4]) * (p - q))
        # rev1g_list.append(int(parts[7]) * (p - q))
        # rev2b_list.append(int(parts[10]) * (p - q))
        # rev2g_list.append(int(parts[13]) * (p - q))
        # rev3b_list.append(int(parts[16]) * (p - q))
        # rev3g_list.append(int(parts[19]) * (p - q))
        # rev4b_list.append(int(parts[22]) * (p - q))
        # rev4g_list.append(int(parts[25]) * (p - q))




def proc_temp11():
    # grep 'scheme=' _d1_brute_0913030119.log > temp11.log
    textfile = '../elogs/temp11.log'
    f = open(textfile, "r")
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回


    result_M_list = []
    result_inc_list = []
    print('-----')
    for line in lines:
        schemeAresult = line.split('scheme=')[1]
        scheme_raw = schemeAresult.split('result=')[0]
        result_raw = schemeAresult.split('result=')[1]
        # print(scheme_raw, result_raw)
        p1 = re.compile(r'[(](.*?)[)]', re.S)  # 最小匹配  'abe(ac)ad)'  ['ac']
        p2 = re.compile(r'[(](.*)[)]', re.S)  # 贪婪匹配  'abe(ac)ad)'  ['ac)ad']

        scheme = re.findall(p1, scheme_raw)[0]
        print(f'({scheme})')
        result = re.findall(p2, result_raw)[0]
        # print(result)

        if '),' in result:
            result_inc = result.split('),')[1].strip()
            result_M = result.split('),')[0].replace('(', '')
        elif '},' in result:
            result_inc = result.split('},')[1].strip()
            result_M = result.split('},')[0].replace('{', '')
        # print(result_inc)
        # print(result_M)
        result_M_list.append(result_M)
        result_inc_list.append(result_inc)

    print('-----')
    for M in result_M_list:
        print(M)

    print('-----')
    for result_inc in result_inc_list:
        print(result_inc)
def proc_temp10():
    # grep 'budget=1; scheme=' _d1_greedy_0913043624.log > temp10.log
    textfile = '../elogs/temp10.log'
    f = open(textfile, "r")
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回


    result_M_list = []
    result_inc_list = []
    print('-----')
    for line in lines:
        schemeAresult = line.split('scheme=')[1]
        scheme_raw = schemeAresult.split('result=')[0]
        result_raw = schemeAresult.split('result=')[1]
        # print(scheme_raw, result_raw)
        p1 = re.compile(r'[(](.*?)[)]', re.S)  # 最小匹配  'abe(ac)ad)'  ['ac']
        p2 = re.compile(r'[(](.*)[)]', re.S)  # 贪婪匹配  'abe(ac)ad)'  ['ac)ad']

        scheme = re.findall(p1, scheme_raw)[0]
        print(f'({scheme})')
        result = re.findall(p2, result_raw)[0]
        # print(result)

        if '),' in result:
            result_inc = result.split('),')[1].strip()
            result_M = result.split('),')[0].replace('(', '')
        elif '},' in result:
            result_inc = result.split('},')[1].strip()
            result_M = result.split('},')[0].replace('{', '')
        # print(result_inc)
        # print(result_M)
        result_M_list.append(result_M)
        result_inc_list.append(result_inc)

    print('-----')
    for M in result_M_list:
        print(M)

    print('-----')
    for result_inc in result_inc_list:
        print(result_inc)


def proc_temp9():
    # grep 'result' d1_brute_0913030824.log > temp9.log
    textfile = '../elogs/temp9.log'
    f = open(textfile, "r")
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回

    result_M_list = []
    result_inc_list = []
    print('-----')
    for line in lines:
        schemeAresult = line.split('scheme=')[1]
        scheme_raw = schemeAresult.split('result=')[0]
        result_raw = schemeAresult.split('result=')[1]
        # print(scheme_raw, result_raw)
        p1 = re.compile(r'[(](.*?)[)]', re.S)  # 最小匹配  'abe(ac)ad)'  ['ac']
        p2 = re.compile(r'[(](.*)[)]', re.S)  # 贪婪匹配  'abe(ac)ad)'  ['ac)ad']
        p3 = re.compile(r'[{](.*?)[}]', re.S)
        scheme = re.findall(p1, scheme_raw)[0]
        print(f'({scheme})')
        result = re.findall(p2, result_raw)[0]
        # print(result)

        if '),' in result:
            result_inc = result.split('),')[1].strip()
            result_M = result.split('),')[0].replace('(', '')
        elif '},' in result:
            result_inc = result.split('},')[1].strip()
            result_M = result.split('},')[0].replace('{', '')
        # print(result_inc)
        # print(result_M)
        result_M_list.append(result_M)
        result_inc_list.append(result_inc)

    print('-----')
    for M in result_M_list:
        print(M)

    print('-----')
    for result_inc in result_inc_list:
        print(result_inc)
def proc_temp8():
    # grep 'result' d1_brute_0913023229.log > temp8.log
    textfile = '../elogs/temp8.log'
    f = open(textfile, "r")
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回

    result_M_list = []
    result_inc_list = []
    print('-----')
    for line in lines:
        schemeAresult = line.split('scheme=')[1]
        scheme_raw = schemeAresult.split('result=')[0]
        result_raw = schemeAresult.split('result=')[1]
        # print(scheme_raw, result_raw)
        p1 = re.compile(r'[(](.*?)[)]', re.S)  # 最小匹配  'abe(ac)ad)'  ['ac']
        p2 = re.compile(r'[(](.*)[)]', re.S)  # 贪婪匹配  'abe(ac)ad)'  ['ac)ad']
        p3 = re.compile(r'[{](.*?)[}]', re.S)
        scheme = re.findall(p1, scheme_raw)[0]
        print(f'({scheme})')
        result = re.findall(p2, result_raw)[0]
        # print(result)

        if '),' in result:
            result_inc = result.split('),')[1].strip()
            result_M = result.split('),')[0].replace('(', '')
        elif '},' in result:
            result_inc = result.split('},')[1].strip()
            result_M = result.split('},')[0].replace('{', '')
        # print(result_inc)
        # print(result_M)
        result_M_list.append(result_M)
        result_inc_list.append(result_inc)

    print('-----')
    for M in result_M_list:
        print(M)

    print('-----')
    for result_inc in result_inc_list:
        print(result_inc)


def proc_temp7():
    # grep 'result' _d1_brute_0913021658.log > temp7.log
    textfile = '../elogs/temp7.log'
    f = open(textfile, "r")
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回

    result_M_list = []
    result_inc_list = []
    print('-----')
    for line in lines:
        schemeAresult = line.split('scheme=')[1]
        scheme_raw = schemeAresult.split('result=')[0]
        result_raw = schemeAresult.split('result=')[1]
        # print(scheme_raw, result_raw)
        p1 = re.compile(r'[(](.*?)[)]', re.S)  # 最小匹配  'abe(ac)ad)'  ['ac']
        p2 = re.compile(r'[(](.*)[)]', re.S)  # 贪婪匹配  'abe(ac)ad)'  ['ac)ad']
        p3 = re.compile(r'[{](.*?)[}]', re.S)
        scheme = re.findall(p1, scheme_raw)[0]
        print(f'({scheme})')
        result = re.findall(p2, result_raw)[0]
        # print(result)

        if '),' in result:
            result_inc = result.split('),')[1].strip()
            result_M = result.split('),')[0].replace('(', '')
        elif '},' in result:
            result_inc = result.split('},')[1].strip()
            result_M = result.split('},')[0].replace('{', '')
        # print(result_inc)
        # print(result_M)
        result_M_list.append(result_M)
        result_inc_list.append(result_inc)

    print('-----')
    for M in result_M_list:
        print(M)

    print('-----')
    for result_inc in result_inc_list:
        print(result_inc)



def proc_temp6():
    #  grep 'result' _d1_brute_0912231648.log
    textfile = '../elogs/temp6.log'
    f = open(textfile, "r")
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回

    print('-----')

    for line in lines:
        parts = line.split('result=')
        part = parts[1]
        if 'result=((' in line:
            nums = part.split("), ")
        elif 'result=({' in line:
            nums = part.split("}, ")
        print(nums[0].replace(')', '').replace('(', '').replace('{', '').replace('}', '').strip())

    print('-----')

    for line in lines:
        parts = line.split('result=')
        part = parts[1]
        if 'result=((' in line:
            nums = part.split("), ")
        elif 'result=({' in line:
            nums = part.split("}, ")
        print(nums[1].replace(')', '').replace('(', '').replace('{', '').replace('}', '').strip())




def proc_temp5():
    textfile = '../elogs/temp5.log'
    f = open(textfile, "r")
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回

    print('-----')
    b=3
    for line in lines:
        parts = line.split(', ')
        M = []
        for i in range(4, 1, -1):
            M.append(int(parts[-i].replace('result=(', '').replace(')', '').replace('(', '').replace('{', '').replace('}', '').strip()))
        print(M.__str__().replace('[', '').replace(']', ''))


    print('-----')
    for line in lines:
        parts = line.split(', ')
        target = parts[-1].replace('result=(', '').replace(')', '').replace('(', '').replace('{', '').replace('}', '').strip()
        print(target)



def proc_temp4():
    #  grep 'result:' d1_greedy_0912233302.log
    textfile = '../elogs/temp4.log'
    f = open(textfile, "r")
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回

    print('======')
    for i, line in enumerate(lines):
        if i%2 == 0:
            result = line.split('result: ')[1]
            M = result.split('},')[0].replace('{', '')
            print(M)
    print('======')
    for i, line in enumerate(lines):
        if i%2 == 0:
            result = line.split('result: ')[1]
            inc = result.split('},')[1].strip()
            print(inc)
    print('======')
    for i, line in enumerate(lines):
        if i%2 == 1:
            result = line.split('result: ')[1]
            M = result.split('},')[0].replace('{', '')
            print(M)
    print('======')
    for i, line in enumerate(lines):
        if i%2 == 1:
            result = line.split('result: ')[1]
            inc = result.split('},')[1].strip()
            print(inc)

def proc_temp3():
    textfile = '../elogs/temp3.log'
    f = open(textfile, "r")
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回
    for line in lines:
        parts = line.split(', ')
        for part in parts:
            if 'scheme=' in part:
                target = part.replace(' ', '').replace('scheme=(', '').replace(')', '')
                nums = target.split(',')
                print(nums[0])
    print('-----')
    for line in lines:
        parts = line.split(', ')
        for part in parts:
            if 'scheme=' in part:
                target = part.replace(' ', '').replace('scheme=(', '').replace(')', '')
                nums = target.split(',')
                print(nums[1 ])

    print('-----')
    for line in lines:
        if 'grep' not in line:
            parts = line.split(',')
            # target1 = parts[-3].replace('result=((', '').replace(')', '').replace(' ', '').rstrip()
            target2 = parts[-3].replace('result=((', '').replace(')', '').replace(' ', '').strip()
            print(f'{target2}')



    print('-----')
    for line in lines:
        if 'grep' not in line:
            parts = line.split(',')
            target = parts[-1].replace('result=((', '').replace(')', '').replace(' ', '').strip()
            print(target)

    # print('-----')
    # for line in lines:
    #     parts = line.split(', ')
    #     for part in parts:
    #         if 'result=' in part:
    #             target = part.replace(' ', '').replace('result=((', '').replace(')', '')
    #             nums = target.split(',')
    #             print(nums[1])
    # print('-----')
    # for line in lines:
    #     parts = line.split(', ')
    #     for part in parts:
    #         if 'result=' in part:
    #             target = part.replace(' ', '').replace('result=((', '').replace(')', '')
    #             nums = target.split(',')
    #             print(nums[2])

def proc_temp2():
    textfile = '../elogs/temp2.log'
    f = open(textfile, "r")
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回
    for line in lines:
        parts = line.split(', ')
        for part in parts:
            if 'scheme=' in part:
                target = part.replace(' ', '').replace('scheme=(', '').replace(')', '')
                nums = target.split(',')
                print(nums[0])
    print('======')
    for i, line in enumerate(lines):
        if i%2 == 0:
            result = line.split('result: ')[1]
            M = result.split('},')[0].replace('{', '')
            print(M)
    print('======')
    for i, line in enumerate(lines):
        if i%2 == 0:
            result = line.split('result: ')[1]
            inc = result.split('},')[1].strip()
            print(inc)
    print('======')
    for i, line in enumerate(lines):
        if i%2 == 1:
            result = line.split('result: ')[1]
            M = result.split('},')[0].replace('{', '')
            print(M)
    print('======')
    for i, line in enumerate(lines):
        if i%2 == 1:
            result = line.split('result: ')[1]
            inc = result.split('},')[1].strip()
            print(inc)


def proc_temp1():
    textfile = '../elogs/temp1.log'
    f = open(textfile, "r")
    lines = f.readlines()  # 读取全部内容 ，并以列表方式返回
    for line in lines:
        parts = line.split(', ')
        for part in parts:
            if 'scheme=' in part:
                target = part.replace(' ', '').replace('scheme=(', '').replace(')', '')
                nums = target.split(',')
                print(nums[0])
    print('-----')
    for line in lines:
        parts = line.split(', ')
        for part in parts:
            if 'scheme=' in part:
                target = part.replace(' ', '').replace('scheme=(', '').replace(')', '')
                nums = target.split(',')
                print(nums[1])

    print('-----')
    for line in lines:
        parts = line.split(', ')
        target1 = parts[-3].replace('result=((', '').replace(')', '').replace(' ', '').rstrip()
        target2 = parts[-2].replace('result=((', '').replace(')', '').replace(' ', '').rstrip()
        print(f'{target1}, {target2}')



    print('-----')
    for line in lines:
        parts = line.split(', ')
        target = parts[-1].replace('result=((', '').replace(')', '').replace(' ', '').rstrip()
        print(target)

    # print('-----')
    # for line in lines:
    #     parts = line.split(', ')
    #     for part in parts:
    #         if 'result=' in part:
    #             target = part.replace(' ', '').replace('result=((', '').replace(')', '')
    #             nums = target.split(',')
    #             print(nums[1])
    # print('-----')
    # for line in lines:
    #     parts = line.split(', ')
    #     for part in parts:
    #         if 'result=' in part:
    #             target = part.replace(' ', '').replace('result=((', '').replace(')', '')
    #             nums = target.split(',')
    #             print(nums[2])


if __name__ == '__main__':
    main()
