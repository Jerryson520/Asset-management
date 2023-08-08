#Import Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Example:固定分数法
# Data Loader
def read_data(path):
    '''
    :param path: 存有5 years螺纹钢主连的收盘价等数据
    :return:
    日期      收盘价(元)
    ...         ...
    ...         ...
    '''
    source_df = pd.read_excel(path)
    df = source_df[["时间", "收盘价(元)"]]
    return df


# Trade results
def backtest_df(df, C, f, loss_limit, guarantee):
    '''
    :param df:
        日期      收盘价(元)
        ...         ...
        ...         ...
    :param C: 初始资金
    :param loss_limit: 每份合约允许的最大亏损额
    :param guarantee: 保证金比例
    :return:
        日期      收盘价(元)      contract_number     Total_asset     Used_asset
        ...         ...             ...                 ...             ...
        ...         ...             ...                 ...             ...
    '''
    con_num1 = int(C * f / loss_limit)  # 合约数 at day1

    total_asset = C * np.ones(len(df))  # 总资金 at day1
    ave_asset = C * np.ones(len(df))  # 30天平均资金
    con_num = con_num1 * np.ones(len(df))  # 合约数 at day1
    used_asset = (con_num1 * 10 *
                  df["收盘价(元)"][0] * guarantee / C) * np.ones(len(df))  # 占用资金 at day1
    lever_ratio = (con_num1 * 10 *
                   df["收盘价(元)"][0] / C) * np.ones(len(df))  # 杠杆率 at day1

    for index in range(1, len(df)):
        # Total asset
        total = con_num[index - 1] * 10 * (df["收盘价(元)"][index] - df["收盘价(元)"][index - 1])
        total_asset[index] = total_asset[index - 1] + total

        '''
        Below is added section: Equity curve trading
        '''
        # Average total asset
        if (index >= 30-1):
            ave_asset[index] = total_asset[index - 29:index + 1].mean()
        else:
            ave_asset[index] = total_asset[index]

        # Contract number
        if (ave_asset[index] > total_asset[index]):
            con_num[index] = 0
        else:
            con_num[index] = int(total_asset[index] * f / loss_limit)

        '''
        End section
        '''

        # Used asset
        used_asset[index] = con_num[index] * 10 * df["收盘价(元)"][index] * guarantee / total_asset[index]
        lever_ratio[index] = con_num[index] * 10 * df["收盘价(元)"][index] / total_asset[index]

    df["contract_number"] = con_num
    df["Total_asset"] = total_asset
    df["Used_asset"] = used_asset
    df["Lever_ratio"] = lever_ratio
    df["Average_asset(30days)"] = ave_asset

    return df

# [优化1]
# 计算周期均线（周期=30天），如果资金 < 30天均线，立刻停止交易
#
# Total asset line v.s. 30 average asset line
def total_30ave_plot(df):  # input is dataframe from backtest_df()
    figure, ax = plt.subplots()
    ax.plot(df["时间"], df["Total_asset"], '-.', label="Total_asset")
    ax.plot(df["时间"], df["Average_asset(30days)"], '--', label="Average price (30days)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Asset")
    ax.set_title("Total_asset v.s. Average asset (30days)")

    plt.legend()

    # 自动调整x坐标轴
    plt.gcf().autofmt_xdate()
    # Show the figure
    plt.show()


# Asset plot
def total_asset_plot(x, y, C):
    '''
    :param x: 图像的x值，一般是日期
    :param y: 图像y值，一般是total asset value
    :return: None，因为要画图
    '''
    fig, ax = plt.subplots()
    ax.plot(x, y)
    # 设置其他参数
    ax.set_xlabel("Date")
    ax.set_ylabel("Asset(yuan)")
    ax.set_xticks(x[::90])
    ax.set_title("Total asset when using Fixed Fractional", fontsize=13)

    # 总资产最高点和最低点
    x = x.to_list()
    y = y.to_list()
    ind_max = y.index(max(y))
    ind_min = y.index(min(y))
    max_benefit = (max(y) - C) * 100 / C
    min_benefit = (min(y) - C) * 100 / C
    ax.axhline(C, color="red", linestyle="--")

    ax.text(x[ind_min], y[ind_min], f"Min:{min(y)}, Benefit:{min_benefit}%")
    ax.text(x[ind_max], y[ind_max], f"Max:{max(y)}, Benefit:{max_benefit}%")
    ax.text(x[0], y[0], f"Orginal Asset:{C}")

    # 自动调整x坐标轴
    plt.gcf().autofmt_xdate()
    # Show the figure
    plt.show()

if __name__ == '__main__':
    # path = "/Users/yuwensun/Documents/实习/申港资管投资部23Summer/资管方法及其应用/螺纹钢主力连续（近五年）.xls"
    path = "/Users/yuwensun/Documents/实习/申港资管投资部23Summer/资管方法及其应用/螺纹钢主力连续（近10年）.xlsx"
    df = read_data(path)  # DataFrame contains 日期and收盘价
    # 交易参数设置
    C = 1000000  # 初始资金
    f = 0.1  # 风险比例
    loss_limit = 1250  # 每份合约最大亏损值
    guarantee = 0.16  # 保证金比例

    final_df = backtest_df(df, C, f, loss_limit, guarantee)

    total_30ave_plot(final_df)
    total_asset_plot(final_df["时间"], final_df["Total_asset"], C)

    # print(sum(final_df["contract_number"] == 80.0))
    # print(max(df["contract_number"]))
    # print(df)

