import h5py
import math
from src.utils.trading_framework import Context


def do_policy(context, lower_bound, upper_bound):
    print("range: [{}, {}]".format(lower_bound, upper_bound))
    for i in range(context.length):
        price_rb = context.get_current_price(0)
        price_hc = context.get_current_price(1)
        spread = price_rb - price_hc
        print("i = {}, spread = {}".format(i, spread))
        if (spread < lower_bound):
            # 如果价差过低，买入rb, 卖出hc
            lot = math.floor(abs(context.founding) * 0.3 / (price_rb + price_hc))
            context.buy_open(0, lot)
            context.sell_open(1, lot)
        elif (spread > upper_bound):
            # 如果价差过低，买入rb, 卖出hc
            lot = math.floor(abs(context.founding) * 0.3 / (price_rb + price_hc))
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


if __name__ =='__main__':
    main()
