import requests
import pandas as pd
import re
import json

def run(csv_file):
    df = pd.read_csv(csv_file, dtype={'number': str})
    for index, row in df.iterrows():
        fund_name = row['name']
        fund_number = row['number']
        fund_info,fund_hold,data_time = get_fund_real_time_estimation(fund_number)
        print(fund_info,fund_hold,data_time)

def get_fund_real_time_estimation(fund_code):
    url = f"https://fundgz.1234567.com.cn/js/{fund_code}.js"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        raw = response.text

        # 去除回调函数包装，如 jsonpgz({...});
        json_str = raw[raw.index("{") : raw.rindex("}") + 1]
        data = json.loads(json_str)

        return data.get('name'),data.get('gszzl'),data.get('gztime')  # 包含 name、gsz（估算净值）、gztime（估值时间）等字段
    except Exception as e:
        print("实时接口请求失败:", e)
        return None




        