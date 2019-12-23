import h5py
import math
from trading_framework import Context


def do_policy(context, lower_bound, upper_bound):
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

def policy(context, lower, upper, pred_diff):
    # lower_bound = -20
    # upper_bound = 250
    rate = 0.1
    for i in range(context.length):
        price_rb = context.get_current_price(0)
        price_hc = context.get_current_price(1)
        spread = -pred_diff[i]
        lower_bound = rate * lower[i]
        upper_bound = rate * upper[i]
        print("i = {}, spread = {}, price_rb = {}, price_hc = {}, lower_bound = {}, upper_bound = {}".format(i, spread, price_rb, price_hc, lower_bound, upper_bound))
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

def main():
    f = h5py.File("../../data/shfe/data.h5", "r")
    rb = f["data"][0].flatten()
    hc = f["data"][1].flatten()
    spread = rb - hc
    train_len = int(len(spread) * 0.5)
    sp_mean = spread[:train_len].mean()
    sp_std = spread[:train_len].std()
    rb_valid = rb[train_len:]
    hc_valid = hc[train_len:]
    context = Context(2000000, rb_valid, hc_valid)
    lower_bound = sp_mean - 2 * sp_std
    upper_bound = sp_mean + 2 * sp_std
    do_policy(context, lower_bound, upper_bound)
    # f = open("FeedingContext.txt")
    # data = f.readlines()
    # hc, rb, pred_diff, lower, upper = [], [], [], [], []
    # for i in data:
        # tmp = i.split(',')
        # hc.append(float(tmp[1]))
        # rb.append(float(tmp[2]))
        # pred_diff.append(-float(tmp[4]))
        # lower.append(-float(tmp[6]))
        # upper.append(-float(tmp[5]))
    # assert len(hc) == len(rb) == len(pred_diff) == len(lower) == len(upper), "Length mis match"
    # length = len(hc)
    # train_len = int(length * 0.5)
    # hc_valid = hc[train_len:]
    # rb_valid = rb[train_len:]
    # lower_valid = lower[train_len:]
    # upper_valid = upper[train_len:]
    # pred_diff_valid = pred_diff[train_len:]
    # context = Context(2000000, rb_valid, hc_valid)
    # policy(context, lower_valid, upper_valid, pred_diff_valid)


if __name__ =='__main__':
    main()
