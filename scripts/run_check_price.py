from autotools.core.get_message import run
from pathlib import Path



if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    csv_file = base_dir/'autotools'/"resources"/'target_csv.csv'
    run(csv_file)