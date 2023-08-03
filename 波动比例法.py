import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


def read_data(path):
    '''
    :param path: file_path; 存有n years螺纹钢主连的收盘价等数据
    :return: DataFrame
    时间      最高价(元)    最低价(元)     收盘价(元)
    ...         ...          ...         ...
    ...         ...          ...         ...

    '''
    source_df = pd.read_excel(path)
    df = source_df[["时间", "最高价(元)", "最低价(元)", "收盘价(元)"]]
    return df


def ATR(df, n):
    '''
    :param df:
    时间      最高价(元)    最低价(元)     收盘价(元)
    ...         ...          ...         ...
    ...         ...          ...         ...
    :param path: 存有n years螺纹钢主连的收盘价等数据
    :param n: # days of True Ranges we need
    :return:
    时间      开盘价(元)     收盘价(元)
    ...         ...          ...
    ...         ...          ...

    '''
    pmax = df["最高价(元)"]
    pmin = df["最低价(元)"]
    pclose = df["收盘价(元)"]
    atr = (pmax[0] - pmin[0]) * np.ones(len(df))

    for i in range(1, len(df)):
        if (pmax[i] < pclose[i - 1]):
            atr[i] = pclose[i - 1] - pmin[i]
        elif (pmin[i] > pclose[i - 1]):
            atr[i] = pmax[i] - pclose[i - 1]
        else:
            atr[i] = pmax[i] - pmin[i]

    # Average true range
    for i in range(n - 1, len(atr)):
        atr[i] = sum(atr[i - n + 1:i + 1]) / n

    return atr


def backtest_df(df, C, atr, vol, vp, guarantee):
    '''
    :param df: DataFrame
    时间      最高价(元)    最低价(元)     收盘价(元)
    ...         ...          ...         ...
    ...         ...          ...         ...

    :param C: int; 初始资金
    :param atr: List; Averate True Range
    :param vol: float; 能够接受的最大波动比例
    :param vp: int; 每个点的对应价格
    :param guarantee: float; 保证金比例
    :return: DataFrame
        时间      收盘价(元)      contract_number     Total_asset     Used_asset
        ...         ...             ...                 ...             ...
        ...         ...             ...                 ...             ...
    '''

    con_num1 = int((C * vol) / (atr[0] * vp))  # 合约数 at day1

    total_asset = C * np.ones(len(df))  # 总资金
    ave_asset = C * np.ones(len(df))  # 30天平均资金
    con_num = con_num1 * np.ones(len(df))  # 合约数
    used_asset = (con_num1 * 10 *
                  df["收盘价(元)"][0] * guarantee / C) * np.ones(len(df))  # 占用资金 at day1
    lever_ratio = (con_num1 * 10 *
                   df["收盘价(元)"][0] / C) * np.ones(len(df))  # 杠杆率 at day1

    for index in range(1, len(df)):
        # Total asset
        total = con_num[index - 1] * 10 * (df["收盘价(元)"][index] - df["收盘价(元)"][index - 1])
        total_asset[index] = total_asset[index - 1] + total

        con_num[index] = int((total_asset[index] * vol) / (atr[index] * vp))
        used_asset[index] = (100) * con_num[index] * 10 * df["收盘价(元)"][index] * guarantee / total_asset[index]
        lever_ratio[index] = con_num[index] * 10 * df["收盘价(元)"][index] / total_asset[index]

    df["contract_number"] = con_num
    df["Total_asset"] = total_asset
    df["Used_asset(%)"] = used_asset
    df["Lever_ratio"] = lever_ratio

    return df


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
    # path = "/Users/yuwensun/Documents/实习/申港资管投资部23Summer/资管方法及其应用/螺纹钢主力连续（近10年）.xlsx"
    path = "/Users/yuwensun/Documents/实习/申港资管投资部23Summer/资管方法及其应用/螺纹钢主连(09-23).xlsx"

    df = read_data(path)  # DataFrame contains 日期and收盘价

    # 交易参数设置
    C = 100000  # 初始资金
    atr_days = 50 # ATR对应的天数
    atr = ATR(df, atr_days)
    vol = 0.02  # 可接受的最大波动比例
    vp = 10  # 每个点的对应价格
    guarantee = 0.16  # 保证金比例

    final_df = backtest_df(df, C, atr, vol, vp, guarantee)
    total_asset_plot(final_df["时间"], final_df["Total_asset"], C)

    print(final_df)