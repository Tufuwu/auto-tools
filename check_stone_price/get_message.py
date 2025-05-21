import requests
from bs4 import BeautifulSoup

def get_fund_info(fund_code):
    url = f"https://fund.eastmoney.com/{fund_code}.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        soup = BeautifulSoup(response.text, 'html.parser')

     
        # 获取基金名称
        fund_name = soup.find("div", class_="fpoptableWrap").get_text(strip=True)
        return  fund_name
        # 获取单位净值、日增长率
        data_item = soup.find("dl", class_="dataItem02")
        net_value = data_item.find("dd", class_="dataNums").find("span").get_text(strip=True)  # 单位净值
        daily_change = data_item.find("dd", class_="dataNums").find_all("span")[1].get_text(strip=True)  # 日增长率

        # 获取基金规模、成立日期等信息
        info_items = soup.find("div", class_="infoOfFund").find_all("td")
        fund_size = info_items[0].get_text(strip=True).replace("基金规模：", "")  # 基金规模
        established_date = info_items[2].get_text(strip=True).replace("成立日期：", "")  # 成立日期

        return {
            "基金代码": fund_code,
            "基金名称": fund_name,
            "单位净值": net_value,
            "日增长率": daily_change,
            "基金规模": fund_size,
            "成立日期": established_date,
        }

    except Exception as e:
        print(f"获取基金信息失败: {e}")
        return None

if __name__ == "__main__":
    fund_code = "014143"  # 替换成你想查询的基金代码
    fund_info = get_fund_info(fund_code)

    print(fund_info)
    if fund_info:
        for key, value in fund_info.items():
            print(f"{key}: {value}")