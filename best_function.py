import pandas as pd
from datetime import datetime, timedelta
import pandas as pd


# === 参数设置 ===
HOLD_DAYS = 7  # 最少持有天数
threshold_buy1 = -0.01
threshold_buy2 = -0.02
threshold_sell1 = 0.01
threshold_sell2 = 0.02
buy_ratio_small = 0.3
buy_ratio_large = 0.8
sell_ratio_small = 0.3
sell_ratio_large = 0.8

# 连续上涨/下跌对仓位的放大系数
# 每多连续一天，仓位乘以这个系数
streak_amp = 1.2

# === 输入数据（你也可以从CSV读入）===


rows = []
csv_file_path = "D:/vscode/3/auto-tools/date_price.csv"
df = pd.read_csv(csv_file_path)
for index, row in df.iterrows():
    date_str = row["FSRQ"]
    nav_str = row["DWJZ"]
    rows.append([datetime.strptime(date_str, "%Y/%m/%d").date(), float(nav_str)])

df = pd.DataFrame(rows, columns=["date", "nav"]).sort_values("date").reset_index(drop=True)
df["ret"] = df["nav"].pct_change().fillna(0)

# === 初始化资金状态 ===
cash = 100.0
position_value = 0.0
total_value = 100.0
positions = []  # list of dict: {"buy_date", "buy_price", "amount", "locked_days"}
trades = []

up_streak = 0
down_streak = 0

# === 主循环 ===
for i in range(1, len(df)):
    today = df.loc[i, "date"]
    ret = df.loc[i, "ret"]
    price = df.loc[i, "nav"]

    # 更新 streak
    if ret > 0:
        up_streak += 1
        down_streak = 0
    elif ret < 0:
        down_streak += 1
        up_streak = 0

    # 解锁旧仓位
    for pos in positions:
        pos["locked_days"] += 1

    # --- 卖出逻辑 ---
    sell_positions = []
    if positions and (ret > threshold_sell1 or ret > threshold_sell2):
        for pos in positions:
            if pos["locked_days"] >= HOLD_DAYS:
                sell_ratio = sell_ratio_large if ret > threshold_sell2 else sell_ratio_small
                sell_ratio *= (streak_amp ** (up_streak - 1)) if up_streak > 1 else 1
                sell_amount = pos["amount"] * sell_ratio
                sell_value = sell_amount * price
                pos["amount"] -= sell_amount
                cash += sell_value
                trades.append({
                    "date": today, "type": "SELL", "price": price,
                    "amount": sell_amount, "value": sell_value
                })
        # 移除空仓
        positions = [p for p in positions if p["amount"] > 1e-9]

    # --- 买入逻辑 ---
    if ret < threshold_buy1 or ret < threshold_buy2:
        buy_ratio = buy_ratio_large if ret < threshold_buy2 else buy_ratio_small
        buy_ratio *= (streak_amp ** (down_streak - 1)) if down_streak > 1 else 1
        invest = cash * buy_ratio
        if invest > 0:
            amount = invest / price
            cash -= invest
            positions.append({"buy_date": today, "buy_price": price, "amount": amount, "locked_days": 0})
            trades.append({
                "date": today, "type": "BUY", "price": price,
                "amount": amount, "value": invest
            })

    # 计算每日总价值
    position_value = sum([p["amount"] * price for p in positions])
    total_value = cash + position_value
    df.loc[i, "cash"] = cash
    df.loc[i, "position_value"] = position_value
    df.loc[i, "total_value"] = total_value

# === 输出结果 ===
print("最终总资产：", round(total_value, 4))
print("\n交易记录：")
print(pd.DataFrame(trades))

