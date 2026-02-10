import pandas as pd
import random

csv_file_path = "D:/vscode/3/auto-tools/temp.csv"
df = pd.read_csv(csv_file_path)

def simulate(x1, x2, x3, x4, df):
    res1 = 0
    res2 = 2000
    money = 0
    number = 0
    flag = -1
    fund = 0
    lend = 0j

    for _, row in df.iterrows():
        nav_str = row["JZZZL"]
        if nav_str > -0.35 and nav_str < 0.35:
            continue

        if nav_str > 0:
            if flag == 1:
                number += 1
            else:
                number = 0
                flag = 1
            money = money * (1 + nav_str / 100) - (nav_str//1) * x1 - x2 * number
            fund += (nav_str//1) * x1 + x2 * number
        else:
            if flag == -1:
                number -= 1
            else:
                number = 0
                flag = -1
            money = money * (1 + nav_str / 100) - (nav_str//1) * x3 - x4 * number
            fund += (nav_str//1) * x3 + x4 * number
            if fund < 0:
                lend += abs(fund)
                fund = 0

        res1 = max(money, res1)
        res2 = min(money, res2)
        #print(fund,'-',money,'-',lend)
    print(res1,'-',res2)
    return (money + fund - lend) / res1 if res1 != 0 else -999999

# 比例优化：x4固定为1
best_score = -999999
best_ratio = None

for _ in range(3000):
    a = random.uniform(0.5, 2.0)  # x1/x4
    b = random.uniform(0.5, 2.0)  # x2/x4
    c = random.uniform(0.5, 2.0)  # x3/x4
    x1 = a
    x2 = b
    x3 = c
    x4 = 1.0

    score = simulate(x1, x2, x3, x4, df)
    if score > best_score:
        best_score = score
        best_ratio = (a, b, c, 1)

    
print(f"✅ 最优比例: x1:x2:x3:x4 = {best_ratio[0]:.2f} : {best_ratio[1]:.2f} : {best_ratio[2]:.2f} : {best_ratio[3]:.2f}")
print(f"最大得分: {best_score}")
