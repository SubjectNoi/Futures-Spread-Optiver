import h5py
import numpy as np
import matplotlib.pyplot as plt
import math


class Context(object):
    def __init__(self, start_founding, prices_0, prices_1):
        self.start_founding = start_founding
        self.founding = start_founding
        assert len(prices_0) == len(prices_1)
        self.length = len(prices_0)
        # 维护价格序列
        self.prices = [prices_0, prices_1]
        # 维护当前持仓量
        self.future_cnt = np.zeros(2)
        # 记录手续费总数
        self.fee_sum = 0
        # 记录交易开仓累计总量
        self.trade_cnt = 0
        # 记录交易次数
        self.trade_frequency = 0
        # 记录卖空保证金
        self.sell_deposit = 0
        # 记录买入保证金
        self.buy_deposit = 0
        self.total_interest_list = []
        self.idx = 0

    def get_price(self, item_num, idx):
        price = self.prices[item_num][idx]
        return price

    def get_current_price(self, item_num):
        price = self.prices[item_num][self.idx]
        return price

    def sell_open(self, item_num, lot):
        self.future_cnt[item_num] -= lot
        price = self.prices[item_num][self.idx]
        self.founding += price * lot
        fee = price * lot * 0.00004
        self.fee_sum += fee
        self.founding -= fee
        deposit = price * lot * 0.08
        self.sell_deposit += deposit
        self.founding -= deposit
        self.trade_cnt += lot
        self.trade_frequency += 1

    def sell_close(self, item_num):
        price = self.prices[item_num][self.idx]
        if self.future_cnt[item_num] < 0:
            lot = abs(self.future_cnt[item_num])
            self.future_cnt[item_num] = 0
            self.founding -= price * lot
            fee = price * lot * 0.00004
            self.fee_sum += fee
            self.founding -= fee
            self.founding += self.sell_deposit
            self.sell_deposit = 0
            self.trade_frequency += 1

    def buy_open(self, item_num, lot):
        self.future_cnt[item_num] += lot
        price = self.prices[item_num][self.idx]
        self.founding -= price * lot
        fee = price * lot * 0.00004
        self.fee_sum += fee
        self.founding -= fee
        deposit = price * lot * 0.08
        self.buy_deposit += deposit
        self.founding -= deposit
        self.trade_cnt += lot
        self.trade_frequency += 1

    def buy_close(self, item_num):
        price = self.prices[item_num][self.idx]
        if self.future_cnt[item_num] > 0:
            lot = self.future_cnt[item_num]
            self.future_cnt[item_num] = 0
            self.founding += price * lot
            fee = price * lot * 0.00004
            self.fee_sum += fee
            self.founding -= fee
            self.founding += self.buy_deposit
            self.buy_deposit = 0
            self.trade_frequency += 1

    def move_to_next(self):
        print("idx = {}, founding = {}, future_cnt = {}".format(self.idx, self.founding, self.future_cnt))
        self.total_interest_list.append((self.founding / self.start_founding) * 100 - 100)
        self.idx += 1
        if (self.idx > self.length):
            raise Exception("run over length!")

    def stat(self):
        print("sum of fee = ", self.fee_sum)
        print("interest ratio ", (self.founding / self.start_founding) * 100 - 100)
        print("sum of trade ", self.trade_cnt)
        print("frequency of trade ", self.trade_frequency)
        plt.title("total interest")
        plt.xlabel("days")
        plt.ylabel("total interest till now")
        x = list(range(self.length))
        plt.plot(x, self.total_interest_list, label="line")
        # plt.plot(x, np.ones(len(x)) * sp_mean - 2 * sp_std, label="lw_bd")
        # plt.plot(x, np.ones(len(x)) * sp_mean + 2 * sp_std, label="ub_bd")
        plt.legend()
        plt.show()



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




