import yaml
import os
import pandas as pd
import glob

root_dir = "C:/Users/workstation/Downloads/Data_Driven_Stock_Analysis/Data/data"

all_data = []

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.yaml') or file.endswith('.yml'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as yaml_file:
                try:
                    content = yaml.safe_load(yaml_file)
                    if isinstance(content, list):
                        all_data.extend(content)
                    elif isinstance(content, dict):
                        all_data.append(content)
                except yaml.YAMLError as e:
                    print(f"Error reading {file_path}: {e}")

output_dir = 'nifty50'
os.makedirs(output_dir, exist_ok=True)

data = pd.DataFrame(all_data)
for symbol, group_df in data.groupby('Ticker'):
    group_df.to_csv(os.path.join(output_dir, f"{symbol}.csv"), index=False)

print("✅ CSV export complete. Files saved in:", output_dir)

files = glob.glob("C:/Users/workstation/Downloads/Data_Driven_Stock_Analysis/nifty50/*")
merged_csv = pd.concat([pd.read_csv(file, usecols=['Ticker', 'close', 'date', 'high', 'low', 'month', 'open', 'volume']) for file in files])
merged_csv.to_csv("Stock Market Data.csv", index=False)
print(f"{len(files)} csv files merged")