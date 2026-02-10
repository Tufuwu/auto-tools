import requests
import re
import json
import math
import time
import csv 

def fetch_one_page(fund_code, page_index=1, page_size=20, start_date="", end_date=""):
    url = "https://api.fund.eastmoney.com/f10/lsjz"
    callback = f"jQuery1830{int(time.time()*1000)}_{int(time.time()*1000)}"
    params = {
        "callback": callback,
        "fundCode": fund_code,
        "pageIndex": page_index,
        "pageSize": page_size,
        "startDate": start_date,
        "endDate": end_date,
        "_": int(time.time()*1000)
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
        "Referer": f"https://fundf10.eastmoney.com/jjjz_{fund_code}.html"
    }
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    text = resp.text
    # 提取 JSON 部分
    m = re.search(r"^[^(]*\((.*)\);?$", text)
    if not m:
        raise ValueError("无法从返回内容提取 JSON 部分： " + text)
    json_str = m.group(1)
    data = json.loads(json_str)
    return data

def fetch_all(fund_code, page_size=20):
    # 先请求第一页，拿 totalcount，算出总页数
    first = fetch_one_page(fund_code, page_index=1, page_size=page_size)
    # “Data” 字段里可能有总条数
    total_count = first.get("Data", {}).get("TotalCount", 0)
    if total_count is None:
        total_count = 0
    total_pages = math.ceil(total_count / page_size) if total_count > 0 else 1

    all_list = []
    # 把第一页的内容加入
    lsjz1 = first.get("Data", {}).get("LSJZList", [])
    all_list.extend(lsjz1)

    # 以后每一页都请求
    for p in range(2, 24):
        try:
            d = fetch_one_page(fund_code, page_index=p, page_size=page_size)
            ls = d.get("Data", {}).get("LSJZList", [])
            all_list.extend(ls)
            time.sleep(0.5)  # 加点延时，防止被封
        except Exception as e:
            print(f"页 {p} 请求失败：", e)
            break
    return all_list

def write_file_in(csv_file,new_data):
        # 打开CSV文件并进行操作
    with open(csv_file, mode='a', newline='', encoding='utf-8',errors='ignore') as file:
        # 创建一个CSV写入器
        writer = csv.DictWriter(file, fieldnames=new_data.keys())

        # 如果文件是空的（或者是首次写入），就写入表头
        if file.tell() == 0:
            writer.writeheader()

        # 写入新的数据行
        writer.writerow(new_data)

    print(f'已将新数据添加到 {csv_file}')

if __name__ == "__main__":
    fund_code = "019504"
    data_list = fetch_all(fund_code, page_size=100)
    # 打印几条看看
    for item in data_list:
        print(item)
        file_path = "D:/vscode/3/auto-tools/date_price.csv"
        write_file_in(file_path,item)
    print("总条目：", len(data_list))