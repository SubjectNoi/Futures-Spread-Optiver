import numpy as np
import matplotlib.pyplot as plt


class Context(object):
    def __init__(self, start_founding, prices_0, prices_1, trade_date):
        self.start_founding = start_founding
        # 维护可用现金量
        self.cash = self.start_founding
        # 资本 = 现金 + 期货0价格 * 期货0持仓 + 期货1价格 * 期货1持仓
        self.founding = start_founding
        assert len(prices_0) == len(prices_1)
        self.length = len(prices_0)
        # 交易日期序列
        self.trade_date = trade_date
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
        # 记录成交量
        self.total_amount_list = []
        self.today_amount = 0
        self.idx = 0
        #log trade for calculate
        self.trade_log_open = []
        self.trade_log_close = []
        self.trade0_open = []
        self.trade0_close = []
        self.trade1_open = []
        self.trade1_close = []
        #single order return
        self.return_0 = []
        self.return_1 = []
        #single array for cal
        self.return0 = []
        self.return1 = []
        #annulized return
        self.a_return =[]

    def get_price(self, item_num, idx):
        price = self.prices[item_num][idx]
        return price

    def get_current_price(self, item_num):
        price = self.prices[item_num][self.idx]
        return price

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
        self.today_amount = lot
        self.trade_log_open.append([self.idx, item_num, price, lot, 0])

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
            self.today_amount = -lot
            self.trade_log_close.append([self.idx, item_num, price, lot, 1])

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
        self.today_amount = -lot
        self.trade_log_open.append([self.idx, item_num, price, lot, 1])

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
            self.today_amount = lot
            self.trade_log_close.append([self.idx, item_num, price, lot, 0])

    def move_to_next(self):
        value0 = self.future_cnt[0] * self.prices[0][self.idx]
        value1 = self.future_cnt[1] * self.prices[1][self.idx]
        self.founding = self.cash + value0 + value1
        print("idx = {}, founding = {}, cash = {}, future_cnt = {}".format(self.idx, self.founding, self.cash, self.future_cnt))
        self.total_interest_list.append((self.founding / self.start_founding) * 100 - 100)
        self.total_amount_list.append(self.today_amount)
        self.today_amount = 0
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

        plt.title("total amount list")
        plt.xlabel("days")
        plt.ylabel("total amount")
        plt.bar(x, self.total_amount_list, label="amount")
        plt.legend()
        plt.show()

    
    def split_trade(self):
        for i in range(len(self.trade_log_open)):
            if self.trade_log_open[i][1] is 0:
                self.trade0_open.append(self.trade_log_open[i])
            else:
                self.trade1_open.append(self.trade_log_open[i])
        for i in range(len(self.trade_log_close)):
            if self.trade_log_close[i][1] is 0:
                self.trade0_close.append(self.trade_log_close[i])
            else:
                self.trade1_close.append(self.trade_log_close[i])

    def cal_return(self):
        day = 0
        j = 0
        for i in range(len(self.trade0_close)):
            while day < self.trade0_close[i][0]:
                #if at the day time, there is open trade
                if day is self.trade0_open[j][0]:
                    #which buy and which sell
                    #if buy 0
                    if self.trade0_open[j][4] is 0:
                        # 0 return
                        r = (self.trade0_close[i][2] - self.trade0_open[j][2]) / self.trade0_open[j][2]
                        self.return_0.append([self.trade0_open[j][0], self.trade0_open[j][3], r, \
                                self.trade0_close[i][0] - self.trade0_open[j][0]])
                        self.return0.append(r)
                        # 1 return
                        r = (self.trade1_open[j][2] - self.trade0_close[i][2]) / self.trade0_open[j][2]
                        self.return_1.append([self.trade1_open[j][0], self.trade1_open[j][3], r, \
                                self.trade1_close[i][0] - self.trade1_open[j][0]])
                        self.return1.append(r)
                    #if buy 1 sell 0
                    else:
                        # 0 return
                        r = (self.trade0_open[j][2] - self.trade0_close[i][2]) / self.trade0_open[j][2]
                        self.return_0.append([self.trade0_open[j][0], self.trade0_open[j][3], r, \
                                self.trade0_close[i][0] - self.trade0_open[j][0]])
                        self.return0.append(r)
                        # 1 return
                        r = (self.trade1_close[i][2] - self.trade0_open[j][2]) / self.trade0_open[j][2]
                        self.return_1.append([self.trade1_open[j][0], self.trade1_open[j][3], r, \
                                self.trade1_close[i][0] - self.trade1_open[j][0]])
                        self.return1.append(r)
                    j = j + 1
                    day = day + 1
                else:
                    day = day + 1
        return self.return0, self.return1

    def annulized_return(self):
        for i in range(len(self.return_0)):
            self.a_return.append(self.return_0[i][2] * (250/self.return_0[i][3]))
            self.a_return.append(self.return_1[i][2] * (250/self.return_1[i][3]))

    def sharpe_ratio(self):
        r = np.array(self.a_return)
        r_m = np.mean(r)
        r_std = np.std(r)
        sharpe_r = r_m / r_std
        return sharpe_r





