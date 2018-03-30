import ffn
import numpy as np
import pandas as pd
from datetime import datetime
import pickle

from inspect import getmembers, isfunction
import all_strategies

# 計算 MaxDD
def DrawDownAnalysis(cumRet):
    dd_series = ffn.core.to_drawdown_series(cumRet)
    dd_details = ffn.core.drawdown_details(dd_series)
    return dd_details['drawdown'].min(), dd_details['days'].max()


# 利用策略產生的持有部位資訊，計算底下四個指標來判斷投資績效
# sharpe ratio: 判斷報酬的好壞跟穩定度，數值越大越好
# maxdd: maximum drawdown, 最糟糕的狀況會賠幾 %
# maxddd: maximum drawdown duration, 低於上一次最高報酬的天數
# cumRet[-1]: 最後賺的 % 數
def indicators(df):
    dailyRet = df['Close'].pct_change()
    excessRet = (dailyRet - 0.04/252)[df['positions'] == 1]
    SharpeRatio = np.sqrt(252.0)*np.mean(excessRet)/np.std(excessRet)

    cumRet = np.cumprod(1+excessRet)

    maxdd, maxddd = DrawDownAnalysis(cumRet)

    return SharpeRatio, maxdd, maxddd, cumRet[-1]


def apply_strategy(strategy, df):
    return strategy(df)


def utf8conversion(filename):
    with open(filename) as fread:
        data = fread.read()
    with open(filename, 'w', encoding="utf-8") as fwrite:
        fwrite.write(data)


def main():

    # 讀出預先下載好的股價資料
    with open('stockdata', 'rb') as f:
        data = pickle.load(file=f)

    # 計算各支股票的回測結果
    results = []

    strategies = [member[1] for member in getmembers(all_strategies) if isfunction(member[1])]

    for symbol in data:
        for strategy in strategies:
            try:
                apply_strategy(strategy, data[symbol])
                if np.all(data[symbol]['signals']==0):
                    print("Symbol:", symbol, "使用", strategy.__name__, "策略沒有出現買賣訊號。")
                    continue
                SharpeRatio, maxdd, maxddd, finalRet = indicators(data[symbol])
                days = (data[symbol].index[-1] - data[symbol].index[0]).days
                results.append((SharpeRatio, maxdd, maxddd, finalRet, days,
                                data[symbol][data[symbol]['signals'] > 0]['signals'].sum(), symbol, strategy.__name__))
            except Exception as e:
                print("Error occurs at symbol:", symbol, "Strategy:", strategy.__name__, "==>", e.args)


    results_df = pd.DataFrame(results, columns=['sharpe','MaxDrawDown','MaxDrawDownDuration','returns',
                                                'days', 'entries','symbol','strategy'])

    print("\n" * 2)

    print("使用 Maximum Drawdown 排序")
    print("=" * 40)
    print(results_df.sort_values('MaxDrawDown',ascending=False).head())

    print("\n" * 2)

    print("使用 returns 排序")
    print("=" * 40)
    print(results_df.sort_values('returns',ascending=False).head())

    results_df.sort_values('MaxDrawDown',ascending=False).to_html("docs/MaxDrawDown.html")
    results_df.sort_values('returns',ascending=False).to_html("docs/Returns.html")
    results_df.sort_values('sharpe',ascending=False).to_html("docs/Sharpe.html")
    results_df.sort_values('MaxDrawDownDuration',ascending=True).to_html("docs/MaximumDrawDownDuration.html")

    utf8conversion('docs/MaxDrawDown.html')
    utf8conversion('docs/Returns.html')
    utf8conversion('docs/Sharpe.html')
    utf8conversion('docs/MaximumDrawDownDuration.html')

if __name__=="__main__":
    main()
