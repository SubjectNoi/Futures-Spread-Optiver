import numpy as np
import matplotlib.pyplot as plt


class Context(object):
    def __init__(self, start_founding, prices_0, prices_1):
        self.start_founding = start_founding
        # 维护可用现金量
        self.cash = self.start_founding
        # 资本 = 现金 + 期货0价格 * 期货0持仓 + 期货1价格 * 期货1持仓
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
        fee = price * lot * 0.00004
        self.fee_sum += fee
        self.cash -= fee
        deposit = price * lot * 0.08
        self.sell_deposit += deposit
        self.cash -= deposit
        self.trade_cnt += lot
        self.trade_frequency += 1

    def sell_close(self, item_num):
        price = self.prices[item_num][self.idx]
        if self.future_cnt[item_num] < 0:
            lot = abs(self.future_cnt[item_num])
            self.future_cnt[item_num] = 0
            self.cash += self.sell_deposit * (1/0.08 + 1)
            self.cash -= price * lot
            fee = price * lot * 0.00004
            self.fee_sum += fee
            self.cash -= fee
            self.sell_deposit = 0
            self.trade_frequency += 1

    def buy_open(self, item_num, lot):
        self.future_cnt[item_num] += lot
        price = self.prices[item_num][self.idx]
        fee = price * lot * 0.00004
        self.fee_sum += fee
        self.cash -= fee
        deposit = price * lot * 0.08
        self.buy_deposit += deposit
        self.cash -= deposit
        self.trade_cnt += lot
        self.trade_frequency += 1

    def buy_close(self, item_num):
        price = self.prices[item_num][self.idx]
        if self.future_cnt[item_num] > 0:
            lot = self.future_cnt[item_num]
            self.future_cnt[item_num] = 0
            self.cash -= self.buy_deposit * (1/0.08 - 1)
            self.cash += price * lot
            fee = price * lot * 0.00004
            self.fee_sum += fee
            self.cash -= fee
            self.buy_deposit = 0
            self.trade_frequency += 1

    def move_to_next(self):
        value0 = self.future_cnt[0] * self.prices[0][self.idx]
        value1 = self.future_cnt[1] * self.prices[1][self.idx]
        self.founding = self.cash + value0 + value1
        print("idx = {}, founding = {}, cash = {}, future_cnt = {}".format(self.idx, self.founding, self.cash, self.future_cnt))
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
        plt.legend()
        plt.show()




