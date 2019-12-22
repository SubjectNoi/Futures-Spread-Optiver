import os
import math

import h5py
import numpy as np

import sys
sys.path.append('..')
#from src.utils.trading_framework import Context
from utils.trading_framework import Context


def do_policy(context, rb, hc, train_ratio, bulin_coeff,out_img_name):
    spread = rb - hc
    train_len = int(len(spread) * train_ratio)
    sp_mean = spread[:train_len].mean()
    sp_std = spread[:train_len].std()
    lower_bound = sp_mean - bulin_coeff * sp_std
    upper_bound = sp_mean + bulin_coeff * sp_std
    print("range: [{}, {}]".format(lower_bound, upper_bound))
    for i in range(context.length):
        price_rb = context.get_current_price(0)
        price_hc = context.get_current_price(1)
        spread = price_rb - price_hc
        print("i = {}, spread = {}".format(i, spread))
        if (spread < lower_bound):
            # 如果价差过低，买入rb, 卖出hc
            lot = math.floor(abs(context.cash) * 0.3 / (price_rb + price_hc))
            context.buy_open(0, lot)
            context.sell_open(1, lot)
        elif (spread > upper_bound):
            # 如果价差过低，买入rb, 卖出hc
            lot = math.floor(abs(context.cash) * 0.3 / (price_rb + price_hc))
            context.buy_open(1, lot)
            context.sell_open(0, lot)
        else:
            # 如果回到正常区间则进行平仓，买入所有空头，卖出所有多头
            if context.future_cnt[0] > 0:
                context.buy_close(0)
                context.sell_close(1)
            elif context.future_cnt[0] < 0:
                context.buy_close(1)
                context.sell_close(0)
        context.move_to_next()
    context.stat(out_img_name)
    context.split_trade()
    r_0, r_1 = context.cal_return()
    context.annulized_return()
    print('-----annulized return -----')
    for i in range(len(context.a_return)):
        print(context.a_return[i], end='\n')
    context.sharpe_ratio()
    sharpe_r = context.sharpe_ratio()
    print('-----sharpe ratio-----')
    print(sharpe_r)


def bld_policy(context, lower_bound, upper_bound):
    print("range: [{}, {}]".format(lower_bound, upper_bound))
    for i in range(context.length):
        price_rb = context.get_current_price(0)
        price_hc = context.get_current_price(1)
        spread = price_rb - price_hc
        print("i = {}, spread = {}".format(i, spread))
        if (spread < lower_bound):
            # 如果价差过低，买入rb, 卖出hc
            lot = math.floor(abs(context.cash) * 0.3 / (price_rb + price_hc))
            context.buy_open(0, lot)
            context.sell_open(1, lot)
        elif (spread > upper_bound):
            # 如果价差过低，买入rb, 卖出hc
            lot = math.floor(abs(context.cash) * 0.3 / (price_rb + price_hc))
            context.buy_open(1, lot)
            context.sell_open(0, lot)
        else:
            # 如果回到正常区间则进行平仓，买入所有空头，卖出所有多头
            if context.future_cnt[0] > 0:
                context.buy_close(0)
                context.sell_close(1)
            elif context.future_cnt[0] < 0:
                context.buy_close(1)
                context.sell_close(0)
        context.move_to_next()
    context.stat()


def data_loader(path):
    date = []
    with open(os.path.join(path, "date.txt"), "r") as f:
        for line in f:
            date.append(line[:-1])
    f = h5py.File(os.path.join(path, "data.h5"), "r")
    rb = f["data"][0].flatten()
    hc = f["data"][1].flatten()
    return date, rb, hc


def lower_bound_func(data_list, target):
    for i in range(len(data_list)):
        if data_list[i] >= target:
            return i
    return -1


def upper_bound_func(data_list, target):
    for i in range(len(data_list)):
        if data_list[i] > target:
            return i
    return -1


def experiment(begin_date, end_date, start_founding, policy_idx, bulin_coeff,out_img_name):
    abs_path = os.path.abspath(__file__)
    data_dir=abs_path.split(os.path.sep)[0:-3]
    data_dir.extend(["data","shfe"])
    data_dir=os.path.sep.join(data_dir)
    date, rb, hc = data_loader(data_dir)
    idx_begin = lower_bound_func(date, begin_date)
    idx_end = upper_bound_func(date, end_date)
    if idx_begin == -1:
        print("begin date not valid!")
    if idx_end == -1:
        print("end date not valid!")
    print("trading date from {} to {}".format(date[idx_begin], date[idx_end - 1]))
    rb_valid = rb[idx_begin:idx_end]
    hc_valid = hc[idx_begin:idx_end]
    date_valid = date[idx_begin:idx_end]
    context = Context(start_founding, rb_valid, hc_valid, date_valid)
    if policy_idx == 0:
        do_policy(context, rb, hc, 0.5, bulin_coeff,out_img_name)


if __name__ =='__main__':
    experiment("20170105", "20181227", 2000000, 0, 2)
