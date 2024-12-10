import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv("C:/Users/mukunoki/Desktop/heatmap_another/psychopy_data_csv/202110011-001_csv/data13_shikuukann_2.csv")  # "path_to_your_file.csv" をCSVファイルのパスに置き換えてください

# 特定の列の最大値を取得してプリント
max_value = df["GazePointX"].max()
print("GazePointYの最大値:", max_value)
