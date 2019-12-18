import h5py
import numpy as np
import matplotlib.pyplot as plt
import math


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
    spread_valid = rb_valid - hc_valid
    print("range: [{}, {}]".format(sp_mean - 2 * sp_std, sp_mean + 2 * sp_std))
    plt.title("Plot for rb and hc")
    plt.xlabel("days")
    plt.ylabel("normed prices")
    x = list(range(rb_valid.shape[0]))
    # plt.plot(x, rb, label="rb")
    # plt.plot(x, hc, label="hc")
    plt.plot(x, spread_valid, label="spread")
    plt.plot(x, np.ones(len(x)) * sp_mean - 2 * sp_std, label="lw_bd")
    plt.plot(x, np.ones(len(x)) * sp_mean + 2 * sp_std, label="ub_bd")
    plt.legend()
    plt.show()
    start_founding = 2000000
    founding = start_founding
    future_cnt = 0
    fee = 0
    deposit = 0
    sum_trade = 0
    for i in range(spread_valid.shape[0]):
        wb = sp_mean - 2 * sp_std
        ub = sp_mean + 2 * sp_std
        if (spread_valid[i] < wb or spread_valid[i] > ub):
            if (spread_valid[i] < wb):
                # 如果价差过低，买入rb, 卖出hc(founding - rb + hc)
                p_cnt = math.floor(abs(founding) * 0.3 / (rb_valid[i] + hc_valid[i]))
                founding -= spread_valid[i] * p_cnt
                founding -= (rb_valid[i] + hc_valid[i]) * p_cnt * 0.00004 #手续费
                fee += (rb_valid[i] + hc_valid[i]) * p_cnt * 0.00004 #手续费
                deposit += (rb_valid[i] + hc_valid[i]) * p_cnt * 0.08
                founding -= (rb_valid[i] + hc_valid[i]) * p_cnt * 0.08
                future_cnt += p_cnt
                sum_trade += p_cnt
            if (spread_valid[i] > ub):
                # 如果价差过高，买入hc, 卖出rb(founding + rb - hc)
                p_cnt = math.floor(abs(founding) * 0.3 / (rb_valid[i] + hc_valid[i]))
                founding += spread_valid[i] * p_cnt
                founding -= (rb_valid[i] + hc_valid[i]) * p_cnt * 0.00004 #手续费
                fee += (rb_valid[i] + hc_valid[i]) * p_cnt * 0.00004  # 手续费
                deposit += (rb_valid[i] + hc_valid[i]) * p_cnt * 0.08
                founding -= (rb_valid[i] + hc_valid[i]) * p_cnt * 0.08
                future_cnt -= p_cnt
                sum_trade += p_cnt
        else:
            #如果回到正常区间，买入所有空头(卖出hc, 买入hb, founding + rb - hc)，卖出所有多头
            if future_cnt > 0:
                founding += spread_valid[i] * future_cnt
                founding += deposit
                deposit = 0
                founding -= (rb_valid[i] + hc_valid[i]) * p_cnt * 0.00004 #手续费
                fee += (rb_valid[i] + hc_valid[i]) * p_cnt * 0.00004  # 手续费
            elif future_cnt < 0:
                founding -= spread_valid[i] * abs(future_cnt)
                founding += deposit
                deposit = 0
                founding -= (rb_valid[i] + hc_valid[i]) * p_cnt * 0.00004  # 手续费
                fee += (rb_valid[i] + hc_valid[i]) * p_cnt * 0.00004  # 手续费
            future_cnt = 0
        print("i = {}, founding = {}, future_cnt = {}".format(i, founding, future_cnt))
    print("sum of fee = ", fee)
    print("interest ratio ", (founding / start_founding) * 100 - 100)
    print("sum of trade ", sum_trade)

if __name__ == "__main__":
    main()
