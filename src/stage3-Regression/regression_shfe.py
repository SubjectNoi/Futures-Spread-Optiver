import h5py
import numpy as np
import matplotlib.pyplot as plt

def main():
    f = h5py.File("../../data/shfe/data.h5", "r")
    rb = f["data"][0].flatten()
    hc = f["data"][1].flatten()
    spread = rb - hc
    sp_mean = spread.mean()
    sp_std = spread.std()

    print("range: [{}, {}]".format(sp_mean - sp_std, sp_mean + sp_std))
    # rb = (rb - rb.mean()) / rb.std()
    # hc = (hc - hc.mean()) / hc.std()
    plt.title("Plot for rb and hc")
    plt.xlabel("days")
    plt.ylabel("normed prices")
    x = list(range(rb.shape[0]))
    # plt.plot(x, rb, label="rb")
    # plt.plot(x, hc, label="hc")
    plt.plot(x, spread, label="spread")
    plt.plot(x, np.ones(len(x)) * sp_mean - sp_std, label="lw_bd")
    plt.plot(x, np.ones(len(x)) * sp_mean + sp_std, label="ub_bd")
    plt.legend()
    plt.show()
    founding = 20000
    future_cnt = 0
    for i in range(rb.shape[0]):
        wb = sp_mean - sp_std
        ub = sp_mean + sp_std
        if (spread[i] < wb or spread[i] > ub):
            if (spread[i] < wb):
                # 如果价差过低，买入rb, 卖出hc(founding - rb + hc)
                # p_cnt = founding / abs(spread[i]) // 2
                p_cnt = 1
                founding -= spread[i] * p_cnt
                future_cnt += 1
            if (spread[i] > ub):
                # 如果价差过高，买入hc, 卖出rb(founding + rb - hc)
                # p_cnt = future_cnt // 2
                p_cnt = 1
                founding += spread[i] * p_cnt
                future_cnt -= 1
        else:
            #如果回到正常区间，买入所有空头(卖出hc, 买入hb, founding + rb - hc)，卖出所有多头
            founding += spread[i] * future_cnt
            future_cnt = 0
        print("i = {}, founding = {}, future_cnt = {}".format(i, founding, future_cnt))



if __name__ == "__main__":
    main()
