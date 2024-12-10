import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from tqdm import tqdm

# CSVファイルを読み込む
df = pd.read_csv("C:/Users/mukunoki/Desktop/heatmap_another/data/001_01_202110011.csv")
df = df.dropna(axis=0)  
# GazePointX, GazePointY を読み込む
x = df['GazePointX'].values
y = df['GazePointY'].values

# データの準備
value = np.vstack([x, y])
kernel = gaussian_kde(value)

# ヒートマップのグリッドを作成
xx, yy = np.mgrid[0:x.max():100j, 0:y.max():100j]
positions = np.vstack([xx.ravel(), yy.ravel()])

# tqdmを使用して処理の進行状況を表示
f = np.zeros(positions.shape[1])
for i in tqdm(range(positions.shape[1])):
    f[i] = kernel(positions[:, i])
f = np.reshape(f, xx.shape)

# ヒートマップを描画
fig = plt.figure()
ax = fig.add_subplot(111)
ax.contourf(xx, yy, f, cmap='Greys')  # カラーマップを白黒の濃淡に変更

# アスペクト比を'equal'に設定
ax.set_aspect('equal')

# タイトル、軸のラベル、軸の目盛りを非表示にする
ax.set_title('')
ax.set_xlabel('')
ax.set_ylabel('')
ax.set_xticks([])
ax.set_yticks([])

# y軸の表示を反転
ax.invert_yaxis()

# ヒートマップを高解像度のPNGファイルとして保存
plt.savefig("C:/Users/mukunoki/Desktop/heatmap_another/psychopy_data_csv_heatmap_another/output1.png", dpi=1000, bbox_inches="tight")

# ヒートマップを表示
plt.show()
