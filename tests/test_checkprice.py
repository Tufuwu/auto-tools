from autotools.core.get_message import get_fund_real_time_estimation
import pandas as pd
from pathlib import Path

def run(csv_file, base_dir):
    df = pd.read_csv(csv_file, dtype={'number': str})

    save_path = Path(base_dir) / 'autotools' / 'resources' / 'message.txt'
    save_path.parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as f:
        for index, row in df.iterrows():
            fund_name = row['name']
            fund_number = row['number']

            fund_info, fund_hold, data_time = get_fund_real_time_estimation(fund_number)

            # 构造一行可读日志
            line = (
                f"{fund_info or fund_name}, "
                f"{fund_hold}, "
                f"{data_time}\n"
            )

            print(line.strip())
            f.write(line)


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    csv_file = base_dir/'autotools'/"resources"/'target_csv.csv'
    run(csv_file,base_dir)