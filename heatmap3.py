import cv2
import numpy as np
from tqdm import tqdm
import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv("C:/Users/mukunoki/Desktop/heatmap_another/psychopy_data_csv/202110011-001_csv_data01_shikuukann_1.csv")
df = df.dropna(axis=0)  # NaN を含む行を削除

def GaussianMask(sizex, sizey, sigma=1, center=None, fix=1):
    x = np.arange(0, sizex, 1, float)
    y = np.arange(0, sizey, 1, float)
    x, y = np.meshgrid(x, y)

    if center is None:
        x0 = sizex // 2
        y0 = sizey // 2
    else:
        if not np.isnan(center[0]) and not np.isnan(center[1]):
            x0 = center[0]
            y0 = center[1]
        else:
            return np.zeros((sizey, sizex))

    return fix * np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / sigma ** 2)

def Fixpos2Densemap(fix_arr, width, height, alpha=0.5, threshold=0):
    heatmap = np.zeros((height, width), np.float64)
    for n_subject in tqdm(range(fix_arr.shape[0])):
        heatmap += GaussianMask(width, height, 33, (fix_arr[n_subject, 0], fix_arr[n_subject, 1]))

    # 正規化して 0-255 の範囲にスケーリング
    heatmap = heatmap / np.amax(heatmap)
    heatmap = (heatmap * 255).astype("uint8")

    # 画像処理の部分を削除し、カラーマップを適用したヒートマップのみを返す
    return heatmap
if __name__ == '__main__':
    # 画像のサイズを直接指定
    W, H = 1920, 1080  # 例: 1920x1080

    # fix_arr の正規化やスケーリングを行わない
    fix_arr = df[['GazePointX', 'GazePointY']].values

    heatmap = Fixpos2Densemap(fix_arr, W, H, alpha=0.7, threshold=5)
    cv2.imwrite("C:/Users/mukunoki/Desktop/heatmap_another/psychopy_data_csv_heatmap_another/output1.png", heatmap)