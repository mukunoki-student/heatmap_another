import cv2
import numpy as np
from tqdm import tqdm
import pandas as pd

df = pd.read_csv("C:/Users/mukunoki/Desktop/heatmap/psychopy_data_csv/202110011-001_csv/data01_shikuukann_1.csv")

df = df.dropna(axis=0)  # NaN を含む列を削除


def GaussianMask(sizex, sizey, sigma=33, center=None, fix=1):
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

if __name__ == '__main__':
    img = cv2.imread("C:/Users/mukunoki/Desktop/heatmap/images_resized/img_1.jpg")
    H, W, _ = img.shape

    fix_arr = df[['GazePointX', 'GazePointY']].values
    fix_arr -= fix_arr.min()
    fix_arr/=fix_arr.max()
    fix_arr[:, 0] *= W
    fix_arr[:, 1] *= H

# fix_arrの最初の3行を抜き出す
first_three_rows = fix_arr[:10]

# 結果を表示
print(first_three_rows)
#print(fix_arr.max())

#df.iloc
#fix_arr

